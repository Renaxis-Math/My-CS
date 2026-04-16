# noise.py — The core diffusion process math.
# Defines how data is corrupted (forward) and denoised (reverse).
# This is where the actual diffusion equations live.

from abc import abstractmethod
from dataclasses import dataclass
from itertools import accumulate
from typing import Literal

import torch
from torch import Tensor

from .base import Noise
from .distribution import Categorical as Cat
from .distribution import Normal as N

__all__ = ["Gaussian", "Categorical"]


# Gaussian noise — the standard DDPM noise type for continuous data (images).
# Precomputes all coefficients from the schedule so forward/reverse are fast.
@dataclass
class Gaussian(Noise[N]):
    # What the model predicts: original data ("x"), noise ("epsilon"), or mean ("mu").
    parameter: Literal["x", "epsilon", "mu"] = "x"
    # How reverse variance is handled: fixed, interpolated range, or learned.
    variance: Literal["fixed", "range", "learned"] = "fixed"

    def schedule(self, alpha: Tensor) -> None:
        # Precompute all needed coefficients from the alpha schedule.
        # delta = cumulative product of alphas = how much original signal remains at step t.
        delta = alpha.cumprod(0)
        self.q1 = delta.sqrt()                                    # sqrt(alpha_bar_t)
        self.q2 = (1 - delta).sqrt()                              # sqrt(1 - alpha_bar_t)
        self.q3 = alpha.sqrt() * (1 - delta.roll(1)) / (1 - delta)  # posterior mean coeff for x_0
        self.q4 = delta.roll(1).sqrt() * (1 - alpha) / (1 - delta)  # posterior mean coeff for z
        self.q5 = ((1 - alpha) * (1 - delta.roll(1)) / (1 - delta)).sqrt()  # posterior std dev
        # Coefficients for model's reverse step depend on what it predicts.
        if self.parameter == "x":
            self.p1, self.p2 = self.q3, self.q4
        elif self.parameter == "epsilon":
            self.p1 = 1 / alpha.sqrt()
            self.p2 = (alpha - 1) / ((1 - delta).sqrt() * alpha.sqrt())
        else:
            self.p1, self.p2 = torch.zeros(alpha.shape), torch.ones(alpha.shape)
        self.p3 = (1 - alpha).log()    # log variance upper bound
        self.p4 = self.q5.log()        # log variance lower bound

    def stationary(self, shape: tuple[int, ...]) -> N:
        # q(x_T): pure standard Gaussian noise. Sampling starts here.
        return N(torch.zeros(shape), torch.ones(shape))

    def prior(self, x: Tensor, t: Tensor) -> N:
        # q(x_t | x_0): forward process — corrupt clean data x at timestep t.
        # x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * noise
        t = t.view(-1, *(1,) * (x.dim() - 1))
        return N(self.q1[t] * x, self.q2[t])

    def posterior(self, x: Tensor, z: Tensor, t: Tensor) -> N:
        # q(x_{t-1} | x_t, x_0): true reverse step (requires knowing x_0).
        # This is the "ideal" answer the model is trying to match.
        t = t.view(-1, *(1,) * (x.dim() - 1))
        return N(self.q3[t] * z + self.q4[t] * x, self.q5[t])

    def approximate(self, z: Tensor, t: Tensor, hat: Tensor) -> N:
        # p(x_{t-1} | x_t): model's learned reverse step.
        # Uses the model's prediction (hat) instead of the unknown x_0.
        t = t.view(-1, *(1,) * (z.dim() - 1))
        return N(
            self.p1[t] * z + self.p2[t] * hat[0],
            self.q5[t]
            if self.variance == "fixed"
            else torch.exp(hat[1] * self.p3[t] + (1 - hat[1]) * self.p4[t])
            if self.variance == "range"
            else hat[1],
        )


