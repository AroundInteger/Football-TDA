#!/usr/bin/env python3
"""
H1 Loop Visualization
======================

Creates presentation-ready visualizations of actual H1 loops,
their persistence, and lifetimes.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from matplotlib.patches import Circle, Polygon, FancyBboxPatch
from matplotlib.collections import LineCollection
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')


def load_loop_data():
    """Load H1 loop analysis data"""
    loops_file = Path('h1_loop_analysis/h1_loops_detailed.csv')
    full_data_file = Path('h1_loop_analysis/h1_loops_full_data.json')
    
    if not loops_file.exists():
        print(f"❌ Loop data not found: {loops_file}")
        print("   Run analyze_h1_loops.py first")
        return None, None
    
    loops_df = pd.read_csv(loops_file)
    
    # Load full data with point clouds if available
    full_data = None
    if full_data_file.exists():
        with open(full_data_file, 'r') as f:
            full_data = json.load(f)
    
    return loops_df, full_data


def create_persistence_diagram(loops_df, scale='individual', output_dir=None):
    """Create persistence diagram (birth vs death) for H1 loops"""
    
    if output_dir is None:
        output_dir = Path('h1_loop_analysis')
    output_dir.mkdir(exist_ok=True)
    
    scale_data = loops_df[loops_df['scale'] == scale].copy()
    
    if len(scale_data) == 0:
        print(f"⚠️  No loops found for {scale} scale")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Extract birth and death times
    births = scale_data['birth'].values
    deaths = scale_data['death'].values
    persistence = scale_data['persistence'].values
    
    # Create scatter plot colored by persistence
    scatter = ax.scatter(births, deaths, c=persistence, 
                        s=100, alpha=0.6, cmap='viridis',
                        edgecolors='black', linewidth=1)
    
    # Add diagonal line (birth = death)
    max_val = max(births.max(), deaths.max())
    ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, 
           alpha=0.5, label='Birth = Death')
    
    # Add persistence lines (vertical distance from diagonal)
    # Highlight top 10% most persistent loops
    threshold = np.percentile(persistence, 90)
    high_persist = scale_data[scale_data['persistence'] >= threshold]
    
    for _, loop in high_persist.iterrows():
        ax.plot([loop['birth'], loop['birth']], 
               [loop['birth'], loop['death']], 
               'orange', linewidth=2, alpha=0.5)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Persistence (Death - Birth)', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Birth Time (Filtration Value)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Death Time (Filtration Value)', fontsize=13, fontweight='bold')
    ax.set_title(f'H1 Persistence Diagram: {scale.capitalize()} Scale\n'
                f'Total Loops: {len(scale_data)} | Mean Persistence: {persistence.mean():.3f}',
                fontsize=14, fontweight='bold', pad=15)
    
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Add statistics text
    stats_text = (f'Statistics:\n'
                 f'Mean persistence: {persistence.mean():.3f}\n'
                 f'Max persistence: {persistence.max():.3f}\n'
                 f'Mean birth: {births.mean():.3f}\n'
                 f'Mean death: {deaths.mean():.3f}')
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    output_file = output_dir / f'h1_persistence_diagram_{scale}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Persistence diagram saved: {output_file}")
    plt.close()
    
    return fig


def create_loop_lifetime_timeline(loops_df, output_dir=None):
    """Create timeline visualization showing loop lifetimes"""
    
    if output_dir is None:
        output_dir = Path('h1_loop_analysis')
    output_dir.mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(3, 1, figsize=(16, 12))
    fig.suptitle('H1 Loop Lifetimes: Temporal Evolution Across Scales', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    scales = ['individual', 'tactical', 'team']
    colors_scale = ['#2E7D32', '#1976D2', '#D32F2F']
    
    for idx, (scale, color) in enumerate(zip(scales, colors_scale)):
        ax = axes[idx]
        
        scale_data = loops_df[loops_df['scale'] == scale].copy()
        
        if len(scale_data) == 0:
            ax.text(0.5, 0.5, f'No loops detected at {scale} scale',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=12, fontweight='bold')
            ax.set_title(f'{scale.capitalize()} Scale', fontsize=13, fontweight='bold')
            continue
        
        # Group by frame to show H1 count over time
        frame_counts = scale_data.groupby('frame_idx').agg({
            'h1_count': 'first',
            'persistence': ['mean', 'max', 'count'],
            'timestamp': 'first'
        }).reset_index()
        
        frame_counts.columns = ['frame_idx', 'h1_count', 'mean_persistence', 
                               'max_persistence', 'loop_count', 'timestamp']
        
        # Plot H1 count over time
        ax.plot(frame_counts['timestamp'], frame_counts['h1_count'], 
               'o-', color=color, linewidth=2, markersize=6,
               alpha=0.7, label='H1 Count', zorder=3)
        
        # Fill area under curve
        ax.fill_between(frame_counts['timestamp'], 0, frame_counts['h1_count'],
                       alpha=0.2, color=color, zorder=2)
        
        # Add persistence information as secondary axis
        ax2 = ax.twinx()
        ax2.plot(frame_counts['timestamp'], frame_counts['mean_persistence'],
                's--', color='orange', linewidth=2, markersize=4,
                alpha=0.7, label='Mean Persistence', zorder=4)
        
        ax.set_xlabel('Time (seconds)', fontsize=11, fontweight='bold')
        ax.set_ylabel('H1 Count (Loops)', fontsize=11, fontweight='bold', color=color)
        ax2.set_ylabel('Mean Persistence', fontsize=11, fontweight='bold', color='orange')
        ax.tick_params(axis='y', labelcolor=color)
        ax2.tick_params(axis='y', labelcolor='orange')
        
        # Statistics
        total_frames = scale_data['frame_idx'].nunique()
        frames_with_loops = len(frame_counts[frame_counts['h1_count'] > 0])
        mean_h1 = scale_data.groupby('frame_idx')['h1_count'].first().mean()
        mean_persist = scale_data['persistence'].mean()
        
        title = (f'{scale.capitalize()} Scale: '
                f'{frames_with_loops}/{total_frames} frames with loops | '
                f'Mean H1: {mean_h1:.2f} | Mean Persistence: {mean_persist:.3f}')
        
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        ax.grid(True, alpha=0.3, zorder=1)
        
        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    output_file = output_dir / 'h1_lifetime_timeline.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Lifetime timeline saved: {output_file}")
    plt.close()
    
    return fig


def visualize_loop_in_formation(point_cloud, h1_diagram, loop_idx, scale_name, frame_idx, output_dir=None):
    """Visualize a specific loop in the formation"""
    
    if output_dir is None:
        output_dir = Path('h1_loop_analysis/loop_visualizations')
    output_dir.mkdir(exist_ok=True)
    
    if len(h1_diagram) == 0 or loop_idx >= len(h1_diagram):
        return None
    
    birth, death = h1_diagram[loop_idx]
    persistence = death - birth
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot points
    ax.scatter(point_cloud[:, 0], point_cloud[:, 1], 
              s=200, c='blue', alpha=0.7, edgecolors='black', 
              linewidth=2, zorder=3, label='Cluster Centroids')
    
    # Add labels
    for i, (x, y) in enumerate(point_cloud):
        ax.text(x, y, f'P{i+1}', ha='center', va='center',
               fontsize=9, fontweight='bold', color='white', zorder=4)
    
    # Draw connections at death time (full loop)
    # Create edges for all pairs within death distance
    n_points = len(point_cloud)
    edges = []
    for i in range(n_points):
        for j in range(i+1, n_points):
            dist = np.linalg.norm(point_cloud[i] - point_cloud[j])
            if dist <= death:
                edges.append([point_cloud[i], point_cloud[j]])
    
    if edges:
        edge_array = np.array(edges)
        lc = LineCollection(edge_array, colors='gray', linewidths=1,
                          alpha=0.3, zorder=1)
        ax.add_collection(lc)
    
    # Highlight loop (connections that form at birth and persist until death)
    # This is simplified - actual loop identification would require complex computation
    # For visualization, we'll highlight edges that appear around birth time
    loop_edges = []
    for i in range(n_points):
        for j in range(i+1, n_points):
            dist = np.linalg.norm(point_cloud[i] - point_cloud[j])
            if birth <= dist <= death:
                loop_edges.append([point_cloud[i], point_cloud[j]])
    
    if loop_edges:
        loop_array = np.array(loop_edges)
        lc_loop = LineCollection(loop_array, colors='red', linewidths=3,
                               alpha=0.7, zorder=2, label='Loop Edges')
        ax.add_collection(lc_loop)
        
        # Highlight loop region
        if len(loop_edges) >= 3:
            # Try to find a closed loop
            points_in_loop = set()
            for edge in loop_edges:
                points_in_loop.add(tuple(edge[0]))
                points_in_loop.add(tuple(edge[1]))
            
            if len(points_in_loop) >= 3:
                loop_points = np.array(list(points_in_loop))
                # Simple convex hull for visualization
                from scipy.spatial import ConvexHull
                try:
                    hull = ConvexHull(loop_points)
                    polygon = Polygon(loop_points[hull.vertices], 
                                    fill=True, alpha=0.2, color='red',
                                    edgecolor='red', linewidth=2, zorder=1)
                    ax.add_patch(polygon)
                except:
                    pass
    
    ax.set_xlabel('X Position (meters)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y Position (meters)', fontsize=12, fontweight='bold')
    ax.set_title(f'H1 Loop #{loop_idx+1} at {scale_name.capitalize()} Scale\n'
                f'Frame {frame_idx} | Persistence: {persistence:.3f} | '
                f'Birth: {birth:.2f} | Death: {death:.2f}',
                fontsize=13, fontweight='bold', pad=15)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Add information box
    info_text = (f'Loop Information:\n'
                f'Persistence: {persistence:.3f}\n'
                f'Birth: {birth:.2f}m\n'
                f'Death: {death:.2f}m\n'
                f'Points: {len(point_cloud)}\n'
                f'Edges in loop: {len(loop_edges)}')
    
    ax.text(0.02, 0.02, info_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='bottom',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                    edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    output_file = output_dir / f'loop_{scale_name}_frame{frame_idx}_loop{loop_idx}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_file


def create_persistence_distribution(loops_df, output_dir=None):
    """Create distribution of persistence values"""
    
    if output_dir is None:
        output_dir = Path('h1_loop_analysis')
    output_dir.mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('H1 Persistence Distribution: How Long Do Loops Survive?', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    scales = ['individual', 'tactical', 'team']
    colors_scale = ['#2E7D32', '#1976D2', '#D32F2F']
    
    for idx, (scale, color) in enumerate(zip(scales, colors_scale)):
        ax = axes[idx]
        
        scale_data = loops_df[loops_df['scale'] == scale].copy()
        
        if len(scale_data) == 0:
            ax.text(0.5, 0.5, f'No loops\nat {scale} scale',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=12, fontweight='bold')
            ax.set_title(f'{scale.capitalize()} Scale', fontsize=12, fontweight='bold')
            continue
        
        persistence = scale_data['persistence'].values
        
        # Histogram
        n_bins = min(20, len(np.unique(persistence)))
        counts, bins, patches = ax.hist(persistence, bins=n_bins, 
                                       color=color, alpha=0.7,
                                       edgecolor='black', linewidth=1.5)
        
        # Color by persistence value
        cmap = plt.cm.viridis
        norm = plt.Normalize(persistence.min(), persistence.max())
        for count, patch in zip(counts, patches):
            patch.set_facecolor(cmap(norm(patch.get_x() + patch.get_width()/2)))
        
        # Add statistics
        mean_persist = persistence.mean()
        median_persist = np.median(persistence)
        max_persist = persistence.max()
        
        ax.axvline(mean_persist, color='red', linestyle='--', linewidth=2,
                  label=f'Mean: {mean_persist:.3f}', zorder=3)
        ax.axvline(median_persist, color='orange', linestyle='--', linewidth=2,
                  label=f'Median: {median_persist:.3f}', zorder=3)
        
        ax.set_xlabel('Persistence (Death - Birth)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title(f'{scale.capitalize()} Scale\n'
                    f'Mean: {mean_persist:.3f} | Max: {max_persist:.3f} | '
                    f'Total: {len(scale_data)} loops',
                    fontsize=12, fontweight='bold', pad=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_file = output_dir / 'h1_persistence_distribution.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Persistence distribution saved: {output_file}")
    plt.close()
    
    return fig


def create_presentation_summary(loops_df, output_dir=None):
    """Create a summary visualization for presentations"""
    
    if output_dir is None:
        output_dir = Path('h1_loop_analysis')
    output_dir.mkdir(exist_ok=True)
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    fig.suptitle('H1 Loop Analysis: Presentation Summary', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    scales = ['individual', 'tactical', 'team']
    colors_scale = ['#2E7D32', '#1976D2', '#D32F2F']
    
    # Row 1: Persistence diagrams
    for idx, (scale, color) in enumerate(zip(scales, colors_scale)):
        ax = fig.add_subplot(gs[0, idx])
        
        scale_data = loops_df[loops_df['scale'] == scale]
        
        if len(scale_data) > 0:
            births = scale_data['birth'].values
            deaths = scale_data['death'].values
            persistence = scale_data['persistence'].values
            
            ax.scatter(births, deaths, c=persistence, s=80, alpha=0.6,
                      cmap='viridis', edgecolors='black', linewidth=1)
            
            max_val = max(births.max(), deaths.max()) if len(births) > 0 else 10
            ax.plot([0, max_val], [0, max_val], 'r--', linewidth=1, alpha=0.5)
            
            ax.set_xlabel('Birth', fontsize=10, fontweight='bold')
            ax.set_ylabel('Death', fontsize=10, fontweight='bold')
            ax.set_title(f'{scale.capitalize()}: {len(scale_data)} loops', 
                        fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No loops', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, fontweight='bold')
            ax.set_title(f'{scale.capitalize()}', fontsize=11, fontweight='bold')
    
    # Row 2: Temporal evolution
    for idx, (scale, color) in enumerate(zip(scales, colors_scale)):
        ax = fig.add_subplot(gs[1, idx])
        
        scale_data = loops_df[loops_df['scale'] == scale]
        
        if len(scale_data) > 0:
            frame_counts = scale_data.groupby('frame_idx').agg({
                'h1_count': 'first',
                'timestamp': 'first'
            }).reset_index()
            
            ax.plot(frame_counts['timestamp'], frame_counts['h1_count'],
                   'o-', color=color, linewidth=2, markersize=4, alpha=0.7)
            ax.fill_between(frame_counts['timestamp'], 0, frame_counts['h1_count'],
                           alpha=0.2, color=color)
            
            ax.set_xlabel('Time (s)', fontsize=10, fontweight='bold')
            ax.set_ylabel('H1 Count', fontsize=10, fontweight='bold')
            ax.set_title(f'Loop Count Over Time', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Row 3: Statistics summary
    for idx, (scale, color) in enumerate(zip(scales, colors_scale)):
        ax = fig.add_subplot(gs[2, idx])
        ax.axis('off')
        
        scale_data = loops_df[loops_df['scale'] == scale]
        
        if len(scale_data) > 0:
            stats_text = (
                f'{scale.upper()} SCALE STATISTICS\n\n'
                f'Total Loops: {len(scale_data)}\n'
                f'Frames with Loops: {scale_data["frame_idx"].nunique()}\n\n'
                f'Persistence:\n'
                f'  Mean: {scale_data["persistence"].mean():.3f}\n'
                f'  Max: {scale_data["persistence"].max():.3f}\n'
                f'  Std: {scale_data["persistence"].std():.3f}\n\n'
                f'Birth/Death:\n'
                f'  Mean Birth: {scale_data["birth"].mean():.2f}\n'
                f'  Mean Death: {scale_data["death"].mean():.2f}'
            )
        else:
            stats_text = f'{scale.upper()} SCALE\n\nNo loops detected'
        
        ax.text(0.5, 0.5, stats_text, transform=ax.transAxes,
               ha='center', va='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.2,
                        edgecolor=color, linewidth=3))
    
    plt.savefig(output_dir / 'h1_loops_presentation_summary.png', 
               dpi=300, bbox_inches='tight')
    print(f"✅ Presentation summary saved")
    plt.close()


def main():
    """Main visualization function"""
    print("="*70)
    print("H1 LOOP VISUALIZATION")
    print("="*70)
    print()
    
    # Load data
    print("📊 Loading loop data...")
    loops_df, full_data = load_loop_data()
    
    if loops_df is None:
        print("❌ Cannot proceed without loop data")
        return
    
    print(f"✅ Loaded {len(loops_df)} loop records")
    print()
    
    output_dir = Path('h1_loop_analysis')
    
    # Create visualizations
    print("📈 Creating visualizations...")
    print()
    
    # Persistence diagrams for each scale
    for scale in ['individual', 'tactical', 'team']:
        create_persistence_diagram(loops_df, scale, output_dir)
    
    # Lifetime timeline
    create_loop_lifetime_timeline(loops_df, output_dir)
    
    # Persistence distribution
    create_persistence_distribution(loops_df, output_dir)
    
    # Presentation summary
    create_presentation_summary(loops_df, output_dir)
    
    print()
    print("="*70)
    print("✅ ALL VISUALIZATIONS COMPLETE!")
    print("="*70)
    print()
    print("📁 Generated files in h1_loop_analysis/:")
    print("  • h1_persistence_diagram_*.png - Birth/death diagrams")
    print("  • h1_lifetime_timeline.png - Temporal evolution")
    print("  • h1_persistence_distribution.png - Persistence histograms")
    print("  • h1_loops_presentation_summary.png - Summary panel")
    print()
    
    # Optionally visualize specific loops if full data available
    if full_data and len(full_data) > 0:
        print("💡 To visualize specific loops in formations:")
        print("   Run: python3 visualize_h1_loops.py --visualize-loops")
        print()
    
    print("="*70)


if __name__ == '__main__':
    main()

