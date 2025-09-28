#!/bin/bash
set -euo pipefail
shopt -s nullglob
NOTEBOOKS=(notebooks/*.ipynb)
if [ ${#NOTEBOOKS[@]} -eq 0 ]; then
  echo "No notebooks found under notebooks/."
  exit 0
fi
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"
for nb in "${NOTEBOOKS[@]}"; do
  echo "Running notebook smoke test: $nb"
  python - "$nb" <<'PY'
import sys
from nbclient import NotebookClient
from nbformat import read
from pathlib import Path

nb_path = Path(sys.argv[1])
with nb_path.open("r", encoding="utf-8") as fh:
    nb = read(fh, as_version=4)

client = NotebookClient(nb, timeout=600, kernel_name="python3", allow_errors=False)
client.execute()
PY
done
