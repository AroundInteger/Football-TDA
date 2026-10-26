"""
Shared TDA utilities for Football-TDA.

Single source of truth for the core persistent homology pipeline:
cutoff clustering, adaptive filtration, ripser computation,
persistence statistics, and closed-cycle identification.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from collections import defaultdict


# ---------------------------------------------------------------------------
#  Validated scale parameters
# ---------------------------------------------------------------------------

VALIDATED_CUTOFFS = {
    'individual': 2.75,
    'tactical': 11.75,
    'team': 23.0,
}

EXPECTED_H0_RANGES = {
    'individual': (15, 22),
    'tactical': (4, 10),
    'team': (1, 2.5),
}


# ---------------------------------------------------------------------------
#  Data classes for results
# ---------------------------------------------------------------------------

@dataclass
class PersistenceResult:
    """Result of a persistent homology computation."""
    h0_diagram: np.ndarray        # (n, 2) birth-death pairs for H0
    h1_diagram: np.ndarray        # (n, 2) birth-death pairs for H1
    h0_count: int
    h1_count: int
    point_cloud: np.ndarray       # the (possibly clustered) point cloud used
    filtration_used: float        # max filtration value
    cluster_count: int            # number of clusters (= len(point_cloud))

    @property
    def h0_stats(self) -> Dict[str, float]:
        return persistence_stats(self.h0_diagram)

    @property
    def h1_stats(self) -> Dict[str, float]:
        return persistence_stats(self.h1_diagram)


@dataclass
class Cycle:
    """A closed cycle representing an H1 feature."""
    nodes: List[int]
    score: float
    edge_distances: List[float]
    birth: float
    death: float

    @property
    def persistence(self) -> float:
        return self.death - self.birth

    @property
    def length(self) -> int:
        return len(self.nodes)


# ---------------------------------------------------------------------------
#  Core functions
# ---------------------------------------------------------------------------

def cutoff_clustering(
    positions: np.ndarray,
    cutoff: float,
    method: str = 'single',
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Hierarchical clustering at a given cutoff distance, returning centroids.

    Args:
        positions: (n, 2) array of player positions.
        cutoff: Maximum linkage distance for cluster formation.
        method: Linkage method ('single', 'complete', 'ward', 'average').

    Returns:
        (centroids, labels) where centroids is (k, 2) cluster centres
        and labels is (n,) cluster assignment per input point.
    """
    if positions is None or len(positions) <= 1:
        return positions.copy() if positions is not None else np.empty((0, 2)), \
               np.zeros(len(positions) if positions is not None else 0, dtype=int)

    distances = pdist(positions)
    if len(distances) == 0:
        return positions.copy(), np.zeros(len(positions), dtype=int)

    linkage_matrix = linkage(distances, method=method)
    labels = fcluster(linkage_matrix, cutoff, criterion='distance')

    unique_labels = np.unique(labels)
    centroids = np.array([
        positions[labels == lab].mean(axis=0)
        for lab in unique_labels
    ])

    return centroids, labels


def adaptive_filtration(
    centroids: np.ndarray,
    cutoff: float,
    percentile: int = 75,
    floor: float = 5.0,
    scale_factor: float = 2.0,
) -> float:
    """
    Maximum Vietoris-Rips filtration for a reduced centroid cloud.

    Paper A (Oct 2026): persistence to cloud diameter (C2 check). The
    percentile/floor arguments are retained for API compatibility but
    ignored when computing the extent.
    """
    del percentile, floor, scale_factor, cutoff
    if centroids is None or len(centroids) <= 1:
        return 0.0

    dists = pdist(centroids)
    if len(dists) == 0:
        return 0.0

    return float(np.max(dists)) + 1e-9


