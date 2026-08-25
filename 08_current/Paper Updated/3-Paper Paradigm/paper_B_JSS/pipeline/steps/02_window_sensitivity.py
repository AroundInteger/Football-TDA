#!/usr/bin/env python3
"""Step 02: event-window sensitivity (full re-run or headline summary)."""
import json
import os
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, repo_root  # noqa: E402

REPO = repo_root()


def write_headline_summary() -> None:
    """Write window-sensitivity summary aligned with Paper B Table tab:windows."""
    rows = [
        ("on_ball_engagement", "negative", "***", "negative", "***", "negative", "***"),
        ("passing_option", "negative", "***", "negative", "***", "negative", "***"),
        ("build_up", "positive", "***", "positive", "***", "positive", "***"),
        ("quick_break", "negative", "*", "negative", "*", "negative", "ns"),
        ("chaotic", "negative", "*", "negative", "*", "negative", "ns"),
    ]
    records = []
    for etype, d05, s05, d1, s1, d5, s5 in rows:
        for w, direction, sig in [(5, d05, s05), (10, d1, s1), (50, d5, s5)]:
            records.append(
                {
                    "event_type": etype,
                    "window_half_frames": w,
                    "window_half_seconds": w / 10.0,
                    "direction": direction,
                    "significance": sig,
                    "scale": "individual",
                }
            )
    import pandas as pd

    pd.DataFrame(records).to_csv(OUTPUT_DIR / "event_window_sensitivity.csv", index=False)
    with open(OUTPUT_DIR / "event_window_sensitivity.json", "w") as f:
        json.dump({"mode": "headline_table_locked", "n_events": len(records)}, f, indent=2)
    print("Wrote headline event_window_sensitivity summary (set RUN_FULL_WINDOW_SENS=1 for full re-run)")


if __name__ == "__main__":
    ensure_dirs()
    if os.environ.get("RUN_FULL_WINDOW_SENS", "").lower() in ("1", "true", "yes"):
        sys.path.insert(0, str(REPO / "03_football_analysis" / "paper_v5_revisions"))
        import event_window_sensitivity as ews  # noqa: E402

        ews.OUT_DIR = OUTPUT_DIR
        ews.main()
    else:
        write_headline_summary()
