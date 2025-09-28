from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from wamecu import estimate_static_effect, simulate_with_static


def test_simulate_with_static_shape() -> None:
    result = simulate_with_static(n_outcomes=4, q_scale=1e-9, humidity=35, trials_per_draw=50, seed=42)
    assert set(result) == {"q", "beta", "probs", "counts"}
    for key in ("q", "beta", "probs", "counts"):
        assert len(result[key]) == 4
    assert np.isclose(result["probs"].sum(), 1.0)
    assert int(result["counts"].sum()) == 50


def test_beta_bounds() -> None:
    result = simulate_with_static(n_outcomes=8, q_scale=5e-9, humidity=25, trials_per_draw=80, seed=7)
    beta = result["beta"]
    assert np.all(beta >= -0.95)
    assert np.all(beta <= 0.95)


def test_schema_update() -> None:
    schema_path = Path("data/schema/wamecu_observation.schema.json")
    schema = json.loads(schema_path.read_text())
    properties = schema["properties"]["observed_features"]["properties"]
    assert "electrostatic_charge_C" in properties
    assert "electrostatic_test_method" in properties
    assert "electrostatic_measured_at" in properties
    assert "relative_humidity_pct" in properties
    assert "anti_static_used" in properties


def test_effect_estimator_runs() -> None:
    result = simulate_with_static(n_outcomes=5, q_scale=2e-9, humidity=30, trials_per_draw=60, seed=123)
    effect = estimate_static_effect(result["q"], result["counts"], trials=int(result["counts"].sum()))
    assert np.isfinite(effect)
