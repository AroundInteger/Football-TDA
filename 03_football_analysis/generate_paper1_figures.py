#!/usr/bin/env python3
"""
Generate Paper 1 Figures
========================

Produces publication-quality figures for the multi-scale TDA paper.

Figures:
  1. Persistence diagrams at individual and tactical scales (representative frame)
  2. Closed-cycle geometric realisation on the pitch
  3. Temporal evolution of mean persistence (149 windows, both scales)
  4. Tactical cutoff sensitivity heatmap
  5. Multi-match H1 comparison (box plots across 11 matches)

Outputs saved to results/figures/

Addresses reviewer Issue 8 (no figures).
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import secondspectrum
from tda_utils import (
    compute_h1_at_scale, cutoff_clustering, adaptive_filtration,
    compute_persistence, persistence_stats, find_closed_cycles,
    VALIDATED_CUTOFFS,
)

FIG_DIR = PROJECT_ROOT / 'results' / 'figures'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

INDIVIDUAL_COLOUR = '#2166AC'
TACTICAL_COLOUR = '#B2182B'
TEAM_COLOUR = '#4DAF4A'


def fig1_persistence_diagrams(match):
    """Persistence diagrams at individual and tactical scales."""
    frame = match.complete_frames[len(match.complete_frames) // 2]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    for ax, (scale, colour) in zip(axes, [
        ('individual', INDIVIDUAL_COLOUR), ('tactical', TACTICAL_COLOUR),
    ]):
        cutoff = VALIDATED_CUTOFFS[scale]
        result = compute_h1_at_scale(frame.all_positions, cutoff)

        max_val = result.filtration_used * 1.05

        ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, lw=0.8)

        if len(result.h0_diagram) > 0:
            h0_finite = result.h0_diagram[np.isfinite(result.h0_diagram[:, 1])]
            if len(h0_finite) > 0:
                ax.scatter(h0_finite[:, 0], h0_finite[:, 1],
                           c='grey', marker='o', s=30, alpha=0.5, label=f'$H_0$ ({len(h0_finite)})')

        if len(result.h1_diagram) > 0:
            ax.scatter(result.h1_diagram[:, 0], result.h1_diagram[:, 1],
                       c=colour, marker='^', s=50, edgecolors='black', linewidths=0.5,
                       label=f'$H_1$ ({len(result.h1_diagram)})', zorder=5)

        ax.set_xlabel('Birth (metres)')
        ax.set_ylabel('Death (metres)')
        ax.set_title(f'{scale.capitalize()} scale ($\\delta$ = {cutoff} m)')
        ax.legend(fontsize=9)
        ax.set_xlim(-0.5, max_val)
        ax.set_ylim(-0.5, max_val)

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig1_persistence_diagrams.pdf')
    fig.savefig(FIG_DIR / 'fig1_persistence_diagrams.png')
    plt.close(fig)
    print("  Figure 1: persistence diagrams saved")


def fig2_cycle_geometry(match):
    """Geometric realisation of a closed cycle on the pitch."""
    frame = match.complete_frames[len(match.complete_frames) // 2]
    cutoff = VALIDATED_CUTOFFS['tactical']
    result = compute_h1_at_scale(frame.all_positions, cutoff)

    if result.h1_count == 0:
        for f in match.complete_frames:
            result = compute_h1_at_scale(f.all_positions, cutoff)
            if result.h1_count > 0:
                frame = f
                break

    if result.h1_count == 0:
        print("  Figure 2: no tactical H1 found, skipping")
        return

    best_idx = np.argmax(result.h1_diagram[:, 1] - result.h1_diagram[:, 0])
    birth = float(result.h1_diagram[best_idx, 0])
    death = float(result.h1_diagram[best_idx, 1])

    cycles = find_closed_cycles(result.point_cloud, birth, death)

    fig, ax = plt.subplots(figsize=(8, 5.5))

    ax.set_facecolor('#2d7a3a')
    ax.set_xlim(-52.5, 52.5)
    ax.set_ylim(-34, 34)
    ax.set_aspect('equal')

    for spine in ax.spines.values():
        spine.set_color('white')
    ax.axhline(0, color='white', lw=0.5, alpha=0.3)
    ax.axvline(0, color='white', lw=0.5, alpha=0.3)

    ax.scatter(frame.home_positions[:, 0], frame.home_positions[:, 1],
               c='white', marker='o', s=60, edgecolors='black', linewidths=0.5, zorder=3, label='Home')
    ax.scatter(frame.away_positions[:, 0], frame.away_positions[:, 1],
               c='red', marker='s', s=60, edgecolors='black', linewidths=0.5, zorder=3, label='Away')

    ax.scatter(result.point_cloud[:, 0], result.point_cloud[:, 1],
               c='yellow', marker='D', s=80, edgecolors='black', linewidths=1, zorder=4, label='Centroids')

    if cycles:
        best = cycles[0]
        nodes = best.nodes
        for i in range(len(nodes)):
            j = (i + 1) % len(nodes)
            p1 = result.point_cloud[nodes[i]]
            p2 = result.point_cloud[nodes[j]]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                    color=TACTICAL_COLOUR, lw=2.5, alpha=0.9, zorder=5)

    ax.set_xlabel('x (metres)')
    ax.set_ylabel('y (metres)')
    ax.set_title(f'Tactical-scale cycle: birth={birth:.1f}m, death={death:.1f}m, '
                 f'persistence={death-birth:.1f}m')
    ax.legend(loc='upper right', fontsize=8, framealpha=0.8)

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig2_cycle_geometry.pdf')
    fig.savefig(FIG_DIR / 'fig2_cycle_geometry.png')
    plt.close(fig)
    print("  Figure 2: cycle geometry saved")


def fig3_temporal_evolution():
    """Temporal evolution of mean persistence from pre-computed windows."""
    csv_path = PROJECT_ROOT / 'results' / 'statistical_tests' / 'per_window_persistence.csv'
    if not csv_path.exists():
        print("  Figure 3: run statistical_tests_temporal.py first")
        return

    df = pd.read_csv(csv_path)
    ss = df[df['match_id'] == df['match_id'].iloc[0]]

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    for ax, (scale, colour) in zip(axes, [
        ('individual', INDIVIDUAL_COLOUR), ('tactical', TACTICAL_COLOUR),
    ]):
        sd = ss[ss['scale'] == scale]
        if len(sd) == 0:
            continue

        ax.plot(sd['window_idx'], sd['mean_persistence'], '-o',
                color=colour, markersize=4, lw=1.5, label=f'{scale.capitalize()}')
        ax.fill_between(sd['window_idx'], 0, sd['mean_persistence'],
                        alpha=0.15, color=colour)

        half_boundary = sd[sd['period'] == 1]['window_idx'].max()
        if pd.notna(half_boundary):
            ax.axvline(half_boundary, color='grey', ls='--', lw=1, alpha=0.6)
            ax.text(half_boundary + 0.3, ax.get_ylim()[1] * 0.9, 'Half-time',
                    fontsize=8, color='grey')

        ax.set_ylabel('Mean H1 persistence (m)')
        ax.legend(fontsize=9)

    axes[1].set_xlabel('Analysis window index')
    fig.suptitle('Temporal evolution of H1 persistence', y=1.01)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig3_temporal_evolution.pdf')
    fig.savefig(FIG_DIR / 'fig3_temporal_evolution.png')
    plt.close(fig)
    print("  Figure 3: temporal evolution saved")


def fig4_sensitivity_heatmap():
    """Cutoff sensitivity heatmap from pre-computed results."""
    csv_path = PROJECT_ROOT / 'results' / 'sensitivity' / 'cutoff_sensitivity.csv'
    if not csv_path.exists():
        print("  Figure 4: run tactical_cutoff_sensitivity.py first")
        return

    df = pd.read_csv(csv_path)
    pivot = df.pivot_table(
        index='frame_idx', columns='cutoff', values='h1', aggfunc='sum',
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    im = ax.imshow(pivot.values.T, aspect='auto', cmap='YlOrRd',
                   extent=[0, len(pivot), pivot.columns.max(), pivot.columns.min()])
    ax.set_xlabel('Frame index')
    ax.set_ylabel('Cutoff distance (m)')
    ax.set_title('H1 loop count by cutoff distance and frame')
    plt.colorbar(im, ax=ax, label='H1 count')

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig4_sensitivity_heatmap.pdf')
    fig.savefig(FIG_DIR / 'fig4_sensitivity_heatmap.png')
    plt.close(fig)
    print("  Figure 4: sensitivity heatmap saved")


def fig5_multi_match_boxplot():
    """Multi-match H1 comparison box plots."""
    csv_path = PROJECT_ROOT / 'results' / 'multi_match' / 'per_frame_results.csv'
    if not csv_path.exists():
        print("  Figure 5: run multi_match_validation.py first")
        return

    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, (scale, colour) in zip(axes, [
        ('individual', INDIVIDUAL_COLOUR), ('tactical', TACTICAL_COLOUR),
    ]):
        sd = df[df['scale'] == scale]
        match_ids = sorted(sd['match_id'].unique(), key=str)
        data = [sd[sd['match_id'] == mid]['h1'].values for mid in match_ids]
        labels = [str(mid)[:8] for mid in match_ids]

        bp = ax.boxplot(data, labels=labels, patch_artist=True, showfliers=False)
        for patch in bp['boxes']:
            patch.set_facecolor(colour)
            patch.set_alpha(0.6)

        ax.set_xlabel('Match')
        ax.set_ylabel('H1 loop count per frame')
        ax.set_title(f'{scale.capitalize()} scale')
        ax.tick_params(axis='x', rotation=45)

    fig.suptitle('H1 loop distribution across matches', y=1.01)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig5_multi_match_boxplot.pdf')
    fig.savefig(FIG_DIR / 'fig5_multi_match_boxplot.png')
    plt.close(fig)
    print("  Figure 5: multi-match box plot saved")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating Paper 1 figures...")

    match = secondspectrum.load_match(sample_every=100, require_complete=True, max_frames=150)

    fig1_persistence_diagrams(match)
    fig2_cycle_geometry(match)
    fig3_temporal_evolution()
    fig4_sensitivity_heatmap()
    fig5_multi_match_boxplot()

    print(f"\nAll figures saved to {FIG_DIR}")


if __name__ == '__main__':
    main()
