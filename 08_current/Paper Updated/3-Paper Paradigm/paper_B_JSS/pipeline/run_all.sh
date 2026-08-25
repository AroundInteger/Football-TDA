#!/usr/bin/env bash
# Paper B (JSS) pipeline — single entry point
set -euo pipefail

PIPELINE_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$(cd "$PIPELINE_DIR/.." && pwd)"

# Prefer paper-local layout (standalone GitHub repo); fall back to monorepo.
if [[ -d "$PAPER_DIR/01_data" && -d "$PAPER_DIR/02_tda_core" ]]; then
  REPO_ROOT="$PAPER_DIR"
else
  REPO_ROOT="$(cd "$PIPELINE_DIR/../../../../.." && pwd)"
fi
cd "$REPO_ROOT"

echo "=== Paper B pipeline ==="
echo "Repo: $REPO_ROOT"
echo "Output: $PIPELINE_DIR/outputs"

python3 "$PIPELINE_DIR/steps/01_event_correlation.py"
python3 "$PIPELINE_DIR/steps/02_window_sensitivity.py"
python3 "$PIPELINE_DIR/steps/03_baseline_vs_topology.py"
python3 "$PIPELINE_DIR/steps/04_bilateral_topology.py"
python3 "$PIPELINE_DIR/steps/05_predictive_utility.py"
python3 "$PIPELINE_DIR/steps/06_figures.py"
python3 "$PIPELINE_DIR/lib/build_numbers.py"
python3 "$PIPELINE_DIR/sync_to_paper.py"
python3 -c "
import sys
sys.path.insert(0, '$PIPELINE_DIR/lib')
from common import write_manifest
write_manifest({'steps_completed': ['01','02','03','04','05','06','build_numbers']})
"
echo "=== Paper B pipeline complete ==="
