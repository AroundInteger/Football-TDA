#!/usr/bin/env python3
"""Step 02: cutoff sweep and regime stability (SkillCorner primary match)."""
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))

import primary_match_skillcorner_analysis as mod  # noqa: E402

if __name__ == "__main__":
    ensure_dirs()

    mod.ensure_match_assets()
    frames, home, away = mod.load_tracking_data(require_complete=True)
    match_name = f"{home} vs {away}"

    sweep_df = mod.run_cutoff_sweep(frames, n_cutoffs=100)
    sweep_df.to_csv(OUTPUT_DIR / "cutoff_sweep_results.csv", index=False)

    regimes, sweep_agg = mod.identify_regimes(sweep_df)
    regimes.to_csv(OUTPUT_DIR / "regime_summary.csv", index=False)

    with open(OUTPUT_DIR / "cutoff_sweep_agg.csv", "w") as f:
        sweep_agg.to_csv(f, index=False)

    print(regimes.to_string(index=False))
    print(f"Saved regime_summary.csv to {OUTPUT_DIR}")
