"""Online estimation utilities for WAMECU β coefficients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .utils import wamecu_probabilities
from .simulate import BetaDriftConfig, beta_drift


def simulate_beta_drift(
    n_outcomes: int,
    n_steps: int,
    drift: str = "random_walk",
    scale: float = 0.05,
    clip: float = 0.8,
    seed: int | None = None,
) -> np.ndarray:
    """Legacy helper that delegates to :func:`wamecu.simulate.beta_drift`."""

    if drift not in {"random_walk", "sinusoidal"}:
        raise ValueError("drift must be 'random_walk' or 'sinusoidal'")

    sin_amplitude = 0.0 if drift == "random_walk" else scale
    config = BetaDriftConfig(
        n_steps=n_steps,
        n_outcomes=n_outcomes,
        walk_scale=scale,
        sin_amplitude=sin_amplitude,
        sin_period=max(60, n_steps // 3),
        clip=clip,
        seed=seed,
    )
    return beta_drift(config)


@dataclass
class EWMAState:
    """State container for the EWMA estimator."""

    probabilities: np.ndarray
    beta: np.ndarray


def ewma_estimator(
    observations: Sequence[int],
    n_outcomes: int,
    alpha: float = 0.05,
    initial_probabilities: Iterable[float] | None = None,
) -> np.ndarray:
    """Estimate β via an exponentially weighted moving average."""

    if n_outcomes < 2:
        raise ValueError("n_outcomes must be at least 2")
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")

    obs_array = np.asarray(list(observations), dtype=int)
    if obs_array.ndim != 1:
        raise ValueError("observations must be 1D")

    if initial_probabilities is None:
        probabilities = np.full(n_outcomes, 1.0 / n_outcomes, dtype=float)
    else:
        probabilities = np.asarray(list(initial_probabilities), dtype=float)
        if probabilities.size != n_outcomes:
            raise ValueError("initial_probabilities length mismatch")
        probabilities = probabilities / probabilities.sum()

    beta_history = np.zeros((obs_array.size, n_outcomes), dtype=float)
    baseline = 1.0 / n_outcomes

    for t, obs in enumerate(obs_array):
        if not 0 <= obs < n_outcomes:
            raise ValueError("observation index out of bounds")
        one_hot = np.zeros(n_outcomes, dtype=float)
        one_hot[obs] = 1.0
        probabilities = (1 - alpha) * probabilities + alpha * one_hot
        probabilities = np.maximum(probabilities, 1e-12)
        probabilities /= probabilities.sum()
        beta = probabilities / baseline - 1.0
        beta -= beta.mean()
        beta = np.clip(beta, -0.99, 0.99)
        beta_history[t] = beta

    return beta_history


def kalman_tracker(
    observations: Sequence[int],
    n_outcomes: int,
    process_var: float = 0.005,
    observation_var: float = 0.05,
    initial_beta: Iterable[float] | None = None,
) -> np.ndarray:
    """Track β using an independent Kalman filter for each outcome."""

    if n_outcomes < 2:
        raise ValueError("n_outcomes must be at least 2")
    if process_var <= 0 or observation_var <= 0:
        raise ValueError("variances must be positive")

    obs_array = np.asarray(list(observations), dtype=int)
    if obs_array.ndim != 1:
        raise ValueError("observations must be 1D")

    if initial_beta is None:
        state = np.zeros(n_outcomes, dtype=float)
    else:
        state = np.asarray(list(initial_beta), dtype=float)
        if state.size != n_outcomes:
            raise ValueError("initial_beta must match n_outcomes")
        state = np.clip(state, -0.99, 0.99)

    covariance = np.full(n_outcomes, 0.25, dtype=float)
    beta_history = np.zeros((obs_array.size, n_outcomes), dtype=float)
    baseline = 1.0 / n_outcomes

    for t, obs in enumerate(obs_array):
        if not 0 <= obs < n_outcomes:
            raise ValueError("observation index out of bounds")

        measurement = np.full(n_outcomes, -baseline, dtype=float)
        measurement[obs] = 1.0 - baseline

        covariance = covariance + process_var
        kalman_gain = covariance / (covariance + observation_var)
        state = state + kalman_gain * (measurement - state)
        covariance = (1 - kalman_gain) * covariance

        state -= state.mean()
        state = np.clip(state, -0.99, 0.99)
        beta_history[t] = state

    return beta_history


class AdaptiveBetaEstimator:
    """Legacy estimator retained for backward compatibility."""

    def __init__(self, n_outcomes: int, smoothing: float = 0.05) -> None:
        self.n_outcomes = n_outcomes
        self.smoothing = smoothing
        self._probabilities = np.full(
            n_outcomes,
            1.0 / n_outcomes,
            dtype=float,
        )
        self.beta_ = np.zeros(n_outcomes, dtype=float)

    def update(self, observation: int) -> np.ndarray:
        history = ewma_estimator(
            [observation],
            self.n_outcomes,
            alpha=self.smoothing,
            initial_probabilities=self._probabilities,
        )
        self._probabilities = (1 - self.smoothing) * self._probabilities
        self._probabilities[observation] += self.smoothing
        self._probabilities /= self._probabilities.sum()
        self.beta_ = history[-1]
        return self.beta_.copy()

    def batch_update(self, observations: Iterable[int]) -> np.ndarray:
        history = ewma_estimator(
            observations,
            self.n_outcomes,
            alpha=self.smoothing,
            initial_probabilities=self._probabilities,
        )
        self.beta_ = history[-1]
        self._probabilities = wamecu_probabilities(self.n_outcomes, self.beta_)
        return history


__all__ = [
    "EWMAState",
    "AdaptiveBetaEstimator",
    "ewma_estimator",
    "kalman_tracker",
    "simulate_beta_drift",
]
