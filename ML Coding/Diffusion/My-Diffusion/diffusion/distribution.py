# distribution.py — Concrete probability distributions used by the noise process.
# These implement the 3 methods required by base.Distribution:
# sample(), nll(), and dkl().

from dataclasses import dataclass

import torch
from torch import Tensor
from typing_extensions import Self

from .base import Distribution


# Gaussian (Normal) distribution — the workhorse of standard diffusion (DDPM).
# Defined by mean (mu) and standard deviation (sigma).
@dataclass
class Normal(Distribution):
    mu: Tensor
    sigma: Tensor

    def sample(self) -> tuple[Tensor, Tensor]:
        # Reparameterization trick: sample = mu + sigma * random_noise.
        # Returns both the sample and the raw noise (epsilon).
        epsilon = torch.randn(self.mu.shape, device=self.mu.device)
        return self.mu + self.sigma * epsilon, epsilon

    def nll(self, x: Tensor) -> Tensor:
        # Negative log-likelihood of x under this Normal.
        # 2.5066... is sqrt(2*pi).
        return (0.5 * ((x - self.mu) / self.sigma)**2 +
                (self.sigma * 2.5066282746310002).log())

    def dkl(self, other: Self) -> Tensor:
        # KL divergence from self to other (both Normal).
        # Measures how different two Gaussians are.
        return (torch.log(other.sigma / self.sigma) +
                (self.sigma**2 + (self.mu - other.mu)**2) / (2 * other.sigma**2) - 0.5)


# Categorical distribution — for discrete/token data (e.g. text diffusion).
# Defined by probability vector p over K possible values.
@dataclass
class Categorical(Distribution):
    p: Tensor  # probability of each category, shape (..., K)

    def __post_init__(self) -> None:
        self.k = self.p.shape[-1]                          # number of categories
        self.i = torch.eye(self.k, device=self.p.device)   # identity for one-hot encoding

    def sample(self) -> tuple[Tensor, None]:
        # Sample a category index, return as one-hot vector.
        # No epsilon to return (discrete has no reparameterization trick).
        c = torch.multinomial(self.p.view(-1, self.k), 1, True)
        return self.i[c.view(*self.p.shape[:-1])], None

    def nll(self, x: Tensor) -> Tensor:
        # Negative log-likelihood: -log(probability of the observed category).
        return -((self.p * x).sum(-1) + 1e-6).log()

    def dkl(self, other: Self) -> Tensor:
        # KL divergence between two Categorical distributions.
        p1, p2 = self.p + 1e-6, other.p + 1e-6
        return (p1 * (p1.log() - p2.log())).sum(-1)
