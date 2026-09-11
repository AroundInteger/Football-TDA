#!/usr/bin/env python3
"""Step 02: SkillCorner-only cardinality-inversion cutoff sweep.

Implements pipeline/CUTOFF_PROTOCOL.md. Does not call the old four-epoch
30% midpoint sweep. Does not import SecondSpectrum.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.metrics import calinski_harabasz_score, silhouette_score

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import (  # noqa: E402
    OUTPUT_DIR,
    PIPELINE_DIR as _PIPELINE_DIR,
    analysis_root,
    ensure_dirs,
    load_config,
)
from cutoff_protocol import (  # noqa: E402
    ACCEPTANCE_BANDS,
    PRIMARY_MATCH_ID,
    REQUIRED_MATCH_IDS,
    SELECTION_RULES,
    acceptance_ok,
    delta_grid,
    invert_cutoffs,
    mean_h0_at,
    silhouette_local_maxima,
)

GRID = delta_grid()


def opendata_root() -> Path:
    root = analysis_root() / "01_data" / "opendata" / "data"
    if not (root / "matches.json").is_file():
        raise FileNotFoundError(
            f"SkillCorner match index not found at {root / 'matches.json'}"
        )
    return root


def load_skillcorner():
    root = analysis_root()
    sys.path.insert(0, str(root / "01_data"))
    from loaders import skillcorner  # noqa: WPS433

    return skillcorner


def require_table_s1_matches(available_ids: set[int]) -> None:
    missing = [i for i in REQUIRED_MATCH_IDS if i not in available_ids]
    if missing:
        raise FileNotFoundError(
            f"Table S1 matches missing from matches.json: {missing}"
        )


def cluster_counts(positions: np.ndarray) -> np.ndarray:
    """Single-linkage cluster count at every grid delta. Shape (n_delta,).

    For single linkage the cophenetic merge distances in ``Z[:, 2]`` are
    monotone, so ``k(δ) = n - #merges with distance ≤ δ``.
    """
    n = len(positions)
    if n <= 1:
        return np.ones(len(GRID), dtype=np.uint8)
    Z = linkage(pdist(positions), method="single")
    n_merges = np.searchsorted(Z[:, 2], GRID, side="right")
    return (n - n_merges).astype(np.uint8)


def info_content(labels: np.ndarray) -> float:
    _u, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs + 1e-12)))


def sweep_match(
    match_id: int,
    *,
    sample_every: int,
    skillcorner,
    data_root: Path,
) -> tuple[np.ndarray, list[int]]:
    """Return (n_frames, n_delta) cluster-count matrix and frame indices."""
    match = skillcorner.load_match(
        match_id,
        opendata_path=data_root,
        sample_every=sample_every,
        require_complete=True,
    )
    frames = match.complete_frames
    if not frames:
        raise RuntimeError(f"No complete frames for match {match_id}")
    k_mat = np.empty((len(frames), len(GRID)), dtype=np.uint8)
    frame_ids = []
    for i, frame in enumerate(frames):
        k_mat[i] = cluster_counts(frame.all_positions)
        frame_ids.append(int(frame.frame_id))
        if (i + 1) % 2000 == 0:
            print(f"    {match_id}: {i + 1}/{len(frames)} frames", flush=True)
    print(f"    {match_id}: {len(frames)} complete frames (sample_every={sample_every})")
    return k_mat, frame_ids


def aggregate_from_blocks(
    blocks: dict[int, np.ndarray],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pooled and per-match mean H0 tables."""
    pooled_rows = []
    per_match_rows = []
    all_k = np.vstack(list(blocks.values()))
    n_all = all_k.shape[0]
    for j, d in enumerate(GRID):
        col = all_k[:, j].astype(np.float64)
        pooled_rows.append(
            {
                "delta": float(d),
                "mean_h0": float(col.mean()),
                "std_h0": float(col.std(ddof=1)) if n_all > 1 else 0.0,
                "p_k_ge_4": float((col >= 4).mean()),
                "n_frames": int(n_all),
            }
        )
    pooled = pd.DataFrame(pooled_rows)

    for mid, k_mat in blocks.items():
        n = k_mat.shape[0]
        for j, d in enumerate(GRID):
            col = k_mat[:, j].astype(np.float64)
            per_match_rows.append(
                {
                    "match_id": int(mid),
                    "delta": float(d),
                    "mean_h0": float(col.mean()),
                    "std_h0": float(col.std(ddof=1)) if n > 1 else 0.0,
                    "p_k_ge_4": float((col >= 4).mean()),
                    "n_frames": int(n),
                }
            )
    return pooled, pd.DataFrame(per_match_rows)


