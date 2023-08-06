"""AutoEncoders"""
from typing import Callable
import torch
import torch.nn as nn
import torch.optim as optim


class AutoEncoder(nn.Module):
    """A simple AutoEncoder Class"""
    def __init__(self, in_dim, hidden_dims, actn: Callable = nn.ReLU(), out_actn_encode=None, out_actn_decode=None):
        """
        Args:
            in_dim (int): number of features for the input data
            hidden_dims (list): a list of numbers for hidden layers where last element will be the encoded dimension
            actn (Callable): activation function for the hidden layers
            out_actn_encode (Callable): activation function for the last layer of the encoder
            out_actn_decode (Callable): activation function for the last layer of the decoder
        """
        super().__init__()
        self.encoder = nn.Sequential(*[
            nn.Linear(in_sz, out_sz)
            for in_sz, out_sz in zip(
                [in_dim] + hidden_dims[:-1], hidden_dims
            )
        ])
        self.decoder = nn.Sequential(*[
            nn.Linear(in_sz, out_sz)
            for in_sz, out_sz in zip(
                hidden_dims[::-1], hidden_dims[-2::-1] + [in_dim]
            )
        ])
        self.actn = actn
        self.out_actn_encode = out_actn_encode
        self.out_actn_decode = out_actn_decode

    def encode(self, x):
        for l in self.encoder[:-1]:
            x = self.actn(l(x))
        if self.out_actn_encode:
            return self.out_actn_encode(self.encoder[-1](x))
        else:
            return self.encoder[-1](x)

    def decode(self, z):
        for l in self.decoder[:-1]:
            z = self.actn(l(z))
        if self.out_actn_decode:
            return self.out_actn_decode(self.decoder[-1](z))
        else:
            return self.decoder[-1](z)

    def forward(self, x):
        return self.decode(self.encode(x))

    def fit(self, x, y=None, num_epoch=1, print_loss_every=1):
        assert y is None, "You do not need a target to train an autoencoder!"
        for epoch in range(num_epoch):
            optimizer = optim.Adam(self.parameters())
            x_encoded = self(x)
            loss = nn.functional.mse_loss(x, x_encoded) + torch.mean(torch.abs(x_encoded))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if epoch % print_loss_every == 0:
                print(f"Epoch {epoch}: {loss.item():.6f}")
