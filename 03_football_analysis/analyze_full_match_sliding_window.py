#!/usr/bin/env python3
"""
Full Match Sliding Window TDA Analysis
=====================================

This script analyzes the complete SecondSpectrum match using sliding windows
to provide comprehensive coverage of formation evolution throughout the match.

Features:
- Sliding window analysis (5-minute windows, 1-minute steps)
- Parallel processing for efficiency
- Complete match coverage
- Temporal continuity analysis
- Formation transition detection

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import json
import sys
import os
from pathlib import Path
import warnings
import time
from datetime import datetime
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp
warnings.filterwarnings('ignore')

# Import TDA libraries
try:
    import ripser
    from ripser import ripser
    RIPSER_AVAILABLE = True
    print("✓ Ripser available")
except ImportError:
    RIPSER_AVAILABLE = False
    print("✗ Ripser not available")

try:
    from scipy.spatial import ConvexHull
    SCIPY_AVAILABLE = True
    print("✓ SciPy available")
except ImportError:
    SCIPY_AVAILABLE = False
    print("✗ SciPy not available")


def analyze_single_window(args):
    """
    Analyze a single sliding window - designed for parallel processing
    
    Args:
        args: Tuple of (data_file, window_id, start_frame, end_frame, max_filtration)
    
    Returns:
        dict: Analysis results for the window
    """
    data_file, window_id, start_frame, end_frame, max_filtration = args
    
    try:
        print(f"[Window {window_id:03d}] Starting analysis: frames {start_frame}-{end_frame}")
        
        # Load data for this window
        frames = []
        with open(data_file, 'r') as f:
            for i, line in enumerate(f):
                if i < start_frame:
                    continue
                if i >= end_frame:
                    break
                try:
                    frame = json.loads(line.strip())
                    frames.append(frame)
                except:
                    continue
        
        if len(frames) == 0:
            return {
                'window_id': window_id,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'error': 'No valid frames found'
            }
        
        n_frames = len(frames)
        print(f"[Window {window_id:03d}] Loaded {n_frames} frames")
        
        # Initialize data arrays
        home_positions = np.full((n_frames, 11, 2), np.nan)
        away_positions = np.full((n_frames, 11, 2), np.nan)
        ball_positions = np.full((n_frames, 2), np.nan)
        game_clock = np.zeros(n_frames)
        period = np.zeros(n_frames)
        
        # Extract data
        for i, frame in enumerate(frames):
            game_clock[i] = frame.get('gameClock', i * 0.04)
            period[i] = frame.get('period', 1)
            
            # Extract home team positions
            home_players = frame.get('homePlayers', [])
            for j, player in enumerate(home_players[:11]):
                xyz = player.get('xyz', [0, 0, 0])
                home_positions[i, j, 0] = xyz[0]
                home_positions[i, j, 1] = xyz[1]
            
            # Extract away team positions
            away_players = frame.get('awayPlayers', [])
            for j, player in enumerate(away_players[:11]):
                xyz = player.get('xyz', [0, 0, 0])
                away_positions[i, j, 0] = xyz[0]
                away_positions[i, j, 1] = xyz[1]
            
            # Extract ball position
            ball = frame.get('ball', {})
            ball_xyz = ball.get('xyz', [0, 0, 0])
            ball_positions[i, 0] = ball_xyz[0]
            ball_positions[i, 1] = ball_xyz[1]
        
        print(f"[Window {window_id:03d}] Calculating team metrics...")
        
        # Calculate team metrics
        home_centroids = np.mean(home_positions, axis=1)
        away_centroids = np.mean(away_positions, axis=1)
        inter_team_distance = np.linalg.norm(home_centroids - away_centroids, axis=1)
        
        home_spread = np.zeros(n_frames)
        away_spread = np.zeros(n_frames)
        
        for i in range(n_frames):
            home_distances = np.linalg.norm(home_positions[i] - home_centroids[i], axis=1)
            home_spread[i] = np.std(home_distances)
            
            away_distances = np.linalg.norm(away_positions[i] - away_centroids[i], axis=1)
            away_spread[i] = np.std(away_distances)
        
        home_areas = np.zeros(n_frames)
        away_areas = np.zeros(n_frames)
        
        for i in range(n_frames):
            try:
                home_hull = ConvexHull(home_positions[i])
                home_areas[i] = home_hull.volume
            except:
                home_areas[i] = np.nan
            
            try:
                away_hull = ConvexHull(away_positions[i])
                away_areas[i] = away_hull.volume
            except:
                away_areas[i] = np.nan
        
        team_area_ratio = home_areas / away_areas
        
        # Calculate Nearest Opponent Distance (NOD)
        home_nod = np.zeros(n_frames)
        away_nod = np.zeros(n_frames)
        
        for i in range(n_frames):
            # Home team NOD
            home_nod_values = []
            for j in range(11):
                if not np.isnan(home_positions[i, j, 0]):
                    distances = np.linalg.norm(home_positions[i, j] - away_positions[i], axis=1)
                    valid_distances = distances[~np.isnan(distances)]
                    if len(valid_distances) > 0:
                        home_nod_values.append(np.min(valid_distances))
            home_nod[i] = np.mean(home_nod_values) if home_nod_values else np.nan
            
            # Away team NOD
            away_nod_values = []
            for j in range(11):
                if not np.isnan(away_positions[i, j, 0]):
                    distances = np.linalg.norm(away_positions[i, j] - home_positions[i], axis=1)
                    valid_distances = distances[~np.isnan(distances)]
                    if len(valid_distances) > 0:
                        away_nod_values.append(np.min(valid_distances))
            away_nod[i] = np.mean(away_nod_values) if away_nod_values else np.nan
        
        print(f"[Window {window_id:03d}] Preparing point cloud...")
        
        # Create point cloud for TDA
        point_cloud = []
        for i in range(n_frames):
            # Team centroids
            point_cloud.append([home_centroids[i, 0], home_centroids[i, 1]])
            point_cloud.append([away_centroids[i, 0], away_centroids[i, 1]])
            
            # Team spreads
            point_cloud.append([home_spread[i], away_spread[i]])
            
            # Inter-team distance and area ratio
            point_cloud.append([inter_team_distance[i], team_area_ratio[i]])
            
            # NOD values
            point_cloud.append([home_nod[i], away_nod[i]])
        
        point_cloud = np.array(point_cloud)
        
        # Remove NaN values
        valid_mask = ~np.isnan(point_cloud).any(axis=1)
        point_cloud = point_cloud[valid_mask]
        
        if len(point_cloud) < 10:
            return {
                'window_id': window_id,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'error': 'Insufficient valid data for TDA'
            }
        
        print(f"[Window {window_id:03d}] Computing TDA...")
        
        # Compute persistent homology
        start_time = time.time()
        diagrams = ripser.ripser(
            point_cloud,
            maxdim=2,
            thresh=max_filtration,
            metric='euclidean'
        )
        
        computation_time = time.time() - start_time
        
        # Extract results
        persistence_diagrams = diagrams['dgms']
        h0_count = len(persistence_diagrams[0])
        h1_count = len(persistence_diagrams[1])
        h2_count = len(persistence_diagrams[2])
        
        print(f"[Window {window_id:03d}] TDA complete: {computation_time:.1f}s, Features: H0={h0_count}, H1={h1_count}, H2={h2_count}")
        
        # Prepare results
        results = {
            'window_id': window_id,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'n_frames': n_frames,
            'time_span': game_clock[-1] - game_clock[0] if len(game_clock) > 0 else 0,
            'point_cloud_shape': point_cloud.shape,
            'h0_count': h0_count,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'total_features': h0_count + h1_count + h2_count,
            'computation_time': computation_time,
            'avg_inter_team_distance': np.mean(inter_team_distance),
            'avg_team_area_ratio': np.nanmean(team_area_ratio),
            'avg_home_nod': np.mean(home_nod),
            'avg_away_nod': np.mean(away_nod),
            'complexity_index': (h0_count + h1_count + h2_count) / len(point_cloud),
            'persistence_diagrams': persistence_diagrams,
            'team_metrics': {
                'inter_team_distance': inter_team_distance,
                'team_area_ratio': team_area_ratio,
                'home_spread': home_spread,
                'away_spread': away_spread,
                'home_areas': home_areas,
                'away_areas': away_areas,
                'home_nod': home_nod,
                'away_nod': away_nod
            }
        }
        
        print(f"[Window {window_id:03d}] Analysis complete!")
        return results
        
    except Exception as e:
        print(f"[Window {window_id:03d}] Analysis failed: {str(e)}")
        return {
            'window_id': window_id,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'error': str(e)
        }


class FullMatchSlidingWindowAnalyzer:
    """
    Analyzes the complete SecondSpectrum match using sliding windows
    """
    
    def __init__(self, data_file, window_size=7500, step_size=1500, max_filtration=2.0, max_workers=None):
        """
        Initialize the sliding window analyzer
        
        Args:
            data_file (str): Path to the SecondSpectrum data file
            window_size (int): Size of each window in frames (default: 7500 = 5 minutes)
            step_size (int): Step size between windows in frames (default: 1500 = 1 minute)
            max_filtration (float): Maximum filtration value for TDA
            max_workers (int): Number of parallel workers (default: CPU count)
        """
        self.data_file = data_file
        self.window_size = window_size
        self.step_size = step_size
        self.max_filtration = max_filtration
        self.max_workers = max_workers or mp.cpu_count()
        
        self.windows = []
        self.results = {}
        self.comprehensive_results = {}
        
        print(f"FullMatchSlidingWindowAnalyzer initialized")
        print(f"  Data file: {data_file}")
        print(f"  Window size: {window_size} frames ({window_size/25/60:.1f} minutes)")
        print(f"  Step size: {step_size} frames ({step_size/25/60:.1f} minutes)")
        print(f"  Max filtration: {max_filtration}")
        print(f"  Max workers: {self.max_workers}")
    
    def create_sliding_windows(self, total_frames=150213):
        """
        Create sliding window definitions
        
        Args:
            total_frames (int): Total number of frames in the dataset
        """
        print(f"\n=== Creating Sliding Windows ===")
        print(f"Total frames: {total_frames}")
        print(f"Window size: {self.window_size} frames")
        print(f"Step size: {self.step_size} frames")
        
        self.windows = []
        window_id = 0
        
        for start_frame in range(0, total_frames - self.window_size + 1, self.step_size):
            end_frame = start_frame + self.window_size
            self.windows.append({
                'window_id': window_id,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'start_time': start_frame / 25 / 60,  # Convert to minutes
                'end_time': end_frame / 25 / 60
            })
            window_id += 1
        
        print(f"Created {len(self.windows)} sliding windows")
        print(f"Coverage: {self.windows[0]['start_time']:.1f} - {self.windows[-1]['end_time']:.1f} minutes")
        print(f"Overlap: {(self.window_size - self.step_size) / self.window_size * 100:.1f}%")
    
    def analyze_all_windows_parallel(self):
        """
        Analyze all windows in parallel
        """
        print(f"\n=== Analyzing All Windows in Parallel ===")
        print(f"Using {self.max_workers} parallel workers")
        
        if not self.windows:
            self.create_sliding_windows()
        
        # Prepare arguments for parallel processing
        window_args = []
        for window in self.windows:
            args = (
                self.data_file,
                window['window_id'],
                window['start_frame'],
                window['end_frame'],
                self.max_filtration
            )
            window_args.append(args)
        
        # Run parallel analysis
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_window = {
                executor.submit(analyze_single_window, args): args[1] 
                for args in window_args
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_window):
                window_id = future_to_window[future]
                try:
                    result = future.result()
                    if 'error' not in result:
                        self.results[window_id] = result
                        print(f"✓ Window {window_id:03d} completed successfully")
                    else:
                        print(f"✗ Window {window_id:03d} failed: {result['error']}")
                except Exception as e:
                    print(f"✗ Window {window_id:03d} failed with exception: {str(e)}")
        
        total_time = time.time() - start_time
        
        print(f"\n✓ Parallel analysis complete!")
        print(f"  Total time: {total_time:.1f} seconds")
        print(f"  Successful windows: {len(self.results)}")
        print(f"  Failed windows: {len(self.windows) - len(self.results)}")
    
    def create_comprehensive_analysis(self):
        """
        Create comprehensive analysis from all window results
        """
        print(f"\n=== Creating Comprehensive Analysis ===")
        
        if len(self.results) == 0:
            print("No results to analyze")
            return
        
        # Extract metrics for comprehensive analysis
        analysis_data = []
        
        for window_id, window_info in self.results.items():
            analysis_data.append({
                'window_id': window_id,
                'start_frame': window_info['start_frame'],
                'end_frame': window_info['end_frame'],
                'start_time': window_info['start_frame'] / 25 / 60,
                'end_time': window_info['end_frame'] / 25 / 60,
                'n_frames': window_info['n_frames'],
                'time_span': window_info['time_span'],
                'h0_count': window_info['h0_count'],
                'h1_count': window_info['h1_count'],
                'h2_count': window_info['h2_count'],
                'total_features': window_info['total_features'],
                'computation_time': window_info['computation_time'],
                'avg_inter_team_distance': window_info['avg_inter_team_distance'],
                'avg_team_area_ratio': window_info['avg_team_area_ratio'],
                'avg_home_nod': window_info['avg_home_nod'],
                'avg_away_nod': window_info['avg_away_nod'],
                'complexity_index': window_info['complexity_index']
            })
        
        self.comprehensive_results = pd.DataFrame(analysis_data)
        
        print("Comprehensive analysis created:")
        print(f"  Total windows analyzed: {len(self.comprehensive_results)}")
        print(f"  Time coverage: {self.comprehensive_results['start_time'].min():.1f} - {self.comprehensive_results['end_time'].max():.1f} minutes")
        print(f"  Average complexity: {self.comprehensive_results['complexity_index'].mean():.4f}")
        print(f"  Total features: {self.comprehensive_results['total_features'].sum()}")
    
    def export_results(self, output_dir='sliding_window_results'):
        """
        Export all results to files
        
        Args:
            output_dir (str): Output directory for results
        """
        print(f"\n=== Exporting Results ===")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export comprehensive results
        self.comprehensive_results.to_csv(f'{output_dir}/comprehensive_analysis.csv', index=False)
        
        # Export individual window results
        for window_id, window_info in self.results.items():
            window_dir = f'{output_dir}/window_{window_id:03d}'
            os.makedirs(window_dir, exist_ok=True)
            
            # Export window summary
            window_summary = {
                'window_id': window_id,
                'start_frame': window_info['start_frame'],
                'end_frame': window_info['end_frame'],
                'n_frames': window_info['n_frames'],
                'time_span': window_info['time_span'],
                'h0_count': window_info['h0_count'],
                'h1_count': window_info['h1_count'],
                'h2_count': window_info['h2_count'],
                'total_features': window_info['total_features'],
                'computation_time': window_info['computation_time'],
                'point_cloud_shape': window_info['point_cloud_shape']
            }
            
            with open(f'{window_dir}/window_summary.json', 'w') as f:
                json.dump(window_summary, f, indent=2, default=str)
            
            # Export persistence diagrams
            for i, diagram in enumerate(window_info['persistence_diagrams']):
                if len(diagram) > 0:
                    df = pd.DataFrame(diagram, columns=['birth', 'death'])
                    df.to_csv(f'{window_dir}/persistence_diagram_H{i}.csv', index=False)
        
        # Create comprehensive report
        report = {
            'analysis_summary': {
                'total_windows': len(self.results),
                'window_size_frames': self.window_size,
                'step_size_frames': self.step_size,
                'window_size_minutes': self.window_size / 25 / 60,
                'step_size_minutes': self.step_size / 25 / 60,
                'overlap_percentage': (self.window_size - self.step_size) / self.window_size * 100,
                'max_filtration': self.max_filtration,
                'total_processing_time': self.comprehensive_results['computation_time'].sum(),
                'average_processing_time': self.comprehensive_results['computation_time'].mean()
            },
            'tda_summary': {
                'total_h0_features': self.comprehensive_results['h0_count'].sum(),
                'total_h1_features': self.comprehensive_results['h1_count'].sum(),
                'total_h2_features': self.comprehensive_results['h2_count'].sum(),
                'total_features': self.comprehensive_results['total_features'].sum(),
                'average_complexity': self.comprehensive_results['complexity_index'].mean(),
                'max_complexity': self.comprehensive_results['complexity_index'].max(),
                'min_complexity': self.comprehensive_results['complexity_index'].min()
            },
            'team_metrics_summary': {
                'avg_inter_team_distance': self.comprehensive_results['avg_inter_team_distance'].mean(),
                'avg_team_area_ratio': self.comprehensive_results['avg_team_area_ratio'].mean(),
                'avg_home_nod': self.comprehensive_results['avg_home_nod'].mean(),
                'avg_away_nod': self.comprehensive_results['avg_away_nod'].mean()
            }
        }
        
        with open(f'{output_dir}/comprehensive_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Results exported to: {output_dir}")
        print(f"  Comprehensive analysis: {output_dir}/comprehensive_analysis.csv")
        print(f"  Individual windows: {output_dir}/window_XXX/")
        print(f"  Comprehensive report: {output_dir}/comprehensive_report.json")


def main():
    """
    Main function to run the full match sliding window analysis
    """
    print("Full Match Sliding Window TDA Analysis")
    print("=" * 50)
    
    # Configuration
    data_file = "FieldTest/g2293068_SecondSpectrum_Data copy.txt"
    window_size = 7500    # 5 minutes at 25Hz
    step_size = 1500      # 1 minute step
    max_filtration = 2.0
    max_workers = 8       # Adjust based on your system
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return
    
    # Initialize analyzer
    analyzer = FullMatchSlidingWindowAnalyzer(
        data_file=data_file,
        window_size=window_size,
        step_size=step_size,
        max_filtration=max_filtration,
        max_workers=max_workers
    )
    
    # Create sliding windows
    analyzer.create_sliding_windows()
    
    # Analyze all windows
    analyzer.analyze_all_windows_parallel()
    
    # Create comprehensive analysis
    analyzer.create_comprehensive_analysis()
    
    # Export results
    analyzer.export_results()
    
    print("\n=== Analysis Complete ===")
    print("Full match sliding window analysis completed successfully!")
    print("Check the 'sliding_window_results' directory for detailed results.")


if __name__ == "__main__":
    main()

