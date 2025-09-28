#!/bin/bash
set -euo pipefail
bash tools/run_smoke_notebooks.sh
pytest -q
black --check src || true
flake8 src || true
