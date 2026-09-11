"""Cardinality-inversion cutoff protocol (Paper A).

Implements pipeline/CUTOFF_PROTOCOL.md line for line. Clustering-quality
metrics are not used here.
"""
from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd

N_AGENTS = 22
DELTA_MIN = 0.25
DELTA_MAX = 40.0
DELTA_STEP = 0.25

INDIVIDUAL_TARGET_H0 = N_AGENTS - 3  # 19
TACTICAL_TARGET_H0 = 5.0
TACTICAL_MIN_P_K_GE_4 = 0.5
TEAM_TARGET_H0 = 2.0

ACCEPTANCE_BANDS = {
    "individual": (15.0, 22.0),
    "tactical": (4.0, 10.0),
    "team": (1.0, 2.5),
}

SELECTION_RULES = {
    "individual": f"largest delta with mean H0 >= {INDIVIDUAL_TARGET_H0}",
    "tactical": (
        f"argmin |mean H0 - {TACTICAL_TARGET_H0:g}| among "
        f"P(k >= 4) >= {TACTICAL_MIN_P_K_GE_4:g}"
    ),
    "team": f"smallest delta with mean H0 <= {TEAM_TARGET_H0:g}",
}

REQUIRED_MATCH_IDS = (
    1886347,
    1899585,
    1925299,
    1953632,
    1996435,
    2006229,
    2011166,
    2013725,
    2015213,
    2017461,
)

PRIMARY_MATCH_ID = 1996435


def delta_grid() -> np.ndarray:
    """Return the locked cutoff grid: 0.25 m to 40.0 m inclusive, step 0.25 m."""
    n = int(round((DELTA_MAX - DELTA_MIN) / DELTA_STEP)) + 1
    grid = np.round(DELTA_MIN + DELTA_STEP * np.arange(n), 4)
    if grid[-1] != DELTA_MAX:
        raise RuntimeError(f"delta grid endpoint {grid[-1]} != {DELTA_MAX}")
    return grid


