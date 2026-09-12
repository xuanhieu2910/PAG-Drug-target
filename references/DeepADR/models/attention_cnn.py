from torch import nn


class AttentionCNN(nn.Module):
    def __init__(self,
                 hidden_dim: None,
                 batch_first: bool,
                 num_heads: None,
                 dropout: None,
                 device: None):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.device = device
        self.batch_first = batch_first
        self.num_heads = num_heads
        self.dropout = dropout

        # ------------------ Layer Projector ------------------------
        self.Q_projector = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.K_V_projector = nn.Linear(self.hidden_dim, self.hidden_dim)

        # ------------------ Multihead attention Layer --------------
        self.cross_attention = nn.MultiheadAttention(
            embed_dim = self.hidden_dim,
            num_heads = self.num_heads,
            dropout = self.dropout,
            batch_first = self.batch_first,
            device = self.device
        )

        #-------------------- CNN -------------------------------------
        self.CNN = nn.Sequential(
            nn.Conv1d(in_channels = self.hidden_dim,out_channels = self.hidden_dim),
            nn.ReLU(),
            nn.Conv1d(in_channels = self.hidden_dim,out_channels = self.hidden_dim),
            nn.ReLU(),
        )

    def forward(self, mol, adr):
        Q = self.Q_projector(mol)
        K = self.K_V_projector(adr)
        V = self.K_V_projector(adr)
        mol_adr_output, mol_adr_weight = self.cross_attention(Q, K, V)
        return self.CNN(mol_adr_output)