#!/usr/bin/env python3
"""
Bootstrap confidence intervals for multi-match headline statistics
==================================================================

Draws ``n_boot`` (default 1000) bootstrap resamples *over matches* of the
multi-match results in ``08_current/data/multi_match/per_frame_results.csv``
and ``event_correlation/event_topology_correlation.csv``, and reports 95%
CIs for:

    - Individual-scale H1 presence rate (fraction of frames with H1 > 0)
    - Tactical-scale H1 presence rate
    - Cross-scale Spearman rho between individual and tactical H1 persistence
    - Fisher-exact odds ratio for cross-scale co-occurrence of H1 features
    - Event-wise mean persistence change for on-ball engagement, passing option,
      build-up phase, quick break, chaotic phase (both scales)

The match is the resampling unit, consistent with the inference level used in
the paper (between-match variability rather than within-match pseudo-replicates).

Usage:
    python bootstrap_multi_match_ci.py --n-boot 1000 --seed 42

Output:
    results/paper_v5_revisions/bootstrap_multi_match_ci.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, spearmanr

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "08_current" / "data"
OUT_DIR = PROJECT_ROOT / "results" / "paper_v5_revisions"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def bootstrap_by_match(per_frame: pd.DataFrame, rng: np.random.Generator, n_boot: int) -> dict:
    matches = per_frame["match_id"].unique()
    n = len(matches)
    ind = per_frame[per_frame["scale"] == "individual"].set_index("match_id")
    tac = per_frame[per_frame["scale"] == "tactical"].set_index("match_id")

    rates_ind, rates_tac, rhos, ors = [], [], [], []
    for _ in range(n_boot):
        sample = rng.choice(matches, size=n, replace=True)
        dfi = pd.concat([ind.loc[[m]] for m in sample])
        dft = pd.concat([tac.loc[[m]] for m in sample])
        rates_ind.append(float((dfi["h1"] > 0).mean()))
        rates_tac.append(float((dft["h1"] > 0).mean()))
        pers_col = "h1_total_persistence"
        merged = dfi[[pers_col]].rename(columns={pers_col: "ind"}).reset_index(drop=True)
        merged["tac"] = dft[pers_col].reset_index(drop=True)
        rho, _ = spearmanr(merged["ind"], merged["tac"], nan_policy="omit")
        rhos.append(float(rho))
        a = int(((merged["ind"] > 0) & (merged["tac"] > 0)).sum())
        b = int(((merged["ind"] > 0) & (merged["tac"] == 0)).sum())
        c = int(((merged["ind"] == 0) & (merged["tac"] > 0)).sum())
        d = int(((merged["ind"] == 0) & (merged["tac"] == 0)).sum())
        try:
            or_val, _ = fisher_exact([[a, b], [c, d]])
        except ValueError:
            or_val = float("nan")
        ors.append(float(or_val))

    def ci(arr):
        a = np.asarray(arr, dtype=float)
        a = a[np.isfinite(a)]
        if a.size == 0:
            return [float("nan")] * 3
        return [float(np.mean(a)), float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]

    return {
        "h1_presence_individual": ci(rates_ind),
        "h1_presence_tactical": ci(rates_tac),
        "spearman_rho_individual_tactical": ci(rhos),
        "fisher_odds_ratio_cooccurrence": ci(ors),
    }


def bootstrap_events(
    events_df: pd.DataFrame, rng: np.random.Generator, n_boot: int, scales: list[str]
) -> dict:
    by_match = {m: g for m, g in events_df.groupby("match_id")}
    matches = list(by_match.keys())
    n = len(matches)
    # Names must match ``event_topology_correlation.csv`` (see 03_football_analysis pipeline).
    event_types = [
        "on_ball_engagement",
        "passing_option",
        "build_up",
        "quick_break",
        "chaotic",
    ]
    out = {}
    for scale in scales:
        out[scale] = {}
        for etype in event_types:
            means = []
            for _ in range(n_boot):
                sample = rng.choice(matches, size=n, replace=True)
                rows = pd.concat([by_match[m] for m in sample])
                sub = rows[(rows["scale"] == scale) & (rows["event_type"] == etype)]
                if sub.empty:
                    means.append(float("nan"))
                    continue
                means.append(float(sub["persistence_delta"].mean()))
            arr = np.asarray(means, dtype=float)
            arr = arr[np.isfinite(arr)]
            if arr.size == 0:
                out[scale][etype] = [float("nan")] * 3
            else:
                out[scale][etype] = [
                    float(np.mean(arr)),
                    float(np.percentile(arr, 2.5)),
                    float(np.percentile(arr, 97.5)),
                ]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    per_frame = pd.read_csv(DATA_DIR / "multi_match" / "per_frame_results.csv")
    match_summary = bootstrap_by_match(per_frame, rng, args.n_boot)

    events_path = DATA_DIR / "event_correlation" / "event_topology_correlation.csv"
    event_summary = {}
    if events_path.exists():
        events_df = pd.read_csv(events_path)
        event_summary = bootstrap_events(events_df, rng, args.n_boot, ["individual", "tactical"])
    else:
        event_summary = {"note": f"missing {events_path}"}

    out = {
        "n_boot": args.n_boot,
        "seed": args.seed,
        "resample_unit": "match",
        "match_level": match_summary,
        "events": event_summary,
    }
    out_json = OUT_DIR / "bootstrap_multi_match_ci.json"
    with open(out_json, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
