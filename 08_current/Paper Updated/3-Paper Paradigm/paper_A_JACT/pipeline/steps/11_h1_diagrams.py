#!/usr/bin/env python3
"""Step 11: scale-separated H1 birth–death display (Figure 4).

Primary-match uniform 150-frame sample. Individual and tactical levels
are never superimposed. Panels (a) and (b) are birth–death diagrams
(same diagonal convention as Figure 1e). Panel (c) is filtration
lifetime p = death − birth, in metres of the Vietoris–Rips parameter,
not clock time.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402
from figure_style import (  # noqa: E402
    STYLE,
    add_panel_letter,
    apply_rcparams,
    export_figure,
)

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))
sys.path.insert(0, str(REPO / "02_tda_core"))

from primary_match_skillcorner_analysis import (  # noqa: E402
    VALIDATED_CUTOFFS,
    ensure_match_assets,
    h1_at_cutoff,
    load_tracking_data,
)

TEXT = STYLE.text
IND_COL = STYLE.individual
TAC_COL = STYLE.tactical
DIAG_COL = STYLE.muted
MARK = STYLE.mark


def finite_pairs(h1: np.ndarray) -> np.ndarray:
    """Return finite (birth, death, p) rows."""
    if h1 is None or len(h1) == 0:
        return np.empty((0, 3))
    dgm = np.asarray(h1, dtype=float)
    mask = np.isfinite(dgm[:, 0]) & np.isfinite(dgm[:, 1])
    dgm = dgm[mask]
    if len(dgm) == 0:
        return np.empty((0, 3))
    p = dgm[:, 1] - dgm[:, 0]
    keep = p > 0
    dgm = dgm[keep]
    p = p[keep]
    if len(dgm) == 0:
        return np.empty((0, 3))
    return np.column_stack([dgm[:, 0], dgm[:, 1], p])


def collect_bars(sample: list, cutoff: float) -> tuple[list[dict], list[np.ndarray]]:
    rows: list[dict] = []
    per_frame: list[np.ndarray] = []
    for i, fr in enumerate(sample):
        _, h1, _, _ = h1_at_cutoff(fr["positions"], cutoff)
        triples = finite_pairs(h1)
        per_frame.append(triples)
        for birth, death, p in triples:
            rows.append(
                {
                    "sample_idx": i,
                    "birth": float(birth),
                    "death": float(death),
                    "p": float(p),
                }
            )
    return rows, per_frame


def plot_diagram(
    ax, triples: np.ndarray, marked_p: float, colour: str, letter: str,
    loc: str = "northwest",
    xy: tuple[float, float] | None = None,
) -> None:
    """Birth–death diagram. The diagonal is death = birth."""
    ax.set_xlabel("Birth (m)")
    ax.set_ylabel("Death (m)")
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(TEXT)
    if len(triples) == 0:
        ax.text(0.5, 0.5, "no finite $H_1$", ha="center", va="center", transform=ax.transAxes)
        add_panel_letter(ax, letter, loc=loc, xy=xy)
        return
    births = triples[:, 0]
    deaths = triples[:, 1]
    lo = float(min(births.min(), deaths.min()))
    hi = float(max(births.max(), deaths.max()))
    pad = 0.08 * (hi - lo) if hi > lo else 1.0
    lo -= pad
    hi += pad
    ax.plot([lo, hi], [lo, hi], color=DIAG_COL, lw=0.9, zorder=1)
    ax.scatter(births, deaths, s=36, c=colour, edgecolors="white", linewidths=0.4, zorder=3)
    idx = int(np.argmax(triples[:, 2]))
    ax.scatter(
        [triples[idx, 0]],
        [triples[idx, 1]],
        s=90,
        facecolors="none",
        edgecolors=MARK,
        linewidths=1.6,
        zorder=4,
    )
    offset = (8, -14) if loc == "northeast" else (8, 8)
    ax.annotate(
        rf"$p={marked_p:.3f}$ m",
        (triples[idx, 0], triples[idx, 1]),
        textcoords="offset points",
        xytext=offset,
        fontsize=STYLE.fs_tick,
        color=TEXT,
    )
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal", adjustable="box")
    add_panel_letter(ax, letter, loc=loc, xy=xy)


def plot_lifetime_tracks(ax, ind_p: np.ndarray, tac_p: np.ndarray, mean_ind: float, mean_tac: float) -> None:
    n_ind = len(ind_p)
    n_tac = len(tac_p)
    # Two tracks sharing the lifetime axis. Individual above, tactical below.
    gap = 4
    y_ind = np.arange(n_ind, dtype=float)
    y_tac = np.arange(n_tac, dtype=float) - n_tac - gap
    order_ind = np.argsort(ind_p)
    order_tac = np.argsort(tac_p)
    for y, p in zip(y_ind, ind_p[order_ind]):
        ax.plot([0, p], [y, y], color=IND_COL, lw=0.7, solid_capstyle="butt")
    for y, p in zip(y_tac, tac_p[order_tac]):
        ax.plot([0, p], [y, y], color=TAC_COL, lw=1.1, solid_capstyle="butt")
    ax.axvline(mean_ind, color=IND_COL, ls="--", lw=1.0, zorder=2, label=rf"individual $\bar{{p}}={mean_ind:.3f}$ m")
    ax.axvline(mean_tac, color=TAC_COL, ls="--", lw=1.0, zorder=2, label=rf"tactical $\bar{{p}}={mean_tac:.3f}$ m")
    ax.legend(
        frameon=False,
        loc="center right",
        bbox_to_anchor=(0.99, 0.62),
    )
    ymax = n_ind + 80
    ymin = float(y_tac.min() - 10)
    ax.set_ylim(ymin, ymax)
    ax.set_yticks(
        [
            (n_ind - 1) / 2 if n_ind else 0,
            (y_tac[0] + y_tac[-1]) / 2 if n_tac else -gap,
        ]
    )
    ax.set_yticklabels([f"Individual ($n={n_ind}$)", f"Tactical ($n={n_tac}$)"])
    ax.set_xlabel(r"Filtration lifetime $p$ (m)")
    ax.set_xlim(left=0)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(TEXT)
    add_panel_letter(ax, "c")


def main() -> None:
    ensure_dirs()
    cfg = load_config()
    ensure_match_assets()
    frames, _, _ = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]
    frame_idx = cfg["figures"]["individual_frame_idx"]
    d_ind = float(VALIDATED_CUTOFFS["individual"])
    d_tac = float(VALIDATED_CUTOFFS["tactical"])

    ind_rows, ind_frames = collect_bars(sample, d_ind)
    tac_rows, tac_frames = collect_bars(sample, d_tac)

    csv_path = OUTPUT_DIR / "h1_bars_primary.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["sample_idx", "level", "cutoff_m", "birth", "death", "p"]
        )
        writer.writeheader()
        for row in ind_rows:
            writer.writerow({**row, "level": "individual", "cutoff_m": d_ind})
        for row in tac_rows:
            writer.writerow({**row, "level": "tactical", "cutoff_m": d_tac})

    ind_p = np.array([r["p"] for r in ind_rows], dtype=float)
    tac_p = np.array([r["p"] for r in tac_rows], dtype=float)
    mean_ind = float(ind_p.mean()) if len(ind_p) else float("nan")
    mean_tac = float(tac_p.mean()) if len(tac_p) else float("nan")

    frame_ind = ind_frames[frame_idx]
    frame_tac = tac_frames[frame_idx]
    mark_ind = float(frame_ind[:, 2].max()) if len(frame_ind) else float("nan")
    mark_tac = float(frame_tac[:, 2].max()) if len(frame_tac) else float("nan")

    apply_rcparams()
    fig = plt.figure(figsize=(10.2, 8.4))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1.05, 1.25], hspace=0.32, wspace=0.28)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])
    plot_diagram(ax_a, frame_ind, mark_ind, IND_COL, "a")
    plot_diagram(
        ax_b, frame_tac, mark_tac, TAC_COL, "b",
        loc="northeast", xy=(0.93, 0.86),
    )
    plot_lifetime_tracks(ax_c, ind_p, tac_p, mean_ind, mean_tac)
    out_pdf = FIGURES_DIR / "fig4_h1_diagrams.pdf"
    out_png = FIGURES_DIR / "fig4_h1_diagrams.png"
    export_figure(fig, out_pdf, out_png, bbox_inches="tight")

    meta = {
        "individual_frame_idx": frame_idx,
        "n_frames": n_sample,
        "sampling_step": step,
        "n_individual_bars": int(len(ind_p)),
        "n_tactical_bars": int(len(tac_p)),
        "mean_p_individual": round(mean_ind, 3),
        "mean_p_tactical": round(mean_tac, 3),
        "frame95_p_individual": round(mark_ind, 3),
        "frame95_p_tactical": round(mark_tac, 3),
        "max_p_individual": round(float(ind_p.max()), 3) if len(ind_p) else None,
        "max_p_tactical": round(float(tac_p.max()), 3) if len(tac_p) else None,
    }
    with open(OUTPUT_DIR / "figure_h1_diagrams.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Wrote {out_pdf}")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
