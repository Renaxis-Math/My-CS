# guidance.py — Conditioning strategy for controlled generation.
# Classifier-free guidance: train with random label dropout,
# then at sampling time amplify the conditional signal to steer output.

from dataclasses import dataclass

from .base import Guidance

__all__ = ["ClassifierFree"]


# Config for classifier-free guidance.
# dropout: fraction of labels randomly set to 0 during training (e.g. 0.1 = 10%).
# strength: how strongly to push toward the target class at sampling time (e.g. 2.0).
#   Higher strength = more on-target but less diverse samples.
@dataclass
class ClassifierFree(Guidance):
    dropout: float
    strength: float
