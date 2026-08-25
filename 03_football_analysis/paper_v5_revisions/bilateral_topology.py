#!/usr/bin/env python3
"""
Bilateral topology (Paper v5 revision, §3.10)
=============================================

Closes the team-identity gap in the main pipeline by running the tactical-scale
TDA pipeline independently on each team's 11-player sub-cloud, then quantifying
the per-frame cross-team coupling.

For each frame in the 10-match uniform sample we compute:

  - Per-team tactical H1 total persistence  H1_A(t), H1_B(t)
  - Per-team tactical H1 count               n_A(t), n_B(t)
  - Cross-team bottleneck distance           d_B(D_A, D_B)
  - Cross-team landscape L^2 distance        ||lambda_A - lambda_B||

Aggregations over the 10-match cohort:

  - Per-team H1 presence rate, mean H1 count, mean H1 total persistence
  - Cross-team Spearman rho on the H1 total-persistence sequence
    (lag 0; lagged +/- 1, 5, 10 frames as a robustness check)
  - Match-level bootstrap 95% CI on each headline statistic (1,000 resamples)
  - Median / IQR / max of cross-team bottleneck and landscape L^2 distances

Usage:
    python bilateral_topology.py --skillcorner-only [--n-boot 1000] [--seed 42]

Outputs:
    results/paper_v5_revisions/bilateral_topology.csv
    results/paper_v5_revisions/bilateral_topology_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
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
LAGS = (-10, -5, -1, 0, 1, 5, 10)


def _diagram_to_array(diagram) -> np.ndarray:
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
    except Exception:
        return float("nan")


def landscape_l2(d1: np.ndarray, d2: np.ndarray, resolution: int = 100) -> float:
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
    except Exception:
        return float("nan")


def per_frame_bilateral(frame) -> dict | None:
    """Run the tactical-scale pipeline independently on each team's sub-cloud."""
    home = np.asarray(frame.home_positions, dtype=float)
    away = np.asarray(frame.away_positions, dtype=float)
    # Need at least 3 points per team for a non-trivial H1; we report exactly 11+11
    # to keep the inference symmetric. Frames with reduced team coverage (e.g.\ red
    # card minutes) are dropped from the bilateral analysis.
    if home.shape[0] != 11 or away.shape[0] != 11:
        return None

    res_home = compute_h1_at_scale(home, TACTICAL_DELTA)
    res_away = compute_h1_at_scale(away, TACTICAL_DELTA)
    d_home = _diagram_to_array(res_home.h1_diagram)
    d_away = _diagram_to_array(res_away.h1_diagram)

    return {
        "home_h1_count": int(res_home.h1_count),
        "home_h1_total_persistence": float(res_home.h1_stats.get("total", 0.0)),
        "home_h1_mean_persistence": float(res_home.h1_stats.get("mean", 0.0)),
        "home_h1_max_persistence": float(res_home.h1_stats.get("max", 0.0)),
        "home_clusters": int(res_home.cluster_count),
        "away_h1_count": int(res_away.h1_count),
        "away_h1_total_persistence": float(res_away.h1_stats.get("total", 0.0)),
        "away_h1_mean_persistence": float(res_away.h1_stats.get("mean", 0.0)),
        "away_h1_max_persistence": float(res_away.h1_stats.get("max", 0.0)),
        "away_clusters": int(res_away.cluster_count),
        "d_bottleneck_AB": bottleneck(d_home, d_away),
        "d_landscape_l2_AB": landscape_l2(d_home, d_away),
    }


def collect(args: argparse.Namespace) -> pd.DataFrame:
    rows: list[dict] = []
    for meta in skillcorner.list_matches():
        mid = meta["id"]
        try:
            match = skillcorner.load_match(
                mid,
                sample_every=args.sample_every,
                require_complete=True,
                max_frames=args.max_frames,
            )
        except FileNotFoundError:
            continue
        complete = match.complete_frames
        print(f"[{mid}] {match.info.home_team} vs {match.info.away_team}: {len(complete)} frames")
        for frame_idx, frame in enumerate(complete):
            res = per_frame_bilateral(frame)
            if res is None:
                continue
            res.update({"match_id": mid, "frame_idx": frame_idx})
            rows.append(res)
    return pd.DataFrame(rows)


def spearman_with_lag(df: pd.DataFrame, lag: int) -> dict:
    """Spearman rho between home/away tactical-H1 total persistence at given lag.

    Sequences are concatenated within match (frame index is uniform sample
    spacing) and a positive lag shifts away forward in time relative to home.
    """
    rhos = []
    weights = []
    for mid, sub in df.groupby("match_id"):
        sub = sub.sort_values("frame_idx").reset_index(drop=True)
        h = sub["home_h1_total_persistence"].to_numpy()
        a = sub["away_h1_total_persistence"].to_numpy()
        if lag > 0:
            h, a = h[:-lag], a[lag:]
        elif lag < 0:
            h, a = h[-lag:], a[:lag]
        if h.size < 3:
            continue
        if np.allclose(h, h[0]) or np.allclose(a, a[0]):
            continue
        rho, _ = spearmanr(h, a, nan_policy="omit")
        if np.isfinite(rho):
            rhos.append(float(rho))
            weights.append(int(h.size))
    if not rhos:
        return {"n_matches": 0, "rho_mean": float("nan"), "rho_weighted_mean": float("nan")}
    rhos_a = np.asarray(rhos)
    w_a = np.asarray(weights, dtype=float)
    return {
        "n_matches": int(rhos_a.size),
        "rho_mean": float(rhos_a.mean()),
        "rho_weighted_mean": float((rhos_a * w_a).sum() / w_a.sum()),
        "rho_min": float(rhos_a.min()),
        "rho_max": float(rhos_a.max()),
    }


