"""BigGAN fully unsupervised training 

1) Trainer code
2) Integrating REMAP to big_gan
"""
import torch 
import torch.nn as nn 
import torch.nn.functional as F
import os, sys
import numpy as np
from remap import Remap, l2_norm
from torchnet.meter import AverageValueMeter
from tqdm import tqdm
from torch import autograd


def conv3x3(in_channel, out_channel):  # not change resolusion
    return nn.Conv2d(in_channel, out_channel,
                      kernel_size=3, stride=1, padding=1, dilation=1, bias=False)


def conv1x1(in_channel, out_channel):  # not change resolution
    return nn.Conv2d(in_channel, out_channel,
                      kernel_size=1, stride=1, padding=0, dilation=1, bias=False)


def init_weight(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.orthogonal_(m.weight, gain=1)
        if m.bias is not None:
            m.bias.data.zero_()
            
    elif classname.find('Batch') != -1:
        m.weight.data.normal_(1,0.02)
        m.bias.data.zero_()
    
    elif classname.find('Linear') != -1:
        nn.init.orthogonal_(m.weight, gain=1)
        if m.bias is not None:
            m.bias.data.zero_()
    
    elif classname.find('Embedding') != -1:
        nn.init.orthogonal_(m.weight, gain=1)


class cSEBlock(nn.Module):
    def __init__(self, c, feat):
        super().__init__()
        self.attention_fc = nn.Linear(feat,1, bias=False)
        self.bias = nn.Parameter(torch.zeros((1,c,1), requires_grad=True))
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout2d(0.1)
        
    def forward(self, inputs):
        batch, c, h, w = inputs.size()
        x = inputs.view(batch, c, -1)
        x = self.attention_fc(x) 
        print(x.shape)
        x = x + self.bias
        x = x.view(batch, c, 1, 1)
        x = self.sigmoid(x)
        x = self.dropout(x)
        return inputs * x


class sSEBlock(nn.Module):
    def __init__(self, c, h, w):
        super().__init__()
        self.attention_fc = nn.Linear(c, 1, bias=False).apply(init_weight)
        self.bias = nn.Parameter(torch.zeros((1, h, w, 1), requires_grad=True))
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, inputs):
        batch, c, h, w = inputs.size()
        x = torch.transpose(inputs, 1, 2)  # (*,c,h,w)->(*,h,c,w)
        x = torch.transpose(x, 2, 3)  # (*,h,c,w)->(*,h,w,c)
        x = self.attention_fc(x) + self.bias
        x = torch.transpose(x, 2, 3)  # (*,h,w,1)->(*,h,1,w)
        x = torch.transpose(x, 1, 2)  # (*,h,1,w)->(*,1,h,w)
        x = self.sigmoid(x)
        return inputs * x


class scSEBlock(nn.Module):
    def __init__(self, c, h, w):
        super().__init__()
        self.cSE = cSEBlock(c, h*w)
        self.sSE = sSEBlock(c, h, w)
    
    def forward(self, inputs):
        x1 = self.cSE(inputs)
        x2 = self.sSE(inputs)
        return x1+x2


