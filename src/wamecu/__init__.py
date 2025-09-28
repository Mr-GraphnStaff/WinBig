"""Core utilities for WAMECU experiments."""

from .anomaly import (
    chi_square_statistic,
    entropy_gap,
    outcome_correlation_matrix,
    rolling_anomaly_scores,
)
from .bias import inverse_mass_probabilities, probabilities_to_beta
from .estimation import (
    AdaptiveBetaEstimator,
    ewma_estimator,
    kalman_tracker,
    simulate_beta_drift,
)
from .metrics import chi_square_test, shannon_entropy
from .pipeline import build_weight_profile, run_wamecu_cycle
from .simulate import (
    BetaDriftConfig,
    beta_drift,
    simulate_draws,
    simulate_time_varying_draws,
    stream_draws,
)
from .utils import wamecu_probabilities

__all__ = [
    "AdaptiveBetaEstimator",
    "BetaDriftConfig",
    "beta_drift",
    "build_weight_profile",
    "chi_square_statistic",
    "chi_square_test",
    "entropy_gap",
    "ewma_estimator",
    "inverse_mass_probabilities",
    "kalman_tracker",
    "outcome_correlation_matrix",
    "probabilities_to_beta",
    "rolling_anomaly_scores",
    "run_wamecu_cycle",
    "shannon_entropy",
    "simulate_beta_drift",
    "simulate_draws",
    "simulate_time_varying_draws",
    "stream_draws",
    "wamecu_probabilities",
]
