# __init__.py — The Model class that glues all modules together.
# This is the main entry point: you plug in data, schedule, noise, net, loss
# and get train() and sample() methods.

import sys
from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Callable, Generic, Iterator, Optional, TypeVar

import torch
import torch.nn as nn
from torch import Tensor
from torch.optim import Adam, Optimizer
from tqdm import tqdm

from . import data, guidance, loss, net, noise, schedule, time
from .base import Batch, Data, Distribution, Guidance, Loss, Net, Noise, Schedule, Time
from .time import Discrete

__all__ = ["data", "loss", "net", "noise", "schedule", "time", "Model"]

D = TypeVar("D", bound=Distribution, covariant=True)


@dataclass
class Model(Generic[D]):
    # The 6 pluggable modules — this is the "LEGO set".
    data: Data
    schedule: Schedule
    noise: Noise[D]
    net: Net
    loss: Loss[D]
    time: Time = field(default_factory=Discrete)         # default: uniform random
    guidance: Optional[Guidance] = None                   # optional conditioning
    optimizer: Optional[Optimizer | Callable[..., Optimizer]] = None
    device: str | torch.device = torch.device("cpu")
    compile: bool = True

    @torch.no_grad()
    def __post_init__(self):
        # Wire everything together: compute schedule, set up optimizer, move to device.
        self.noise.schedule(self.schedule.compute().to(self.device))
        parameters = chain(self.data.parameters(), self.net.parameters())
        if self.optimizer is None:
            self.optimizer = Adam(parameters, lr=1e-4)
        elif callable(self.optimizer):
            self.optimizer = self.optimizer(parameters)
        self.net = self.net.to(self.device)
        for name, value in vars(self.data).items():
            if isinstance(value, nn.Module):
                setattr(self.data, name, value.to(self.device))
        if self.compile and sys.version_info < (3, 11):
            self.net = torch.compile(self.net)  # type: ignore[union-attr]
        if isinstance(self.device, str):
            self.device = torch.device(self.device)

    @torch.enable_grad()
    def train(self, epochs: int = 1, progress: bool = True) -> Iterator[float]:
        """Train the model. Yields loss after each epoch for validation loops."""
        self.net.train()
        batch = Batch[D](self.device)  # type: ignore[union-attr]
        for _ in range(epochs):
            bar = tqdm(self.data, disable=not progress)
            for batch.w, batch.y in self.data:
                # Classifier-free guidance: randomly drop labels during training.
                if isinstance(self.guidance, guidance.ClassifierFree):
                    i = torch.randperm(batch.y.shape[0])
                    batch.y[i[:int(batch.y.shape[0] * self.guidance.dropout)]] = 0
                # Encode raw data, sample timesteps, corrupt with noise.
                batch.x = self.data.encode(batch.w)
                batch.t = self.time.sample(self.schedule.steps, batch.x.shape[0])
                batch.z, batch.epsilon = self.noise.prior(batch.x, batch.t).sample()
                # Model predicts from noisy input.
                batch.hat = self.net(batch.z, batch.y, batch.t)
                # Compute true and approximate posterior distributions.
                batch.q = self.noise.posterior(batch.x, batch.z, batch.t)
                batch.p = self.noise.approximate(batch.z, batch.t, batch.hat)
                # Compute loss and backpropagate.
                batch.l = self.loss.compute(batch)
                self.optimizer.zero_grad()  # type: ignore[union-attr]
                batch.l.backward()
                self.optimizer.step()  # type: ignore[union-attr]
                bar.set_postfix(loss=f"{batch.l.item():.2e}")
                bar.update()
            bar.close()
            yield batch.l.item()

    @torch.no_grad()
    def sample(
        self,
        y: Optional[Tensor] = None,
        batch: int = 1,
        progress: bool = True,
    ) -> Tensor:
        """Generate samples by reversing the noise process step by step."""
        self.net.eval()
        if y is None:
            shape = 1, *(() if self.data.y is None else self.data.y.shape[1:])
            y = torch.zeros(shape, dtype=torch.int, device=self.device)
        y = y.repeat_interleave(batch, 0).to(self.device)
        # Start from pure noise.
        pi = self.noise.stationary((y.shape[0], *self.data.shape))
        z = pi.sample()[0].to(self.device)
        l = self.data.decode(z)[None]
        bar = tqdm(total=self.schedule.steps, disable=not progress)
        # Reverse step by step from t=T down to t=1.
        for t in range(self.schedule.steps, 0, -1):
            t = torch.full((batch,), t, device=self.device)
            hat = self.net(z, y, t)
            # Classifier-free guidance: amplify conditional signal at sampling time.
            if isinstance(self.guidance, guidance.ClassifierFree):
                s = self.guidance.strength
                hat = (1 + s) * hat - s * self.net(z, torch.zeros_like(y), t)
            z, _ = self.noise.approximate(z, t, hat).sample()
            w = self.data.decode(z)
            l = torch.cat((l, w[None]), 0)
            bar.update()
        bar.close()
        return l

    @torch.no_grad()
    def inpaint(
        self,
        x_known: Tensor,
        mask: Tensor,
        y: Optional[Tensor] = None,
        batch: int = 1,
        progress: bool = True,
    ) -> Tensor:
        """Conditional generation via inpainting.

        Given partial known data (e.g. one stock's returns), generate the
        unknown parts (e.g. another stock's returns) that are consistent
        with the known parts under the learned joint distribution.

        Args:
            x_known: the known data, same shape as one training sample.
                     Unknown positions can be anything (will be overwritten).
            mask:    binary tensor, same shape as x_known.
                     1 = known (will be forced), 0 = unknown (will be generated).
            y:       optional labels (usually None for joint approach).
            batch:   number of samples to generate per known input.
        """
        self.net.eval()
        x_known = x_known.to(self.device)
        mask = mask.to(self.device)
        if y is None:
            shape = x_known.shape[0], *(() if self.data.y is None else self.data.y.shape[1:])
            y = torch.zeros(shape, dtype=torch.int, device=self.device)
        x_known = x_known.repeat_interleave(batch, 0)
        mask = mask.repeat_interleave(batch, 0)
        y = y.repeat_interleave(batch, 0).to(self.device)
        # Start from pure noise.
        z = self.noise.stationary((y.shape[0], *self.data.shape)).sample()[0].to(self.device)
        bar = tqdm(total=self.schedule.steps, disable=not progress)
        for t_val in range(self.schedule.steps, 0, -1):
            t = torch.full((z.shape[0],), t_val, device=self.device)
            # Model denoises everything freely.
            hat = self.net(z, y, t)
            if isinstance(self.guidance, guidance.ClassifierFree):
                s = self.guidance.strength
                hat = (1 + s) * hat - s * self.net(z, torch.zeros_like(y), t)
            z_model, _ = self.noise.approximate(z, t, hat).sample()
            # Noise the known data to the current timestep level.
            z_known, _ = self.noise.prior(self.data.encode(x_known), t).sample()
            # Replace: keep known channels from noised real data,
            # keep unknown channels from model's denoising.
            z = mask * z_known + (1 - mask) * z_model
            bar.update()
        bar.close()
        return self.data.decode(z)

    @torch.no_grad()
    def load(self, path: Path | str):
        """Load saved model weights."""
        state = torch.load(path)
        self.net.load_state_dict(state["net"])
        for name, dict in state["data"].items():
            getattr(self.data, name).load_state_dict(dict)

    @torch.no_grad()
    def save(self, path: Path | str):
        """Save model weights."""
        state = {
            "net": self.net.state_dict(),
            "data": {
                name: value.state_dict()
                for name, value in vars(self.data).items()
                if isinstance(value, nn.Module)
            }
        }
        torch.save(state, path)
