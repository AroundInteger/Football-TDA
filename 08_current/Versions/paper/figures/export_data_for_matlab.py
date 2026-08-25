#!/usr/bin/env python3
"""
Export data from project results into clean CSV files for MATLAB figure generation.
Run from the Football-TDA root directory.

Reads H₁ loop records from ``TDA_H1_LOOPS_JSON`` if set; otherwise prefers
``04_h1_loops/h1_loop_analysis/h1_loops_skillcorner_1996435.json`` when present,
else ``h1_loops_full_data.json``.
"""
import csv
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.spatial.distance import pdist, squareform


def repo_root(from_path: Path) -> Path:
    for p in [from_path] + list(from_path.parents):
        if (p / '01_data').is_dir() and (p / '02_tda_core').is_dir():
            return p
    raise RuntimeError(f'Football-TDA repo root not found above {from_path}')


ROOT = repo_root(Path(__file__).resolve())
OUT = ROOT / '06_papers' / 'Paper1_MultiscaleTDA' / 'figures'


def loops_json_path() -> Path:
    env = os.environ.get('TDA_H1_LOOPS_JSON')
    if env:
        return Path(env).expanduser().resolve()
    primary = ROOT / '04_h1_loops' / 'h1_loop_analysis' / 'h1_loops_skillcorner_1996435.json'
    fallback = ROOT / '04_h1_loops' / 'h1_loop_analysis' / 'h1_loops_full_data.json'
    return primary if primary.exists() else fallback

# ── Figure 1: Cycle geometry data ──────────────────────────────────────────


def find_best_cycle(points, birth, death):
    """Reconstruct the BFS closed cycle from a point cloud and persistence interval."""
    pts = np.array(points)
    D = squareform(pdist(pts))
    n = len(pts)
    midpoint = (birth + death) / 2.0

    adj = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            if birth <= D[i, j] <= death:
                adj[i].append(j)
                adj[j].append(i)

    def bfs_cycles(start, max_len=8):
        cycles = []
        queue = [(start, [start])]
        seen = set()
        while queue:
            cur, path = queue.pop(0)
            if len(path) >= 4 and cur == start:
                key = tuple(sorted(path[:-1]))
                if key not in seen:
                    cycles.append(path[:-1])
                    seen.add(key)
            if len(path) < max_len:
                for nb in adj[cur]:
                    if len(path) == 1 or nb != path[-2]:
                        if nb == start and len(path) >= 3:
                            queue.append((nb, path + [nb]))
                        elif nb not in path:
                            queue.append((nb, path + [nb]))
        return cycles

    all_cycles = []
    for v in range(n):
        all_cycles.extend(bfs_cycles(v))

    if not all_cycles:
        connected = set()
        for i in range(n):
            for j in adj[i]:
                connected.add(i)
                connected.add(j)
        return sorted(connected)

    def score(cycle):
        edges = []
        for k in range(len(cycle)):
            i, j = cycle[k], cycle[(k + 1) % len(cycle)]
            edges.append(D[i, j])
        return 1.0 / (1.0 + np.mean(np.abs(np.array(edges) - midpoint)))

    return max(all_cycles, key=score)


lp = loops_json_path()
print(f'Loading H1 loop data from {lp}')
with open(lp) as f:
    loops = json.load(f)

tactical = sorted([l for l in loops if l['scale'] == 'tactical'],
                  key=lambda x: x['persistence'], reverse=True)
best_tac = tactical[0]

individual = sorted([l for l in loops if l['scale'] == 'individual'],
                    key=lambda x: x['persistence'], reverse=True)
best_ind = individual[0]

print(f'  Tactical: frame {best_tac["frame_idx"]}, persistence {best_tac["persistence"]:.3f}')
print(f'  Individual: frame {best_ind["frame_idx"]}, persistence {best_ind["persistence"]:.3f}')

print('  Computing BFS cycles...')
tac_cycle = find_best_cycle(best_tac['point_cloud'], best_tac['birth'], best_tac['death'])
ind_cycle = find_best_cycle(best_ind['point_cloud'], best_ind['birth'], best_ind['death'])

print(f'  Tactical cycle nodes: {tac_cycle}')
print(f'  Individual cycle nodes: {ind_cycle}')

OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / 'fig1_tactical_points.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['node_idx', 'x', 'y', 'is_cycle_node'])
    for i, p in enumerate(best_tac['point_cloud']):
        w.writerow([i, p[0], p[1], 1 if i in tac_cycle else 0])

