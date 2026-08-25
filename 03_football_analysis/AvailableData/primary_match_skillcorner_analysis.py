#!/usr/bin/env python3
"""
Primary Match Analysis: SkillCorner Match 1996435 (Sydney FC vs Adelaide United)
================================================================================

Replaces the SecondSpectrum 'primary match' role with fully open-access
SkillCorner broadcast tracking data. Runs:

  1. Cutoff distance parameter sweep (0.5–30.0 m, 100 test points, 4 epoch lengths)
     — recovers individual / tactical / team regimes via CH, silhouette, info-content
  2. Temporal analysis (2-min non-overlapping windows, Wilcoxon half-time test)
  3. Sensitivity analysis (tactical cutoff 6–17 m; filtration percentile P50–P95)

Outputs (all written to results/primary_skillcorner/):
  - cutoff_sweep_results.csv       raw per-(cutoff, epoch, window) stats
  - regime_summary.csv             three identified regimes + validation rates
  - temporal_windows.csv           per-window H0/H1 at individual + tactical scales
  - temporal_halftime_test.json    Wilcoxon results comparing halves
  - sensitivity_cutoff.csv         H1 counts/presence across tactical cutoff range
  - sensitivity_percentile.csv     H1 counts across filtration percentile ablation
  - analysis_summary.json          headline numbers for paper tables

Run from the project root:
    python 03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py

Alternatively, clone https://github.com/SkillCorner/opendata into ``01_data/opendata`` so that
``data/matches/1996435/`` contains the match assets (see ``01_data/SKILLCORNER_DATA_INTEGRATION_PLAN.md``).

The script will attempt to download tracking JSONL and ``1996435_match.json`` if not already present.
"""

import sys
import json
import warnings
import time
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

warnings.filterwarnings('ignore')


def repo_root(start: Path) -> Path:
    """Walk parents until Football-TDA repo root (has ``01_data`` and ``02_tda_core``)."""
    p = start.resolve()
    for _ in range(12):
        if (p / '01_data').is_dir() and (p / '02_tda_core').is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise RuntimeError(
        f"Could not find project root from {start}; expected ancestors to contain "
        "both '01_data' and '02_tda_core'."
    )


# ---------------------------------------------------------------------------
#  Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(PROJECT_ROOT / '01_data'))
sys.path.insert(0, str(PROJECT_ROOT / '02_tda_core'))

OPENDATA_ROOT  = PROJECT_ROOT / '01_data' / 'opendata' / 'data'
MATCH_ID       = 1996435
MATCH_DIR      = OPENDATA_ROOT / 'matches' / str(MATCH_ID)
TRACKING_FILE  = MATCH_DIR / f'{MATCH_ID}_tracking_extrapolated.jsonl'
MATCH_JSON     = MATCH_DIR / f'{MATCH_ID}_match.json'
EVENTS_FILE    = MATCH_DIR / f'{MATCH_ID}_dynamic_events.csv'
PHASES_FILE    = MATCH_DIR / f'{MATCH_ID}_phases_of_play.csv'

OUTPUT_DIR = PROJECT_ROOT / 'results' / 'primary_skillcorner'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FPS = 10.0   # SkillCorner broadcast tracking rate

# ---------------------------------------------------------------------------
#  Validated scale parameters (carry over from paper)
# ---------------------------------------------------------------------------
VALIDATED_CUTOFFS = {'individual': 2.98, 'tactical': 12.0, 'team': 30.0}
EXPECTED_H0 = {'individual': (15, 22), 'tactical': (2, 12), 'team': (1, 3)}

# ---------------------------------------------------------------------------
#  Step 0: Download match assets if absent
# ---------------------------------------------------------------------------

def _github_media_url(filename: str) -> str:
    return (
        f"https://media.githubusercontent.com/media/SkillCorner/opendata/master"
        f"/data/matches/{MATCH_ID}/{filename}"
    )


