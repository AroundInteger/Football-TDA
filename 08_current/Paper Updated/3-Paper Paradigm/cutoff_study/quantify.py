#!/usr/bin/env python3
"""Numerical dossier for the three adopted cutoffs.

Reads committed Paper A sweep tables only. Does not re-run tracking.
Does not write into paper_A_JACT/sections.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

HERE = Path(__file__).resolve().parent
PAPER_A = HERE.parent / "paper_A_JACT"
OUT = HERE / "outputs"
SWEEP_AGG = PAPER_A / "pipeline" / "outputs" / "cutoff_sweep_agg.csv"
SWEEP_RAW = PAPER_A / "pipeline" / "outputs" / "cutoff_sweep_results.csv"

ADOPTED = {"individual": 2.98, "tactical": 12.0, "team": 30.0}
NAMED = {
    "ch_peak": 1.39,
    "ic_tactical": 6.87,
    "sil_tactical": 16.31,
}
H0_BANDS = {
    "individual": (15, 22),
    "tactical": (2, 12),
    "team": (1, 3),
}


def _nearest(agg: pd.DataFrame, delta: float) -> pd.Series:
    return agg.iloc[(agg["cutoff"] - delta).abs().to_numpy().argmin()]


def _stability(raw: pd.DataFrame, delta: float, tol: float = 0.5) -> dict:
    sub = raw[np.abs(raw["cutoff"] - delta) < tol]
    if sub.empty:
        return {"n": 0, "stability": None, "median_h0": None}
    med = float(sub["n_clusters"].median())
    stab = float((np.abs(sub["n_clusters"] - med) <= 2).mean())
    return {
        "n": int(len(sub)),
        "stability": round(stab, 4),
        "median_h0": med,
        "mean_h0": round(float(sub["n_clusters"].mean()), 3),
        "sd_h0": round(float(sub["n_clusters"].std()), 3),
    }


def _band_interval(agg: pd.DataFrame, lo: float, hi: float) -> dict:
    m = (agg["mean_n_clusters"] >= lo) & (agg["mean_n_clusters"] <= hi)
    if not m.any():
        return {"delta_min": None, "delta_max": None, "n_grid": 0}
    d = agg.loc[m, "cutoff"]
    return {
        "delta_min": round(float(d.min()), 4),
        "delta_max": round(float(d.max()), 4),
        "n_grid": int(m.sum()),
        "width_m": round(float(d.max() - d.min()), 4),
    }


def _row_pack(row: pd.Series) -> dict:
    return {
        "grid_cutoff_m": round(float(row["cutoff"]), 4),
        "mean_h0": round(float(row["mean_n_clusters"]), 3),
        "sd_h0": round(float(row["std_n_clusters"]), 3),
        "mean_ch": round(float(row["mean_ch"]), 3),
        "mean_sil": round(float(row["mean_sil"]), 4),
        "mean_ic": round(float(row["mean_ic"]), 4),
        "val_individual": round(float(row["val_individual"]), 4),
        "val_tactical": round(float(row["val_tactical"]), 4),
        "val_team": round(float(row["val_team"]), 4),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    agg = pd.read_csv(SWEEP_AGG).sort_values("cutoff").reset_index(drop=True)
    raw = pd.read_csv(SWEEP_RAW)

    grid = {
        "n_cutoffs": int(len(agg)),
        "delta_min": float(agg["cutoff"].min()),
        "delta_max": float(agg["cutoff"].max()),
        "n_raw_rows": int(len(raw)),
        "n_windows_unique": int(raw.groupby(["epoch", "win_idx"]).ngroups),
        "epochs": sorted(raw["epoch"].unique().tolist()),
        "windows_per_epoch": {
            str(k): int(v) for k, v in raw.groupby("epoch")["win_idx"].nunique().items()
        },
        "paper_caption_claims_58": True,
        "seconds_spectrum_58_design": {
            "1min": 31, "2min": 16, "5min": 7, "10min": 4, "total": 58
        },
        "right_endpoint_is_30": bool(np.isclose(agg["cutoff"].max(), 30.0)),
    }

    optima = {
        "ch_argmax_m": float(agg.loc[agg["mean_ch"].idxmax(), "cutoff"]),
        "sil_argmax_m": float(agg.loc[agg["mean_sil"].idxmax(), "cutoff"]),
        "ic_argmax_m": float(agg.loc[agg["mean_ic"].idxmax(), "cutoff"]),
        "ic_argmin_m": float(agg.loc[agg["mean_ic"].idxmin(), "cutoff"]),
        "sil_argmax_h0": float(agg.loc[agg["mean_sil"].idxmax(), "mean_n_clusters"]),
        "ch_argmax_h0": float(agg.loc[agg["mean_ch"].idxmax(), "mean_n_clusters"]),
    }

    peaks_idx, _ = find_peaks(agg["mean_sil"].to_numpy(), prominence=0.01)
    sil_peaks = []
    for i in peaks_idx:
        sil_peaks.append({
            "delta_m": round(float(agg.loc[i, "cutoff"]), 4),
            "silhouette": round(float(agg.loc[i, "mean_sil"]), 4),
            "mean_h0": round(float(agg.loc[i, "mean_n_clusters"]), 3),
        })

    adopted = {}
    for name, delta in ADOPTED.items():
        row = _nearest(agg, delta)
        adopted[name] = {
            "stated_m": delta,
            "offset_from_grid_m": round(float(row["cutoff"] - delta), 4),
            **_row_pack(row),
            "stability_pm0.5m": _stability(raw, delta),
            "h0_band_prior": list(H0_BANDS[name]),
            "mean_h0_in_prior_band": bool(
                H0_BANDS[name][0] <= row["mean_n_clusters"] <= H0_BANDS[name][1]
            ),
        }

    named = {}
    for name, delta in NAMED.items():
        row = _nearest(agg, delta)
        named[name] = {"stated_m": delta, **_row_pack(row)}

    bands = {k: _band_interval(agg, lo, hi) for k, (lo, hi) in H0_BANDS.items()}

    # Original methodology restricted the search to named δ-bands, then
    # averaged per-epoch argmax (SecondSpectrum GPS, 58 windows).
    original_bands = {
        "individual_ch_0.5_3.0": ("mean_ch", 0.5, 3.0, "max"),
        "tactical_sil_8_15": ("mean_sil", 8.0, 15.0, "max"),
        "tactical_ic_8_15": ("mean_ic", 8.0, 15.0, "max"),
        "team_ic_15_25": ("mean_ic", 15.0, 25.0, "min"),
        "team_sil_15_25": ("mean_sil", 15.0, 25.0, "max"),
    }
    restricted = {}
    for name, (col, lo, hi, how) in original_bands.items():
        sub = agg[(agg["cutoff"] >= lo) & (agg["cutoff"] <= hi)]
        if sub.empty:
            restricted[name] = None
            continue
        idx = sub[col].idxmin() if how == "min" else sub[col].idxmax()
        restricted[name] = {
            "delta_m": round(float(sub.loc[idx, "cutoff"]), 4),
            "metric": round(float(sub.loc[idx, col]), 4),
            "mean_h0": round(float(sub.loc[idx, "mean_n_clusters"]), 3),
        }

    # Per-epoch argmax then mean: the original "cross-epoch mean" rule.
    per_epoch = {}
    epoch_optima = []
    for epoch, g in raw.groupby("epoch"):
        eagg = g.groupby("cutoff", as_index=False).mean(numeric_only=True)
        per_epoch[epoch] = {
            "n_windows": int(g["win_idx"].nunique()),
            "ch_argmax_m": round(float(eagg.loc[eagg["ch_score"].idxmax(), "cutoff"]), 4),
            "sil_argmax_m": round(float(eagg.loc[eagg["sil_score"].idxmax(), "cutoff"]), 4),
            "ic_argmin_m": round(float(eagg.loc[eagg["info_content"].idxmin(), "cutoff"]), 4),
        }
        epoch_optima.append(per_epoch[epoch])
    cross_epoch_mean = {
        "ch_argmax_m": round(float(np.mean([e["ch_argmax_m"] for e in epoch_optima])), 4),
        "sil_argmax_m": round(float(np.mean([e["sil_argmax_m"] for e in epoch_optima])), 4),
        "ic_argmin_m": round(float(np.mean([e["ic_argmin_m"] for e in epoch_optima])), 4),
    }

    tac = agg[(agg["mean_n_clusters"] >= 2) & (agg["mean_n_clusters"] <= 12)]
    metric_only = {
        "individual_if_ch": round(float(agg.loc[agg["mean_ch"].idxmax(), "cutoff"]), 4),
        "tactical_if_sil_in_h0_2_12": (
            round(float(tac.loc[tac["mean_sil"].idxmax(), "cutoff"]), 4)
            if len(tac) else None
        ),
        "tactical_if_ic_in_h0_2_12": (
            round(float(tac.loc[tac["mean_ic"].idxmax(), "cutoff"]), 4)
            if len(tac) else None
        ),
        "team_if_sil_global": round(float(agg.loc[agg["mean_sil"].idxmax(), "cutoff"]), 4),
        "team_if_ic_min": round(float(agg.loc[agg["mean_ic"].idxmin(), "cutoff"]), 4),
        "team_if_first_mean_h0_le_2": (
            round(float(agg.loc[agg["mean_n_clusters"] <= 2, "cutoff"].iloc[0]), 4)
            if (agg["mean_n_clusters"] <= 2).any() else None
        ),
        "restricted_to_original_bands": restricted,
        "per_epoch": per_epoch,
        "cross_epoch_mean_of_argmax": cross_epoch_mean,
    }

    dossier = {
        "source": {
            "sweep_agg": str(SWEEP_AGG.relative_to(PAPER_A.parent)),
            "sweep_raw": str(SWEEP_RAW.relative_to(PAPER_A.parent)),
        },
        "grid": grid,
        "optima_unrestricted": {k: round(v, 4) if isinstance(v, float) else v
                                for k, v in optima.items()},
        "silhouette_peaks_prominence_0.01": sil_peaks,
        "adopted": adopted,
        "named_paper_marks": named,
        "h0_band_occupied_intervals": bands,
        "metric_only_alternatives": metric_only,
        "circularity": {
            "note": (
                "H0 validation rates use pre-set bands. A cutoff is then "
                "called validated if mean H0 lands in that band."
            ),
            "bands_are_priors": True,
        },
        "provenance": {
            "2.98": (
                "SecondSpectrum GPS, 58-window 30% coverage, Calinski-Harabasz "
                "cross-epoch mean in the 0.5-3.0 m search band. Not the "
                "SkillCorner unrestricted CH argmax (1.39 m)."
            ),
            "6.87": (
                "SecondSpectrum GPS. Goal-specific tactical information-content "
                "(rewards H0 in 0.2-0.5 of 22 players), not the entropy IC "
                "in cutoff_sweep_agg.csv."
            ),
            "12.0": (
                "Domain heuristic (half a football zone width), retained after "
                "a 50-frame single-frame check against 16.31 m. Not a metric "
                "argmax on either corpus."
            ),
            "16.31": (
                "SecondSpectrum GPS. Silhouette cross-epoch mean. Listed under "
                "tactical range 8-15 m even though 16.31 lies outside that band."
            ),
            "28.11": (
                "SecondSpectrum GPS. Goal-specific team information-content "
                "cross-epoch mean. Listed under range 15-25 m even though "
                "28.11 lies outside that band."
            ),
            "30.0": (
                "Right endpoint of np.linspace(0.5, 30.0, 100). identify_regimes "
                "selects min IC among rows with val_team > 0.9; IC falls as "
                "clusters merge, so the rule returns the grid edge."
            ),
        },
    }

    OUT.joinpath("dossier.json").write_text(json.dumps(dossier, indent=2) + "\n")
    print(json.dumps(dossier, indent=2))


if __name__ == "__main__":
    main()
