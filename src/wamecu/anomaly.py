"""Statistical diagnostics for WAMECU simulations."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
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


def rolling_anomaly_scores(
    draws: Iterable[int],
    baseline_probabilities: np.ndarray,
    window_size: int,
) -> pd.DataFrame:
    """Compute rolling chi-square and entropy diagnostics."""

    draws = np.asarray(list(draws), dtype=int)
    baseline_probabilities = np.asarray(baseline_probabilities, dtype=float)
    if draws.ndim != 1:
        raise ValueError("draws must be one-dimensional")
    if np.any(baseline_probabilities < 0) or not np.isclose(baseline_probabilities.sum(), 1.0):
        raise ValueError("baseline_probabilities must form a valid distribution")
    if window_size <= 1:
        raise ValueError("window_size must be greater than 1")

    n_outcomes = baseline_probabilities.size
    if draws.size < window_size:
        raise ValueError("draws must contain at least one full window")

    records: list[dict[str, float]] = []
    expected_counts = baseline_probabilities * window_size

    for end in range(window_size, draws.size + 1):
        window = draws[end - window_size : end]
        counts = np.bincount(window, minlength=n_outcomes)
        stat, p_value = chi_square_statistic(counts, expected_counts)
        empirical = counts / window_size
        ent_gap = entropy_gap(empirical, baseline_probabilities)
        records.append(
            {
                "step": end - 1,
                "chi2_stat": stat,
                "chi2_pvalue": p_value,
                "entropy_gap": ent_gap,
            }
        )

    return pd.DataFrame.from_records(records)


def outcome_correlation_matrix(draws: Iterable[int], n_outcomes: int) -> np.ndarray:
    """Return the Pearson correlation matrix of one-hot encoded draws."""

    draws = np.asarray(list(draws), dtype=int)
    if draws.ndim != 1:
        raise ValueError("draws must be one-dimensional")
    if n_outcomes <= 1:
        raise ValueError("n_outcomes must be greater than 1")
    if draws.size == 0:
        raise ValueError("draws cannot be empty")

    one_hot = np.eye(n_outcomes)[draws]
    correlation = np.corrcoef(one_hot, rowvar=False)
    correlation = np.nan_to_num(correlation)
    return correlation
