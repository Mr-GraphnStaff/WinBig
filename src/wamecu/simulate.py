"""Simulation utilities focused on beta drift and streaming draws."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .utils import wamecu_probabilities


@dataclass
class BetaDriftConfig:
    """Configuration for :func:`beta_drift`.

    Attributes
    ----------
    n_steps:
        Number of time steps to simulate.
    n_outcomes:
        Number of categorical outcomes.
    walk_scale:
        Standard deviation of the Gaussian random walk increment.
    sin_amplitude:
        Amplitude of the sinusoidal component applied to the first outcome.
    sin_period:
        Period of the sinusoidal component in steps. Values <= 0 disable the
        sinusoid.
    clip:
        Maximum absolute value for :math:`\beta` to keep probabilities valid.
    seed:
        Optional random seed for reproducibility.
    """

    n_steps: int
    n_outcomes: int
    walk_scale: float = 0.03
    sin_amplitude: float = 0.08
    sin_period: int = 120
    clip: float = 0.95
    seed: int | None = 7


def beta_drift(config: BetaDriftConfig) -> np.ndarray:
    """Generate a reproducible time series of drifting :math:`\beta` vectors.

    The first outcome experiences an additional sinusoidal term to model a
    cyclical mechanical bias, while the remaining outcomes follow a centered
    random walk. The resulting series is mean-centered at each step and clipped
    to ``[-config.clip, config.clip]``.
    """

    if config.n_outcomes < 2:
        raise ValueError("n_outcomes must be at least 2")
    if config.n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if not 0 < config.clip < 1:
        raise ValueError("clip must be between 0 and 1")

    rng = np.random.default_rng(config.seed)
    betas = np.zeros((config.n_steps, config.n_outcomes), dtype=float)
    current = np.zeros(config.n_outcomes, dtype=float)

    phase = rng.uniform(0, 2 * np.pi)
    for t in range(config.n_steps):
        noise = rng.normal(0.0, config.walk_scale, size=config.n_outcomes)
        current += noise
        current -= current.mean()

        if config.sin_period > 0 and config.sin_amplitude != 0:
            sinusoid = config.sin_amplitude * np.sin(
                2 * np.pi * t / config.sin_period + phase
            )
            current[0] += sinusoid

        current = np.clip(current, -config.clip, config.clip)
        betas[t] = current

    return betas


def stream_draws(
    beta_series: Sequence[Sequence[float]],
    seed: int | None = None,
) -> np.ndarray:
    """Simulate streaming categorical draws for each :math:`\beta_t`."""

    beta_array = np.asarray(beta_series, dtype=float)
    if beta_array.ndim != 2:
        raise ValueError("beta_series must be 2D with shape (steps, outcomes)")

    n_steps, n_outcomes = beta_array.shape
    draws = np.empty(n_steps, dtype=int)
    rng = np.random.default_rng(seed)

    for t in range(n_steps):
        probs = wamecu_probabilities(n_outcomes, beta_array[t])
        draws[t] = rng.choice(n_outcomes, p=probs)

    return draws


def simulate_draws(
    probabilities: Iterable[float],
    n_trials: int,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate i.i.d. draws from a fixed probability vector."""

    probs = np.asarray(list(probabilities), dtype=float)
    if probs.ndim != 1:
        raise ValueError("probabilities must be 1D")
    if np.any(probs < 0):
        raise ValueError("probabilities must be non-negative")
    total = probs.sum()
    if not np.isclose(total, 1.0):
        probs = probs / total
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")

    rng = np.random.default_rng(seed)
    support = np.arange(probs.size)
    return rng.choice(support, size=n_trials, p=probs)


def simulate_time_varying_draws(
    beta_series: Sequence[Sequence[float]],
    seed: int | None = None,
) -> np.ndarray:
    """Backward compatible alias for :func:`stream_draws`."""

    return stream_draws(beta_series, seed=seed)


__all__ = [
    "BetaDriftConfig",
    "beta_drift",
    "simulate_draws",
    "simulate_time_varying_draws",
    "stream_draws",
]
