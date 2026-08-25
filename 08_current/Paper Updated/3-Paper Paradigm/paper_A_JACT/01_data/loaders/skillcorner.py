"""
SkillCorner tracking data loader.

Reads JSONL tracking + match JSON + dynamic events CSV + phases of play CSV
from the SkillCorner open data format (10 Hz broadcast tracking).
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional, Tuple

from . import Frame, MatchInfo, MatchData


OPENDATA_ROOT = Path('01_data/opendata/data')
FPS = 10.0


def list_matches(opendata_path: Optional[Path] = None) -> List[dict]:
    """
    List all available SkillCorner matches.

    Returns:
        List of dicts with id, home_team, away_team, date_time.
    """
    root = Path(opendata_path) if opendata_path else OPENDATA_ROOT
    matches_json = root / 'matches.json'
    if not matches_json.exists():
        raise FileNotFoundError(f"matches.json not found: {matches_json}")

    with open(matches_json, 'r') as f:
        return json.load(f)


def load_match(
    match_id: int,
    opendata_path: Optional[Path] = None,
    max_frames: Optional[int] = None,
    sample_every: int = 1,
    require_complete: bool = False,
) -> MatchData:
    """
    Load a SkillCorner match.

    Args:
        match_id: SkillCorner match ID.
        opendata_path: Root of opendata/data/ directory.
        max_frames: Stop after this many frames.
        sample_every: Load every Nth frame.
        require_complete: Only keep frames with 22 players.

    Returns:
        MatchData with all loaded frames.
    """
    root = Path(opendata_path) if opendata_path else OPENDATA_ROOT
    match_dir = root / 'matches' / str(match_id)

    match_json_path = match_dir / f'{match_id}_match.json'
    tracking_path = match_dir / f'{match_id}_tracking_extrapolated.jsonl'

    if not match_json_path.exists():
        raise FileNotFoundError(f"Match JSON not found: {match_json_path}")
    if not tracking_path.exists():
        raise FileNotFoundError(
            f"Tracking data not found: {tracking_path}. "
            f"Run 'git lfs pull' in the opendata directory."
        )

    with open(match_json_path, 'r') as f:
        match_meta = json.load(f)

    home_team_id, away_team_id, home_name, away_name = _extract_team_ids(match_meta)
    player_team_map = _build_player_team_map(match_meta, home_team_id, away_team_id)

    pitch_length = match_meta.get('pitch_length', 105.0)
    pitch_width = match_meta.get('pitch_width', 68.0)

    info = MatchInfo(
        match_id=str(match_id),
        home_team=home_name,
        away_team=away_name,
        source='skillcorner',
        fps=FPS,
        pitch_length=pitch_length,
        pitch_width=pitch_width,
    )

    frames = []
    with open(tracking_path, 'r') as f:
        for i, line in enumerate(f):
            if i % sample_every != 0:
                continue
            if max_frames is not None and len(frames) >= max_frames:
                break

            data = json.loads(line)
            frame = _parse_frame(data, i, player_team_map)
            if frame is None:
                continue
            if require_complete and not frame.is_complete:
                continue
            frames.append(frame)

    return MatchData(info=info, frames=frames)


def load_events(
    match_id: int,
    opendata_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Load dynamic events CSV for a match."""
    root = Path(opendata_path) if opendata_path else OPENDATA_ROOT
    events_path = root / 'matches' / str(match_id) / f'{match_id}_dynamic_events.csv'
    if not events_path.exists():
        raise FileNotFoundError(f"Events not found: {events_path}")
    return pd.read_csv(events_path)


def load_phases(
    match_id: int,
    opendata_path: Optional[Path] = None,
) -> pd.DataFrame:
    """Load phases of play CSV for a match."""
    root = Path(opendata_path) if opendata_path else OPENDATA_ROOT
    phases_path = root / 'matches' / str(match_id) / f'{match_id}_phases_of_play.csv'
    if not phases_path.exists():
        raise FileNotFoundError(f"Phases not found: {phases_path}")
    return pd.read_csv(phases_path)


def _extract_team_ids(match_meta: dict) -> Tuple[int, int, str, str]:
    """Extract home/away team IDs and names from match JSON."""
    home_team = match_meta.get('home_team', {})
    away_team = match_meta.get('away_team', {})
    home_id = home_team.get('id', home_team.get('team_id', -1))
    away_id = away_team.get('id', away_team.get('team_id', -2))
    home_name = home_team.get('short_name', home_team.get('name', 'Home'))
    away_name = away_team.get('short_name', away_team.get('name', 'Away'))
    return home_id, away_id, home_name, away_name


def _build_player_team_map(match_meta: dict, home_id: int, away_id: int) -> dict:
    """
    Build mapping from player_id -> 'home' | 'away'.

    SkillCorner match JSON has 'players' list with 'team_id' per player.
    """
    player_map = {}
    for player in match_meta.get('players', []):
        trackable = player.get('trackable_object')
        player_id = player.get('id')
        tid = player.get('team_id')
        if tid is not None:
            team = 'home' if tid == home_id else 'away' if tid == away_id else None
            if team:
                if trackable is not None:
                    player_map[trackable] = team
                if player_id is not None:
                    player_map[player_id] = team
    return player_map


def _parse_frame(data: dict, line_index: int, player_team_map: dict) -> Optional[Frame]:
    """Parse a single SkillCorner tracking JSONL line."""
    home_pos = []
    away_pos = []

    for player in data.get('player_data', []):
        x = player.get('x')
        y = player.get('y')
        pid = player.get('player_id')

        if x is None or y is None:
            continue

        team = player_team_map.get(pid)
        if team == 'home':
            home_pos.append([x, y])
        elif team == 'away':
            away_pos.append([x, y])
        # Players not in map are skipped (referees, unknown)

    if not home_pos and not away_pos:
        return None

    home_arr = np.array(home_pos, dtype=np.float64) if home_pos else np.empty((0, 2))
    away_arr = np.array(away_pos, dtype=np.float64) if away_pos else np.empty((0, 2))

    if len(home_pos) and len(away_pos):
        all_arr = np.vstack([home_arr, away_arr])
    elif len(home_pos):
        all_arr = home_arr
    else:
        all_arr = away_arr

    ball = None
    ball_data = data.get('ball_data')
    if ball_data and ball_data.get('x') is not None:
        ball = np.array([ball_data['x'], ball_data['y']], dtype=np.float64)

    timestamp_str = data.get('timestamp', '')
    timestamp = _parse_timestamp(timestamp_str, line_index)
    period = data.get('period', 1)

    return Frame(
        home_positions=home_arr,
        away_positions=away_arr,
        all_positions=all_arr,
        timestamp=timestamp,
        period=int(period),
        frame_id=data.get('frame', line_index),
        ball_position=ball,
    )


def _parse_timestamp(ts: str, fallback_index: int) -> float:
    """Parse SkillCorner timestamp string (MM:SS.s or seconds) to float seconds."""
    if not ts:
        return fallback_index / FPS

    if isinstance(ts, (int, float)):
        return float(ts)

    try:
        if ':' in str(ts):
            parts = str(ts).split(':')
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60.0 + seconds
        return float(ts)
    except (ValueError, IndexError):
        return fallback_index / FPS
