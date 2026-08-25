#!/usr/bin/env bash
# ============================================================
# run_primary_match.sh
# Wrapper to run the SkillCorner primary match analysis.
# Run from the Football-TDA project root:
#   bash 03_football_analysis/AvailableData/run_primary_match.sh
# ============================================================

set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
echo "Project root: $(pwd)"

# Check Python 3
python3 --version 2>&1 || { echo "ERROR: python3 not found"; exit 1; }

# Install/check dependencies
echo ""
echo "Checking Python dependencies..."
python3 -c "import ripser" 2>/dev/null || pip3 install ripser --break-system-packages -q
python3 -c "import scipy"  2>/dev/null || pip3 install scipy  --break-system-packages -q
python3 -c "import sklearn" 2>/dev/null || pip3 install scikit-learn --break-system-packages -q
python3 -c "import matplotlib" 2>/dev/null || pip3 install matplotlib --break-system-packages -q
python3 -c "import pandas" 2>/dev/null || pip3 install pandas --break-system-packages -q
python3 -c "import ripser, scipy, sklearn, matplotlib, pandas; print('All dependencies OK')"

echo ""
echo "Starting analysis (this will take ~15-30 min depending on CPU)..."
echo "Tracking data (~100 MB) will be downloaded automatically if not present."
echo ""

time python3 03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py

echo ""
echo "Done. Results in: results/primary_skillcorner/"
ls -lh results/primary_skillcorner/
