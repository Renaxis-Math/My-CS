# base.py — Abstract contracts for every module in the diffusion system.
# Every other file will implement one of the base classes defined here.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar

import torch
import torch.nn as nn
from torch import Tensor
from typing_extensions import Self

from .utils.nn import Sequential


# Any probability distribution in the system must implement these 3 methods.
class Distribution(ABC):

    @abstractmethod
    def sample(self) -> tuple[Tensor, Optional[Tensor]]:
        """Draw a random sample from this distribution."""
        raise NotImplementedError

    @abstractmethod
    def nll(self, x: Tensor) -> Tensor:
        """Negative log-likelihood: how unlikely is x under this distribution?"""
        raise NotImplementedError

    @abstractmethod
    def dkl(self, other: Self) -> Tensor:
        """KL divergence: how different is this distribution from another?"""
        raise NotImplementedError

# a generic type variable so later code can say "this works with any Distribution subclass"
D = TypeVar("D", bound=Distribution, covariant=True)


# Container that holds everything about one training batch as it flows
# through the pipeline: raw data, encoded data, timesteps, noise,
# noisy input, model prediction, distributions, and loss.
@dataclass
class Batch(Generic[D]):
    device: torch.device
    w: Tensor = field(init=False)          # raw data (e.g. pixel values)
    x: Tensor = field(init=False)          # encoded data
    y: Tensor = field(init=False)          # labels (for conditional generation)
    t: Tensor = field(init=False)          # sampled timesteps
    epsilon: Optional[Tensor] = field(init=False)  # noise that was added
    z: Tensor = field(init=False)          # noisy version of x at timestep t
    hat: Tensor = field(init=False)        # model's prediction (denoised output)
    q: D = field(init=False)               # true posterior distribution
    p: D = field(init=False)               # model's approximate distribution
    l: Tensor = field(init=False)          # computed loss value

    def __setattr__(self, prop: str, val: Any):
        # Auto-move any tensor to the correct device when assigned.
        if isinstance(val, Tensor):
            if hasattr(self, prop):
                del self.__dict__[prop]
            val = val.to(self.device)
        super().__setattr__(prop, val)


