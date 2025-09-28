import numpy as np
import pytest

from wamecu import chi_square_statistic, entropy_gap


def test_chi_square_detects_bias():
    observed = np.array([60, 25, 15])
    expected = np.array([100 / 3, 100 / 3, 100 / 3])
    statistic, p_value = chi_square_statistic(observed, expected)
    assert statistic > 0
    assert p_value < 0.05


def test_entropy_gap_signals_concentration():
    empirical = np.array([0.6, 0.3, 0.1])
    baseline = np.full(3, 1 / 3)
    gap = entropy_gap(empirical, baseline)
    assert gap < 0


def test_entropy_gap_validates_inputs():
    with pytest.raises(ValueError):
        entropy_gap(np.array([0.5, 0.5]), np.array([0.4, 0.4]))
