#!/usr/bin/env python3
"""
C2 collaborator check: compare H1 at adaptive ε_max vs VR to centroid diameter.

Samples: primary match uniform_150 (150 frames) and ten-match SkillCorner
uniform_150 (1,500 frame-scale observations). Scales: individual and tactical
(where H1 loops appear).

Writes pipeline/outputs/epsmax_diameter_check.json for the harness log.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import pdist

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, analysis_root, ensure_dirs, load_config  # noqa: E402

REPO = analysis_root()
OPENDATA = REPO / "01_data" / "opendata" / "data"
sys.path.insert(0, str(REPO / "01_data"))
sys.path.insert(0, str(REPO / "02_tda_core"))
sys.path.insert(0, str(REPO / "03_football_analysis"))

from loaders import skillcorner, subsample_uniform  # noqa: E402
from tda_utils import (  # noqa: E402
    VALIDATED_CUTOFFS,
    adaptive_filtration,
    compute_h1_at_scale,
    compute_persistence,
    cutoff_clustering,
)

H1_SCALES = ("individual", "tactical")


def _diameter(centroids: np.ndarray) -> float:
    if centroids is None or len(centroids) <= 1:
        return 0.0
    d = pdist(centroids)
    return float(np.max(d)) if len(d) else 0.0


def _finite_h1_pairs(h1_diagram: np.ndarray) -> list[tuple[float, float]]:
    if h1_diagram is None or len(h1_diagram) == 0:
        return []
    out = []
    for birth, death in h1_diagram:
        if np.isfinite(death) and np.isfinite(birth):
            out.append((float(birth), float(death)))
    return out


def _extra_bars(adaptive_pairs, diameter_pairs, tol=1e-4):
    """Bars present at diameter filtration but not at adaptive (approximate)."""
    extra = []
    for b, d in diameter_pairs:
        matched = any(
            abs(b - ba) < tol and abs(d - da) < tol for ba, da in adaptive_pairs
        )
        if not matched:
            extra.append((b, d))
    return extra


def analyse_positions(positions: np.ndarray, cutoff: float) -> dict:
    centroids, _ = cutoff_clustering(positions, cutoff, method="single")
    eps_adaptive = adaptive_filtration(centroids, cutoff, percentile=75)
    diam = _diameter(centroids)
    eps_diam = diam + 1e-6 if diam > 0 else eps_adaptive

    res_ad = compute_persistence(centroids, eps_adaptive)
    res_di = compute_persistence(centroids, eps_diam)

    ad_pairs = _finite_h1_pairs(res_ad.h1_diagram)
    di_pairs = _finite_h1_pairs(res_di.h1_diagram)
    extra = _extra_bars(ad_pairs, di_pairs)

    return {
        "n_centroids": int(len(centroids)),
        "eps_adaptive": float(eps_adaptive),
        "eps_diameter": float(eps_diam),
        "h1_finite_adaptive": len(ad_pairs),
        "h1_finite_diameter": len(di_pairs),
        "extra_at_diameter": extra,
    }


def iter_primary_frames(n_frames: int):
    cfg = load_config()
    mid = int(cfg["primary_match_id"])
    match = skillcorner.load_match(
        mid, opendata_path=OPENDATA, sample_every=1, require_complete=True
    )
    sampled, _ = subsample_uniform(match.complete_frames, n_frames)
    for fi, frame in enumerate(sampled):
        yield f"primary_{mid}", fi, frame.all_positions


def iter_multi_match_frames(n_per_match: int):
    for meta in skillcorner.list_matches(opendata_path=OPENDATA):
        mid = int(meta["id"])
        try:
            match = skillcorner.load_match(
                mid,
                opendata_path=OPENDATA,
                sample_every=1,
                require_complete=True,
            )
        except FileNotFoundError:
            continue
        sampled, _ = subsample_uniform(match.complete_frames, n_per_match)
        for fi, frame in enumerate(sampled):
            yield str(mid), fi, frame.all_positions


def run_sample(label: str, frame_iter, max_frames: int | None = None) -> dict:
    summary = {
        "label": label,
        "frames_checked": 0,
        "frames_with_extra_h1": 0,
        "max_extra_bars_in_frame": 0,
        "examples": [],
    }
    for _match, fi, positions in frame_iter:
        if max_frames is not None and summary["frames_checked"] >= max_frames:
            break
        frame_extra = 0
        for scale in H1_SCALES:
            cutoff = VALIDATED_CUTOFFS[scale]
            row = analyse_positions(positions, cutoff)
            n_extra = len(row["extra_at_diameter"])
            frame_extra = max(frame_extra, n_extra)
            if n_extra and len(summary["examples"]) < 5:
                summary["examples"].append(
                    {
                        "match": _match,
                        "frame": fi,
                        "scale": scale,
                        **row,
                    }
                )
        if frame_extra:
            summary["frames_with_extra_h1"] += 1
            summary["max_extra_bars_in_frame"] = max(
                summary["max_extra_bars_in_frame"], frame_extra
            )
        summary["frames_checked"] += 1
    return summary


def main() -> None:
    os.chdir(REPO)
    ensure_dirs()
    cfg = load_config()
    n150 = int(cfg["sampling"]["uniform_150"]["n_frames"])

    primary = run_sample("uniform_150_primary", iter_primary_frames(n150))
    multi = run_sample(
        "uniform_150_ten_match",
        iter_multi_match_frames(n150),
    )

    any_extra = (
        primary["frames_with_extra_h1"] > 0 or multi["frames_with_extra_h1"] > 0
    )
    decision = (
        "keep_epsmax_with_modelling_reason"
        if any_extra
        else "drop_adaptive_epsmax"
    )

    out = {
        "decision": decision,
        "any_extra_finite_h1_at_diameter": any_extra,
        "primary_match": primary,
        "ten_match_aggregate": multi,
        "interpretation": (
            "No additional finite H1 bar appears when extending filtration "
            "from adaptive eps_max to centroid diameter; collaborator C2 "
            "supports removing adaptive truncation from Paper A."
            if not any_extra
            else "At least one frame/scale shows H1 bars at diameter not "
            "captured at adaptive eps_max; keep an explicit cut with "
            "modelling justification."
        ),
    }

    path = OUTPUT_DIR / "epsmax_diameter_check.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
