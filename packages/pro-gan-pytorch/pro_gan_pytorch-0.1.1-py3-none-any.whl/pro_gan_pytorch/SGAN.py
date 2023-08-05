""" Contains implementations for
- DCGAN
- WGAN
- SGAN
"""
import torch 
import torch.nn as nn
from torch.optim import Adam
from torch.nn import DataParallel
from torchnet.meter import AverageValueMeter

import numpy as np 
import time
import timeit
from tqdm import tqdm
import sys

def create_grid(samples, scale_factor, img_file):
    """
    utility function to create a grid of GAN samples
    :param samples: generated samples for storing
    :param scale_factor: factor for upscaling the image
    :param img_file: name of file to write
    :return: None (saves a file)
    """
    from torchvision.utils import save_image
    from torch.nn.functional import interpolate

    # upsample the image
    if scale_factor > 1:
        samples = interpolate(samples, scale_factor=scale_factor)

    # save the images:
    save_image(samples, img_file, nrow=int(np.sqrt(len(samples))),
                normalize=True, scale_each=True)


def weights_init_normal(m):
    classname = m.__class__.__name__
    if classname.find("Conv") != -1:
        torch.nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find("BatchNorm") != -1:
        torch.nn.init.normal_(m.weight.data, 1.0, 0.02)
        torch.nn.init.constant_(m.bias.data, 0.0)


class Generator(nn.Module):
    def __init__(self, latent_dim, img_size, channels=3):
        super(Generator, self).__init__()
        self.latent_dim = latent_dim 
        self.img_size = img_size
        self.channels = channels

        self.init_size = self.img_size // 4  # Initial size before upsampling
        self.l1 = nn.Sequential(nn.Linear(self.latent_dim, 128 * self.init_size ** 2))

        self.conv_blocks = nn.Sequential(
            nn.BatchNorm2d(128),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=False),
            nn.Upsample(scale_factor=2),
            nn.Conv2d(128, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=False),
            nn.Conv2d(64, self.channels, 3, stride=1, padding=1),
            nn.Tanh(),
        )

    def forward(self, noise):
        out = self.l1(noise)
        out = out.view(out.shape[0], 128, self.init_size, self.init_size)
        img = self.conv_blocks(out)
        return img

class Discriminator(nn.Module):
    def __init__(self, img_size, num_classes=1, num_channels=3, sgan=False):
        super(Discriminator, self).__init__()
        self.img_size = img_size
        self.sgan = sgan
        self.num_classes = num_classes
        self.num_channels = num_channels

        def discriminator_block(in_filters, out_filters, bn=True):
            """Returns layers of each discriminator block"""
            block = [nn.Conv2d(in_filters, out_filters, 3, 2, 1), nn.LeakyReLU(0.2, inplace=False), nn.Dropout2d(0.25)]
            if bn:
                block.append(nn.BatchNorm2d(out_filters, 0.8))
            return block

        self.conv_blocks = nn.Sequential(
            *discriminator_block(self.num_channels, 16, bn=False),
            *discriminator_block(16, 32),
            *discriminator_block(32, 64),
            *discriminator_block(64, 128),
        )

        # The height and width of downsampled image
        ds_size = self.img_size // 2 ** 4
        self.sgan = sgan ## Weather it is supervised or not.

        # Output layers
        self.adv_layer = nn.Sequential(nn.Linear(128 * ds_size ** 2, 1), nn.Sigmoid())
        if self.sgan:
            self.aux_layer = nn.Sequential(nn.Linear(128 * ds_size ** 2, self.num_classes), nn.Softmax(dim=1))

    def forward(self, img):
        out = self.conv_blocks(img)
        out = out.view(out.shape[0], -1)
        validity = self.adv_layer(out)
        if self.sgan:
            label = self.aux_layer(out)
            return validity, label 
        else:
            return validity