# Base for discrete/categorical noise — corrupts tokens via transition matrices.
# Instead of adding continuous noise, tokens randomly flip to other tokens.
class Categorical(Noise[Cat]):
    @abstractmethod
    def q(self, t: Tensor) -> Tensor:
        """One-step transition matrix at time t."""
        raise NotImplementedError

    @abstractmethod
    def r(self, t: Tensor) -> Tensor:
        """Cumulative transition matrix from step 0 to t."""
        raise NotImplementedError

    def prior(self, x: Tensor, t: Tensor) -> Cat:
        # q(x_t | x_0): multiply one-hot x by cumulative transition matrix.
        return Cat(x @ self.r(t))

    def posterior(self, x: Tensor, z: Tensor, t: Tensor) -> Cat:
        # q(x_{t-1} | x_t, x_0): Bayes' rule combining forward and reverse.
        return Cat(
            (z @ self.q(t).transpose(1, 2))
            * (x @ self.r(t - 1))
            / (x @ self.r(t) * z).sum(2, keepdim=True)
        )

    def approximate(self, z: Tensor, t: Tensor, hat: Tensor) -> Cat:
        # p(x_{t-1} | x_t): use model's predicted x_0 (hat) in place of true x_0.
        return self.posterior(hat[0], z, t)


# Stores all transition matrices in memory. Simple but uses lots of RAM.
class MemoryInefficientCategorical(Categorical):
    def schedule(self, alpha: Tensor) -> None:
        self._q = self.transition(alpha)
        # Cumulative product of transition matrices.
        self._r = torch.stack([*accumulate(self._q, torch.mm)])

    @abstractmethod
    def transition(self, alpha: Tensor) -> Tensor:
        """Build the transition matrix from the alpha schedule."""
        raise NotImplementedError

    def q(self, t: Tensor) -> Tensor:
        return self._q[t]

    def r(self, t: Tensor) -> Tensor:
        return self._r[t]


# Computes transition matrices on-the-fly instead of storing them all.
# Uses formula: Q_t = alpha_t * I + (1 - alpha_t) * A, where A is the "target" matrix.
@dataclass
class MemoryEfficientCategorical(Categorical):
    k: int  # number of categories (vocabulary size)

    def schedule(self, alpha: Tensor) -> None:
        self.alpha = alpha.view(-1, 1, 1)
        self.delta = self.alpha.cumprod(0)       # cumulative alpha
        self.i = torch.eye(self.k, device=alpha.device)[None]  # identity matrix

    @property
    @abstractmethod
    def a(self) -> Tensor:
        """Target distribution matrix — where tokens drift toward."""
        raise NotImplementedError

    def q(self, t: Tensor) -> Tensor:
        # One-step transition: mix between identity (stay) and target (flip).
        return self.alpha[t] * self.i + (1 - self.alpha[t]) * self.a

    def r(self, t: Tensor) -> Tensor:
        # Cumulative transition: same formula but with cumulative alpha.
        return self.delta[t] * self.i + (1 - self.delta[t]) * self.a


# Tokens can flip to any token with equal probability.
class Uniform(MemoryEfficientCategorical):
    @property
    def a(self) -> Tensor:
        # Each token equally likely — uniform 1/k matrix.
        return torch.ones(self.k, self.k, device=self.i.device) / self.k

    def stationary(self, shape: tuple[int, ...]) -> Cat:
        # At t=T, every token is equally likely.
        return Cat(torch.full(shape, 1 / self.k))


# Tokens can only flip to one special "mask" token (index m).
# Like masked language modeling — tokens get progressively masked out.
@dataclass
class Absorbing(MemoryEfficientCategorical):
    m: int = -1  # index of the mask/absorbing token (default: last token)

    @property
    def a(self) -> Tensor:
        # Every row points to the mask token — all tokens drift toward it.
        return self.i[:, self.m].repeat(1, self.k, 1)

    def stationary(self, shape: tuple[int, ...]) -> Cat:
        # At t=T, everything is the mask token.
        return Cat(torch.eye(self.k)[self.m].repeat(*shape[:-1], 1))
