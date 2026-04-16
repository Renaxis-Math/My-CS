# utils/nn/__init__.py — Custom PyTorch layers used by the denoising networks.
# These fill gaps where standard PyTorch modules don't quite fit.

from typing import Any, Callable

import torch
from torch import Tensor
from torch.nn import Conv2d, Module, Parameter
from torch.nn import Sequential as _Sequential
from torch.nn.functional import conv2d

__all__ = [
    "FastGELU",
    "Lambda",
    "WeightStdConv2d",
    "Swish",
    "SinusoidalPositionalEmbedding",
]


# Custom Sequential that can pass multiple arguments (e.g. x and t) through.
# PyTorch's built-in Sequential only supports a single input.
class Sequential(_Sequential):

    def forward(self, *input: Any) -> Any:
        for module in self._modules.values():
            if type(input) == tuple:
                input = module(*input)
            else:
                input = module(input)
        return input


# Wraps any function into an nn.Module so it can be used inside Sequential.
class Lambda(Module):

    def __init__(self, function: Callable[..., Any]):
        super().__init__()
        self.function = function

    def forward(self, *input: Any):  # type: ignore
        return self.function(*input)


# Conv2d that normalizes its weights to have zero mean and unit variance
# before each forward pass. Stabilizes training in deep networks.
class WeightStdConv2d(Conv2d):

    def forward(self, input: Tensor) -> Tensor:
        mean = self.weight.mean((1, 2, 3), keepdim=True)
        var = self.weight.var((1, 2, 3), unbiased=False, keepdim=True)
        return conv2d(
            input,
            (self.weight - mean) * var.rsqrt(),  # standardized weights
            self.bias,
            self.stride,
            self.padding,
            self.dilation,
            self.groups,
        )


# Encodes a scalar timestep into a high-dimensional vector using sin/cos waves.
# This is how the network knows "how noisy is this input?"
# Same concept as positional encoding in Transformers.
class SinusoidalPositionalEmbedding(Module):

    def __init__(self, size: int = 32, base: float = 1e4) -> None:
        super().__init__()
        # Frequencies at different scales so each dimension captures different info.
        self.w = Parameter(base**torch.arange(0, -1, -2 / size)[None])

    def forward(self, t: Tensor) -> Tensor:
        wt = self.w * t[:, None]
        # Interleave sin and cos to produce final embedding.
        return torch.stack((wt.sin(), wt.cos()), 2).flatten(1)


# Fast approximation of GELU activation. Used in Transformer blocks.
# GELU is like ReLU but smooth — doesn't hard-clip at zero.
class FastGELU(Module):

    def forward(self, x: Tensor) -> Tensor:
        return x * torch.sigmoid(1.702 * x)


# Swish activation as nn.Module. Used in UNet blocks.
# Same as functional.swish but usable inside Sequential.
class Swish(Module):

    def forward(self, x: Tensor) -> Tensor:
        return x * torch.sigmoid(x)
