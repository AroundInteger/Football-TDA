"""
Shared numerics for the Adversarial TDA toy model.

Built on the independent Python verification of `adversarial_tda.m`.
H0 is exact via the MST (Carlsson–Mémoli). Wasserstein-p is the exact
optimal-transport distance on birth-zero diagrams, including diagonal
matching; the original sort-and-match rule is retained as
`wasserstein1_naive` because it overestimates W1(A_WIDE, A_NARROW).

The Fréchet mean is the W2 barycentre (Turner et al., 2014). For equal-
cardinality H0 diagrams the coordinatewise mean of sorted deaths is exact
for W2, not for W1 — that is why the verification counterexample exists.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform

try:
    from ripser import ripser
except ImportError:  # H1 figures need ripser; H0 verification does not
    ripser = None


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------

def tri_cluster(cx, cy, r=2.0):
    """Three agents in an isosceles triangle about (cx, cy).

    Within-cluster distances are 2r and r*sqrt(4.0625) ~ 2.0156 r, so with
    r = 2 the local H0 deaths are 4.00 and 4.03.
    """
    return np.array([
        [cx,     cy - r * 1.1],
        [cx - r, cy + r * 0.65],
        [cx + r, cy + r * 0.65],
    ], dtype=float)


def make_team(centres, r=2.0):
    """Stack `tri_cluster` blocks for a list of (cx, cy) cluster centres."""
    return np.vstack([tri_cluster(cx, cy, r) for cx, cy in centres])


def ring_clusters(cx, cy, rho=22.0, k=4, r=2.0):
    """k triangular clusters equally spaced on a circle (H1 encirclement)."""
    theta = np.linspace(0.0, 2.0 * np.pi, k, endpoint=False)
    centres = [(cx + rho * np.cos(t), cy + rho * np.sin(t)) for t in theta]
    return make_team(centres, r)


def interpolate_cloud(p0, p1, e):
    """Linear blend of two point clouds, e in [0, 1]."""
    return (1.0 - e) * p0 + e * p1


def smoothstep(t, t0, t1):
    """C1-smoothstep weight: 0 for t < t0, 1 for t >= t1."""
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    u = (t - t0) / (t1 - t0)
    return u * u * (3.0 - 2.0 * u)


# ---------------------------------------------------------------------------
# Persistent homology
# ---------------------------------------------------------------------------

def compute_h0(pts):
    """H0 persistence via the MST (exact for Vietoris–Rips H0)."""
    D = squareform(pdist(pts))
    mst = minimum_spanning_tree(D)
    weights = mst.toarray()
    deaths = weights[weights > 0]
    return np.sort(deaths)


def n_components_at_delta(pts, delta):
    """Connected-component count of the VR graph at threshold delta."""
    D = squareform(pdist(pts))
    n = D.shape[0]
    visited = np.zeros(n, dtype=bool)
    comps = 0
    for i in range(n):
        if visited[i]:
            continue
        comps += 1
        stack = [i]
        visited[i] = True
        while stack:
            u = stack.pop()
            nbr = np.where((~visited) & (D[u] <= delta))[0]
            visited[nbr] = True
            stack.extend(nbr.tolist())
    return comps


def h1_diagram(pts, thresh=None):
    """Finite H1 bars as an (n, 2) array of (birth, death). Requires ripser."""
    if ripser is None:
        raise ImportError("ripser is required for H1 diagrams")
    D = squareform(pdist(pts))
    if thresh is None:
        thresh = float(D.max()) + 1.0
    dgm = ripser(pts, maxdim=1, thresh=thresh)["dgms"][1]
    if dgm.size == 0:
        return np.zeros((0, 2))
    finite = np.isfinite(dgm[:, 1])
    return dgm[finite]


def h1_persistence(pts, thresh=None, birth_max=None):
    """Total finite H1 persistence (sum of death − birth).

    If `birth_max` is set, only bars born at or below that scale are kept.
    That isolates encirclement loops (born ~27) from the global rectangular
    hole of a two-formation layout (born ~60).
    """
    dgm = h1_diagram(pts, thresh)
    if dgm.size == 0:
        return 0.0
    if birth_max is not None:
        dgm = dgm[dgm[:, 0] <= birth_max]
        if dgm.size == 0:
            return 0.0
    return float(np.sum(dgm[:, 1] - dgm[:, 0]))


def encirclement_h1(pts, birth_max=45.0):
    """H1 persistence of loops born below `birth_max` (predator ring)."""
    return h1_persistence(pts, birth_max=birth_max)


def encirclement_bars(dgm, birth_max=45.0):
    """Filter an H1 diagram to encirclement-scale bars."""
    if dgm.size == 0:
        return dgm
    return dgm[dgm[:, 0] <= birth_max]


def betti_at(pts, delta):
    """(beta_0, beta_1) of the VR complex at a single scale."""
    b0 = n_components_at_delta(pts, delta)
    dgm = h1_diagram(pts)
    b1 = int(np.sum((dgm[:, 0] <= delta) & (dgm[:, 1] > delta))) if dgm.size else 0
    return b0, b1


# ---------------------------------------------------------------------------
# Distances and Fréchet means
# ---------------------------------------------------------------------------

def wasserstein1_naive(a, b):
    """Sort-and-match W1, leftover points sent to the diagonal at cost d/2.

    This is the rule in the original briefing. It is *not* the true W1
    whenever a point is cheaper to match to the diagonal than to its
    sorted partner. Kept so the overestimate can be quoted.
    """
    s1, s2 = np.sort(np.asarray(a).ravel()), np.sort(np.asarray(b).ravel())
    n = min(len(s1), len(s2))
    d = np.sum(np.abs(s1[:n] - s2[:n]))
    if len(s1) > n:
        d += np.sum(s1[n:] / 2.0)
    elif len(s2) > n:
        d += np.sum(s2[n:] / 2.0)
    return float(d)


def wasserstein_p(a, b, p=1):
    """Exact p-Wasserstein distance between birth-zero H0 diagrams.

    Ground metric is L-infinity on the plane, so matching two deaths costs
    |d_i − d_j| and matching a death to the diagonal costs d_i / 2. Solved
    as a linear assignment problem on the augmented cost matrix, which also
    handles unequal cardinality.
    """
    s1 = np.sort(np.asarray(a, dtype=float).ravel())
    s2 = np.sort(np.asarray(b, dtype=float).ravel())
    n, m = s1.size, s2.size
    if n == 0 and m == 0:
        return 0.0
    C = np.full((n + m, n + m), 1e12)
    if n and m:
        C[:n, :m] = np.abs(s1[:, None] - s2[None, :]) ** p
    for i in range(n):
        C[i, m + i] = (s1[i] / 2.0) ** p
    for j in range(m):
        C[n + j, j] = (s2[j] / 2.0) ** p
    C[n:, m:] = 0.0
    rows, cols = linear_sum_assignment(C)
    return float(C[rows, cols].sum() ** (1.0 / p))


def wasserstein1(a, b):
    """Exact W1 (preferred name; see `wasserstein_p`)."""
    return wasserstein_p(a, b, p=1)


def frechet_mean(diags):
    """Exact W2 barycentre of equal-cardinality birth-zero H0 diagrams."""
    stacked = np.vstack([np.sort(np.asarray(d).ravel()) for d in diags])
    if len({row.size for row in stacked}) != 1:
        raise ValueError("Fréchet mean here requires equal cardinality")
    return stacked.mean(axis=0)


def frechet_variance(diags, mu=None, p=2):
    """Mean squared W_p distance to the barycentre."""
    if mu is None:
        mu = frechet_mean(diags)
    return float(np.mean([wasserstein_p(d, mu, p=p) ** 2 for d in diags]))


# ---------------------------------------------------------------------------
# CUSUM
# ---------------------------------------------------------------------------

def cusum_path(w, kappa, mon0=0):
    """One-sided CUSUM; `w[t]` is the observation at frame t."""
    C = np.zeros_like(w, dtype=float)
    c = 0.0
    for t in range(mon0, len(w)):
        c = max(0.0, c + w[t] - kappa)
        C[t] = c
    return C


def first_alarm(C, h, mon0=0):
    """First index at which the CUSUM meets or exceeds h, or None."""
    hit = np.where(C[mon0:] >= h)[0]
    if hit.size == 0:
        return None
    return int(hit[0] + mon0)


def run_cusum(w, kappa, h, mon0=0):
    """CUSUM path and first alarm (None if the threshold is never met)."""
    C = cusum_path(w, kappa, mon0=mon0)
    return first_alarm(C, h, mon0=mon0), C


def cluster_centres(pts, group_size=3):
    """Centroid of each consecutive block of `group_size` agents."""
    pts = np.asarray(pts, dtype=float)
    n = pts.shape[0]
    if n % group_size:
        raise ValueError("point count must be a multiple of group_size")
    return pts.reshape(-1, group_size, 2).mean(axis=1)


def displace_clusters(template, base_centres, new_centres, group_size=3):
    """Move whole clusters, preserving internal geometry."""
    pts = np.asarray(template, dtype=float).copy()
    for i, (old, new) in enumerate(zip(base_centres, new_centres)):
        sl = slice(i * group_size, (i + 1) * group_size)
        pts[sl] = template[sl] + (new - old)
    return pts


def clip_cloud(pts, xlim, ylim):
    """Clamp a point cloud to a rectangular domain."""
    out = np.asarray(pts, dtype=float).copy()
    out[:, 0] = np.clip(out[:, 0], xlim[0], xlim[1])
    out[:, 1] = np.clip(out[:, 1], ylim[0], ylim[1])
    return out


def death_gap_scales(deaths, gap_factor=1.8):
    """Split a sorted H0 death vector at large gaps; return groups and mid-gap scales.

    Display thresholds should sit in the returned midpoints, not at football's
    5 / 40 / 66, and not at Paper A's clustering cutoffs.
    """
    d = np.sort(np.asarray(deaths, dtype=float).ravel())
    if d.size < 2:
        return [d], []
    # A new organisational level starts when the next death is substantially
    # larger than the last (multiplicative), not merely larger than the median
    # of tiny within-level repeats. Default 1.8: 17 vs 7 splits, 20 vs 17 does not.
    cuts = np.where(d[1:] >= gap_factor * np.maximum(d[:-1], 1e-9))[0]
    groups = np.split(d, cuts + 1)
    mids = [0.5 * (groups[i].max() + groups[i + 1].min()) for i in range(len(groups) - 1)]
    return groups, mids


def coupled_series(
    A0,
    B0,
    T,
    noise,
    drift,
    phi,
    rho,
    seed,
    coupled=True,
    group_size_a=3,
    group_size_b=3,
    xlim=None,
    ylim=None,
):
    """Two dependence structures with identical one-frame marginals.

    Port of the MATLAB `coupled_series`. The statistic is per-frame
    W1(D_t, D_ref) against the undisturbed configuration — not consecutive-
    frame W1, which is autocorrelated even under independence.
    """
    rng = np.random.default_rng(seed)
    Ac0 = cluster_centres(A0, group_size_a)
    Bc0 = cluster_centres(B0, group_size_b)
    refA = compute_h0(A0)
    refB = compute_h0(B0)
    nA, nB = Ac0.shape[0], Bc0.shape[0]
    UA = rng.normal(scale=drift, size=(nA, 2))
    V = rng.normal(scale=drift, size=(nB, 2))
    sA = np.zeros(T + 1)
    sB = np.zeros(T + 1)
    for t in range(T + 1):
        if coupled:
            UA_prev = UA
            UA = phi * UA + np.sqrt(1.0 - phi ** 2) * drift * rng.normal(size=(nA, 2))
            V = phi * V + np.sqrt(1.0 - phi ** 2) * drift * rng.normal(size=(nB, 2))
            n_share = min(nA, nB)
            UB = rng.normal(scale=drift, size=(nB, 2))
            UB[:n_share] = (
                rho * UA_prev[:n_share]
                + np.sqrt(1.0 - rho ** 2) * V[:n_share]
            )
        else:
            UA = drift * rng.normal(size=(nA, 2))
            UB = drift * rng.normal(size=(nB, 2))
        A = displace_clusters(A0, Ac0, Ac0 + UA, group_size_a)
        B = displace_clusters(B0, Bc0, Bc0 + UB, group_size_b)
        A = A + rng.normal(scale=noise, size=A.shape)
        B = B + rng.normal(scale=noise, size=B.shape)
        if xlim is not None and ylim is not None:
            A = clip_cloud(A, xlim, ylim)
            B = clip_cloud(B, xlim, ylim)
        sA[t] = wasserstein_p(compute_h0(A), refA, p=1)
        sB[t] = wasserstein_p(compute_h0(B), refB, p=1)
    return sA, sB


# ---------------------------------------------------------------------------
# Canonical geometries (corrected A_NARROW: uniform 16-unit spacing)
# ---------------------------------------------------------------------------

R = 2.0

A_WIDE = make_team([(18, 22), (18, 58), (82, 22), (82, 58)], R)
A_NARROW = make_team([(47, 16), (47, 32), (47, 48), (47, 64)], R)
A_LINE = make_team([(10, 40), (40, 40), (80, 40), (105, 40)], R)
B_PRESS = make_team([(5, 22), (35, 6), (35, 74), (96, 40)], R)
B_SPREAD = make_team([(26, 26), (26, 54), (66, 22), (66, 58)], R)

# Predator rings used by the GTPPF switching preview (Figure 10 / H1).
B_RING = ring_clusters(50, 40, rho=22, k=4, r=R)   # press in midfield
A_RING = ring_clusters(50, 40, rho=22, k=4, r=R)   # same trap, inverted occupant
B_WIDE = make_team([(20, 20), (20, 60), (84, 20), (84, 60)], R)
