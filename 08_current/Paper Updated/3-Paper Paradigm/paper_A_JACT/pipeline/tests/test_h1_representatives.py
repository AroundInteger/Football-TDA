"""Vietoris--Rips H1 representatives are present at birth."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

CORE = Path(__file__).resolve().parents[2] / "02_tda_core"
sys.path.insert(0, str(CORE))

from tda_utils import rips_h1_representatives  # noqa: E402


def test_three_points_have_no_finite_h1():
    triangle = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    assert rips_h1_representatives(triangle) == []


def test_square_cycle_is_present_at_birth():
    square = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    reps = rips_h1_representatives(square)
    assert len(reps) == 1
    rep = reps[0]
    assert rep.is_simple_cycle
    assert rep.n_vertices == 4
    assert rep.nodes is not None and len(rep.nodes) == 4
    assert rep.present_at_birth()
    assert rep.longest_is_birth()
    assert abs(rep.birth - 1.0) < 1e-9
    assert abs(rep.death - np.sqrt(2)) < 1e-9
    # The representative is the four sides. The diagonal is the death edge
    # and is not part of the cycle.
    assert all(abs(d - 1.0) < 1e-9 for d in rep.edge_distances)


if __name__ == "__main__":
    test_three_points_have_no_finite_h1()
    test_square_cycle_is_present_at_birth()
    print("ok")