class Attention(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.channels = channels
        self.theta = nn.utils.spectral_norm(conv1x1(channels, channels//8)).apply(init_weight)
        self.phi = nn.utils.spectral_norm(conv1x1(channels, channels//8)).apply(init_weight)
        self.g = nn.utils.spectral_norm(conv1x1(channels, channels//2)).apply(init_weight)
        self.o = nn.utils.spectral_norm(conv1x1(channels//2, channels)).apply(init_weight)
        self.gamma = nn.Parameter(torch.tensor(0.), requires_grad=True)
        
    def forward(self, inputs):
        batch, c, h, w = inputs.size()
        theta = self.theta(inputs)  # ->(*,c/8,h,w)
        phi = F.max_pool2d(self.phi(inputs), [2,2])  # ->(*,c/8,h/2,w/2)
        g = F.max_pool2d(self.g(inputs), [2,2])  # ->(*,c/2,h/2,w/2)
        
        theta = theta.view(batch, self.channels//8, -1)  # ->(*,c/8,h*w)
        phi = phi.view(batch, self.channels//8, -1)  # ->(*,c/8,h*w/4)
        g = g.view(batch, self.channels//2, -1)  # ->(*,c/2,h*w/4)
        
        beta = F.softmax(torch.bmm(theta.transpose(1,2), phi), -1)  # ->(*,h*w,h*w/4)
        o = self.o(torch.bmm(g, beta.transpose(1,2)).view(batch,self.channels//2,h,w))  # ->(*,c,h,w)
        return self.gamma*o + inputs


class ConditionalNorm(nn.Module):
    def __init__(self, in_channel, n_condition):
        super().__init__()
        self.bn = nn.BatchNorm2d(in_channel, affine=False)  # no learning parameters
        self.embed = nn.Linear(n_condition, in_channel*2)
        
        nn.init.orthogonal_(self.embed.weight.data[:, :in_channel], gain=1)
        self.embed.weight.data[:, in_channel:].zero_()

    def forward(self, inputs, label):
        out = self.bn(inputs)
        embed = self.embed(label.float())
        gamma, beta = embed.chunk(2, dim=1)
        gamma = gamma.unsqueeze(2).unsqueeze(3)
        beta = beta.unsqueeze(2).unsqueeze(3)
        out = gamma * out + beta
        return out


class ResBlock_G(nn.Module):
    def __init__(self, in_channel, out_channel, condition_dim, upsample=True):
        super().__init__()
        self.cbn1 = ConditionalNorm(in_channel, condition_dim)
        self.upsample = nn.Sequential()
        if upsample:
            self.upsample.add_module('upsample', nn.Upsample(scale_factor=2, mode='nearest'))
        self.conv3x3_1 = nn.utils.spectral_norm(conv3x3(in_channel, out_channel)).apply(init_weight)
        self.cbn2 = ConditionalNorm(out_channel, condition_dim)
        self.conv3x3_2 = nn.utils.spectral_norm(conv3x3(out_channel, out_channel)).apply(init_weight)
        self.conv1x1 = nn.utils.spectral_norm(conv1x1(in_channel, out_channel)).apply(init_weight)

    def forward(self, inputs, condition):
        x = F.leaky_relu(self.cbn1(inputs, condition))
        x = self.upsample(x)
        x = self.conv3x3_1(x)
        x = self.conv3x3_2(F.leaky_relu(self.cbn2(x, condition)))
        x += self.conv1x1(self.upsample(inputs))  # shortcut
        return x


class Generator(nn.Module):
    def __init__(self, n_feat, codes_dim):
        super().__init__()
        self.codes_dim = codes_dim
        self.fc = nn.Sequential(
            nn.utils.spectral_norm(nn.Linear(codes_dim, 16 * n_feat * 4 * 4)).apply(init_weight)
        )
        self.res1 = ResBlock_G(16 * n_feat, 16 * n_feat, codes_dim, upsample=True)
        self.res2 = ResBlock_G(16 * n_feat, 8 * n_feat, codes_dim, upsample=True)
        self.res3 = ResBlock_G(8 * n_feat, 4 * n_feat, codes_dim, upsample=True)
        self.attn = Attention(4 * n_feat)
        self.res4 = ResBlock_G(4 * n_feat, 2 * n_feat, codes_dim, upsample=True)
        self.conv = nn.Sequential(
            # nn.BatchNorm2d(2*n_feat).apply(init_weight),
            nn.LeakyReLU(),
            nn.utils.spectral_norm(conv3x3(2 * n_feat, 3)).apply(init_weight),
        )

    def forward(self, z):
        '''
        z.shape = (*,Z_DIM)
        label_ohe.shape = (*,n_classes)
        '''
        batch = z.size(0)
        z = z.squeeze()
        codes = torch.split(z, self.codes_dim, dim=1)

        x = self.fc(codes[0])  # ->(*,16ch*4*4)
        x = x.view(batch, -1, 4, 4)  # ->(*,16ch,4,4)
        x = self.res1(x, codes[1])  # ->(*,16ch,8,8)
        x = self.res2(x, codes[2])  # ->(*,8ch,16,16)

        x = self.res3(x, codes[3])  # ->(*,4ch,32,32)
        x = self.attn(x)  # not change shape

        x = self.res4(x, codes[4])  # ->(*,2ch,64,64)

        x = self.conv(x)  # ->(*,3,64,64)
        x = torch.tanh(x)
        return x


class ResBlock_D(nn.Module):
    def __init__(self, in_channel, out_channel, downsample=True):
        super().__init__()
        self.layer = nn.Sequential(
            nn.LeakyReLU(0.2),
            nn.utils.spectral_norm(conv3x3(in_channel, out_channel)).apply(init_weight),
            nn.LeakyReLU(0.2),
            nn.utils.spectral_norm(conv3x3(out_channel, out_channel)).apply(init_weight),
        )
        self.shortcut = nn.Sequential(
            nn.utils.spectral_norm(conv1x1(in_channel, out_channel)).apply(init_weight),
        )
        if downsample:
            self.layer.add_module('avgpool', nn.AvgPool2d(kernel_size=2, stride=2))
            self.shortcut.add_module('avgpool', nn.AvgPool2d(kernel_size=2, stride=2))

    def forward(self, inputs):
        x = self.layer(inputs)
        x += self.shortcut(inputs)
        return x


class Discriminator(nn.Module):
    def __init__(self, n_feat):
        super().__init__()
        self.res1 = ResBlock_D(3, n_feat, downsample=True)
        self.attn = Attention(n_feat)
        self.res2 = ResBlock_D(n_feat, 2 * n_feat, downsample=True)
        self.res3 = ResBlock_D(2 * n_feat, 4 * n_feat, downsample=True)
        self.res4 = ResBlock_D(4 * n_feat, 8 * n_feat, downsample=True)
        self.res5 = ResBlock_D(8 * n_feat, 16 * n_feat, downsample=False)
        self.fc = nn.utils.spectral_norm(nn.Linear(16 * n_feat, 1)).apply(init_weight)

    def forward(self, inputs):
        batch = inputs.size(0)  # (*,3,64,64)
        h = self.res1(inputs)  # ->(*,ch,32,32)
        h = self.attn(h)  # not change shape
        h = self.res2(h)  # ->(*,2ch,16,16)
        h = self.res3(h)  # ->(*,4ch,8,8)
        h = self.res4(h)  # ->(*,8ch,4,4)
        h = self.res5(h)  # ->(*,16ch,4,4)
        h = torch.sum((F.leaky_relu(h, 0.2)).view(batch, -1, 4 * 4), dim=2)  # GlobalSumPool ->(*,16ch)
        outputs = self.fc(h)  # ->(*,1)
        outputs = torch.sigmoid(outputs)
        return outputs


class Discriminator_Remap(nn.Module):
    def __init__(self, n_feat, img_size=(64, 64), pca_channels=128, n_regions=40, n_layers=2):
        super().__init__()
        self.res1 = ResBlock_D(3, n_feat, downsample=True)
        self.attn = Attention(n_feat)
        self.res2 = ResBlock_D(n_feat, 2*n_feat, downsample=True)
        self.res3 = ResBlock_D(2*n_feat, 4*n_feat, downsample=True)
        self.res4 = ResBlock_D(4*n_feat, 8*n_feat, downsample=True)
        self.res5 = ResBlock_D(8*n_feat, 16*n_feat, downsample=True)
        self.fc = nn.utils.spectral_norm(nn.Linear(16*n_feat, 1)).apply(init_weight)
        self.remap = Remap_decoder(1, [16*n_feat, 8*n_feat, 4*n_feat, 2*n_feat, n_feat][:n_layers], pca_channels,
                                   img_size, n_regions, n_layers)

    def forward(self, inputs):
        batch = inputs.size(0)  # (*,3,64,64)
        x1 = self.res1(inputs)  # ->(*,ch,32,32)
        h = self.attn(x1)  # not change shape
        x2 = self.res2(h)  # ->(*,2ch,16,16)
        x3 = self.res3(x2)  # ->(*,4ch,8,8)
        x4 = self.res4(x3)  # ->(*,8ch,4,4)
        x5 = self.res5(x4)  # ->(*,16ch,2, 2)

        output = [x5, x4, x3, x2, x1]
        output = self.remap(output)
        output = torch.sigmoid(output)
            
        return output


class Remap_decoder(nn.Module):
    def __init__(self, classes, output_channels, pca_channels, img_size, n_regions, n_layers):
        """ Applying remap module as given in the paper 

        classes: number of classes to output
        output_shapes: tuple: list of output shapes 
        encoder_name: str, name of the encoder 
        pca_channels: int, number of channels in the bottleneck layer 
        img_size: tuple, (w, h) width and height of the input image
        """
        super().__init__()

        self.n_regions = n_regions
        self.pca_channels = pca_channels
        self.classes = classes
        self.n_layers = n_layers
        out_shapes = [(img_size[0]//scale, img_size[1]//scale) for scale in [32, 16, 8, 4, 2]][:self.n_layers]
        
        self.in_channels_pca = sum(output_channels[:self.n_layers])
        self.linear_pca = nn.utils.spectral_norm(nn.Linear(self.in_channels_pca, self.pca_channels, bias=True)).apply(init_weight)
        self.remap = Remap(output_channels[:n_layers], out_shapes, self.n_regions)
        self.classifier = nn.Linear(self.pca_channels, self.classes)
    
    def forward(self, x):
        x = x[:self.n_layers]
        output = self.remap(x)
        output = l2_norm(output)
        pca_output = self.linear_pca(output)
        fc = self.classifier(pca_output)
        return fc


class BigGAN:
    def __init__(self, latent_dim, n_featG=2, n_featD=32, channels=3, n_critic=1, beta_1=0, beta_2=0.99,
                 learning_rate=0.001, metrics=[], device=torch.device("cpu"), dataparallel=False, verbose=True):
        self.gen = Generator(n_featG, codes_dim=24)
        self.dis = Discriminator_Remap(n_featD)

        if device == torch.device("cuda"):
            self.gen = self.gen.cuda()
            self.dis = self.dis.cuda()

        if dataparallel:
            self.gen = DataParallel(self.gen)
            self.dis = DataParallel(self.dis)

        self.latent_dim = latent_dim
        self.channels = channels
        self.n_critic = n_critic
        self.device = device
        self.metrics = metrics
        self.verbose = verbose

        self.gen_optim = torch.optim.Adam(self.gen.parameters(), lr=learning_rate, betas=(beta_1, beta_2))
        self.dis_optim = torch.optim.Adam(self.dis.parameters(), lr=learning_rate, betas=(beta_1, beta_2))
        self.loss = self.__setup_loss()

    def __setup_loss(self):
        loss = nn.BCELoss()
        # import pro_gan_pytorch.wgan_loss as losses
        # loss = losses.WganLoss(dis=self.dis)
        return loss

    def optimize_discriminator(self, noise, real_images):
        self.dis_optim.zero_grad()
        real_label = 1
        fake_label = 0

        # train with real
        dis_output = self.dis(real_images)  # dis shape=(*,1)
        batch_size = real_images.size(0)
        dis_labels = torch.full((batch_size, 1), real_label, device=self.device)  # shape=(*,)
        loss_real = self.loss(dis_output, dis_labels)
        loss_real.backward()

        # train with fake
        fake = self.gen(noise)  # output shape=(*,3,64,64)
        # loss_fake = self.loss.dis_loss(real_images, fake)
        dis_output = self.dis(fake.detach())
        dis_labels.fill_(fake_label)
        loss_fake = self.loss(dis_output, dis_labels)
        loss_fake.backward()

        self.dis_optim.step()
        return loss_real.item() + loss_fake.item()
        # return loss_fake.item()

    def optimize_generator(self, noise, real_images):
        batch_size = real_images.size(0)
        real_label = 1
        dis_labels = torch.full((batch_size, 1), real_label, device=self.device)  # shape=(*,)
        dis_labels.fill_(real_label)  # fake labels are real for generator cost
        fake_samples = self.gen(noise)
        # loss = self.loss.gen_loss(fake_samples)
        dis_output = self.dis(fake_samples)
        loss = self.loss(dis_output, dis_labels)
        self.gen_optim.zero_grad()
        loss.backward()
        self.gen_optim.step()

        return loss.item()

    def on_train_start(self):
        self.dis.train()
        self.gen.train()

    def train_batch_update(self, i, x1):
        """
        i : index
        x1: labeled_examples
        """
        gen_input = torch.randn(x1.shape[0], self.latent_dim).to(self.device)
        dis_loss = self.optimize_discriminator(gen_input, x1)

        # Train the generator
        gen_loss = self.optimize_generator(gen_input, x1)

        return dis_loss, gen_loss

    def train_run(self, dataloader):
        self.on_train_start()
        logs = {}
        gen_loss_meter = AverageValueMeter()
        dis_loss_meter = AverageValueMeter()
        metrics_meters = {metric.__name__: AverageValueMeter() for metric in self.metrics}

        with tqdm(dataloader, desc="train", file=sys.stdout, disable=not self.verbose) as iterator:
            i = 0
            for x1 in iterator:
                x1 = x1.to(self.device)
                print(x1.shape)
                gen_loss, dis_loss = self.train_batch_update(i, x1)
                gen_loss_meter.add(gen_loss)
                dis_loss_meter.add(dis_loss)
                loss_logs = {"gen_loss": gen_loss_meter.mean, "dis_loss": dis_loss_meter.mean}
                logs.update(loss_logs)

                metrics_logs = {k: v.mean for k, v in metrics_meters.items()}
                logs.update(metrics_logs)
                i = i + 1

                if self.verbose:
                    s = self._format_logs(logs)
                    iterator.set_postfix_str(s)
        return logs

    def train(self, dataset, epochs, batch_sizes,
              fade_in_percentage, num_samples=16,
              start_depth=0, num_workers=2, feedback_factor=100,
              log_dir="", sample_dir="", save_dir="",
              checkpoint_factor=1, start_epoch=0):

        from DataTools import get_data_loader
        dataloader = get_data_loader(dataset, batch_size=batch_sizes, num_workers=num_workers)

        #  writing losses to the log file
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "losses.log")
        for i in range(start_epoch, epochs):
            print('\nEpoch: {}'.format(i))
            with autograd.detect_anomaly():
                train_logs = self.train_run(dataloader)

            # update loss into log file
            with open(log_file, "a") as log:
                train_logs["epoch"] = i
                log.write(str(train_logs)+"\n")

            self.save_models(save_dir+"_{}".format(i))
            print('Model saved!')

    def _format_logs(self, logs):
        str_logs = ['{} - {:.4}'.format(k, v) for k, v in logs.items()]
        s = ', '.join(str_logs)
        return s

    def save_models(self, save_dir):
        import os
        os.makedirs(save_dir, exist_ok=True)
        gen_save_file = os.path.join(save_dir, "GAN_GEN.pth")
        dis_save_file = os.path.join(save_dir, "GAN_DIS.pth")
        gen_optim_save_file = os.path.join(save_dir, "GAN_GEN_OPTIM.pth")
        dis_optim_save_file = os.path.join(save_dir, "GAN_DIS_OPTIM.pth")

        torch.save(self.gen.state_dict(), gen_save_file)
        torch.save(self.dis.state_dict(), dis_save_file)
        torch.save(self.gen_optim.state_dict(), gen_optim_save_file)
        torch.save(self.dis_optim.state_dict(), dis_optim_save_file)


# if __name__ == "__main__":
#     import torch 
#     x = torch.zeros((32, 512, 40, 40))
#     block = cSEBlock(512, 1600)
#     block2 = sSEBlock(512, 40, 40)
#     block3 = scSEBlock(512, 40, 40)
#     attention = Attention(512)
#     y = block(x)
#     y2 = block(x)
#     y3 = block(x)
#     y4 = block(x)
#     print("y4", y4.shape)
#     print(y3.shape)
#     print(y2.shape)
#     print(y.shape)

#     resg = ResBlock_G(512, 256, True)
#     out = resg(x)
#     print("resblock", out.shape)

#     gen = Generator(2)
#     z = torch.randn(32, 512)
#     gen_out = gen(z)
#     print(gen_out.shape)

#     print("working on Discriminator")
#     disc = Discriminator_Remap(n_feat=32)
#     x,y = disc(torch.randn(32, 3, 128, 128))
#     print(y.shape)



