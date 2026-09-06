#!/usr/bin/env python3
"""Generate Figure 1: Methods pipeline schematic (Sections 2.2, 2.4, 2.5).

Four equal-sized panels: step label above each box; schematic inside a fixed
viewport. Figure width matches A4 \\textwidth (16 cm); labels are 10 pt at
that scale. Explanatory prose lives in the LaTeX caption.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from scipy.spatial import ConvexHull

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, ensure_dirs  # noqa: E402
from fig1_layout import Fig1Layout, load_layout  # noqa: E402

TEXTWIDTH_IN = 16.0 / 2.54
FONT_PT = 10

ARROW = "#333333"
TEXT = "#222222"
LOOP = "#C62828"
EDGE = "#90A4AE"
PANEL_BG = "#FAFAFA"
BORDER = "#CCCCCC"
NON_CYCLE = "#546E7A"
GRAPH_EDGE = "#B0BEC5"

CLUSTER_PALETTE = ["#43A047", "#1E88E5", "#FB8C00", "#8E24AA", "#00897B"]

N_PANELS = 4
MARGIN_L = 0.01
MARGIN_R = 0.01
PANEL_BOTTOM = 0.10
PANEL_TOP = 0.86
HEADER_Y = 0.905
ARROW_W = 0.048  # wide enough for visible arrow shafts between panels


DELTA_LS = (0, (4, 3, 1, 3))  # dashed δ-radius circles in panel (a)
DELTA_COLOR = "#757575"


def _schematic_clustering_layout(
    layout: Fig1Layout,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Four separated micro-clusters on $P(t)$; centroids from their means."""
    rng = np.random.default_rng(11)
    micro_centres = np.array([
        [-6.0,  7.0],
        [-1.0,  4.0],
        [-6.0, -1.0],
        [-1.0, -6.0],
    ])
    sizes = [4, 4, 4, 4]
    pts_parts, label_parts = [], []
    for i, (c, n) in enumerate(zip(micro_centres, sizes)):
        block = c + rng.normal(0, 0.72, size=(n, 2))
        pts_parts.append(block)
        label_parts.append(np.full(n, i + 1, dtype=int))
    pts = np.vstack(pts_parts)
    labels = np.concatenate(label_parts)
    cents = _centroids(pts, labels)
    return pts, labels, cents, layout.left_slots_array(), layout.right_slots_array()


def _centroids(pts: np.ndarray, labels: np.ndarray) -> np.ndarray:
    return np.array([pts[labels == k].mean(axis=0) for k in np.unique(labels)])


def _cluster_colours(n: int) -> list:
    return CLUSTER_PALETTE[:n]


def _filtration_positions(layout: Fig1Layout) -> tuple[np.ndarray, np.ndarray]:
    """Centre $P(t)$ slot geometry in panel (b); preserve relative layout from (a)."""
    mapped_raw = layout.left_slots_array()
    target = np.array([0.50, 0.48])
    shift = target - mapped_raw.mean(axis=0)
    return mapped_raw + shift, shift


def _fit_to_box(
    pts: np.ndarray,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    pad: float = 0.12,
) -> np.ndarray:
    lo = pts.min(axis=0)
    hi = pts.max(axis=0)
    span = np.maximum(hi - lo, 1e-9)
    centre = (lo + hi) / 2.0
    half = span / 2.0 / (1.0 - pad)
    out = (pts - centre) / half
    sx = (x1 - x0) / 2.0
    sy = (y1 - y0) / 2.0
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    out[:, 0] = out[:, 0] * sx + cx
    out[:, 1] = out[:, 1] * sy + cy
    return out


def _panel_rects() -> list[tuple[float, float, float, float]]:
    gap_total = (N_PANELS - 1) * ARROW_W
    avail = 1.0 - MARGIN_L - MARGIN_R - gap_total
    pw = avail / N_PANELS
    ph = PANEL_TOP - PANEL_BOTTOM
    rects, x = [], MARGIN_L
    for _ in range(N_PANELS):
        rects.append((x, PANEL_BOTTOM, pw, ph))
        x += pw + ARROW_W
    return rects


def _style_axes(ax) -> None:
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")


def _panel_header(fig, rect: tuple[float, float, float, float], letter: str, title: str) -> None:
    x, _y, _w, _h = rect
    fig.text(
        x + 0.006, HEADER_Y, rf"$\mathbf{{({letter})}}$  {title}",
        ha="left", va="bottom", fontsize=FONT_PT, color=TEXT,
    )


def _panel_border(ax) -> None:
    ax.add_patch(Rectangle(
        (0, 0), 1, 1, fill=False, edgecolor=BORDER, linewidth=0.8, zorder=0,
    ))


