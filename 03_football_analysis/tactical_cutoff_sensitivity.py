#!/usr/bin/env python3
"""
Tactical Cutoff Sensitivity Analysis
=====================================

Tests robustness of H1 results across the tactical cutoff range
(6.87-16.31 m) in 1 m increments. Also runs the adaptive filtration
ablation (P50, P75, P90) addressing reviewer Issues 1 and 5.

Outputs:
    results/sensitivity/cutoff_sensitivity.csv
    results/sensitivity/filtration_ablation.csv
    results/sensitivity/sensitivity_summary.json
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import secondspectrum
from tda_utils import (
    cutoff_clustering, adaptive_filtration, compute_persistence,
    persistence_stats, VALIDATED_CUTOFFS,
)

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'sensitivity'

CUTOFF_RANGE = np.arange(6.0, 17.5, 1.0)  # 6-17 m in 1 m steps
PERCENTILES = [50, 60, 75, 90, 95]
SAMPLE_EVERY = 100
MAX_FRAMES = 150


def cutoff_sensitivity(match):
    """Sweep cutoff distance and record H1 detection at each value."""
    complete = match.complete_frames
    rows = []

    for fi, frame in enumerate(complete):
        for cutoff in CUTOFF_RANGE:
            centroids, _ = cutoff_clustering(frame.all_positions, cutoff)
            filt = adaptive_filtration(centroids, cutoff, percentile=75)
            result = compute_persistence(centroids, filt)
            stats = persistence_stats(result.h1_diagram)

            rows.append({
                'frame_idx': fi,
                'cutoff': float(cutoff),
                'h0': result.h0_count,
                'h1': result.h1_count,
                'mean_persistence': stats['mean'],
                'max_persistence': stats['max'],
                'total_persistence': stats['total'],
                'filtration': result.filtration_used,
                'n_centroids': result.cluster_count,
            })

    return pd.DataFrame(rows)


def filtration_ablation(match):
    """Test different percentiles for adaptive filtration formula."""
    complete = match.complete_frames
    cutoff = VALIDATED_CUTOFFS['tactical']
    rows = []

    for fi, frame in enumerate(complete):
        centroids, _ = cutoff_clustering(frame.all_positions, cutoff)

        for pct in PERCENTILES:
            filt = adaptive_filtration(centroids, cutoff, percentile=pct)
            result = compute_persistence(centroids, filt)
            stats = persistence_stats(result.h1_diagram)

            rows.append({
                'frame_idx': fi,
                'percentile': pct,
                'h1': result.h1_count,
                'mean_persistence': stats['mean'],
                'total_persistence': stats['total'],
                'filtration': result.filtration_used,
            })

    return pd.DataFrame(rows)


def summarise(cutoff_df, ablation_df):
    """Produce summary statistics."""
    summary = {'cutoff_sensitivity': {}, 'filtration_ablation': {}}

    for c in CUTOFF_RANGE:
        cd = cutoff_df[cutoff_df['cutoff'] == c]
        summary['cutoff_sensitivity'][f'{c:.0f}m'] = {
            'total_h1': int(cd['h1'].sum()),
            'h1_presence': float((cd['h1'] > 0).mean()),
            'mean_h0': float(cd['h0'].mean()),
            'mean_persistence': float(cd[cd['h1'] > 0]['mean_persistence'].mean())
                if (cd['h1'] > 0).any() else 0.0,
        }

    for p in PERCENTILES:
        pd_sub = ablation_df[ablation_df['percentile'] == p]
        summary['filtration_ablation'][f'P{p}'] = {
            'total_h1': int(pd_sub['h1'].sum()),
            'h1_presence': float((pd_sub['h1'] > 0).mean()),
            'mean_filtration': float(pd_sub['filtration'].mean()),
        }

    # Identify stable range where H1 detection is robust
    h1_presence = {c: (cutoff_df[cutoff_df['cutoff'] == c]['h1'] > 0).mean()
                   for c in CUTOFF_RANGE}
    max_presence = max(h1_presence.values())
    stable = [c for c, v in h1_presence.items() if v >= max_presence * 0.5]
    summary['stable_range'] = {
        'min': float(min(stable)) if stable else None,
        'max': float(max(stable)) if stable else None,
    }

    return summary


def main():
    print("=" * 70)
    print("TACTICAL CUTOFF SENSITIVITY + FILTRATION ABLATION")
    print("=" * 70)

    match = secondspectrum.load_match(
        sample_every=SAMPLE_EVERY, require_complete=True, max_frames=MAX_FRAMES,
    )
    print(f"Loaded {match.n_frames} frames")

    print("\nSweeping cutoff distances (6-17 m)...")
    cutoff_df = cutoff_sensitivity(match)

    print("Running filtration ablation (P50-P95)...")
    ablation_df = filtration_ablation(match)

    summary = summarise(cutoff_df, ablation_df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cutoff_df.to_csv(OUTPUT_DIR / 'cutoff_sensitivity.csv', index=False)
    ablation_df.to_csv(OUTPUT_DIR / 'filtration_ablation.csv', index=False)
    with open(OUTPUT_DIR / 'sensitivity_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print("\n" + "=" * 70)
    print("CUTOFF SENSITIVITY RESULTS")
    print("=" * 70)
    for c in CUTOFF_RANGE:
        s = summary['cutoff_sensitivity'][f'{c:.0f}m']
        print(f"  {c:5.1f}m: H1 total={s['total_h1']:4d}, "
              f"presence={s['h1_presence']:.1%}, "
              f"mean H0={s['mean_h0']:.1f}")

    print(f"\nStable range: {summary['stable_range']}")

    print("\nFILTRATION ABLATION RESULTS")
    for p in PERCENTILES:
        s = summary['filtration_ablation'][f'P{p}']
        print(f"  P{p:2d}: H1 total={s['total_h1']:4d}, "
              f"presence={s['h1_presence']:.1%}, "
              f"filt={s['mean_filtration']:.1f}m")

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
