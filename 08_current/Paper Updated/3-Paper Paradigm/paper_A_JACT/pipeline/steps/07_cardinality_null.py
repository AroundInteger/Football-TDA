#!/usr/bin/env python3
"""Step 07: is H1 detection driven by centroid count or by centroid arrangement?

Remark `rem:teamnull` proves H1 vanishes when clustering leaves three or fewer
centroids. The tactical scale operates close to that floor, so a referee can
reasonably ask whether the reported H1 presence rates measure formation
geometry or merely cluster cardinality.

This step answers that by holding cardinality fixed. For every sampled frame
and every scale, the observed centroids are replaced by k points drawn
uniformly from the convex hull of those same centroids, where k is the
observed count. The null therefore matches the real frame on both the number
of centroids and the spatial envelope they occupy, and destroys only their
arrangement. The adaptive filtration is recomputed on each null cloud by the
same formula used on real data, so nothing else differs.

Excess of observed over null presence is evidence that arrangement carries the
signal. Absence of excess would mean the H1 results are cardinality effects.

Outputs (pipeline/outputs/cardinality_null/):
    per_frame_null.csv        one row per frame per scale
    conditional_presence.csv  P(H1 > 0 | k), observed against null
    summary.json              pooled tests and match-level bootstrap
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "01_data"))
sys.path.insert(0, str(REPO / "02_tda_core"))

from loaders import skillcorner  # noqa: E402
from tda_utils import (  # noqa: E402
    VALIDATED_CUTOFFS,
    adaptive_filtration,
    compute_persistence,
    cutoff_clustering,
)

# H1 is empty on three or fewer points for any admissible filtration, so the
# null and the observation agree trivially there (Remark rem:teamnull).
MIN_POINTS_FOR_H1 = 4
SCALES = ("individual", "tactical")


def sample_in_hull(points: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """Draw k points uniformly from the convex hull of `points`.

    Falls back to the bounding segment or box when the hull is degenerate,
    which only happens for near-collinear centroid sets. Those frames cannot
    carry H1 under either the observation or the null, so the fallback never
    affects a comparison that matters.
    """
    from scipy.spatial import Delaunay, QhullError

    try:
        tri = Delaunay(points)
    except (QhullError, ValueError):
        lo, hi = points.min(axis=0), points.max(axis=0)
        return rng.uniform(lo, hi, size=(k, 2))

    simplices = points[tri.simplices]
    # Triangle areas, so that sampling is uniform over the hull rather than
    # uniform over the triangles.
    a = simplices[:, 1] - simplices[:, 0]
    b = simplices[:, 2] - simplices[:, 0]
    areas = np.abs(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]) / 2.0
    total = areas.sum()
    if not np.isfinite(total) or total <= 0:
        lo, hi = points.min(axis=0), points.max(axis=0)
        return rng.uniform(lo, hi, size=(k, 2))

    idx = rng.choice(len(simplices), size=k, p=areas / total)
    r1 = rng.random((k, 1))
    r2 = rng.random((k, 1))
    # Reflect into the lower triangle to get uniform barycentric weights.
    flip = (r1 + r2) > 1.0
    r1[flip] = 1.0 - r1[flip]
    r2[flip] = 1.0 - r2[flip]
    tri_pts = simplices[idx]
    return tri_pts[:, 0] + r1 * (tri_pts[:, 1] - tri_pts[:, 0]) + r2 * (
        tri_pts[:, 2] - tri_pts[:, 0]
    )


def h1_present(cloud: np.ndarray, cutoff: float, percentile: int) -> bool:
    """Apply the pipeline's adaptive filtration and report H1 presence."""
    max_filt = adaptive_filtration(cloud, cutoff, percentile=percentile)
    return compute_persistence(cloud, max_filt).h1_count > 0


