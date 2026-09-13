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
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402
from cutoff_protocol import silhouette_local_maxima  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))
sys.path.insert(0, str(REPO / "02_tda_core"))

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


def render_diagnostics_si() -> Path:
    """Supplement: clustering-quality diagnostics on the 1 Hz subset.

    These are not the selector. The silhouette rise beyond the tactical
    level is computed on a shrinking k >= 2 subsample.
    """
    ensure_dirs()
    d_ind, d_tac, d_team = _adopted()
    adopted = (d_ind, d_tac, d_team)

    plt.rcParams.update({
        "font.size": FONT_PT,
        "axes.labelsize": FONT_PT,
        "xtick.labelsize": FONT_PT - 1,
        "ytick.labelsize": FONT_PT - 1,
        "legend.fontsize": FONT_PT - 1,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
    })

    fig, ax = plt.subplots(figsize=(TEXTWIDTH_IN * 0.62, 6.4 / 2.54))
    fig.subplots_adjust(bottom=0.16, left=0.13, right=0.97, top=0.94)

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
        peaks = silhouette_local_maxima(md, metrics["mean_sil"].to_numpy())
        for p in peaks:
            ax.axvline(p, color=PEAK_COL, ls=":", lw=1.0, zorder=1)
            ax.text(p + 0.6, 1.02, f"{p:g} m", color=PEAK_COL,
                    fontsize=FONT_PT - 2, ha="left", va="top")
        (OUTPUT_DIR / "silhouette_local_maxima.json").write_text(
            json.dumps({"deltas_m": peaks}, indent=2)
        )
    else:
        ax.text(0.5, 0.5, "1 Hz diagnostics not yet written",
                ha="center", va="center", transform=ax.transAxes)

    for x in adopted:
        ax.axvline(x, color=ADOPTED_COL, ls="-", lw=1.0, zorder=2)
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(-0.05, 1.08)
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel("Metric (min-max scaled)")
    ax.legend(loc="upper center", frameon=False, borderaxespad=0.15)
    ax.tick_params(color="#666666", labelcolor=TEXT)
    for spine in ax.spines.values():
        spine.set_color("#666666")

    out_pdf = FIGURES_DIR / "figS2_cutoff_diagnostics.pdf"
    out_png = FIGURES_DIR / "figS2_cutoff_diagnostics.png"
    fig.savefig(out_pdf, dpi=300)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"Wrote {out_pdf}")
    return out_pdf


TARGETS = (("individual", 19.0), ("tactical", 5.0), ("team", 2.0))
BAND_COL = "#8FB8DE"
QUANT_COL = "#4C72B0"
FEASIBLE_COL = "#009E73"

PITCH_COL = (0.22, 0.56, 0.24)
PITCH_LINE = (1, 1, 1)
SINGLETON_COL = (0.80, 0.80, 0.80)
CLUSTER_PALETTE = (
    "#D55E00", "#0072B2", "#E69F00", "#009E73",
    "#CC79A7", "#56B4E9", "#F0E442", "#8C564B",
)


