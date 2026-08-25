#!/usr/bin/env python3
"""
Statistical Tests: Temporal Evolution
======================================

Runs Wilcoxon rank-sum tests on first-half vs second-half mean \(H_1\) persistence
for SkillCorner broadcast tracking windows.

Primary match (**1996435**): non-overlapping **2-minute** windows at **10 Hz**
(\(1200\) frames per window), matching manuscript Figure~3 methods.

Older exploratory behaviour (`--legacy-multi`): SecondSpectrum fixture plus three
SkillCorner matches with coarse 100-frame windows is retained for troubleshooting.

Outputs:
    results/statistical_tests/temporal_tests.json
    results/statistical_tests/per_window_persistence.csv
"""

import argparse
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import secondspectrum, skillcorner, MatchData
from tda_utils import compute_h1_at_scale, persistence_stats, VALIDATED_CUTOFFS

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'statistical_tests'
PRIMARY_SKILLCORNER_ID = 1996435

# SkillCorner manuscript windows: two minutes @ 10 Hz broadcast tracking
WINDOW_SIZE_PRIMARY = 1200
WINDOW_STEP_PRIMARY = 1200

WINDOW_SIZE_LEGACY = 100
WINDOW_STEP_LEGACY = 100


def compute_window_persistence(
    match: MatchData,
    scale: str,
    *,
    window_size: int,
    window_step: int,
) -> pd.DataFrame:
    """Compute mean H1 persistence per sliding window."""
    cutoff = VALIDATED_CUTOFFS[scale]
    complete = match.complete_frames

    rows = []
    window_idx = 0
    span = window_size - 1
    for start in range(0, len(complete) - span, window_step):
        window_frames = complete[start:start + window_size]
        h1_counts = []
        persistences = []

        for frame in window_frames:
            result = compute_h1_at_scale(frame.all_positions, cutoff)
            h1_counts.append(result.h1_count)
            if result.h1_count > 0:
                stats = persistence_stats(result.h1_diagram)
                persistences.append(stats['mean'])

        mid_frame = window_frames[window_size // 2]
        rows.append({
            'window_idx': window_idx,
            'timestamp': mid_frame.timestamp,
            'period': mid_frame.period,
            'scale': scale,
            'match_id': match.info.match_id,
            'h1_count_mean': float(np.mean(h1_counts)),
            'h1_presence': float(np.mean([1 if c > 0 else 0 for c in h1_counts])),
            'mean_persistence': float(np.mean(persistences)) if persistences else 0.0,
            'n_frames': len(window_frames),
        })
        window_idx += 1

    return pd.DataFrame(rows)


def half_comparison(df: pd.DataFrame) -> dict:
    """Compare first vs second half with statistical tests."""
    h1 = df[df['period'] == 1]['mean_persistence'].values
    h2 = df[df['period'] == 2]['mean_persistence'].values

    if len(h1) < 3 or len(h2) < 3:
        return {'error': 'Too few windows per half'}

    mean_h1 = float(np.mean(h1))
    mean_h2 = float(np.mean(h2))
    pct_change = float((mean_h2 - mean_h1) / mean_h1 * 100) if mean_h1 > 0 else 0.0

    stat_mwu, p_mwu = mannwhitneyu(h1, h2, alternative='two-sided')
    p_perm = _permutation_test(h1, h2, n_perm=10000)

    return {
        'n_first_half': int(len(h1)),
        'n_second_half': int(len(h2)),
        'mean_first_half': mean_h1,
        'mean_second_half': mean_h2,
        'pct_change': pct_change,
        'mannwhitney_stat': float(stat_mwu),
        'mannwhitney_p': float(p_mwu),
        'permutation_p': float(p_perm),
        'significant_005': bool(p_mwu < 0.05),
        'significant_001': bool(p_mwu < 0.01),
    }


def _permutation_test(a: np.ndarray, b: np.ndarray, n_perm: int = 10000) -> float:
    """Two-sided permutation test on difference of means."""
    observed = abs(np.mean(a) - np.mean(b))
    combined = np.concatenate([a, b])
    n_a = len(a)
    count = 0

    rng = np.random.default_rng(42)
    for _ in range(n_perm):
        perm = rng.permutation(combined)
        perm_diff = abs(np.mean(perm[:n_a]) - np.mean(perm[n_a:]))
        if perm_diff >= observed:
            count += 1

    return count / n_perm


def main():
    parser = argparse.ArgumentParser(description='Per-window temporal H1 persistence.')
    parser.add_argument(
        '--legacy-multi',
        action='store_true',
        help='SecondSpectrum fixture + first three SkillCorner matches (100-frame windows).',
    )
    args = parser.parse_args()

    print("=" * 70)
    print("STATISTICAL TESTS: TEMPORAL EVOLUTION")
    print("=" * 70)

    all_windows = []
    all_tests = {}

    def run_match_bundle(label: str, match: MatchData, wsize: int, wstep: int):
        mid = match.info.match_id
        name = f"{match.info.home_team} vs {match.info.away_team}"
        print(f"\n[{label}] {name} ({match.n_frames} frames, window={wsize})")

        for scale in ['individual', 'tactical']:
            print(f"  Computing {scale} scale persistence windows...")
            wdf = compute_window_persistence(
                match, scale, window_size=wsize, window_step=wstep,
            )
            all_windows.append(wdf)

            result = half_comparison(wdf)
            key = f"{mid}_{scale}"
            all_tests[key] = {
                'match_id': mid,
                'source': label,
                'match_name': name,
                'scale': scale,
                **result,
            }

            if 'error' not in result:
                sig = "***" if result['significant_001'] else ("*" if result['significant_005'] else "ns")
                print(
                    f"    H1 mean: {result['mean_first_half']:.3f} -> "
                    f"{result['mean_second_half']:.3f} ({result['pct_change']:+.1f}%), "
                    f"p={result['mannwhitney_p']:.4f} {sig}",
                )

    if not args.legacy_multi:
        try:
            match = skillcorner.load_match(
                PRIMARY_SKILLCORNER_ID,
                sample_every=1,
                require_complete=True,
            )
            run_match_bundle(
                'SkillCorner',
                match,
                WINDOW_SIZE_PRIMARY,
                WINDOW_STEP_PRIMARY,
            )
        except FileNotFoundError as exc:
            print(f"SkillCorner primary match not available: {exc}")
            return

    else:
        try:
            ss = secondspectrum.load_match(sample_every=1, require_complete=True)
            run_match_bundle('SecondSpectrum', ss, WINDOW_SIZE_LEGACY, WINDOW_STEP_LEGACY)
        except FileNotFoundError:
            print("SecondSpectrum not found")

        try:
            sc_list = skillcorner.list_matches()
            for m in sc_list[:3]:
                try:
                    sc = skillcorner.load_match(m['id'], sample_every=10, require_complete=True)
                    run_match_bundle('SkillCorner', sc, WINDOW_SIZE_LEGACY, WINDOW_STEP_LEGACY)
                except FileNotFoundError:
                    pass
        except FileNotFoundError:
            pass

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if all_windows:
        pd.concat(all_windows, ignore_index=True).to_csv(
            OUTPUT_DIR / 'per_window_persistence.csv', index=False,
        )

    with open(OUTPUT_DIR / 'temporal_tests.json', 'w') as f:
        json.dump(all_tests, f, indent=2, default=str)

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
