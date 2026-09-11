#!/usr/bin/env python3
"""Generate Figure 2: cutoff sweep (Section 2.3).

Pooled H0 inversion on all complete frames of the ten Table S1 matches.
Panel (b) uses the 1 Hz diagnostic metrics. This is not \\tilde{T}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs  # noqa: E402
from cutoff_protocol import silhouette_local_maxima  # noqa: E402

TEXTWIDTH_IN = 16.0 / 2.54
FONT_PT = 10

TEXT = "#222222"
H0_LINE = "#222222"
RIBBON = "#B0B0B0"
CH_COL = "#0072B2"
SIL_COL = "#D55E00"
IC_COL = "#009E73"
ADOPTED_COL = "#111111"
PEAK_COL = "#D55E00"


def _minmax(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    finite = x[np.isfinite(x)]
    if finite.size == 0:
        return np.zeros_like(x)
    lo, hi = float(np.min(finite)), float(np.max(finite))
    if hi <= lo:
        return np.zeros_like(x)
    out = (x - lo) / (hi - lo)
    out[~np.isfinite(x)] = np.nan
    return out


def _adopted() -> tuple[float, float, float]:
    regimes = pd.read_csv(OUTPUT_DIR / "regime_summary.csv")
    vals = {
        str(r["scale"]): float(r["adopted_cutoff_m"])
        for _, r in regimes.iterrows()
    }
    return vals["individual"], vals["tactical"], vals["team"]


def render_figure() -> Path:
    ensure_dirs()
    pooled = pd.read_csv(OUTPUT_DIR / "cutoff_sweep_agg.csv")
    per_match = pd.read_csv(OUTPUT_DIR / "cutoff_sweep_per_match.csv")
    adopted = _adopted()

    delta = pooled["delta"].to_numpy()
    h0 = pooled["mean_h0"].to_numpy()
    match_means = (
        per_match.groupby("delta")["mean_h0"].agg(["mean", "std"]).reset_index()
    )
    match_means = match_means.set_index("delta").reindex(delta)
    h0_match_sd = match_means["std"].to_numpy(dtype=float)

    plt.rcParams.update({
        "font.size": FONT_PT,
        "axes.labelsize": FONT_PT,
        "xtick.labelsize": FONT_PT - 1,
        "ytick.labelsize": FONT_PT - 1,
        "legend.fontsize": FONT_PT - 1,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
    })

    fig, axes = plt.subplots(
        1, 2, figsize=(TEXTWIDTH_IN, 6.4 / 2.54),
    )
    fig.subplots_adjust(wspace=0.34, bottom=0.16, left=0.08, right=0.99, top=0.90)

    ax = axes[0]
    ax.fill_between(
        delta, h0 - h0_match_sd, h0 + h0_match_sd,
        color=RIBBON, alpha=0.45, lw=0,
    )
    ax.plot(delta, h0, color=H0_LINE, lw=1.6)
    for x in adopted:
        ax.axvline(x, color=ADOPTED_COL, ls="-", lw=1.0, zorder=2)
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(0, 23)
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel(r"Mean cluster count ($H_0$)")
    ax.set_title("(a)", loc="left", fontsize=FONT_PT, fontweight="bold", pad=4)

    ax = axes[1]
    metrics_path = OUTPUT_DIR / "cutoff_sweep_metrics.csv"
    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path)
        md = metrics["delta"].to_numpy()
        ax.plot(md, _minmax(metrics["mean_ch"].to_numpy()), color=CH_COL, lw=1.6,
                label="Calinski-Harabasz")
        ax.plot(md, _minmax(metrics["mean_sil"].to_numpy()), color=SIL_COL, lw=1.6,
                label="Silhouette")
        ax.plot(md, _minmax(metrics["mean_ic"].to_numpy()), color=IC_COL, lw=1.6,
                label="Information-content")
        peaks = silhouette_local_maxima(
            md, metrics["mean_sil"].to_numpy()
        )
        for p in peaks:
            ax.axvline(p, color=PEAK_COL, ls=":", lw=1.0, zorder=1)
        (OUTPUT_DIR / "silhouette_local_maxima.json").write_text(
            json.dumps({"deltas_m": peaks}, indent=2)
        )
    else:
        ax.text(
            0.5, 0.5, "1 Hz diagnostics not yet written",
            ha="center", va="center", transform=ax.transAxes,
        )
    for x in adopted:
        ax.axvline(x, color=ADOPTED_COL, ls="-", lw=1.0, zorder=2)
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(-0.05, 1.08)
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel("Metric (min-max scaled)")
    ax.set_title("(b)", loc="left", fontsize=FONT_PT, fontweight="bold", pad=4)
    ax.legend(loc="upper right", frameon=False, borderaxespad=0.15)

    for a in axes:
        a.tick_params(color="#666666", labelcolor=TEXT)
        for spine in a.spines.values():
            spine.set_color("#666666")

    out_pdf = FIGURES_DIR / "fig2_cutoff_sweep.pdf"
    out_png = FIGURES_DIR / "fig2_cutoff_sweep.png"
    fig.savefig(out_pdf, dpi=300)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"Wrote {out_pdf}")
    return out_pdf


def main() -> None:
    render_figure()


if __name__ == "__main__":
    main()
