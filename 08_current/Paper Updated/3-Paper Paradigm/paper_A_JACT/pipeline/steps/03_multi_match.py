#!/usr/bin/env python3
"""Step 03: ten-match SkillCorner validation."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "01_data"))
sys.path.insert(0, str(REPO / "02_tda_core"))
sys.path.insert(0, str(REPO / "03_football_analysis"))

import json
import pandas as pd
import multi_match_validation as mm  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    out = OUTPUT_DIR / "multi_match"
    out.mkdir(parents=True, exist_ok=True)
    mm.OUTPUT_DIR = out
    cfg = load_config()
    mm.FRAMES_PER_MATCH = int(cfg["sampling"]["uniform_150"]["n_frames"])

    sys.argv = ["03_multi_match.py", "--skillcorner-only"]
    mm.main()

    # Copy aggregate for downstream steps
    agg_path = out / "aggregate_stats.json"
    if agg_path.exists():
        with open(OUTPUT_DIR / "aggregate_stats.json", "w") as f:
            json.dump(json.loads(agg_path.read_text()), f, indent=2)
