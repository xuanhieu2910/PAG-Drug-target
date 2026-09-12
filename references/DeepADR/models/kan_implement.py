import torch.nn as nn
from kan import *
from kan import KAN

class KANImplement(nn.Module):
    def __init__(self,
                 width: None,
                 grid: None,
                 k: None,
                 seed: None):
        super(KANImplement, self).__init__()
        self.width = width
        self.grid = grid
        self.k = k
        self.seed = seed

        self.kan = KAN(width = self.width,
                       grid = self.grid,
                       k = self.k,
                       seed= self.seed)

    def forward(self,features_input):
        return self.kan(features_input)