def ensure_match_assets() -> Path:
    """Download tracking JSONL and match.json from GitHub if not already on disk."""
    import urllib.request

    MATCH_DIR.mkdir(parents=True, exist_ok=True)

    # --- match.json (small; required for player→team mapping)
    if MATCH_JSON.exists() and MATCH_JSON.stat().st_size > 100:
        print(f"Match metadata already present ({MATCH_JSON.stat().st_size / 1024:.1f} KB)")
    else:
        url = _github_media_url(f'{MATCH_ID}_match.json')
        print(f"Downloading match metadata from:\n  {url}")
        try:
            t0 = time.time()
            urllib.request.urlretrieve(url, MATCH_JSON)
            print(f"  Downloaded {MATCH_JSON.stat().st_size / 1024:.1f} KB in {time.time()-t0:.1f}s")
        except Exception as exc:
            print(f"\n  ERROR downloading match.json: {exc}")
            print("  Manual download or clone SkillCorner/opendata — see module docstring.")
            print(f"    wget '{url}' -O '{MATCH_JSON}'")
            sys.exit(1)

    # --- tracking JSONL (large)
    if TRACKING_FILE.exists() and TRACKING_FILE.stat().st_size > 1_000_000:
        print(f"Tracking data already present ({TRACKING_FILE.stat().st_size / 1e6:.1f} MB)")
        return TRACKING_FILE

    url = _github_media_url(f'{MATCH_ID}_tracking_extrapolated.jsonl')
    print(f"Downloading tracking data from:\n  {url}")
    print("  (this is ~100 MB — may take 1–2 minutes on a typical connection)")

    try:
        t0 = time.time()
        urllib.request.urlretrieve(url, TRACKING_FILE)
        size_mb = TRACKING_FILE.stat().st_size / 1e6
        print(f"  Downloaded {size_mb:.1f} MB in {time.time()-t0:.1f}s")
    except Exception as exc:
        print(f"\n  ERROR downloading: {exc}")
        print("  Manual download:")
        print(f"    wget '{url}' -O '{TRACKING_FILE}'")
        sys.exit(1)

    return TRACKING_FILE


# ---------------------------------------------------------------------------
#  Step 1: Load tracking data
# ---------------------------------------------------------------------------

def load_tracking_data(max_frames: int = None, require_complete: bool = True):
    """
    Load all frames from the SkillCorner JSONL file.

    Returns
    -------
    frames : list of dict  {positions: np.ndarray (n,2), period: int, timestamp: float}
    """
    import json

    # Load match JSON for team/player mapping
    with open(MATCH_JSON) as f:
        match_meta = json.load(f)

    # Build player → team map
    home_team = match_meta.get('home_team', {})
    away_team = match_meta.get('away_team', {})
    home_id = home_team.get('id', home_team.get('team_id', -1))
    away_id = away_team.get('id', away_team.get('team_id', -2))
    home_name = home_team.get('short_name', home_team.get('name', 'Home'))
    away_name = away_team.get('short_name', away_team.get('name', 'Away'))

    player_map = {}  # trackable_object_id → 'home' | 'away'
    for player in match_meta.get('players', []):
        tid = player.get('team_id')
        if tid is None:
            continue
        team = 'home' if tid == home_id else ('away' if tid == away_id else None)
        if team is None:
            continue
        for key in ['trackable_object', 'id']:
            pid = player.get(key)
            if pid is not None:
                player_map[pid] = team

    print(f"Match: {home_name} vs {away_name}  (ID {MATCH_ID})")
    print(f"Player map entries: {len(player_map)}")

    frames = []
    t_start = time.time()

    with open(TRACKING_FILE) as f:
        for i, line in enumerate(f):
            if max_frames and len(frames) >= max_frames:
                break
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            all_pos, home_pos, away_pos = [], [], []
            for p in data.get('player_data', []):
                x, y = p.get('x'), p.get('y')
                pid   = p.get('player_id')
                if x is None or y is None or pid is None:
                    continue
                team = player_map.get(pid)
                if team == 'home':
                    home_pos.append([x, y])
                elif team == 'away':
                    away_pos.append([x, y])

            all_pos = home_pos + away_pos
            if require_complete and len(all_pos) != 22:
                continue
            if len(all_pos) < 10:
                continue

            # Parse timestamp (MM:SS.s  or float seconds)
            ts_raw = data.get('timestamp', '')
            try:
                if ':' in str(ts_raw):
                    parts = str(ts_raw).split(':')
                    ts = int(parts[0]) * 60 + float(parts[1])
                else:
                    ts = float(ts_raw) if ts_raw else i / FPS
            except Exception:
                ts = i / FPS

            period = int(data.get('period', 1))

            frames.append({
                'positions': np.array(all_pos, dtype=np.float64),
                'period': period,
                'timestamp': ts,
                'frame_id': data.get('frame', i),
                'n_players': len(all_pos),
            })

            if (i + 1) % 10000 == 0:
                print(f"  ... {i+1} lines read, {len(frames)} valid frames")

    print(f"Loaded {len(frames)} frames in {time.time()-t_start:.1f}s")
    return frames, home_name, away_name


# ---------------------------------------------------------------------------
#  Core TDA helpers (self-contained; mirrors tda_utils.py)
# ---------------------------------------------------------------------------

