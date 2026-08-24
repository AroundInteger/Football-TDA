"""
Independent verification of the Adversarial TDA Toy Model
=========================================================

Re-implements, in Python, the core algorithms from `adversarial_tda.m` and
checks every numeric claim against the corrected specification (August 2026).

Three independent checks, run in sequence:

  PART 1 — Reproduce the static (noise-free) reference values: H0 diagrams
           for A_WIDE / A_NARROW / A_LINE, exact W1 distances, and the
           delta=35 single-scale-failure component count.

  PART 2 — Test whether "coordinatewise mean of sorted death vectors" is
           the exact minimiser of E[W1(D_i, mu)^2]. It is not (W1). It *is*
           exact for the W2 Fréchet functional used by Turner et al. (2014)
           and by the MATLAB implementation.

  PART 3 — Repeat the W1 test in the low-noise sliding-window regime.

Requires: numpy, scipy. Optional: ripser (not used here).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import pdist

from atda_core import (
    A_LINE,
    A_NARROW,
    A_WIDE,
    B_PRESS,
    B_SPREAD,
    compute_h0,
    frechet_mean,
    n_components_at_delta,
    tri_cluster,
    wasserstein1_naive,
    wasserstein_p,
)

np.set_printoptions(precision=2, suppress=True)


def _fmt(v):
    return " ".join(f"{x:.2f}" for x in v)


def part1_reference_values():
    print("=" * 70)
    print("PART 1 — static reference values (noise = 0)")
    print("=" * 70)

    dA_wide = compute_h0(A_WIDE)
    dA_narrow = compute_h0(A_NARROW)
    dA_line = compute_h0(A_LINE)
    dB_press = compute_h0(B_PRESS)
    dB_spread = compute_h0(B_SPREAD)

    print("\nH0(A_WIDE)   :", _fmt(dA_wide))
    print("  expected    : 4.00 x4, 4.03 x4, 32.56, 32.56, 60.00")
    print("\nH0(A_NARROW) :", _fmt(dA_narrow))
    print("  expected    : 4.00 x4, 4.03 x4, 12.66, 12.66, 12.66")
    print("  (uniform 16-unit spacing at y = 16, 32, 48, 64)")
    print("\nH0(A_LINE)   :", _fmt(dA_line))
    print("  expected    : 4.00 x4, 4.03 x4, 21.00, 26.00, 36.00")
    print("\nH0(B_PRESS)  :", _fmt(dB_press))
    print("H0(B_SPREAD) :", _fmt(dB_spread))

    w1 = wasserstein_p(dA_wide, dA_narrow, p=1)
    w1_naive = wasserstein1_naive(dA_wide, dA_narrow)
    w1_line = wasserstein_p(dA_wide, dA_line, p=1)
    print(f"\nW1(A_WIDE, A_NARROW) exact  = {w1:.2f}   (expected 76.13)")
    print(f"W1(A_WIDE, A_NARROW) naive  = {w1_naive:.2f}   (sort-and-match overestimate)")
    print(f"W1(A_WIDE, A_LINE)   exact  = {w1_line:.2f}   (expected 42.12)")

    tc = tri_cluster(0, 0, 2.0)
    sides = np.sort(pdist(tc))
    print(f"\ntri_cluster side lengths (r=2): {sides}")
    print(f"max within-cluster distance    = {sides.max():.3f}  (briefing said ~4.4)")

    c_wide = n_components_at_delta(A_WIDE, 35)
    c_line = n_components_at_delta(A_LINE, 35)
    print(f"\ncomponents at delta=35: A_WIDE = {c_wide}, A_LINE = {c_line}  (both 2)")
    print(f"pitch diameter = {np.hypot(120, 80):.2f}")


def _w1_objective(mu, diags):
    mu = np.sort(np.clip(np.asarray(mu, dtype=float), 0.0, None))
    return np.mean([wasserstein_p(d, mu, p=1) ** 2 for d in diags])


def _w2_objective(mu, diags):
    return np.mean([wasserstein_p(d, mu, p=2) ** 2 for d in diags])


def part2_w1_vs_w2():
    print("\n" + "=" * 70)
    print("PART 2 — coordinatewise mean: exact for W2, not for W1")
    print("=" * 70)

    diags = [
        np.array([2.0, 10.0, 50.0]),
        np.array([3.0, 12.0, 20.0]),
        np.array([1.0, 40.0, 45.0]),
        np.array([5.0, 15.0, 60.0]),
    ]
    coord = frechet_mean(diags)
    print("\ncoordinatewise mean (W2 barycentre):", coord)
    print(f"W1 Fréchet functional at this mean  : {_w1_objective(coord, diags):.3f}")
    print(f"W2 Fréchet functional at this mean  : {_w2_objective(coord, diags):.3f}")

    rng = np.random.default_rng(0)
    bounds = [(0.0, None)] * 3
    best_w1 = None
    for _ in range(40):
        x0 = np.sort(np.clip(coord + rng.normal(scale=10, size=3), 0, None))
        res = minimize(_w1_objective, x0, args=(diags,), method="Nelder-Mead",
                       bounds=bounds,
                       options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 20000})
        if best_w1 is None or res.fun < best_w1.fun:
            best_w1 = res

    print("W1-optimised mu                     :", np.sort(best_w1.x))
    print(f"W1 functional at W1 optimum         : {best_w1.fun:.3f}")
    print(f"gap (coordwise vs W1 optimum)       : {_w1_objective(coord, diags) - best_w1.fun:.3f}")
    print("-> Turner et al. define Fréchet means of diagrams with W2; the")
    print("   MATLAB toy model now uses W2 throughout.")


def part3_realistic_regime():
    print("\n" + "=" * 70)
    print("PART 3 — W1 gap in the toy model's low-noise sliding window")
    print("=" * 70)

    base = np.array([4, 4, 4, 4, 4.03, 4.03, 4.03, 4.03, 32.56, 32.56, 60.0])
    rng = np.random.default_rng(1)
    diags = [np.sort(base + rng.normal(scale=1.2, size=11)) for _ in range(10)]
    coord = frechet_mean(diags)
    obj_mean = _w1_objective(coord, diags)

    bounds = [(0.0, None)] * 11
    best = None
    for _ in range(25):
        x0 = np.sort(np.clip(coord + rng.normal(scale=2, size=11), 0, None))
        res = minimize(_w1_objective, x0, args=(diags,), method="Nelder-Mead",
                       bounds=bounds,
                       options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 30000})
        if best is None or res.fun < best.fun:
            best = res

    print(f"\nW1 functional at coordinatewise mean : {obj_mean:.4f}")
    print(f"W1 functional at numeric W1 optimum   : {best.fun:.4f}")
    print(f"relative gap                          : {100 * (obj_mean - best.fun) / best.fun:.2f}%")
    print(f"global feature, coordinatewise        : {coord[-1]:.3f}")
    print(f"global feature, W1 optimum            : {np.sort(best.x)[-1]:.3f}")
    print("\nIn this regime the W1 gap is small; the MATLAB code nonetheless")
    print("reports the W2 barycentre, which is exact by construction.")


if __name__ == "__main__":
    part1_reference_values()
    part2_w1_vs_w2()
    part3_realistic_regime()