# Bridge between raw data and tensor world.
# Subclasses define encode (raw -> tensor) and decode (tensor -> raw).
# Also handles batching and shuffling for the training loop.
@dataclass
class Data(ABC):
    w: Tensor                    # raw data tensor
    y: Optional[Tensor] = None   # optional labels
    batch: int = 1               # batch size
    shuffle: bool = False        # shuffle each epoch?

    @property
    def shape(self) -> tuple[int, ...]:
        # Shape of one encoded sample (used to know what size to generate).
        return self.encode(self.w[:1]).shape[1:]

    def parameters(self) -> Iterator[nn.Parameter]:
        # Collect trainable parameters from any nn.Module fields (e.g. learned embeddings).
        return chain.from_iterable(
            var.parameters() for var in vars(self) if isinstance(var, nn.Module))

    def __iter__(self) -> Iterator[tuple[Tensor, Tensor]]:
        if self.y is None:
            self.y = torch.zeros(self.w.shape[0], dtype=torch.int)
        if self.shuffle:
            index = torch.randperm(self.w.shape[0])
            self.w, self.y = self.w[index], self.y[index]
        self.data = zip(self.w.split(self.batch), self.y.split(self.batch))
        return self

    def __next__(self) -> tuple[Tensor, Tensor]:
        return next(self.data)

    def __len__(self) -> int:
        return -(self.w.shape[0] // -self.batch)

    @abstractmethod
    def encode(self, w: Tensor) -> Tensor:
        """Convert raw data to the tensor format diffusion operates on."""
        raise NotImplementedError

    @abstractmethod
    def decode(self, x: Tensor) -> Tensor:
        """Convert diffusion tensors back to raw data format."""
        raise NotImplementedError


# How to randomly sample timesteps during training.
class Time(ABC):

    @abstractmethod
    def sample(self, steps: int, size: int) -> Tensor:
        """Return a batch of random timesteps."""
        raise NotImplementedError


# Defines how noise level changes across T timesteps.
# Computes alpha_t values that control how much signal vs noise at each step.
@dataclass
class Schedule(ABC):
    steps: int

    @abstractmethod
    def compute(self) -> Tensor:
        """Compute alpha_t for t = 0, ..., T"""
        raise NotImplementedError

# The core diffusion process. Defines 4 key distributions:
#   stationary: q(x_T) — pure noise at the end
#   prior:      q(x_t | x_0) — noisy version of data at step t
#   posterior:  q(x_{t-1} | x_t, x_0) — true reverse step (needs x_0)
#   approximate: p(x_{t-1} | x_t) — model's learned reverse step
@dataclass
class Noise(ABC, Generic[D]):

    @abstractmethod
    def schedule(self, alpha: Tensor) -> None:
        """Precompute needed values from the noise schedule."""
        raise NotImplementedError

    @abstractmethod
    def stationary(self, shape: tuple[int, ...]) -> D:
        """Pure noise distribution q(x_T) — starting point for sampling."""
        raise NotImplementedError

    @abstractmethod
    def prior(self, x: Tensor, t: Tensor) -> D:
        """Forward process: q(x_t | x_0) — how to corrupt data."""
        raise NotImplementedError

    @abstractmethod
    def posterior(self, x: Tensor, z: Tensor, t: Tensor) -> D:
        """True reverse: q(x_{t-1} | x_t, x_0) — ideal denoising step."""
        raise NotImplementedError

    @abstractmethod
    def approximate(self, z: Tensor, t: Tensor, hat: Tensor) -> D:
        """Model's reverse: p(x_{t-1} | x_t) — learned denoising step."""
        raise NotImplementedError


# The denoising neural network. Takes noisy input (x), labels (y),
# and timestep (t), and outputs a prediction (denoised data or noise).
class Net(ABC, nn.Module):
    __call__: Callable[[Tensor, Tensor, Tensor], Tensor]

    @abstractmethod
    def forward(self, x: Tensor, y: Tensor, t: Tensor) -> Tensor:
        raise NotImplementedError

    def __or__(self, module: nn.Module) -> "Net":
        # Pipe operator: lets you do `net | Softmax()` to chain post-processing.
        return Sequential(self, module)  # type: ignore


# Optional conditioning strategy (e.g. classifier-free guidance).
# Just a marker base class — concrete subclass holds config like dropout/strength.
class Guidance(ABC):
    pass


# Training objective. Compares model output to ground truth.
# Supports arithmetic: you can combine losses like `Simple() + 0.001 * VLB()`.
class Loss(ABC, Generic[D]):

    @abstractmethod
    def compute(self, batch: Batch[D]) -> Tensor:
        raise NotImplementedError

    def __mul__(self, factor: float) -> "Mul[D]":
        return Mul(factor, self)

    def __rmul__(self, factor: float) -> "Mul[D]":
        return Mul(factor, self)

    def __truediv__(self, divisor: float) -> "Mul[D]":
        return Mul(1 / divisor, self)

    def __add__(self, other: "Loss[D]") -> "Add[D]":
        return Add(self, other)

    def __sub__(self, other: "Loss[D]") -> "Add[D]":
        return Add(self, Mul(-1, other))


# Helper: wraps a loss with a scalar multiplier.
@dataclass
class Mul(Loss[D]):
    factor: float
    loss: Loss[D]

    def compute(self, batch: Batch[D]) -> Tensor:
        return self.factor * self.loss.compute(batch)


# Helper: adds multiple losses together.
class Add(Loss[D]):

    def __init__(self, *losses: Loss[D]) -> None:
        self.losses = losses

    def compute(self, batch: Batch[D]) -> Tensor:
        sum = self.losses[0].compute(batch)
        for loss in self.losses[1:]:
            sum += loss.compute(batch)
        return sum
