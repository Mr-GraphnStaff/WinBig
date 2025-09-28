"""Statistical diagnostics for WAMECU simulations."""
from __future__ import annotations

import numpy as np
from scipy.stats import chi2


def chi_square_statistic(observed: np.ndarray, expected: np.ndarray) -> tuple[float, float]:
    """Return the chi-square statistic and p-value for observed vs. expected counts."""
    observed = np.asarray(observed, dtype=float)
    expected = np.asarray(expected, dtype=float)
    if observed.shape != expected.shape:
        raise ValueError("observed and expected must have the same shape")
    if np.any(expected <= 0):
        raise ValueError("expected counts must be positive")

    statistic = np.sum((observed - expected) ** 2 / expected)
    dof = observed.size - 1
    p_value = 1 - chi2.cdf(statistic, df=dof)
    return float(statistic), float(p_value)


def entropy_gap(empirical_prob: np.ndarray, baseline_prob: np.ndarray) -> float:
    """Compute the Shannon entropy gap between empirical and baseline distributions."""
    empirical_prob = np.asarray(empirical_prob, dtype=float)
    baseline_prob = np.asarray(baseline_prob, dtype=float)
    if empirical_prob.shape != baseline_prob.shape:
        raise ValueError("probability vectors must have matching shape")
    if not np.isclose(empirical_prob.sum(), 1.0):
        raise ValueError("empirical_prob must sum to 1")
    if not np.isclose(baseline_prob.sum(), 1.0):
        raise ValueError("baseline_prob must sum to 1")

    # avoid log(0); only include terms where probability > 0
    mask_empirical = empirical_prob > 0
    mask_baseline = baseline_prob > 0
    entropy_empirical = -np.sum(empirical_prob[mask_empirical] * np.log2(empirical_prob[mask_empirical]))
    entropy_baseline = -np.sum(baseline_prob[mask_baseline] * np.log2(baseline_prob[mask_baseline]))
    return float(entropy_empirical - entropy_baseline)