class SGAN:
    def __init__(self, latent_dim, img_size, channels=3, num_classes=2, n_critic=1, beta_1=0, beta_2=0.99, eps=1e-8, learning_rate=0.001, losses="bce_cce", metrics=None, device=torch.device("cpu"), dataparallel=False, verbose=True):
        self.gen = Generator(latent_dim, img_size, channels)
        self.dis = Discriminator(img_size, num_classes=num_classes, num_channels=channels, sgan=True)

        if device == torch.device("cuda"):
            self.gen = self.gen.cuda()
            self.dis = self.dis.cuda()
        
        if dataparallel:
            self.gen = DataParallel(self.gen)
            self.dis = DataParallel(self.dis)

        self.gen.apply(weights_init_normal)
        self.dis.apply(weights_init_normal)
        
        self.latent_dim = latent_dim 
        self.img_size = img_size 
        self.channels = channels 
        self.num_classes = num_classes 
        self.losses = losses
        self.n_critic = n_critic 
        self.device = device
        self.metrics = metrics
        self.verbose = verbose

        self.gen_optim = Adam(self.gen.parameters(), lr=learning_rate, betas=(beta_1, beta_2), eps=eps)
        self.dis_optim = Adam(self.dis.parameters(), lr=learning_rate, betas=(beta_1, beta_2), eps=eps)
        self.loss = self.__setup_loss(self.losses)

    def __setup_loss(self, loss):
        import pro_gan_pytorch.sgan_loss as losses

        if isinstance(loss, str):
            loss = loss.lower()  # lowercase the string
            if loss == "bce_cce":
                cuda = True if self.device==torch.device("cuda") else False
                loss = losses.BCE_CCE(self.dis, cuda=cuda)
                # note if you use just wgan, you will have to use weight clipping
                # in order to prevent gradient explodin

        elif not isinstance(loss, losses.ConditionalSGANLoss):
            raise ValueError("loss is neither an instance of GANLoss nor a string")

        return loss
    
    def optimize_discriminator(self, noise, real_batch_labeled, real_batch_unlabeled, labels):
        loss_val = 0
        for _ in range(self.n_critic):
            fake_samples = self.gen(noise).detach()
            loss, pred_labels = self.loss.dis_loss(real_batch_labeled, real_batch_unlabeled, fake_samples, labels)
            self.dis_optim.zero_grad()
            loss.backward()
            self.dis_optim.step()
            loss_val += loss.item()
        return loss_val/self.n_critic, pred_labels

    def optimize_generator(self, noise):
        fake_samples = self.gen(noise)
        loss = self.loss.gen_loss(fake_samples)
        self.gen_optim.zero_grad()
        loss.backward()
        self.gen_optim.step()

        return loss.item()
    
    def on_train_start(self):
        self.dis.train()
        self.gen.train()
    
    def train_batch_update(self, x1, x2, y):
        """
        x1: labeled_examples
        x2: unlabeled_examples
        y: labels of x1 
        """
        gen_input = torch.randn(x1.shape[0], self.latent_dim).to(self.device)
        dis_loss, preds = self.optimize_discriminator(gen_input, x1, x2, y)
        gen_loss = self.optimize_generator(gen_input)
        return dis_loss, gen_loss, preds

    def val_batch_update(self, x1, y):
        with torch.no_grad():
            _, y_pred = self.dis(x1)
        return y_pred

    def train_run(self, dataloader):
        self.on_train_start()
        logs = {}
        gen_loss_meter = AverageValueMeter()
        dis_loss_meter = AverageValueMeter()
        metrics_meters = {metric.__name__: AverageValueMeter() for metric in self.metrics}

        with tqdm(dataloader, desc="train", file=sys.stdout, disable=not(self.verbose)) as iterator:
            for x1, x2, y in iterator:
                x1, x2, y = x1.to(self.device), x2.to(self.device), y.to(self.device)

                gen_loss, dis_loss, predictions = self.train_batch_update(x1, x2, y)
                gen_loss_meter.add(gen_loss)
                dis_loss_meter.add(dis_loss)
                loss_logs = {"gen_loss": gen_loss_meter.mean, "dis_loss": dis_loss_meter.mean}
                logs.update(loss_logs)

                # update the metrics:
                for metric_fn in self.metrics:
                    metric_value = metric_fn(predictions, y).cpu().detach().numpy()
                    metrics_meters[metric_fn.__name__].add(metric_value)
                metrics_logs = {k: v.mean for k, v in metrics_meters.items()}
                logs.update(metrics_logs)

                if self.verbose:
                    s = self._format_logs(logs)
                    iterator.set_postfix_str(s)
        return logs

    def on_val_start(self):
        self.dis.eval()
        self.gen.eval()
    
    def val_run(self, dataloader):
        self.on_val_start()
        logs = {}
        metrics_meters = {metric.__name__: AverageValueMeter() for metric in self.metrics}

        with tqdm(dataloader, desc="val", file=sys.stdout, disable=not(self.verbose)) as iterator:
            for x, y in iterator:
                x, y = x.to(self.device), y.to(self.device)
                _, y_pred = self.dis(x)
                # update the metrics:
                for metric_fn in self.metrics:
                    metric_value = metric_fn(y_pred, y).cpu().detach().numpy()
                    metrics_meters[metric_fn.__name__].add(metric_value)
                metrics_logs = {k: v.mean for k, v in metrics_meters.items()}
                logs.update(metrics_logs)

                if self.verbose:
                    s = self._format_logs(logs)
                    iterator.set_postfix_str(s)
        return logs
    
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