def compute_persistence(
    point_cloud: np.ndarray,
    max_filtration: float,
    maxdim: int = 1,
) -> PersistenceResult:
    """
    Compute persistent homology using ripser.

    Args:
        point_cloud: (n, 2) or (n, d) array of points.
        max_filtration: Maximum filtration threshold.
        maxdim: Maximum homology dimension (default 1 for H0 + H1).

    Returns:
        PersistenceResult with diagrams and counts.
    """
    from ripser import ripser

    if point_cloud is None or len(point_cloud) <= 1:
        empty = np.empty((0, 2))
        return PersistenceResult(
            h0_diagram=empty, h1_diagram=empty,
            h0_count=len(point_cloud) if point_cloud is not None else 0,
            h1_count=0,
            point_cloud=point_cloud if point_cloud is not None else np.empty((0, 2)),
            filtration_used=max_filtration,
            cluster_count=len(point_cloud) if point_cloud is not None else 0,
        )

    try:
        result = ripser(point_cloud, maxdim=maxdim, thresh=max_filtration)
        h0 = result['dgms'][0]
        h1 = result['dgms'][1] if maxdim >= 1 else np.empty((0, 2))

        return PersistenceResult(
            h0_diagram=h0,
            h1_diagram=h1,
            h0_count=len(h0),
            h1_count=len(h1),
            point_cloud=point_cloud,
            filtration_used=max_filtration,
            cluster_count=len(point_cloud),
        )
    except Exception:
        empty = np.empty((0, 2))
        return PersistenceResult(
            h0_diagram=empty, h1_diagram=empty,
            h0_count=len(point_cloud), h1_count=0,
            point_cloud=point_cloud,
            filtration_used=max_filtration,
            cluster_count=len(point_cloud),
        )


def compute_h1_at_scale(
    positions: np.ndarray,
    cutoff: float,
    linkage_method: str = 'single',
    percentile: int = 75,
) -> PersistenceResult:
    """
    End-to-end: cluster at cutoff, adapt filtration, compute persistence.

    This is the convenience function that combines all three steps.

    Args:
        positions: (n, 2) raw player positions.
        cutoff: Clustering cutoff distance in metres.
        linkage_method: Hierarchical clustering method.
        percentile: Percentile for adaptive filtration.

    Returns:
        PersistenceResult with full diagram information.
    """
    centroids, labels = cutoff_clustering(positions, cutoff, method=linkage_method)
    max_filt = adaptive_filtration(centroids, cutoff, percentile=percentile)
    result = compute_persistence(centroids, max_filt)
    return result


# ---------------------------------------------------------------------------
#  Persistence statistics
# ---------------------------------------------------------------------------

def persistence_stats(diagram: np.ndarray) -> Dict[str, float]:
    """
    Compute summary statistics from a persistence diagram.

    Args:
        diagram: (n, 2) array of (birth, death) pairs.

    Returns:
        Dict with mean, std, max, min persistence, and feature count.
    """
    if diagram is None or len(diagram) == 0:
        return {
            'count': 0, 'mean': 0.0, 'std': 0.0,
            'max': 0.0, 'min': 0.0, 'total': 0.0,
        }

    lifetimes = diagram[:, 1] - diagram[:, 0]
    finite_mask = np.isfinite(lifetimes)
    lifetimes = lifetimes[finite_mask]

    if len(lifetimes) == 0:
        return {
            'count': 0, 'mean': 0.0, 'std': 0.0,
            'max': 0.0, 'min': 0.0, 'total': 0.0,
        }

    return {
        'count': int(len(lifetimes)),
        'mean': float(np.mean(lifetimes)),
        'std': float(np.std(lifetimes)),
        'max': float(np.max(lifetimes)),
        'min': float(np.min(lifetimes)),
        'total': float(np.sum(lifetimes)),
    }


# ---------------------------------------------------------------------------
#  H1 representatives from the Vietoris--Rips boundary reduction
# ---------------------------------------------------------------------------

