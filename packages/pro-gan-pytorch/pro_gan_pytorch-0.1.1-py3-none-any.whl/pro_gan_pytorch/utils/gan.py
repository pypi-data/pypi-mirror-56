from PRO_GAN import ProGAN
from wgan import WGAN
from big_gan import BigGAN
from metrics import *
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_metric(cfg):
    metrics = []
    if cfg.metrics is not None:
        for name in cfg.metrics:
            if name == "accuracy":
                metrics.append(Accuracy(activation=cfg.activation, thresh=cfg.threshold))
            else:
                raise NotImplementedError("This metric is not implemented")
    return metrics


def get_gan(gan_name, config):
    if gan_name == "progan":
        gan = ProGAN(
            depth=config.depth,
            latent_size=config.latent_size,
            learning_rate=config.learning_rate,
            beta_1=config.beta_1,
            beta_2=config.beta_2,
            eps=config.eps,
            drift=config.drift,
            n_critic=config.n_critic,
            use_eql=config.use_eql,
            loss=config.loss_function,
            use_ema=config.use_ema,
            ema_decay=config.ema_decay,
            device=DEVICE
        )
    elif gan_name == "wgan":
        gan = WGAN(
            latent_dim=config.latent_dim,
            img_size=config.img_dims,
            channels=config.num_channels,
            learning_rate=config.learning_rate,
            beta_1=config.beta_1,
            beta_2=config.beta_2,
            use_gp=config.use_gp,
            n_critic=config.n_critic,
            metrics=get_metric(config),
            clip_value=config.clip_value,
            device=DEVICE,
            verbose=True,
        )

    elif gan_name == "BigGAN":
        gan = BigGAN(
            latent_dim=config.latent_dim,
            n_featD=config.n_featD,
            n_featG=config.n_featG,
            channels=config.num_channels,
            learning_rate=config.learning_rate,
            beta_1=config.beta_1,
            beta_2=config.beta_2,
            metrics=get_metric(config),
            device=DEVICE,
            verbose=True,
        )

    else:
        raise NotImplementedError("The following gan is not implemented")

    return gan
