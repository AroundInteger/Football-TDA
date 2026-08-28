#!/usr/bin/env bash
# Paper A (JACT) pipeline — single entry point
set -euo pipefail

PIPELINE_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$(cd "$PIPELINE_DIR/.." && pwd)"

# Prefer paper-local layout (standalone GitHub repo); fall back to monorepo.
# The test is the match index, not the directory: in the monorepo the
# paper-local 01_data/ holds only the primary match and no matches.json, so
# testing for the directory alone sends the ten-match steps to a tree that
# cannot serve them.
if [[ -f "$PAPER_DIR/01_data/opendata/data/matches.json" && -d "$PAPER_DIR/02_tda_core" ]]; then
  REPO_ROOT="$PAPER_DIR"
else
  REPO_ROOT="$(cd "$PIPELINE_DIR/../../../../.." && pwd)"
fi
cd "$REPO_ROOT"

if [[ ! -f "01_data/opendata/data/matches.json" ]]; then
  echo "ERROR: no SkillCorner match index at $REPO_ROOT/01_data/opendata/data/matches.json" >&2
  exit 1
fi

echo "=== Paper A pipeline ==="
echo "Repo: $REPO_ROOT"
echo "Output: $PIPELINE_DIR/outputs"

python3 "$PIPELINE_DIR/steps/00_pipeline_figure.py"
python3 "$PIPELINE_DIR/steps/01_primary_uniform.py"
python3 "$PIPELINE_DIR/steps/02_cutoff_sweep.py"
python3 "$PIPELINE_DIR/steps/03_multi_match.py"
python3 "$PIPELINE_DIR/steps/05_event_validity.py"
python3 "$PIPELINE_DIR/steps/04_complementarity.py"
python3 "$PIPELINE_DIR/steps/07_cardinality_null.py"
python3 "$PIPELINE_DIR/steps/08_linkage_comparison.py"
python3 "$PIPELINE_DIR/steps/06_figures.py"
python3 "$PIPELINE_DIR/steps/09_acf_supplement.py"
python3 "$PIPELINE_DIR/lib/build_numbers.py"

python3 "$PIPELINE_DIR/sync_to_paper.py" || true

python3 -c "
import sys
sys.path.insert(0, '$PIPELINE_DIR/lib')
from common import write_manifest
write_manifest({'steps_completed': ['00','01','02','03','04','05','06','07','08','09','build_numbers']})
"

echo "=== Paper A pipeline complete ==="
