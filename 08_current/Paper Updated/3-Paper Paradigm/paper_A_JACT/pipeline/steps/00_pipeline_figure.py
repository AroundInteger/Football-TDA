#!/usr/bin/env python3
"""Generate Figure 1: Methods pipeline schematic (Sections 2.2, 2.4, 2.5).

Bounded-domain TDA cartoon: clustering on a pitch, three-step
Vietoris--Rips growth on the centroids, birth--death diagram, barcode,
then a cycle proxy. Figure width matches A4 \\textwidth (16 cm).
Explanatory prose lives in the LaTeX caption.
"""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from scipy.spatial import ConvexHull

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, ensure_dirs  # noqa: E402
from fig1_layout import Fig1Layout, load_layout  # noqa: E402
from figure_style import (  # noqa: E402
    STYLE,
    TEXTWIDTH_IN,
    add_panel_letter,
    apply_rcparams,
    export_figure,
)

FONT_PT = STYLE.fs_tick

ARROW = "#333333"
TEXT = STYLE.text
LOOP = "#C62828"
EDGE = "#37474F"
PANEL_BG = "#FAFAFA"
BORDER = "#CCCCCC"
BALL_FACE = "#FFE0B2"
BALL_EDGE = "#EF6C00"
PITCH_COL = (0.22, 0.56, 0.24)
LINE_COL = (1.0, 1.0, 1.0)
# Okabe--Ito-ish, no green: clusters must read on the pitch.
CLUSTER_PALETTE = ["#F0E442", "#56B4E9", "#E69F00", "#CC79A7"]

DELTA_LS = (0, (4, 3, 1, 3))
DELTA_COLOR = "#ECEFF1"

# Crop to the play and the halfway line so the bound is visible
# without empty grass dominating the boxes.
PITCH_XLIM = (-48.0, 12.0)
PITCH_YLIM = (-28.0, 26.0)


# Schematic (birth, death) pairs shared by panels (e) and (f).
PD_PAIRS = np.array([
    [0.20, 0.40],
    [0.35, 0.52],
    [0.50, 0.68],
    [0.24, 0.26],
])


