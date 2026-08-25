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
    'individual': 2.98,
    'tactical': 12.0,
    'team': 30.0,
}

EXPECTED_H0_RANGES = {
    'individual': (15, 22),
    'tactical': (2, 12),
    'team': (1, 3),
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
    Compute adaptive max filtration for the Vietoris-Rips complex.

    Formula: max(P_percentile(inter-centroid distances), max(floor, scale_factor * cutoff))

    Args:
        centroids: (k, 2) cluster centroid positions.
        cutoff: The clustering cutoff distance used.
        percentile: Percentile of pairwise distances (default 75).
        floor: Minimum absolute filtration value (default 5.0 m).
        scale_factor: Multiplier on cutoff for minimum (default 2.0).

    Returns:
        Maximum filtration value (float).
    """
    if centroids is None or len(centroids) <= 1:
        return max(floor, scale_factor * cutoff)

    dists = pdist(centroids)
    if len(dists) == 0:
        return max(floor, scale_factor * cutoff)

    data_driven = np.percentile(dists, percentile)
    scale_minimum = max(floor, scale_factor * cutoff)
    return max(data_driven, scale_minimum)


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
    Find closed cycles representing H1 loops in the Vietoris-Rips complex.

    Constructs the adjacency graph of edges with distances in [birth, death]
    and enumerates simple cycles via BFS.

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
