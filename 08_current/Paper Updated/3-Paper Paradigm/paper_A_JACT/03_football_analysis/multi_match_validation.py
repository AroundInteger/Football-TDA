#!/usr/bin/env python3
"""
Multi-Match Validation
======================

Runs the full multi-scale TDA pipeline (H0 + H1) across all available matches
(SecondSpectrum + SkillCorner by default) to validate that the single-match
findings generalise. Use ``--skillcorner-only`` for open-data-only aggregates.
Produces per-match summaries plus aggregate statistics with confidence intervals.

Addresses reviewer Issue 2 (team-scale H1 absence) and the single-match limitation.

Outputs:
    results/multi_match/per_match_summary.csv
    results/multi_match/aggregate_stats.json
    results/multi_match/h1_loops_all_matches.csv
"""

import argparse
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

from loaders import secondspectrum, skillcorner, MatchData
from tda_utils import compute_h1_at_scale, VALIDATED_CUTOFFS, persistence_stats

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'multi_match'
FRAMES_PER_MATCH = 150
SAMPLE_RATE = 100  # every 100th frame


def load_all_matches(skillcorner_only: bool = False) -> list:
    """Load all available matches from SecondSpectrum and SkillCorner."""
    matches = []

    if not skillcorner_only:
        # SecondSpectrum
        try:
            ss = secondspectrum.load_match(
                sample_every=SAMPLE_RATE, require_complete=True, max_frames=FRAMES_PER_MATCH,
            )
            matches.append(ss)
            print(f"  [SecondSpectrum] {ss.info.home_team} vs {ss.info.away_team}: {ss.n_frames} frames")
        except FileNotFoundError:
            print("  [SecondSpectrum] Data not found, skipping.")
    else:
        print("  [SecondSpectrum] Skipped (--skillcorner-only).")

    # SkillCorner
    try:
        sc_matches = skillcorner.list_matches()
    except FileNotFoundError:
        sc_matches = []

    for m in sc_matches:
        mid = m['id']
        try:
            sc = skillcorner.load_match(
                mid, sample_every=SAMPLE_RATE, require_complete=True, max_frames=FRAMES_PER_MATCH,
            )
            matches.append(sc)
            print(f"  [SkillCorner] {sc.info.home_team} vs {sc.info.away_team}: {sc.n_frames} frames")
        except FileNotFoundError as e:
            print(f"  [SkillCorner] Match {mid}: {e}")

    return matches


def analyse_match(match: MatchData) -> pd.DataFrame:
    """Run multi-scale H0/H1 on every sampled frame of a match."""
    complete = match.complete_frames
    rows = []

    for fi, frame in enumerate(complete):
        for scale, cutoff in VALIDATED_CUTOFFS.items():
            result = compute_h1_at_scale(frame.all_positions, cutoff)
            row = {
                'match_id': match.info.match_id,
                'source': match.info.source,
                'home_team': match.info.home_team,
                'away_team': match.info.away_team,
                'frame_idx': fi,
                'timestamp': frame.timestamp,
                'period': frame.period,
                'scale': scale,
                'cutoff': cutoff,
                'h0': result.h0_count,
                'h1': result.h1_count,
                'cluster_count': result.cluster_count,
                'filtration': result.filtration_used,
            }

            stats = persistence_stats(result.h1_diagram)
            row['h1_mean_persistence'] = stats['mean']
            row['h1_max_persistence'] = stats['max']
            row['h1_total_persistence'] = stats['total']

            rows.append(row)

    return pd.DataFrame(rows)


def compute_aggregate(all_df: pd.DataFrame) -> dict:
    """Compute aggregate statistics across all matches."""
    agg = {}

    for scale in ['individual', 'tactical', 'team']:
        sd = all_df[all_df['scale'] == scale]

        per_match = sd.groupby('match_id').agg(
            h0_mean=('h0', 'mean'),
            h0_std=('h0', 'std'),
            h1_total=('h1', 'sum'),
            h1_mean_per_frame=('h1', 'mean'),
            h1_presence=('h1', lambda x: (x > 0).mean()),
            mean_persistence=('h1_mean_persistence', 'mean'),
            n_frames=('h0', 'count'),
        ).reset_index()

        n_matches = len(per_match)
        agg[scale] = {
            'n_matches': int(n_matches),
            'h0_grand_mean': float(per_match['h0_mean'].mean()),
            'h0_grand_std': float(per_match['h0_mean'].std()),
            'h1_total_all': int(sd['h1'].sum()),
            'h1_presence_rate': float(per_match['h1_presence'].mean()),
            'h1_presence_rate_std': float(per_match['h1_presence'].std()),
            'mean_persistence_grand': float(per_match['mean_persistence'].mean()),
            'per_match': per_match.to_dict('records'),
        }

    return agg


def main():
    parser = argparse.ArgumentParser(description="Multi-match TDA validation (H0 + H1).")
    parser.add_argument(
        "--skillcorner-only",
        action="store_true",
        help="Use SkillCorner matches only (exclude SecondSpectrum).",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("MULTI-MATCH VALIDATION")
    if args.skillcorner_only:
        print("(SkillCorner only)")
    print("=" * 70)
    print()
    print("Loading matches...")
    matches = load_all_matches(skillcorner_only=args.skillcorner_only)
    print(f"\nTotal matches loaded: {len(matches)}")

    if not matches:
        print("No matches found. Exiting.")
        return

    all_dfs = []
    for i, match in enumerate(matches):
        print(f"\n[{i+1}/{len(matches)}] Analysing {match.info.home_team} vs {match.info.away_team}...")
        df = analyse_match(match)
        all_dfs.append(df)
        n_h1 = df[df['h1'] > 0].shape[0]
        print(f"  {len(df)} observations, {n_h1} frames with H1 loops")

    all_df = pd.concat(all_dfs, ignore_index=True)
    agg = compute_aggregate(all_df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_df.to_csv(OUTPUT_DIR / 'per_frame_results.csv', index=False)
    with open(OUTPUT_DIR / 'aggregate_stats.json', 'w') as f:
        json.dump(agg, f, indent=2, default=str)

    # Summary
    print("\n" + "=" * 70)
    print("AGGREGATE RESULTS")
    print("=" * 70)
    for scale in ['individual', 'tactical', 'team']:
        a = agg[scale]
        print(f"\n{scale.upper()} (cutoff={VALIDATED_CUTOFFS[scale]}m):")
        print(f"  H0 grand mean: {a['h0_grand_mean']:.2f} +/- {a['h0_grand_std']:.2f}")
        print(f"  Total H1 loops: {a['h1_total_all']}")
        print(f"  H1 presence rate: {a['h1_presence_rate']:.1%} +/- {a['h1_presence_rate_std']:.1%}")
        print(f"  Mean persistence: {a['mean_persistence_grand']:.3f}")

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
