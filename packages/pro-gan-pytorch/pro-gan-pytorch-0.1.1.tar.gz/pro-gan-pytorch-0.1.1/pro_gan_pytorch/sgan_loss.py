import torch

class ConditionalSGANLoss:
    """ Base class for all conditional losses """

    def __init__(self, dis):
        self.dis = dis

    def dis_loss(self, real_samps, fake_samps, labels):
        raise NotImplementedError("dis_loss method has not been implemented")

    def gen_loss(self, real_samps, fake_samps, labels):
        raise NotImplementedError("gen_loss method has not been implemented")


class BCE_CCE(ConditionalSGANLoss):
    __name__ = "bce_cce"
    
    def __init__(self, dis, cuda=False):
        super().__init__(dis)
        self.cuda = cuda
        self.cce = torch.nn.CrossEntropyLoss()
        self.bce = torch.nn.BCELoss()
    
    def dis_loss(self, real_samples_labeled, real_samples_unlabeled, fake_samps, real_labels): ## labels is a long tensor
        fake_label = 0 
        real_label = 1
        fake_out, _ = self.dis(fake_samps)
        _, pred_labels = self.dis(real_samples_labeled)
        real_out2, _ = self.dis(real_samples_unlabeled)
        
        label1 = torch.full((real_samples_labeled.shape[0], 1), real_label)
        label2 = torch.full((real_samples_labeled.shape[0], 1), fake_label)
        if self.cuda:
            label1 = label1.cuda()
            label2 = label2.cuda()

        errd_bce_unsupervised= self.bce(real_out2, label1)
        errd_bce_fake = self.bce(fake_out, label2)
        errd_cls = self.cce(pred_labels, real_labels.squeeze(1))

        total_unsupervised = (errd_bce_fake+ errd_bce_unsupervised)/2
        total_dis_loss = errd_cls + total_unsupervised
        return total_dis_loss, pred_labels
    
    def gen_loss(self, fake_samps):
        # calculate the WGAN loss for generator
        real_label = 1 
        output, _ = self.dis(fake_samps)
        label = torch.full((fake_samps.shape[0], 1), real_label)
        if self.cuda:
            label = label.cuda()
        errd_gen = self.bce(output, label)
        return errd_gen