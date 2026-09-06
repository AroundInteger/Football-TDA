"""Shared layout config for Figure~1 pipeline schematic (panels a--b)."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import yaml

PIPELINE_DIR = Path(__file__).resolve().parents[1]
LAYOUT_PATH = PIPELINE_DIR / "config" / "fig1_layout.yaml"

CLUSTER_NAMES = ["green", "blue", "orange", "purple"]


@dataclass
class Fig1Layout:
    """Panel-normalised coordinates in $[0,1]^2$ (axes of each schematic box)."""

    left_slots: list[list[float]] = field(default_factory=lambda: [
        [0.08, 0.70],
        [0.38, 0.54],
        [0.08, 0.32],
        [0.38, 0.12],
    ])
    right_slots: list[list[float]] = field(default_factory=lambda: [
        [0.86, 0.52],
        [0.86, 0.40],
        [0.86, 0.28],
        [0.86, 0.16],
    ])
    label_pt: list[float] = field(default_factory=lambda: [0.20, 0.972])
    label_pt_tilde: list[float] = field(default_factory=lambda: [0.86, 0.972])
    label_pt_tilde_b: list[float] = field(default_factory=lambda: [0.20, 0.972])
    label_delta_disk: list[float] = field(default_factory=lambda: [0.015, 0.70])
    delta_bracket: list[int] = field(default_factory=lambda: [2, 3])
    delta_bracket_label_offset: list[float] = field(default_factory=lambda: [0.09, -0.055])
    delta_r: float = 0.088
    local_scale: float = 0.030
    eps_scale: float = 0.50
    eps_label_index: int = 3
    eps_label_pos: list[float] | None = None

    def left_slots_array(self) -> np.ndarray:
        return np.asarray(self.left_slots, dtype=float)

    def right_slots_array(self) -> np.ndarray:
        return np.asarray(self.right_slots, dtype=float)

    @classmethod
    def default(cls) -> Fig1Layout:
        return cls()

    def save(self, path: Path | None = None) -> Path:
        path = path or LAYOUT_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(asdict(self), fh, default_flow_style=False, sort_keys=False)
        return path

    @classmethod
    def load(cls, path: Path | None = None) -> Fig1Layout:
        path = path or LAYOUT_PATH
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        return cls(**data)


def load_layout(path: Path | None = None) -> Fig1Layout:
    path = path or LAYOUT_PATH
    if path.is_file():
        return Fig1Layout.load(path)
    layout = Fig1Layout.default()
    layout.save(path)
    return layout
