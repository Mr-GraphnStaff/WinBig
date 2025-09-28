"""Simulation helpers implementing the WAMECU probability law."""
from __future__ import annotations

import math
from typing import Iterable, Sequence

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


def simulate_time_varying_draws(
    beta_series: Sequence[Sequence[float]], seed: int | None = None
) -> np.ndarray:
    """Simulate streaming draws for a sequence of bias coefficients.

    Parameters
    ----------
    beta_series:
        Iterable of bias coefficient vectors. ``beta_series[t]`` represents
        :math:`\beta_t` at time step ``t``.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Array of draws where the ``t``-th entry is generated from the
        categorical distribution induced by ``beta_series[t]``.
    """

    beta_array = np.asarray(beta_series, dtype=float)
    if beta_array.ndim != 2:
        raise ValueError("beta_series must be a 2D array of shape (steps, outcomes)")

    n_steps, n_outcomes = beta_array.shape
    draws = np.empty(n_steps, dtype=int)
    rng = np.random.default_rng(seed)

    for t in range(n_steps):
        probabilities = wamecu_probabilities(n_outcomes, beta_array[t])
        draws[t] = rng.choice(n_outcomes, p=probabilities)

    return draws
