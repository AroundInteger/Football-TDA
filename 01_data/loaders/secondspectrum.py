"""
SecondSpectrum tracking data loader.

Reads JSONL files from the SecondSpectrum optical tracking system (25 Hz).
Each line is a JSON object with homePlayers/awayPlayers arrays containing
xyz coordinates.
"""

import json
import numpy as np
from pathlib import Path
from typing import Optional

from . import Frame, MatchInfo, MatchData


DEFAULT_PATH = Path('01_data/FieldTest/g2293068_SecondSpectrum_Data.jsonl')
FPS = 25.0


def load_match(
    jsonl_path: Optional[Path] = None,
    max_frames: Optional[int] = None,
    sample_every: int = 1,
    require_complete: bool = False,
) -> MatchData:
    """
    Load a SecondSpectrum match from JSONL.

    Args:
        jsonl_path: Path to .jsonl file. Uses default if None.
        max_frames: Stop after loading this many frames (None = all).
        sample_every: Load every Nth frame (1 = all frames).
        require_complete: If True, only keep frames with exactly 22 players.

    Returns:
        MatchData with all loaded frames.
    """
    jsonl_path = Path(jsonl_path) if jsonl_path else DEFAULT_PATH
    if not jsonl_path.exists():
        raise FileNotFoundError(f"SecondSpectrum data not found: {jsonl_path}")

    match_id = jsonl_path.stem.split('_')[0]
    info = MatchInfo(
        match_id=match_id,
        home_team='home',
        away_team='away',
        source='secondspectrum',
        fps=FPS,
    )

    metadata_path = jsonl_path.with_name(
        jsonl_path.stem.replace('Data', 'Metadata') + '.json'
    )
    if metadata_path.exists():
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
        info.home_team = meta.get('homeTeamName', 'home')
        info.away_team = meta.get('awayTeamName', 'away')

    frames = []
    with open(jsonl_path, 'r') as f:
        for i, line in enumerate(f):
            if i % sample_every != 0:
                continue
            if max_frames is not None and len(frames) >= max_frames:
                break

            data = json.loads(line)
            frame = _parse_frame(data, i)
            if frame is None:
                continue
            if require_complete and not frame.is_complete:
                continue
            frames.append(frame)

    return MatchData(info=info, frames=frames)


def _parse_frame(data: dict, line_index: int) -> Optional[Frame]:
    """Parse a single JSONL line into a Frame."""
    home_pos = []
    for player in data.get('homePlayers', []):
        xyz = player.get('xyz', [])
        if len(xyz) >= 2:
            home_pos.append([xyz[0], xyz[1]])

    away_pos = []
    for player in data.get('awayPlayers', []):
        xyz = player.get('xyz', [])
        if len(xyz) >= 2:
            away_pos.append([xyz[0], xyz[1]])

    if not home_pos and not away_pos:
        return None

    home_arr = np.array(home_pos, dtype=np.float64)
    away_arr = np.array(away_pos, dtype=np.float64)
    all_arr = np.vstack([home_arr, away_arr]) if len(home_pos) and len(away_pos) \
        else home_arr if len(home_pos) else away_arr

    ball = None
    if 'ball' in data and 'xyz' in data['ball']:
        bxyz = data['ball']['xyz']
        if len(bxyz) >= 2:
            ball = np.array(bxyz[:2], dtype=np.float64)

    timestamp = data.get('gameClock', line_index / FPS)
    period = data.get('period', 1)

    return Frame(
        home_positions=home_arr,
        away_positions=away_arr,
        all_positions=all_arr,
        timestamp=float(timestamp),
        period=int(period),
        frame_id=line_index,
        ball_position=ball,
    )
