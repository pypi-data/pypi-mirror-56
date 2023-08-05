import torch
import torch.nn as nn
from tqdm import tqdm
import h5py
from dcgan_models import Discriminator


class SaveFeatures():
    """class to save features from a particular layer
    """
    def __init__(self, module):
        self.hook = module.register_forward_hook(self.hook_fn)

    def hook_fn(self, module, input, output):
        self.features = torch.tensor(output,requires_grad=True).cuda()

    def close(self):
        self.hook.remove()


def flatten(t):
    """flatten tensor t
    """
    t = t.reshape(1, -1)
    t = t.squeeze()
    return t


def get_feature(kernel_size, conv_feature):
    """apply maxpool and flatten out
    """
    max_pool = nn.MaxPool2d(kernel_size=kernel_size, padding=0)
    feature = flatten(max_pool(conv_feature))
    return feature


def save_features(N, dim, dataloader, save_features_path, weights_path):
    """extract features and save them into save_features_path
    """
    # Initializing dicriminator
    netD = Discriminator(ndf=64, nc=3)
    netD = netD.cuda().eval()

    # Load dicriminator weights
    netD.load_state_dict(torch.load(weights_path), strict=True)

    h5_file = h5py.File(save_features_path, 'w')
    datax = h5_file.create_dataset('data', (N, dim), maxshape=(None, dim), dtype="float")

    for i, data in tqdm(enumerate(dataloader)):
        activations_layer1 = SaveFeatures(list(netD.children())[0][0])  # from 1st con2D layer
        activations_layer2 = SaveFeatures(list(netD.children())[0][2])  # from 2nd con2D layer
        activations_layer3 = SaveFeatures(list(netD.children())[0][5])  # from 3rd con2D layer

        output = netD(data.cuda())

        feature1 = get_feature(8, activations_layer1.features)
        feature2 = get_feature(4, activations_layer2.features)
        feature3 = get_feature(2, activations_layer3.features)

        # clear memory
        activations_layer1.close()
        activations_layer2.close()
        activations_layer3.close()

        feature = torch.cat((feature1, feature2, feature3)).cpu().detach().numpy()
        datax[i] = feature

    h5_file.close()
