#!/usr/bin/env python3
"""Step 03: baseline geometric descriptors vs tactical persistence."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
import baseline_vs_topology as bvt  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    bvt.OUT_DIR = OUTPUT_DIR
    sys.argv = ["baseline_vs_topology.py", "--skillcorner-only"]
    bvt.main()
