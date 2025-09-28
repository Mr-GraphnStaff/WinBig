import numpy as np
import pytest

from wamecu import BetaDriftConfig, ewma_estimator, beta_drift, wamecu_probabilities


def test_wamecu_probabilities_properties():
    beta = [0.1, -0.05, -0.05]
    probs = wamecu_probabilities(3, beta)
    assert probs.shape == (3,)
    assert np.isclose(probs.sum(), 1.0)
    assert np.all(probs >= 0)

    with pytest.raises(ValueError):
        wamecu_probabilities(3, [0.5, 0.5, -2.0])


def test_beta_drift_bounds():
    config = BetaDriftConfig(n_steps=200, n_outcomes=4, clip=0.95, seed=0)
    series = beta_drift(config)
    assert series.shape == (200, 4)
    assert np.all(series <= 0.95 + 1e-9)
    assert np.all(series >= -0.95 - 1e-9)


def test_ewma_estimator_shape():
    draws = [0, 1, 1, 2, 2, 2]
    history = ewma_estimator(draws, n_outcomes=3, alpha=0.2)
    assert history.shape == (len(draws), 3)
    assert np.all(np.isfinite(history))
