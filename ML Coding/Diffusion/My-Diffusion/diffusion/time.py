# time.py — How timesteps are sampled during training.
# During training, each sample in the batch gets a random timestep.
# The model learns to denoise at all timesteps by seeing random ones.

from dataclasses import dataclass

import torch
from torch import Tensor

from .base import Time


# Uniform random timestep sampling between 1 and T.
@dataclass
class Discrete(Time):

    def sample(self, steps: int, size: int) -> Tensor:
        # Pick `size` random integers from 1 to `steps` (inclusive).
        # Each sample in the batch gets its own random timestep.
        return torch.randint(1, steps + 1, (size,))
