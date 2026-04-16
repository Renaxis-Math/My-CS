# net.py — Denoising neural networks.
# These are the trainable models that learn to reverse the noise process.
# UNet for images, Transformer for sequences/text.

from typing import Sequence

import torch
from einops.layers.torch import Rearrange
from torch import Tensor
from torch.nn import (
    Conv2d,
    Embedding,
    GroupNorm,
    Identity,
    LayerNorm,
    Linear,
    Module,
    ModuleList,
    MultiheadAttention,
    Sequential,
    SiLU,
    Upsample,
)
from torch.nn.functional import pad, silu
from torchvision.transforms.functional import crop

from .base import Net
from .utils.nn import FastGELU, SinusoidalPositionalEmbedding, WeightStdConv2d, Swish

__all__ = ["UNet", "Transformer"]


# ============================================================
# UNet — The classic diffusion architecture for images.
# Structure: Encoder (downsample) -> Bottleneck -> Decoder (upsample)
# with skip connections between encoder and decoder at each level.
# ============================================================

class UNet(Net):

    # A single residual block: two convolutions + timestep/label conditioning.
    # The conditioning vector (c) scales and shifts the hidden features
    # so the network behaves differently at different noise levels.
    class Block(Module):

        def __init__(self, hidden: int, channels: tuple[int, int], groups: int) -> None:
            super().__init__()
            self.linear = Linear(hidden, 2 * channels[1])  # produces scale (a) and shift (b)
            self.conv1 = WeightStdConv2d(*channels, 3, 1, 1)
            self.norm1 = GroupNorm(groups, channels[1])
            self.conv2 = WeightStdConv2d(channels[1], channels[1], 3, 1, 1)
            self.norm2 = GroupNorm(groups, channels[1])

        def forward(self, x: Tensor, c: Tensor) -> Tensor:
            # c -> scale (a) and shift (b) via linear + activation.
            a, b = torch.chunk(silu(self.linear(c))[..., None, None], 2, 1)
            # Conv -> Norm -> condition with (a, b) -> activate.
            x = silu(self.norm1(self.conv1(x)) * (a + 1) + b)
            x = silu(self.norm2(self.conv2(x)))
            return x

    # Self-attention layer — lets the network look at the entire image at once,
    # capturing long-range dependencies that convolutions miss.
    class Attention(Module):

        def __init__(self, hidden: int, heads: int) -> None:
            super().__init__()
            self.attention = MultiheadAttention(hidden, heads)

        def forward(self, x: Tensor) -> Tensor:
            shape = x.shape
            x = x.flatten(2).permute(2, 0, 1)  # (B,C,H,W) -> (H*W, B, C)
            x, _ = self.attention(x, x, x, need_weights=False)
            x = x.permute(1, 2, 0).reshape(shape)  # back to (B,C,H,W)
            return x

    def __init__(
        self,
        channels: Sequence[int],
        labels: int = 0,
        parameters: int = 1,
        hidden: int = 256,
        heads: int = 8,
        groups: int = 16,
    ) -> None:
        super().__init__()
        # Embed label and timestep into a shared conditioning vector.
        self.label = Embedding(labels + 1, hidden)
        self.time = SinusoidalPositionalEmbedding(hidden)
        # Initial convolution to go from input channels to first hidden channels.
        self.input = Conv2d(channels[0], channels[1], 3, 1, 1)
        # Encoder: progressively downsample, doubling channels at each level.
        self.encoder = ModuleList([
            ModuleList([
                UNet.Block(hidden, 2 * (channels_[0],), groups),
                UNet.Block(hidden, 2 * (channels_[0],), groups),
                UNet.Attention(channels_[0], heads),
                GroupNorm(groups, channels_[0]),
                Sequential(
                    Rearrange("b c (h p1) (w p2) -> b (c p1 p2) h w", p1=2, p2=2) if
                    (last := channels_[1] < channels[-1]) else Identity(),
                    Conv2d(channels_[0] * (1 + 3 * last), channels_[1], 1),
                )
            ]) for channels_ in zip(channels[1:], channels[2:])
        ])
        # Bottleneck: process at the lowest resolution.
        self.bottleneck = ModuleList([
            UNet.Block(hidden, (channels[-1], channels[-1]), groups),
            UNet.Attention(channels[-1], heads),
            UNet.Block(hidden, (channels[-1], channels[-1]), groups),
        ])
        # Decoder: progressively upsample, using skip connections from encoder.
        self.decoder = ModuleList([
            ModuleList([
                UNet.Block(hidden, (sum(channels_), channels_[0]), groups),
                UNet.Block(hidden, (sum(channels_), channels_[0]), groups),
                UNet.Attention(channels_[0], heads),
                GroupNorm(groups, channels_[0]),
                Sequential(
                    Upsample(None, 2, "nearest")
                    if channels_[1] > channels[1] else Identity(),
                    Conv2d(channels_[0], channels_[1], 3, 1, 1),
                )
            ]) for channels_ in zip(channels[:1:-1], channels[-2::-1])
        ])
        # Final convolution to go from hidden channels back to output.
        self.output = Sequential(
            Conv2d(channels[1], parameters * channels[0], 3, 1, 1),
            Rearrange("b (p c) h w -> p b c h w", p=parameters),
        )

    def forward(self, x: Tensor, y: Tensor, t: Tensor) -> Tensor:
        x = self.input(x)
        # Combine label embedding + timestep embedding into conditioning vector.
        c = self.label(y) + self.time(t)
        # Encoder: process and save features for skip connections.
        h = list[Tensor]()
        for block1, block2, attention, norm, transform in self.encoder:  # type: ignore[assignment]
            x = block1(x, c)
            h.append(x)
            x = block2(x, c)
            x = attention(norm(x)) + x  # attention with residual connection
            h.append(x)
            x = pad(x, (0, x.shape[2] % 2, 0, x.shape[3] % 2))
            x = transform(x)  # downsample
        # Bottleneck.
        x = self.bottleneck[0](x, c)
        x = self.bottleneck[1](x)
        x = self.bottleneck[2](x, c)
        # Decoder: upsample and concatenate skip connections from encoder.
        for block1, block2, attention, norm, transform in self.decoder:  # type: ignore[assignment]
            x = crop(x, 0, 0, *h[-1].shape[2:])
            x = block1(torch.cat((x, h.pop()), 1), c)  # skip connection
            x = block2(torch.cat((x, h.pop()), 1), c)  # skip connection
            x = attention(norm(x)) + x
            x = transform(x)  # upsample
        x = self.output(x)
        return x


