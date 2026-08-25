#!/usr/bin/env python3
"""Aggregate Paper B pipeline outputs into numbers.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, load_config  # noqa: E402


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


if __name__ == "__main__":
    cfg = load_config()
    event = load_json(OUTPUT_DIR / "event_correlation_summary.json")
    baseline = load_json(OUTPUT_DIR / "baseline_vs_topology_summary.json")
    bilateral = load_json(OUTPUT_DIR / "bilateral_topology_summary.json")
    predictive = load_json(OUTPUT_DIR / "predictive_utility_summary.json")

    buildup = predictive.get("results", {}).get(
        "is_buildup_with_total_persistence", {}
    )
    block_a = buildup.get("block_A_baselines_only", {}).get("metrics", {})
    block_b = buildup.get("block_B_baselines_plus_topology", {}).get("metrics", {})

    lag0 = (
        bilateral.get("cross_team_spearman_by_lag", {})
        .get("lag_0", {})
        .get("rho_mean")
    )
    partial = baseline.get(
        "partial_r2_baseline_residual_explained_by_topology", {}
    )

    numbers = {
        "primary_match_id": cfg["primary_match_id"],
        "event_pairs": event.get("n_events_total"),
        "baseline": baseline,
        "bilateral": bilateral,
        "predictive_buildup": buildup,
        "headline": {
            "event_topology_pairs": event.get("n_events_total"),
            "cross_team_spearman_lag0": lag0,
            "spearman_width": baseline.get("spearman_width_m", {}).get("rho"),
            "spearman_hull": baseline.get("spearman_hull_area_m2", {}).get("rho"),
            "partial_r2_hull": partial.get("hull_area_m2"),
            "home_h1_presence": bilateral.get("per_team", {})
            .get("home", {})
            .get("h1_presence_rate"),
            "away_h1_presence": bilateral.get("per_team", {})
            .get("away", {})
            .get("h1_presence_rate"),
            "auc_baseline": block_a.get("auc"),
            "auc_with_topology": block_b.get("auc"),
            "delta_auc": buildup.get("delta_auc_pooled"),
            "chaotic_prevalence": predictive.get("results", {})
            .get("is_chaotic_with_total_persistence", {})
            .get("block_A_baselines_only", {})
            .get("metrics", {})
            .get("prevalence"),
        },
    }
    out = OUTPUT_DIR / "numbers.json"
    with open(out, "w") as f:
        json.dump(numbers, f, indent=2)
    print(f"Wrote {out}")
