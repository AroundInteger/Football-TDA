#!/usr/bin/env python3
"""
Baseline-vs-Topology (Paper v5 revision, §3.9)
==============================================

Quantifies how much information tactical-scale H1 persistence carries beyond
standard geometric descriptors used in football analytics. For every analysis
frame we compute:

  - Tactical-scale H1 persistence (sum of birth-death lifetimes at delta=12 m)
  - Team length (max - min x of the 22 players)
  - Team width (max - min y)
  - Convex-hull area
  - Voronoi dispersion entropy (Shannon entropy of cell areas)

and report Spearman rho between each baseline and the topological variable,
plus the partial R^2 of the topological variable after regressing on the
baseline block.

Usage:
    python baseline_vs_topology.py --skillcorner-only

Outputs:
    results/paper_v5_revisions/baseline_vs_topology.csv
    results/paper_v5_revisions/baseline_vs_topology_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull, Voronoi
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "01_data"))
sys.path.insert(0, str(PROJECT_ROOT / "02_tda_core"))

from loaders import skillcorner  # noqa: E402
from tda_utils import VALIDATED_CUTOFFS, compute_h1_at_scale  # noqa: E402

OUT_DIR = PROJECT_ROOT / "results" / "paper_v5_revisions"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TACTICAL_DELTA = VALIDATED_CUTOFFS["tactical"]
SAMPLE_EVERY = 100
MAX_FRAMES = 150


def voronoi_entropy(points: np.ndarray) -> float:
    """Shannon entropy of (bounded) Voronoi cell areas; robust to unbounded cells."""
    if points.shape[0] < 4:
        return np.nan
    try:
        vor = Voronoi(points)
    except Exception:
        return np.nan
    areas = []
    for region_index in vor.point_region:
        region = vor.regions[region_index]
        if not region or -1 in region:
            continue
        verts = vor.vertices[region]
        if verts.shape[0] < 3:
            continue
        try:
            areas.append(ConvexHull(verts).volume)  # volume is area in 2D
        except Exception:
            continue
    if not areas:
        return np.nan
    a = np.asarray(areas, dtype=float)
    a = a[a > 0]
    if a.size == 0:
        return np.nan
    p = a / a.sum()
    return float(-(p * np.log(p)).sum())


def per_frame_features(positions: np.ndarray) -> dict:
    """Return baseline geometric descriptors + tactical H1 persistence."""
    xy = np.asarray(positions, dtype=float)
    length = float(xy[:, 0].ptp())
    width = float(xy[:, 1].ptp())
    try:
        hull_area = float(ConvexHull(xy).volume)
    except Exception:
        hull_area = np.nan
    vent = voronoi_entropy(xy)
    diagrams = compute_h1_at_scale(xy, TACTICAL_DELTA)
    h1_persistence = float(diagrams.h1_stats.get("total", 0.0))
    return {
        "length_m": length,
        "width_m": width,
        "hull_area_m2": hull_area,
        "voronoi_entropy": vent,
        "tactical_h1_persistence": h1_persistence,
    }


def partial_r2(y: np.ndarray, x_topology: np.ndarray, x_baseline: np.ndarray) -> float:
    """Partial R^2 of x_topology after regressing y on x_baseline."""
    from numpy.linalg import lstsq

    y = np.asarray(y, dtype=float)
    x_baseline = np.asarray(x_baseline, dtype=float)
    x_topology = np.asarray(x_topology, dtype=float).reshape(-1, 1)
    mask = np.all(np.isfinite(np.column_stack([y, x_baseline, x_topology])), axis=1)
    y = y[mask]
    x_baseline = x_baseline[mask]
    x_topology = x_topology[mask]
    if y.size < 10:
        return float("nan")
    Xb = np.column_stack([np.ones_like(y), x_baseline])
    beta, *_ = lstsq(Xb, y, rcond=None)
    resid_baseline = y - Xb @ beta
    Xf = np.column_stack([Xb, x_topology])
    beta_full, *_ = lstsq(Xf, y, rcond=None)
    resid_full = y - Xf @ beta_full
    ss_b = float((resid_baseline ** 2).sum())
    ss_f = float((resid_full ** 2).sum())
    if ss_b <= 0:
        return float("nan")
    return (ss_b - ss_f) / ss_b


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skillcorner-only", action="store_true")
    args = parser.parse_args()

    rows = []
    sc_matches = skillcorner.list_matches()
    for meta in sc_matches:
        mid = meta["id"]
        try:
            match = skillcorner.load_match(
                mid,
                sample_every=SAMPLE_EVERY,
                require_complete=True,
                max_frames=MAX_FRAMES,
            )
        except FileNotFoundError:
            continue
        complete = match.complete_frames
        print(f"[{mid}] {match.info.home_team} vs {match.info.away_team}: {len(complete)} frames")
        for frame_idx, frame in enumerate(complete):
            features = per_frame_features(frame.all_positions)
            features.update({"match_id": mid, "frame_idx": frame_idx})
            rows.append(features)

    df = pd.DataFrame(rows)
    out_csv = OUT_DIR / "baseline_vs_topology.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} ({len(df)} rows)")

    summary = {"n_frames": int(len(df)), "n_matches": int(df["match_id"].nunique())}
    baseline_cols = ["length_m", "width_m", "hull_area_m2", "voronoi_entropy"]
    for col in baseline_cols:
        rho, p = spearmanr(df[col], df["tactical_h1_persistence"], nan_policy="omit")
        summary[f"spearman_{col}"] = {"rho": float(rho), "p": float(p)}
    # Per baseline: share of that geometric measure explained by tactical H1 after
    # controlling for the other three baselines (not incremental R² for H1 on itself).
    r2_each = {}
    for col in baseline_cols:
        r2_each[col] = partial_r2(
            df[col].to_numpy(),
            df["tactical_h1_persistence"].to_numpy(),
            df[[c for c in baseline_cols if c != col]].to_numpy(),
        )
    summary["partial_r2_baseline_residual_explained_by_topology"] = r2_each

    out_json = OUT_DIR / "baseline_vs_topology_summary.json"
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
