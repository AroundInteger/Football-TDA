#!/usr/bin/env python3
"""
H1 Loop Analysis and Visualization
===================================

Identifies actual H1 loops in formations, tracks their persistence/lifetimes,
and creates visualizations for presentations.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from scipy.spatial.distance import pdist
from ripser import ripser
from scipy.cluster.hierarchy import linkage, fcluster
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings('ignore')


def compute_h1_with_persistence(player_positions, cutoff_distance, max_filtration=None):
    """
    Compute H1 with full persistence diagram information
    
    Returns:
        h0_count, h1_count, h1_diagram, point_cloud, filtration_used
    """
    if player_positions is None or len(player_positions) == 0:
        return 1, 0, np.array([]), player_positions, None
    
    if len(player_positions) == 1:
        return 1, 0, np.array([]), player_positions, None
    
    # Hierarchical clustering
    distances = pdist(player_positions)
    if len(distances) == 0:
        point_cloud = player_positions
    else:
        linkage_matrix = linkage(distances, method='single')
        cluster_labels = fcluster(linkage_matrix, cutoff_distance, criterion='distance')
        
        # Compute cluster centroids
        unique_labels = np.unique(cluster_labels)
        cluster_centers = []
        for label in unique_labels:
            cluster_points = player_positions[cluster_labels == label]
            center = np.mean(cluster_points, axis=0)
            cluster_centers.append(center)
        
        point_cloud = np.array(cluster_centers)
    
    # Adaptive filtration
    if max_filtration is None or max_filtration <= 0:
        point_distances = pdist(point_cloud)
        if len(point_distances) > 0:
            adaptive_filtration = np.percentile(point_distances, 75)
            min_filtration = max(5.0, cutoff_distance * 2.0)
            max_filtration = max(adaptive_filtration, min_filtration)
        else:
            max_filtration = max(5.0, cutoff_distance * 2.0)
    
    # Persistent homology with full diagrams
    if len(point_cloud) > 1:
        try:
            diagrams = ripser(point_cloud, maxdim=1, thresh=max_filtration)
            h0_diagram = diagrams['dgms'][0]
            h1_diagram = diagrams['dgms'][1]
            
            h0_count = len(h0_diagram)
            h1_count = len(h1_diagram)
            
            return h0_count, h1_count, h1_diagram, point_cloud, max_filtration
        except Exception as e:
            print(f"Error in ripser: {e}")
            return len(point_cloud), 0, np.array([]), point_cloud, max_filtration
    else:
        return 1, 0, np.array([]), point_cloud, max_filtration


def analyze_loops_comprehensive():
    """Analyze H1 loops across all frames with persistence tracking"""
    
    print("="*70)
    print("H1 LOOP ANALYSIS: PERSISTENCE AND LIFETIME TRACKING")
    print("="*70)
    print()
    
    # Load GPS data
    jsonl_file = Path('FieldTest/g2293068_SecondSpectrum_Data.jsonl')
    if not jsonl_file.exists():
        print(f"❌ Data file not found: {jsonl_file}")
        return None
    
    print("📂 Loading GPS data...")
    positions_list = []
    frame_indices = []
    timestamps = []
    
    try:
        with open(jsonl_file, 'r') as f:
            for i, line in enumerate(f):
                if i % 100 != 0:  # Sample every 100th frame
                    continue
                if len(positions_list) >= 150:  # Limit to 150 frames
                    break
                
                data = json.loads(line)
                
                # Extract player positions
                all_positions = []
                if 'homePlayers' in data:
                    for player in data['homePlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                if 'awayPlayers' in data:
                    for player in data['awayPlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                if len(all_positions) == 22:
                    positions_list.append(np.array(all_positions))
                    frame_indices.append(i)
                    timestamps.append(data.get('gameClock', i / 25.0))
        
        print(f"✅ Loaded {len(positions_list)} frames")
        print()
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None
    
    # Analyze loops with persistence
    print("🔬 Analyzing H1 loops with persistence information...")
    print()
    
    cutoffs = {
        'individual': 2.98,
        'tactical': 12.0,
        'team': 28.11
    }
    
    all_loop_data = []
    
    for frame_idx, (positions, frame_id, timestamp) in enumerate(zip(positions_list, frame_indices, timestamps)):
        for scale_name, cutoff in cutoffs.items():
            h0, h1, h1_diagram, point_cloud, filtration = compute_h1_with_persistence(
                positions, cutoff, max_filtration=None
            )
            
            # Extract loop information
            for loop_idx, (birth, death) in enumerate(h1_diagram):
                persistence = death - birth
                
                loop_info = {
                    'frame_idx': frame_idx,
                    'frame_id': frame_id,
                    'timestamp': timestamp,
                    'scale': scale_name,
                    'cutoff': cutoff,
                    'loop_idx': loop_idx,
                    'birth': birth,
                    'death': death,
                    'persistence': persistence,
                    'h0_count': h0,
                    'h1_count': h1,
                    'n_points': len(point_cloud),
                    'filtration': filtration,
                    'point_cloud': point_cloud.tolist()  # Store for visualization
                }
                
                all_loop_data.append(loop_info)
        
        if (frame_idx + 1) % 50 == 0:
            print(f"  Processed {frame_idx + 1}/{len(positions_list)} frames...")
    
    print()
    print(f"✅ Analyzed {len(positions_list)} frames")
    print(f"✅ Found {len(all_loop_data)} total loops across all scales")
    print()
    
    # Convert to DataFrame
    loops_df = pd.DataFrame(all_loop_data)
    
    # Save detailed results
    output_dir = Path('h1_loop_analysis')
    output_dir.mkdir(exist_ok=True)
    
    # Save full data (without point clouds for CSV)
    loops_df_export = loops_df.drop(columns=['point_cloud'])
    loops_df_export.to_csv(output_dir / 'h1_loops_detailed.csv', index=False)
    
    # Save with point clouds as JSON
    loops_data_dict = loops_df.to_dict('records')
    with open(output_dir / 'h1_loops_full_data.json', 'w') as f:
        json.dump(loops_data_dict, f, indent=2)
    
    print(f"📁 Results saved to: {output_dir}")
    print()
    
    # Summary statistics
    print("="*70)
    print("LOOP SUMMARY STATISTICS")
    print("="*70)
    print()
    
    for scale in ['individual', 'tactical', 'team']:
        scale_loops = loops_df[loops_df['scale'] == scale]
        
        if len(scale_loops) > 0:
            print(f"{scale.upper()} SCALE:")
            print(f"  Total loops detected: {len(scale_loops)}")
            print(f"  Frames with loops: {scale_loops['frame_idx'].nunique()}/{len(positions_list)}")
            print(f"  Mean persistence: {scale_loops['persistence'].mean():.3f}")
            print(f"  Max persistence: {scale_loops['persistence'].max():.3f}")
            print(f"  Mean birth: {scale_loops['birth'].mean():.3f}")
            print(f"  Mean death: {scale_loops['death'].mean():.3f}")
            print()
        else:
            print(f"{scale.upper()} SCALE: No loops detected")
            print()
    
    return loops_df, positions_list, frame_indices, timestamps


def track_loop_lifetimes(loops_df):
    """Track loop lifetimes across consecutive frames"""
    
    print("="*70)
    print("LOOP LIFETIME TRACKING")
    print("="*70)
    print()
    
    # Group by scale and track loops across frames
    lifetime_data = []
    
    for scale in ['individual', 'tactical', 'team']:
        scale_loops = loops_df[loops_df['scale'] == scale].copy()
        
        if len(scale_loops) == 0:
            continue
        
        # Sort by frame and persistence
        scale_loops = scale_loops.sort_values(['frame_idx', 'persistence'], ascending=[True, False])
        
        # Track loops across frames (simple heuristic: same number of loops and similar persistence)
        current_loops = []
        
        for frame_idx in scale_loops['frame_idx'].unique():
            frame_loops = scale_loops[scale_loops['frame_idx'] == frame_idx].copy()
            
            # Match loops between frames (simplified: assume order stability)
            if len(current_loops) > 0 and len(frame_loops) > 0:
                # Match based on persistence similarity
                for i, new_loop in frame_loops.iterrows():
                    best_match = None
                    best_diff = float('inf')
                    
                    for old_loop_idx, old_loop in enumerate(current_loops):
                        if old_loop['frame_idx'] == frame_idx - 1:  # Previous frame
                            pers_diff = abs(new_loop['persistence'] - old_loop['persistence'])
                            if pers_diff < best_diff and pers_diff < 2.0:  # Threshold
                                best_diff = pers_diff
                                best_match = old_loop_idx
                    
                    if best_match is not None:
                        # Update lifetime
                        lifetime_data.append({
                            'scale': scale,
                            'loop_id': current_loops[best_match].get('loop_id', len(lifetime_data)),
                            'start_frame': current_loops[best_match]['frame_idx'],
                            'end_frame': frame_idx,
                            'lifetime_frames': frame_idx - current_loops[best_match]['frame_idx'] + 1,
                            'mean_persistence': (new_loop['persistence'] + current_loops[best_match]['persistence']) / 2,
                            'frames': list(range(current_loops[best_match]['frame_idx'], frame_idx + 1))
                        })
            
            # Update current loops
            frame_loops_dict = frame_loops.to_dict('records')
            for loop in frame_loops_dict:
                loop['loop_id'] = len(current_loops)
                current_loops.append(loop)
            
            # Keep only recent frames (limit memory)
            current_loops = [l for l in current_loops if l['frame_idx'] >= frame_idx - 5]
    
    if lifetime_data:
        lifetimes_df = pd.DataFrame(lifetime_data)
        lifetimes_df.to_csv('h1_loop_analysis/loop_lifetimes.csv', index=False)
        print(f"✅ Tracked {len(lifetime_data)} loop lifetimes")
        print(f"   Mean lifetime: {lifetimes_df['lifetime_frames'].mean():.1f} frames")
        print(f"   Max lifetime: {lifetimes_df['lifetime_frames'].max():.0f} frames")
        print()
    
    return lifetime_data if lifetime_data else None


if __name__ == '__main__':
    try:
        loops_df, positions_list, frame_indices, timestamps = analyze_loops_comprehensive()
        
        if loops_df is not None and len(loops_df) > 0:
            lifetimes = track_loop_lifetimes(loops_df)
            print("✅ H1 loop analysis complete!")
            print("   Run visualize_h1_loops.py to create visualizations")
        else:
            print("⚠️  No loops detected - cannot proceed with visualization")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

