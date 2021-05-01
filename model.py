import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()

        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        x = position * div_term

        pe = torch.zeros(max_len, d_model)
        pe[:, 0::2] = torch.sin(x)
        pe[:, 1::2] = torch.cos(x)
        pe = pe.unsqueeze(0).transpose(0, 1)

        self.register_buffer('pe', pe)

    def forward(self, x: torch.tensor) -> torch.tensor:
        x = x + self.pe[:x.size(0), :]

        return self.dropout(x)


class ZReader(nn.Module):
    def __init__(self, token_size: int, pe_max_len: int, num_layers: int, d_model: int, n_heads: int, d_ff: int,
                 dropout: float = 0.1):
        super(ZReader, self).__init__()
        self.scale = math.sqrt(d_model)
        self.token_size = token_size

        self.mapping = nn.Linear(in_features=token_size, out_features=d_model)

        self.pe = PositionalEncoding(d_model=d_model, dropout=dropout, max_len=pe_max_len)

        self.encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads, dim_feedforward=d_ff,
                                                        dropout=dropout)
        self.encoder = nn.TransformerEncoder(encoder_layer=self.encoder_layer, num_layers=num_layers)

        self.decoder_layer = nn.TransformerDecoderLayer(d_model=d_model, nhead=n_heads, dim_feedforward=d_ff,
                                                        dropout=dropout)
        self.decoder = nn.TransformerDecoder(decoder_layer=self.decoder_layer, num_layers=num_layers)

        self.inv_mapping = nn.Linear(in_features=d_model, out_features=token_size)

        self.init_weights()

    def init_weights(self) -> None:
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(self, src: torch.tensor, src_pad_mask: torch.tensor,
                tgt_inp: torch.tensor, tgt_attn_mask: torch.tensor, tgt_pad_mask: torch.tensor) -> torch.tensor:

        src = F.relu(self.mapping(src)) * self.scale
        src = self.pe(src)

        tgt_inp = F.relu(self.mapping(tgt_inp)) * self.scale
        tgt_inp = self.pe(tgt_inp)

        encoded_src = self.encoder(src=src, src_key_padding_mask=src_pad_mask)

        decoded = self.decoder(tgt=tgt_inp, memory=encoded_src, tgt_mask=tgt_attn_mask,
                               tgt_key_padding_mask=tgt_pad_mask, memory_key_padding_mask=src_pad_mask)

        return self.inv_mapping(decoded)

    def save_parameters(self, filename: str) -> None:
        torch.save(self.state_dict(), filename)

    def load_parameters(self, filename: str, device: torch.device) -> None:
        self.load_state_dict(torch.load(filename, map_location=device))


if __name__ == "__main__":
    pass