@dataclass
class H1Representative:
    """Homology representative of one finite H1 bar.

    ``edges`` is the support of the reduced boundary of the 2-simplex that
    destroys the class. Every edge is present at birth, and the longest
    edge is the edge that creates the class.
    """
    birth: float
    death: float
    edges: List[Tuple[int, int]]
    edge_distances: List[float]
    nodes: Optional[List[int]]
    is_simple_cycle: bool

    @property
    def persistence(self) -> float:
        return self.death - self.birth

    @property
    def n_vertices(self) -> int:
        verts = set()
        for i, j in self.edges:
            verts.add(i)
            verts.add(j)
        return len(verts)

    @property
    def longest_edge(self) -> float:
        if not self.edge_distances:
            return float("nan")
        return float(max(self.edge_distances))

    def present_at_birth(self, tol: float = 1e-6) -> bool:
        return bool(self.edge_distances) and self.longest_edge <= self.birth + tol

    def longest_is_birth(self, tol: float = 1e-6) -> bool:
        return bool(self.edge_distances) and abs(self.longest_edge - self.birth) <= tol


def _order_simple_cycle(edges: List[Tuple[int, int]]) -> Optional[List[int]]:
    """Return vertex order when ``edges`` is a single circuit."""
    adj: Dict[int, List[int]] = defaultdict(list)
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    if not adj or any(len(nbrs) != 2 for nbrs in adj.values()):
        return None
    start = min(adj)
    cycle = [start]
    prev = None
    cur = start
    while True:
        nbrs = adj[cur]
        if prev is None:
            nxt = nbrs[0]
        elif nbrs[0] == prev:
            nxt = nbrs[1]
        else:
            nxt = nbrs[0]
        if nxt == start:
            break
        cycle.append(nxt)
        prev, cur = cur, nxt
        if len(cycle) > len(adj):
            return None
    if len(cycle) != len(adj):
        return None
    return cycle


def rips_h1_representatives(
    points: np.ndarray,
    tol: float = 1e-8,
) -> List[H1Representative]:
    """Finite H1 bars and their reduction cycles on a Vietoris--Rips complex.

    The complex is filtered by Euclidean length, with no threshold short of
    the diameter: every edge and every triangle on ``points`` enters.
    A bar is the pair (creating edge, destroying triangle) from F2 column
    reduction. The representative is the reduced boundary of that triangle.
    Pairs with persistence at most ``tol`` are the filled triangles of a
    flag complex and are omitted.

    The birth--death values agree with Ripser up to Ripser's float32
    rounding. The cycle itself is not the cocycle array Ripser returns:
    that cocycle is a cohomology representative and can contain the edge
    that destroys the class.
    """
    pts = np.asarray(points, dtype=float)
    n = len(pts)
    if n < 4:
        return []

    dist = squareform(pdist(pts))
    simplices: List[Tuple[float, int, Tuple[int, ...]]] = []
    for i in range(n):
        for j in range(i + 1, n):
            simplices.append((float(dist[i, j]), 1, (i, j)))
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                filt = float(max(dist[i, j], dist[i, k], dist[j, k]))
                simplices.append((filt, 2, (i, j, k)))
    simplices.sort(key=lambda s: (s[0], s[1], s[2]))

    edge_index = {
        simp: idx for idx, (_filt, dim, simp) in enumerate(simplices) if dim == 1
    }
    columns: List[set] = []
    for _filt, dim, simp in simplices:
        if dim == 1:
            columns.append(set())
            continue
        i, j, k = simp
        columns.append({
            edge_index[(i, j)],
            edge_index[(i, k)],
            edge_index[(j, k)],
        })

    pivot_of: Dict[int, int] = {}
    for col_idx, (_filt, dim, _simp) in enumerate(simplices):
        if dim != 2:
            continue
        column = set(columns[col_idx])
        while column:
            pivot = max(column)
            if pivot not in pivot_of:
                pivot_of[pivot] = col_idx
                columns[col_idx] = column
                break
            column.symmetric_difference_update(columns[pivot_of[pivot]])
        else:
            columns[col_idx] = set()

    reps: List[H1Representative] = []
    for creator, destroyer in pivot_of.items():
        if simplices[creator][1] != 1:
            continue
        birth = simplices[creator][0]
        death = simplices[destroyer][0]
        if death <= birth + tol:
            continue
        edges = [simplices[idx][2] for idx in sorted(columns[destroyer])]
        edge_distances = [float(dist[i, j]) for i, j in edges]
        nodes = _order_simple_cycle(edges)
        if nodes is not None:
            edge_distances = [
                float(dist[nodes[t], nodes[(t + 1) % len(nodes)]])
                for t in range(len(nodes))
            ]
            edges = [
                tuple(sorted((nodes[t], nodes[(t + 1) % len(nodes)])))
                for t in range(len(nodes))
            ]
        reps.append(H1Representative(
            birth=birth,
            death=death,
            edges=edges,
            edge_distances=edge_distances,
            nodes=nodes,
            is_simple_cycle=nodes is not None,
        ))
    reps.sort(key=lambda r: (r.birth, r.death))
    return reps