def cutoff_cluster(positions: np.ndarray, cutoff: float, method: str = 'single'):
    """Single-linkage hierarchical clustering at given cutoff."""
    if len(positions) <= 1:
        return positions.copy(), np.zeros(len(positions), dtype=int)
    dists = pdist(positions)
    Z = linkage(dists, method=method)
    labels = fcluster(Z, cutoff, criterion='distance')
    unique = np.unique(labels)
    centroids = np.array([positions[labels == u].mean(axis=0) for u in unique])
    return centroids, labels


def adaptive_max_filtration(centroids: np.ndarray, cutoff: float, pct: int = 75) -> float:
    """εmax = max(P_pct(pairwise distances), max(5.0, 2*cutoff))."""
    if len(centroids) <= 1:
        return max(5.0, 2.0 * cutoff)
    dists = pdist(centroids)
    data_driven = float(np.percentile(dists, pct))
    scale_min   = max(5.0, 2.0 * cutoff)
    return max(data_driven, scale_min)


def compute_ph(point_cloud: np.ndarray, max_filt: float):
    """Vietoris–Rips persistent homology via ripser. Returns (h0_dgm, h1_dgm)."""
    from ripser import ripser as _ripser
    if len(point_cloud) <= 1:
        return np.empty((0, 2)), np.empty((0, 2))
    try:
        res = _ripser(point_cloud, maxdim=1, thresh=max_filt)
        return res['dgms'][0], res['dgms'][1]
    except Exception:
        return np.empty((0, 2)), np.empty((0, 2))


def h1_at_cutoff(positions: np.ndarray, cutoff: float, pct: int = 75):
    """Full pipeline: cluster → adaptive filtration → PH. Returns (h0_dgm, h1_dgm, centroids)."""
    centroids, _ = cutoff_cluster(positions, cutoff)
    max_filt = adaptive_max_filtration(centroids, cutoff, pct=pct)
    h0, h1 = compute_ph(centroids, max_filt)
    return h0, h1, centroids, max_filt


def finite_persistence(diagram: np.ndarray) -> np.ndarray:
    """Return finite persistence values from a diagram."""
    if len(diagram) == 0:
        return np.array([])
    mask = np.isfinite(diagram[:, 1])
    return diagram[mask, 1] - diagram[mask, 0]


def info_content(labels: np.ndarray) -> float:
    """Entropy of cluster size distribution as information content metric."""
    unique, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs + 1e-12)))


# ---------------------------------------------------------------------------
#  Step 2: Cutoff parameter sweep
# ---------------------------------------------------------------------------

def run_cutoff_sweep(frames: list, n_cutoffs: int = 100, random_seed: int = 42):
    """
    Sweep cutoff distances 0.5–30.0 m across multiple epoch lengths.

    For each epoch length, sample 30 % of available non-overlapping windows
    uniformly (matching the paper's '30% coverage' normalisation).

    Returns
    -------
    df : pd.DataFrame with one row per (cutoff, epoch_key, window_idx)
    """
    np.random.seed(random_seed)
    cutoffs = np.linspace(0.5, 30.0, n_cutoffs)

    # Epoch sizes at 10 Hz
    epoch_configs = {
        '1min':  int(1  * 60 * FPS),   # 600 frames
        '2min':  int(2  * 60 * FPS),   # 1200 frames
        '5min':  int(5  * 60 * FPS),   # 3000 frames
        '10min': int(10 * 60 * FPS),   # 6000 frames
    }

    total_frames = len(frames)
    records = []

    for epoch_key, epoch_size in epoch_configs.items():
        # Build non-overlapping window start indices
        n_windows = total_frames // epoch_size
        all_starts = [i * epoch_size for i in range(n_windows)]

        # 30 % sample (min 3 windows)
        n_sample = max(3, int(0.30 * n_windows))
        sampled_starts = sorted(
            np.random.choice(all_starts, size=min(n_sample, len(all_starts)), replace=False)
        )

        print(f"  Epoch {epoch_key}: {n_windows} windows → sampling {len(sampled_starts)}")

        for win_idx, start in enumerate(sampled_starts):
            win_frames = frames[start: start + epoch_size]
            if not win_frames:
                continue

            # Mean positions for the window (representative frame = median frame)
            mid_idx = len(win_frames) // 2
            positions = win_frames[mid_idx]['positions']

            for cutoff in cutoffs:
                centroids, labels = cutoff_cluster(positions, cutoff)
                n_clusters = len(centroids)

                # Clustering quality metrics (need ≥2 clusters, ≥2 samples)
                ch_score = 0.0
                sil_score = 0.0
                if len(positions) > 2 and n_clusters > 1 and n_clusters < len(positions):
                    try:
                        ch_score = float(calinski_harabasz_score(positions, labels))
                    except Exception:
                        pass
                    try:
                        sil_score = float(silhouette_score(positions, labels))
                    except Exception:
                        pass

                ic = info_content(labels)

                # H0 validation: is n_clusters in expected range?
                in_individual = EXPECTED_H0['individual'][0] <= n_clusters <= EXPECTED_H0['individual'][1]
                in_tactical   = EXPECTED_H0['tactical'][0]   <= n_clusters <= EXPECTED_H0['tactical'][1]
                in_team       = EXPECTED_H0['team'][0]       <= n_clusters <= EXPECTED_H0['team'][1]

                records.append({
                    'cutoff':       round(float(cutoff), 4),
                    'epoch':        epoch_key,
                    'win_idx':      win_idx,
                    'n_clusters':   n_clusters,
                    'ch_score':     ch_score,
                    'sil_score':    sil_score,
                    'info_content': ic,
                    'h0_in_individual': in_individual,
                    'h0_in_tactical':   in_tactical,
                    'h0_in_team':       in_team,
                })

    df = pd.DataFrame(records)
    print(f"Cutoff sweep complete: {len(df)} records")
    return df


