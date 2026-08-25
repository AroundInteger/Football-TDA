#!/usr/bin/env python3
"""Step 05: predictive utility (build-up phase classification)."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
import predictive_utility as pu  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    pu.OUT_DIR = OUTPUT_DIR
    sys.argv = [
        "predictive_utility.py",
        "--skillcorner-only",
        "--n-boot",
        str(cfg["predictive"]["n_boot"]),
        "--n-perm",
        str(cfg["predictive"]["n_perm"]),
        "--seed",
        str(cfg["predictive"]["seed"]),
    ]
    pu.main()
