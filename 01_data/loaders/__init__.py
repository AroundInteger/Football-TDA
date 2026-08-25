"""
Shared data loaders for Football-TDA.

Provides a unified interface for loading tracking data from
SecondSpectrum, SkillCorner, and StatsBomb into a common format.

Usage:
    from loaders.secondspectrum import load_match
    from loaders.skillcorner import load_match, load_events, load_phases
    from loaders.statsbomb import load_match_events
"""

from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np


@dataclass
class Frame:
    """A single frame of tracking data (source-agnostic)."""
    home_positions: np.ndarray    # (n_home, 2)
    away_positions: np.ndarray    # (n_away, 2)
    all_positions: np.ndarray     # (n_home + n_away, 2) concatenated
    timestamp: float              # seconds from match start
    period: int                   # 1 or 2
    frame_id: int                 # original frame index in source data
    ball_position: Optional[np.ndarray] = None  # (2,) or (3,)

    @property
    def n_players(self) -> int:
        return len(self.all_positions)

    @property
    def is_complete(self) -> bool:
        """True if 22 players are present (standard 11v11)."""
        return self.n_players == 22


@dataclass
class MatchInfo:
    """Metadata for a match."""
    match_id: str
    home_team: str
    away_team: str
    source: str                   # 'secondspectrum', 'skillcorner', 'statsbomb'
    fps: float                    # frames per second
    pitch_length: float = 105.0   # metres
    pitch_width: float = 68.0     # metres


@dataclass
class MatchData:
    """Complete match tracking data."""
    info: MatchInfo
    frames: List[Frame] = field(default_factory=list)

    @property
    def n_frames(self) -> int:
        return len(self.frames)

    @property
    def complete_frames(self) -> List[Frame]:
        """Frames with exactly 22 players."""
        return [f for f in self.frames if f.is_complete]

    def get_window(self, start_sec: float, end_sec: float) -> List[Frame]:
        """Get frames within a time window (seconds)."""
        return [f for f in self.frames
                if start_sec <= f.timestamp < end_sec]

    def get_period(self, period: int) -> List[Frame]:
        """Get frames for a specific match period."""
        return [f for f in self.frames if f.period == period]