def bootstrap_spearman_lag0(df: pd.DataFrame, n_boot: int, rng: np.random.Generator) -> list[float]:
    """Match-level bootstrap on the lag-0 weighted-mean cross-team Spearman rho."""
    matches = df["match_id"].unique()
    per_match = {}
    for mid, sub in df.groupby("match_id"):
        sub = sub.sort_values("frame_idx").reset_index(drop=True)
        h = sub["home_h1_total_persistence"].to_numpy()
        a = sub["away_h1_total_persistence"].to_numpy()
        if h.size < 3 or np.allclose(h, h[0]) or np.allclose(a, a[0]):
            continue
        rho, _ = spearmanr(h, a, nan_policy="omit")
        if np.isfinite(rho):
            per_match[mid] = (float(rho), int(h.size))
    if not per_match:
        return [float("nan"), float("nan"), float("nan")]
    keys = list(per_match.keys())
    boot = []
    for _ in range(n_boot):
        sample = rng.choice(keys, size=len(keys), replace=True)
        rhos = np.asarray([per_match[m][0] for m in sample])
        ws = np.asarray([per_match[m][1] for m in sample], dtype=float)
        boot.append(float((rhos * ws).sum() / ws.sum()))
    arr = np.asarray(boot)
    return [float(np.mean(arr)), float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))]


def team_summary(df: pd.DataFrame) -> dict:
    """Per-team aggregate H1 statistics, pooled across matches."""
    out = {}
    for side in ("home", "away"):
        h1 = df[f"{side}_h1_count"]
        pers = df[f"{side}_h1_total_persistence"]
        mean_pers = df[f"{side}_h1_mean_persistence"]
        out[side] = {
            "n_frames": int(h1.size),
            "h1_presence_rate": float((h1 > 0).mean()),
            "mean_h1_count_per_frame": float(h1.mean()),
            "mean_h1_total_persistence": float(pers.mean()),
            "mean_h1_mean_persistence_when_present": float(mean_pers[mean_pers > 0].mean()) if (mean_pers > 0).any() else 0.0,
        }
    return out


def distance_summary(series: pd.Series, finite_only: bool = False) -> dict:
    s = series.dropna()
    if finite_only:
        s = s[np.isfinite(s)]
    if s.empty:
        return {"median": float("nan"), "iqr": float("nan"), "max": float("nan"), "n": 0}
    return {
        "median": float(s.median()),
        "iqr": float(s.quantile(0.75) - s.quantile(0.25)),
        "max": float(s.max()) if np.isfinite(s.max()) else float("inf"),
        "n": int(s.size),
    }


def cooccurrence_summary(df: pd.DataFrame) -> dict:
    h_pres = df["home_h1_count"] > 0
    a_pres = df["away_h1_count"] > 0
    n = int(len(df))
    both = int((h_pres & a_pres).sum())
    home_only = int((h_pres & ~a_pres).sum())
    away_only = int((~h_pres & a_pres).sum())
    neither = int((~h_pres & ~a_pres).sum())
    return {
        "n_frames": n,
        "both_teams_h1_present": both,
        "home_only": home_only,
        "away_only": away_only,
        "neither": neither,
        "p_both": float(both / n) if n else float("nan"),
        "p_home_only": float(home_only / n) if n else float("nan"),
        "p_away_only": float(away_only / n) if n else float("nan"),
        "p_neither": float(neither / n) if n else float("nan"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skillcorner-only", action="store_true")
    ap.add_argument("--sample-every", type=int, default=SAMPLE_EVERY)
    ap.add_argument("--max-frames", type=int, default=MAX_FRAMES)
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = collect(args)
    if df.empty:
        raise SystemExit("No bilateral frames retained (no 11+11 frames).")

    out_csv = OUT_DIR / "bilateral_topology.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} ({len(df)} rows, {df['match_id'].nunique()} matches)")

    rng = np.random.default_rng(args.seed)
    summary = {
        "n_frames_total": int(len(df)),
        "n_matches": int(df["match_id"].nunique()),
        "cutoff_delta_m": TACTICAL_DELTA,
        "sample_every": args.sample_every,
        "max_frames_per_match": args.max_frames,
        "per_team": team_summary(df),
        "cross_team_spearman_by_lag": {f"lag_{lag}": spearman_with_lag(df, lag) for lag in LAGS},
        "cross_team_spearman_lag0_bootstrap_ci": bootstrap_spearman_lag0(df, args.n_boot, rng),
        "bottleneck_AB": distance_summary(df["d_bottleneck_AB"]),
        "bottleneck_AB_finite_only": distance_summary(df["d_bottleneck_AB"], finite_only=True),
        "landscape_l2_AB": distance_summary(df["d_landscape_l2_AB"]),
        "cooccurrence": cooccurrence_summary(df),
    }

    out_json = OUT_DIR / "bilateral_topology_summary.json"
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {out_json}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
