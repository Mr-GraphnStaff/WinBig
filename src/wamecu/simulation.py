"""Backward-compatible wrappers for simulation utilities."""

from __future__ import annotations

from .simulate import (
    BetaDriftConfig,
    beta_drift,
    simulate_draws,
    simulate_time_varying_draws,
    stream_draws,
)
from .utils import wamecu_probabilities

__all__ = [
    "BetaDriftConfig",
    "beta_drift",
    "simulate_draws",
    "simulate_time_varying_draws",
    "stream_draws",
    "wamecu_probabilities",
]
