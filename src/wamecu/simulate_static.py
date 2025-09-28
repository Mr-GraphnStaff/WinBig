"""Electrostatic toy simulations supporting the WAMECU manifesto.

The routines below translate hypothesised electrostatic charge patterns on draw
balls into a bias vector :math:`\beta` that perturbs outcome probabilities. The
mapping is intentionally simple yet explicit so other researchers can swap it
for richer physics if they gather better evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np

from .utils import wamecu_probabilities

# Physical constants used in the Coulomb-inspired transformation.  The
# parameters are exposed for documentation and easy tuning within notebooks.
K_COULOMB = 8.9875517923e9  # Vacuum permittivity constant (N·m²·C⁻²)
PAIRWISE_DISTANCE_M = 0.05  # Assume 5 cm average separation inside a machine
BETA_SCALE = 1e-6  # Tunable scalar mapping Newtons → dimensionless beta
MECHANICAL_BETA_SCALE = 0.01  # Residual non-electrostatic variability
BETA_CLIP = 0.95


@dataclass
class StaticSimulationResult:
    """Structured output container for :func:`simulate_with_static`.

    Attributes
    ----------
    q:
        Electrostatic charge assigned to each outcome in Coulombs.
    beta:
        Combined bias coefficients :math:`\beta_i` after electrostatic and
        baseline mechanical contributions.
    probs:
        Normalised probabilities derived from the WAMECU law.
    counts:
        Synthetic counts generated via a multinomial draw using ``probs``.
    """

    q: np.ndarray
    beta: np.ndarray
    probs: np.ndarray
    counts: np.ndarray

    def as_dict(self) -> Dict[str, np.ndarray]:
        """Return a JSON / dict serialisable representation."""

        return {
            "q": self.q,
            "beta": self.beta,
            "probs": self.probs,
            "counts": self.counts,
        }


def _humidity_scale(humidity: float) -> float:
    """Map relative humidity to a damping multiplier.

    High humidity dissipates charge quickly, while dry air lets it accumulate.
    We adopt a conservative linear attenuation clipped to ``[0.1, 1.0]``::

        s(h) = clip(1 - h / 100, 0.1, 1.0)

    Researchers can replace this with an exponential decay or empirical fit if
    laboratory data becomes available.
    """

    return float(np.clip(1.0 - humidity / 100.0, 0.1, 1.0))


def simulate_with_static(
    n_outcomes: int,
    q_scale: float = 1e-9,
    humidity: float = 40.0,
    trials_per_draw: int = 200,
    seed: Optional[int] = None,
) -> Dict[str, np.ndarray]:
    """Simulate outcome bias caused by electrostatic charge accumulation.

    The procedure intentionally exposes each modelling decision:

    1. Sample per-outcome charge ``q_i`` from ``N(0, q_scale)`` and damp them by
       the humidity scaling factor ``s(h)`` defined in :func:`_humidity_scale`.
    2. Approximate the net Coulomb force on ball ``i`` via
       ``F_i = k_e * q_i * (sum_j q_j - q_i) / d^2``.
    3. Convert ``F_i`` into a dimensionless bias contribution with a tunable
       linear scale ``BETA_SCALE`` and clip to ``[-BETA_CLIP, BETA_CLIP]``.
    4. Add small zero-mean mechanical noise ``\epsilon_i`` to represent residual
       machine asymmetry (controllable via ``MECHANICAL_BETA_SCALE``).
    5. Transform the combined bias vector through :func:`wamecu_probabilities`
       and draw synthetic outcome counts using a multinomial sample.

    Parameters
    ----------
    n_outcomes:
        Number of discrete outcomes (balls) to simulate.
    q_scale:
        Standard deviation of the Gaussian charge prior in Coulombs before
        humidity damping.  Adjust to explore stronger/weaker charge regimes.
    humidity:
        Relative humidity percentage; higher humidity damps the sampled charges.
    trials_per_draw:
        Number of synthetic draws used to convert probabilities into counts.
        Keep small for notebook smoke tests; increase for precision studies.
    seed:
        Optional integer seed forwarded to :class:`numpy.random.Generator` for
        reproducibility.

    Returns
    -------
    dict
        Dictionary containing ``q``, ``beta``, ``probs``, and ``counts`` arrays.
        Use :class:`StaticSimulationResult` for ergonomic accessors if desired.

    Notes
    -----
    Alternative mappings: researchers might prefer a non-linear scaling (e.g.,
    ``tanh`` or ``log1p``) from Coulomb forces to ``\beta``.  The linear version
    here keeps the algebra transparent and highlights where empirical constants
    could be substituted once measured.
    """

    if n_outcomes < 2:
        raise ValueError("n_outcomes must be at least 2")
    if trials_per_draw <= 0:
        raise ValueError("trials_per_draw must be positive")

    rng = np.random.default_rng(seed)
    humidity_factor = _humidity_scale(humidity)

    q = rng.normal(loc=0.0, scale=q_scale, size=n_outcomes) * humidity_factor

    net_charge = np.sum(q)
    force = K_COULOMB * q * (net_charge - q) / (PAIRWISE_DISTANCE_M**2)
    beta_elec = np.clip(force * BETA_SCALE, -BETA_CLIP, BETA_CLIP)

    beta_mech = rng.normal(loc=0.0, scale=MECHANICAL_BETA_SCALE, size=n_outcomes)
    beta = np.clip(beta_elec + beta_mech, -BETA_CLIP, BETA_CLIP)

    probs = wamecu_probabilities(n_outcomes, beta)
    counts = rng.multinomial(trials_per_draw, probs)

    result = StaticSimulationResult(q=q, beta=beta, probs=probs, counts=counts)
    return result.as_dict()


def estimate_static_effect(
    q: np.ndarray,
    counts: np.ndarray,
    trials: int,
) -> float:
    """Estimate the effect size linking electrostatic charge to outcome bias.

    We fit a one-parameter linear model between charge and log-odds deviation::

        y_i = logit(p_i) - logit(1 / n)
        effect = \frac{\sum_i (q_i - \bar{q}) y_i}{\sum_i (q_i - \bar{q})^2 + \epsilon}

    where ``p_i = counts_i / trials`` and ``n`` is the number of outcomes.  The
    estimator is intentionally simple, robust to translation of ``q``, and easy
    to compare across simulations.  A positive coefficient suggests that higher
    positive charge increases the log-odds of being drawn relative to a fair
    baseline.  Researchers with richer datasets could swap in a logistic
    regression or non-parametric estimator.

    Parameters
    ----------
    q:
        Array of per-outcome charges in Coulombs.
    counts:
        Observed counts for each outcome from ``trials`` synthetic draws.
    trials:
        Total number of draws.  Should equal ``counts.sum()`` but we do not
        enforce exact equality to stay tolerant of rounded inputs.

    Returns
    -------
    float
        Estimated slope linking charge to log-odds deviation.
    """

    q = np.asarray(q, dtype=float)
    counts = np.asarray(counts, dtype=float)
    if q.shape != counts.shape:
        raise ValueError("q and counts must have the same shape")
    if trials <= 0:
        raise ValueError("trials must be positive")

    n = q.size
    baseline_p = 1.0 / n
    observed_p = counts / float(trials)
    observed_p = np.clip(observed_p, 1e-9, 1 - 1e-9)

    logit = np.log(observed_p / (1.0 - observed_p))
    baseline_logit = np.log(baseline_p / (1.0 - baseline_p))
    y = logit - baseline_logit

    q_centered = q - q.mean()
    denom = np.sum(q_centered**2) + 1e-24
    effect = float(np.sum(q_centered * y) / denom)
    return effect


__all__ = [
    "StaticSimulationResult",
    "simulate_with_static",
    "estimate_static_effect",
]
