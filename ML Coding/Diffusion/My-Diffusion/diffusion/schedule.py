# schedule.py — Noise schedules that control how fast data is destroyed.
# Each schedule computes alpha_t values for t = 0..T.
# alpha_t near 1 = mostly clean, alpha_t near 0 = mostly noise.

from dataclasses import dataclass

import torch
from torch import Tensor

from .base import Schedule

__all__ = ["Constant", "Linear", "Cosine", "Sqrt"]


# Same alpha value at every timestep. Simplest possible schedule.
@dataclass
class Constant(Schedule):
    value: float

    def compute(self) -> Tensor:
        return torch.full((self.steps + 1,), self.value)


# Alpha decreases evenly from `start` to `end` over T steps.
# Used in the original DDPM paper (Ho et al. 2020).
@dataclass
class Linear(Schedule):
    start: float
    end: float

    def compute(self) -> Tensor:
        return torch.linspace(self.start, self.end, self.steps + 1)


# Destroys information more gradually than Linear, especially early on.
# From "Improved DDPM" (Nichol & Dhariwal 2021).
@dataclass
class Cosine(Schedule):
    offset: float = 8e-3
    exponent: float = 2

    def compute(self) -> Tensor:
        t = torch.arange(self.steps + 2)
        # Compute cumulative noise level using a cosine curve.
        delta = ((t / (self.steps + 2) + self.offset) / (1 + self.offset) * torch.pi /
                   2).cos()**self.exponent
        # Back out per-step alpha from consecutive cumulative values.
        alpha = torch.clip(delta[1:] / delta[:-1], 1e-3, 1)
        return alpha


# Square root schedule — used for text/discrete diffusion.
@dataclass
class Sqrt(Schedule):
    offset: float = 8e-3

    def compute(self) -> Tensor:
        t = torch.arange(self.steps + 2)
        delta = 1 - torch.sqrt(t / (self.steps + 1) + self.offset)
        alpha = torch.clip(delta[1:] / delta[:-1], 0, 0.999)
        return alpha
