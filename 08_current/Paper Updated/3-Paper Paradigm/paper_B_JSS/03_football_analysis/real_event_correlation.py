#!/usr/bin/env python3
"""
Real Event Correlation
======================

Correlates H1 topological transitions with actual match events from
SkillCorner dynamic_events.csv and phases_of_play.csv. Replaces the
synthetic event approach in the original paper.

Addresses reviewer Issue 3 (synthetic events).

Outputs:
    results/event_correlation/event_topology_correlation.csv
    results/event_correlation/event_correlation_summary.json
"""

import argparse
import json
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

from loaders import skillcorner, MatchData
from tda_utils import compute_h1_at_scale, persistence_stats, VALIDATED_CUTOFFS

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'event_correlation'


def _event_window_frames() -> int:
    """Half-width in analysis frames; overridden by env ``EVENT_WINDOW_HALF`` (paper §3.8 sensitivity)."""
    v = os.environ.get("EVENT_WINDOW_HALF")
    if v is not None:
        return int(v)
    return 5


WB = _event_window_frames()
WINDOW_BEFORE = WB
WINDOW_AFTER = WB
SAMPLE_EVERY = 10   # every 10th frame = 1 Hz effective rate


def compute_per_frame_topology(match: MatchData, scale: str = 'tactical') -> pd.DataFrame:
    """Compute H1 statistics for every sampled frame."""
    cutoff = VALIDATED_CUTOFFS[scale]
    complete = match.complete_frames[::SAMPLE_EVERY]

    rows = []
    for fi, frame in enumerate(complete):
        result = compute_h1_at_scale(frame.all_positions, cutoff)
        stats = persistence_stats(result.h1_diagram)
        rows.append({
            'frame_idx': fi,
            'frame_id': frame.frame_id,
            'timestamp': frame.timestamp,
            'period': frame.period,
            'h0': result.h0_count,
            'h1': result.h1_count,
            'mean_persistence': stats['mean'],
            'total_persistence': stats['total'],
            'max_persistence': stats['max'],
        })

    return pd.DataFrame(rows)


def _parse_time_str(ts) -> float:
    """Parse 'MM:SS.S' or numeric to seconds."""
    if pd.isna(ts):
        return float('nan')
    if isinstance(ts, (int, float)):
        return float(ts)
    s = str(ts)
    try:
        if ':' in s:
            parts = s.split(':')
            return int(parts[0]) * 60 + float(parts[1])
        return float(s)
    except (ValueError, IndexError):
        return float('nan')


