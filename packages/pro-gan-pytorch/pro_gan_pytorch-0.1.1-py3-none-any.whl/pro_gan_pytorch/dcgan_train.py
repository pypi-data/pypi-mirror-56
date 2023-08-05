import torch
import torchvision.transforms as tt 
import os 
import argparse 
import glob
import logging


from pro_gan_pytorch.dataloaders import FacesDB
from pro_gan_pytorch.dcgan_models import Generator, Discriminator, train_epoch
from pro_gan_pytorch.dcgan_models import weights_init

parser = argparse.ArgumentParser(description="DCGAN Training")
parser.add_argument('-nz', '--dim_vec', help='', default=100)
parser.add_argument("-ngf", "--g_channels", help="", default=64)
parser.add_argument("-ndf", "--d_channels", help="", default=64)
parser.add_argument("-nc", "--channels", help="", default=3)
parser.add_argument("-im", "--img_size", help="", default=64)
parser.add_argument("-lr", "--learning_rate", help="", default=0.00005)
parser.add_argument("-b1", "--beta1", help="", default=0.5)
parser.add_argument("-ep", "--epochs", help="", default=100)
parser.add_argument("-bz", "--batch_size", help="", default=128)
parser.add_argument("-ncr", "--n_critic", help='', default=5)
parser.add_argument("-cv", "--clip_value", help='', default=0.01)
parser.add_argument("-sf", "--save_folder", help="", default="data/wdcgan_2_09")
parser.add_argument("-d", "--dataset", help="", default="data/celeba.txt")
parser.add_argument("--log_file", help="", default="losses_2_09.log")

args = parser.parse_args()
logging.basicConfig(filename=args.log_file, level=logging.DEBUG)
img_size = (args.img_size, args.img_size)

imgs = [i.split()[0].rsplit(",") for i in open(args.dataset, "r")]
print("total_images: {}".format(len(imgs)))

# scaling training images to the range of the tanh activation function [-1, 1]
dataset = FacesDB(imgs, transforms=tt.Compose([tt.Resize(img_size), tt.ToTensor(), tt.Normalize([0.5], [0.5])]))
dataloader = torch.utils.data.DataLoader(dataset, batch_size=args.batch_size,shuffle=True, num_workers=4)

netG = Generator(nz=args.dim_vec, ngf=args.g_channels, nc=args.channels)
netD = Discriminator(ndf=args.d_channels, nc=args.channels)
if torch.cuda.is_available():
    print("cuda is being used")
    netG = netG.cuda()
    netD = netD.cuda()

# Apply the weights_init function to randomly initialize all weights to mean=0, stdev=0.2.
netG.apply(weights_init)
netD.apply(weights_init)


if args.n_critic==1:
    optimizerD = torch.optim.Adam(netD.parameters(), lr=args.learning_rate, betas=(args.beta1, 0.999))
    optimizerG = torch.optim.Adam(netG.parameters(), lr=args.learning_rate, betas=(args.beta1, 0.999))

else:
    optimizerD = torch.optim.RMSprop(netD.parameters(), lr=args.learning_rate)
    optimizerG = torch.optim.RMSprop(netG.parameters(), lr=args.learning_rate)

criterion = torch.nn.BCELoss()

fixed_noise = torch.randn(args.batch_size, args.dim_vec, 1, 1)

kwargs = {'fixed_noise': fixed_noise, 'dataloader': dataloader, 'loss': criterion, 'netD' : netD, 'netG':netG, 
          'nz':args.dim_vec, 'ncr': args.n_critic, 'clip_value': args.clip_value, 'optimD' : optimizerD, 'optimG': optimizerG, 'cuda': True, 'save_folder': args.save_folder, 
          'verbose': 100 }


for ep in range(args.epochs):
    errD, errG = train_epoch(ep, **kwargs)
    print('Loss_D: %.4f Loss_G: %.4f'
              % (errD.item(), errG.item()))
    logging.debug('Loss_D: %.4f Loss_G: %.4f'
              % (errD.item(), errG.item()))
    torch.save(netG.state_dict(), '%s/netG_epoch_%d.pth' % (args.save_folder, ep))
    torch.save(netD.state_dict(), '%s/netD_epoch_%d.pth' % (args.save_folder, ep))

