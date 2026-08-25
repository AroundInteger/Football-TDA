#!/usr/bin/env python3
"""Step 08: linkage-method comparison (Discussion §Limitations)."""
import json
import os
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, analysis_root, ensure_dirs  # noqa: E402

REPO = analysis_root()
sys.path.insert(0, str(REPO / "03_football_analysis"))

import linkage_method_comparison as lc  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()
    out = OUTPUT_DIR / "linkage"
    out.mkdir(parents=True, exist_ok=True)
    lc.OUTPUT_DIR = out

    os.chdir(REPO)
    lc.main()

    summary_path = out / "linkage_summary.json"
    if not summary_path.exists():
        raise SystemExit(f"Expected {summary_path} after linkage comparison")

    summary = json.loads(summary_path.read_text())
    meta = {
        "n_matches": 4,
        "n_frames_per_match": 150,
        "n_frames_total": 600,
        "methods": lc.METHODS,
        "tactical_cutoff_m": lc.VALIDATED_CUTOFFS["tactical"],
        "tactical_h1_total": {
            method: summary["tactical"][method]["total_h1"] for method in lc.METHODS
        },
    }
    with open(out / "linkage_headline.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Linkage headline: {meta['tactical_h1_total']}")
