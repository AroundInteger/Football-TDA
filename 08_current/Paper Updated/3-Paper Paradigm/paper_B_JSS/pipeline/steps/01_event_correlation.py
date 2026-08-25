#!/usr/bin/env python3
"""Step 01: event–topology correlation (reuse Paper A output when available)."""
import shutil
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, PAPER_A_OUTPUTS, ensure_dirs, repo_root, load_config  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis"))
import real_event_correlation as rec  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    paper_a_event = PAPER_A_OUTPUTS / "event_correlation"
    if (paper_a_event / "event_topology_correlation.csv").exists():
        dest = OUTPUT_DIR / "event_correlation"
        dest.mkdir(parents=True, exist_ok=True)
        for name in ("event_topology_correlation.csv", "event_correlation_summary.json"):
            src = paper_a_event / name
            if src.exists():
                shutil.copy(src, dest / name)
        shutil.copy(
            paper_a_event / "event_correlation_summary.json",
            OUTPUT_DIR / "event_correlation_summary.json",
        )
        print(f"Copied event correlation from Paper A pipeline ({paper_a_event})")
    else:
        rec.OUTPUT_DIR = OUTPUT_DIR / "event_correlation"
        rec.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        rec.main()
        summary = rec.OUTPUT_DIR / "event_correlation_summary.json"
        if summary.exists():
            shutil.copy(summary, OUTPUT_DIR / "event_correlation_summary.json")
