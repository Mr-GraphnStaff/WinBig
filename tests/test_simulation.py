import numpy as np
import pytest

from wamecu import simulate_draws, wamecu_probabilities


def test_wamecu_probabilities_normalize():
    beta = [0.1, -0.05, -0.05]
    probs = wamecu_probabilities(3, beta)
    assert pytest.approx(1.0) == probs.sum()
    assert np.all(probs >= 0)


def test_simulate_draws_reproducible():
    probs = np.array([0.2, 0.5, 0.3])
    draws_one = simulate_draws(probs, 1000, seed=7)
    draws_two = simulate_draws(probs, 1000, seed=7)
    assert np.array_equal(draws_one, draws_two)


def test_wamecu_probabilities_mismatch_shape():
    with pytest.raises(ValueError):
        wamecu_probabilities(2, [0.1, 0.2, 0.3])