# ============================================================
# Transformer — Alternative architecture, used for sequences/text
# and also for image generation with patch-based approaches.
# ============================================================

class Transformer(Net):

    # A single Transformer block with self-attention + MLP,
    # both conditioned on timestep/label via scale-and-shift (AdaLN).
    class Block(Module):

        def __init__(self, width: int, heads: int) -> None:
            super().__init__()
            self.mlp1 = Sequential(SiLU(), Linear(width, 6 * width))  # produces 6 conditioning values
            self.norm1 = LayerNorm(width)
            self.attn = MultiheadAttention(width, heads, batch_first=True)
            self.norm2 = LayerNorm(width)
            self.mlp2 = Sequential(
                Linear(width, width * 4),
                FastGELU(),
                Linear(width * 4, width),
            )

        def forward(self, x: Tensor, c: Tensor) -> Tensor:
            # 6 conditioning values: scale/shift for attention, scale/shift for MLP.
            a, b, c, d, e, f = torch.chunk(self.mlp1(c)[:, None], 6, 2)
            x = x + a * self.attn(*[b * self.norm1(x) + c] * 3, need_weights=False)[0]
            x = x + d * self.mlp2(e * self.norm2(x) + f)
            return x

    def __init__(
        self,
        input: int,
        labels: int = 0,
        context_dim: int = 0,
        parameters: int = 1,
        depth: int = 6,
        width: int = 256,
        heads: int = 8,
    ) -> None:
        super().__init__()
        self.linear1 = Linear(input, width)        # project input to hidden dim
        self.position = SinusoidalPositionalEmbedding(width)  # sequence position
        # labels > 0: discrete conditioning (class labels via Embedding)
        # context_dim > 0: continuous conditioning (e.g. another stock's returns via Linear)
        if context_dim > 0:
            self.label = Linear(context_dim, width)
        else:
            self.label = Embedding(labels + 1, width)
        self.time = SinusoidalPositionalEmbedding(width)      # timestep embedding
        self.blocks = Sequential(
            *[Transformer.Block(width, heads) for _ in range(depth)])
        self.linear2 = Linear(width, input * parameters)      # project back to input dim
        self.rearrange = Rearrange("b l (p e) -> p b l e", p=parameters)

    def forward(self, x: Tensor, y: Tensor, t: Tensor) -> Tensor:
        # Add positional encoding to input, combine label + timestep for conditioning.
        x = self.linear1(x) + self.position(torch.arange(x.shape[1], device=x.device))
        c = self.label(y) + self.time(t)
        for block in self.blocks:
            x = block(x, c)
        return self.rearrange(self.linear2(x))
