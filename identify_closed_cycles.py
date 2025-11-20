#!/usr/bin/env python3
"""
Closed Cycle Identification for H1 Loops
=========================================

Identifies actual closed cycles (node-vertex loops) in the graph
to properly visualize H1 loops.
"""

import numpy as np
from scipy.spatial.distance import squareform, pdist
from collections import defaultdict


def find_closed_cycles_bfs(adjacency, min_cycle_length=3, max_cycle_length=8):
    """
    Find all closed cycles in a graph using BFS
    
    Args:
        adjacency: Dict of {node: [neighbors]}
        min_cycle_length: Minimum cycle length
        max_cycle_length: Maximum cycle length
    
    Returns:
        List of cycles, where each cycle is a list of node indices forming a closed path
    """
    cycles = []
    n = len(adjacency)
    
    def find_cycles_from_start(start):
        """Find all cycles starting from a given node"""
        # BFS to find paths that return to start
        queue = [(start, [start])]  # (current_node, path)
        visited_paths = set()
        
        while queue:
            current, path = queue.pop(0)
            
            # Check if we can return to start (forming a cycle)
            if len(path) >= min_cycle_length + 1 and current == start and len(path) > 2:
                cycle_tuple = tuple(sorted(path[:-1]))  # Remove duplicate start
                if cycle_tuple not in visited_paths:
                    cycles.append(path[:-1])  # Remove duplicate start
                    visited_paths.add(cycle_tuple)
            
            # Continue BFS if path not too long
            if len(path) < max_cycle_length:
                for neighbor in adjacency[current]:
                    # Don't go back immediately (avoid trivial cycles)
                    if len(path) == 1 or neighbor != path[-2]:
                        if neighbor not in path or (neighbor == start and len(path) >= min_cycle_length):
                            queue.append((neighbor, path + [neighbor]))
    
    # Find cycles starting from each node
    for start in range(n):
        find_cycles_from_start(start)
    
    # Remove duplicates (cycles that are rotations/reversals of each other)
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        cycle_set = frozenset(cycle)
        if cycle_set not in seen and len(cycle) >= min_cycle_length:
            unique_cycles.append(cycle)
            seen.add(cycle_set)
    
    return unique_cycles


def identify_h1_closed_cycles(point_cloud, birth, death):
    """
    Identify closed cycles that represent H1 loops
    
    A closed cycle is a path: v0 -> v1 -> ... -> vk -> v0
    where all edges are in the [birth, death] range
    """
    n = len(point_cloud)
    if n < 3:
        return []
    
    distances = squareform(pdist(point_cloud))
    
    # Build adjacency list: nodes connected by edges in birth-death range
    adjacency = defaultdict(list)
    loop_edges = []
    
    for i in range(n):
        for j in range(i+1, n):
            d = distances[i, j]
            if birth <= d <= death:
                adjacency[i].append(j)
                adjacency[j].append(i)
                loop_edges.append((i, j))
    
    # Find closed cycles
    cycles = find_closed_cycles_bfs(adjacency, min_cycle_length=3, max_cycle_length=min(8, n))
    
    # Score cycles by how well they represent the loop
    # Prefer cycles where all edges are close to the middle of birth-death range
    scored_cycles = []
    mid_point = (birth + death) / 2
    
    for cycle in cycles:
        # Calculate average edge distance from midpoint
        cycle_edges = []
        for i in range(len(cycle)):
            j = (i + 1) % len(cycle)
            d = distances[cycle[i], cycle[j]]
            cycle_edges.append(d)
        
        avg_dist_from_mid = np.mean([abs(d - mid_point) for d in cycle_edges])
        score = 1.0 / (1.0 + avg_dist_from_mid)  # Higher score = better
        
        scored_cycles.append({
            'cycle': cycle,
            'score': score,
            'edges': cycle_edges,
            'avg_distance': np.mean(cycle_edges)
        })
    
    # Sort by score
    scored_cycles.sort(key=lambda x: x['score'], reverse=True)
    
    return scored_cycles, loop_edges


def find_simple_cycles_graph(point_cloud, birth, death):
    """
    Alternative: Find simple cycles using a graph algorithm
    
    Returns the longest/most significant cycle
    """
    n = len(point_cloud)
    distances = squareform(pdist(point_cloud))
    
    # Build adjacency matrix
    adj = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i+1, n):
            d = distances[i, j]
            if birth <= d <= death:
                adj[i, j] = True
                adj[j, i] = True
    
    # Find cycles using DFS
    def find_cycle_dfs(start, current, path, visited_edges):
        """Find cycle starting from start, currently at current"""
        if len(path) >= 3 and current == start:
            return path
        
        if len(path) > n:
            return None
        
        for neighbor in range(n):
            if adj[current, neighbor] and (current, neighbor) not in visited_edges:
                if neighbor == start and len(path) >= 3:
                    return path + [start]
                elif neighbor not in path:
                    result = find_cycle_dfs(start, neighbor, path + [neighbor], 
                                           visited_edges | {(current, neighbor), (neighbor, current)})
                    if result:
                        return result
        return None
    
    # Try to find cycles
    cycles = []
    for start in range(n):
        cycle = find_cycle_dfs(start, start, [start], set())
        if cycle and cycle not in cycles:
            cycles.append(cycle)
    
    return cycles


if __name__ == '__main__':
    # Test
    import json
    
    with open('h1_loop_analysis/h1_loops_full_data.json', 'r') as f:
        loops_data = json.load(f)
    
    # Test on a tactical loop
    tactical_loops = [l for l in loops_data if l['scale'] == 'tactical' and l['persistence'] > 8]
    
    if tactical_loops:
        loop = tactical_loops[0]
        pc = np.array(loop['point_cloud'])
        birth = loop['birth']
        death = loop['death']
        
        print(f"Testing cycle identification on tactical loop:")
        print(f"  Frame {loop['frame_idx']}, Persistence={loop['persistence']:.3f}")
        print(f"  Points: {len(pc)}, Birth: {birth:.2f}, Death: {death:.2f}")
        print()
        
        cycles, edges = identify_h1_closed_cycles(pc, birth, death)
        
        print(f"Found {len(cycles)} closed cycles")
        if cycles:
            best_cycle = cycles[0]
            print(f"\nBest cycle (score={best_cycle['score']:.3f}):")
            print(f"  Nodes: {best_cycle['cycle']}")
            print(f"  Edge distances: {[f'{d:.2f}' for d in best_cycle['edges']]}")
            print(f"  Forms closed loop: {best_cycle['cycle'][0]} -> ... -> {best_cycle['cycle'][-1]} -> {best_cycle['cycle'][0]}")
        else:
            print("  No closed cycles found!")
            print(f"  Total edges in range: {len(edges)}")

