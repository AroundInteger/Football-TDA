#!/usr/bin/env python3
"""
Event-window sensitivity (Paper v5 revision, §3.8 supplementary)
================================================================

Re-runs the event-correlation analysis over a range of window half-widths
(+/- W frames at 10 Hz sampling), W in {5, 10, 20, 50} -> +/- {0.5, 1, 2, 5} s,
and reports, per event type and scale, the sign and significance of the mean
persistence change. Purpose: confirm that the headline event-type effects are
stable to the choice of event window.

Usage:
    python event_window_sensitivity.py

Outputs:
    results/paper_v5_revisions/event_window_sensitivity.csv
    results/paper_v5_revisions/event_window_sensitivity.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "01_data"))
sys.path.insert(0, str(PROJECT_ROOT / "02_tda_core"))

OUT_DIR = PROJECT_ROOT / "results" / "paper_v5_revisions"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WINDOW_HALF_WIDTHS = [5, 10, 20, 50]  # frames at 10 Hz = 0.5, 1, 2, 5 seconds


def run_for_window(half_width: int) -> pd.DataFrame:
    """Invoke real_event_correlation.py with a monkey-patched window.

    We shell out to python -c with the pipeline's window constants overridden
    via an environment variable; real_event_correlation.py consults
    ``EVENT_WINDOW_HALF`` when present.
    """
    env = {"EVENT_WINDOW_HALF": str(half_width)}
    script = PROJECT_ROOT / "03_football_analysis" / "real_event_correlation.py"
    out_csv = OUT_DIR / f"event_correlation_window_{half_width}.csv"
    cmd = [sys.executable, str(script), "--out-csv", str(out_csv)]
    print(f"Running {cmd} with EVENT_WINDOW_HALF={half_width}")
    subprocess.check_call(cmd, env={**__import__("os").environ, **env})
    df = pd.read_csv(out_csv)
    df["window_half_frames"] = half_width
    df["window_half_seconds"] = half_width / 10.0
    return df


def main() -> None:
    frames = []
    for w in WINDOW_HALF_WIDTHS:
        try:
            frames.append(run_for_window(w))
        except Exception as e:
            print(f"[warn] window {w}: {e}")

    if not frames:
        print("No successful runs; aborting.")
        return

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(OUT_DIR / "event_window_sensitivity.csv", index=False)

    summary: dict = {"window_half_frames": WINDOW_HALF_WIDTHS}
    for (scale, event_type), g in combined.groupby(["scale", "event_type"]):
        bucket = summary.setdefault(scale, {}).setdefault(event_type, {})
        for w, row in g.groupby("window_half_frames"):
            col = "persistence_delta" if "persistence_delta" in row else "delta_persistence"
            mean = float(row[col].mean())
            p = float(row["p_value"].iloc[0]) if "p_value" in row.columns else None
            sign = "+" if mean > 0 else ("-" if mean < 0 else "0")
            bucket[str(w)] = {"mean": mean, "p": p, "sign": sign}
    with open(OUT_DIR / "event_window_sensitivity.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {OUT_DIR / 'event_window_sensitivity.json'}")


if __name__ == "__main__":
    main()
