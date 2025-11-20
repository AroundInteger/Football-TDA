#!/usr/bin/env python3
"""
H1 Loops In-Play Visualization
===============================

Visualizes actual H1 loops from Vietoris-Rips complexes overlaid
on player positions (x, y, t) on the field.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster
from ripser import ripser
from matplotlib.patches import Circle, Polygon, FancyBboxPatch, Rectangle
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')


def reconstruct_vr_complex(point_cloud, max_filtration):
    """
    Reconstruct Vietoris-Rips complex structure at max_filtration
    
    Returns:
        edges: List of edges (pairs of indices)
        triangles: List of triangles (triples of indices)
    """
    n = len(point_cloud)
    if n < 2:
        return [], []
    
    # Compute distance matrix
    distances = squareform(pdist(point_cloud))
    
    # Find edges (pairs within filtration distance)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if distances[i, j] <= max_filtration:
                edges.append((i, j))
    
    # Find triangles (triples where all edges within filtration)
    triangles = []
    for i in range(n):
        for j in range(i+1, n):
            if distances[i, j] <= max_filtration:
                for k in range(j+1, n):
                    if distances[i, k] <= max_filtration and distances[j, k] <= max_filtration:
                        triangles.append((i, j, k))
    
    return edges, triangles


def find_closed_cycles_graph(point_cloud, birth, death):
    """
    Find actual closed cycles (node-vertex loops) in the graph
    
    Returns closed cycles as lists of node indices forming loops
    """
    from collections import defaultdict
    
    n = len(point_cloud)
    if n < 3:
        return []
    
    distances = squareform(pdist(point_cloud))
    
    # Build adjacency list: nodes connected by edges in birth-death range
    adjacency = defaultdict(list)
    for i in range(n):
        for j in range(i+1, n):
            d = distances[i, j]
            if birth <= d <= death:
                adjacency[i].append(j)
                adjacency[j].append(i)
    
    # Find cycles using DFS
    def find_cycle_dfs(start, current, path, visited_edges, max_depth=8):
        """Find cycle starting from start, currently at current"""
        # Found a cycle: path returns to start and has at least 3 nodes
        if len(path) >= 3 and current == start:
            return path[:-1]  # Remove duplicate start
        
        # Prevent infinite loops
        if len(path) > max_depth or len(path) > n:
            return None
        
        # Continue DFS
        for neighbor in adjacency[current]:
            edge = tuple(sorted([current, neighbor]))
            
            # Can return to start if path is long enough
            if neighbor == start and len(path) >= 3:
                return path
            
            # Continue path if neighbor not in path (except for closing cycle)
            if neighbor not in path and edge not in visited_edges:
                result = find_cycle_dfs(start, neighbor, path + [neighbor],
                                       visited_edges | {edge}, max_depth)
                if result:
                    return result
        
        return None
    
    # Find cycles starting from each node
    cycles = []
    seen_cycles = set()
    
    for start in range(n):
        cycle = find_cycle_dfs(start, start, [start], set())
        if cycle:
            # Normalize cycle (start from smallest index, canonical form)
            cycle_set = frozenset(cycle)
            if cycle_set not in seen_cycles and len(cycle) >= 3:
                cycles.append(cycle)
                seen_cycles.add(cycle_set)
    
    return cycles


def identify_h1_loop_cycles(point_cloud, edges, triangles, birth, death):
    """
    Identify actual closed cycles (node-vertex loops) that form H1 loops
    
    H1 loops are CLOSED CYCLES: v0 -> v1 -> ... -> vk -> v0
    where all edges are in the [birth, death] range
    """
    n = len(point_cloud)
    distances = squareform(pdist(point_cloud))
    
    # Find actual closed cycles
    closed_cycles = find_closed_cycles_graph(point_cloud, birth, death)
    
    # Extract edges from closed cycles
    cycle_edges = []
    if closed_cycles:
        # Use the longest cycle (likely the main loop)
        main_cycle = max(closed_cycles, key=len)
        for i in range(len(main_cycle)):
            j = (i + 1) % len(main_cycle)  # Wrap around to close the cycle
            cycle_edges.append((main_cycle[i], main_cycle[j]))
    else:
        # Fallback: show all edges in birth-death range
        for i, j in edges:
            d = distances[i, j]
            if birth <= d <= death:
                cycle_edges.append((i, j))
    
    # Find triangles that bound loops
    # In VR complex, triangles can "fill in" the loop (causing its death)
    loop_triangles = []
    for i, j, k in triangles:
        d_ij = distances[i, j]
        d_jk = distances[j, k]
        d_ki = distances[k, i]
        
        # Triangle fills loop if all edges appear, closing the hole
        max_edge = max(d_ij, d_jk, d_ki)
        min_edge = min(d_ij, d_jk, d_ki)
        
        if birth <= min_edge and max_edge <= death:
            loop_triangles.append((i, j, k))
    
    return cycle_edges, loop_triangles, closed_cycles


def visualize_loop_in_formation(frame_data, loop_info, output_dir=None):
    """
    Visualize a specific H1 loop overlaid on the actual formation
    
    Args:
        frame_data: Dictionary with player positions and loop info
        loop_info: Loop information (birth, death, persistence, etc.)
        output_dir: Output directory
    """
    if output_dir is None:
        output_dir = Path('h1_loop_analysis/in_play_visualizations')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    point_cloud = np.array(frame_data['point_cloud'])
    birth = loop_info['birth']
    death = loop_info['death']
    persistence = loop_info['persistence']
    scale = loop_info['scale']
    frame_idx = loop_info['frame_idx']
    
    # Reconstruct VR complex at death (when loop is fully formed)
    edges, triangles = reconstruct_vr_complex(point_cloud, death)
    
    # Identify loop cycles (including closed cycles)
    cycle_edges, loop_triangles, closed_cycles = identify_h1_loop_cycles(point_cloud, edges, triangles, birth, death)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Draw field background (football field ~105m x 68m)
    # Coordinates are centered at (0, 0), so field should be centered
    field_length = 105
    field_width = 68
    
    # Calculate field bounds (centered at origin)
    field_x_min = -field_length / 2
    field_x_max = field_length / 2
    field_y_min = -field_width / 2
    field_y_max = field_width / 2
    
    # Field rectangle (centered at origin)
    field = Rectangle((field_x_min, field_y_min), field_length, field_width, 
                     facecolor='#2d5016', edgecolor='white', linewidth=2, zorder=0)
    ax.add_patch(field)
    
    # Center line (vertical line at x=0)
    ax.axvline(0, color='white', linestyle='-', linewidth=2, alpha=0.5, zorder=1)
    
    # Center circle (centered at origin)
    center_circle = Circle((0, 0), 9.15, 
                          fill=False, edgecolor='white', linewidth=2, alpha=0.5, zorder=1)
    ax.add_patch(center_circle)
    
    # Add penalty areas and goal areas (optional, for better context)
    # Penalty area: 16.5m x 40.3m
    penalty_length = 16.5
    penalty_width = 40.3
    
    # Left penalty area
    penalty_left = Rectangle((field_x_min, -penalty_width/2), penalty_length, penalty_width,
                            fill=False, edgecolor='white', linewidth=1.5, alpha=0.7, zorder=1)
    ax.add_patch(penalty_left)
    
    # Right penalty area
    penalty_right = Rectangle((field_x_max - penalty_length, -penalty_width/2), penalty_length, penalty_width,
                             fill=False, edgecolor='white', linewidth=1.5, alpha=0.7, zorder=1)
    ax.add_patch(penalty_right)
    
    # Draw all edges (gray, low opacity)
    if edges:
        edge_coords = [[point_cloud[i], point_cloud[j]] for i, j in edges]
        edge_array = np.array(edge_coords)
        lc_all = LineCollection(edge_array, colors='lightgray', linewidths=0.5,
                               alpha=0.2, zorder=2, label='VR Complex Edges')
        ax.add_collection(lc_all)
    
    # Draw cycle edges (red, highlight loops)
    if cycle_edges:
        cycle_coords = [[point_cloud[i], point_cloud[j]] for i, j in cycle_edges]
        cycle_array = np.array(cycle_coords)
        lc_cycles = LineCollection(cycle_array, colors='red', linewidths=3,
                                  alpha=0.7, zorder=4, label='H1 Loop (Closed Cycle)')
        ax.add_collection(lc_cycles)
    
    # Highlight closed cycle structure if found
    if closed_cycles and len(closed_cycles) > 0:
        main_cycle = max(closed_cycles, key=len)
        cycle_points = point_cloud[main_cycle]
        
        # Draw cycle as a polygon to show it's closed
        cycle_polygon = Polygon(cycle_points, fill=False, edgecolor='red', 
                               linewidth=4, linestyle='-', alpha=0.9, zorder=5,
                               label='Closed Cycle Structure')
        ax.add_patch(cycle_polygon)
        
        # Highlight cycle nodes
        ax.scatter(cycle_points[:, 0], cycle_points[:, 1],
                  s=400, c='red', alpha=0.8, edgecolors='yellow',
                  linewidth=3, zorder=6, marker='s', label='Cycle Nodes')
        
        # Add cycle path labels
        for idx, node_idx in enumerate(main_cycle):
            x, y = point_cloud[node_idx]
            ax.text(x, y + 2, f'{idx+1}', ha='center', va='bottom',
                   fontsize=11, fontweight='bold', color='yellow',
                   bbox=dict(boxstyle='circle', facecolor='red', alpha=0.8),
                   zorder=7)
    
    # Draw loop triangles (filled, highlight enclosed regions)
    if loop_triangles:
        triangle_coords = []
        for i, j, k in loop_triangles:
            triangle_coords.append([point_cloud[i], point_cloud[j], point_cloud[k]])
        
        triangle_array = np.array(triangle_coords)
        for triangle in triangle_array:
            polygon = Polygon(triangle, fill=True, alpha=0.3, 
                            color='red', edgecolor='red', linewidth=2, zorder=3)
            ax.add_patch(polygon)
    
    # Draw points (cluster centroids or players)
    ax.scatter(point_cloud[:, 0], point_cloud[:, 1], 
              s=300, c='blue', alpha=0.8, edgecolors='white', 
              linewidth=2, zorder=5, label='Cluster Centroids')
    
    # Add point labels
    for i, (x, y) in enumerate(point_cloud):
        ax.text(x, y, f'{i+1}', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white', zorder=6)
    
    # Title and info
    title = (f'H1 Loop in Play: {scale.capitalize()} Scale | Frame {frame_idx}\n'
            f'Persistence: {persistence:.3f} | Birth: {birth:.2f}m | Death: {death:.2f}m')
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='white',
                bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.8))
    
    ax.set_xlabel('Field X Position (meters, center at 0)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Field Y Position (meters, center at 0)', fontsize=12, fontweight='bold')
    
    # Set limits based on actual data with padding
    x_min, x_max = point_cloud[:, 0].min(), point_cloud[:, 0].max()
    y_min, y_max = point_cloud[:, 1].min(), point_cloud[:, 1].max()
    
    # Ensure field is fully visible, but also show data
    x_range = max(field_length, x_max - x_min) + 10
    y_range = max(field_width, y_max - y_min) + 10
    
    ax.set_xlim(-x_range/2, x_range/2)
    ax.set_ylim(-y_range/2, y_range/2)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.3, color='white', linestyle='--', zorder=1)
    
    # Info box
    cycle_info = ""
    if closed_cycles and len(closed_cycles) > 0:
        main_cycle = max(closed_cycles, key=len)
        cycle_info = f'Closed Cycle: {" -> ".join([str(i+1) for i in main_cycle])} -> {main_cycle[0]+1}\n'
    
    info_text = (f'Loop Information:\n'
                f'Scale: {scale.capitalize()}\n'
                f'Persistence: {persistence:.3f}\n'
                f'Birth: {birth:.2f}m\n'
                f'Death: {death:.2f}m\n'
                f'Points: {len(point_cloud)}\n'
                f'Cycle Edges: {len(cycle_edges)}\n'
                f'Closed Cycles: {len(closed_cycles)}\n'
                f'{cycle_info}')
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9,
                    edgecolor='black', linewidth=2), zorder=10)
    
    # Legend
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    
    # Invert y-axis for proper field orientation (if needed)
    # ax.invert_yaxis()
    
    plt.tight_layout()
    output_file = output_dir / f'loop_in_play_{scale}_frame{frame_idx}_persistence{persistence:.2f}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output_file


def create_temporal_loop_sequence(loops_data, scale='individual', max_loops=10):
    """Create sequence of frames showing loop evolution"""
    
    output_dir = Path('h1_loop_analysis/in_play_visualizations')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get loops for this scale, sorted by persistence
    scale_loops = [l for l in loops_data if l['scale'] == scale]
    scale_loops.sort(key=lambda x: x['persistence'], reverse=True)
    
    # Take top N most persistent loops
    selected_loops = scale_loops[:max_loops]
    
    print(f"Creating temporal sequence for {len(selected_loops)} loops at {scale} scale...")
    
    created_files = []
    for loop_info in selected_loops:
        if 'point_cloud' in loop_info and loop_info['point_cloud']:
            output_file = visualize_loop_in_formation(
                {'point_cloud': loop_info['point_cloud']}, 
                loop_info, 
                output_dir
            )
            if output_file:
                created_files.append(output_file)
    
    return created_files


def create_multi_loop_comparison(loops_data, frame_indices=None, scale='individual'):
    """Compare multiple loops at different frames"""
    
    if frame_indices is None:
        # Select frames with highest H1 counts
        frame_data = {}
        for loop in loops_data:
            if loop['scale'] == scale:
                frame_idx = loop['frame_idx']
                if frame_idx not in frame_data:
                    frame_data[frame_idx] = []
                frame_data[frame_idx].append(loop)
        
        # Get frames with most loops
        frame_counts = {f: len(loops) for f, loops in frame_data.items()}
        frame_indices = sorted(frame_counts.keys(), key=lambda x: frame_counts[x], reverse=True)[:4]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'H1 Loops In-Play: {scale.capitalize()} Scale - Frame Comparison', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    axes = axes.flatten()
    
    for idx, frame_idx in enumerate(frame_indices[:4]):
        ax = axes[idx]
        
        # Find loops for this frame
        frame_loops = [l for l in loops_data 
                      if l['scale'] == scale and l['frame_idx'] == frame_idx]
        
        if not frame_loops:
            ax.text(0.5, 0.5, f'No loops\nat frame {frame_idx}',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=12, fontweight='bold')
            ax.set_title(f'Frame {frame_idx}', fontsize=12, fontweight='bold')
            continue
        
        # Use the most persistent loop for visualization
        best_loop = max(frame_loops, key=lambda x: x['persistence'])
        point_cloud = np.array(best_loop['point_cloud'])
        birth = best_loop['birth']
        death = best_loop['death']
        
        # Draw field background (centered at origin)
        field_length, field_width = 105, 68
        field = Rectangle((-field_length/2, -field_width/2), field_length, field_width, 
                         facecolor='#2d5016', edgecolor='white', linewidth=1, zorder=0)
        ax.add_patch(field)
        ax.axvline(0, color='white', linestyle='-', linewidth=1, alpha=0.5, zorder=1)
        
        # Center circle
        center_circle = Circle((0, 0), 9.15, 
                              fill=False, edgecolor='white', linewidth=1, alpha=0.5, zorder=1)
        ax.add_patch(center_circle)
        
        # Reconstruct VR complex
        edges, triangles = reconstruct_vr_complex(point_cloud, death)
        cycle_edges, loop_triangles, closed_cycles = identify_h1_loop_cycles(point_cloud, edges, triangles, birth, death)
        
        # Draw edges
        if edges:
            edge_coords = [[point_cloud[i], point_cloud[j]] for i, j in edges]
            lc_all = LineCollection(edge_coords, colors='lightgray', linewidths=0.3,
                                   alpha=0.1, zorder=2)
            ax.add_collection(lc_all)
        
        # Draw loops (closed cycles)
        if cycle_edges:
            cycle_coords = [[point_cloud[i], point_cloud[j]] for i, j in cycle_edges]
            lc_cycles = LineCollection(cycle_coords, colors='red', linewidths=2,
                                      alpha=0.7, zorder=4)
            ax.add_collection(lc_cycles)
        
        # Highlight closed cycle structure
        if closed_cycles and len(closed_cycles) > 0:
            main_cycle = max(closed_cycles, key=len)
            cycle_points = point_cloud[main_cycle]
            cycle_polygon = Polygon(cycle_points, fill=False, edgecolor='red',
                                   linewidth=3, linestyle='-', alpha=0.9, zorder=5)
            ax.add_patch(cycle_polygon)
        
        # Draw loop regions (triangles that fill the loop)
        for i, j, k in loop_triangles:
            polygon = Polygon([point_cloud[i], point_cloud[j], point_cloud[k]],
                            fill=True, alpha=0.2, color='red', edgecolor='red', 
                            linewidth=1, zorder=3)
            ax.add_patch(polygon)
        
        # Draw points
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], 
                  s=150, c='blue', alpha=0.8, edgecolors='white', 
                  linewidth=1.5, zorder=5)
        
        ax.set_title(f'Frame {frame_idx}: {len(frame_loops)} loop(s) | '
                    f'Max persistence: {best_loop["persistence"]:.2f}',
                    fontsize=11, fontweight='bold', pad=10)
        
        # Set limits based on data
        x_min, x_max = point_cloud[:, 0].min(), point_cloud[:, 0].max()
        y_min, y_max = point_cloud[:, 1].min(), point_cloud[:, 1].max()
        x_range = max(field_length, x_max - x_min) + 10
        y_range = max(field_width, y_max - y_min) + 10
        
        ax.set_xlim(-x_range/2, x_range/2)
        ax.set_ylim(-y_range/2, y_range/2)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(True, alpha=0.2, color='white', linestyle='--', zorder=1)
    
    output_dir = Path('h1_loop_analysis/in_play_visualizations')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.tight_layout()
    output_file = output_dir / f'h1_loops_comparison_{scale}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Multi-loop comparison saved: {output_file}")
    plt.close()
    
    return output_file


def main():
    """Main visualization function"""
    print("="*70)
    print("H1 LOOPS IN-PLAY VISUALIZATION")
    print("="*70)
    print()
    
    # Load full loop data with point clouds
    full_data_file = Path('h1_loop_analysis/h1_loops_full_data.json')
    
    if not full_data_file.exists():
        print(f"❌ Full loop data not found: {full_data_file}")
        print("   Run analyze_h1_loops.py first")
        return
    
    print("📊 Loading loop data with point clouds...")
    with open(full_data_file, 'r') as f:
        loops_data = json.load(f)
    
    print(f"✅ Loaded {len(loops_data)} loop records")
    print()
    
    # Filter to loops with point clouds
    loops_with_data = [l for l in loops_data if 'point_cloud' in l and l['point_cloud']]
    print(f"✅ {len(loops_with_data)} loops have point cloud data")
    print()
    
    # Create visualizations for each scale
    print("📈 Creating in-play visualizations...")
    print()
    
    for scale in ['individual', 'tactical']:
        scale_loops = [l for l in loops_with_data if l['scale'] == scale]
        
        if len(scale_loops) > 0:
            print(f"  {scale.capitalize()} scale: {len(scale_loops)} loops with data")
            
            # Create individual loop visualizations (top 5 most persistent)
            scale_loops_sorted = sorted(scale_loops, key=lambda x: x['persistence'], reverse=True)
            top_loops = scale_loops_sorted[:5]
            
            for loop_info in top_loops:
                visualize_loop_in_formation(
                    {'point_cloud': loop_info['point_cloud']},
                    loop_info
                )
            
            # Create multi-loop comparison
            create_multi_loop_comparison(loops_with_data, scale=scale)
    
    print()
    print("="*70)
    print("✅ ALL IN-PLAY VISUALIZATIONS COMPLETE!")
    print("="*70)
    print()
    print("📁 Generated files in h1_loop_analysis/in_play_visualizations/:")
    print("  • loop_in_play_*.png - Individual loop visualizations")
    print("  • h1_loops_comparison_*.png - Multi-frame comparisons")
    print()
    print("💡 These visualizations show:")
    print("  • Actual player/cluster positions on field")
    print("  • Vietoris-Rips complex edges (gray)")
    print("  • H1 loop structures (red edges and filled regions)")
    print("  • Loop persistence and birth/death times")
    print()
    print("="*70)


if __name__ == '__main__':
    main()

