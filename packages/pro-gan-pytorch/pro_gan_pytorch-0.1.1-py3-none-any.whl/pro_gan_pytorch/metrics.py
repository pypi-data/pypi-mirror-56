import torch 
import torch.nn as nn 

def accuracy(inputs, targs):
    """Computes accuracy with `targs` when `input` is bs * n_classes.
    """
    n = targs.shape[0]
    inputs = inputs.argmax(dim=-1).view(n,-1)
    targs = targs.view(n,-1)
    return (inputs==targs).float().mean()

def accuracy_thresh(y_pred, y_true, thresh=0.5, sigmoid=True):
    "Computes accuracy when `y_pred` and `y_true` are the same size."
    if sigmoid: y_pred = y_pred.sigmoid()
    return ((y_pred>thresh).byte()==y_true.byte()).float().mean()


class Accuracy(nn.Module):
    __name__ = "accuracy"

    def __init__(self, thresh=0.5, activation="sigmoid"):
        super().__init__()
        self.activation = activation
        self.thresh = thresh
    
    def forward(self, y_pr, y_gt):
        if self.activation == "softmax":
            acc = accuracy(y_pr, y_gt)
        elif self.activation == "sigmoid":
            acc = accuracy_thresh(y_pr, y_gt, thresh=self.thresh)
        else:
            raise NotImplementedError("The activation function accuracy is not implemented")
        return acc