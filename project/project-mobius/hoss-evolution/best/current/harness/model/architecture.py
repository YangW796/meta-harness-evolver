"""Target-aware reranking model."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class RerankingModelConfig:
    vocab_size: int = 22
    chain_vocab_size: int = 4
    hidden_dim: int = 256
    num_layers: int = 4
    num_heads: int = 8
    dropout: float = 0.1
    num_utility_targets: int = 8
    num_confidence_tiers: int = 6
    num_ddg_statuses: int = 5


class SequenceEncoder(nn.Module):
    """Sequence encoder over concatenated antibody and antigen chains."""

    def __init__(self, config: RerankingModelConfig) -> None:
        super().__init__()
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_dim)
        self.chain_embedding = nn.Embedding(config.chain_vocab_size, config.hidden_dim)
        layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_dim,
            nhead=config.num_heads,
            dim_feedforward=config.hidden_dim * 4,
            dropout=config.dropout,
            batch_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=config.num_layers)
        self.norm = nn.LayerNorm(config.hidden_dim)

    def forward(
        self,
        tokens: torch.Tensor,
        chain_ids: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        x = (
            self.token_embedding(tokens)
            + self.chain_embedding(chain_ids)
            + sinusoidal_position_encoding(tokens.shape[1], tokens.device, self.token_embedding.embedding_dim)
        )
        x = self.encoder(x, src_key_padding_mask=~mask)
        return masked_mean(self.norm(x), mask)


class StructureEncoder(nn.Module):
    """Residue-level encoder over generated structure CA coordinates."""

    def __init__(self, config: RerankingModelConfig) -> None:
        super().__init__()
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_dim)
        self.chain_embedding = nn.Embedding(config.chain_vocab_size, config.hidden_dim)
        self.coord_mlp = nn.Sequential(
            nn.Linear(3, config.hidden_dim),
            nn.GELU(),
            nn.LayerNorm(config.hidden_dim),
        )
        self.distance_summary_mlp = nn.Sequential(
            nn.Linear(4, config.hidden_dim),
            nn.GELU(),
            nn.LayerNorm(config.hidden_dim),
        )
        layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_dim,
            nhead=config.num_heads,
            dim_feedforward=config.hidden_dim * 4,
            dropout=config.dropout,
            batch_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=config.num_layers)
        self.norm = nn.LayerNorm(config.hidden_dim)

    def forward(
        self,
        tokens: torch.Tensor,
        chain_ids: torch.Tensor,
        ca_coords: torch.Tensor,
        mask: torch.Tensor,
    ) -> torch.Tensor:
        centered_coords = center_coordinates(ca_coords, mask)
        distance_summary = residue_distance_summary(centered_coords, mask)
        x = (
            self.token_embedding(tokens)
            + self.chain_embedding(chain_ids)
            + self.coord_mlp(centered_coords)
            + self.distance_summary_mlp(distance_summary)
        )
        x = self.encoder(x, src_key_padding_mask=~mask)
        return masked_mean(self.norm(x), mask)


class MobiusReranker(nn.Module):
    """Multi-task surrogate model for dry-dry reranking."""

    def __init__(self, config: RerankingModelConfig | None = None) -> None:
        super().__init__()
        self.config = config or RerankingModelConfig()
        self.sequence_encoder = SequenceEncoder(self.config)
        self.structure_encoder = StructureEncoder(self.config)
        self.fusion = nn.Sequential(
            nn.Linear(self.config.hidden_dim * 4, self.config.hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(self.config.dropout),
            nn.LayerNorm(self.config.hidden_dim * 2),
            nn.Linear(self.config.hidden_dim * 2, self.config.hidden_dim),
            nn.GELU(),
            nn.LayerNorm(self.config.hidden_dim),
        )
        self.utility_head = nn.Linear(self.config.hidden_dim, self.config.num_utility_targets)
        self.score_head = nn.Linear(self.config.hidden_dim, 1)
        self.confidence_head = nn.Linear(
            self.config.hidden_dim,
            self.config.num_confidence_tiers,
        )
        self.ddg_status_head = nn.Linear(
            self.config.hidden_dim,
            self.config.num_ddg_statuses,
        )

    def forward(self, batch: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
        """
        Model interface (must stay compatible with mobius.reranking.lightning.module).

        Inputs
        - batch: dict[str, torch.Tensor] containing at least:
          - seq_tokens: (B, Ls) long
          - seq_chain_ids: (B, Ls) long
          - seq_mask: (B, Ls) bool
          - struct_tokens: (B, Lr) long
          - struct_chain_ids: (B, Lr) long
          - ca_coords: (B, Lr, 3) float
          - struct_mask: (B, Lr) bool

        Outputs
        - dict with keys used by reranking_loss(...):
          - pred_utility: (B, num_utility_targets) float in [0, 1]
          - pred_score_direct: (B,) float in [0, 1]
          - confidence_logits: (B, num_confidence_tiers) float (unnormalized)
          - ddg_status_logits: (B, num_ddg_statuses) float (unnormalized)
        """
        seq_repr = self.sequence_encoder(
            batch["seq_tokens"],
            batch["seq_chain_ids"],
            batch["seq_mask"],
        )
        struct_repr = self.structure_encoder(
            batch["struct_tokens"],
            batch["struct_chain_ids"],
            batch["ca_coords"],
            batch["struct_mask"],
        )
        fused_input = torch.cat(
            [
                seq_repr,
                struct_repr,
                torch.abs(seq_repr - struct_repr),
                seq_repr * struct_repr,
            ],
            dim=-1,
        )
        fused = self.fusion(fused_input)
        pred_utility = torch.sigmoid(self.utility_head(fused))
        pred_score_direct = torch.sigmoid(self.score_head(fused)).squeeze(-1)
        return {
            "pred_utility": pred_utility,
            "pred_score_direct": pred_score_direct,
            "confidence_logits": self.confidence_head(fused),
            "ddg_status_logits": self.ddg_status_head(fused),
        }


def masked_mean(x: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    mask_f = mask.unsqueeze(-1).to(dtype=x.dtype)
    denom = mask_f.sum(dim=1).clamp_min(1.0)
    return (x * mask_f).sum(dim=1) / denom


def center_coordinates(coords: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    mask_f = mask.unsqueeze(-1).to(dtype=coords.dtype)
    denom = mask_f.sum(dim=1, keepdim=True).clamp_min(1.0)
    center = (coords * mask_f).sum(dim=1, keepdim=True) / denom
    return (coords - center) * mask_f


def residue_distance_summary(coords: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Per-residue distance summary to inject structure geometry cheaply."""
    valid = mask.unsqueeze(1) & mask.unsqueeze(2)
    distances = torch.cdist(coords, coords)
    distances = distances.masked_fill(~valid, 0.0)
    denom = valid.sum(dim=-1).clamp_min(1).to(dtype=coords.dtype)
    mean_dist = distances.sum(dim=-1) / denom
    max_dist = distances.max(dim=-1).values
    min_nonzero = distances.masked_fill(~valid | (distances <= 0), float("inf")).min(dim=-1).values
    min_nonzero = torch.where(torch.isfinite(min_nonzero), min_nonzero, torch.zeros_like(min_nonzero))
    neighbor_count = ((distances < 8.0) & valid & (distances > 0)).sum(dim=-1).to(dtype=coords.dtype)
    return torch.stack(
        [
            mean_dist / 100.0,
            max_dist / 100.0,
            min_nonzero / 100.0,
            neighbor_count / 64.0,
        ],
        dim=-1,
    )


def sinusoidal_position_encoding(length: int, device: torch.device, dim: int) -> torch.Tensor:
    position = torch.arange(length, device=device, dtype=torch.float32).unsqueeze(1)
    div_term = torch.exp(
        torch.arange(0, dim, 2, device=device, dtype=torch.float32)
        * (-torch.log(torch.tensor(10000.0, device=device)) / dim)
    )
    pe = torch.zeros(length, dim, device=device, dtype=torch.float32)
    pe[:, 0::2] = torch.sin(position * div_term)
    if dim % 2 == 0:
        pe[:, 1::2] = torch.cos(position * div_term)
    else:
        pe[:, 1::2] = torch.cos(position * div_term[:-1])
    return pe.unsqueeze(0)
