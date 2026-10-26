#!/usr/bin/env python3
"""Definition checks for Paper A.

1. Wilcoxon signed-rank tests on the stored event Δ values.
2. Team-level group-count histogram at δ = 23.0 m on every complete frame,
   and H1 representatives only on frames with k ≥ 4.
3. Reduction cycles for the 403 primary-match finite H1 bars, checked
   against the stored Ripser birth–death pairs.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from scipy.stats import wilcoxon

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import OUTPUT_DIR, analysis_root, ensure_dirs  # noqa: E402
from cutoff_protocol import PRIMARY_MATCH_ID, REQUIRED_MATCH_IDS  # noqa: E402

sys.path.insert(0, str(analysis_root() / "02_tda_core"))
from tda_utils import (  # noqa: E402
    VALIDATED_CUTOFFS,
    cutoff_clustering,
    rips_h1_representatives,
)

TEAM_DELTA = 23.0
MATCH_TOL = 1e-3
BIRTH_TOL = 1e-6


def _pct(n: int, total: int) -> float:
    return 100.0 * n / total if total else float("nan")


def wilcoxon_from_stored() -> dict:
    """One-sample signed-rank test of each event class against zero.

    ``zero_method='wilcox'`` drops exact zeros before ranking.
    ``method='auto'`` selects SciPy's asymptotic approximation when the
    ranked sample is too large for an exact null.
    """
    path = OUTPUT_DIR / "event_correlation" / "event_topology_correlation.csv"
    df = pd.read_csv(path)
    out = {
        "scipy_version": scipy.__version__,
        "zero_method": "wilcox",
        "method": "auto",
        "alternative": "two-sided",
        "source": str(path.name),
        "scales": {},
    }
    for scale, g in df.groupby("scale"):
        classes = {}
        for etype, edf in g.groupby("event_type"):
            deltas = edf["persistence_delta"].to_numpy(dtype=float)
            n_zero = int(np.sum(deltas == 0))
            stat, p_val = wilcoxon(
                deltas,
                alternative="two-sided",
                zero_method="wilcox",
                method="auto",
            )
            classes[str(etype)] = {
                "n_events": int(len(deltas)),
                "n_zero_delta": n_zero,
                "n_ranked": int(len(deltas) - n_zero),
                "mean_delta": float(np.mean(deltas)),
                "wilcoxon_stat": float(stat),
                "p_value": float(p_val),
            }
        out["scales"][str(scale)] = classes
    dest = OUTPUT_DIR / "event_correlation" / "wilcoxon_summary.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"Wrote {dest}")
    return out


def _k_and_linkage(positions: np.ndarray, delta: float):
    n = len(positions)
    condensed = pdist(positions)
    merged = linkage(condensed, method="single")
    n_merges = int(np.searchsorted(merged[:, 2], delta, side="right"))
    return n - n_merges, merged


def team_tail(primary_positions: list[np.ndarray] | None = None) -> tuple[dict, list[np.ndarray]]:
    """Histogram of k at 23.0 m, and H1 on the k ≥ 4 frames."""
    root = analysis_root()
    sys.path.insert(0, str(root / "01_data"))
    from loaders import skillcorner  # noqa: WPS433

    data_root = root / "01_data" / "opendata" / "data"
    counts = np.zeros(23, dtype=np.int64)
    ge4_rows = []
    n_frames = 0
    n_k_disagree = 0
    kept_primary: list[np.ndarray] = [] if primary_positions is None else primary_positions

    for match_id in REQUIRED_MATCH_IDS:
        match = skillcorner.load_match(
            match_id,
            opendata_path=data_root,
            sample_every=1,
            require_complete=True,
        )
        frames = match.complete_frames
        print(f"  {match_id}: {len(frames)} complete frames", flush=True)
        if match_id == PRIMARY_MATCH_ID and primary_positions is None:
            kept_primary = [np.asarray(fr.all_positions, dtype=float) for fr in frames]
        for fr in frames:
            pos = np.asarray(fr.all_positions, dtype=float)
            k, merged = _k_and_linkage(pos, TEAM_DELTA)
            counts[k] += 1
            n_frames += 1
            if k < 4:
                continue
            labels = fcluster(merged, TEAM_DELTA, criterion="distance")
            unique = np.unique(labels)
            if len(unique) != k:
                n_k_disagree += 1
            cents = np.array([pos[labels == lab].mean(axis=0) for lab in unique])
            reps = rips_h1_representatives(cents)
            ge4_rows.append({
                "match_id": int(match_id),
                "frame_id": int(fr.frame_id),
                "k": int(k),
                "n_bars": len(reps),
                "max_persistence_m": float(max((r.persistence for r in reps), default=0.0)),
                "all_present_at_birth": all(r.present_at_birth(BIRTH_TOL) for r in reps),
                "all_longest_is_birth": all(r.longest_is_birth(BIRTH_TOL) for r in reps),
                "all_at_least_four_vertices": all(r.n_vertices >= 4 for r in reps),
            })
            if n_frames % 20000 == 0:
                print(f"    {n_frames} frames, k≥4 so far {len(ge4_rows)}", flush=True)

    k_ge4 = int(counts[4:].sum())
    k3 = int(counts[3])
    k_le2 = int(counts[1] + counts[2])
    n_with_h1 = sum(1 for row in ge4_rows if row["n_bars"] > 0)
    n_bars = sum(row["n_bars"] for row in ge4_rows)
    summary = {
        "delta_m": TEAM_DELTA,
        "n_frames": int(n_frames),
        "n_k_disagree": int(n_k_disagree),
        "counts": {str(k): int(counts[k]) for k in range(1, 23) if counts[k]},
        "k_le_2": k_le2,
        "k_eq_3": k3,
        "k_ge_4": k_ge4,
        "pct_k_le_2": _pct(k_le2, n_frames),
        "pct_k_eq_3": _pct(k3, n_frames),
        "pct_k_ge_4": _pct(k_ge4, n_frames),
        "k_ge_4_frames_with_h1": int(n_with_h1),
        "k_ge_4_h1_bars": int(n_bars),
        "k_ge_4_representatives_ok": all(
            row["all_present_at_birth"]
            and row["all_longest_is_birth"]
            and row["all_at_least_four_vertices"]
            for row in ge4_rows
        ),
    }
    payload = {"summary": summary, "k_ge_4_frames": ge4_rows}
    dest = OUTPUT_DIR / "team_k_histogram.json"
    dest.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {dest}")
    print(
        f"  k≤2 {summary['pct_k_le_2']:.4f}%  "
        f"k=3 {summary['pct_k_eq_3']:.4f}%  "
        f"k≥4 {summary['pct_k_ge_4']:.4f}%  "
        f"H1 frames {n_with_h1} bars {n_bars}"
    )
    return summary, kept_primary


def _match_bars(stored: np.ndarray, reps) -> tuple[list, int, float]:
    """Greedy match of stored (birth, death) rows to reduction cycles."""
    unused = set(range(len(reps)))
    matched = []
    unmatched = 0
    max_resid = 0.0
    for birth, death in stored:
        best = None
        best_resid = None
        for idx in unused:
            resid = abs(reps[idx].birth - birth) + abs(reps[idx].death - death)
            if best_resid is None or resid < best_resid:
                best, best_resid = idx, resid
        if best is None or best_resid > MATCH_TOL:
            unmatched += 1
            continue
        unused.remove(best)
        max_resid = max(max_resid, best_resid)
        matched.append(reps[best])
    return matched, unmatched, max_resid


def primary_representatives(positions: list[np.ndarray]) -> dict:
    """Audit reduction cycles on the primary-match uniform sample."""
    n_sample = 150
    step = max(1, len(positions) // n_sample)
    sample = positions[::step][:n_sample]
    stored = pd.read_csv(OUTPUT_DIR / "h1_bars_primary.csv")
    vertex_counts = []
    n_bars = 0
    n_simple = 0
    n_present = 0
    n_longest = 0
    n_ge4 = 0
    n_unmatched = 0
    max_resid = 0.0
    by_level = {}

    for level, cutoff in (
        ("individual", VALIDATED_CUTOFFS["individual"]),
        ("tactical", VALIDATED_CUTOFFS["tactical"]),
    ):
        level_unmatched = 0
        level_resid = 0.0
        level_n = 0
        for sample_idx, pos in enumerate(sample):
            cents, _labels = cutoff_clustering(pos, cutoff)
            reps = rips_h1_representatives(cents)
            rows = stored[
                (stored["level"] == level) & (stored["sample_idx"] == sample_idx)
            ]
            pairs = rows[["birth", "death"]].to_numpy(dtype=float)
            matched, unmatched, resid = _match_bars(pairs, reps)
            level_unmatched += unmatched
            level_resid = max(level_resid, resid)
            level_n += len(matched)
            for rep in matched:
                n_bars += 1
                vertex_counts.append(rep.n_vertices)
                n_simple += int(rep.is_simple_cycle)
                n_present += int(rep.present_at_birth(BIRTH_TOL))
                n_longest += int(rep.longest_is_birth(BIRTH_TOL))
                n_ge4 += int(rep.n_vertices >= 4)
        by_level[level] = {
            "n_matched": level_n,
            "n_unmatched": level_unmatched,
            "max_birth_death_residual_m": level_resid,
        }
        n_unmatched += level_unmatched
        max_resid = max(max_resid, level_resid)
        print(f"  {level}: matched {level_n}, unmatched {level_unmatched}", flush=True)

    hist = dict(sorted(Counter(vertex_counts).items()))
    summary = {
        "n_sample_frames": len(sample),
        "stride": step,
        "n_stored_bars": int(len(stored)),
        "n_matched_bars": n_bars,
        "n_unmatched_bars": n_unmatched,
        "max_birth_death_residual_m": max_resid,
        "n_present_at_birth": n_present,
        "n_longest_edge_is_birth": n_longest,
        "n_at_least_four_vertices": n_ge4,
        "n_simple_cycles": n_simple,
        "vertex_count_histogram": {str(k): int(v) for k, v in hist.items()},
        "vertex_count_min": int(min(vertex_counts)) if vertex_counts else None,
        "vertex_count_max": int(max(vertex_counts)) if vertex_counts else None,
        "by_level": by_level,
        "birth_tolerance_m": BIRTH_TOL,
        "match_tolerance_m": MATCH_TOL,
    }
    dest = OUTPUT_DIR / "h1_representatives_summary.json"
    dest.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {dest}")
    return summary


def sample_k_from_results() -> dict:
    """Group-count split already stored for the 1,500-frame sample."""
    path = OUTPUT_DIR / "multi_match" / "per_frame_results.csv"
    df = pd.read_csv(path)
    team = df[df["scale"] == "team"]
    k = team["cluster_count"].to_numpy(dtype=int)
    n = len(k)
    out = {
        "n_frames": n,
        "k_le_2": int(np.sum(k <= 2)),
        "k_eq_3": int(np.sum(k == 3)),
        "k_ge_4": int(np.sum(k >= 4)),
        "h1_bars": int(team["h1"].sum()),
    }
    return out


def main() -> None:
    ensure_dirs()
    print("Wilcoxon", flush=True)
    wilcoxon_from_stored()
    print("Sample k (1,500 frames)", flush=True)
    sample = sample_k_from_results()
    print(sample)
    (OUTPUT_DIR / "team_k_sample1500.json").write_text(json.dumps(sample, indent=2))
    print("Team tail and primary positions", flush=True)
    _summary, primary = team_tail()
    print(f"Primary complete frames kept: {len(primary)}", flush=True)
    print("Primary representatives", flush=True)
    primary_representatives(primary)


if __name__ == "__main__":
    main()
