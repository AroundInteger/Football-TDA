"""
StatsBomb open data loader.

Reads event JSON and Three-Sixty freeze-frame data from the
StatsBomb open-data repository.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional

from . import Frame, MatchInfo, MatchData


OPENDATA_ROOT = Path('01_data/open-data/data')


def list_matches(
    competition_id: Optional[int] = None,
    data_path: Optional[Path] = None,
) -> List[dict]:
    """
    List available StatsBomb matches.

    Args:
        competition_id: Filter by competition. None = all.
        data_path: Root of open-data/data/ directory.

    Returns:
        List of match dicts with id, home_team, away_team, etc.
    """
    root = Path(data_path) if data_path else OPENDATA_ROOT
    matches_dir = root / 'matches'
    if not matches_dir.exists():
        raise FileNotFoundError(f"Matches directory not found: {matches_dir}")

    all_matches = []
    for comp_dir in matches_dir.iterdir():
        if not comp_dir.is_dir():
            continue
        if competition_id is not None and comp_dir.name != str(competition_id):
            continue
        for season_file in comp_dir.glob('*.json'):
            with open(season_file, 'r') as f:
                matches = json.load(f)
            for m in matches:
                all_matches.append({
                    'match_id': m['match_id'],
                    'home_team': m.get('home_team', {}).get('home_team_name', ''),
                    'away_team': m.get('away_team', {}).get('away_team_name', ''),
                    'competition': m.get('competition', {}).get('competition_name', ''),
                    'season': m.get('season', {}).get('season_name', ''),
                    'match_date': m.get('match_date', ''),
                })
    return all_matches


def load_match_events(
    match_id: int,
    data_path: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Load StatsBomb events for a match.

    Returns DataFrame with columns including type, location, timestamp, etc.
    """
    root = Path(data_path) if data_path else OPENDATA_ROOT
    events_path = root / 'events' / f'{match_id}.json'
    if not events_path.exists():
        raise FileNotFoundError(f"Events not found: {events_path}")

    with open(events_path, 'r') as f:
        events = json.load(f)

    rows = []
    for evt in events:
        row = {
            'event_id': evt.get('id'),
            'type': evt.get('type', {}).get('name', ''),
            'timestamp': evt.get('timestamp', ''),
            'minute': evt.get('minute', 0),
            'second': evt.get('second', 0),
            'period': evt.get('period', 1),
            'team': evt.get('team', {}).get('name', ''),
            'player': evt.get('player', {}).get('name', ''),
        }
        loc = evt.get('location')
        if loc and len(loc) >= 2:
            row['x'] = loc[0]
            row['y'] = loc[1]
        else:
            row['x'] = None
            row['y'] = None
        rows.append(row)

    return pd.DataFrame(rows)


def load_match_tracking(
    match_id: int,
    data_path: Optional[Path] = None,
    events_df: Optional[pd.DataFrame] = None,
) -> MatchData:
    """
    Build tracking-like data from StatsBomb events with locations.

    StatsBomb doesn't provide continuous tracking, so we construct
    pseudo-frames from events that have location data, grouping by
    (minute, second) to approximate snapshots.

    Args:
        match_id: StatsBomb match ID.
        data_path: Root data path.
        events_df: Pre-loaded events DataFrame. Loaded if None.

    Returns:
        MatchData with pseudo-frames built from event locations.
    """
    root = Path(data_path) if data_path else OPENDATA_ROOT

    if events_df is None:
        events_df = load_match_events(match_id, root)

    info = MatchInfo(
        match_id=str(match_id),
        home_team=events_df[events_df['type'] == 'Starting XI']['team'].iloc[0]
            if len(events_df[events_df['type'] == 'Starting XI']) > 0 else 'Home',
        away_team=events_df[events_df['type'] == 'Starting XI']['team'].iloc[1]
            if len(events_df[events_df['type'] == 'Starting XI']) > 1 else 'Away',
        source='statsbomb',
        fps=1.0,  # approximate: one frame per unique timestamp
    )

    # Build pseudo-frames from Three-Sixty data if available
    three_sixty_path = root / 'three-sixty' / f'{match_id}.json'
    if three_sixty_path.exists():
        return _load_from_three_sixty(three_sixty_path, info)

    # Fallback: build frames from event locations grouped by timestamp
    located = events_df.dropna(subset=['x', 'y']).copy()
    located['time_sec'] = located['minute'] * 60 + located['second']

    frames = []
    for (period, time_sec), group in located.groupby(['period', 'time_sec']):
        home_events = group[group['team'] == info.home_team]
        away_events = group[group['team'] == info.away_team]

        home_pos = home_events[['x', 'y']].values if len(home_events) else np.empty((0, 2))
        away_pos = away_events[['x', 'y']].values if len(away_events) else np.empty((0, 2))

        if len(home_pos) == 0 and len(away_pos) == 0:
            continue

        all_pos = np.vstack([home_pos, away_pos]) if len(home_pos) and len(away_pos) \
            else home_pos if len(home_pos) else away_pos

        frames.append(Frame(
            home_positions=home_pos.astype(np.float64),
            away_positions=away_pos.astype(np.float64),
            all_positions=all_pos.astype(np.float64),
            timestamp=float(time_sec),
            period=int(period),
            frame_id=int(time_sec),
        ))

    return MatchData(info=info, frames=frames)


def _load_from_three_sixty(path: Path, info: MatchInfo) -> MatchData:
    """Load tracking from Three-Sixty freeze-frame data."""
    with open(path, 'r') as f:
        data = json.load(f)

    frames = []
    for entry in data:
        freeze = entry.get('freeze_frame', [])
        if not freeze:
            continue

        teammate_pos = []
        opponent_pos = []
        for player in freeze:
            loc = player.get('location', [])
            if len(loc) < 2:
                continue
            if player.get('teammate', False):
                teammate_pos.append(loc[:2])
            else:
                opponent_pos.append(loc[:2])

        home_arr = np.array(teammate_pos, dtype=np.float64) if teammate_pos else np.empty((0, 2))
        away_arr = np.array(opponent_pos, dtype=np.float64) if opponent_pos else np.empty((0, 2))

        if len(teammate_pos) == 0 and len(opponent_pos) == 0:
            continue

        all_arr = np.vstack([home_arr, away_arr]) if len(teammate_pos) and len(opponent_pos) \
            else home_arr if len(teammate_pos) else away_arr

        event_id = entry.get('event_uuid', '')
        timestamp = entry.get('timestamp', 0)
        period = entry.get('period', 1)

        frames.append(Frame(
            home_positions=home_arr,
            away_positions=away_arr,
            all_positions=all_arr,
            timestamp=float(timestamp) if isinstance(timestamp, (int, float)) else 0.0,
            period=int(period) if isinstance(period, int) else 1,
            frame_id=hash(event_id) % (10**8),
        ))

    return MatchData(info=info, frames=frames)
