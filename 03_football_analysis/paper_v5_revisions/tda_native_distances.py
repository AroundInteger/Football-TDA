#!/usr/bin/env python3
"""
TDA-native distances (Paper v5 revision, §3.5)
==============================================

For each sampled frame of each match, computes TDA-native distances between
the individual-scale and tactical-scale H1 persistence diagrams:

  - Bottleneck distance d_B(D_ind, D_tac) via gudhi.bottleneck_distance
  - Landscape L^2 distance between persistence landscapes (Bubenik 2015)
    computed via gudhi.representations.Landscape

The resulting distributions augment the Spearman/Fisher summary of scale
complementarity (§3.5) with TDA-native measures; a short paragraph of
summary statistics (median, IQR, max) is added to §3.5 on execution.

Usage:
    python tda_native_distances.py --skillcorner-only

Outputs:
    results/paper_v5_revisions/tda_native_distances.csv
    results/paper_v5_revisions/tda_native_distances_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "01_data"))
sys.path.insert(0, str(PROJECT_ROOT / "02_tda_core"))

from loaders import skillcorner  # noqa: E402
from tda_utils import VALIDATED_CUTOFFS, compute_h1_at_scale  # noqa: E402

OUT_DIR = PROJECT_ROOT / "results" / "paper_v5_revisions"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _diagram_to_array(diagram) -> np.ndarray:
    """Coerce an H1 diagram to an (n, 2) float array of (birth, death)."""
    if diagram is None:
        return np.zeros((0, 2), dtype=float)
    arr = np.asarray(diagram, dtype=float)
    if arr.ndim == 1 and arr.size == 2:
        return arr.reshape(1, 2)
    if arr.ndim == 2 and arr.shape[1] >= 2:
        return arr[:, :2]
    return np.zeros((0, 2), dtype=float)


def bottleneck(d1: np.ndarray, d2: np.ndarray) -> float:
    try:
        from gudhi import bottleneck_distance

        return float(bottleneck_distance(d1.tolist(), d2.tolist()))
    except Exception as e:
        print(f"[gudhi bottleneck failed] {e}")
        return float("nan")


def landscape_l2(d1: np.ndarray, d2: np.ndarray, resolution: int = 100) -> float:
    """L² distance between persistence landscapes; empty diagrams use a far-off off-diagonal point."""
    try:
        from gudhi.representations import Landscape

        d1 = np.asarray(d1, dtype=np.float64).reshape((-1, 2)) if d1.size else np.zeros((0, 2), dtype=np.float64)
        d2 = np.asarray(d2, dtype=np.float64).reshape((-1, 2)) if d2.size else np.zeros((0, 2), dtype=np.float64)
        if d1.shape[0] == 0 and d2.shape[0] == 0:
            return 0.0
        empty = np.array([[0.0, 0.0]], dtype=np.float64)
        use1, use2 = (d1 if d1.shape[0] else empty), (d2 if d2.shape[0] else empty)
        stacked = np.vstack([use1, use2])
        bounds = [float(stacked[:, 0].min()), float(stacked[:, 1].max())]
        if not np.isfinite(bounds[0]) or not np.isfinite(bounds[1]) or bounds[0] >= bounds[1]:
            bounds = [0.0, 1.0]
        lscape = Landscape(num_landscapes=3, resolution=resolution)
        lscape.sample_range = bounds
        L = lscape.fit_transform([use1, use2])
        return float(np.linalg.norm(L[0].astype(float) - L[1].astype(float)))
    except Exception as e:
        print(f"[gudhi landscape failed] {e}")
        return float("nan")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skillcorner-only", action="store_true")
    ap.add_argument("--sample-every", type=int, default=100)
    ap.add_argument("--max-frames", type=int, default=150)
    args = ap.parse_args()

    rows = []
    for meta in skillcorner.list_matches():
        try:
            match = skillcorner.load_match(
                meta["id"],
                sample_every=args.sample_every,
                require_complete=True,
                max_frames=args.max_frames,
            )
        except FileNotFoundError:
            continue
        print(f"[{meta['id']}] {len(match.complete_frames)} frames")
        for frame_idx, frame in enumerate(match.complete_frames):
            ind = compute_h1_at_scale(frame.all_positions, VALIDATED_CUTOFFS["individual"])
            tac = compute_h1_at_scale(frame.all_positions, VALIDATED_CUTOFFS["tactical"])
            d_ind = _diagram_to_array(getattr(ind, "h1_diagram", ind))
            d_tac = _diagram_to_array(getattr(tac, "h1_diagram", tac))
            rows.append(
                {
                    "match_id": meta["id"],
                    "frame_idx": frame_idx,
                    "d_bottleneck": bottleneck(d_ind, d_tac),
                    "d_landscape_l2": landscape_l2(d_ind, d_tac),
                    "n_h1_individual": int(d_ind.shape[0]),
                    "n_h1_tactical": int(d_tac.shape[0]),
                }
            )

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "tda_native_distances.csv", index=False)

    def summary(series: pd.Series) -> dict:
        s = series.dropna()
        if s.empty:
            return {
                "median": float("nan"),
                "iqr": float("nan"),
                "p95": float("nan"),
                "max": float("nan"),
            }
        return {
            "median": float(s.median()),
            "iqr": float(s.quantile(0.75) - s.quantile(0.25)),
            # results.tex quotes p95 as the tail. It must be emitted here, or a
            # re-run silently unbacks that number (ruling R14).
            "p95": float(np.percentile(s, 95)),
            "max": float(s.max()),
            "n": int(s.size),
        }

    out = {
        "n_frames": int(len(df)),
        "n_matches": int(df["match_id"].nunique()),
        "source_csv": "tda_native_distances.csv",
        "bottleneck": summary(df["d_bottleneck"]),
        "landscape_l2": summary(df["d_landscape_l2"]),
    }
    with open(OUT_DIR / "tda_native_distances_summary.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
