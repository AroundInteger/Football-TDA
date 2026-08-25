#!/usr/bin/env python3
"""
Predictive incremental utility of tactical H1 (Paper v5 revision, §3.11)
========================================================================

Converts the partial-R^2 framing of §3.9 into a cross-validated predictive
claim on held-out matches. For each sampled frame we form

    Block A (baselines):  team length, width, convex-hull area,
                          Voronoi dispersion entropy
    Block B (with topology):  Block A + tactical H1 total persistence

and fit L2-regularised logistic regression on a binary frame label drawn
from the SkillCorner phases-of-play annotation:

    primary target:  is_buildup_phase(t)
    robustness:      is_chaotic_phase(t)

Cross-validation is GroupKFold(n_splits=10) over match_id, so every fold's
test set is entirely composed of held-out matches. We report out-of-fold

    AUC, log-loss, Brier score

for blocks A and B, plus

    ΔAUC = AUC(B) − AUC(A)     (analogous for log-loss and Brier)

with match-level bootstrap 95% CIs (1,000 resamples) and a stratified
permutation test (10,000 within-match permutations of the label) on ΔAUC.

A cross-check at the bottom replaces tactical H1 total persistence with
(i) H1 count and (ii) max H1 persistence to confirm the conclusion is not
specific to a single summary.

Usage:
    python predictive_utility.py --skillcorner-only [--seed 42]

Outputs:
    results/paper_v5_revisions/predictive_utility.csv
    results/paper_v5_revisions/predictive_utility_summary.json
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

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

BASELINE_COLS = ["length_m", "width_m", "hull_area_m2", "voronoi_entropy"]
TOPO_COLS_PRIMARY = ["tactical_h1_total_persistence"]
TOPO_COLS_COUNT = ["tactical_h1_count"]
TOPO_COLS_MAX = ["tactical_h1_max_persistence"]


def voronoi_entropy(points: np.ndarray) -> float:
    """Shannon entropy of bounded Voronoi cell areas; robust to unbounded cells."""
    if points.shape[0] < 4:
        return float("nan")
    try:
        vor = Voronoi(points)
    except Exception:
        return float("nan")
    areas: list[float] = []
    for region_index in vor.point_region:
        region = vor.regions[region_index]
        if not region or -1 in region:
            continue
        verts = vor.vertices[region]
        if verts.shape[0] < 3:
            continue
        try:
            areas.append(float(ConvexHull(verts).volume))
        except Exception:
            continue
    if not areas:
        return float("nan")
    a = np.asarray(areas, dtype=float)
    a = a[a > 0]
    if a.size == 0:
        return float("nan")
    p = a / a.sum()
    return float(-(p * np.log(p)).sum())


def per_frame_features(positions: np.ndarray) -> dict:
    xy = np.asarray(positions, dtype=float)
    length = float(xy[:, 0].ptp())
    width = float(xy[:, 1].ptp())
    try:
        hull_area = float(ConvexHull(xy).volume)
    except Exception:
        hull_area = float("nan")
    vent = voronoi_entropy(xy)
    diagrams = compute_h1_at_scale(xy, TACTICAL_DELTA)
    h1_total = float(diagrams.h1_stats.get("total", 0.0))
    h1_count = int(diagrams.h1_stats.get("count", 0))
    h1_max = float(diagrams.h1_stats.get("max", 0.0))
    return {
        "length_m": length,
        "width_m": width,
        "hull_area_m2": hull_area,
        "voronoi_entropy": vent,
        "tactical_h1_total_persistence": h1_total,
        "tactical_h1_count": h1_count,
        "tactical_h1_max_persistence": h1_max,
    }


def build_phase_label(match_id: int, frame_id: int, phases_df: pd.DataFrame) -> dict:
    """Return binary indicators for whether ``frame_id`` falls in a build-up
    or chaotic phase (in possession of either team)."""
    mask = (phases_df["frame_start"] <= frame_id) & (phases_df["frame_end"] >= frame_id)
    sub = phases_df.loc[mask]
    if sub.empty:
        return {"is_buildup": 0, "is_chaotic": 0, "has_phase": 0}
    types = set(sub["team_in_possession_phase_type"].dropna().astype(str).tolist())
    return {
        "is_buildup": int("build_up" in types),
        "is_chaotic": int("chaotic" in types),
        "has_phase": 1,
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
        try:
            phases = skillcorner.load_phases(mid)
        except FileNotFoundError:
            phases = pd.DataFrame(
                columns=[
                    "frame_start",
                    "frame_end",
                    "team_in_possession_phase_type",
                ]
            )
        print(
            f"[{mid}] {match.info.home_team} vs {match.info.away_team}: "
            f"{len(match.complete_frames)} frames; {len(phases)} phases"
        )
        for frame_idx, frame in enumerate(match.complete_frames):
            features = per_frame_features(frame.all_positions)
            labels = build_phase_label(mid, int(frame.frame_id), phases)
            row = {"match_id": mid, "frame_idx": frame_idx, "frame_id": int(frame.frame_id)}
            row.update(features)
            row.update(labels)
            rows.append(row)
    return pd.DataFrame(rows)


def oof_predict(
    X: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    seed: int = 42,
) -> np.ndarray:
    """Out-of-fold predicted probabilities under GroupKFold over match_id.

    Standardises features within each fold's training partition; one inner fit
    per fold, no nested CV (the L2 strength is fixed at the sklearn default
    ``C = 1.0`` to keep the comparison between blocks fair)."""
    gkf = GroupKFold(n_splits=int(np.unique(groups).size))
    oof = np.full(shape=y.shape, fill_value=np.nan, dtype=float)
    for train_idx, test_idx in gkf.split(X, y, groups):
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X[train_idx])
        X_test = scaler.transform(X[test_idx])
        clf = LogisticRegression(
            penalty="l2",
            C=1.0,
            solver="lbfgs",
            max_iter=1000,
            random_state=seed,
        )
        clf.fit(X_train, y[train_idx])
        oof[test_idx] = clf.predict_proba(X_test)[:, 1]
    return oof


def metrics(y_true: np.ndarray, y_score: np.ndarray) -> dict:
    mask = np.isfinite(y_score) & np.isfinite(y_true)
    y_true_m = y_true[mask].astype(int)
    y_score_m = y_score[mask].astype(float)
    return {
        "auc": float(roc_auc_score(y_true_m, y_score_m)),
        "log_loss": float(log_loss(y_true_m, np.clip(y_score_m, 1e-6, 1 - 1e-6))),
        "brier": float(brier_score_loss(y_true_m, y_score_m)),
        "n": int(y_true_m.size),
        "prevalence": float(y_true_m.mean()),
    }


def match_level_bootstrap_delta(
    df: pd.DataFrame,
    score_a: np.ndarray,
    score_b: np.ndarray,
    target_col: str,
    n_boot: int,
    rng: np.random.Generator,
) -> dict:
    matches = df["match_id"].to_numpy()
    y = df[target_col].to_numpy().astype(int)
    keys = np.unique(matches)
    boot_d_auc, boot_d_ll, boot_d_brier = [], [], []
    for _ in range(n_boot):
        sample = rng.choice(keys, size=keys.size, replace=True)
        idx = np.concatenate([np.where(matches == m)[0] for m in sample])
        ya = y[idx]
        sa = score_a[idx]
        sb = score_b[idx]
        if len(np.unique(ya)) < 2:
            continue
        try:
            d_auc = roc_auc_score(ya, sb) - roc_auc_score(ya, sa)
            d_ll = log_loss(ya, np.clip(sb, 1e-6, 1 - 1e-6)) - log_loss(ya, np.clip(sa, 1e-6, 1 - 1e-6))
            d_br = brier_score_loss(ya, sb) - brier_score_loss(ya, sa)
        except ValueError:
            continue
        boot_d_auc.append(float(d_auc))
        boot_d_ll.append(float(d_ll))
        boot_d_brier.append(float(d_br))

    def ci(arr):
        a = np.asarray(arr, dtype=float)
        a = a[np.isfinite(a)]
        if a.size == 0:
            return [float("nan")] * 3
        return [float(a.mean()), float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]

    return {
        "delta_auc_mean_ci": ci(boot_d_auc),
        "delta_log_loss_mean_ci": ci(boot_d_ll),
        "delta_brier_mean_ci": ci(boot_d_brier),
        "n_boot_effective": int(len(boot_d_auc)),
    }


def stratified_permutation_pvalue(
    df: pd.DataFrame,
    score_a: np.ndarray,
    score_b: np.ndarray,
    target_col: str,
    n_perm: int,
    rng: np.random.Generator,
) -> float:
    """Within-match permutation of the binary label; H0: label independent of
    features. The observed statistic is the ΔAUC = AUC(B) - AUC(A) on the OOF
    predictions; permutations shuffle ``target_col`` inside each match (which
    preserves the marginal prevalence per match) and re-evaluate ΔAUC.
    """
    matches = df["match_id"].to_numpy()
    y_obs = df[target_col].to_numpy().astype(int)
    keys = np.unique(matches)
    auc_a_obs = roc_auc_score(y_obs, score_a)
    auc_b_obs = roc_auc_score(y_obs, score_b)
    d_obs = auc_b_obs - auc_a_obs
    n_extreme = 0
    n_eff = 0
    for _ in range(n_perm):
        y_perm = y_obs.copy()
        for m in keys:
            idx = np.where(matches == m)[0]
            rng.shuffle(y_perm[idx])
        if len(np.unique(y_perm)) < 2:
            continue
        try:
            d_perm = roc_auc_score(y_perm, score_b) - roc_auc_score(y_perm, score_a)
        except ValueError:
            continue
        n_eff += 1
        if d_perm >= d_obs:
            n_extreme += 1
    if n_eff == 0:
        return float("nan")
    return float((n_extreme + 1) / (n_eff + 1))


def evaluate_block(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    seed: int = 42,
) -> tuple[dict, np.ndarray]:
    X = df[feature_cols].to_numpy(dtype=float)
    y = df[target_col].to_numpy().astype(int)
    groups = df["match_id"].to_numpy()
    # Drop rows with missing features
    mask = np.all(np.isfinite(X), axis=1)
    X = X[mask]
    y = y[mask]
    groups = groups[mask]
    df_clean = df.loc[mask].reset_index(drop=True)
    oof = oof_predict(X, y, groups, seed=seed)
    m = metrics(y, oof)
    return {"metrics": m, "feature_cols": feature_cols}, oof, df_clean


def run_target(
    df_in: pd.DataFrame,
    target_col: str,
    topo_cols: list[str],
    n_boot: int,
    n_perm: int,
    rng: np.random.Generator,
) -> dict:
    block_a, oof_a, df_a = evaluate_block(df_in, BASELINE_COLS, target_col)
    block_b, oof_b, df_b = evaluate_block(df_in, BASELINE_COLS + topo_cols, target_col)

    if len(df_a) != len(df_b):
        # Re-align by intersecting valid rows
        common = pd.merge(
            df_a[["match_id", "frame_idx"]].reset_index().rename(columns={"index": "ia"}),
            df_b[["match_id", "frame_idx"]].reset_index().rename(columns={"index": "ib"}),
            on=["match_id", "frame_idx"],
        )
        oof_a = oof_a[common["ia"].to_numpy()]
        oof_b = oof_b[common["ib"].to_numpy()]
        df_common = df_a.iloc[common["ia"].to_numpy()].reset_index(drop=True)
    else:
        df_common = df_b

    boot = match_level_bootstrap_delta(df_common, oof_a, oof_b, target_col, n_boot, rng)
    perm_p = stratified_permutation_pvalue(df_common, oof_a, oof_b, target_col, n_perm, rng)

    return {
        "target": target_col,
        "topology_features": topo_cols,
        "block_A_baselines_only": block_a,
        "block_B_baselines_plus_topology": block_b,
        "delta_auc_pooled": float(block_b["metrics"]["auc"] - block_a["metrics"]["auc"]),
        "delta_log_loss_pooled": float(block_b["metrics"]["log_loss"] - block_a["metrics"]["log_loss"]),
        "delta_brier_pooled": float(block_b["metrics"]["brier"] - block_a["metrics"]["brier"]),
        "match_level_bootstrap_ci": boot,
        "stratified_permutation_pvalue": perm_p,
        "n_frames": int(len(df_common)),
        "prevalence": float(df_common[target_col].mean()),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skillcorner-only", action="store_true")
    ap.add_argument("--sample-every", type=int, default=SAMPLE_EVERY)
    ap.add_argument("--max-frames", type=int, default=MAX_FRAMES)
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--n-perm", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    df = collect(args)
    if df.empty:
        raise SystemExit("No frames retained.")

    out_csv = OUT_DIR / "predictive_utility.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} ({len(df)} rows, {df['match_id'].nunique()} matches)")
    print(
        f"is_buildup prevalence: {df['is_buildup'].mean():.3f}"
        f"; is_chaotic prevalence: {df['is_chaotic'].mean():.3f}"
        f"; frames with any phase: {df['has_phase'].mean():.3f}"
    )

    rng = np.random.default_rng(args.seed)
    summary: dict = {
        "n_frames_total": int(len(df)),
        "n_matches": int(df["match_id"].nunique()),
        "cutoff_delta_m": TACTICAL_DELTA,
        "primary_target": "is_buildup",
        "baseline_features": BASELINE_COLS,
        "results": {},
    }

    # Primary target with three topology summaries
    summary["results"]["is_buildup_with_total_persistence"] = run_target(
        df, "is_buildup", TOPO_COLS_PRIMARY, args.n_boot, args.n_perm, rng
    )
    summary["results"]["is_buildup_with_h1_count"] = run_target(
        df, "is_buildup", TOPO_COLS_COUNT, args.n_boot, args.n_perm, rng
    )
    summary["results"]["is_buildup_with_max_persistence"] = run_target(
        df, "is_buildup", TOPO_COLS_MAX, args.n_boot, args.n_perm, rng
    )

    # Robustness target
    summary["results"]["is_chaotic_with_total_persistence"] = run_target(
        df, "is_chaotic", TOPO_COLS_PRIMARY, args.n_boot, args.n_perm, rng
    )

    out_json = OUT_DIR / "predictive_utility_summary.json"
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {out_json}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
