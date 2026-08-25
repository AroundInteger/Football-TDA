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
            cutoff_col = (
                "adopted_cutoff_m"
                if "adopted_cutoff_m" in df.columns
                else "optimal_cutoff"
            )
            stability_col = (
                "stability_at_adopted"
                if "stability_at_adopted" in df.columns
                else "stability"
            )
            entry = {
                "adopted_cutoff_m": float(row[cutoff_col]),
                "validation_rate": float(row["validation_rate"]),
                "stability_at_adopted": float(row[stability_col]),
            }
            if "ch_optimum_m" in df.columns and pd.notna(row.get("ch_optimum_m")):
                entry["ch_optimum_m"] = float(row["ch_optimum_m"])
            if "stability_at_ch_optimum" in df.columns and pd.notna(
                row.get("stability_at_ch_optimum")
            ):
                entry["stability_at_ch_optimum"] = float(row["stability_at_ch_optimum"])
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
        "stability_individual": regimes.get("individual", {}).get(
            "stability_at_adopted", regimes.get("individual", {}).get("stability")
        ),
        "stability_tactical": regimes.get("tactical", {}).get(
            "stability_at_adopted", regimes.get("tactical", {}).get("stability")
        ),
        "stability_team": regimes.get("team", {}).get(
            "stability_at_adopted", regimes.get("team", {}).get("stability")
        ),
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
