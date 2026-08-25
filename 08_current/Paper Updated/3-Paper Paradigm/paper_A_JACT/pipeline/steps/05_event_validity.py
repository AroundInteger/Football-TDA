#!/usr/bin/env python3
"""Step 05: event correlation construct-validity check (summary for Paper A)."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis"))

import real_event_correlation as rec  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    event_dir = OUTPUT_DIR / "event_correlation"
    event_dir.mkdir(parents=True, exist_ok=True)
    rec.OUTPUT_DIR = event_dir
    rec.main()

    # Copy summary to pipeline root outputs
    summary_src = event_dir / "event_correlation_summary.json"
    if summary_src.exists():
        import shutil
        shutil.copy(summary_src, OUTPUT_DIR / "event_correlation_summary.json")