def regime_rows(
    pooled: pd.DataFrame,
    per_match: pd.DataFrame,
    adopted: dict[str, float],
) -> pd.DataFrame:
    rows = []
    per_match_stars = {level: [] for level in adopted}
    for mid, g in per_match.groupby("match_id"):
        stars = invert_cutoffs(g)
        for level, val in stars.items():
            per_match_stars[level].append(val)
            m_h0 = mean_h0_at(
                g["delta"].to_numpy(), g["mean_h0"].to_numpy(), adopted[level]
            )
            rows.append(
                {
                    "scale": level,
                    "match_id": int(mid),
                    "adopted_cutoff_m": adopted[level],
                    "match_inverted_cutoff_m": val,
                    "mean_h0_at_adopted": m_h0,
                    "acceptance_ok": acceptance_ok(m_h0, level),
                    "selection_rule": SELECTION_RULES[level],
                    "acceptance_lo": ACCEPTANCE_BANDS[level][0],
                    "acceptance_hi": ACCEPTANCE_BANDS[level][1],
                    "n_frames": int(g["n_frames"].iloc[0]),
                }
            )

    summary_rows = []
    for level, cutoff in adopted.items():
        m_h0 = mean_h0_at(
            pooled["delta"].to_numpy(), pooled["mean_h0"].to_numpy(), cutoff
        )
        stars = np.array(per_match_stars[level], dtype=float)
        acc = [
            r["acceptance_ok"]
            for r in rows
            if r["scale"] == level
        ]
        summary_rows.append(
            {
                "scale": level,
                "adopted_cutoff_m": cutoff,
                "selection_rule": SELECTION_RULES[level],
                "pooled_mean_h0": m_h0,
                "acceptance_lo": ACCEPTANCE_BANDS[level][0],
                "acceptance_hi": ACCEPTANCE_BANDS[level][1],
                "acceptance_all_ok": all(acc),
                "n_matches_failing_acceptance": int(sum(not x for x in acc)),
                "per_match_delta_mean": float(stars.mean()),
                "per_match_delta_std": float(stars.std(ddof=1)) if len(stars) > 1 else 0.0,
                "n_matches": int(len(stars)),
                "n_frames_pooled": int(pooled["n_frames"].iloc[0]),
            }
        )
    return pd.DataFrame(summary_rows), pd.DataFrame(rows)


def write_config_cutoffs(adopted: dict[str, float]) -> None:
    path = _PIPELINE_DIR / "config.yaml"
    text = path.read_text()
    block = (
        "validated_cutoffs:\n"
        f"  individual: {adopted['individual']}\n"
        f"  tactical: {adopted['tactical']}\n"
        f"  team: {adopted['team']}\n"
    )
    new, n = re.subn(
        r"validated_cutoffs:\n(?:  \w+: [0-9.]+\n){3}",
        block,
        text,
        count=1,
    )
    if n != 1:
        raise RuntimeError("Could not update validated_cutoffs in config.yaml")
    path.write_text(new)


