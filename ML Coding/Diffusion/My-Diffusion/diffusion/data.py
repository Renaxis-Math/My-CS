# data.py — How raw data is converted to/from tensors for the diffusion process.
# Each class implements encode() and decode() from base.Data.

from dataclasses import dataclass
from typing import Optional

import torch
from torch import Tensor, nn

from .base import Data


# No transformation — data is already in the right format.
# Used for images that are already normalized tensors.
class Identity(Data):

    def encode(self, w: Tensor) -> Tensor:
        return w

    def decode(self, x: Tensor) -> Tensor:
        return x


# Converts integer token IDs to one-hot vectors and back.
# Used for discrete/text diffusion with Categorical noise.
@dataclass
class OneHot(Data):
    k: Optional[int] = None  # vocabulary size (number of categories)

    def __post_init__(self):
        assert self.k is not None
        self.i = torch.eye(self.k)

    def encode(self, w: Tensor) -> Tensor:
        # Token ID 3 -> [0, 0, 0, 1, 0, ...] (one-hot vector).
        self.i = self.i.to(w.device)
        return self.i[w]

    def decode(self, x: Tensor) -> Tensor:
        # One-hot vector -> token ID (pick the highest value).
        return x.argmax(-1)


# Maps token IDs through a learnable embedding layer.
# Used for continuous-space text diffusion (Gaussian noise on embeddings).
@dataclass
class Embedding(Data):
    k: Optional[int] = None  # vocabulary size
    d: Optional[int] = None  # embedding dimension

    def __post_init__(self) -> None:
        assert self.k is not None and self.d is not None
        self.embedding = nn.Embedding(self.k, self.d)

    def encode(self, w: Tensor) -> Tensor:
        # Token ID -> learned d-dimensional vector.
        return self.embedding(w)

    def decode(self, x: Tensor) -> Tensor:
        # Find the nearest embedding vector for each position.
        return torch.cdist(x, self.embedding.weight).argmin(-1)
