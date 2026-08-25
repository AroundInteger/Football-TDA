#!/usr/bin/env python3
"""
Half-level random-effects test (Paper v5 revision, §3.4)
========================================================

Formalises the "match-specific dynamics" claim by fitting a linear mixed
model for per-window tactical-scale H1 persistence across 10 matches:

    persistence ~ half + (half | match)

and reports the fixed-effect for ``half`` (point estimate, 95% CI, p-value)
plus the random slope variance. A permutation test stratified by match
complements the LMM.

Usage:
    python half_level_random_effects.py

Outputs:
    results/paper_v5_revisions/half_level_random_effects.json
"""

from __future__ import annotations

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

TACTICAL_DELTA = VALIDATED_CUTOFFS["tactical"]
FRAMES_PER_HALF = 250  # uniform sample per half


def per_half_windows(match, frames_per_half: int = FRAMES_PER_HALF) -> pd.DataFrame:
    """Compute one tactical-scale persistence value per 2-minute window
    separately in first and second halves."""
    complete = match.complete_frames
    if not complete:
        return pd.DataFrame()
    # Split halves by median frame index as a robust proxy
    mid = len(complete) // 2
    halves = {"first": complete[:mid], "second": complete[mid:]}
    rows = []
    for hname, frames in halves.items():
        # 2-min windows at 10 Hz = 1200 frames
        step = 1200
        for start in range(0, len(frames) - step, step):
            window = frames[start : start + step]
            persistences = []
            for fr in window[::10]:  # sub-sample 1 Hz within window
                diagrams = compute_h1_at_scale(fr.all_positions, TACTICAL_DELTA)
                persistences.append(float(diagrams.h1_stats.get("total", 0.0)))
            if persistences:
                rows.append(
                    {
                        "match_id": match.info.match_id,
                        "half": hname,
                        "window_idx": start // step,
                        "persistence": float(np.mean(persistences)),
                    }
                )
    return pd.DataFrame(rows)


def permutation_test_stratified(
    df: pd.DataFrame, n_perm: int = 10000, seed: int = 42
) -> float:
    """Within-match permutation of half labels; returns two-sided p-value."""
    rng = np.random.default_rng(seed)
    obs = (
        df.groupby("match_id")
        .apply(
            lambda g: g.loc[g.half == "second", "persistence"].mean()
            - g.loc[g.half == "first", "persistence"].mean()
        )
        .mean()
    )
    count = 0
    for _ in range(n_perm):
        permuted = df.copy()
        for mid, g in df.groupby("match_id"):
            idx = g.index.to_numpy()
            shuffled = rng.permutation(g["half"].to_numpy())
            permuted.loc[idx, "half"] = shuffled
        stat = (
            permuted.groupby("match_id")
            .apply(
                lambda g: g.loc[g.half == "second", "persistence"].mean()
                - g.loc[g.half == "first", "persistence"].mean()
            )
            .mean()
        )
        if abs(stat) >= abs(obs):
            count += 1
    return (count + 1) / (n_perm + 1)


def fit_lmm(df: pd.DataFrame) -> dict:
    import statsmodels.formula.api as smf

    df = df.copy()
    df["half_bin"] = (df["half"] == "second").astype(int)
    try:
        model = smf.mixedlm(
            "persistence ~ half_bin", df, groups=df["match_id"], re_formula="~half_bin"
        )
        res = model.fit(method="lbfgs", reml=True)
        coef = float(res.params.get("half_bin"))
        se = float(res.bse.get("half_bin"))
        p = float(res.pvalues.get("half_bin"))
        re_var = res.cov_re.to_dict() if hasattr(res, "cov_re") else {}
    except Exception as e:
        return {"error": repr(e)}
    return {
        "fixed_half_coef": coef,
        "fixed_half_se": se,
        "fixed_half_ci95": [coef - 1.96 * se, coef + 1.96 * se],
        "fixed_half_p": p,
        "random_effects_cov": re_var,
    }


def main() -> None:
    rows = []
    for meta in skillcorner.list_matches():
        try:
            match = skillcorner.load_match(meta["id"])
        except FileNotFoundError:
            continue
        df_match = per_half_windows(match)
        rows.append(df_match)
        print(f"[{meta['id']}] {len(df_match)} windows")
    df = pd.concat(rows, ignore_index=True)
    df.to_csv(OUT_DIR / "half_level_windows.csv", index=False)

    lmm = fit_lmm(df)
    perm_p = permutation_test_stratified(df, n_perm=10000)
    out = {
        "n_matches": int(df["match_id"].nunique()),
        "n_windows": int(len(df)),
        "lmm": lmm,
        "permutation_test_stratified_p": float(perm_p),
    }
    with open(OUT_DIR / "half_level_random_effects.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
