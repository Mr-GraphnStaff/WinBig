"""Diagnostic metrics grounded in the WAMECU manifesto."""

from __future__ import annotations

import numpy as np
from scipy.stats import chi2


def chi_square_test(
    observed: np.ndarray,
    expected: np.ndarray,
) -> tuple[float, float]:
    """Return chi-square statistic and p-value."""

    observed_arr = np.asarray(observed, dtype=float)
    expected_arr = np.asarray(expected, dtype=float)
    if observed_arr.shape != expected_arr.shape:
        raise ValueError("observed and expected must share the same shape")
    if np.any(expected_arr <= 0):
        raise ValueError("expected counts must be positive")

    statistic = np.sum((observed_arr - expected_arr) ** 2 / expected_arr)
    dof = observed_arr.size - 1
    p_value = 1 - chi2.cdf(statistic, df=dof)
    return float(statistic), float(p_value)


def shannon_entropy(probabilities: np.ndarray) -> float:
    """Compute Shannon entropy in bits for a discrete probability vector."""

    probs = np.asarray(probabilities, dtype=float)
    if probs.ndim != 1:
        raise ValueError("probabilities must be one-dimensional")
    if np.any(probs < 0) or not np.isclose(probs.sum(), 1.0):
        raise ValueError("probabilities must sum to 1 and be non-negative")

    mask = probs > 0
    return float(-np.sum(probs[mask] * np.log2(probs[mask])))


__all__ = ["chi_square_test", "shannon_entropy"]
