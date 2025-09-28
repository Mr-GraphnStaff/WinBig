"""End-to-end orchestration utilities for the WAMECU workflow."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from .anomaly import outcome_correlation_matrix, rolling_anomaly_scores
from .bias import inverse_mass_probabilities, probabilities_to_beta
from .estimation import AdaptiveBetaEstimator, simulate_beta_drift
from .simulation import simulate_time_varying_draws, wamecu_probabilities


def build_weight_profile(n_outcomes: int, heaviness: float = 1.5) -> np.ndarray:
    """Create a default weight profile with heavier tails."""

    if n_outcomes <= 1:
        raise ValueError("n_outcomes must be greater than 1")
    if heaviness <= 0:
        raise ValueError("heaviness must be positive")

    weights = np.linspace(1.0, heaviness, num=n_outcomes)
    return weights


def run_wamecu_cycle(
    n_outcomes: int = 6,
    n_steps: int = 400,
    drift: str = "sinusoidal",
    weight_profile: Iterable[float] | None = None,
    softness: float = 1.0,
    smoothing: float = 0.05,
    window_size: int = 50,
    drift_scale: float = 0.05,
    seed: int | None = 42,
) -> dict[str, object]:
    """Execute the full WAMECU simulation and monitoring cycle."""

    if window_size >= n_steps:
        raise ValueError("window_size must be smaller than n_steps")

    rng = np.random.default_rng(seed)

    if weight_profile is None:
        weights = build_weight_profile(n_outcomes)
        rng.shuffle(weights)
    else:
        weights = np.asarray(list(weight_profile), dtype=float)
        if weights.size != n_outcomes:
            raise ValueError("weight_profile size must match n_outcomes")

    baseline_probabilities = inverse_mass_probabilities(weights, softness=softness)
    baseline_beta = probabilities_to_beta(baseline_probabilities)

    drift_series = simulate_beta_drift(
        n_outcomes=n_outcomes,
        n_steps=n_steps,
        drift=drift,
        scale=drift_scale,
        seed=None if seed is None else seed + 1,
    )

    beta_series = drift_series + baseline_beta

    min_adjusted = np.min(1 + beta_series)
    if min_adjusted <= 0:
        safety = 0.95 * np.min(1 + baseline_beta)
        beta_series = baseline_beta + (beta_series - baseline_beta) * max(safety / (safety - min_adjusted), 0.5)

    probabilities = np.vstack([wamecu_probabilities(n_outcomes, beta) for beta in beta_series])
    draws = simulate_time_varying_draws(beta_series, seed=None if seed is None else seed + 2)

    estimator = AdaptiveBetaEstimator(n_outcomes=n_outcomes, smoothing=smoothing)
    estimated_beta = estimator.batch_update(draws)

    anomalies = rolling_anomaly_scores(draws, baseline_probabilities, window_size=window_size)
    correlations = outcome_correlation_matrix(draws, n_outcomes)

    timeline = np.arange(n_steps)
    probability_df = pd.DataFrame(probabilities, columns=[f"Outcome {i}" for i in range(n_outcomes)])
    probability_df.insert(0, "step", timeline)

    return {
        "weights": weights,
        "baseline_probabilities": baseline_probabilities,
        "baseline_beta": baseline_beta,
        "beta_series": beta_series,
        "probabilities": probability_df,
        "draws": draws,
        "estimated_beta": estimated_beta,
        "anomalies": anomalies,
        "correlations": correlations,
    }
