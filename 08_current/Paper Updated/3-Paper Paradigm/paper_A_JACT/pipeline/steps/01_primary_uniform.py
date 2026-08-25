#!/usr/bin/env python3
"""Step 01: uniform 150-frame primary match analysis."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))

import primary_match_uniform_sampling as mod  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    mod.UNIFORM_DIR = OUTPUT_DIR / "uniform_150"
    mod.UNIFORM_DIR.mkdir(parents=True, exist_ok=True)
    mod.main()
