from torch import nn
from .attention_cnn import AttentionCNN
from .kan_implement import KANImplement
from .variational_autoencoder_implement import VariationalAutoencoderImplement

class DeepADR(nn.Module):
    def __init__(self,
                 hidden_dim: None,
                 batch_first: bool,
                 num_heads: None,
                 dropout: None,
                 device: None,
                 width: None,
                 grid: None,
                 k: None,
                 seed: None
                 ):
        super(DeepADR, self).__init__()

        self.hidden_dim = hidden_dim
        self.batch_first = batch_first,
        self.num_heads = num_heads,
        self.dropout = dropout,
        self.device = device,
        self.width = width,
        self.grid = grid,
        self.k = k,
        self.seed = seed

        self.attention_cnn = AttentionCNN(
            hidden_dim=self.hidden_dim,
            batch_first=self.batch_first,
            num_heads=self.num_heads,
            dropout=self.dropout,
            device=self.device,
        )

        self.kan_implement = KANImplement(
            width = self.width,
            grid = self.grid,
            k = self.k,
            seed = self.seed
        )

        self.variational_autoencoder = VariationalAutoencoderImplement()

    def forward(self, drug_target, mol, adr):
        drug_target_vea = self.variational_autoencoder()
        mol_adr_attention = self.attention_cnn(mol, adr)
        pass