def _as_aligned_arrays(
    h0_by_delta: Mapping[float, float] | pd.DataFrame,
    p_k_ge_4: Mapping[float, float] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Normalise either a DataFrame or a {delta: mean_h0} map."""
    if isinstance(h0_by_delta, pd.DataFrame):
        df = h0_by_delta.copy()
        if "delta" in df.columns:
            deltas = df["delta"].to_numpy(dtype=float)
        elif "cutoff" in df.columns:
            deltas = df["cutoff"].to_numpy(dtype=float)
        else:
            raise ValueError("DataFrame must have a 'delta' or 'cutoff' column")
        if "mean_h0" in df.columns:
            mean_h0 = df["mean_h0"].to_numpy(dtype=float)
        elif "mean_n_clusters" in df.columns:
            mean_h0 = df["mean_n_clusters"].to_numpy(dtype=float)
        else:
            raise ValueError("DataFrame must have 'mean_h0' or 'mean_n_clusters'")
        if p_k_ge_4 is None:
            if "p_k_ge_4" not in df.columns:
                raise ValueError("DataFrame must have 'p_k_ge_4' for tactical inversion")
            p_k = df["p_k_ge_4"].to_numpy(dtype=float)
        elif isinstance(p_k_ge_4, pd.DataFrame):
            p_k = p_k_ge_4["p_k_ge_4"].to_numpy(dtype=float)
        else:
            p_k = np.array([p_k_ge_4[float(d)] for d in deltas], dtype=float)
    else:
        deltas = np.array(sorted(h0_by_delta.keys()), dtype=float)
        mean_h0 = np.array([h0_by_delta[float(d)] for d in deltas], dtype=float)
        if p_k_ge_4 is None:
            raise ValueError("p_k_ge_4 is required when h0_by_delta is a mapping")
        if isinstance(p_k_ge_4, pd.DataFrame):
            raise ValueError("p_k_ge_4 mapping expected when h0_by_delta is a mapping")
        p_k = np.array([p_k_ge_4[float(d)] for d in deltas], dtype=float)

    order = np.argsort(deltas)
    return deltas[order], mean_h0[order], p_k[order]


def invert_cutoffs(
    h0_by_delta: Mapping[float, float] | pd.DataFrame,
    p_k_ge_4: Mapping[float, float] | None = None,
) -> dict[str, float]:
    """Return adopted cutoffs from a pooled mean-H0 curve.

    Parameters
    ----------
    h0_by_delta
        Mapping delta -> mean H0, or a DataFrame with columns
        ``delta`` (or ``cutoff``), ``mean_h0`` (or ``mean_n_clusters``),
        and ``p_k_ge_4`` unless ``p_k_ge_4`` is passed separately.
    p_k_ge_4
        Mapping delta -> P(k >= 4). Required if ``h0_by_delta`` is a mapping.
    """
    deltas, mean_h0, p_k = _as_aligned_arrays(h0_by_delta, p_k_ge_4)
    return {
        "individual": invert_individual(deltas, mean_h0),
        "tactical": invert_tactical(deltas, mean_h0, p_k),
        "team": invert_team(deltas, mean_h0),
    }


def invert_individual(deltas: np.ndarray, mean_h0: np.ndarray) -> float:
    mask = mean_h0 >= INDIVIDUAL_TARGET_H0
    if not np.any(mask):
        raise ValueError(f"No delta has mean H0 >= {INDIVIDUAL_TARGET_H0}")
    return float(deltas[mask].max())


def invert_tactical(
    deltas: np.ndarray, mean_h0: np.ndarray, p_k_ge_4: np.ndarray
) -> float:
    mask = p_k_ge_4 >= TACTICAL_MIN_P_K_GE_4
    if not np.any(mask):
        raise ValueError(
            f"No delta has P(k >= 4) >= {TACTICAL_MIN_P_K_GE_4}"
        )
    gap = np.abs(mean_h0 - TACTICAL_TARGET_H0)
    gap = np.where(mask, gap, np.inf)
    min_gap = float(np.min(gap))
    tied = np.where(np.isfinite(gap) & np.isclose(gap, min_gap))[0]
    return float(deltas[tied].min())


def invert_team(deltas: np.ndarray, mean_h0: np.ndarray) -> float:
    mask = mean_h0 <= TEAM_TARGET_H0
    if not np.any(mask):
        raise ValueError(f"No delta has mean H0 <= {TEAM_TARGET_H0}")
    return float(deltas[mask].min())


def mean_h0_at(deltas: np.ndarray, mean_h0: np.ndarray, cutoff: float) -> float:
    """Mean H0 at the grid point nearest to ``cutoff``."""
    idx = int(np.argmin(np.abs(deltas - cutoff)))
    return float(mean_h0[idx])


def acceptance_ok(mean_h0: float, level: str) -> bool:
    lo, hi = ACCEPTANCE_BANDS[level]
    return lo <= mean_h0 <= hi


def silhouette_local_maxima(
    deltas: np.ndarray,
    silhouette: np.ndarray,
    *,
    min_prominence: float = 0.0,
) -> list[float]:
    """Deltas at strict local maxima of a silhouette curve.

    Endpoints count if they exceed their single neighbour. NaN values
    (undefined silhouette) are ignored.
    """
    d = np.asarray(deltas, dtype=float)
    s = np.asarray(silhouette, dtype=float)
    peaks: list[float] = []
    for i in range(len(s)):
        if not np.isfinite(s[i]):
            continue
        left_ok = i > 0 and np.isfinite(s[i - 1])
        right_ok = i + 1 < len(s) and np.isfinite(s[i + 1])
        if not (left_ok and right_ok):
            continue
        left = s[i - 1]
        right = s[i + 1]
        if s[i] > left and s[i] > right and (s[i] - max(left, right)) >= min_prominence:
            peaks.append(float(d[i]))
    return peaks
