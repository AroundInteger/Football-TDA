#!/usr/bin/env python3
"""
Linkage Method Comparison
=========================

Compares single-linkage, complete-linkage, and Ward's method for
hierarchical clustering, quantifying chaining effects and their
impact on H0/H1 detection.

Addresses reviewer Issue 12 (clustering method choice).

Outputs:
    results/linkage/linkage_comparison.csv
    results/linkage/linkage_summary.json
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage as hc_linkage, fcluster
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import secondspectrum, skillcorner
from tda_utils import (
    cutoff_clustering, adaptive_filtration, compute_persistence,
    persistence_stats, VALIDATED_CUTOFFS,
)

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'linkage'

METHODS = ['single', 'complete', 'ward']


def chaining_metric(positions, labels):
    """
    Quantify chaining: ratio of largest cluster size to second-largest.
    A high ratio indicates chaining (single-linkage pathology).
    """
    if labels is None or len(labels) == 0:
        return 0.0
    sizes = np.bincount(labels)[1:]  # fcluster labels are 1-indexed
    if len(sizes) < 2:
        return float(sizes[0]) if len(sizes) else 0.0
    sorted_sizes = np.sort(sizes)[::-1]
    return float(sorted_sizes[0] / sorted_sizes[1]) if sorted_sizes[1] > 0 else float('inf')


def compare_methods(match, max_frames=150):
    """Run all linkage methods at all scales on a match."""
    complete = match.complete_frames[:max_frames]
    rows = []

    for fi, frame in enumerate(complete):
        for scale, cutoff in VALIDATED_CUTOFFS.items():
            for method in METHODS:
                centroids, labels = cutoff_clustering(
                    frame.all_positions, cutoff, method=method,
                )
                filt = adaptive_filtration(centroids, cutoff)
                result = compute_persistence(centroids, filt)
                stats = persistence_stats(result.h1_diagram)
                chain_ratio = chaining_metric(frame.all_positions, labels)

                rows.append({
                    'frame_idx': fi,
                    'match_id': match.info.match_id,
                    'scale': scale,
                    'cutoff': cutoff,
                    'method': method,
                    'n_clusters': result.cluster_count,
                    'h0': result.h0_count,
                    'h1': result.h1_count,
                    'mean_persistence': stats['mean'],
                    'max_persistence': stats['max'],
                    'chaining_ratio': chain_ratio,
                })

    return pd.DataFrame(rows)


def summarise(df):
    """Aggregate comparison statistics."""
    summary = {}

    for scale in ['individual', 'tactical', 'team']:
        sd = df[df['scale'] == scale]
        summary[scale] = {}
        for method in METHODS:
            md = sd[sd['method'] == method]
            summary[scale][method] = {
                'mean_clusters': float(md['n_clusters'].mean()),
                'std_clusters': float(md['n_clusters'].std()),
                'total_h1': int(md['h1'].sum()),
                'h1_presence': float((md['h1'] > 0).mean()),
                'mean_chaining_ratio': float(md['chaining_ratio'].mean()),
                'max_chaining_ratio': float(md['chaining_ratio'].max()),
            }

    return summary


def main():
    print("=" * 70)
    print("LINKAGE METHOD COMPARISON")
    print("=" * 70)

    matches = []
    try:
        matches.append(secondspectrum.load_match(
            sample_every=100, require_complete=True, max_frames=150,
        ))
    except FileNotFoundError:
        pass

    try:
        for m in skillcorner.list_matches()[:3]:
            try:
                matches.append(skillcorner.load_match(
                    m['id'], sample_every=100, require_complete=True, max_frames=150,
                ))
            except FileNotFoundError:
                pass
    except FileNotFoundError:
        pass

    all_dfs = []
    for match in matches:
        name = f"{match.info.home_team} vs {match.info.away_team}"
        print(f"\n  Analysing {name}...")
        df = compare_methods(match)
        all_dfs.append(df)

    combined = pd.concat(all_dfs, ignore_index=True)
    summary = summarise(combined)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT_DIR / 'linkage_comparison.csv', index=False)
    with open(OUTPUT_DIR / 'linkage_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n{'=' * 70}")
    print("RESULTS")
    print(f"{'=' * 70}")
    for scale in ['individual', 'tactical', 'team']:
        print(f"\n{scale.upper()} (cutoff={VALIDATED_CUTOFFS[scale]}m):")
        for method in METHODS:
            s = summary[scale][method]
            print(f"  {method:10s}: clusters={s['mean_clusters']:.1f}+/-{s['std_clusters']:.1f}, "
                  f"H1={s['total_h1']:4d}, presence={s['h1_presence']:.1%}, "
                  f"chain={s['mean_chaining_ratio']:.2f}")

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