def identify_regimes(sweep_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify three validated regimes from sweep results.

    Strategy:
    - Individual: cutoff that maximises CH score (averaged across epochs)
    - Team:       cutoff that maximises info_content (captures single-cluster transition)
    - Tactical:   domain-informed selection within [6, 17] m where tactical H0 validated ≥90%

    Returns a DataFrame with one row per regime.
    """
    # Aggregate across epochs & windows
    agg = (
        sweep_df
        .groupby('cutoff')
        .agg(
            mean_n_clusters  = ('n_clusters',   'mean'),
            std_n_clusters   = ('n_clusters',   'std'),
            mean_ch          = ('ch_score',     'mean'),
            mean_sil         = ('sil_score',    'mean'),
            mean_ic          = ('info_content', 'mean'),
            val_individual   = ('h0_in_individual', 'mean'),
            val_tactical     = ('h0_in_tactical',   'mean'),
            val_team         = ('h0_in_team',        'mean'),
        )
        .reset_index()
    )

    # Individual regime: max CH score
    idx_ind = agg['mean_ch'].idxmax()
    cutoff_individual = float(agg.loc[idx_ind, 'cutoff'])
    val_individual    = float(agg.loc[idx_ind, 'val_individual'])

    # Team regime: max info_content (high IC = all players in one cluster = flat distribution)
    # Actually, team scale = min IC (one big cluster) → find the cutoff where IC drops
    # and H0_in_team validation is highest
    team_candidates = agg[agg['val_team'] > 0.9]
    if len(team_candidates) > 0:
        idx_team = team_candidates['mean_ic'].idxmin()
        cutoff_team = float(team_candidates.loc[idx_team, 'cutoff'])
        val_team    = float(team_candidates.loc[idx_team, 'val_team'])
    else:
        # Fallback: highest H0 team validation
        idx_team = agg['val_team'].idxmax()
        cutoff_team = float(agg.loc[idx_team, 'cutoff'])
        val_team    = float(agg.loc[idx_team, 'val_team'])

    # Tactical: domain-informed at 12.0 m, validated in [6, 17] m range
    # Report validation rate at exactly 12.0 m (nearest point)
    nearest_12 = agg.iloc[(agg['cutoff'] - 12.0).abs().argsort()[:1]]
    cutoff_tactical = 12.0
    val_tactical    = float(nearest_12['val_tactical'].values[0])

    # Compute stability scores: fraction of windows where H0 stays within ±2 of median
    stability = {}
    for scale, cutoff_val in [
        ('individual', cutoff_individual),
        ('tactical',   cutoff_tactical),
        ('team',       cutoff_team),
    ]:
        subset = sweep_df[np.abs(sweep_df['cutoff'] - cutoff_val) < 0.5]
        if len(subset) > 0:
            med = subset['n_clusters'].median()
            stable = (np.abs(subset['n_clusters'] - med) <= 2).mean()
            stability[scale] = float(stable)
        else:
            stability[scale] = 0.0

    regimes = pd.DataFrame([
        {
            'scale':          'individual',
            'optimal_cutoff': round(cutoff_individual, 2),
            'validation_rate': round(val_individual, 3),
            'stability':       round(stability['individual'], 3),
            'expected_h0_lo':  EXPECTED_H0['individual'][0],
            'expected_h0_hi':  EXPECTED_H0['individual'][1],
            'selection_method': 'CH optimum',
        },
        {
            'scale':          'tactical',
            'optimal_cutoff': cutoff_tactical,
            'validation_rate': round(val_tactical, 3),
            'stability':       round(stability['tactical'], 3),
            'expected_h0_lo':  EXPECTED_H0['tactical'][0],
            'expected_h0_hi':  EXPECTED_H0['tactical'][1],
            'selection_method': 'domain-informed (12.0 m)',
        },
        {
            'scale':          'team',
            'optimal_cutoff': round(cutoff_team, 2),
            'validation_rate': round(val_team, 3),
            'stability':       round(stability['team'], 3),
            'expected_h0_lo':  EXPECTED_H0['team'][0],
            'expected_h0_hi':  EXPECTED_H0['team'][1],
            'selection_method': 'IC / H0 team validation',
        },
    ])

    return regimes, agg


# ---------------------------------------------------------------------------
#  Step 3: Temporal analysis (2-min non-overlapping windows)
# ---------------------------------------------------------------------------

def run_temporal_analysis(frames: list, window_size_min: float = 2.0):
    """
    Compute H0 and H1 at individual + tactical scales for each 2-min window.

    Returns
    -------
    df : pd.DataFrame   one row per window
    """
    window_size = int(window_size_min * 60 * FPS)  # frames
    total = len(frames)
    n_windows = total // window_size

    print(f"Temporal analysis: {n_windows} non-overlapping {window_size_min:.0f}-min windows "
          f"({window_size} frames each)")

    records = []

    for win_i in range(n_windows):
        start = win_i * window_size
        end   = start + window_size
        win   = frames[start:end]

        # Representative set: all frames (compute mean H stats over window)
        h0_ind_list, h1_ind_list = [], []
        h0_tac_list, h1_tac_list = [], []
        pers_ind_list, pers_tac_list = [], []

        # Sample every 10th frame within the window for speed
        sample_step = max(1, len(win) // 60)
        sampled = win[::sample_step]

        for frame in sampled:
            pos = frame['positions']

            # Individual scale
            h0_i, h1_i, _, _ = h1_at_cutoff(pos, VALIDATED_CUTOFFS['individual'])
            h0_ind_list.append(len(h0_i))
            h1_ind_list.append(len(h1_i))
            p_i = finite_persistence(h1_i)
            pers_ind_list.append(float(np.mean(p_i)) if len(p_i) > 0 else 0.0)

            # Tactical scale
            h0_t, h1_t, _, _ = h1_at_cutoff(pos, VALIDATED_CUTOFFS['tactical'])
            h0_tac_list.append(len(h0_t))
            h1_tac_list.append(len(h1_t))
            p_t = finite_persistence(h1_t)
            pers_tac_list.append(float(np.mean(p_t)) if len(p_t) > 0 else 0.0)

        # Window centre time
        mid_frame = win[len(win) // 2]
        t_centre   = mid_frame['timestamp']
        period     = mid_frame['period']

        records.append({
            'window':          win_i,
            'period':          period,
            't_start':         win[0]['timestamp'],
            't_end':           win[-1]['timestamp'],
            't_centre':        t_centre,

            'h0_individual':   float(np.mean(h0_ind_list)),
            'h1_individual':   float(np.mean(h1_ind_list)),
            'h1_ind_total':    int(np.sum(h1_ind_list)),
            'mean_pers_ind':   float(np.mean([p for p in pers_ind_list if p > 0]) if any(p > 0 for p in pers_ind_list) else 0.0),

            'h0_tactical':     float(np.mean(h0_tac_list)),
            'h1_tactical':     float(np.mean(h1_tac_list)),
            'h1_tac_total':    int(np.sum(h1_tac_list)),
            'mean_pers_tac':   float(np.mean([p for p in pers_tac_list if p > 0]) if any(p > 0 for p in pers_tac_list) else 0.0),
        })

        if (win_i + 1) % 5 == 0:
            print(f"  Window {win_i+1}/{n_windows}  t={t_centre/60:.1f}min  "
                  f"H1_ind={np.mean(h1_ind_list):.2f}  H1_tac={np.mean(h1_tac_list):.2f}")

    return pd.DataFrame(records)


def run_halftime_tests(temporal_df: pd.DataFrame) -> dict:
    """
    Wilcoxon rank-sum (Mann-Whitney U) test comparing first vs second half.
    Mirrors Table 3 of the paper.
    """
    h1 = temporal_df[temporal_df['period'] == 1]['mean_pers_ind'].dropna().values
    h2 = temporal_df[temporal_df['period'] == 2]['mean_pers_ind'].dropna().values
    h1_tac = temporal_df[temporal_df['period'] == 1]['mean_pers_tac'].dropna().values
    h2_tac = temporal_df[temporal_df['period'] == 2]['mean_pers_tac'].dropna().values

    def wilcoxon(a, b):
        if len(a) < 3 or len(b) < 3:
            return {'stat': None, 'p': None, 'n1': len(a), 'n2': len(b)}
        stat, p = stats.mannwhitneyu(a, b, alternative='two-sided')
        return {'stat': float(stat), 'p': float(p), 'n1': len(a), 'n2': len(b)}

    results = {
        'individual': {
            'first_half_mean':  float(np.mean(h1))  if len(h1)  else None,
            'second_half_mean': float(np.mean(h2))  if len(h2)  else None,
            'pct_change':       float(100*(np.mean(h2)-np.mean(h1))/np.mean(h1)) if len(h1) and len(h2) and np.mean(h1) > 0 else None,
            **wilcoxon(h1, h2),
        },
        'tactical': {
            'first_half_mean':  float(np.mean(h1_tac)) if len(h1_tac) else None,
            'second_half_mean': float(np.mean(h2_tac)) if len(h2_tac) else None,
            'pct_change':       float(100*(np.mean(h2_tac)-np.mean(h1_tac))/np.mean(h1_tac)) if len(h1_tac) and len(h2_tac) and np.mean(h1_tac) > 0 else None,
            **wilcoxon(h1_tac, h2_tac),
        },
    }
    return results


# ---------------------------------------------------------------------------
#  Step 4: Sensitivity analysis
# ---------------------------------------------------------------------------

def run_sensitivity_cutoff(frames: list, cutoffs: list = None, n_frames: int = 150):
    """
    H1 detection across tactical cutoff range 6–17 m on a sample of frames.
    Mirrors Table 4 (cutoff sensitivity) in the paper.
    """
    if cutoffs is None:
        cutoffs = [6, 8, 10, 12, 14, 16, 17]

    # Sample n_frames uniformly across the match
    step = max(1, len(frames) // n_frames)
    sample = frames[::step][:n_frames]

    records = []
    for cutoff in cutoffs:
        h1_counts, h0_counts = [], []
        for frame in sample:
            h0_d, h1_d, _, _ = h1_at_cutoff(frame['positions'], float(cutoff))
            h1_counts.append(len(h1_d))
            h0_counts.append(len(h0_d))

        records.append({
            'cutoff':      cutoff,
            'h1_total':    int(sum(h1_counts)),
            'h1_presence': float(np.mean([c > 0 for c in h1_counts])),
            'mean_h0':     float(np.mean(h0_counts)),
        })
        print(f"  δ={cutoff:4.1f}m  H1_total={records[-1]['h1_total']:4d}  "
              f"presence={records[-1]['h1_presence']:.1%}  mean_H0={records[-1]['mean_h0']:.1f}")

    return pd.DataFrame(records)


def run_sensitivity_percentile(frames: list, pcts: list = None, cutoff: float = 12.0, n_frames: int = 150):
    """
    Adaptive filtration percentile ablation at δ=12.0 m.
    Mirrors Table 5 (percentile sensitivity) in the paper.
    """
    if pcts is None:
        pcts = [50, 60, 75, 90, 95]

    step = max(1, len(frames) // n_frames)
    sample = frames[::step][:n_frames]

    records = []
    for pct in pcts:
        h1_counts, filtrations = [], []
        for frame in sample:
            centroids, _ = cutoff_cluster(frame['positions'], cutoff)
            max_filt = adaptive_max_filtration(centroids, cutoff, pct=pct)
            _, h1_d = compute_ph(centroids, max_filt)
            h1_counts.append(len(h1_d))
            filtrations.append(max_filt)

        records.append({
            'percentile':      pct,
            'h1_total':        int(sum(h1_counts)),
            'h1_presence':     float(np.mean([c > 0 for c in h1_counts])),
            'mean_filtration': float(np.mean(filtrations)),
        })
        print(f"  P{pct:2d}  H1_total={records[-1]['h1_total']:4d}  "
              f"presence={records[-1]['h1_presence']:.1%}  mean_filt={records[-1]['mean_filtration']:.1f}m")

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
#  Step 5: Figures
# ---------------------------------------------------------------------------

def make_figures(sweep_agg: pd.DataFrame, temporal_df: pd.DataFrame,
                 regimes: pd.DataFrame, match_name: str):
    """Generate the two key figures for the paper."""

    # --- Figure A: Cutoff sweep -----------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    ax = axes[0]
    ax.plot(sweep_agg['cutoff'], sweep_agg['mean_ch'], color='steelblue', lw=1.5)
    ax.set_xlabel('Cutoff distance (m)')
    ax.set_ylabel('Calinski–Harabász index (mean)')
    ax.set_title('CH optimum → Individual scale')
    ax.axvline(regimes.loc[regimes['scale']=='individual', 'optimal_cutoff'].values[0],
               color='red', linestyle='--', alpha=0.7, label='Individual cutoff')
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(sweep_agg['cutoff'], sweep_agg['val_individual'], label='Individual', lw=1.5)
    ax.plot(sweep_agg['cutoff'], sweep_agg['val_tactical'],   label='Tactical',   lw=1.5)
    ax.plot(sweep_agg['cutoff'], sweep_agg['val_team'],       label='Team',       lw=1.5)
    ax.set_xlabel('Cutoff distance (m)')
    ax.set_ylabel('H₀ validation rate')
    ax.set_title('Scale validation rates')
    ax.legend(fontsize=8)
    for cut, col in [(regimes.loc[regimes['scale']==s, 'optimal_cutoff'].values[0], c)
                     for s, c in [('individual','C0'),('tactical','C1'),('team','C2')]]:
        ax.axvline(cut, color=col, linestyle='--', alpha=0.5)

    ax = axes[2]
    ax.plot(sweep_agg['cutoff'], sweep_agg['mean_n_clusters'], color='darkorange', lw=1.5)
    ax.set_xlabel('Cutoff distance (m)')
    ax.set_ylabel('Mean H₀ (cluster count)')
    ax.set_title('Mean cluster count vs cutoff')
    for cut, lab in [(regimes.loc[regimes['scale']==s, 'optimal_cutoff'].values[0], s)
                     for s in ['individual', 'tactical', 'team']]:
        ax.axvline(cut, linestyle='--', alpha=0.6, label=lab)
    ax.legend(fontsize=8)

    fig.suptitle(f'Cutoff sweep — {match_name}', fontsize=11, y=1.01)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / 'fig_cutoff_sweep.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  Saved fig_cutoff_sweep.png")

    # --- Figure B: Temporal evolution -----------------------------------------
    if temporal_df is not None and len(temporal_df) > 0:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

        t_min = temporal_df['t_centre'] / 60.0
        c1 = temporal_df['period'] == 1

        ax1.plot(t_min[c1],  temporal_df['mean_pers_ind'][c1],  'b-o', ms=3, lw=1.2, label='1st half')
        ax1.plot(t_min[~c1], temporal_df['mean_pers_ind'][~c1], 'r-o', ms=3, lw=1.2, label='2nd half')
        ax1.set_ylabel('Mean H₁ persistence (m)')
        ax1.set_title('Individual scale (δ=2.98 m)')
        ax1.legend(fontsize=8)

        ax2.plot(t_min[c1],  temporal_df['mean_pers_tac'][c1],  'b-o', ms=3, lw=1.2, label='1st half')
        ax2.plot(t_min[~c1], temporal_df['mean_pers_tac'][~c1], 'r-o', ms=3, lw=1.2, label='2nd half')
        ax2.set_xlabel('Match time (min)')
        ax2.set_ylabel('Mean H₁ persistence (m)')
        ax2.set_title('Tactical scale (δ=12.0 m)')
        ax2.legend(fontsize=8)

        fig.suptitle(f'Temporal evolution of H₁ persistence — {match_name}', fontsize=11)
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / 'fig_temporal_evolution.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        print("  Saved fig_temporal_evolution.png")


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" Primary Match Analysis: SkillCorner 1996435")
    print(" Sydney FC vs Adelaide United (A-League 2024/25)")
    print("=" * 60)

    # 0. Ensure data is present
    ensure_match_assets()

    # 1. Load data
    print("\n[1] Loading tracking data …")
    frames, home_name, away_name = load_tracking_data(require_complete=True)
    match_name = f"{home_name} vs {away_name}"
    print(f"    {len(frames)} complete (22-player) frames loaded")

    # Quick summary stats
    periods = [f['period'] for f in frames]
    p1_frames = sum(1 for p in periods if p == 1)
    p2_frames = sum(1 for p in periods if p == 2)
    print(f"    Period 1: {p1_frames} frames  Period 2: {p2_frames} frames")
    print(f"    Approx duration: {len(frames)/FPS/60:.1f} min at {FPS:.0f} Hz")

    # 2. Cutoff sweep
    print("\n[2] Running cutoff distance sweep (100 test points) …")
    t0 = time.time()
    sweep_df = run_cutoff_sweep(frames, n_cutoffs=100)
    print(f"    Sweep complete in {time.time()-t0:.1f}s")
    sweep_df.to_csv(OUTPUT_DIR / 'cutoff_sweep_results.csv', index=False)

    print("\n[2b] Identifying regimes …")
    regimes, sweep_agg = identify_regimes(sweep_df)
    print(regimes.to_string(index=False))
    regimes.to_csv(OUTPUT_DIR / 'regime_summary.csv', index=False)

    # 3. Temporal analysis
    print("\n[3] Running temporal analysis (2-min windows) …")
    t0 = time.time()
    temporal_df = run_temporal_analysis(frames, window_size_min=2.0)
    print(f"    Done in {time.time()-t0:.1f}s  ({len(temporal_df)} windows)")
    temporal_df.to_csv(OUTPUT_DIR / 'temporal_windows.csv', index=False)

    print("\n[3b] Half-time Wilcoxon tests …")
    ht_results = run_halftime_tests(temporal_df)
    for scale, res in ht_results.items():
        print(f"    {scale}: 1st={res.get('first_half_mean','?'):.3f}  "
              f"2nd={res.get('second_half_mean','?'):.3f}  "
              f"Δ={res.get('pct_change','?'):+.1f}%  p={res.get('p','?')}")
    with open(OUTPUT_DIR / 'temporal_halftime_test.json', 'w') as f:
        json.dump(ht_results, f, indent=2)

    # 4. Sensitivity analysis
    print("\n[4a] Tactical cutoff sensitivity (6–17 m, 150 frames) …")
    sens_cut = run_sensitivity_cutoff(frames)
    sens_cut.to_csv(OUTPUT_DIR / 'sensitivity_cutoff.csv', index=False)

    print("\n[4b] Filtration percentile ablation (P50–P95, δ=12.0 m, 150 frames) …")
    sens_pct = run_sensitivity_percentile(frames)
    sens_pct.to_csv(OUTPUT_DIR / 'sensitivity_percentile.csv', index=False)

    # 5. Figures
    print("\n[5] Generating figures …")
    make_figures(sweep_agg, temporal_df, regimes, match_name)

    # 6. Compile headline summary
    print("\n[6] Compiling headline summary …")
    total_ind = int(temporal_df['h1_ind_total'].sum())
    total_tac = int(temporal_df['h1_tac_total'].sum())
    n_windows = len(temporal_df)
    presence_ind = float((temporal_df['h1_ind_total'] > 0).mean())
    presence_tac = float((temporal_df['h1_tac_total'] > 0).mean())

    summary = {
        'match_id':   MATCH_ID,
        'match_name': match_name,
        'source':     'SkillCorner broadcast tracking (open data)',
        'fps':        FPS,
        'total_frames': len(frames),
        'n_temporal_windows': n_windows,
        'regimes': regimes.to_dict(orient='records'),
        'h1_individual': {
            'total_loops': total_ind,
            'windows_with_loops': int((temporal_df['h1_ind_total'] > 0).sum()),
            'presence_rate': round(presence_ind, 3),
            'mean_per_window': round(temporal_df['h1_individual'].mean(), 3),
            'mean_persistence': round(temporal_df['mean_pers_ind'][temporal_df['mean_pers_ind']>0].mean(), 3)
                                 if (temporal_df['mean_pers_ind'] > 0).any() else 0.0,
        },
        'h1_tactical': {
            'total_loops': total_tac,
            'windows_with_loops': int((temporal_df['h1_tac_total'] > 0).sum()),
            'presence_rate': round(presence_tac, 3),
            'mean_per_window': round(temporal_df['h1_tactical'].mean(), 3),
            'mean_persistence': round(temporal_df['mean_pers_tac'][temporal_df['mean_pers_tac']>0].mean(), 3)
                                 if (temporal_df['mean_pers_tac'] > 0).any() else 0.0,
        },
        'temporal_halftime': ht_results,
        'sensitivity_cutoff': sens_cut.to_dict(orient='records'),
        'sensitivity_percentile': sens_pct.to_dict(orient='records'),
    }

    with open(OUTPUT_DIR / 'analysis_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Print the headline comparison table
    print("\n" + "=" * 60)
    print(" RESULTS SUMMARY — for paper Table comparison")
    print("=" * 60)
    print(f"\nMatch: {match_name}  (SkillCorner ID {MATCH_ID})")
    print(f"Frames (22-player): {len(frames):,}  at {FPS:.0f} Hz")
    print(f"Temporal windows:   {n_windows} (non-overlapping, 2 min each)\n")
    print("Validated regimes:")
    print(regimes[['scale','optimal_cutoff','validation_rate','stability']].to_string(index=False))
    print(f"\nH₁ loops — individual scale: {total_ind:,} total  ({presence_ind:.1%} windows with loops)")
    print(f"H₁ loops — tactical scale:   {total_tac:,} total  ({presence_tac:.1%} windows with loops)")
    print(f"\nHalf-time comparison (Wilcoxon p-values):")
    for scale, res in ht_results.items():
        p = res.get('p')
        pstr = f"{p:.3f}" if p is not None else "N/A"
        pct = res.get('pct_change')
        pctstr = f"{pct:+.1f}%" if pct is not None else "N/A"
        print(f"  {scale:12s}: {pctstr}  p={pstr}")

    print(f"\nAll results saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == '__main__':
    main()