# ---------------------------------------------------------------------------
#  Closed cycle identification
# ---------------------------------------------------------------------------

def find_closed_cycles(
    point_cloud: np.ndarray,
    birth: float,
    death: float,
    min_length: int = 3,
    max_length: int = 8,
) -> List[Cycle]:
    """
    Legacy midpoint proxy. Not used for Paper A representatives.

    Constructs the adjacency graph of edges with distances in [birth, death]
    and enumerates simple cycles via BFS. A three-vertex cycle in a
    Vietoris--Rips complex is the boundary of a triangle, and an edge in
    this graph can be longer than birth. Use ``rips_h1_representatives``.

    Args:
        point_cloud: (n, 2) point positions.
        birth: Birth filtration value of the H1 feature.
        death: Death filtration value of the H1 feature.
        min_length: Minimum cycle vertex count (default 3).
        max_length: Maximum cycle vertex count (default 8).

    Returns:
        List of Cycle objects sorted by score (best first).
    """
    n = len(point_cloud)
    if n < min_length:
        return []

    dist_matrix = squareform(pdist(point_cloud))
    max_len = min(max_length, n)

    adjacency = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            d = dist_matrix[i, j]
            if birth <= d <= death:
                adjacency[i].append(j)
                adjacency[j].append(i)

    raw_cycles = _bfs_cycles(adjacency, n, min_length, max_len)

    mid = (birth + death) / 2.0
    scored = []
    for cycle_nodes in raw_cycles:
        edge_dists = [
            dist_matrix[cycle_nodes[i], cycle_nodes[(i + 1) % len(cycle_nodes)]]
            for i in range(len(cycle_nodes))
        ]
        avg_dev = np.mean([abs(d - mid) for d in edge_dists])
        score = 1.0 / (1.0 + avg_dev)

        scored.append(Cycle(
            nodes=cycle_nodes,
            score=score,
            edge_distances=edge_dists,
            birth=birth,
            death=death,
        ))

    scored.sort(key=lambda c: c.score, reverse=True)
    return scored


def _bfs_cycles(
    adjacency: dict,
    n_nodes: int,
    min_length: int,
    max_length: int,
) -> List[List[int]]:
    """BFS-based enumeration of simple cycles."""
    all_cycles = []
    seen = set()

    for start in range(n_nodes):
        queue = [(start, [start])]
        while queue:
            current, path = queue.pop(0)

            if len(path) >= min_length + 1 and current == start and len(path) > 2:
                key = frozenset(path[:-1])
                if key not in seen:
                    all_cycles.append(path[:-1])
                    seen.add(key)

            if len(path) < max_length:
                for nbr in adjacency.get(current, []):
                    if len(path) == 1 or nbr != path[-2]:
                        if nbr not in path or (nbr == start and len(path) >= min_length):
                            queue.append((nbr, path + [nbr]))

    return all_cycles