def _schematic_cloud() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Four groups on the left half of a pitch; centroids from their means."""
    rng = np.random.default_rng(11)
    centres = np.array([
        [-37.0,   8.5],
        [-18.0,   7.0],
        [-16.5, -14.0],
        [-36.0, -15.5],
    ])
    pts_parts, label_parts = [], []
    for i, c in enumerate(centres):
        ang = np.linspace(0.0, 2.0 * np.pi, 5)[:-1] + rng.uniform(-0.25, 0.25)
        rad = 3.4 + rng.normal(0.0, 0.35, size=4)
        block = np.column_stack([c[0] + rad * np.cos(ang), c[1] + rad * np.sin(ang)])
        pts_parts.append(block)
        label_parts.append(np.full(4, i + 1, dtype=int))
    pts = np.vstack(pts_parts)
    labels = np.concatenate(label_parts)
    cents = np.array([pts[labels == k].mean(axis=0) for k in np.unique(labels)])
    return pts, labels, cents


def _cluster_colours(n: int) -> list:
    return CLUSTER_PALETTE[:n]


def _pairwise(cents: np.ndarray) -> np.ndarray:
    return np.linalg.norm(cents[:, None, :] - cents[None, :, :], axis=2)


def _eps_stages(cents: np.ndarray) -> tuple[float, float, float]:
    """Three increasing ε on the centroids, truncated at ε_max.

    Chosen so the snapshots read: isolated balls; some edges; the hull
    closes (the usual TDA cartoon, after clustering).
    """
    d = _pairwise(cents)
    iu = np.triu_indices(len(cents), k=1)
    pair = d[iu]
    ordered = np.sort(pair)
    hull = ConvexHull(cents)
    hull_edges = []
    verts = list(hull.vertices) + [hull.vertices[0]]
    for i, j in zip(verts[:-1], verts[1:]):
        hull_edges.append(float(np.linalg.norm(cents[i] - cents[j])))
    # Balls of radius ε/2 meet when ε equals the pairwise distance.
    eps1 = 0.55 * float(ordered[0])
    eps2 = 1.02 * float(ordered[1])
    eps_max = 1.04 * max(hull_edges)
    return eps1, eps2, eps_max


def _draw_pitch(ax) -> None:
    ax.add_patch(Rectangle(
        (-52.5, -34), 105, 68,
        facecolor=PITCH_COL, edgecolor=LINE_COL, linewidth=0.9, zorder=0,
    ))
    ax.axvline(0, color=LINE_COL, lw=0.8, zorder=1)
    theta = np.linspace(0, 2 * np.pi, 80)
    ax.plot(9.15 * np.cos(theta), 9.15 * np.sin(theta),
            color=LINE_COL, lw=0.8, zorder=1)
    ax.set_xlim(*PITCH_XLIM)
    ax.set_ylim(*PITCH_YLIM)
    ax.set_aspect("equal", adjustable="box")
    ax.set_facecolor(PITCH_COL)
    ax.axis("off")


def _scale_bar(ax, origin=(-45.0, -24.0), length=10.0) -> None:
    x0, y0 = origin
    x1 = x0 + length
    ax.plot([x0, x1], [y0, y0], color=LINE_COL, lw=2.0, solid_capstyle="butt", zorder=6)
    ax.plot([x0, x0], [y0 - 1.0, y0 + 1.0], color=LINE_COL, lw=1.6, zorder=6)
    ax.plot([x1, x1], [y0 - 1.0, y0 + 1.0], color=LINE_COL, lw=1.6, zorder=6)
    ax.text(x1 + 1.6, y0, "10 m", color=LINE_COL, ha="left", va="center",
            fontsize=FONT_PT - 2, zorder=6)


def _draw_vr(ax, cents: np.ndarray, eps: float, colours: list, labels: np.ndarray) -> None:
    """Balls of radius ε/2; an edge when pairwise distance ≤ ε."""
    radius = 0.5 * eps
    d = _pairwise(cents)
    n = len(cents)
    for c in cents:
        ax.add_patch(Circle(
            c, radius, facecolor=BALL_FACE, edgecolor=BALL_EDGE,
            linewidth=0.6, alpha=0.45, zorder=2,
        ))
    segs = []
    for i, j in combinations(range(n), 2):
        if d[i, j] <= eps + 1e-9:
            segs.append([cents[i], cents[j]])
    if segs:
        ax.add_collection(LineCollection(segs, colors=EDGE, linewidths=1.05, zorder=3))
    for i, j, k in combinations(range(n), 3):
        if d[i, j] <= eps + 1e-9 and d[j, k] <= eps + 1e-9 and d[i, k] <= eps + 1e-9:
            tri = cents[[i, j, k]]
            ax.fill(tri[:, 0], tri[:, 1], color=LOOP, alpha=0.16, zorder=2)
    unique = np.unique(labels)
    for i, k in enumerate(unique):
        ax.scatter(
            cents[i, 0], cents[i, 1], s=44, c=[colours[k - 1]], marker="D",
            edgecolors="white", linewidths=0.55, zorder=5,
        )


def _panel_clustering(ax, pts, labels, colours, cents) -> None:
    """(a) Groups on $P(\\tilde t)$ with $\\delta$-disks; no centroid markers."""
    _draw_pitch(ax)
    _scale_bar(ax)
    delta_r = 7.0
    unique = np.unique(labels)
    for i, k in enumerate(unique):
        cloud = pts[labels == k]
        colour = colours[k - 1]
        ax.add_patch(Circle(
            cents[i], delta_r, fill=False, edgecolor=DELTA_COLOR,
            linewidth=0.9, ls=DELTA_LS, zorder=3,
        ))
        ax.scatter(
            cloud[:, 0], cloud[:, 1], s=48, c=[colour],
            edgecolors="#222222", linewidths=0.4, zorder=4,
        )
    gap = cents.mean(axis=0)
    ax.text(
        gap[0], gap[1], r"$<\delta$",
        fontsize=FONT_PT, ha="center", va="center", color=DELTA_COLOR, zorder=6,
    )
    ax.text(
        0.34, 0.97, r"$P(\tilde{t})$",
        transform=ax.transAxes,
        fontsize=FONT_PT, ha="center", va="top", color="white", zorder=6,
    )
    add_panel_letter(ax, "a", loc="northeast", fontsize=FONT_PT)


def _panel_filtration(ax, cents, labels, colours, eps, letter: str | None, eps_note: str) -> None:
    _draw_pitch(ax)
    _draw_vr(ax, cents, eps, colours, labels)
    ax.text(
        0.50, 0.07, eps_note,
        transform=ax.transAxes, fontsize=FONT_PT, ha="center", va="bottom",
        color="white", zorder=6,
    )
    if letter:
        add_panel_letter(ax, letter, loc="northeast", fontsize=FONT_PT)


def _panel_persistence(ax) -> None:
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.add_patch(Rectangle(
        (0, 0), 1, 1, fill=False, edgecolor=BORDER, linewidth=0.8, zorder=0,
    ))
    inset = (0.22, 0.18, 0.88, 0.84)
    x0, y0, x1, y1 = inset

    def _map(u, v):
        return np.array([x0 + u * (x1 - x0), y0 + v * (y1 - y0)])

    ax.plot([x0, x1], [y0, y1], color="#9E9E9E", lw=0.9, zorder=2)
    xy = np.array([_map(u, v) for u, v in PD_PAIRS])
    ax.scatter(xy[:, 0], xy[:, 1], s=28, c=LOOP, zorder=3,
               edgecolors="white", linewidths=0.3)
    ax.text((x0 + x1) / 2, 0.07, "birth", fontsize=FONT_PT, ha="center", va="center", color=TEXT)
    ax.text(0.07, (y0 + y1) / 2, "death", fontsize=FONT_PT, ha="center", va="center",
            color=TEXT, rotation=90)
    add_panel_letter(ax, "e", fontsize=FONT_PT)


def _panel_barcode(ax) -> None:
    """(f) The same finite $H_1$ pairs as (e), drawn as bars."""
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle(
        (0, 0), 1, 1, fill=False, edgecolor=BORDER, linewidth=0.8, zorder=0,
    ))
    pairs = PD_PAIRS[np.argsort(PD_PAIRS[:, 1] - PD_PAIRS[:, 0])]
    n = len(pairs)
    ys = np.linspace(0.24, 0.80, n)
    x0, x1 = 0.18, 0.90

    def _mx(u):
        return x0 + u * (x1 - x0)

    longest = int(np.argmax(pairs[:, 1] - pairs[:, 0]))
    for i, ((birth, death), y) in enumerate(zip(pairs, ys)):
        is_long = i == longest
        ax.plot(
            [_mx(birth), _mx(death)], [y, y],
            color=LOOP if is_long else EDGE,
            lw=2.4 if is_long else 1.6,
            solid_capstyle="butt", zorder=3,
        )
    ax.text(0.54, 0.07, r"$\varepsilon$", fontsize=FONT_PT, ha="center", va="center", color=TEXT)
    ax.text(0.07, 0.52, r"$H_1$", fontsize=FONT_PT, ha="center", va="center",
            color=TEXT, rotation=90)
    add_panel_letter(ax, "f", fontsize=FONT_PT)


def _panel_cycle(ax, pts, labels, cents, colours, cycle: list[int]) -> None:
    _draw_pitch(ax)
    _scale_bar(ax)
    ax.scatter(
        pts[:, 0], pts[:, 1], s=12, c="#D0D0D0",
        edgecolors="none", zorder=2, alpha=0.9,
    )
    segs = [[cents[i], cents[j]]
            for i in range(len(cents)) for j in range(i + 1, len(cents))]
    ax.add_collection(LineCollection(segs, colors="#B0BEC5", linewidths=0.9, zorder=3))
    loop_pts = cents[cycle]
    closed = np.vstack([loop_pts, loop_pts[0]])
    ax.fill(closed[:, 0], closed[:, 1], color=LOOP, alpha=0.16, zorder=4)
    ax.plot(closed[:, 0], closed[:, 1], color=LOOP, lw=2.0, zorder=5)
    cycle_set = set(cycle)
    unique = np.unique(labels)
    for i, k in enumerate(unique):
        if i in cycle_set:
            ax.scatter(
                cents[i, 0], cents[i, 1], s=52, c=[LOOP],
                edgecolors="white", linewidths=0.6, zorder=6,
            )
        else:
            ax.scatter(
                cents[i, 0], cents[i, 1], s=40, c=[colours[k - 1]], marker="D",
                edgecolors="white", linewidths=0.55, zorder=6,
            )
    add_panel_letter(ax, "g", loc="northeast", fontsize=FONT_PT)


def _arrow(fig, ax0, ax1) -> None:
    """Short arrow in figure coordinates between two axes."""
    b0 = ax0.get_position()
    b1 = ax1.get_position()
    y = 0.5 * (b0.y0 + b0.y1)
    fig.add_artist(FancyArrowPatch(
        (b0.x1 + 0.004, y), (b1.x0 - 0.004, y),
        transform=fig.transFigure,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.2,
        color=ARROW,
        shrinkA=0,
        shrinkB=0,
        zorder=10,
        clip_on=False,
    ))


def render_figure(layout: Fig1Layout | None = None) -> Path:
    """Build and save Figure~1.

    ``layout`` is kept so the old editor can still call export; the
    published geometry is a pitch schematic and does not read the YAML
    slots.
    """
    del layout  # unused; see docstring
    ensure_dirs()
    apply_rcparams()
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "dejavuserif",
    })

    pts, labels, cents = _schematic_cloud()
    colours = _cluster_colours(len(np.unique(labels)))
    hull = ConvexHull(cents)
    cycle = list(hull.vertices)
    eps1, eps2, eps_max = _eps_stages(cents)

    fig_h = TEXTWIDTH_IN * 0.70
    fig = plt.figure(figsize=(TEXTWIDTH_IN, fig_h))
    gs_top = GridSpec(
        1, 4, figure=fig,
        wspace=0.07,
        left=0.02, right=0.99, top=0.98, bottom=0.54,
    )
    ax_a = fig.add_subplot(gs_top[0, 0])
    ax_b1 = fig.add_subplot(gs_top[0, 1])
    ax_b2 = fig.add_subplot(gs_top[0, 2])
    ax_b3 = fig.add_subplot(gs_top[0, 3])

    # Square PD, barcode, and a pitch panel on the bottom row.
    bot_h = 0.40
    bot_y = 0.04
    pd_w = (bot_h * fig_h) / TEXTWIDTH_IN
    bc_w = pd_w * 1.12
    pitch_aspect = (PITCH_XLIM[1] - PITCH_XLIM[0]) / (PITCH_YLIM[1] - PITCH_YLIM[0])
    d_w = pd_w * pitch_aspect
    gap = 0.028
    total = pd_w + bc_w + d_w + 2 * gap
    x_e = 0.5 - total / 2
    x_f = x_e + pd_w + gap
    x_g = x_f + bc_w + gap
    ax_e = fig.add_axes([x_e, bot_y, pd_w, bot_h])
    ax_f = fig.add_axes([x_f, bot_y, bc_w, bot_h])
    ax_g = fig.add_axes([x_g, bot_y, d_w, bot_h])

    _panel_clustering(ax_a, pts, labels, colours, cents)
    _panel_filtration(ax_b1, cents, labels, colours, eps1, "b", r"$\varepsilon_1$")
    _panel_filtration(ax_b2, cents, labels, colours, eps2, "c", r"$\varepsilon_2$")
    _panel_filtration(ax_b3, cents, labels, colours, eps_max, "d", r"$\varepsilon_{\max}$")
    _panel_persistence(ax_e)
    _panel_barcode(ax_f)
    _panel_cycle(ax_g, pts, labels, cents, colours, cycle)

    fig.canvas.draw()
    _arrow(fig, ax_a, ax_b1)

    out_pdf = FIGURES_DIR / "fig1_pipeline_schematic.pdf"
    out_png = FIGURES_DIR / "fig1_pipeline_schematic.png"
    export_figure(fig, out_pdf, out_png)
    print(f"Wrote {out_pdf} ({TEXTWIDTH_IN:.2f}×{fig_h:.2f} in)")
    print(f"  schematic ε = {eps1:.2f}, {eps2:.2f}, {eps_max:.2f} m")
    return out_pdf


def main() -> None:
    load_layout()  # keep YAML present for the editor; geometry does not use it
    render_figure()


if __name__ == "__main__":
    main()
