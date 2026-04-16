# loss.py — Training objectives that measure how wrong the model's prediction is.
# Can be combined: Simple("epsilon") + 0.001 * VLB()

from dataclasses import dataclass
from typing import Callable, Literal, TypeVar

import torch
from torch import Tensor

from .base import Batch, Distribution, Loss

__all__ = ["Lambda", "Simple", "VLB"]

D = TypeVar("D", bound=Distribution)


# Custom loss: pass any function that takes a Batch and returns a scalar.
# Useful for adding extra regularization or experimental losses.
@dataclass
class Lambda(Loss[D]):
    function: Callable[[Batch[D]], Tensor]

    def compute(self, batch: Batch[D]) -> Tensor:
        return self.function(batch)


# Simple MSE loss from DDPM (Ho et al. 2020).
# Compares model's prediction to either the clean data ("x") or the noise ("epsilon").
@dataclass
class Simple(Loss[Distribution]):
    parameter: Literal["x", "epsilon"] = "x"
    index = 0

    def compute(self, batch: Batch[Distribution]) -> Tensor:
        # Mean squared error between target (x or epsilon) and prediction (hat).
        return torch.mean((getattr(batch, self.parameter) - batch.hat[self.index])**2)


# Variational Lower Bound loss — theoretically grounded.
# Uses KL divergence between true posterior q and model's approximate p.
# At t=1 uses negative log-likelihood instead (boundary case).
class VLB(Loss[Distribution]):

    def compute(self, batch: Batch[Distribution]) -> Tensor:
        t = batch.t.view(-1, *(1,) * (batch.x.ndim - 1))
        # KL divergence for t > 1, negative log-likelihood for t = 1.
        return batch.q.dkl(batch.p).where(t > 1, batch.p.nll(batch.x)).mean()
