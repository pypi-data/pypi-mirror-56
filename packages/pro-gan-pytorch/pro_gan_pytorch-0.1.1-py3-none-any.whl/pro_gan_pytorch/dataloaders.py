import torch
import torchvision
from torch.utils.data import Dataset
from PIL import Image
import numpy as np
import glob


class FacesDB(Dataset):
    def __init__(self, folder, transforms=None, crop=True):
        self.folder = folder
        self.locs = self._get_locs(self.folder)
        self.transforms = transforms
        self.crop = crop
    
    def _get_locs(self, folder):
        return glob.glob(self.folder+"*.jpg")
    
    def __getitem__(self, idx):
        fields = self.locs[idx]
        if self.crop:
            img_loc = fields[0]
        else:
            img_loc = fields
        img = Image.open(img_loc)
        if self.crop:
            y1, x2, y2, x1 = [int(i) for i in fields[1:]]
            img = img.crop([x1, y1, x2, y2])
        if self.transforms is not None:
            img = self.transforms(img)
        return img 

    def __len__(self):
        return len(self.locs)


class ClassFolders(Dataset):
    def __init__(self, folder, transforms=None, crop=True):
        self.folder = folder
        self.locs = self._get_locs(self.folder)
        self.transforms = transforms
        self.crop = crop

    def _get_locs(self, folder):
        return glob.glob(self.folder + "*/*")

    def __getitem__(self, idx):
        fields = self.locs[idx]
        if self.crop:
            img_loc = fields[0]
        else:
            img_loc = fields
        img = Image.open(img_loc)
        if self.crop:
            y1, x2, y2, x1 = [int(i) for i in fields[1:]]
            img = img.crop([x1, y1, x2, y2])
        if self.transforms is not None:
            img = self.transforms(img)
        return img

    def __len__(self):
        return len(self.locs)


class DatasetsUnsupervised(torch.utils.data.Dataset):
    def __init__(self, num_labeled, images, labels, transforms=None):
        super(DatasetsUnsupervised).__init__()
        self.num_labeled = num_labeled 
        self.transforms = transforms
        self.images = images
        self.labels = labels 
        self.labeled_idx = np.random.randint(0, self.images.shape[0], self.num_labeled*np.unique(labels).shape[0])
        self.unlabeled_idx = [i for i in range(self.images.shape[0]) if i not in self.labeled_idx]
    
    def __getitem__(self, idx):
        x1_ = self.labeled_idx[np.random.randint(len(self.labeled_idx))]
        x2_ = self.unlabeled_idx[np.random.randint(len(self.unlabeled_idx))]
        img_supervised = Image.fromarray(self.images[x1_, :, :, :])
        img_unsupervised = Image.fromarray(self.images[x2_, :, :, :])
        img_label = self.labels[x1_]
        if self.transforms is not None:
            img_supervised = self.transforms(img_supervised)
            img_unsupervised = self.transforms(img_unsupervised)
        return img_supervised, img_unsupervised, torch.Tensor([img_label]).long()
    
    def __len__(self):
        return self.images.shape[0]


def get_sgan_data_loader(dataset_name, num_labeled, transforms):
    if dataset_name == "cifar10":
        testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transforms)
        trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=False)
        dataset_supervised = DatasetsUnsupervised(num_labeled, trainset.data, trainset.targets, transforms=transforms)
    else:
        raise NotImplementedError("The following dataset is not implemented")
    return dataset_supervised, testset


def get_wgan_data_loader(dataset_name, transforms):
    if dataset_name == "mnist":
        trainset = torchvision.datasets.MNIST("./data", train=True, download=True, transform=transforms)
    elif dataset_name == "cifar10":
        trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transforms)
    else:
        raise NotImplementedError("The following dataset is not implemented")
    return trainset