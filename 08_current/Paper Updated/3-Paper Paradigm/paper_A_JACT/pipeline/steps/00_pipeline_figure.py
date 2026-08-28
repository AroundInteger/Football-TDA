#!/usr/bin/env python3
"""Generate Figure 1: Methods pipeline schematic (Sections 2.2, 2.4, 2.5).

Toy geometry only — no tracking data required. Vector PDF + PNG.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, FancyBboxPatch, Polygon
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial import ConvexHull

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, ensure_dirs  # noqa: E402

ARROW = "#333333"
TEXT = "#222222"
CLUSTER_FACE = "#E3F2FD"
FILT_FACE = "#FFF8E1"
CYCLE_FACE = "#F3E5F5"
PLAYER = "#37474F"
CENTROID = "#1565C0"
LOOP = "#C62828"
EDGE = "#90A4AE"


def _toy_cloud(seed: int = 4) -> np.ndarray:
    rng = np.random.default_rng(seed)
    centres = np.array([
        [-18.0, 8.0], [-6.0, -4.0], [8.0, 10.0], [20.0, -8.0], [4.0, -14.0],
    ])
    sizes = [5, 5, 4, 4, 4]
    pts = [c + rng.normal(0, 1.8, size=(n, 2)) for c, n in zip(centres, sizes)]
    return np.vstack(pts)


def _cluster(pts: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray]:
    z = linkage(pts, method="single")
    labels = fcluster(z, t=delta, criterion="distance")
    cents = np.array([pts[labels == k].mean(axis=0) for k in np.unique(labels)])
    return labels, cents


def _draw_box(ax, x, y, w, h, face, title, body, title_color):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=face, edgecolor=ARROW, linewidth=1.0, zorder=2,
    ))
    ax.text(x + w / 2, y + h - 0.22, title, ha="center", va="top",
            fontsize=8.5, fontweight="bold", color=title_color, zorder=3)
    ax.text(x + w / 2, y + 0.18, body, ha="center", va="bottom",
            fontsize=7.6, color=TEXT, zorder=3, linespacing=1.25)


def _flow_row(ax) -> None:
    ax.set_xlim(0, 16.2)
    ax.set_ylim(0, 2.15)
    ax.axis("off")
    boxes = [
        (0.15, 0.25, 2.85, 1.65, "#FAFAFA", "Point cloud",
         r"$P(t)$: 22 player" + "\npositions", TEXT),
        (3.35, 0.25, 2.85, 1.65, CLUSTER_FACE, r"§2.2 Clustering",
         r"single-linkage at $\delta$" + "\n" + r"$\rightarrow$ centroids $\tilde P$",
         "#1565C0"),
        (6.55, 0.25, 2.85, 1.65, FILT_FACE, r"§2.4 Filtration",
         r"VR on $\tilde P$; truncate" + "\n" + r"at adaptive $\varepsilon_{\max}$",
         "#E65100"),
        (9.75, 0.25, 2.85, 1.65, "#FFEBEE", r"$H_1$ diagram",
         "finite birth–death" + "\npairs", "#B71C1C"),
        (12.95, 0.25, 2.95, 1.65, CYCLE_FACE, r"§2.5 Cycle",
         "BFS graph cycle on" + "\nedges in [birth, death]",
         "#6A1B9A"),
    ]
    for b in boxes:
        _draw_box(ax, *b)
    for i in range(len(boxes) - 1):
        x1 = boxes[i][0] + boxes[i][2]
        x2 = boxes[i + 1][0]
        y = boxes[i][1] + boxes[i][3] / 2
        ax.annotate(
            "", xy=(x2 - 0.04, y), xytext=(x1 + 0.04, y),
            arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.35),
            zorder=1,
        )


def _panel_cluster(ax, pts: np.ndarray, labels: np.ndarray, cents: np.ndarray) -> None:
    ax.set_aspect("equal")
    ax.axis("off")
    colours = plt.cm.Set2(np.linspace(0, 1, labels.max()))
    for k in np.unique(labels):
        cloud = pts[labels == k]
        if len(cloud) >= 3:
            hull = ConvexHull(cloud)
            poly = Polygon(cloud[hull.vertices], closed=True,
                           facecolor=colours[k - 1], edgecolor="none", alpha=0.28)
            ax.add_patch(poly)
        elif len(cloud) == 2:
            ax.plot(cloud[:, 0], cloud[:, 1], color=colours[k - 1], lw=4, alpha=0.35)
        ax.scatter(cloud[:, 0], cloud[:, 1], s=22, c=[PLAYER], zorder=3)
    ax.scatter(cents[:, 0], cents[:, 1], s=70, c=CENTROID, marker="D",
               edgecolors="white", linewidths=0.6, zorder=4)
    ax.set_title(r"(a) Clustering at $\delta$ (Section 2.2)", fontsize=9, pad=4)


def _panel_filtration(ax, cents: np.ndarray, eps: float) -> None:
    ax.set_aspect("equal")
    ax.axis("off")
    for c in cents:
        ax.add_patch(Circle(c, eps, facecolor="#FFE0B2", edgecolor="#EF6C00",
                            linewidth=0.8, alpha=0.35, zorder=1))
        ax.add_patch(Circle(c, eps * 0.45, facecolor="#FFF3E0", edgecolor="#FFB74D",
                            linewidth=0.5, alpha=0.5, zorder=2))
    segs = []
    for i in range(len(cents)):
        for j in range(i + 1, len(cents)):
            if np.linalg.norm(cents[i] - cents[j]) <= eps:
                segs.append([cents[i], cents[j]])
    if segs:
        ax.add_collection(LineCollection(segs, colors=EDGE, linewidths=1.1, zorder=3))
    ax.scatter(cents[:, 0], cents[:, 1], s=70, c=CENTROID, marker="D",
               edgecolors="white", linewidths=0.6, zorder=4)
    ax.annotate(
        r"$\varepsilon_{\max}$",
        xy=(cents[0, 0] + eps * 0.7, cents[0, 1]),
        fontsize=8, color="#E65100",
    )
    ax.set_title(r"(b) Adaptive VR truncation (Section 2.4)", fontsize=9, pad=4)


def _panel_cycle(ax, cents: np.ndarray, cycle: list[int]) -> None:
    ax.set_aspect("equal")
    ax.axis("off")
    # complete graph faint
    segs = [[cents[i], cents[j]] for i in range(len(cents)) for j in range(i + 1, len(cents))]
    ax.add_collection(LineCollection(segs, colors="#ECEFF1", linewidths=0.6, zorder=1))
    loop_pts = cents[cycle]
    closed = np.vstack([loop_pts, loop_pts[0]])
    ax.fill(closed[:, 0], closed[:, 1], color=LOOP, alpha=0.12, zorder=2)
    ax.plot(closed[:, 0], closed[:, 1], color=LOOP, lw=2.2, zorder=3)
    ax.scatter(cents[:, 0], cents[:, 1], s=36, c="#B0BEC5", zorder=4)
    ax.scatter(loop_pts[:, 0], loop_pts[:, 1], s=80, c=LOOP, edgecolors="white",
               linewidths=0.7, zorder=5)
    ax.set_title(r"(c) Graph-cycle proxy (Section 2.5)", fontsize=9, pad=4)


def _mini_pd(ax) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.plot([0, 1], [0, 1], color="#9E9E9E", lw=0.9)
    pts = np.array([[0.18, 0.42], [0.32, 0.55], [0.48, 0.70], [0.22, 0.28]])
    ax.scatter(pts[:, 0], pts[:, 1], s=18, c=LOOP, zorder=3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"birth", fontsize=7, labelpad=1)
    ax.set_ylabel(r"death", fontsize=7, labelpad=1)
    ax.set_title(r"schematic $H_1$", fontsize=8, pad=2)
    for spine in ax.spines.values():
        spine.set_linewidth(0.6)


def main() -> None:
    ensure_dirs()
    pts = _toy_cloud()
    labels, cents = _cluster(pts, delta=8.0)
    # four-cycle on a convex quadrilateral of centroids, if available
    if len(cents) >= 4:
        hull = ConvexHull(cents)
        verts = list(hull.vertices[:4])
        if len(verts) < 4:
            verts = list(range(min(4, len(cents))))
        cycle = verts
    else:
        cycle = list(range(len(cents)))

    # filtration radius: mid-range pairwise so some edges appear
    d = np.linalg.norm(cents[:, None, :] - cents[None, :, :], axis=2)
    iu = np.triu_indices(len(cents), k=1)
    eps = float(np.percentile(d[iu], 60)) if len(cents) > 1 else 8.0

    fig = plt.figure(figsize=(11.2, 7.6))
    fig.suptitle("Multi-scale analysis pipeline", fontsize=12, fontweight="bold", y=0.98)

    gs = fig.add_gridspec(
        3, 4, height_ratios=[1.05, 2.15, 0.85],
        width_ratios=[1, 1, 1, 0.72],
        hspace=0.38, wspace=0.28,
        left=0.04, right=0.98, top=0.92, bottom=0.04,
    )
    ax_flow = fig.add_subplot(gs[0, :])
    _flow_row(ax_flow)

    ax_a = fig.add_subplot(gs[1, 0])
    ax_b = fig.add_subplot(gs[1, 1])
    ax_c = fig.add_subplot(gs[1, 2])
    ax_pd = fig.add_subplot(gs[1, 3])
    _panel_cluster(ax_a, pts, labels, cents)
    _panel_filtration(ax_b, cents, eps)
    _panel_cycle(ax_c, cents, cycle)
    _mini_pd(ax_pd)

    ax_note = fig.add_subplot(gs[2, :])
    ax_note.axis("off")
    ax_note.text(
        0.0, 0.7,
        r"Homology is computed on cluster centroids $\tilde{P}(t)$, not on the raw 22-player cloud.",
        fontsize=8.2, va="top", ha="left", color="#424242",
        transform=ax_note.transAxes,
    )
    ax_note.text(
        0.0, 0.38,
        r"$\varepsilon_{\max}=\max(P_{75}\{d(\bar{c}_i,\bar{c}_j)\},\max(5,2\delta))$ truncates the Vietoris--Rips parameter (equation (1)); it is not a new filtration. "
        r"The closed cycle is a geometric proxy for a persistence pair. Figure 2 shows the same cycle step on real tracking data.",
        fontsize=8.2, va="top", ha="left", color="#424242",
        transform=ax_note.transAxes,
    )

    out_pdf = FIGURES_DIR / "fig1_pipeline_schematic.pdf"
    out_png = FIGURES_DIR / "fig1_pipeline_schematic.png"
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_pdf}")


if __name__ == "__main__":
    main()
