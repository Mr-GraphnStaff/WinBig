"""Simulation helpers implementing the WAMECU probability law."""
from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def wamecu_probabilities(n_outcomes: int, beta: Iterable[float]) -> np.ndarray:
    """Convert bias coefficients into a normalized probability distribution."""
    beta_array = np.asarray(list(beta), dtype=float)
    if beta_array.size != n_outcomes:
        raise ValueError("beta vector must match number of outcomes")

    base = np.full(n_outcomes, 1.0 / n_outcomes)
    adjusted = base * (1 + beta_array)

    if np.any(adjusted < 0):
        raise ValueError("bias coefficients yield negative probabilities")

    total = adjusted.sum()
    if total <= 0:
        raise ValueError("bias coefficients collapse the probability mass")

    if not math.isclose(total, 1.0):
        adjusted = adjusted / total
    return adjusted


def simulate_draws(probabilities: np.ndarray, n_trials: int, seed: int | None = None) -> np.ndarray:
    """Simulate draws from a categorical distribution defined by ``probabilities``."""
    if n_trials <= 0:
        raise ValueError("n_trials must be positive")
    rng = np.random.default_rng(seed)
    support = np.arange(probabilities.size)
    return rng.choice(support, size=n_trials, p=probabilities)
