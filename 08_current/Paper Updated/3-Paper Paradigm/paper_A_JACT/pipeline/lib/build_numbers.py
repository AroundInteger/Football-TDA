#!/usr/bin/env python3
"""Aggregate pipeline outputs into numbers.json for sync_to_paper."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, load_config  # noqa: E402


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def main() -> None:
    cfg = load_config()
    uniform = load_json(OUTPUT_DIR / "uniform_150" / "uniform_summary.json")
    agg = load_json(OUTPUT_DIR / "aggregate_stats.json")
    comp = load_json(OUTPUT_DIR / "complementarity" / "complementarity_tests.json")
    card_null = load_json(OUTPUT_DIR / "cardinality_null" / "summary.json")
    linkage = load_json(OUTPUT_DIR / "linkage" / "linkage_headline.json")
    boot = load_json(OUTPUT_DIR / "complementarity" / "bootstrap_multi_match_ci.json")
    event = load_json(OUTPUT_DIR / "event_correlation_summary.json")
    event_pairs = event.get("n_events_total")
    fig_meta = load_json(OUTPUT_DIR / "figure_cycle_geometry.json")

    regimes = {}
    regime_path = OUTPUT_DIR / "regime_summary.csv"
    if regime_path.exists():
        df = pd.read_csv(regime_path)
        for _, row in df.iterrows():
            if "adopted_cutoff_m" not in df.columns:
                raise ValueError(
                    "regime_summary.csv must come from the cardinality-inversion "
                    "protocol (column adopted_cutoff_m)."
                )
            entry = {
                "adopted_cutoff_m": float(row["adopted_cutoff_m"]),
                "selection_rule": row.get("selection_rule"),
                "pooled_mean_h0": (
                    float(row["pooled_mean_h0"])
                    if "pooled_mean_h0" in df.columns
                    else None
                ),
                "acceptance_all_ok": (
                    bool(row["acceptance_all_ok"])
                    if "acceptance_all_ok" in df.columns
                    else None
                ),
                "per_match_delta_mean": (
                    float(row["per_match_delta_mean"])
                    if "per_match_delta_mean" in df.columns
                    else None
                ),
                "per_match_delta_std": (
                    float(row["per_match_delta_std"])
                    if "per_match_delta_std" in df.columns
                    else None
                ),
            }
            regimes[row["scale"]] = entry

    h1_primary = uniform.get("h1", {})
    numbers = {
        "primary_match_id": cfg["primary_match_id"],
        "sampling_uniform": uniform.get("sampling"),
        "sampling_step": uniform.get("sampling"),
        "n_frames_analysed_primary": uniform.get("n_frames_analysed"),
        "total_frames_primary": uniform.get("total_frames_in_match"),
        "h0_primary": uniform.get("h0"),
        "h1_primary": h1_primary,
        "regimes": regimes,
        "multi_match": {
            "individual": agg.get("individual", {}),
            "tactical": agg.get("tactical", {}),
            "team": agg.get("team", {}),
        },
        "complementarity": comp.get("complementarity", {}),
        "cardinality_null": card_null,
        "linkage": linkage,
        "bootstrap": boot.get("match_level", {}),
        "tda_native": comp.get("tda_native", load_json(
            OUTPUT_DIR / "complementarity" / "tda_native_distances_summary.json"
        )),
        "event_pairs": event_pairs,
        "figure_cycle_geometry": fig_meta,
    }

    # Flatten headline scalars for sync
    flat = {
        "primary_h1_individual_total": h1_primary.get("individual", {}).get("total_loops"),
        "primary_h1_individual_presence_pct": round(
            100 * h1_primary.get("individual", {}).get("presence_rate", 0), 1
        ),
        "primary_h1_tactical_total": h1_primary.get("tactical", {}).get("total_loops"),
        "primary_h1_tactical_presence_pct": round(
            100 * h1_primary.get("tactical", {}).get("presence_rate", 0), 1
        ),
        "multi_h1_individual_presence_pct": round(
            100 * agg.get("individual", {}).get("h1_presence_rate", 0), 1
        ),
        "multi_h1_tactical_presence_pct": round(
            100 * agg.get("tactical", {}).get("h1_presence_rate", 0), 1
        ),
        "spearman_rho": comp.get("complementarity", {}).get("spearman_rho"),
        "spearman_rho_counts": comp.get("complementarity", {}).get("spearman_rho_counts"),
        "cutoff_individual": regimes.get("individual", {}).get("adopted_cutoff_m"),
        "cutoff_tactical": regimes.get("tactical", {}).get("adopted_cutoff_m"),
        "cutoff_team": regimes.get("team", {}).get("adopted_cutoff_m"),
        "event_topology_pairs": event_pairs,
    }
    if linkage.get("tactical_h1_total"):
        th = linkage["tactical_h1_total"]
        flat["linkage_tactical_h1_single"] = th.get("single")
        flat["linkage_tactical_h1_complete"] = th.get("complete")
        flat["linkage_tactical_h1_ward"] = th.get("ward")
    numbers["headline"] = flat

    out = OUTPUT_DIR / "numbers.json"
    with open(out, "w") as f:
        json.dump(numbers, f, indent=2)
    print(f"Wrote {out}")
    print(json.dumps(flat, indent=2))


if __name__ == "__main__":
    main()
