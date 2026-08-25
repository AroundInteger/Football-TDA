#!/usr/bin/env python3
"""Step 04: bilateral (home/away) tactical topology."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
import bilateral_topology as bt  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    bt.OUT_DIR = OUTPUT_DIR
    sys.argv = [
        "bilateral_topology.py",
        "--skillcorner-only",
        "--n-boot",
        str(cfg["bootstrap"]["n_boot"]),
        "--seed",
        str(cfg["bootstrap"]["seed"]),
    ]
    bt.main()