def _panel_clustering(
    ax,
    pts: np.ndarray,
    labels: np.ndarray,
    colours: list,
    layout: Fig1Layout,
) -> None:
    """(a) Separated micro-clusters on $P(t)$ with gap $<\\delta$; centroids on $\\tilde{P}(t)$."""
    _style_axes(ax)
    _panel_border(ax)

    rng = np.random.default_rng(11)
    left_slots = layout.left_slots_array()
    right_slots = layout.right_slots_array()
    delta_r = layout.delta_r
    local_scale = layout.local_scale

    for i, k in enumerate(np.unique(labels)):
        mask = labels == k
        local = pts[mask] - pts[mask].mean(axis=0)
        slot = left_slots[i]
        cloud = slot + local * local_scale + rng.normal(0, 0.003, size=local.shape)

        ax.add_patch(Circle(
            slot, delta_r, fill=False, edgecolor=DELTA_COLOR,
            linewidth=0.85, ls=DELTA_LS, zorder=1,
        ))

        colour = colours[k - 1]
        ax.scatter(
            cloud[:, 0], cloud[:, 1], s=20, c=[colour],
            edgecolors="white", linewidths=0.35, zorder=3,
        )

    i, j = layout.delta_bracket
    p, q = left_slots[i], left_slots[j]
    mid = (p + q) / 2
    ax.annotate(
        "", xy=(q[0] - 0.025, q[1] - 0.025), xytext=(p[0] + 0.025, p[1] + 0.025),
        arrowprops=dict(arrowstyle="<->", color=DELTA_COLOR, lw=0.85),
        zorder=2,
    )
    off = layout.delta_bracket_label_offset
    ax.text(mid[0] + off[0], mid[1] + off[1], r"$<\delta$",
            fontsize=FONT_PT, ha="center", va="top", color=DELTA_COLOR)

    ax.text(layout.label_pt[0], layout.label_pt[1], r"$P(t)$", fontsize=FONT_PT,
            ha="center", va="top", color=TEXT)

    for i, k in enumerate(np.unique(labels)):
        right_pt = right_slots[i]
        left_centre = left_slots[i]
        ax.plot(
            [left_centre[0], right_pt[0]], [left_centre[1], right_pt[1]],
            color=colours[k - 1], alpha=0.55, lw=1.0, ls="--", zorder=2,
        )
        ax.scatter(
            right_pt[0], right_pt[1], s=58, c=[colours[k - 1]], marker="D",
            edgecolors="white", linewidths=0.6, zorder=5,
        )

    ax.text(layout.label_pt_tilde[0], layout.label_pt_tilde[1], r"$\tilde{P}(t)$",
            fontsize=FONT_PT, ha="center", va="top", color=TEXT)


def _panel_filtration(
    ax,
    cents: np.ndarray,
    labels: np.ndarray,
    colours: list,
    eps: float,
    layout: Fig1Layout,
) -> None:
    """(b) VR filtration on $\\tilde{P}(t)$ at fixed centroid positions (same layout as (a))."""
    _style_axes(ax)
    _panel_border(ax)

    mapped, shift = _filtration_positions(layout)
    pair_d = [
        float(np.linalg.norm(mapped[i] - mapped[j]))
        for i in range(len(mapped))
        for j in range(i + 1, len(mapped))
    ]
    data_d = np.linalg.norm(cents[:, None, :] - cents[None, :, :], axis=2)
    raw_span = float(np.max(cents.max(axis=0) - cents.min(axis=0)))
    panel_span = float(max(pair_d))
    eps_draw = eps / max(raw_span, 1e-9) * panel_span * layout.eps_scale

    for c in mapped:
        ax.add_patch(Circle(
            c, eps_draw, facecolor="#FFE0B2", edgecolor="#EF6C00",
            linewidth=0.6, alpha=0.32, zorder=1,
        ))
    segs = []
    for i in range(len(mapped)):
        for j in range(i + 1, len(mapped)):
            if data_d[i, j] <= eps * 1.001:
                segs.append([mapped[i], mapped[j]])
    if segs:
        ax.add_collection(LineCollection(segs, colors=EDGE, linewidths=0.9, zorder=2))

    for i, k in enumerate(np.unique(labels)):
        ax.scatter(
            mapped[i, 0], mapped[i, 1], s=46, c=[colours[k - 1]], marker="D",
            edgecolors="white", linewidths=0.6, zorder=4,
        )

    ax.text(
        layout.label_pt_tilde_b[0], layout.label_pt_tilde_b[1],
        r"$\tilde{P}(t)$", fontsize=FONT_PT, ha="center", va="top", color=TEXT,
    )
    eps_pt = (
        np.asarray(layout.eps_label_pos, dtype=float) + shift
        if layout.eps_label_pos is not None
        else mapped[layout.eps_label_index]
    )
    ax.text(
        eps_pt[0], eps_pt[1], r"$\varepsilon_{\max}$",
        fontsize=FONT_PT, color="#E65100", ha="center", va="center", zorder=5,
    )


