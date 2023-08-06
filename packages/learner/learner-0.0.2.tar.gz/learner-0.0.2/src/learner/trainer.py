"""Trainer can help the leaner to update model based on data"""
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

optim_lookup = {
    'asgd':     optim.ASGD,
    'adadelta': optim.Adadelta,
    'adagrad':  optim.Adagrad,
    'adam':     optim.Adam,
    'rmsprop':  optim.RMSprop,
    'sgd':      optim.SGD
}


class Trainer:
    """Base Class for Trainer"""

    def __init__(self):
        pass

    def train_model(self, model, data):
        raise NotImplementedError


class SGDTrainer(Trainer):
    """A general trainer based on SGD"""

    def __init__(self, criterion=None, optimizer=None):
        super().__init__()
        self.criterion = criterion
        self.optimizer = optimizer

    def train_model(self, model: nn.Module, dataloader: DataLoader):
        for x, y in dataloader:
            self.optimizer.zero_grad()
            out = model(x)
            loss = self.criterion(out, y)
            loss.backward()
            self.optimizer.step()


if __name__ == '__main__':
    pass