def _convex_hull(pts):
    pts = np.unique(np.asarray(pts, dtype=float), axis=0)
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    order = pts[np.lexsort((pts[:, 1], pts[:, 0]))]
    lower, upper = [], []
    for p in order:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(tuple(p))
    for p in order[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(tuple(p))
    return np.asarray(lower[:-1] + upper[:-1])


def _draw_pitch(ax):
    ax.add_patch(plt.Rectangle(
        (-52.5, -34), 105, 68, facecolor=PITCH_COL,
        edgecolor=PITCH_LINE, linewidth=0.8,
    ))
    ax.axvline(0, color=PITCH_LINE, lw=0.8)
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(9.15 * np.cos(theta), 9.15 * np.sin(theta),
            color=PITCH_LINE, lw=0.8)
    ax.plot([-48.0, -38.0], [-31.0, -31.0], color=PITCH_LINE, lw=2.0,
            solid_capstyle="butt")
    ax.text(-37.0, -31.0, "10 m", color=PITCH_LINE, ha="left", va="center",
            fontsize=FONT_PT - 3)
    ax.set_xlim(-55, 55)
    ax.set_ylim(-37, 37)
    ax.set_aspect("equal")
    ax.axis("off")


def plot_cluster_snapshot(ax, positions, cutoff, panel, level):
    """One frame clustered at ``cutoff``. Colour multi-member clusters."""
    from primary_match_skillcorner_analysis import cutoff_cluster

    _draw_pitch(ax)
    pos = np.asarray(positions)
    _, labels = cutoff_cluster(pos, cutoff)
    unique, counts = np.unique(labels, return_counts=True)
    order = unique[np.argsort(-counts)]
    palette_i = 0
    for lab in order:
        members = pos[labels == lab]
        if len(members) >= 2:
            col = CLUSTER_PALETTE[palette_i % len(CLUSTER_PALETTE)]
            palette_i += 1
            if len(members) >= 3:
                hull = _convex_hull(members)
                closed = np.vstack([hull, hull[0]])
                ax.fill(closed[:, 0], closed[:, 1], color=col, alpha=0.16,
                        zorder=1)
            ax.scatter(members[:, 0], members[:, 1], s=26, c=[col],
                       edgecolors="#222222", linewidths=0.4, zorder=4)
        else:
            ax.scatter(members[:, 0], members[:, 1], s=20, c=[SINGLETON_COL],
                       edgecolors="#222222", linewidths=0.35, zorder=3)
    ax.text(
        52.0, 31.0, f"$H_0 = {len(unique)}$", color=PITCH_LINE,
        ha="right", va="top", fontsize=FONT_PT - 1, fontweight="bold",
        zorder=6,
    )
    ax.set_title(
        f"({panel}) {level}  ($\\delta = {cutoff:g}$ m)",
        loc="left", fontsize=FONT_PT - 1, fontweight="bold", pad=3,
    )


def _pooled_h0_quantiles(qs=(5, 25, 50, 75, 95)):
    """Per-frame H0 quantiles vs delta, pooled over all ten matches."""
    z = np.load(OUTPUT_DIR / "cutoff_sweep_h0.npz")
    deltas = z["deltas"]
    stacked = np.concatenate(
        [z[f"k_{mid}"] for mid in z["match_ids"]], axis=0
    ).astype(np.float32)
    out = {q: np.percentile(stacked, q, axis=0) for q in qs}
    return deltas, out, stacked.shape[0]


def render_figure() -> Path:
    """Figure 2: cardinality-inversion estimator (top) and spatial realisation."""
    ensure_dirs()
    pooled = pd.read_csv(OUTPUT_DIR / "cutoff_sweep_agg.csv")
    per_match = pd.read_csv(OUTPUT_DIR / "cutoff_sweep_per_match.csv")
    regimes = pd.read_csv(OUTPUT_DIR / "regime_summary.csv").set_index("scale")
    per_level = pd.read_csv(OUTPUT_DIR / "regime_per_match.csv")
    d_ind, d_tac, d_team = _adopted()
    adopted = {"individual": d_ind, "tactical": d_tac, "team": d_team}

    delta = pooled["delta"].to_numpy()
    h0 = pooled["mean_h0"].to_numpy()
    p_k4 = pooled["p_k_ge_4"].to_numpy()
    qdelta, quants, n_frames = _pooled_h0_quantiles()

    # Primary-match frame 95 for the spatial row (same frame as Figure 3).
    from primary_match_skillcorner_analysis import (
        ensure_match_assets, load_tracking_data,
    )
    cfg = load_config()
    ensure_match_assets()
    frames, _, _ = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    fstep = max(1, len(frames) // n_sample)
    frame_idx = cfg["figures"]["individual_frame_idx"]
    snap_pos = frames[::fstep][:n_sample][frame_idx]["positions"]

    plt.rcParams.update({
        "font.size": FONT_PT,
        "axes.labelsize": FONT_PT,
        "xtick.labelsize": FONT_PT - 1,
        "ytick.labelsize": FONT_PT - 1,
        "legend.fontsize": FONT_PT - 2,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
    })

    fig, axes = plt.subplots(2, 3, figsize=(TEXTWIDTH_IN, 13.6 / 2.54))
    fig.subplots_adjust(wspace=0.40, hspace=0.30, bottom=0.09, left=0.08,
                        right=0.99, top=0.90)

    # (a) the estimator: target cardinalities intersect one curve
    ax = axes[0, 0]
    for mid, grp in per_match.groupby("match_id"):
        ax.plot(grp["delta"], grp["mean_h0"], color=RIBBON, lw=0.6, alpha=0.9,
                zorder=1)
    ax.plot(delta, h0, color=H0_LINE, lw=1.7, zorder=3)
    for level, target in TARGETS:
        x = adopted[level]
        ax.axhline(target, color=ADOPTED_COL, ls=(0, (4, 3)), lw=0.8, zorder=2)
        ax.plot([x, x], [0, target], color=ADOPTED_COL, ls="-", lw=1.0, zorder=2)
        ax.plot([x], [target], "o", ms=4.2, mfc="white", mec=ADOPTED_COL,
                mew=1.3, zorder=5)
    label_xy = {"individual": (22.0, 19.0), "tactical": (5.6, 5.0),
                "team": (25.0, 2.0)}
    for level, target in TARGETS:
        x = adopted[level]
        ax.axhline(target, color=ADOPTED_COL, ls=(0, (4, 3)), lw=0.8, zorder=2)
        ax.plot([x, x], [0, target], color=ADOPTED_COL, ls="-", lw=1.0, zorder=2)
        ax.plot([x], [target], "o", ms=4.2, mfc="white", mec=ADOPTED_COL,
                mew=1.3, zorder=5)
        lx, ly = label_xy[level]
        ax.annotate(
            f"$\\overline{{H_0}} = {target:.0f}$",
            xy=(lx, ly), xytext=(0, 3.0), textcoords="offset points",
            fontsize=FONT_PT - 2, ha="left", va="bottom", color=TEXT, zorder=6,
        )
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(0, 23)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel(r"Mean cluster count ($H_0$)")
    ax.set_title("(a) Inversion", loc="left", fontsize=FONT_PT,
                 fontweight="bold", pad=16)

    top = ax.secondary_xaxis("top")
    top.set_xticks([d_ind, d_tac, d_team])
    top.set_xticklabels([f"{v:g}" for v in (d_ind, d_tac, d_team)])
    top.tick_params(labelsize=FONT_PT - 2, color="#666666", labelcolor=TEXT,
                    length=3)
    top.spines["top"].set_color("#666666")

    inset = ax.inset_axes([0.45, 0.32, 0.50, 0.38])
    inset.plot(delta, h0, color=H0_LINE, lw=1.3)
    inset.axhline(19.0, color=ADOPTED_COL, ls=(0, (4, 3)), lw=0.8)
    inset.axvline(d_ind, color=ADOPTED_COL, lw=1.0)
    inset.set_xlim(0.0, 5.0)
    inset.set_ylim(17.5, 22.5)
    inset.tick_params(labelsize=FONT_PT - 3, color="#666666", labelcolor=TEXT)
    for spine in inset.spines.values():
        spine.set_color("#666666")

    # (b) distribution across frames plus the acceptance test
    ax = axes[0, 1]
    ax.fill_between(qdelta, quants[5], quants[95], color=BAND_COL, alpha=0.45,
                    lw=0, zorder=1)
    ax.fill_between(qdelta, quants[25], quants[75], color=BAND_COL, alpha=0.8,
                    lw=0, zorder=2)
    ax.plot(qdelta, quants[50], color=QUANT_COL, lw=1.5, zorder=3)
    for level, _ in TARGETS:
        x = adopted[level]
        lo = float(regimes.loc[level, "acceptance_lo"])
        hi = float(regimes.loc[level, "acceptance_hi"])
        ax.plot([x, x], [lo, hi], color=ADOPTED_COL, lw=1.4, zorder=5,
                solid_capstyle="butt")
        for cap in (lo, hi):
            ax.plot([x - 0.9, x + 0.9], [cap, cap], color=ADOPTED_COL, lw=1.4,
                    zorder=5)
        means = per_level.loc[per_level["scale"] == level, "mean_h0_at_adopted"]
        ax.plot([x] * len(means), means, "o", ms=2.8, mfc=PEAK_COL,
                mec="white", mew=0.4, zorder=6)
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(0, 23)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel(r"$H_0$ per frame")
    ax.set_title("(b) Acceptance", loc="left", fontsize=FONT_PT,
                 fontweight="bold", pad=4)

    # (c) the feasibility constraint on the tactical rule
    ax = axes[0, 2]
    feasible = delta[p_k4 >= 0.5]
    d_feas = float(feasible.max()) if feasible.size else 0.0
    ax.axvspan(0.0, d_feas, color=FEASIBLE_COL, alpha=0.14, lw=0, zorder=1)
    ax.plot(delta, p_k4, color=FEASIBLE_COL, lw=1.7, zorder=3)
    ax.axhline(0.5, color=ADOPTED_COL, ls=(0, (4, 3)), lw=0.8, zorder=2)
    ax.axvline(d_tac, color=ADOPTED_COL, lw=1.0, zorder=4)
    ax.plot([d_tac], [p_k4[int(np.argmin(np.abs(delta - d_tac)))]], "o", ms=4.2,
            mfc="white", mec=ADOPTED_COL, mew=1.3, zorder=5)
    ax.text(d_feas + 1.5, 0.92, f"feasible\n$\\delta \\leq {d_feas:g}$ m",
            fontsize=FONT_PT - 2, ha="left", va="top", color=TEXT)
    ax.annotate(
        f"{d_tac:g} m", xy=(d_tac, 0.0), xytext=(2.5, 1.5),
        textcoords="offset points", fontsize=FONT_PT - 2, ha="left",
        va="bottom", color=TEXT, rotation=90, zorder=6,
    )
    ax.set_xlim(0.0, 40.5)
    ax.set_ylim(-0.04, 1.06)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel(r"Cutoff $\delta$ (m)")
    ax.set_ylabel(r"$P(k \geq 4)$")
    ax.set_title("(c) Feasibility", loc="left", fontsize=FONT_PT,
                 fontweight="bold", pad=4)

    for a in axes[0]:
        a.tick_params(color="#666666", labelcolor=TEXT)
        for spine in a.spines.values():
            spine.set_color("#666666")

    # bottom row: the spatial realisation of H0 = 19, 5, 2 on frame 95
    plot_cluster_snapshot(axes[1, 0], snap_pos, d_ind, "d", "Individual")
    plot_cluster_snapshot(axes[1, 1], snap_pos, d_tac, "e", "Tactical")
    plot_cluster_snapshot(axes[1, 2], snap_pos, d_team, "f", "Team")
    print(f"Figure 2 built on {n_frames:,} complete frames")
    out_pdf = FIGURES_DIR / "fig2_cutoff_sweep.pdf"
    out_png = FIGURES_DIR / "fig2_cutoff_sweep.png"
    fig.savefig(out_pdf, dpi=300)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"Wrote {out_pdf}")
    return out_pdf


def main() -> None:
    render_figure()
    render_diagnostics_si()


if __name__ == "__main__":
    main()
