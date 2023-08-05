import torch
import torch.nn as nn
from torch.nn import DataParallel
from torchnet.meter import AverageValueMeter
import numpy as np
from tqdm import tqdm
import sys
import os


class Generator(nn.Module):
    def __init__(self, latent_dim, img_size, channels=3):
        super(Generator, self).__init__()
        self.latent_dim = latent_dim
        self.img_size = img_size
        self.channels = channels
        self.img_shape = (self.channels, self.img_size, self.img_size)
        self.model = nn.Sequential(
            nn.Linear(self.latent_dim, 128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 512),
            nn.BatchNorm1d(512, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 1024),
            nn.BatchNorm1d(1024, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(1024, int(np.prod(self.img_shape))),
            nn.Tanh()
        )

    def forward(self, z):
        img = self.model(z)
        img = img.view(img.shape[0], *self.img_shape)
        return img


class Discriminator(nn.Module):
    def __init__(self, img_size, num_channels=3):
        super(Discriminator, self).__init__()
        self.img_size = img_size
        self.channels = num_channels
        self.img_shape = (self.channels, self.img_size, self.img_size)
        self.model = nn.Sequential(
            nn.Linear(int(np.prod(self.img_shape)), 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
        )

    def forward(self, img):
        img_flat = img.view(img.shape[0], -1)
        validity = self.model(img_flat)
        return validity


class WGAN:
    def __init__(self, latent_dim, img_size, channels=3, n_critic=1, beta_1=0, beta_2=0.99, learning_rate=0.001,
                 use_gp=False, clip_value=0.01, metrics=[], device=torch.device("cpu"), dataparallel=False,
                 verbose=True):
        self.gen = Generator(latent_dim, img_size, channels)
        self.dis = Discriminator(img_size, num_channels=channels)

        if device == torch.device("cuda"):
            self.gen = self.gen.cuda()
            self.dis = self.dis.cuda()

        if dataparallel:
            self.gen = DataParallel(self.gen)
            self.dis = DataParallel(self.dis)

        self.latent_dim = latent_dim
        self.img_size = img_size
        self.channels = channels
        self.n_critic = n_critic
        self.device = device
        self.metrics = metrics
        self.verbose = verbose
        self.use_gp = use_gp
        self.clip_value = clip_value

        self.gen_optim = torch.optim.Adam(self.gen.parameters(), lr=learning_rate, betas=(beta_1, beta_2))
        self.dis_optim = torch.optim.Adam(self.dis.parameters(), lr=learning_rate, betas=(beta_1, beta_2))
        self.loss = self.__setup_loss()

    def __setup_loss(self):
        import pro_gan_pytorch.wgan_loss as losses
        loss = losses.WganLoss(dis=self.dis, use_gp=self.use_gp)
        return loss

    def optimize_discriminator(self, noise, real_batch_labeled):
        fake_samples = self.gen(noise).detach()
        loss = self.loss.dis_loss(real_batch_labeled, fake_samples)
        self.dis_optim.zero_grad()
        loss.backward()
        self.dis_optim.step()
        return loss.item()

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

    def train_batch_update(self, i, x1):
        """
        i : index
        x1: labeled_examples
        """
        gen_input = torch.randn(x1.shape[0], self.latent_dim).to(self.device)
        dis_loss = self.optimize_discriminator(gen_input, x1)

        # Clip weights of discriminator if gradient penalty is not used
        if not self.use_gp:
            for p in self.dis.parameters():
                p.data.clamp_(-self.clip_value, self.clip_value)

        # Train the generator every n_critic iterations
        if i % self.n_critic == 0:
            gen_loss = self.optimize_generator(gen_input)
        else:
            gen_loss = 0.0
        return dis_loss, gen_loss

    def train_run(self, dataloader):
        self.on_train_start()
        logs = {}
        gen_loss_meter = AverageValueMeter()
        dis_loss_meter = AverageValueMeter()
        metrics_meters = {metric.__name__: AverageValueMeter() for metric in self.metrics}

        with tqdm(dataloader, desc="train", file=sys.stdout, disable=not self.verbose) as iterator:
            i = 0
            for x1, y in iterator:
                x1 = x1.to(self.device)
                gen_loss, dis_loss = self.train_batch_update(i, x1)
                if i % self.n_critic == 0:
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

        from pro_gan_pytorch.DataTools import get_data_loader
        dataloader = get_data_loader(dataset, batch_size=batch_sizes, num_workers=num_workers)

        #  writing losses to the log file
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "losses.log")
        for i in range(start_epoch, epochs):
            print('\nEpoch: {}'.format(i))
            train_logs = self.train_run(dataloader)

            # update loss into log file
            with open(log_file, "a") as log:
                train_logs["epoch"] = i
                log.write(str(train_logs)+"\n")

            self.save_models(save_dir)
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



