"""
Ecology-led and robotics generators for the methods note.

These clouds are *not* A_WIDE / A_NARROW painted onto another background.
Each domain has its own N, diameter, cluster counts, and interaction kernel.
Gap scales are re-derived from the noise-free H0 death vector.

Ecology (lead)
    Territory Omega = [0, 240] x [0, 180]. Prey N=15 (five triples, r=3.5);
    predators N=12 (four triples, r=2.8). Programmed T*: dispersed hunting
    -> encircling a herded prey group. Predators track prey centroids.

Robotics (second)
    Corridor Omega = [0, 180] x [0, 50]. Pursuers N=8 (four pairs, r=2.4);
    evaders N=6 (three pairs, r=2.4). Programmed T*: open transit -> funnel
    intercept. Pair geometry is deliberately not the football triangle.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
# paper_C_methods → 3-Paper Paradigm → Paper Updated → 08_current
_TOY = _HERE.parents[2] / "grant" / "evidence" / "toy_models"
for _p in (_TOY, _HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from atda_core import (  # noqa: E402
    clip_cloud,
    compute_h0,
    death_gap_scales,
    interpolate_cloud,
    make_team,
    ring_clusters,
    smoothstep,
    wasserstein_p,
)

# ---------------------------------------------------------------------------
# Ecology: territorial predator–prey
# ---------------------------------------------------------------------------

ECO_XLIM = (0.0, 240.0)
ECO_YLIM = (0.0, 180.0)
ECO_DIAMETER = float(np.hypot(ECO_XLIM[1] - ECO_XLIM[0],
                              ECO_YLIM[1] - ECO_YLIM[0]))
R_PREY = 3.5
R_PRED = 2.8

# Five hunting groups spread across the territory (not a 4-triple pitch).
PREY_DISPERSED = make_team(
    [(42, 38), (42, 142), (120, 90), (198, 38), (198, 142)],
    r=R_PREY,
)
# Same five groups collapsed into a meadow (herd).
PREY_HERDED = make_team(
    [(152, 92), (176, 118), (200, 92), (176, 66), (176, 92)],
    r=R_PREY,
)
# Scale-conflation witness: a north–south column, same N, different hierarchy.
PREY_COLUMN = make_team(
    [(120, 30), (120, 62), (120, 94), (120, 126), (120, 158)],
    r=R_PREY,
)

# Four hunting groups tracking different prey sectors.
PRED_HUNT = make_team(
    [(58, 55), (110, 125), (170, 55), (210, 125)],
    r=R_PRED,
)
# Four groups on a ring around the herded meadow centroid (176, 92).
PRED_RING = ring_clusters(176.0, 92.0, rho=48.0, k=4, r=R_PRED)

ECO_T_STAR = 55
ECO_T_END = 64
ECO_NOISE = 1.8


def ecology_config(t, noise=0.0, rng=None):
    """Prey and predator clouds at frame t. T* = dispersed hunt -> encircle."""
    e = smoothstep(t, ECO_T_STAR, ECO_T_END)
    prey = interpolate_cloud(PREY_DISPERSED, PREY_HERDED, e)
    pred = interpolate_cloud(PRED_HUNT, PRED_RING, e)
    if noise > 0:
        prey = prey + rng.normal(scale=noise, size=prey.shape)
        pred = pred + rng.normal(scale=noise, size=pred.shape)
        prey = clip_cloud(prey, ECO_XLIM, ECO_YLIM)
        pred = clip_cloud(pred, ECO_XLIM, ECO_YLIM)
    return prey, pred


# ---------------------------------------------------------------------------
# Robotics: corridor pursuit–evasion (pair geometry, not triples)
# ---------------------------------------------------------------------------

ROB_XLIM = (0.0, 180.0)
ROB_YLIM = (0.0, 50.0)
ROB_DIAMETER = float(np.hypot(ROB_XLIM[1] - ROB_XLIM[0],
                              ROB_YLIM[1] - ROB_YLIM[0]))
R_PAIR = 2.4


def make_pairs(centres, r=R_PAIR, axis="y"):
    """Two-agent clusters. Internal distance 2r (not the football triangle)."""
    blocks = []
    for cx, cy in centres:
        if axis == "y":
            blocks.append(np.array([[cx, cy - r], [cx, cy + r]], dtype=float))
        else:
            blocks.append(np.array([[cx - r, cy], [cx + r, cy]], dtype=float))
    return np.vstack(blocks)


# Four pursuer pairs stacked across a gate, then pinched as they intercept.
# A rigid x-translation would leave H0 invariant (W1 = 0); the chase must
# change the hierarchy.
PURSUERS_GATE = make_pairs([(28, 8), (28, 19), (28, 31), (28, 42)], r=R_PAIR)
PURSUERS_CHASE = make_pairs([(118, 12), (118, 21), (118, 30), (118, 39)], r=R_PAIR)
# Three evader pairs in open transit vs bunched into a funnel.
EVADERS_OPEN = make_pairs([(35, 10), (95, 40), (160, 10)], r=R_PAIR, axis="x")
EVADERS_FUNNEL = make_pairs([(95, 21), (95, 25), (95, 29)], r=R_PAIR, axis="x")
# Scale-conflation: a single file along the corridor centreline.
EVADERS_FILE = make_pairs([(50, 25), (95, 25), (140, 25)], r=R_PAIR, axis="x")

ROB_T_STAR = 40
ROB_T_END = 44
ROB_NOISE = 1.2


def robotics_config(t, noise=0.0, rng=None):
    """Pursuers and evaders at frame t. T*: open transit -> funnel intercept."""
    e = smoothstep(t, ROB_T_STAR, ROB_T_END)
    pursuers = interpolate_cloud(PURSUERS_GATE, PURSUERS_CHASE, e)
    evaders = interpolate_cloud(EVADERS_OPEN, EVADERS_FUNNEL, e)
    if noise > 0:
        pursuers = pursuers + rng.normal(scale=noise, size=pursuers.shape)
        evaders = evaders + rng.normal(scale=noise, size=evaders.shape)
        pursuers = clip_cloud(pursuers, ROB_XLIM, ROB_YLIM)
        evaders = clip_cloud(evaders, ROB_XLIM, ROB_YLIM)
    return pursuers, evaders


# ---------------------------------------------------------------------------
# Reference report
# ---------------------------------------------------------------------------

def _fmt(v):
    return " ".join(f"{x:.2f}" for x in np.asarray(v).ravel())


def _print_cloud(name, pts, xlim, ylim):
    d = compute_h0(pts)
    groups, mids = death_gap_scales(d)
    diam = float(np.hypot(xlim[1] - xlim[0], ylim[1] - ylim[0]))
    print(f"\n{name}")
    print(f"  N = {len(pts)},  domain diameter = {diam:.2f}")
    print(f"  H0 deaths : {_fmt(d)}")
    print(f"  gap mids  : " + (", ".join(f"{m:.2f}" for m in mids) if mids else "(none)"))
    for i, g in enumerate(groups, start=1):
        print(f"    cluster {i}: n={len(g)}  [{g.min():.2f}, {g.max():.2f}]")
    return d, mids


def reference_report():
    """Noise-free H0 deaths and re-derived gap scales. No football numbers."""
    print("=" * 70)
    print("ECOLOGY generator (territory 240 x 180)")
    print("=" * 70)
    d_disp, m_disp = _print_cloud("PREY_DISPERSED", PREY_DISPERSED, ECO_XLIM, ECO_YLIM)
    d_herd, m_herd = _print_cloud("PREY_HERDED", PREY_HERDED, ECO_XLIM, ECO_YLIM)
    d_col, m_col = _print_cloud("PREY_COLUMN", PREY_COLUMN, ECO_XLIM, ECO_YLIM)
    d_hunt, m_hunt = _print_cloud("PRED_HUNT", PRED_HUNT, ECO_XLIM, ECO_YLIM)
    d_ring, m_ring = _print_cloud("PRED_RING", PRED_RING, ECO_XLIM, ECO_YLIM)

    w_herd = wasserstein_p(d_disp, d_herd, p=1)
    w_col = wasserstein_p(d_disp, d_col, p=1)
    print(f"\nW1(PREY_DISPERSED, PREY_HERDED) = {w_herd:.2f}")
    print(f"W1(PREY_DISPERSED, PREY_COLUMN) = {w_col:.2f}")
    print(f"W1(PRED_HUNT, PRED_RING)        = {wasserstein_p(d_hunt, d_ring, p=1):.2f}")

    print("\n" + "=" * 70)
    print("ROBOTICS generator (corridor 180 x 50)")
    print("=" * 70)
    d_gate, _ = _print_cloud("PURSUERS_GATE", PURSUERS_GATE, ROB_XLIM, ROB_YLIM)
    d_chase, _ = _print_cloud("PURSUERS_CHASE", PURSUERS_CHASE, ROB_XLIM, ROB_YLIM)
    d_open, _ = _print_cloud("EVADERS_OPEN", EVADERS_OPEN, ROB_XLIM, ROB_YLIM)
    d_fun, _ = _print_cloud("EVADERS_FUNNEL", EVADERS_FUNNEL, ROB_XLIM, ROB_YLIM)
    d_file, _ = _print_cloud("EVADERS_FILE", EVADERS_FILE, ROB_XLIM, ROB_YLIM)
    print(f"\nW1(PURSUERS_GATE, PURSUERS_CHASE) = {wasserstein_p(d_gate, d_chase, p=1):.2f}")
    print(f"W1(EVADERS_OPEN, EVADERS_FUNNEL)  = {wasserstein_p(d_open, d_fun, p=1):.2f}")
    print(f"W1(EVADERS_OPEN, EVADERS_FILE)    = {wasserstein_p(d_open, d_file, p=1):.2f}")

    return {
        "prey_dispersed": d_disp,
        "prey_herded": d_herd,
        "prey_column": d_col,
        "pred_hunt": d_hunt,
        "pred_ring": d_ring,
        "w1_prey_jump": w_herd,
        "mids_dispersed": m_disp,
        "mids_herded": m_herd,
        "mids_column": m_col,
        "mids_hunt": m_hunt,
        "mids_ring": m_ring,
    }


if __name__ == "__main__":
    reference_report()
