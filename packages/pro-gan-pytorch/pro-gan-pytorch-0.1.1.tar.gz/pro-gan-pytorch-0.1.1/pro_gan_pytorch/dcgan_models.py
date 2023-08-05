import torch
import torch.nn as nn
import torchvision.utils as vutils

from PIL import Image
from tqdm import tqdm 

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

class Generator(nn.Module):
    def __init__(self, nz, ngf, nc):
        super(Generator, self).__init__()
        self.nz = nz
        self.ngf = ngf 
        self.nc = nc
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d( self.nz, self.ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(self.ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(self.ngf * 8, self.ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(self.ngf * 4, self.ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(self.ngf * 2, self.ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(self.ngf, self.nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        output = self.main(input)
        return output
    

class Discriminator(nn.Module):
    def __init__(self, ndf, nc):
        super(Discriminator, self).__init__()
        self.ndf = ndf 
        self.nc = nc
        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(self.nc, self.ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(self.ndf, self.ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(self.ndf * 2, self.ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(self.ndf * 4, self.ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(self.ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(self.ndf * 8, 1, 4, 1, 0, bias=False),
        )

    def forward(self, input):
        output = self.main(input)
        return output.view(-1, 1).squeeze(1)



def train_epoch(epoch, fixed_noise, dataloader, loss, netD, netG, nz, ncr, clip_value, optimD, optimG, cuda=True, save_folder="", verbose=100):
    fake_label = 0
    real_label = 1 
    xerrd = []
    xerrg = []
    for i, real_data in tqdm(enumerate(dataloader)):
        ## training discriminator

        # train with real
        batch_size = real_data.shape[0]
        label = torch.full((batch_size,), real_label)
        if cuda:
            real_data, label = real_data.cuda(), label.cuda()
        netD.zero_grad()
        output = netD(real_data)
        ## ncr aka n_critic > 1 results in wgan mode training 
        if ncr == 1:
            output_ = torch.sigmoid(output)
            errD_real = loss(output_, label)
            errD_real.backward()
        
        # train with fake 
        noise = torch.randn(batch_size, nz, 1, 1)
        if cuda:
            noise = noise.cuda()
        fake_data = netG(noise)
        label.fill_(fake_label)
        output = netD(fake_data.detach()) ## Required so that grads are not carried
        
        if ncr == 1:
            output_ = torch.sigmoid(output)
            errD_fake = loss(output_, label)
            errD_fake.backward()
            errD = errD_real + errD_fake ## loss for DCGAN
        else:
            errD = - torch.mean(netD(real_data)) + torch.mean(netD(fake_data)) ##loss for WGAN
            errD.backward()
        optimD.step()

        if ncr>1:
            for p in netD.parameters():
                p.data.clamp_(-clip_value, clip_value)


        ## train the generator
        if i%ncr==0:
            netG.zero_grad()
            fake_data = netG(noise)
            label.fill_(real_label)
            if ncr==1:
                output = netD(fake_data)
                output_ = torch.sigmoid(output)
                errG = loss( output_, label)
            else:
                errG = -torch.mean(netD(fake_data))
            errG.backward()
            optimG.step()
            xerrg.append(errG.detach().cpu().numpy())
            xerrd.append(errD.detach().cpu().numpy())
            #errD_ = errD

        if i % 100 == 0:
            vutils.save_image(real_data.cpu().detach(),
                    '%s/real_samples.png' % save_folder,
                    normalize=False)
            
            if cuda:
                fixed_noise = fixed_noise.cuda()
            fake = netG(fixed_noise)
            vutils.save_image(fake.detach(),
                    '%s/fake_samples_%03d_%03d.png' % (save_folder, epoch, i),
                    normalize=False)

    return xerrg, xerrd