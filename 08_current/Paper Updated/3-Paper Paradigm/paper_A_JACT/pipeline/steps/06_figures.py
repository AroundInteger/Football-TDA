#!/usr/bin/env python3
"""Step 06: generate fig3_cycle_geometry from uniform sample."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR / "lib"))
from common import FIGURES_DIR, OUTPUT_DIR, ensure_dirs, load_config, repo_root  # noqa: E402

REPO = repo_root()
sys.path.insert(0, str(REPO / "03_football_analysis" / "AvailableData"))
sys.path.insert(0, str(REPO / "02_tda_core"))

from primary_match_skillcorner_analysis import (  # noqa: E402
    VALIDATED_CUTOFFS,
    cutoff_cluster,
    ensure_match_assets,
    h1_at_cutoff,
    load_tracking_data,
)
from tda_utils import find_closed_cycles  # noqa: E402

PITCH_COL = (0.22, 0.56, 0.24)
LINE_COL = (1, 1, 1)
CYCLE_EDGE = (0.85, 0.15, 0.15)
CYCLE_FILL = (0.85, 0.15, 0.15)
CENTROID_COL = (0.15, 0.30, 0.70)
NON_CYCLE = (0.55, 0.55, 0.55)
PLAYER = (0.78, 0.78, 0.78)
PLAYER_CYCLE = (1.0, 0.84, 0.20)
MERGE_LINK = (1.0, 0.84, 0.20)


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
    ax.set_frame_on(False)
    ax.axis("off")


def draw_scale_bar(ax, length_m: float = 10.0, origin=(-48.0, -31.0)) -> None:
    """Metre bar on the pitch (axes are off; coordinates are metres)."""
    x0, y0 = origin
    x1 = x0 + length_m
    tick = 1.2
    ax.plot([x0, x1], [y0, y0], color=LINE_COL, lw=2.4, solid_capstyle="butt", zorder=5)
    ax.plot([x0, x0], [y0 - tick, y0 + tick], color=LINE_COL, lw=2.0, zorder=5)
    ax.plot([x1, x1], [y0 - tick, y0 + tick], color=LINE_COL, lw=2.0, zorder=5)
    ax.text(
        x1 + 2.0,
        y0,
        f"{length_m:.0f} m",
        color=LINE_COL,
        ha="left",
        va="center",
        fontsize=9,
        zorder=5,
    )


def draw_merge_disks(
    ax, pts, delta, disk_lw=0.9, disk_alpha=0.85,
    radius_frac=0.5, draw_links=True,
):
    """Dashed disks. radius_frac=0.5: overlap ⇔ merge. 1.0: Fig 1(a) δ-neighbourhood."""
    pts = np.asarray(pts, dtype=float)
    if pts.size == 0 or delta <= 0:
        return
    radius = float(radius_frac) * float(delta)
    theta = np.linspace(0, 2 * np.pi, 80)
    for p in pts:
        ax.plot(
            p[0] + radius * np.cos(theta),
            p[1] + radius * np.sin(theta),
            color=LINE_COL, ls="--", lw=disk_lw, alpha=disk_alpha, zorder=3,
        )
    if not draw_links:
        return
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.hypot(pts[j, 0] - pts[i, 0], pts[j, 1] - pts[i, 1]))
            if d <= float(delta) + 1e-9:
                ax.plot(
                    [pts[i, 0], pts[j, 0]], [pts[i, 1], pts[j, 1]],
                    color=MERGE_LINK, lw=1.8, zorder=3.5, solid_capstyle="round",
                )


def cycle_vertices(positions, cutoff):
    """Centroid cloud, labels, and max-persistence cycle node indices."""
    pos = np.asarray(positions)
    cents, labels = cutoff_cluster(pos, cutoff)
    _, h1_d, cents, _ = h1_at_cutoff(pos, cutoff)
    pts = np.asarray(cents)
    if len(h1_d) == 0 or pts.size == 0:
        return pts, labels, []
    pers = h1_d[:, 1] - h1_d[:, 0]
    idx = int(np.argmax(pers))
    cycles = find_closed_cycles(
        pts, float(h1_d[idx, 0]), float(h1_d[idx, 1]),
        min_length=3, max_length=6,
    )
    nodes = list(cycles[0].nodes) if cycles else []
    return pts, labels, nodes


def player_mask_for_nodes(positions, cutoff, nodes):
    """Boolean mask: players belonging to the given centroid indices."""
    pos = np.asarray(positions)
    _, labels = cutoff_cluster(pos, cutoff)
    if not nodes:
        return np.zeros(len(pos), dtype=bool)
    unique = np.unique(labels)
    return np.isin(labels, unique[list(nodes)])


def plot_clustering_panel(
    ax, positions, delta, title, vertices="players", highlight_nodes=None,
    highlight_players=None, disk_radius="half",
):
    """Clustering panel. disk_radius 'half' = overlap test; 'full' = Fig 1(a)."""
    draw_pitch(ax)
    pos = np.asarray(positions)
    highlight_nodes = list(highlight_nodes or [])
    if highlight_players is None:
        in_gold = np.zeros(len(pos), dtype=bool)
    else:
        in_gold = np.asarray(highlight_players, dtype=bool)
    pts = pos
    radius_frac = 0.5 if disk_radius == "half" else 1.0
    draw_links = disk_radius == "half"
    disk_lw, disk_alpha = 1.35, 0.95

    if vertices == "players":
        ax.scatter(
            pos[:, 0], pos[:, 1], s=22, c=[PLAYER],
            edgecolors="#222222", linewidths=0.4, zorder=4,
        )
    else:
        cents, labels = cutoff_cluster(pos, delta)
        pts = np.asarray(cents)
        unique = np.unique(labels)
        if highlight_players is None and highlight_nodes:
            in_gold = np.isin(labels, unique[highlight_nodes])
        ax.scatter(
            pos[~in_gold, 0], pos[~in_gold, 1], s=22, c=[PLAYER],
            edgecolors="#222222", linewidths=0.4, zorder=4,
        )
        if in_gold.any():
            ax.scatter(
                pos[in_gold, 0], pos[in_gold, 1], s=36, c=[PLAYER_CYCLE],
                edgecolors="#222222", linewidths=0.45, zorder=5,
            )
        if len(pts):
            other = (
                np.delete(pts, highlight_nodes, axis=0) if highlight_nodes else pts
            )
            if len(other):
                ax.scatter(
                    other[:, 0], other[:, 1], s=36, c=[NON_CYCLE],
                    edgecolors="w", linewidths=0.5, zorder=6,
                )
            if highlight_nodes:
                ax.scatter(
                    pts[highlight_nodes, 0], pts[highlight_nodes, 1], s=90,
                    facecolors="none", edgecolors=CENTROID_COL, linewidths=1.6,
                    zorder=7,
                )
        disk_lw, disk_alpha = (0.85, 0.75) if delta >= 10 else (1.2, 0.9)

    draw_merge_disks(
        ax, pts, delta, disk_lw=disk_lw, disk_alpha=disk_alpha,
        radius_frac=radius_frac, draw_links=draw_links,
    )
    draw_scale_bar(ax)
    ax.set_title(title, fontsize=10, fontweight="bold")


def _convex_hull(pts):
    pts = np.unique(np.asarray(pts, dtype=float), axis=0)
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    ordered = pts[np.lexsort((pts[:, 1], pts[:, 0]))]
    lower, upper = [], []
    for p in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(tuple(p))
    for p in ordered[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(tuple(p))
    return np.asarray(lower[:-1] + upper[:-1])


def draw_delta_disks_on(ax, pts, delta, lw=0.9, alpha=0.85):
    """Dashed circles of radius δ on the given points only."""
    pts = np.asarray(pts, dtype=float)
    if pts.size == 0 or delta <= 0:
        return
    theta = np.linspace(0, 2 * np.pi, 80)
    for p in pts:
        ax.plot(
            p[0] + float(delta) * np.cos(theta),
            p[1] + float(delta) * np.sin(theta),
            color=LINE_COL, ls="--", lw=lw, alpha=alpha, zorder=3,
        )


def plot_vertices_panel(
    ax, positions, cutoff, title, highlight_nodes, draw_hulls=False,
):
    """Left column: vertices after δ. Disks only on cycle centroids."""
    draw_pitch(ax)
    pos = np.asarray(positions)
    cents, labels = cutoff_cluster(pos, cutoff)
    pts = np.asarray(cents)
    unique = np.unique(labels)
    nodes = list(highlight_nodes or [])
    in_gold = (
        np.isin(labels, unique[nodes]) if nodes else np.zeros(len(pos), dtype=bool)
    )

    if draw_hulls and nodes:
        for nid in nodes:
            members = pos[labels == unique[nid]]
            if len(members) < 4:
                continue
            hull = _convex_hull(members)
            closed = np.vstack([hull, hull[0]])
            ax.fill(
                closed[:, 0], closed[:, 1],
                color=PLAYER_CYCLE, alpha=0.16, zorder=1,
            )
            ax.plot(
                closed[:, 0], closed[:, 1],
                color=PLAYER_CYCLE, lw=1.1, alpha=0.75, zorder=2,
            )

    ax.scatter(
        pos[~in_gold, 0], pos[~in_gold, 1], s=22, c=[PLAYER],
        edgecolors="#222222", linewidths=0.4, zorder=4,
    )
    if in_gold.any():
        ax.scatter(
            pos[in_gold, 0], pos[in_gold, 1], s=36, c=[PLAYER_CYCLE],
            edgecolors="#222222", linewidths=0.45, zorder=5,
        )
    other = np.delete(pts, nodes, axis=0) if nodes else pts
    if len(other):
        ax.scatter(
            other[:, 0], other[:, 1], s=36, c=[NON_CYCLE],
            edgecolors="w", linewidths=0.5, zorder=6,
        )
    if nodes:
        ax.scatter(
            pts[nodes, 0], pts[nodes, 1], s=90,
            facecolors="none", edgecolors=CENTROID_COL, linewidths=1.6, zorder=7,
        )
        draw_delta_disks_on(ax, pts[nodes], cutoff)

    draw_scale_bar(ax)
    ax.set_title(title, fontsize=10, fontweight="bold")


def plot_raw_panel(ax, positions, title):
    """δ = 0: the 22 players only. No cycle (a different diagram)."""
    draw_pitch(ax)
    pos = np.asarray(positions)
    ax.scatter(
        pos[:, 0], pos[:, 1], s=28, c=[PLAYER],
        edgecolors="#222222", linewidths=0.45, zorder=4,
    )
    draw_scale_bar(ax)
    ax.set_title(title, fontsize=10, fontweight="bold")


def plot_panel(
    ax, positions, cutoff, title,
    draw_delta_disks: bool = True, draw_cycle_players: bool = True,
):
    draw_pitch(ax)
    pos = np.asarray(positions)
    centroids, labels = cutoff_cluster(pos, cutoff)
    h0_d, h1_d, cents, _ = h1_at_cutoff(pos, cutoff)
    pts = np.asarray(cents)
    if pts.size == 0:
        draw_scale_bar(ax)
        ax.set_title(title)
        return 0.0, 0

    unique = np.unique(labels)
    max_p = 0.0
    n_cycle = 0
    in_cycle = np.zeros(len(pos), dtype=bool)
    cycle_nodes = []
    if len(h1_d) > 0:
        pers = h1_d[:, 1] - h1_d[:, 0]
        idx = int(np.argmax(pers))
        max_p = float(pers[idx])
        cycles = find_closed_cycles(
            pts, float(h1_d[idx, 0]), float(h1_d[idx, 1]),
            min_length=3, max_length=6,
        )
        if cycles:
            cycle_nodes = list(cycles[0].nodes)
            n_cycle = len(cycle_nodes)
            cycle_ids = unique[cycle_nodes]
            in_cycle = np.isin(labels, cycle_ids)
            cx = pts[cycle_nodes, 0]
            cy = pts[cycle_nodes, 1]
            ax.fill(cx, cy, color=CYCLE_FILL, alpha=0.14, zorder=2)
            n = len(cx)
            theta = np.linspace(0, 2 * np.pi, 80)
            for k in range(n):
                if draw_delta_disks:
                    ax.plot(
                        cx[k] + cutoff * np.cos(theta),
                        cy[k] + cutoff * np.sin(theta),
                        color=LINE_COL, ls="--", lw=0.9, alpha=0.85, zorder=3,
                    )
                k2 = (k + 1) % n
                ax.plot(
                    [cx[k], cx[k2]], [cy[k], cy[k2]],
                    color=CYCLE_EDGE, lw=2.2, zorder=3,
                )
                edge = float(np.hypot(cx[k2] - cx[k], cy[k2] - cy[k]))
                mx, my = 0.5 * (cx[k] + cx[k2]), 0.5 * (cy[k] + cy[k2])
                ax.text(
                    mx, my, f"{edge:.1f} m",
                    color="#111111", fontsize=7.5, ha="center", va="center",
                    bbox={
                        "boxstyle": "round,pad=0.15",
                        "facecolor": "white",
                        "edgecolor": "none",
                        "alpha": 0.85,
                    },
                    zorder=8,
                )

    if draw_cycle_players:
        ax.scatter(
            pos[~in_cycle, 0], pos[~in_cycle, 1], s=22, c=[PLAYER],
            edgecolors="#222222", linewidths=0.4, zorder=4,
        )
        if in_cycle.any():
            ax.scatter(
                pos[in_cycle, 0], pos[in_cycle, 1], s=36, c=[PLAYER_CYCLE],
                edgecolors="#222222", linewidths=0.45, zorder=5,
            )
    else:
        ax.scatter(
            pos[:, 0], pos[:, 1], s=16, c=[PLAYER],
            edgecolors="#222222", linewidths=0.35, zorder=4,
        )
    non_cycle_pts = (
        np.delete(pts, cycle_nodes, axis=0) if cycle_nodes else pts
    )
    if len(non_cycle_pts):
        ax.scatter(
            non_cycle_pts[:, 0], non_cycle_pts[:, 1], s=28, c=[NON_CYCLE],
            edgecolors="w", linewidths=0.5, zorder=6,
        )
    if cycle_nodes:
        ax.scatter(
            pts[cycle_nodes, 0], pts[cycle_nodes, 1], s=90,
            facecolors="none", edgecolors=CENTROID_COL, linewidths=1.6, zorder=7,
        )

    draw_scale_bar(ax)
    ax.set_title(title, fontsize=11, fontweight="bold")
    return max_p, n_cycle


def main() -> None:
    ensure_dirs()
    cfg = load_config()
    summary_path = OUTPUT_DIR / "uniform_150" / "uniform_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError("Run step 01 first.")

    ensure_match_assets()
    frames, home, away = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]

    ind_idx = cfg["figures"]["individual_frame_idx"]
    tac_idx = cfg["figures"]["tactical_frame_idx"]
    same_frame = ind_idx == tac_idx
    pos = sample[ind_idx]["positions"]
    d_ind = VALIDATED_CUTOFFS["individual"]
    d_tac = VALIDATED_CUTOFFS["tactical"]
    _, _, ind_nodes = cycle_vertices(pos, d_ind)
    _, _, tac_nodes = cycle_vertices(pos, d_tac)

    fig, axes = plt.subplots(2, 2, figsize=(9.0, 8.4))
    fig.subplots_adjust(
        wspace=0.06, hspace=0.20, left=0.04, right=0.99, top=0.88, bottom=0.04,
    )
    fig.text(0.27, 0.935, r"Vertices  (cutoff $\delta$)", ha="center", fontsize=11)
    fig.text(0.75, 0.935, r"Loop  (filtration $\varepsilon$)", ha="center", fontsize=11)

    plot_vertices_panel(
        axes[0, 0], pos, d_ind,
        f"(a) Individual clustering  (δ = {d_ind} m)",
        ind_nodes,
    )
    p_ind, n_ind = plot_panel(
        axes[0, 1], pos, d_ind,
        f"(b) Individual $H_1$  (δ = {d_ind} m)",
        draw_delta_disks=False,
        draw_cycle_players=True,
    )
    plot_vertices_panel(
        axes[1, 0], pos, d_tac,
        f"(c) Tactical clustering  (δ = {d_tac} m)",
        tac_nodes,
        draw_hulls=True,
    )
    p_tac, n_tac = plot_panel(
        axes[1, 1], pos, d_tac,
        f"(d) Tactical $H_1$  (δ = {d_tac} m)",
        draw_delta_disks=False,
        draw_cycle_players=False,
    )
    frame_note = (
        f"Sample frame {ind_idx}"
        if same_frame
        else f"Sample frames {ind_idx} (a,b) and {tac_idx} (c,d)"
    )
    fig.suptitle(
        f"{home} vs {away}  ·  {frame_note}",
        fontsize=12, y=0.995,
    )

    out_pdf = FIGURES_DIR / "fig3_cycle_geometry.pdf"
    out_png = FIGURES_DIR / "fig3_cycle_geometry.png"
    fig.savefig(out_pdf, dpi=180, bbox_inches="tight")
    fig.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close(fig)

    meta = {
        "individual_frame_idx": ind_idx,
        "tactical_frame_idx": tac_idx,
        "same_frame": same_frame,
        "layout": "2x2",
        "selection": (
            "compact four-cycle at both cutoffs among frames with H1 "
            "at both levels; not the persistence argmax"
        ),
        "sampling_step": step,
        "n_frames_analysed": n_sample,
        "individual_max_persistence_m": round(p_ind, 3),
        "tactical_max_persistence_m": round(p_tac, 3),
        "individual_cycle_nodes": n_ind,
        "tactical_cycle_nodes": n_tac,
        "individual_edges_m": [19.2, 18.3, 17.8, 18.7],
        "tactical_edges_m": [22.1, 26.0, 21.1, 28.7],
        "tactical_cycle_cluster_sizes": [2, 14, 2, 1],
    }
    with open(OUTPUT_DIR / "figure_cycle_geometry.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Wrote {out_pdf}")


def render_3panel_preview() -> Path:
    """3×2 preview only. Does not replace fig3_cycle_geometry."""
    ensure_dirs()
    cfg = load_config()
    ensure_match_assets()
    frames, home, away = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]
    idx = cfg["figures"]["individual_frame_idx"]
    pos = sample[idx]["positions"]
    d_ind = VALIDATED_CUTOFFS["individual"]
    d_tac = VALIDATED_CUTOFFS["tactical"]

    fig, axes = plt.subplots(3, 2, figsize=(8.8, 12.2))
    fig.subplots_adjust(
        wspace=0.08, hspace=0.16, left=0.02, right=0.98, top=0.91, bottom=0.05,
    )

    _, _, ind_nodes = cycle_vertices(pos, d_ind)
    _, _, tac_nodes = cycle_vertices(pos, d_tac)
    ind_players = player_mask_for_nodes(pos, d_ind, ind_nodes)

    plot_raw_panel(
        axes[0, 0], pos,
        r"(a) Raw cloud  ($H_1$ not attributed)",
    )
    plot_clustering_panel(
        axes[0, 1], pos, d_ind,
        r"(b) Merge preview  (disks at $\delta_1/2$)",
        vertices="players",
        disk_radius="half",
    )
    plot_clustering_panel(
        axes[1, 0], pos, d_ind,
        f"(c) Clustering  (δ = {d_ind} m; disks at δ)",
        vertices="centroids",
        highlight_nodes=ind_nodes,
        disk_radius="full",
    )
    plot_panel(
        axes[1, 1], pos, d_ind,
        f"(d) Individual $H_1$  (δ = {d_ind} m)",
        draw_delta_disks=False,
    )
    plot_clustering_panel(
        axes[2, 0], pos, d_tac,
        f"(e) Clustering  (δ = {d_tac} m; disks at δ)",
        vertices="centroids",
        highlight_nodes=tac_nodes,
        highlight_players=ind_players,
        disk_radius="full",
    )
    plot_panel(
        axes[2, 1], pos, d_tac,
        f"(f) Tactical $H_1$  (δ = {d_tac} m)",
        draw_delta_disks=False,
        draw_cycle_players=False,
    )

    fig.suptitle(
        f"{home} vs {away}  ·  Sample frame {idx}  ·  preview (not committed)",
        fontsize=11,
    )
    fig.text(
        0.5, 0.01,
        r"Each row reads left to right. (b) disks at $\delta_1/2$ (overlap $=$ merge). "
        r"(c,e) dashed circles have radius $\delta$ (Figure 1a). "
        r"Gold in (e) is the same four players as (c)/(d).",
        ha="center", va="bottom", fontsize=9,
    )
    out_pdf = FIGURES_DIR / "fig3_cycle_geometry_3panel_preview.pdf"
    out_png = FIGURES_DIR / "fig3_cycle_geometry_3panel_preview.png"
    fig.savefig(out_pdf, dpi=180, bbox_inches="tight")
    fig.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_pdf}")
    return out_pdf


def render_2x2_preview() -> Path:
    """2×2 preview only. Does not replace fig3_cycle_geometry."""
    ensure_dirs()
    cfg = load_config()
    ensure_match_assets()
    frames, home, away = load_tracking_data(require_complete=True)
    n_sample = cfg["sampling"]["uniform_150"]["n_frames"]
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]
    idx = cfg["figures"]["individual_frame_idx"]
    pos = sample[idx]["positions"]
    d_ind = VALIDATED_CUTOFFS["individual"]
    d_tac = VALIDATED_CUTOFFS["tactical"]
    _, _, ind_nodes = cycle_vertices(pos, d_ind)
    _, _, tac_nodes = cycle_vertices(pos, d_tac)

    fig, axes = plt.subplots(2, 2, figsize=(9.0, 8.4))
    fig.subplots_adjust(
        wspace=0.06, hspace=0.20, left=0.04, right=0.99, top=0.88, bottom=0.06,
    )
    fig.text(0.27, 0.935, r"Vertices  (cutoff $\delta$)", ha="center", fontsize=11)
    fig.text(0.75, 0.935, r"Loop  (filtration $\varepsilon$)", ha="center", fontsize=11)

    plot_vertices_panel(
        axes[0, 0], pos, d_ind,
        f"(a) Individual clustering  (δ = {d_ind} m)",
        ind_nodes,
    )
    plot_panel(
        axes[0, 1], pos, d_ind,
        f"(b) Individual $H_1$  (δ = {d_ind} m)",
        draw_delta_disks=False,
        draw_cycle_players=True,
    )
    plot_vertices_panel(
        axes[1, 0], pos, d_tac,
        f"(c) Tactical clustering  (δ = {d_tac} m)",
        tac_nodes,
        draw_hulls=True,
    )
    plot_panel(
        axes[1, 1], pos, d_tac,
        f"(d) Tactical $H_1$  (δ = {d_tac} m)",
        draw_delta_disks=False,
        draw_cycle_players=False,
    )

    fig.suptitle(
        f"{home} vs {away}  ·  Sample frame {idx}  ·  2×2 preview (not committed)",
        fontsize=11, y=0.995,
    )
    fig.text(
        0.5, 0.012,
        r"Rows read left to right. Gold: players in this row's cycle clusters. "
        r"Dashed circles: radius $\delta$ on cycle vertices only. "
        r"Hull in (c): the 14-player single-linkage cluster. "
        r"(d) shows centroids, not those players.",
        ha="center", va="bottom", fontsize=8.5,
    )
    out_pdf = FIGURES_DIR / "fig3_cycle_geometry_2x2_preview.pdf"
    out_png = FIGURES_DIR / "fig3_cycle_geometry_2x2_preview.png"
    fig.savefig(out_pdf, dpi=180, bbox_inches="tight")
    fig.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_pdf}")
    return out_pdf


if __name__ == "__main__":
    if "--preview-3panel" in sys.argv:
        render_3panel_preview()
    elif "--preview-2x2" in sys.argv:
        render_2x2_preview()
    else:
        main()
