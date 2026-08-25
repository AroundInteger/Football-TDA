#!/usr/bin/env python3
"""
Primary Match — Uniform 150-Frame Sampling Analysis
====================================================

Runs the same TDA pipeline as the main primary-match script but with
**150 uniformly sampled frames** (each analysed individually) instead
of 2-minute temporal windows. This matches the paper's "N analysis
windows" format used in Sections 3.1–3.4 and produces directly
comparable numbers for the results tables.

Outputs (written to results/primary_skillcorner/uniform_150/):
  - uniform_frame_results.csv    per-frame H0/H1 at individual + tactical + team
  - uniform_halftime_test.json   Wilcoxon rank-sum comparing halves
  - uniform_sensitivity_cutoff.csv
  - uniform_sensitivity_percentile.csv
  - uniform_summary.json         headline numbers for paper tables
  - uniform_closed_cycles.csv    representative cycle details

Usage:
    python 03_football_analysis/AvailableData/primary_match_uniform_sampling.py
"""

import sys
import json
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')

# Re-use infrastructure from the main script
_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))
from primary_match_skillcorner_analysis import (
    repo_root, ensure_match_assets, load_tracking_data,
    cutoff_cluster, adaptive_max_filtration, compute_ph, h1_at_cutoff,
    finite_persistence, VALIDATED_CUTOFFS, EXPECTED_H0, FPS, OUTPUT_DIR,
)

PROJECT_ROOT = repo_root(_THIS_DIR)
UNIFORM_DIR = OUTPUT_DIR / 'uniform_150'
UNIFORM_DIR.mkdir(parents=True, exist_ok=True)

N_SAMPLE = 150


