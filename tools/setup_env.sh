#!/bin/bash
set -euo pipefail
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install --upgrade -r requirements.txt
else
  pip install --upgrade numpy pandas scipy matplotlib scikit-learn jupyterlab notebook nbclient papermill pytest seaborn black flake8
fi
