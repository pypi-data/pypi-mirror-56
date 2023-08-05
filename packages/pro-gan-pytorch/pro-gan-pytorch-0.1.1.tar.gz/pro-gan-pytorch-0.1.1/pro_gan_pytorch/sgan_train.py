import argparse 
import numpy as np 
import torch 
import yaml
from pro_gan_pytorch.SGAN import SGAN
from pro_gan_pytorch.dataloaders import get_sgan_data_loader
from pro_gan_pytorch.DataTools import get_transform
from pro_gan_pytorch.metrics import *

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

torch.manual_seed(2019)

def parse_arguments():
    """
    command line arguments parser
    :return: args => parsed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="store", type=str, default="configs/sgan.yaml",
                        help="default configuration for the Network")
    parser.add_argument("--start_epoch", action="store", type=int, default=0,
                        help="Starting epoch for training the network")
    parser.add_argument("--generator_file", action="store", type=str, default=None,
                        help="pretrained Generator file (compatible with my code)")
    parser.add_argument("--discriminator_file", action="store", type=str, default=None,
                        help="pretrained Discriminator file (compatible with my code)")
    parser.add_argument("--gen_optim_file", action="store", type=str, default=None,
                        help="saved state of generator optimizer")
    parser.add_argument("--dis_optim_file", action="store", type=str, default=None,
                        help="saved_state of discriminator optimizer")
    args = parser.parse_args()

    return args


def get_config(conf_file):
    """
    parse and load the provided configuration
    :param conf_file: configuration file
    :return: conf => parsed configuration
    """
    from easydict import EasyDict as edict

    with open(conf_file, "r") as file_descriptor:
        data = yaml.load(file_descriptor)

    # convert the data into an easyDictionary
    return edict(data)


def get_metric(cfg):
    metrics = []
    for name in cfg.metrics:
        if name == "accuracy":
            metrics.append(Accuracy(activation=cfg.activation, thresh=cfg.threshold))
        else:
            raise NotImplementedError("This metric is not implemented")
    return metrics


def main(args):
    print(args.config)
    config = get_config(args.config)
    print("current_configuration: ", config)

    print("calling dataloaders")
    trainset, testset = get_sgan_data_loader(config.dataset_name, config.num_labeled, transforms=get_transform(new_size=None))
    train_dataloader =  torch.utils.data.DataLoader(trainset, batch_size=config.batch_sizes, shuffle=True, num_workers=2)
    val_dataloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

    print("total training examples: {}".format(len(trainset)))

    sgan = SGAN(
        latent_dim=config.latent_dim,
        img_size=config.img_dims,
        channels=config.num_channels,
        num_classes=config.num_classes,
        learning_rate=config.learning_rate,
        beta_1=config.beta_1,
        beta_2=config.beta_2,
        n_critic=config.n_critic,
        losses=config.loss_function,
        eps=config.eps,
        metrics=get_metric(config),
        device=DEVICE,
        verbose=True,
    )
    if args.generator_file is not None:
        print("Loading generator from:", args.generator_file)
        sgan.gen.load_state_dict(torch.load(args.generator_file))

    if args.discriminator_file is not None:
        print("Loading discriminator from:", args.discriminator_file)
        sgan.dis.load_state_dict(torch.load(args.discriminator_file))

    if args.gen_optim_file is not None:
        print("Loading generator optimizer from:", args.gen_optim_file)
        sgan.gen_optim.load_state_dict(torch.load(args.gen_optim_file))

    if args.dis_optim_file is not None:
        print("Loading discriminator optimizer from:", args.dis_optim_file)
        sgan.dis_optim.load_state_dict(torch.load(args.dis_optim_file))
    
    print("Generator_configuration:\n%s" % str(sgan.gen))
    print("Discriminator_configuration:\n%s" % str(sgan.dis))

    max_score = 0
    for i in range(args.start_epoch, config.epochs):
        
        print('\nEpoch: {}'.format(i))
        train_logs = sgan.train_run(train_dataloader)
        valid_logs = sgan.val_run(val_dataloader)
        
        # do something (save model, change lr, etc.)
        if max_score < valid_logs[config.metrics[0]]:
            max_score = valid_logs[config.metrics[0]]
            sgan.save_models(config.save_dir)
            print('Model saved!')

    

if __name__ == '__main__':
    # invoke the main function of the script
    main(parse_arguments())