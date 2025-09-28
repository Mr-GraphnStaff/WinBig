"""Utility helpers for implementing the WAMECU manifesto experiments."""

from __future__ import annotations

from typing import Iterable

import numpy as np


def wamecu_probabilities(n_outcomes: int, beta: Iterable[float]) -> np.ndarray:
    """Return normalized probabilities under the WAMECU bias law.

    Parameters
    ----------
    n_outcomes:
        Number of distinct categorical outcomes.
    beta:
        Iterable of bias coefficients :math:`\beta_i` of length ``n_outcomes``.

    Returns
    -------
    numpy.ndarray
        Normalized probability vector obeying ``sum(p_i) == 1``.

    Raises
    ------
    ValueError
        If ``beta`` length mismatches ``n_outcomes`` or produces negative mass.
    """

    beta_array = np.asarray(list(beta), dtype=float)
    if beta_array.size != n_outcomes:
        raise ValueError("beta vector must match number of outcomes")

    base = np.full(n_outcomes, 1.0 / n_outcomes, dtype=float)
    adjusted = base * (1.0 + beta_array)

    if np.any(adjusted < 0):
        raise ValueError("bias coefficients yield negative probabilities")

    total = adjusted.sum()
    if total <= 0:
        raise ValueError("bias coefficients collapse the probability mass")

    return adjusted / total


__all__ = ["wamecu_probabilities"]
