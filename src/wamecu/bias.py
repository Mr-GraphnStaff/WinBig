"""Bias utilities for WAMECU digital twin experiments."""
from __future__ import annotations

from typing import Iterable

import numpy as np


def inverse_mass_probabilities(weights: Iterable[float], softness: float = 1.0) -> np.ndarray:
    """Convert outcome weights into a probability distribution.

    The heuristic follows a simple physical metaphor: heavier outcomes have
    lower selection probability. The ``softness`` parameter controls how
    quickly probability mass decreases with weight.
    """

    weights = np.asarray(list(weights), dtype=float)
    if weights.ndim != 1:
        raise ValueError("weights must be one-dimensional")
    if np.any(weights <= 0):
        raise ValueError("weights must be strictly positive")

    softness = float(softness)
    if softness <= 0:
        raise ValueError("softness must be positive")

    inverse_mass = 1.0 / np.power(weights, softness)
    probabilities = inverse_mass / inverse_mass.sum()
    return probabilities


def probabilities_to_beta(probabilities: Iterable[float]) -> np.ndarray:
    """Map probabilities back to :math:`\beta` coefficients under WAMECU."""

    probabilities = np.asarray(list(probabilities), dtype=float)
    if probabilities.ndim != 1:
        raise ValueError("probabilities must be one-dimensional")
    if probabilities.size == 0:
        raise ValueError("probabilities cannot be empty")
    if np.any(probabilities < 0):
        raise ValueError("probabilities must be non-negative")
    total = probabilities.sum()
    if not np.isclose(total, 1.0):
        raise ValueError("probabilities must sum to 1")

    n_outcomes = probabilities.size
    baseline = 1.0 / n_outcomes
    beta = probabilities / baseline - 1.0
    return beta