def align_events_to_topology(
    topo_df: pd.DataFrame,
    events_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    For each event, find the nearest topology frame and compute
    persistence change around the event.
    """
    # Determine time column (SkillCorner uses time_start/frame_start)
    time_col = None
    frame_col = None
    for c in ['time_start', 'start_time', 'time', 'timestamp']:
        if c in events_df.columns:
            time_col = c
            break
    for c in ['frame_start', 'frame']:
        if c in events_df.columns:
            frame_col = c
            break

    results = []
    topo_frames = topo_df['frame_id'].values
    topo_timestamps = topo_df['timestamp'].values

    for _, evt in events_df.iterrows():
        # Match by frame ID if available, else by time
        if frame_col and not pd.isna(evt.get(frame_col)):
            evt_frame = int(evt[frame_col])
            idx = np.argmin(np.abs(topo_frames - evt_frame))
        elif time_col:
            evt_time = _parse_time_str(evt.get(time_col))
            if np.isnan(evt_time):
                continue
            idx = np.argmin(np.abs(topo_timestamps - evt_time))
        else:
            continue

        if idx < WINDOW_BEFORE or idx >= len(topo_df) - WINDOW_AFTER:
            continue

        before = topo_df.iloc[idx - WINDOW_BEFORE:idx]
        after = topo_df.iloc[idx + 1:idx + WINDOW_AFTER + 1]
        at_event = topo_df.iloc[idx]

        mean_before = before['total_persistence'].mean()
        mean_after = after['total_persistence'].mean()
        delta = mean_after - mean_before

        etype = evt.get('event_type', evt.get('team_in_possession_phase_type', 'unknown'))
        team = evt.get('team_shortname', evt.get('team_in_possession_shortname', ''))

        results.append({
            'event_frame': int(topo_frames[idx]),
            'event_type': etype,
            'team': team,
            'h1_at_event': int(at_event['h1']),
            'mean_persistence_before': float(mean_before),
            'mean_persistence_after': float(mean_after),
            'persistence_delta': float(delta),
            'h1_before': float(before['h1'].mean()),
            'h1_after': float(after['h1'].mean()),
        })

    return pd.DataFrame(results)


def statistical_tests(corr_df: pd.DataFrame) -> dict:
    """Run statistical tests on event-topology correlations."""
    if len(corr_df) == 0:
        return {}

    results = {}

    for etype in corr_df['event_type'].unique():
        edf = corr_df[corr_df['event_type'] == etype]
        if len(edf) < 5:
            continue

        deltas = edf['persistence_delta'].values
        stat, p_val = mannwhitneyu(deltas, np.zeros(len(deltas)), alternative='two-sided')

        results[etype] = {
            'n_events': int(len(edf)),
            'mean_delta': float(np.mean(deltas)),
            'std_delta': float(np.std(deltas)),
            'mannwhitney_stat': float(stat),
            'p_value': float(p_val),
            'significant_005': bool(p_val < 0.05),
        }

    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--out-csv",
        type=Path,
        default=None,
        help="Where to write event_topology rows (default: results/event_correlation/event_topology_correlation.csv)",
    )
    args = p.parse_args()

    print("=" * 70)
    print("REAL EVENT CORRELATION ANALYSIS")
    print("=" * 70)
    if WINDOW_BEFORE != 5 or WINDOW_AFTER != 5:
        print(f"Event window half-width: {WINDOW_BEFORE} frames (EVENT_WINDOW_HALF)")

    sc_matches = skillcorner.list_matches()
    print(f"Found {len(sc_matches)} SkillCorner matches\n")

    all_corr = []

    for m in sc_matches:
        mid = m['id']
        try:
            match = skillcorner.load_match(mid, sample_every=1, require_complete=True)
        except FileNotFoundError:
            continue

        if match.n_frames < 100:
            print(f"  [{mid}] Too few frames ({match.n_frames}), skipping")
            continue

        print(f"[{mid}] {match.info.home_team} vs {match.info.away_team}: {match.n_frames} frames")

        for scale in ['individual', 'tactical']:
            topo_df = compute_per_frame_topology(match, scale)

            try:
                events = skillcorner.load_events(mid)
                corr = align_events_to_topology(topo_df, events)
                corr['match_id'] = mid
                corr['scale'] = scale
                corr['data_source'] = 'dynamic_events'
                all_corr.append(corr)
                print(f"  {scale}: {len(corr)} event-topology pairs from dynamic_events")
            except FileNotFoundError:
                pass

            try:
                phases = skillcorner.load_phases(mid)
                corr_p = align_events_to_topology(topo_df, phases)
                corr_p['match_id'] = mid
                corr_p['scale'] = scale
                corr_p['data_source'] = 'phases_of_play'
                all_corr.append(corr_p)
                print(f"  {scale}: {len(corr_p)} phase-topology pairs from phases_of_play")
            except FileNotFoundError:
                pass

    if not all_corr:
        print("\nNo event correlations computed. Exiting.")
        return

    corr_all = pd.concat(all_corr, ignore_index=True)

    out_csv = Path(args.out_csv) if args.out_csv else (OUTPUT_DIR / "event_topology_correlation.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    corr_all.to_csv(out_csv, index=False)

    tests = {}
    for scale in corr_all['scale'].unique():
        sd = corr_all[corr_all['scale'] == scale]
        tests[scale] = statistical_tests(sd)

    summary = {
        'n_matches': len(corr_all['match_id'].unique()),
        'n_events_total': len(corr_all),
        'statistical_tests': tests,
    }

    with open(OUTPUT_DIR / 'event_correlation_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\n{'=' * 70}")
    print("RESULTS")
    print(f"{'=' * 70}")
    print(f"Total event-topology pairs: {len(corr_all)}")

    for scale in corr_all['scale'].unique():
        print(f"\n{scale.upper()} scale:")
        for etype, t in tests.get(scale, {}).items():
            sig = "*" if t['significant_005'] else ""
            print(f"  {etype}: delta={t['mean_delta']:.3f}, p={t['p_value']:.4f}{sig} (n={t['n_events']})")

    print(f"\nResults saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
