#!/usr/bin/env python3
"""
Generate Paper Figure 3: Temporal evolution of H1 persistence across analysis windows.

Two-panel figure: individual and tactical persistence with half-time marker and
smoothed trend lines. Uses fig2_temporal.csv (same as MATLAB version).

Run from Football-TDA root: python 06_papers/Paper1_MultiscaleTDA/figures/fig3_temporal_evolution.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parent

IND_COL = (0.20, 0.40, 0.75)
TAC_COL = (0.75, 0.15, 0.15)
TREND_IND = (0.10, 0.20, 0.55)
TREND_TAC = (0.55, 0.10, 0.10)
HALF_COL = (0.4, 0.4, 0.4)


def main():
    df = pd.read_csv(FIG_DIR / 'fig2_temporal.csv')
    primary_id = df['match_id'].iloc[0]
    df = df[df['match_id'] == primary_id]

    ind = df[df['scale'] == 'individual'].sort_values('window_idx')
    tac = df[df['scale'] == 'tactical'].sort_values('window_idx')

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for ax, scale_df, col, trend_col in [
        (axes[0], ind, IND_COL, TREND_IND),
        (axes[1], tac, TAC_COL, TREND_TAC),
    ]:
        if len(scale_df) == 0:
            continue

        x = scale_df['window_idx'].values
        y = scale_df['mean_persistence'].values

        markerline, stemlines, baseline = ax.stem(x, y, linefmt='-', markerfmt='o', basefmt=' ')
        plt.setp(stemlines, color=col, linewidth=0.5, alpha=0.35)
        plt.setp(markerline, color=col, markersize=2)
        y_smooth = pd.Series(y).rolling(25, min_periods=1, center=True).mean().values
        ax.plot(x, y_smooth, color=trend_col, lw=2.2)

        ht_idx = max(x) / 2
        ax.axvline(ht_idx, ls='--', color=HALF_COL, lw=1.2, label='Half-time')
        yl = [0, max(y) * 1.1]
        ax.fill_between([0, ht_idx, ht_idx, 0], [yl[0], yl[0], yl[1], yl[1]],
                        color=col, alpha=0.04)

        ax.set_ylabel('Mean H₁ persistence (m)', fontsize=10)
        ax.set_ylim(yl)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)

    axes[0].set_title('(a) Individual scale (δ = 2.98 m)', fontsize=11, fontweight='bold')
    axes[1].set_title('(b) Tactical scale (δ = 12.0 m)', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Analysis window index', fontsize=10)

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig3_temporal_evolution.pdf', bbox_inches='tight')
    fig.savefig(FIG_DIR / 'fig3_temporal_evolution.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Paper Figure 3 saved to {FIG_DIR}')


if __name__ == '__main__':
    main()
