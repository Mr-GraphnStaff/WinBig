"""Core utilities for WAMECU experiments."""

from .anomaly import (
    chi_square_statistic,
    entropy_gap,
    outcome_correlation_matrix,
    rolling_anomaly_scores,
)
from .bias import inverse_mass_probabilities, probabilities_to_beta
from .estimation import AdaptiveBetaEstimator, simulate_beta_drift
from .pipeline import build_weight_profile, run_wamecu_cycle
from .simulation import simulate_draws, simulate_time_varying_draws, wamecu_probabilities

__all__ = [
    "AdaptiveBetaEstimator",
    "build_weight_profile",
    "chi_square_statistic",
    "entropy_gap",
    "inverse_mass_probabilities",
    "outcome_correlation_matrix",
    "probabilities_to_beta",
    "rolling_anomaly_scores",
    "run_wamecu_cycle",
    "simulate_beta_drift",
    "simulate_draws",
    "simulate_time_varying_draws",
    "wamecu_probabilities",
]
