#!/usr/bin/env python3
"""
Generate Figure: Persistence diagrams at individual and tactical scales.

Creates a two-panel figure showing (birth, death) for H1 features from
representative frames. Uses h1_loops_full_data.json.

Run from Football-TDA root: python 06_papers/Paper1_MultiscaleTDA/figures/generate_fig_persistence_diagrams.py
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIG_DIR = Path(__file__).resolve().parent
DATA_FILE = ROOT / '04_h1_loops' / 'h1_loop_analysis' / 'h1_loops_full_data.json'

INDIVIDUAL_COLOUR = '#2166AC'
TACTICAL_COLOUR = '#B2182B'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'figure.dpi': 300,
})


def main():
    with open(DATA_FILE) as f:
        loops = json.load(f)

    # Representative frames from the paper: Frame 72 (individual), Frame 73 (tactical)
    ind_loops = [l for l in loops if l['scale'] == 'individual' and l['frame_idx'] == 72]
    tac_loops = [l for l in loops if l['scale'] == 'tactical' and l['frame_idx'] == 73]

    # Fallback: use frames with most loops if representative frames empty
    if not ind_loops:
        ind_by_frame = {}
        for l in loops:
            if l['scale'] == 'individual':
                fid = l['frame_idx']
                ind_by_frame[fid] = ind_by_frame.get(fid, []) + [l]
        best_frame = max(ind_by_frame.items(), key=lambda x: len(x[1]))[0]
        ind_loops = ind_by_frame[best_frame]

    if not tac_loops:
        tac_by_frame = {}
        for l in loops:
            if l['scale'] == 'tactical':
                fid = l['frame_idx']
                tac_by_frame[fid] = tac_by_frame.get(fid, []) + [l]
        if tac_by_frame:
            best_frame = max(tac_by_frame.items(), key=lambda x: len(x[1]))[0]
            tac_loops = tac_by_frame[best_frame]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    for ax, (scale_loops, colour, scale_name, cutoff) in zip(axes, [
        (ind_loops, INDIVIDUAL_COLOUR, 'Individual', 2.98),
        (tac_loops, TACTICAL_COLOUR, 'Tactical', 12.0),
    ]):
        if not scale_loops:
            ax.text(0.5, 0.5, f'No H1 loops in\n{scale_name} scale', ha='center', va='center')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            continue

        births = np.array([l['birth'] for l in scale_loops])
        deaths = np.array([l['death'] for l in scale_loops])
        persistence = deaths - births

        max_val = max(births.max(), deaths.max()) * 1.1
        ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.4, lw=1)

        ax.scatter(births, deaths, c=colour, marker='^', s=60,
                   edgecolors='black', linewidths=0.5, zorder=5,
                   label=f'$H_1$ ({len(births)} loops)')

        ax.set_xlabel('Birth (m)')
        ax.set_ylabel('Death (m)')
        ax.set_title(f'({scale_name[0].lower()}) {scale_name} scale (δ = {cutoff} m)')
        ax.legend(fontsize=9)
        ax.set_xlim(-0.5, max_val)
        ax.set_ylim(-0.5, max_val)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, alpha=0.3)

    fig.suptitle('Representative persistence diagrams', fontsize=12, fontweight='bold', y=1.02)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig_persistence_diagrams.pdf', bbox_inches='tight')
    fig.savefig(FIG_DIR / 'fig_persistence_diagrams.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Persistence diagram figure saved to {FIG_DIR}")


if __name__ == '__main__':
    main()
