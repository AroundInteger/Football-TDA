#!/usr/bin/env python3
"""
H1 Loop Analysis
================

Identifies H1 loops in player formations, tracks their persistence and
lifetimes across multiple spatial scales using the shared TDA pipeline.

Outputs:
    h1_loop_analysis/h1_loops_detailed.csv
    h1_loop_analysis/h1_loops_full_data.json
"""

import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import secondspectrum, skillcorner, MatchData
from tda_utils import compute_h1_at_scale, VALIDATED_CUTOFFS


def analyze_match(
    match: MatchData,
    sample_every: int = 1,
    max_frames: int = 150,
    scales: dict = None,
) -> pd.DataFrame:
    """
    Run multi-scale H1 analysis on a loaded match.

    Args:
        match: MatchData from any loader.
        sample_every: Analyse every Nth complete frame.
        max_frames: Maximum frames to analyse.
        scales: Dict of {name: cutoff_distance}. Defaults to VALIDATED_CUTOFFS.

    Returns:
        DataFrame with one row per detected H1 loop.
    """
    if scales is None:
        scales = VALIDATED_CUTOFFS

    complete = match.complete_frames
    selected = complete[::sample_every][:max_frames]
    print(f"Analysing {len(selected)} frames from {match.info.home_team} vs {match.info.away_team}")

    all_loop_data = []

    for frame_idx, frame in enumerate(selected):
        for scale_name, cutoff in scales.items():
            result = compute_h1_at_scale(frame.all_positions, cutoff)

            for loop_idx in range(result.h1_count):
                birth = float(result.h1_diagram[loop_idx, 0])
                death = float(result.h1_diagram[loop_idx, 1])

                all_loop_data.append({
                    'frame_idx': frame_idx,
                    'frame_id': frame.frame_id,
                    'timestamp': frame.timestamp,
                    'period': frame.period,
                    'scale': scale_name,
                    'cutoff': cutoff,
                    'loop_idx': loop_idx,
                    'birth': birth,
                    'death': death,
                    'persistence': death - birth,
                    'h0_count': result.h0_count,
                    'h1_count': result.h1_count,
                    'n_points': result.cluster_count,
                    'filtration': result.filtration_used,
                    'point_cloud': result.point_cloud.tolist(),
                    'match_id': match.info.match_id,
                    'source': match.info.source,
                })

        if (frame_idx + 1) % 50 == 0:
            print(f"  Processed {frame_idx + 1}/{len(selected)} frames...")

    return pd.DataFrame(all_loop_data)


def track_loop_lifetimes(loops_df: pd.DataFrame) -> pd.DataFrame:
    """Track loop lifetimes across consecutive frames."""
    lifetime_data = []

    for scale in loops_df['scale'].unique():
        scale_loops = loops_df[loops_df['scale'] == scale].sort_values(
            ['frame_idx', 'persistence'], ascending=[True, False]
        )
        current = []

        for frame_idx in scale_loops['frame_idx'].unique():
            frame_loops = scale_loops[scale_loops['frame_idx'] == frame_idx]

            for _, new_loop in frame_loops.iterrows():
                best_match = None
                best_diff = float('inf')

                for old_idx, old_loop in enumerate(current):
                    if old_loop['frame_idx'] == frame_idx - 1:
                        diff = abs(new_loop['persistence'] - old_loop['persistence'])
                        if diff < best_diff and diff < 2.0:
                            best_diff = diff
                            best_match = old_idx

                if best_match is not None:
                    lifetime_data.append({
                        'scale': scale,
                        'start_frame': current[best_match]['frame_idx'],
                        'end_frame': frame_idx,
                        'lifetime_frames': frame_idx - current[best_match]['frame_idx'] + 1,
                        'mean_persistence': (new_loop['persistence'] + current[best_match]['persistence']) / 2,
                    })

            records = frame_loops.to_dict('records')
            current = [r for r in current if r['frame_idx'] >= frame_idx - 5]
            current.extend(records)

    return pd.DataFrame(lifetime_data) if lifetime_data else pd.DataFrame()


