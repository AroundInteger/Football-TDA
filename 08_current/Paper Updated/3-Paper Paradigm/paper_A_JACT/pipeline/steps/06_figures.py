#!/usr/bin/env python3
"""Step 06: generate fig2_cycle_geometry from uniform sample."""
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

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))
sys.path.insert(0, str(REPO / "02_tda_core"))

from primary_match_skillcorner_analysis import (  # noqa: E402
    ensure_match_assets,
    load_tracking_data,
    h1_at_cutoff,
    VALIDATED_CUTOFFS,
    FPS,
)
from tda_utils import find_closed_cycles  # noqa: E402

PITCH_COL = (0.22, 0.56, 0.24)
LINE_COL = (1, 1, 1)
CYCLE_EDGE = (0.85, 0.15, 0.15)
CYCLE_FILL = (0.85, 0.15, 0.15)
CENTROID_COL = (0.15, 0.30, 0.70)
NON_CYCLE = (0.55, 0.55, 0.55)


def draw_pitch(ax):
    rect = plt.Rectangle((-52.5, -34), 105, 68, facecolor=PITCH_COL, edgecolor=LINE_COL, linewidth=1)
    ax.add_patch(rect)
    ax.axvline(0, color=LINE_COL, lw=1)
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(9.15 * np.cos(theta), 9.15 * np.sin(theta), color=LINE_COL, lw=1)
    ax.set_facecolor(PITCH_COL)
    ax.set_xlim(-55, 55)
    ax.set_ylim(-37, 37)
    ax.set_aspect("equal")
    ax.axis("off")


def plot_panel(ax, positions, cutoff, title):
    draw_pitch(ax)
    h0_d, h1_d, centroids, _ = h1_at_cutoff(positions, cutoff)
    pts = np.asarray(centroids)
    if pts.size == 0:
        ax.set_title(title)
        return 0.0

    ax.scatter(pts[:, 0], pts[:, 1], s=40, c=[NON_CYCLE], edgecolors="w", linewidths=0.5)

    max_p = 0.0
    if len(h1_d) > 0:
        pers = h1_d[:, 1] - h1_d[:, 0]
        idx = int(np.argmax(pers))
        max_p = float(pers[idx])
        cycles = find_closed_cycles(
            np.asarray(centroids), float(h1_d[idx, 0]), float(h1_d[idx, 1])
        )
        if cycles:
            cycle_nodes = cycles[0].nodes
            cx = pts[cycle_nodes, 0]
            cy = pts[cycle_nodes, 1]
            ax.fill(cx, cy, color=CYCLE_FILL, alpha=0.12)
            n = len(cx)
            for k in range(n):
                k2 = (k + 1) % n
                ax.plot([cx[k], cx[k2]], [cy[k], cy[k2]], color=CYCLE_EDGE, lw=2.2)
            ax.scatter(cx, cy, s=70, c=[CENTROID_COL], edgecolors="w", linewidths=0.8)

    ax.set_title(title, fontsize=11, fontweight="bold")
    return max_p


if __name__ == "__main__":
    ensure_dirs()
    cfg = load_config()
    summary_path = OUTPUT_DIR / "uniform_150" / "uniform_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError("Run step 01 first.")

    with open(summary_path) as f:
        summary = json.load(f)

    ensure_match_assets()
    frames, home, away = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]

    ind_idx = cfg["figures"]["individual_frame_idx"]
    tac_idx = cfg["figures"]["tactical_frame_idx"]

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    p_ind = plot_panel(
        axes[0],
        sample[ind_idx]["positions"],
        VALIDATED_CUTOFFS["individual"],
        f"(a) Individual scale (δ = 2.98 m)\nSample frame {ind_idx}",
    )
    p_tac = plot_panel(
        axes[1],
        sample[tac_idx]["positions"],
        VALIDATED_CUTOFFS["tactical"],
        f"(b) Tactical scale (δ = 12.0 m)\nSample frame {tac_idx}",
    )
    fig.suptitle(f"H1 cycle geometry: {home} vs {away}", fontsize=12)
    fig.tight_layout()

    out_pdf = FIGURES_DIR / "fig2_cycle_geometry.pdf"
    out_png = FIGURES_DIR / "fig2_cycle_geometry.png"
    fig.savefig(out_pdf, dpi=150, bbox_inches="tight")
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)

    meta = {
        "individual_frame_idx": ind_idx,
        "tactical_frame_idx": tac_idx,
        "sampling_step": step,
        "n_frames_analysed": n_sample,
        "individual_max_persistence_m": round(p_ind, 3),
        "tactical_max_persistence_m": round(p_tac, 3),
    }
    with open(OUTPUT_DIR / "figure_cycle_geometry.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Wrote {out_pdf}")