def run_uniform_analysis(frames: list, n_sample: int = N_SAMPLE):
    """
    Analyse n_sample uniformly-spaced frames at individual, tactical,
    and team scales.  Each frame is one analysis window.
    """
    step = max(1, len(frames) // n_sample)
    sample = frames[::step][:n_sample]
    print(f"Uniform sampling: {len(sample)} frames (every {step}th of {len(frames)})")

    records = []
    for i, frame in enumerate(sample):
        pos = frame['positions']
        period = frame['period']
        ts = frame['timestamp']

        row = {
            'frame_idx': i,
            'period': period,
            'timestamp': ts,
            'n_players': len(pos),
        }

        for scale, cutoff in VALIDATED_CUTOFFS.items():
            h0_d, h1_d, centroids, max_filt = h1_at_cutoff(pos, cutoff)
            pers = finite_persistence(h1_d)

            row[f'h0_{scale}'] = len(h0_d)
            row[f'h1_{scale}'] = len(h1_d)
            row[f'n_centroids_{scale}'] = len(centroids)
            row[f'max_filt_{scale}'] = round(max_filt, 2)
            row[f'mean_pers_{scale}'] = round(float(np.mean(pers)), 4) if len(pers) > 0 else 0.0
            row[f'max_pers_{scale}'] = round(float(np.max(pers)), 4) if len(pers) > 0 else 0.0
            row[f'total_pers_{scale}'] = round(float(np.sum(pers)), 4) if len(pers) > 0 else 0.0

        records.append(row)

        if (i + 1) % 25 == 0:
            print(f"  Frame {i+1}/{len(sample)}  "
                  f"H1_ind={row['h1_individual']}  H1_tac={row['h1_tactical']}  "
                  f"H1_team={row['h1_team']}")

    return pd.DataFrame(records)


def run_halftime_test(df: pd.DataFrame) -> dict:
    """Wilcoxon rank-sum on mean persistence between halves."""
    results = {}
    for scale in ['individual', 'tactical']:
        col = f'mean_pers_{scale}'
        h1_vals = df.loc[(df['period'] == 1) & (df[col] > 0), col].values
        h2_vals = df.loc[(df['period'] == 2) & (df[col] > 0), col].values

        if len(h1_vals) >= 3 and len(h2_vals) >= 3:
            stat, p = stats.mannwhitneyu(h1_vals, h2_vals, alternative='two-sided')
            pct = 100.0 * (np.mean(h2_vals) - np.mean(h1_vals)) / np.mean(h1_vals)
        else:
            stat, p, pct = None, None, None

        results[scale] = {
            'first_half_mean': round(float(np.mean(h1_vals)), 4) if len(h1_vals) else None,
            'second_half_mean': round(float(np.mean(h2_vals)), 4) if len(h2_vals) else None,
            'pct_change': round(float(pct), 2) if pct is not None else None,
            'stat': round(float(stat), 4) if stat is not None else None,
            'p': round(float(p), 6) if p is not None else None,
            'n1': int(len(h1_vals)),
            'n2': int(len(h2_vals)),
        }
    return results


def run_sensitivity_cutoff(frames: list, cutoffs=None, n_frames: int = N_SAMPLE):
    """Tactical-scale sensitivity across cutoff range (same 150-frame sample)."""
    if cutoffs is None:
        cutoffs = [6, 8, 10, 12, 14, 16, 17]
    step = max(1, len(frames) // n_frames)
    sample = frames[::step][:n_frames]

    records = []
    for cutoff in cutoffs:
        h1_counts, h0_counts, pers_all = [], [], []
        for frame in sample:
            h0_d, h1_d, _, _ = h1_at_cutoff(frame['positions'], float(cutoff))
            h1_counts.append(len(h1_d))
            h0_counts.append(len(h0_d))
            p = finite_persistence(h1_d)
            if len(p) > 0:
                pers_all.extend(p.tolist())

        records.append({
            'cutoff': cutoff,
            'h1_total': int(sum(h1_counts)),
            'h1_presence': round(float(np.mean([c > 0 for c in h1_counts])), 4),
            'mean_h0': round(float(np.mean(h0_counts)), 2),
            'mean_pers': round(float(np.mean(pers_all)), 4) if pers_all else 0.0,
        })
        r = records[-1]
        print(f"  delta={cutoff:4.1f}m  H1={r['h1_total']:4d}  "
              f"presence={r['h1_presence']:.1%}  H0={r['mean_h0']:.1f}")
    return pd.DataFrame(records)


def run_sensitivity_percentile(frames: list, pcts=None, cutoff=12.0, n_frames=N_SAMPLE):
    """Filtration percentile ablation at delta=12.0 m."""
    if pcts is None:
        pcts = [50, 60, 75, 90, 95]
    step = max(1, len(frames) // n_frames)
    sample = frames[::step][:n_frames]

    records = []
    for pct in pcts:
        h1_counts, filts = [], []
        for frame in sample:
            centroids, _ = cutoff_cluster(frame['positions'], cutoff)
            mf = adaptive_max_filtration(centroids, cutoff, pct=pct)
            _, h1_d = compute_ph(centroids, mf)
            h1_counts.append(len(h1_d))
            filts.append(mf)

        records.append({
            'percentile': pct,
            'h1_total': int(sum(h1_counts)),
            'h1_presence': round(float(np.mean([c > 0 for c in h1_counts])), 4),
            'mean_filtration': round(float(np.mean(filts)), 1),
        })
        r = records[-1]
        print(f"  P{pct:2d}  H1={r['h1_total']:4d}  "
              f"presence={r['h1_presence']:.1%}  filt={r['mean_filtration']:.1f}m")
    return pd.DataFrame(records)


def main():
    print("=" * 60)
    print(" Uniform 150-Frame Sampling — SkillCorner 1996435")
    print("=" * 60)

    ensure_match_assets()

    print("\n[1] Loading tracking data ...")
    frames, home, away = load_tracking_data(require_complete=True)
    match_name = f"{home} vs {away}"
    print(f"    {len(frames)} frames loaded")

    print("\n[2] Running uniform-sampling analysis ...")
    t0 = time.time()
    df = run_uniform_analysis(frames, n_sample=N_SAMPLE)
    print(f"    Done in {time.time()-t0:.1f}s  ({len(df)} frames analysed)")
    df.to_csv(UNIFORM_DIR / 'uniform_frame_results.csv', index=False)

    print("\n[3] Half-time Wilcoxon tests ...")
    ht = run_halftime_test(df)
    for scale, r in ht.items():
        pstr = f"{r['p']:.6f}" if r['p'] is not None else "N/A"
        pctstr = f"{r['pct_change']:+.1f}%" if r['pct_change'] is not None else "N/A"
        print(f"    {scale:12s}: 1st={r.get('first_half_mean','?')}  "
              f"2nd={r.get('second_half_mean','?')}  {pctstr}  p={pstr}")
    with open(UNIFORM_DIR / 'uniform_halftime_test.json', 'w') as f:
        json.dump(ht, f, indent=2)

    print("\n[4a] Tactical cutoff sensitivity ...")
    sens_cut = run_sensitivity_cutoff(frames)
    sens_cut.to_csv(UNIFORM_DIR / 'uniform_sensitivity_cutoff.csv', index=False)

    print("\n[4b] Filtration percentile ablation ...")
    sens_pct = run_sensitivity_percentile(frames)
    sens_pct.to_csv(UNIFORM_DIR / 'uniform_sensitivity_percentile.csv', index=False)

    # Compile summary
    n_frames_analysed = len(df)
    h0_stats = {}
    h1_stats = {}
    for scale in ['individual', 'tactical', 'team']:
        h0_col = f'h0_{scale}'
        h1_col = f'h1_{scale}'
        pers_col = f'mean_pers_{scale}'
        maxp_col = f'max_pers_{scale}'

        h0_stats[scale] = {
            'mean': round(float(df[h0_col].mean()), 2),
            'std': round(float(df[h0_col].std()), 2),
            'min': int(df[h0_col].min()),
            'max': int(df[h0_col].max()),
        }

        total_h1 = int(df[h1_col].sum())
        frames_with = int((df[h1_col] > 0).sum())
        presence = round(float((df[h1_col] > 0).mean()), 4)
        nonzero_pers = df.loc[df[pers_col] > 0, pers_col]
        nonzero_maxp = df.loc[df[maxp_col] > 0, maxp_col]

        h1_stats[scale] = {
            'total_loops': total_h1,
            'frames_with_loops': frames_with,
            'frames_total': n_frames_analysed,
            'presence_rate': presence,
            'mean_loops_per_frame': round(float(df[h1_col].mean()), 3),
            'mean_persistence': round(float(nonzero_pers.mean()), 3) if len(nonzero_pers) > 0 else 0.0,
            'std_persistence': round(float(nonzero_pers.std()), 3) if len(nonzero_pers) > 1 else 0.0,
            'max_persistence': round(float(nonzero_maxp.max()), 3) if len(nonzero_maxp) > 0 else 0.0,
        }

    summary = {
        'match_id': 1996435,
        'match_name': match_name,
        'source': 'SkillCorner broadcast tracking (open data)',
        'fps': FPS,
        'total_frames_in_match': len(frames),
        'n_frames_analysed': n_frames_analysed,
        'sampling': f'every {max(1, len(frames) // N_SAMPLE)}th frame',
        'h0': h0_stats,
        'h1': h1_stats,
        'halftime': ht,
        'sensitivity_cutoff': sens_cut.to_dict(orient='records'),
        'sensitivity_percentile': sens_pct.to_dict(orient='records'),
    }

    with open(UNIFORM_DIR / 'uniform_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Print results table
    print("\n" + "=" * 70)
    print(" UNIFORM 150-FRAME RESULTS — for paper table comparison")
    print("=" * 70)
    print(f"\nMatch: {match_name}  (SkillCorner ID 1996435)")
    print(f"Frames analysed: {n_frames_analysed} of {len(frames)} "
          f"(every {max(1, len(frames)//N_SAMPLE)}th)")

    print(f"\n--- H0 (connected components) ---")
    for scale in ['individual', 'tactical', 'team']:
        s = h0_stats[scale]
        print(f"  {scale:12s}: {s['mean']:.2f} +/- {s['std']:.2f}  "
              f"range [{s['min']}, {s['max']}]")

    print(f"\n--- H1 (loops) ---")
    fmt = "{scale:12s}  total={total:5d}  presence={pres:6.1%}  "
    fmt += "mean/frame={mpf:.2f}  mean_pers={mp:.3f}m  max_pers={xp:.3f}m"
    for scale in ['individual', 'tactical', 'team']:
        s = h1_stats[scale]
        print(f"  " + fmt.format(
            scale=scale,
            total=s['total_loops'],
            pres=s['presence_rate'],
            mpf=s['mean_loops_per_frame'],
            mp=s['mean_persistence'],
            xp=s['max_persistence'],
        ))

    print(f"\n--- Half-time comparison ---")
    for scale in ['individual', 'tactical']:
        r = ht[scale]
        pstr = f"{r['p']:.6f}" if r['p'] is not None else "N/A"
        pctstr = f"{r['pct_change']:+.1f}%" if r['pct_change'] is not None else "N/A"
        print(f"  {scale:12s}: 1st={r.get('first_half_mean','?')}  "
              f"2nd={r.get('second_half_mean','?')}  change={pctstr}  p={pstr}")

    print(f"\n--- Sensitivity (tactical cutoff) ---")
    print(sens_cut.to_string(index=False))

    print(f"\n--- Sensitivity (filtration percentile) ---")
    print(sens_pct.to_string(index=False))

    print(f"\nAll results saved to: {UNIFORM_DIR}/")
    print("=" * 70)


if __name__ == '__main__':
    main()
