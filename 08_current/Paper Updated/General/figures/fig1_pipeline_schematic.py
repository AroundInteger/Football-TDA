#!/usr/bin/env python3
"""
Generate Paper Figure 1: Multi-scale TDA pipeline schematic.

Highlights the two methodological contributions (scale decomposition via δ;
adaptive filtration via ε_max) and includes a schematic persistence diagram
(birth/death plot) so the figure matches prose that refers to the PD stage.

Run from Football-TDA root:
  python 08_current/paper/figures/fig1_pipeline_schematic.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

FIG_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'axes.labelsize': 10,
    'figure.dpi': 300,
})

ARROW_COLOUR = '#333333'
TEXT_COLOUR = '#222222'
CONTRIB1_FACE = '#E3F2FD'
CONTRIB2_FACE = '#FFF8E1'
PD_POINT = '#C62828'


def _draw_mini_pd(ax, x0: float, y0: float, w: float, h: float) -> None:
    """Schematic persistence diagram (H1 points above the diagonal)."""
    xs = np.linspace(0.0, 1.0, 32)
    ax.plot(x0 + xs * w, y0 + xs * h, color='#666666', lw=1.0, zorder=2)
    pts = np.array([
        [0.12, 0.38], [0.28, 0.52], [0.42, 0.58], [0.58, 0.72],
    ])
    ax.scatter(
        x0 + pts[:, 0] * w, y0 + pts[:, 1] * h,
        s=22, c=PD_POINT, edgecolors='white', linewidths=0.4, zorder=4,
    )
    ax.text(
        x0 + 0.04 * w, y0 + 0.82 * h, r'$H_1$', fontsize=7,
        color=TEXT_COLOUR,
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(14.5, 5.2))
    ax.set_xlim(0, 18.2)
    ax.set_ylim(0, 5.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Contribution backgrounds (behind boxes)
    ax.add_patch(Rectangle(
        (0.35, 1.05), 8.55, 2.95, facecolor=CONTRIB1_FACE,
        edgecolor='none', zorder=0, alpha=0.95,
    ))
    ax.add_patch(Rectangle(
        (9.05, 1.05), 5.55, 2.95, facecolor=CONTRIB2_FACE,
        edgecolor='none', zorder=0, alpha=0.95,
    ))

    ax.text(
        4.6, 4.55, 'Contribution 1: scale decomposition',
        ha='center', va='bottom', fontsize=10, fontweight='bold',
        color='#1565C0',
    )
    ax.text(
        4.6, 4.2, r'single-linkage clustering at cutoff $\delta$',
        ha='center', va='bottom', fontsize=8.5, color='#1565C0',
    )
    ax.text(
        11.85, 4.55, 'Contribution 2: adaptive filtration',
        ha='center', va='bottom', fontsize=10, fontweight='bold',
        color='#E65100',
    )
    ax.text(
        11.85, 4.2,
        r'$\varepsilon_{\max}$ adapts VR scale to centroid geometry',
        ha='center', va='bottom', fontsize=8.5, color='#E65100',
    )

    # Main flow boxes (x_centre, y_centre, width, height)
    boxes = [
        (1.6, 2.35, 2.05, 1.25),
        (4.6, 2.35, 2.05, 1.25),
        (7.6, 2.35, 2.05, 1.25),
        (10.6, 2.35, 2.05, 1.25),
        (13.6, 2.35, 2.05, 1.25),
        (16.45, 2.35, 1.85, 1.25),
    ]
    labels = [
        '22 player\npositions',
        'Hierarchical\nclustering ($\\delta$)',
        r'Cluster centroids' + '\n' + r'$\tilde P(t)$',
        r'Vietoris--Rips' + '\n' + r'($\varepsilon \leq \varepsilon_{\max}$)',
        None,
        r'Closed cycles $\rightarrow$' + '\n' + 'geometric realisation',
    ]

    for (x, y, w, h), label in zip(boxes, labels):
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle='round,pad=0.02,rounding_size=0.12',
            facecolor='white', edgecolor=ARROW_COLOUR,
            linewidth=1.15, zorder=2,
        )
        ax.add_patch(box)
        if label is not None:
            ax.text(
                x, y, label, ha='center', va='center', fontsize=8.8,
                color=TEXT_COLOUR, zorder=3,
            )

    # Schematic PD inside the persistence-diagram box (box index 4)
    bx, by, bw, bh = boxes[4]
    ax.text(
        bx, by + 0.38, 'Persistence diagram', ha='center', va='center',
        fontsize=8.8, color=TEXT_COLOUR, zorder=3,
    )
    ax.text(
        bx, by + 0.12, r'(schematic $H_1$)', ha='center', va='center',
        fontsize=7.5, color='#555555', zorder=3,
    )
    pd_w, pd_h = 0.88, 0.52
    _draw_mini_pd(
        ax,
        bx + bw / 2 - pd_w / 2,
        by - bh / 2 + 0.08,
        pd_w,
        pd_h,
    )

    # Arrows between boxes
    for i in range(len(boxes) - 1):
        x1 = boxes[i][0] + boxes[i][2] / 2
        x2 = boxes[i + 1][0] - boxes[i + 1][2] / 2
        ax.annotate(
            '', xy=(x2, 2.35), xytext=(x1, 2.35),
            arrowprops=dict(arrowstyle='->', color=ARROW_COLOUR, lw=1.45),
            zorder=1,
        )

    ax.set_title(
        'Multi-scale TDA analysis pipeline',
        fontsize=12, fontweight='bold', pad=8, y=1.02,
    )

    fig.tight_layout()
    fig.savefig(FIG_DIR / 'fig1_pipeline_schematic.pdf', bbox_inches='tight')
    fig.savefig(FIG_DIR / 'fig1_pipeline_schematic.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Paper Figure 1 (pipeline schematic) saved to {FIG_DIR}')


if __name__ == '__main__':
    main()
