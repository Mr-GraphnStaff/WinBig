"""Adaptive estimation utilities for WAMECU bias coefficients."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


def simulate_beta_drift(
    n_outcomes: int,
    n_steps: int,
    drift: str = "random_walk",
    scale: float = 0.05,
    clip: float = 0.8,
    seed: int | None = None,
) -> np.ndarray:
    """Generate a time series of :math:`\beta` coefficients.

    The simulated drift is centered to keep the implied probabilities valid.
    ``clip`` controls the maximum absolute value to avoid negative
    probabilities.
    """

    if n_outcomes <= 1:
        raise ValueError("n_outcomes must be greater than 1")
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if clip <= 0 or clip >= 1:
        raise ValueError("clip must be in (0, 1)")

    rng = np.random.default_rng(seed)
    betas = np.zeros((n_steps, n_outcomes), dtype=float)

    if drift == "random_walk":
        current = np.zeros(n_outcomes, dtype=float)
        for t in range(n_steps):
            current += rng.normal(0.0, scale, size=n_outcomes)
            current -= current.mean()
            current = np.clip(current, -clip, clip)
            betas[t] = current
    elif drift == "sinusoidal":
        time = np.arange(n_steps)
        frequencies = rng.uniform(0.5, 1.5, size=n_outcomes)
        phases = rng.uniform(0, 2 * np.pi, size=n_outcomes)
        amplitudes = rng.normal(scale, scale / 3, size=n_outcomes)
        for i in range(n_outcomes):
            betas[:, i] = amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * time / n_steps + phases[i])
        betas -= betas.mean(axis=1, keepdims=True)
        betas = np.clip(betas, -clip, clip)
    else:
        raise ValueError("unsupported drift type")

    return betas


@dataclass
class AdaptiveBetaEstimator:
    """Exponentially weighted estimator for streaming :math:`\beta` values."""

    n_outcomes: int
    smoothing: float = 0.05

    def __post_init__(self) -> None:
        if self.n_outcomes <= 1:
            raise ValueError("n_outcomes must be greater than 1")
        if not (0 < self.smoothing <= 1):
            raise ValueError("smoothing must be in (0, 1]")

        self._probabilities = np.full(self.n_outcomes, 1.0 / self.n_outcomes)
        self.beta_ = np.zeros(self.n_outcomes)

    @property
    def probabilities_(self) -> np.ndarray:
        return self._probabilities

    def update(self, observation: int) -> np.ndarray:
        if not 0 <= observation < self.n_outcomes:
            raise ValueError("observation index out of bounds")

        one_hot = np.zeros(self.n_outcomes)
        one_hot[observation] = 1.0
        self._probabilities = (1 - self.smoothing) * self._probabilities + self.smoothing * one_hot
        self._probabilities = np.maximum(self._probabilities, 1e-9)
        self._probabilities /= self._probabilities.sum()

        baseline = 1.0 / self.n_outcomes
        self.beta_ = self._probabilities / baseline - 1.0
        return self.beta_.copy()

    def batch_update(self, observations: Iterable[int]) -> np.ndarray:
        history = []
        for obs in observations:
            history.append(self.update(int(obs)))
        return np.asarray(history)
