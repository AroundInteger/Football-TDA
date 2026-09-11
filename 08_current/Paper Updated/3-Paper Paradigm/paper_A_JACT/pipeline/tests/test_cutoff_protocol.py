"""Synthetic tests for the locked cardinality-inversion tree."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(LIB))

from cutoff_protocol import (  # noqa: E402
    ACCEPTANCE_BANDS,
    INDIVIDUAL_TARGET_H0,
    TACTICAL_TARGET_H0,
    TEAM_TARGET_H0,
    acceptance_ok,
    delta_grid,
    invert_cutoffs,
    invert_individual,
    invert_tactical,
    invert_team,
    silhouette_local_maxima,
)


def _piecewise_curve():
    """Monotone H0 curve with known inversion points.

    Individual last hold of H0 >= 19 is 3.00 m.
    Tactical |H0 - 5| is uniquely minimised at 12.00 m.
    Team first H0 <= 2 is 22.00 m.
    """
    deltas = delta_grid()
    mean_h0 = np.empty(len(deltas))
    p_k = np.empty(len(deltas))
    for i, d in enumerate(deltas):
        if d <= 2.75:
            mean_h0[i] = 22.0
        elif d <= 3.00:
            mean_h0[i] = 19.0
        elif d < 12.00:
            mean_h0[i] = 19.0 - (d - 3.00) * (14.0 / 9.00)
        elif d == 12.00:
            mean_h0[i] = 5.0
        elif d < 22.00:
            mean_h0[i] = 5.0 - (d - 12.00) * (3.0 / 10.00)
        elif d == 22.00:
            mean_h0[i] = 2.0
        else:
            mean_h0[i] = max(1.0, 2.0 - 0.05 * (d - 22.00))
        p_k[i] = 1.0 if mean_h0[i] >= 4.0 else 0.0
    return deltas, mean_h0, p_k


def test_delta_grid_locked():
    g = delta_grid()
    assert g[0] == 0.25
    assert g[-1] == 40.0
    assert len(g) == 160
    assert np.allclose(np.diff(g), 0.25)


def test_invert_known_crossings():
    deltas, mean_h0, p_k = _piecewise_curve()
    table = {float(d): float(h) for d, h in zip(deltas, mean_h0)}
    pk = {float(d): float(p) for d, p in zip(deltas, p_k)}
    out = invert_cutoffs(table, pk)
    assert out["individual"] == 3.00
    assert out["tactical"] == 12.00
    assert out["team"] == 22.00


def test_invert_from_dataframe():
    import pandas as pd

    deltas, mean_h0, p_k = _piecewise_curve()
    df = pd.DataFrame(
        {"delta": deltas, "mean_h0": mean_h0, "p_k_ge_4": p_k}
    )
    out = invert_cutoffs(df)
    assert out["individual"] == 3.00
    assert out["tactical"] == 12.00
    assert out["team"] == 22.00


def test_tactical_tie_takes_smaller_delta():
    deltas = np.array([10.00, 10.25, 10.50, 11.00])
    # |H0-5|: 0.2, 0.2, 0.4, 1.0  -> tie at 10.00 and 10.25
    mean_h0 = np.array([5.2, 4.8, 5.4, 6.0])
    p_k = np.ones(4)
    assert invert_tactical(deltas, mean_h0, p_k) == 10.00


def test_tactical_excludes_low_pk():
    deltas = np.array([8.00, 12.00, 20.00])
    mean_h0 = np.array([5.0, 5.1, 2.0])
    p_k = np.array([0.4, 0.9, 0.0])  # 8.00 is closer to 5 but fails P(k>=4)
    assert invert_tactical(deltas, mean_h0, p_k) == 12.00


def test_missing_individual_raises():
    try:
        invert_individual(np.array([1.0, 2.0]), np.array([10.0, 8.0]))
    except ValueError as exc:
        assert "mean H0" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_missing_team_raises():
    try:
        invert_team(np.array([1.0, 2.0]), np.array([22.0, 20.0]))
    except ValueError as exc:
        assert "mean H0" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_acceptance_bands():
    assert acceptance_ok(19.0, "individual")
    assert not acceptance_ok(14.0, "individual")
    assert acceptance_ok(5.0, "tactical")
    assert not acceptance_ok(3.0, "tactical")
    assert acceptance_ok(1.4, "team")
    assert not acceptance_ok(3.0, "team")
    assert ACCEPTANCE_BANDS["individual"][0] == 15.0


def test_targets_are_roster_statements():
    assert INDIVIDUAL_TARGET_H0 == 19
    assert TACTICAL_TARGET_H0 == 5.0
    assert TEAM_TARGET_H0 == 2.0


def test_silhouette_local_maxima():
    deltas = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
    sil = np.array([0.1, 0.4, 0.2, 0.15, 0.5, 0.3, 0.1])
    peaks = silhouette_local_maxima(deltas, sil)
    assert peaks == [2.0, 5.0]


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"{len(tests)} passed")
