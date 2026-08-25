#!/usr/bin/env python3
"""
Generate Paper Figure 4: Persistence change by match event type.

Grouped horizontal bar chart for significant event types at individual and
tactical scales. Uses fig3_event_correlation.csv (same as MATLAB version).

Run from Football-TDA root: python 08_current/paper/figures/fig4_event_correlation.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parent

IND_COL = (0.20, 0.40, 0.75)
TAC_COL = (0.75, 0.15, 0.15)


def main():
    df = pd.read_csv(FIG_DIR / 'fig3_event_correlation.csv')
    df = df[df['significant'] == 1]

    ind = df[df['scale'] == 'individual']
    tac = df[df['scale'] == 'tactical']
    all_events = sorted(set(ind['event_type'].tolist() + tac['event_type'].tolist()))

    deltas = np.full((len(all_events), 2), np.nan)
    pvals = np.full((len(all_events), 2), np.nan)
    counts = np.full((len(all_events), 2), np.nan)

    for k, ev in enumerate(all_events):
        ri = ind[ind['event_type'] == ev]
        rt = tac[tac['event_type'] == ev]
        if len(ri) > 0:
            deltas[k, 0] = ri['mean_delta'].iloc[0]
            pvals[k, 0] = ri['p_value'].iloc[0]
            counts[k, 0] = ri['n_events'].iloc[0]
        if len(rt) > 0:
            deltas[k, 1] = rt['mean_delta'].iloc[0]
            pvals[k, 1] = rt['p_value'].iloc[0]
            counts[k, 1] = rt['n_events'].iloc[0]

    sort_val = np.where(np.isnan(deltas[:, 0]), deltas[:, 1], deltas[:, 0])
    sort_idx = np.argsort(sort_val)
    all_events = [all_events[i] for i in sort_idx]
    deltas = deltas[sort_idx]
    pvals = pvals[sort_idx]
    counts = counts[sort_idx]

    labels = [e.replace('_', ' ').capitalize() for e in all_events]
    y = np.arange(len(all_events))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axvline(0, color=(0.3, 0.3, 0.3), lw=1)

    for k in range(len(all_events)):
        if not np.isnan(deltas[k, 0]):
            ax.barh(y[k] + bar_width/2, deltas[k, 0], bar_width, color=IND_COL, alpha=0.85, edgecolor='none')
            p = pvals[k, 0]
            star = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            if star:
                nudge = -0.02 if deltas[k, 0] < 0 else 0.02
                ax.text(deltas[k, 0] + nudge, y[k] + bar_width/2, star, fontsize=8, fontweight='bold',
                       ha='right' if deltas[k, 0] < 0 else 'left', va='center')
        if not np.isnan(deltas[k, 1]):
            ax.barh(y[k] - bar_width/2, deltas[k, 1], bar_width, color=TAC_COL, alpha=0.85, edgecolor='none')
            p = pvals[k, 1]
            star = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            if star:
                nudge = -0.02 if deltas[k, 1] < 0 else 0.02
                ax.text(deltas[k, 1] + nudge, y[k] - bar_width/2, star, fontsize=8, fontweight='bold',
                       ha='right' if deltas[k, 1] < 0 else 'left', va='center')

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel('Mean persistence change (Δ, metres)', fontsize=10)
    ax.set_ylim(-0.3, len(all_events) - 0.7)
    ax.invert_yaxis()

    from matplotlib.patches import Patch
    ax.legend([Patch(facecolor=IND_COL, alpha=0.85), Patch(facecolor=TAC_COL, alpha=0.85)],
              ['Individual scale', 'Tactical scale'], loc='lower right', frameon=False, fontsize=9)
    ax.set_title('Persistence change by match event type', fontsize=11, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig4_event_correlation.pdf', bbox_inches='tight')
    fig.savefig(FIG_DIR / 'fig4_event_correlation.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Paper Figure 4 saved to {FIG_DIR}')


if __name__ == '__main__':
    main()
