# AGENTS.md

## Project Purpose
This repository is not a standard software package. It is the experimental laboratory for **WAMECU**:

> P(Outcome_i) = (1/N) * (1 + β_i(WAMECU))

Where **WAMECU** = Weight, Atmosphere, Mechanics, Entropy deviations, Correlated drift, and Unknowns.  

Agents and contributors are expected to treat this as a research playground for building a **new AI-powered mathematics of predictability and bias**.

---

## Environment Setup
- Language: Python 3.11+  
- Notebook interface: Jupyter Lab (preferred)  
- Core libraries:  
  - `numpy`, `scipy`, `pandas`, `matplotlib`  
  - `scikit-learn` (for baseline models)  
  - `jupyter` for interactive exploration  
- Optional: `pytest` for unit testing  

### Setup commands
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
Workflow Guidelines
Everything is an experiment.
New code should be dropped in /notebooks first as a proof of concept. Once stable, migrate to /src.

Bias coefficient β_i is the nucleus.
All experiments should, in some way, test, measure, or model β_i across the WAMECU domains.

Simulation before speculation.
If proposing a new bias mechanism, first implement a toy simulation. Hypotheses without data are noise.

Adaptive by design.
Models should learn from data over time — static hard-coded coefficients are discouraged unless for baseline tests.

Testing Instructions
Run pytest in the /tests folder for unit checks.

Execute all notebooks from top to bottom before submitting changes; notebooks must run without manual fixes.

For randomness experiments, fix a seed for reproducibility when comparing runs.

PR / Commit Rules
Branch naming: exp/<short-description> for experiments, fix/<short-description> for fixes.

Commit style: [WAMECU] <summary>

Example: [WAMECU] Add entropy bias toy simulation

Pull requests must include:

A short abstract (2–3 sentences) of what the code tests or proves.

At least one visualization or metric if applicable.

Custom Notes for Agents
Do not trivialize: Avoid auto-generating filler code. Contributions must tie directly to the WAMECU law or its supporting framework.

Prefer clarity over cleverness: readable, transparent code is better than exotic tricks.

Honor the manifesto: The README and paper draft are the constitution. Any code that drifts away from the law’s intent should be rejected.

