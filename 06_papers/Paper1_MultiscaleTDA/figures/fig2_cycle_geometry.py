#!/usr/bin/env python3
"""
Generate Paper Figure 2: Geometric realisation of H1 loops at individual and tactical scales.

Two-panel figure on football pitch with cycle edges and shaded enclosed region.
Uses CSV data exported by export_data_for_matlab.py (fig1_* point files).

Run from Football-TDA root: python 06_papers/Paper1_MultiscaleTDA/figures/fig2_cycle_geometry.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parent

CYCLE_EDGE = (0.85, 0.15, 0.15)
CYCLE_FILL = (0.85, 0.15, 0.15)
FILL_ALPHA = 0.12
CENTROID_COL = (0.15, 0.30, 0.70)
NON_CYCLE = (0.55, 0.55, 0.55)
PITCH_COL = (0.22, 0.56, 0.24)
LINE_COL = (1, 1, 1)


def draw_pitch(ax):
    """Draw football pitch outline."""
    rect = plt.Rectangle((-52.5, -34), 105, 68, facecolor=PITCH_COL, edgecolor=LINE_COL, linewidth=1)
    ax.add_patch(rect)
    ax.axvline(0, color=LINE_COL, lw=1)
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(9.15 * np.cos(theta), 9.15 * np.sin(theta), color=LINE_COL, lw=1)
    ax.add_patch(plt.Rectangle((-52.5, -20.16), 16.5, 40.32, fill=False, edgecolor=LINE_COL, lw=1))
    ax.add_patch(plt.Rectangle((36, -20.16), 16.5, 40.32, fill=False, edgecolor=LINE_COL, lw=1))
    ax.add_patch(plt.Rectangle((-52.5, -9.16), 5.5, 18.32, fill=False, edgecolor=LINE_COL, lw=1))
    ax.add_patch(plt.Rectangle((47, -9.16), 5.5, 18.32, fill=False, edgecolor=LINE_COL, lw=1))
    ax.set_facecolor(PITCH_COL)
    ax.set_xlim(-55, 55)
    ax.set_ylim(-37, 37)
    ax.set_aspect('equal')
    ax.axis('off')


def main():
    ind_pts = pd.read_csv(FIG_DIR / 'fig1_individual_points.csv')
    ind_cycle = pd.read_csv(FIG_DIR / 'fig1_individual_cycle.csv')
    ind_meta = pd.read_csv(FIG_DIR / 'fig1_individual_meta.csv')

    tac_pts = pd.read_csv(FIG_DIR / 'fig1_tactical_points.csv')
    tac_cycle = pd.read_csv(FIG_DIR / 'fig1_tactical_cycle.csv')
    tac_meta = pd.read_csv(FIG_DIR / 'fig1_tactical_meta.csv')

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # Panel (a): Individual scale
    ax1 = axes[0]
    draw_pitch(ax1)
    is_cycle = ind_pts['is_cycle_node'].astype(bool)
    ax1.scatter(ind_pts.loc[~is_cycle, 'x'], ind_pts.loc[~is_cycle, 'y'],
                s=40, c=[NON_CYCLE], edgecolors='w', linewidths=0.5)
    ax1.scatter(ind_pts.loc[is_cycle, 'x'], ind_pts.loc[is_cycle, 'y'],
                s=60, c=[CENTROID_COL], edgecolors='w', linewidths=0.8)

    cycle_idx = (ind_cycle['node_idx'] + 1).values
    cx = ind_pts.loc[cycle_idx - 1, 'x'].values
    cy = ind_pts.loc[cycle_idx - 1, 'y'].values
    ax1.fill(cx, cy, color=CYCLE_FILL, alpha=FILL_ALPHA)
    n = len(cx)
    for k in range(n):
        k2 = (k + 1) % n
        ax1.plot([cx[k], cx[k2]], [cy[k], cy[k2]], color=CYCLE_EDGE, lw=2.2)
    ax1.scatter(cx, cy, s=70, c=[CENTROID_COL], edgecolors='w', linewidths=0.8)
    ax1.set_title(f'(a) Individual scale (δ = 2.98 m)\nPersistence = {ind_meta["persistence"].iloc[0]:.2f} m',
                  fontsize=11, fontweight='bold')

    # Panel (b): Tactical scale
    ax2 = axes[1]
    draw_pitch(ax2)
    is_cycle_t = tac_pts['is_cycle_node'].astype(bool)
    ax2.scatter(tac_pts.loc[~is_cycle_t, 'x'], tac_pts.loc[~is_cycle_t, 'y'],
                s=50, c=[NON_CYCLE], edgecolors='w', linewidths=0.5)
    ax2.scatter(tac_pts.loc[is_cycle_t, 'x'], tac_pts.loc[is_cycle_t, 'y'],
                s=80, c=[CENTROID_COL], marker='D', edgecolors='w', linewidths=0.8)

    cycle_idx_t = (tac_cycle['node_idx'] + 1).values
    tx = tac_pts.loc[cycle_idx_t - 1, 'x'].values
    ty = tac_pts.loc[cycle_idx_t - 1, 'y'].values
    ax2.fill(tx, ty, color=CYCLE_FILL, alpha=FILL_ALPHA)
    n_t = len(tx)
    for k in range(n_t):
        k2 = (k + 1) % n_t
        ax2.plot([tx[k], tx[k2]], [ty[k], ty[k2]], color=CYCLE_EDGE, lw=2.5)
    ax2.scatter(tx, ty, s=90, c=[CENTROID_COL], marker='D', edgecolors='w', linewidths=0.8)
    ax2.set_title(f'(b) Tactical scale (δ = 12.0 m)\nPersistence = {tac_meta["persistence"].iloc[0]:.2f} m',
                  fontsize=11, fontweight='bold')

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig2_cycle_geometry.pdf', bbox_inches='tight')
    fig.savefig(FIG_DIR / 'fig2_cycle_geometry.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Paper Figure 2 saved to {FIG_DIR}')


if __name__ == '__main__':
    main()