with open(OUT / 'fig1_tactical_cycle.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['order', 'node_idx'])
    for k, idx in enumerate(tac_cycle):
        w.writerow([k, idx])

with open(OUT / 'fig1_tactical_meta.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['birth', 'death', 'persistence', 'frame_idx', 'n_points'])
    w.writerow([best_tac['birth'], best_tac['death'], best_tac['persistence'],
                best_tac['frame_idx'], best_tac['n_points']])

with open(OUT / 'fig1_individual_points.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['node_idx', 'x', 'y', 'is_cycle_node'])
    for i, p in enumerate(best_ind['point_cloud']):
        w.writerow([i, p[0], p[1], 1 if i in ind_cycle else 0])

with open(OUT / 'fig1_individual_cycle.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['order', 'node_idx'])
    for k, idx in enumerate(ind_cycle):
        w.writerow([k, idx])

with open(OUT / 'fig1_individual_meta.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['birth', 'death', 'persistence', 'frame_idx', 'n_points'])
    w.writerow([best_ind['birth'], best_ind['death'], best_ind['persistence'],
                best_ind['frame_idx'], best_ind['n_points']])

print('  Figure 1 data exported.')

print('Copying temporal data...')
src = ROOT / 'results' / 'statistical_tests' / 'per_window_persistence.csv'
dst = OUT / 'fig2_temporal.csv'
if src.is_file():
    shutil.copy2(src, dst)
    print('  Figure 3 temporal data exported (fig2_temporal.csv).')
else:
    print(f'  WARNING: temporal source missing ({src}); skip fig2_temporal.csv.')

print('Exporting event correlation data...')
ec_path = ROOT / 'results' / 'event_correlation' / 'event_correlation_summary.json'
if not ec_path.is_file():
    print(f'  WARNING: {ec_path} missing; skip fig3_event_correlation.csv.')
    ec = None
else:
    with open(ec_path) as f:
        ec = json.load(f)

if ec is not None:
    with open(OUT / 'fig3_event_correlation.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['event_type', 'scale', 'n_events', 'mean_delta', 'std_delta', 'p_value', 'significant'])
        for scale in ['individual', 'tactical']:
            for etype, vals in ec['statistical_tests'][scale].items():
                w.writerow([
                    etype, scale, vals['n_events'], vals['mean_delta'],
                    vals['std_delta'], vals['p_value'],
                    1 if vals['significant_005'] else 0])
    print('  Figure 4 event-correlation CSV exported.')

print('  Event correlation export step finished.')

print('Exporting persistence diagram data...')
_ind_fid = best_ind['frame_idx']
_tac_fid = best_tac['frame_idx']
ind_loops = [
    l for l in loops
    if l['scale'] == 'individual' and l['frame_idx'] == _ind_fid
]
tac_loops = [
    l for l in loops
    if l['scale'] == 'tactical' and l['frame_idx'] == _tac_fid
]
if not ind_loops:
    ind_by_frame = {}
    for l in loops:
        if l['scale'] == 'individual':
            fid = l['frame_idx']
            ind_by_frame[fid] = ind_by_frame.get(fid, []) + [l]
    best_frame = max(ind_by_frame.items(), key=lambda x: len(x[1]))[0]
    ind_loops = ind_by_frame[best_frame]
if not tac_loops:
    tac_by_frame = {}
    for l in loops:
        if l['scale'] == 'tactical':
            fid = l['frame_idx']
            tac_by_frame[fid] = tac_by_frame.get(fid, []) + [l]
    if tac_by_frame:
        best_frame = max(tac_by_frame.items(), key=lambda x: len(x[1]))[0]
        tac_loops = tac_by_frame[best_frame]

with open(OUT / 'fig_persistence_individual.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['birth', 'death', 'persistence', 'frame_idx'])
    for l in ind_loops:
        w.writerow([l['birth'], l['death'], l['persistence'], l['frame_idx']])

with open(OUT / 'fig_persistence_tactical.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['birth', 'death', 'persistence', 'frame_idx'])
    for l in tac_loops:
        w.writerow([l['birth'], l['death'], l['persistence'], l['frame_idx']])

print('  Persistence diagram data exported.')
print('\nAll data exported to:', OUT)

OUT_MIRRORS = [
    ROOT / '08_current' / 'Paper Updated' / 'figures',
    ROOT / '08_current' / 'paper' / 'figures',
    ROOT / '08_current' / 'Versions' / 'paper' / 'figures',
]
for OUT_CURRENT in OUT_MIRRORS:
    OUT_CURRENT.mkdir(parents=True, exist_ok=True)
    for fn in OUT.glob('*.csv'):
        shutil.copy2(fn, OUT_CURRENT / fn.name)
    print('CSVs mirrored to:', OUT_CURRENT)