def _scores_for_frame(pos: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """CH, silhouette, and entropy at every grid delta, reusing partitions."""
    n = len(pos)
    ch = np.full(len(GRID), np.nan)
    sil = np.full(len(GRID), np.nan)
    ic = np.full(len(GRID), np.nan)
    if n < 3:
        return ch, sil, ic
    Z = linkage(pdist(pos), method="single")
    n_merges = np.searchsorted(Z[:, 2], GRID, side="right")
    # Evaluate metrics only when the partition changes (at most n-1 times).
    last_merges = -1
    cached = (np.nan, np.nan, np.nan)
    for i, nm in enumerate(n_merges):
        if nm != last_merges:
            labels = fcluster(Z, float(GRID[i]), criterion="distance")
            k = int(np.unique(labels).size)
            ic_val = info_content(labels)
            ch_val = np.nan
            sil_val = np.nan
            if 1 < k < n:
                try:
                    ch_val = float(calinski_harabasz_score(pos, labels))
                except ValueError:
                    ch_val = np.nan
                try:
                    sil_val = float(silhouette_score(pos, labels))
                except ValueError:
                    sil_val = np.nan
            cached = (ch_val, sil_val, ic_val)
            last_merges = nm
        ch[i], sil[i], ic[i] = cached
    return ch, sil, ic


def diagnostic_metrics(
    match_ids: tuple[int, ...],
    *,
    skillcorner,
    data_root: Path,
) -> pd.DataFrame:
    """1 Hz quality metrics. Silhouette omitted when k is 1 or n."""
    records = []
    for mid in match_ids:
        match = skillcorner.load_match(
            mid,
            opendata_path=data_root,
            sample_every=10,
            require_complete=True,
        )
        n_frames = len(match.complete_frames)
        print(f"  diagnostics {mid}: {n_frames} frames at 1 Hz", flush=True)
        for fi, frame in enumerate(match.complete_frames):
            pos = frame.all_positions
            ch, sil, ic = _scores_for_frame(pos)
            for j, d in enumerate(GRID):
                records.append(
                    {
                        "match_id": int(mid),
                        "delta": float(d),
                        "ch_score": ch[j],
                        "sil_score": sil[j],
                        "info_content": ic[j],
                    }
                )
            if (fi + 1) % 500 == 0:
                print(f"    {mid}: {fi + 1}/{n_frames}", flush=True)
    raw = pd.DataFrame(records)
    agg = (
        raw.groupby("delta", as_index=False)
        .agg(
            mean_ch=("ch_score", "mean"),
            mean_sil=("sil_score", "mean"),
            mean_ic=("info_content", "mean"),
            n=("ch_score", "size"),
        )
    )
    return agg


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--smoke",
        action="store_true",
        help="Primary match only, every 10th complete frame. Do not freeze cutoffs.",
    )
    p.add_argument(
        "--skip-diagnostics",
        action="store_true",
        help="Skip the 1 Hz CH/silhouette/IC pass.",
    )
    p.add_argument(
        "--diagnostics-only",
        action="store_true",
        help="Write 1 Hz quality metrics only. Do not re-invert or touch config.yaml.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ensure_dirs()
    skillcorner = load_skillcorner()
    data_root = opendata_root()
    listed = {int(m["id"]) for m in skillcorner.list_matches(data_root)}
    require_table_s1_matches(listed)

    if args.diagnostics_only:
        match_ids = (PRIMARY_MATCH_ID,) if args.smoke else REQUIRED_MATCH_IDS
        print(f"DIAGNOSTICS ONLY: {len(match_ids)} matches at 1 Hz")
        metrics = diagnostic_metrics(
            match_ids, skillcorner=skillcorner, data_root=data_root
        )
        metrics.to_csv(OUTPUT_DIR / "cutoff_sweep_metrics.csv", index=False)
        peaks = silhouette_local_maxima(
            metrics["delta"].to_numpy(), metrics["mean_sil"].to_numpy()
        )
        (OUTPUT_DIR / "silhouette_local_maxima.json").write_text(
            json.dumps({"deltas_m": peaks}, indent=2)
        )
        print(f"Silhouette local maxima (m): {peaks}")
        print(f"Wrote {OUTPUT_DIR / 'cutoff_sweep_metrics.csv'}")
        return

    if args.smoke:
        match_ids = (PRIMARY_MATCH_ID,)
        sample_every = 10
        print("SMOKE: primary match, sample_every=10 (1 Hz)")
    else:
        match_ids = REQUIRED_MATCH_IDS
        sample_every = 1
        print(f"FULL: {len(match_ids)} matches, every complete frame")

    blocks: dict[int, np.ndarray] = {}
    frame_index: dict[int, list[int]] = {}
    for mid in match_ids:
        print(f"Sweeping match {mid}...", flush=True)
        k_mat, fids = sweep_match(
            mid,
            sample_every=sample_every,
            skillcorner=skillcorner,
            data_root=data_root,
        )
        blocks[mid] = k_mat
        frame_index[mid] = fids

    pooled, per_match = aggregate_from_blocks(blocks)
    adopted = invert_cutoffs(pooled)
    summary, match_detail = regime_rows(pooled, per_match, adopted)

    out = OUTPUT_DIR
    if args.smoke:
        out = OUTPUT_DIR / "cutoff_sweep_smoke"
        out.mkdir(parents=True, exist_ok=True)

    pooled.to_csv(out / "cutoff_sweep_agg.csv", index=False)
    per_match.to_csv(out / "cutoff_sweep_per_match.csv", index=False)
    summary.to_csv(out / "regime_summary.csv", index=False)
    match_detail.to_csv(out / "regime_per_match.csv", index=False)

    np.savez_compressed(
        out / "cutoff_sweep_h0.npz",
        deltas=GRID,
        match_ids=np.array(list(blocks.keys()), dtype=np.int64),
        **{f"k_{mid}": mat for mid, mat in blocks.items()},
        **{f"frames_{mid}": np.array(fids, dtype=np.int64) for mid, fids in frame_index.items()},
    )

    if not args.skip_diagnostics:
        metrics = diagnostic_metrics(
            match_ids, skillcorner=skillcorner, data_root=data_root
        )
        metrics.to_csv(out / "cutoff_sweep_metrics.csv", index=False)
        peaks = silhouette_local_maxima(
            metrics["delta"].to_numpy(), metrics["mean_sil"].to_numpy()
        )
        (out / "silhouette_local_maxima.json").write_text(
            json.dumps({"deltas_m": peaks}, indent=2)
        )
        print(f"Silhouette local maxima (m): {peaks}")

    payload = {
        "smoke": bool(args.smoke),
        "sample_every": sample_every,
        "match_ids": list(match_ids),
        "n_frames": {str(k): int(v.shape[0]) for k, v in blocks.items()},
        "adopted_cutoffs": adopted,
        "preview_note": "compare smoke to ~2.9 / ~12 / ~22 m on the old 38-snapshot curve",
    }
    (out / "cutoff_sweep_summary.json").write_text(json.dumps(payload, indent=2))

    print(summary.to_string(index=False))
    print("Adopted cutoffs:", adopted)

    if not args.smoke:
        write_config_cutoffs(adopted)
        print(f"Wrote validated_cutoffs to {_PIPELINE_DIR / 'config.yaml'}")


if __name__ == "__main__":
    main()
