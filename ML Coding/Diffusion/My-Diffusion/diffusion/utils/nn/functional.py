# functional.py — Function-form neural network helpers.
# Keeps simple math functions separate from nn.Module classes.

import torch
from torch import Tensor


def swish(x: Tensor) -> Tensor:
    # Smooth activation: x * sigmoid(x). Alternative to ReLU.
    return x * torch.sigmoid(x)