def _panel_persistence(ax) -> None:
    _style_axes(ax)
    _panel_border(ax)
    inset = (0.22, 0.18, 0.88, 0.84)
    x0, y0, x1, y1 = inset

    def _map(u, v):
        return np.array([x0 + u * (x1 - x0), y0 + v * (y1 - y0)])

    ax.plot([x0, x1], [y0, y1], color="#9E9E9E", lw=0.9, zorder=2)
    pts = np.array([[0.20, 0.40], [0.35, 0.52], [0.50, 0.68], [0.24, 0.26]])
    xy = np.array([_map(u, v) for u, v in pts])
    ax.scatter(xy[:, 0], xy[:, 1], s=26, c=LOOP, zorder=3,
               edgecolors="white", linewidths=0.3)
    ax.text((x0 + x1) / 2, 0.07, "birth", fontsize=FONT_PT, ha="center", va="center", color=TEXT)
    ax.text(0.07, (y0 + y1) / 2, "death", fontsize=FONT_PT, ha="center", va="center",
            color=TEXT, rotation=90)


def _panel_cycle(
    ax,
    cents: np.ndarray,
    labels: np.ndarray,
    colours: list,
    cycle: list[int],
) -> None:
    _style_axes(ax)
    _panel_border(ax)
    box = (0.10, 0.12, 0.90, 0.88)
    x0, y0, x1, y1 = box
    mapped = _fit_to_box(cents, x0, x1, y0, y1, pad=0.20)

    segs = [[mapped[i], mapped[j]]
            for i in range(len(mapped)) for j in range(i + 1, len(mapped))]
    ax.add_collection(LineCollection(segs, colors=GRAPH_EDGE, linewidths=1.0, zorder=1))

    loop_pts = mapped[cycle]
    closed = np.vstack([loop_pts, loop_pts[0]])
    ax.fill(closed[:, 0], closed[:, 1], color=LOOP, alpha=0.12, zorder=2)
    ax.plot(closed[:, 0], closed[:, 1], color=LOOP, lw=2.0, zorder=3)

    cycle_set = set(cycle)
    unique = np.unique(labels)
    for i, k in enumerate(unique):
        p = mapped[i]
        colour = colours[k - 1]
        if i in cycle_set:
            ax.scatter(p[0], p[1], s=58, c=[LOOP], edgecolors="white",
                       linewidths=0.7, zorder=5)
        else:
            ax.scatter(p[0], p[1], s=40, c=[colour], edgecolors=NON_CYCLE,
                       linewidths=1.0, zorder=4)


def _inter_panel_arrows(fig, rects) -> None:
    y = PANEL_BOTTOM + (PANEL_TOP - PANEL_BOTTOM) / 2
    for r0, r1 in zip(rects[:-1], rects[1:]):
        x_start = r0[0] + r0[2] + 0.003
        x_end = r1[0] - 0.003
        fig.add_artist(FancyArrowPatch(
            (x_start, y), (x_end, y),
            transform=fig.transFigure,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.35,
            color=ARROW,
            shrinkA=0,
            shrinkB=0,
            zorder=10,
            clip_on=False,
        ))


def render_figure(layout: Fig1Layout | None = None) -> Path:
    """Build and save the full four-panel Figure~1 from *layout*."""
    ensure_dirs()
    layout = layout or load_layout()
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": FONT_PT,
        "mathtext.fontset": "dejavuserif",
    })

    pts, labels, cents, _left, _right = _schematic_clustering_layout(layout)
    colours = _cluster_colours(len(np.unique(labels)))

    if len(cents) >= 4:
        hull = ConvexHull(cents)
        cycle = list(hull.vertices[:4])
    else:
        cycle = list(range(len(cents)))

    d = np.linalg.norm(cents[:, None, :] - cents[None, :, :], axis=2)
    iu = np.triu_indices(len(cents), k=1)
    eps = float(np.percentile(d[iu], 60)) if len(cents) > 1 else 8.0

    fig_h = TEXTWIDTH_IN * 0.34
    fig = plt.figure(figsize=(TEXTWIDTH_IN, fig_h))
    rects = _panel_rects()

    titles = ["Clustering", "Filtration", r"$H_1$ diagram", "Closed cycle"]
    draw_fns = [
        lambda ax: _panel_clustering(ax, pts, labels, colours, layout),
        lambda ax: _panel_filtration(ax, cents, labels, colours, eps, layout),
        lambda ax: _panel_persistence(ax),
        lambda ax: _panel_cycle(ax, cents, labels, colours, cycle),
    ]

    for rect, letter, title, draw in zip(rects, "abcd", titles, draw_fns):
        ax = fig.add_axes(rect)
        draw(ax)
        _panel_header(fig, rect, letter, title)

    _inter_panel_arrows(fig, rects)

    out_pdf = FIGURES_DIR / "fig1_pipeline_schematic.pdf"
    out_png = FIGURES_DIR / "fig1_pipeline_schematic.png"
    fig.savefig(out_pdf, dpi=300)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    pw_in = TEXTWIDTH_IN * rects[0][2]
    ph_in = fig_h * (PANEL_TOP - PANEL_BOTTOM)
    print(f"Wrote {out_pdf} (panels {pw_in:.2f}×{ph_in:.2f} in, {FONT_PT} pt)")
    return out_pdf


def main() -> None:
    render_figure()


if __name__ == "__main__":
    main()