def analyse_frame(
    positions: np.ndarray,
    cutoff: float,
    n_null: int,
    percentile: int,
    rng: np.random.Generator,
) -> tuple[int, int, float]:
    """Return (k, observed presence, null presence rate) for one frame."""
    centroids, _ = cutoff_clustering(positions, cutoff)
    k = len(centroids)
    if k < MIN_POINTS_FOR_H1:
        return k, 0, 0.0

    observed = int(h1_present(centroids, cutoff, percentile))
    hits = sum(
        h1_present(sample_in_hull(centroids, k, rng), cutoff, percentile)
        for _ in range(n_null)
    )
    return k, observed, hits / n_null


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-null", type=int, default=200, help="null replicates per frame")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--percentile", type=int, default=75)
    ap.add_argument("--primary-only", action="store_true", help="smoke test on one match")
    args = ap.parse_args()

    ensure_dirs()
    cfg = load_config()
    out_dir = OUTPUT_DIR / "cardinality_null"
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    mm = cfg["multi_match"]
    match_ids = [m["id"] for m in skillcorner.list_matches()]
    if args.primary_only:
        match_ids = [cfg["primary_match_id"]]

    rows = []
    for n, mid in enumerate(match_ids, 1):
        match = skillcorner.load_match(
            mid,
            sample_every=mm["sample_every"],
            require_complete=True,
            max_frames=mm["frames_per_match"],
        )
        frames = match.complete_frames
        print(f"[{n}/{len(match_ids)}] match {mid}: {len(frames)} frames", flush=True)
        for fi, frame in enumerate(frames):
            for scale in SCALES:
                k, observed, null_rate = analyse_frame(
                    frame.all_positions,
                    VALIDATED_CUTOFFS[scale],
                    args.n_null,
                    args.percentile,
                    rng,
                )
                rows.append(
                    {
                        "match_id": mid,
                        "frame_idx": fi,
                        "scale": scale,
                        "k": k,
                        "h1_observed": observed,
                        "null_presence_rate": null_rate,
                    }
                )

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "per_frame_null.csv", index=False)

    cond = (
        df.groupby(["scale", "k"])
        .agg(
            n_frames=("h1_observed", "size"),
            observed_presence=("h1_observed", "mean"),
            null_presence=("null_presence_rate", "mean"),
        )
        .reset_index()
    )
    cond["excess"] = cond["observed_presence"] - cond["null_presence"]
    cond.to_csv(out_dir / "conditional_presence.csv", index=False)

    summary = {
        "n_null_per_frame": args.n_null,
        "seed": args.seed,
        "null_model": "uniform on the convex hull of the observed centroids, k fixed",
        "n_matches": int(df["match_id"].nunique()),
        "n_frames": int(df.groupby("scale").size().max()),
        "scales": {},
    }

    for scale in SCALES:
        sub = df[df["scale"] == scale]
        observed_count = int(sub["h1_observed"].sum())
        expected = float(sub["null_presence_rate"].sum())
        # Poisson-binomial normal approximation. Frames within a match are not
        # independent, so this is reported alongside a match-level bootstrap
        # rather than on its own.
        var = float((sub["null_presence_rate"] * (1 - sub["null_presence_rate"])).sum())
        z = (observed_count - expected) / np.sqrt(var) if var > 0 else float("nan")

        matches = sub["match_id"].unique()
        diffs = []
        for _ in range(1000):
            pick = rng.choice(matches, size=len(matches), replace=True)
            block = pd.concat([sub[sub["match_id"] == m] for m in pick])
            diffs.append(
                float(block["h1_observed"].mean() - block["null_presence_rate"].mean())
            )
        diffs = np.asarray(diffs)

        summary["scales"][scale] = {
            "observed_presence": float(sub["h1_observed"].mean()),
            "null_presence": float(sub["null_presence_rate"].mean()),
            "excess": float(sub["h1_observed"].mean() - sub["null_presence_rate"].mean()),
            "observed_frames_with_h1": observed_count,
            "expected_frames_with_h1": expected,
            "z_poisson_binomial": float(z),
            "match_bootstrap_mean": float(diffs.mean()),
            "match_bootstrap_ci": [
                float(np.percentile(diffs, 2.5)),
                float(np.percentile(diffs, 97.5)),
            ],
        }

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary["scales"], indent=2))
    print(f"\nWrote {out_dir}")


if __name__ == "__main__":
    main()