def save_results(
    loops_df: pd.DataFrame,
    output_dir: Path,
    *,
    json_name: str = 'h1_loops_full_data.json',
    csv_name: str = 'h1_loops_detailed.csv',
):
    """Save loop analysis results to CSV and JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    export_df = loops_df.drop(columns=['point_cloud'], errors='ignore')
    export_df.to_csv(output_dir / csv_name, index=False)

    with open(output_dir / json_name, 'w') as f:
        json.dump(loops_df.to_dict('records'), f, indent=2)

    print(f"Results saved to {output_dir / json_name}")


def print_summary(loops_df: pd.DataFrame):
    """Print loop detection summary."""
    print("\n" + "=" * 60)
    print("LOOP SUMMARY")
    print("=" * 60)

    for scale in ['individual', 'tactical', 'team']:
        sl = loops_df[loops_df['scale'] == scale]
        if len(sl) > 0:
            n_frames_with = sl['frame_idx'].nunique()
            total_frames = loops_df['frame_idx'].nunique()
            print(f"\n{scale.upper()}:")
            print(f"  Loops: {len(sl)}")
            print(f"  Frames with loops: {n_frames_with}/{total_frames} ({100*n_frames_with/total_frames:.1f}%)")
            print(f"  Mean persistence: {sl['persistence'].mean():.3f} +/- {sl['persistence'].std():.3f}")
            print(f"  Max persistence: {sl['persistence'].max():.3f}")
        else:
            print(f"\n{scale.upper()}: No loops detected")


def _default_output_dir() -> Path:
    return PROJECT_ROOT / '04_h1_loops' / 'h1_loop_analysis'


def main():
    p = argparse.ArgumentParser(description='H1 loop extraction for one match (multi-scale).')
    p.add_argument(
        '--skillcorner',
        action='store_true',
        help='Load SkillCorner tracking (otherwise SecondSpectrum fixture).',
    )
    p.add_argument('--match-id', type=int, default=1996435, help='SkillCorner match ID.')
    p.add_argument(
        '--sample-every',
        type=int,
        default=None,
        help='Analyse every Nth complete frame in analyze_match '
        '(default: 100 for SkillCorner primary paper sample, same as loader for SecondSpectrum).',
    )
    p.add_argument(
        '--max-frames',
        type=int,
        default=150,
        help='Cap on analysis frames after subsampling.',
    )
    p.add_argument(
        '--no-require-complete',
        action='store_true',
        help='Allow incomplete frames instead of restricting to complete 22.',
    )
    p.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help=f'Directory for CSV/JSON (default: {_default_output_dir()}).',
    )
    p.add_argument(
        '--json-name',
        type=str,
        default=None,
        help='Filename for full loop JSON '
        '(default: h1_loops_skillcorner_<match-id>.json for SkillCorner, else h1_loops_full_data.json).',
    )
    p.add_argument(
        '--csv-name',
        type=str,
        default=None,
        help='Filename for loop summary CSV '
        '(default: h1_loops_skillcorner_<match-id>_detailed.csv for SkillCorner, else h1_loops_detailed.csv).',
    )
    args = p.parse_args()

    print('=' * 60)
    print('H1 LOOP ANALYSIS')
    print('=' * 60)

    out_dir = Path(args.output_dir) if args.output_dir else _default_output_dir()

    if args.skillcorner:
        samp = args.sample_every if args.sample_every is not None else 100
        # Sample in the loader so we do not ingest the full dense match (~40k frames).
        match =         skillcorner.load_match(
            args.match_id,
            sample_every=samp,
            require_complete=not args.no_require_complete,
            max_frames=args.max_frames,
        )
        loops_df = analyze_match(match, sample_every=1, max_frames=len(match.complete_frames))
        json_name = args.json_name or f'h1_loops_skillcorner_{args.match_id}.json'
        csv_name = args.csv_name or f'h1_loops_skillcorner_{args.match_id}_detailed.csv'
        lifelines = out_dir / f'loop_lifetimes_skillcorner_{args.match_id}.csv'
    else:
        samp_loader = args.sample_every if args.sample_every is not None else 100
        match = secondspectrum.load_match(
            sample_every=samp_loader,
            require_complete=not args.no_require_complete,
            max_frames=args.max_frames,
        )
        loops_df = analyze_match(match)
        json_name = args.json_name or 'h1_loops_full_data.json'
        csv_name = args.csv_name or 'h1_loops_detailed.csv'
        lifelines = out_dir / 'loop_lifetimes.csv'

    if len(loops_df) <= 0:
        print('No loops detected.')
        return

    save_results(loops_df, out_dir, json_name=json_name, csv_name=csv_name)
    print_summary(loops_df)
    lifetimes = track_loop_lifetimes(loops_df)
    if len(lifetimes) > 0:
        lifelines.parent.mkdir(parents=True, exist_ok=True)
        lifetimes.to_csv(lifelines, index=False)
        print(
            '\nLifetimes: ',
            len(lifetimes),
            ' tracked, mean=',
            f"{lifetimes['lifetime_frames'].mean():.1f}",
            ' frames',
            sep='',
        )


if __name__ == '__main__':
    main()
