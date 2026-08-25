#!/usr/bin/env python3
"""
Second Half Efficient Sliding Window TDA Analysis
===============================================

This script analyzes the second half of the SecondSpectrum match using the same
efficient approach as the first half analysis.

Features:
- Sliding window analysis (2-minute windows, 24-second steps)
- Second half focus (45-90 minutes)
- Sequential processing for stability
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


def analyze_single_window_efficient(data_file, window_id, start_frame, end_frame, max_filtration=1.5):
    """
    Analyze a single window with efficient memory usage
    
    Args:
        data_file (str): Path to data file
        window_id (int): Window identifier
        start_frame (int): Start frame
        end_frame (int): End frame
        max_filtration (float): Maximum filtration value
    
    Returns:
        dict: Analysis results
    """
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
        
        # Sample frames to reduce data size (every 5th frame)
        sample_rate = 5
        sampled_frames = frames[::sample_rate]
        n_sampled = len(sampled_frames)
        
        print(f"[Window {window_id:03d}] Sampled {n_sampled} frames (every {sample_rate}th frame)")
        
        # Initialize data arrays
        home_positions = np.full((n_sampled, 11, 2), np.nan)
        away_positions = np.full((n_sampled, 11, 2), np.nan)
        ball_positions = np.full((n_sampled, 2), np.nan)
        game_clock = np.zeros(n_sampled)
        
        # Extract data
        for i, frame in enumerate(sampled_frames):
            game_clock[i] = frame.get('gameClock', i * 0.04 * sample_rate)
            
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
        
        # Calculate team centroids
        home_centroids = np.mean(home_positions, axis=1)
        away_centroids = np.mean(away_positions, axis=1)
        inter_team_distance = np.linalg.norm(home_centroids - away_centroids, axis=1)
        
        # Calculate team spreads
        home_spread = np.zeros(n_sampled)
        away_spread = np.zeros(n_sampled)
        
        for i in range(n_sampled):
            home_distances = np.linalg.norm(home_positions[i] - home_centroids[i], axis=1)
            home_spread[i] = np.std(home_distances)
            
            away_distances = np.linalg.norm(away_positions[i] - away_centroids[i], axis=1)
            away_spread[i] = np.std(away_distances)
        
        # Calculate team areas
        home_areas = np.zeros(n_sampled)
        away_areas = np.zeros(n_sampled)
        
        for i in range(n_sampled):
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
        
        print(f"[Window {window_id:03d}] Creating efficient point cloud...")
        
        # Create a much smaller, more efficient point cloud
        point_cloud = []
        
        # Use only every 10th frame for point cloud to reduce size
        cloud_sample_rate = 10
        for i in range(0, n_sampled, cloud_sample_rate):
            if i < n_sampled:
                # Team centroids only
                point_cloud.append([home_centroids[i, 0], home_centroids[i, 1]])
                point_cloud.append([away_centroids[i, 0], away_centroids[i, 1]])
                
                # Team spreads
                point_cloud.append([home_spread[i], away_spread[i]])
                
                # Inter-team distance and area ratio
                point_cloud.append([inter_team_distance[i], team_area_ratio[i]])
        
        point_cloud = np.array(point_cloud)
        
        # Remove NaN values
        valid_mask = ~np.isnan(point_cloud).any(axis=1)
        point_cloud = point_cloud[valid_mask]
        
        print(f"[Window {window_id:03d}] Point cloud size: {point_cloud.shape}")
        
        if len(point_cloud) < 5:
            return {
                'window_id': window_id,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'error': 'Insufficient valid data for TDA'
            }
        
        print(f"[Window {window_id:03d}] Computing TDA...")
        
        # Compute persistent homology with reduced filtration
        start_time = time.time()
        diagrams = ripser(
            point_cloud,
            maxdim=1,  # Only compute H0 and H1 to reduce computation
            thresh=max_filtration,
            metric='euclidean'
        )
        
        computation_time = time.time() - start_time
        
        # Extract results
        persistence_diagrams = diagrams['dgms']
        h0_count = len(persistence_diagrams[0])
        h1_count = len(persistence_diagrams[1])
        
        print(f"[Window {window_id:03d}] TDA complete: {computation_time:.1f}s, Features: H0={h0_count}, H1={h1_count}")
        
        # Prepare results
        results = {
            'window_id': window_id,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'n_frames': n_frames,
            'n_sampled': n_sampled,
            'time_span': game_clock[-1] - game_clock[0] if len(game_clock) > 0 else 0,
            'point_cloud_shape': point_cloud.shape,
            'h0_count': h0_count,
            'h1_count': h1_count,
            'total_features': h0_count + h1_count,
            'computation_time': computation_time,
            'avg_inter_team_distance': np.mean(inter_team_distance),
            'avg_team_area_ratio': np.nanmean(team_area_ratio),
            'avg_home_spread': np.mean(home_spread),
            'avg_away_spread': np.mean(away_spread),
            'complexity_index': (h0_count + h1_count) / len(point_cloud),
            'persistence_diagrams': persistence_diagrams,
            'team_metrics': {
                'inter_team_distance': inter_team_distance,
                'team_area_ratio': team_area_ratio,
                'home_spread': home_spread,
                'away_spread': away_spread,
                'home_areas': home_areas,
                'away_areas': away_areas
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


class SecondHalfEfficientAnalyzer:
    """
    Efficiently analyzes the second half using smaller windows and reduced data
    """
    
    def __init__(self, data_file, window_size=3000, step_size=600, max_filtration=1.5):
        """
        Initialize the efficient analyzer
        
        Args:
            data_file (str): Path to the SecondSpectrum data file
            window_size (int): Size of each window in frames (default: 3000 = 2 minutes)
            step_size (int): Step size between windows in frames (default: 600 = 24 seconds)
            max_filtration (float): Maximum filtration value for TDA
        """
        self.data_file = data_file
        self.window_size = window_size
        self.step_size = step_size
        self.max_filtration = max_filtration
        
        self.windows = []
        self.results = {}
        self.comprehensive_results = {}
        
        print(f"SecondHalfEfficientAnalyzer initialized")
        print(f"  Data file: {data_file}")
        print(f"  Window size: {window_size} frames ({window_size/25/60:.1f} minutes)")
        print(f"  Step size: {step_size} frames ({step_size/25/60:.1f} minutes)")
        print(f"  Max filtration: {max_filtration}")
    
    def create_second_half_windows(self):
        """
        Create efficient window definitions for the second half (45-90 minutes)
        """
        print(f"\n=== Creating Second Half Efficient Windows ===")
        
        # Second half: 45 to 90 minutes (67,500 to 135,000 frames at 25Hz)
        second_half_start_frame = 45 * 60 * 25  # 67,500 frames
        second_half_end_frame = 90 * 60 * 25    # 135,000 frames
        
        print(f"Second half: {second_half_start_frame} - {second_half_end_frame} frames (45 - 90 minutes)")
        print(f"Window size: {self.window_size} frames")
        print(f"Step size: {self.step_size} frames")
        
        self.windows = []
        window_id = 0
        
        for start_frame in range(second_half_start_frame, second_half_end_frame - self.window_size + 1, self.step_size):
            end_frame = start_frame + self.window_size
            self.windows.append({
                'window_id': window_id,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'start_time': start_frame / 25 / 60,  # Convert to minutes
                'end_time': end_frame / 25 / 60
            })
            window_id += 1
        
        print(f"Created {len(self.windows)} efficient windows for second half")
        print(f"Coverage: {self.windows[0]['start_time']:.1f} - {self.windows[-1]['end_time']:.1f} minutes")
        print(f"Overlap: {(self.window_size - self.step_size) / self.window_size * 100:.1f}%")
    
    def analyze_all_windows_sequential(self):
        """
        Analyze all windows sequentially to avoid memory issues
        """
        print(f"\n=== Analyzing All Second Half Windows Sequentially ===")
        
        if not self.windows:
            self.create_second_half_windows()
        
        start_time = time.time()
        
        for window in self.windows:
            result = analyze_single_window_efficient(
                self.data_file,
                window['window_id'],
                window['start_frame'],
                window['end_frame'],
                self.max_filtration
            )
            
            if 'error' not in result:
                self.results[window['window_id']] = result
                print(f"✓ Window {window['window_id']:03d} completed successfully")
            else:
                print(f"✗ Window {window['window_id']:03d} failed: {result['error']}")
        
        total_time = time.time() - start_time
        
        print(f"\n✓ Second half sequential analysis complete!")
        print(f"  Total time: {total_time:.1f} seconds")
        print(f"  Successful windows: {len(self.results)}")
        print(f"  Failed windows: {len(self.windows) - len(self.results)}")
    
    def create_comprehensive_analysis(self):
        """
        Create comprehensive analysis from all window results
        """
        print(f"\n=== Creating Second Half Comprehensive Analysis ===")
        
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
                'n_sampled': window_info['n_sampled'],
                'time_span': window_info['time_span'],
                'h0_count': window_info['h0_count'],
                'h1_count': window_info['h1_count'],
                'total_features': window_info['total_features'],
                'computation_time': window_info['computation_time'],
                'avg_inter_team_distance': window_info['avg_inter_team_distance'],
                'avg_team_area_ratio': window_info['avg_team_area_ratio'],
                'avg_home_spread': window_info['avg_home_spread'],
                'avg_away_spread': window_info['avg_away_spread'],
                'complexity_index': window_info['complexity_index']
            })
        
        self.comprehensive_results = pd.DataFrame(analysis_data)
        
        print("Second half comprehensive analysis created:")
        print(f"  Total windows analyzed: {len(self.comprehensive_results)}")
        print(f"  Time coverage: {self.comprehensive_results['start_time'].min():.1f} - {self.comprehensive_results['end_time'].max():.1f} minutes")
        print(f"  Average complexity: {self.comprehensive_results['complexity_index'].mean():.4f}")
        print(f"  Total features: {self.comprehensive_results['total_features'].sum()}")
    
    def export_results(self, output_dir='second_half_efficient_results'):
        """
        Export all results to files
        """
        print(f"\n=== Exporting Second Half Results ===")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if we have results to export
        if len(self.results) == 0:
            print("No results to export")
            return
        
        # Export comprehensive results
        self.comprehensive_results.to_csv(f'{output_dir}/efficient_comprehensive_analysis.csv', index=False)
        
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
                'n_sampled': window_info['n_sampled'],
                'time_span': window_info['time_span'],
                'h0_count': window_info['h0_count'],
                'h1_count': window_info['h1_count'],
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
                'half': 'Second Half (Efficient)',
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
                'total_features': self.comprehensive_results['total_features'].sum(),
                'average_complexity': self.comprehensive_results['complexity_index'].mean(),
                'max_complexity': self.comprehensive_results['complexity_index'].max(),
                'min_complexity': self.comprehensive_results['complexity_index'].min()
            },
            'team_metrics_summary': {
                'avg_inter_team_distance': self.comprehensive_results['avg_inter_team_distance'].mean(),
                'avg_team_area_ratio': self.comprehensive_results['avg_team_area_ratio'].mean(),
                'avg_home_spread': self.comprehensive_results['avg_home_spread'].mean(),
                'avg_away_spread': self.comprehensive_results['avg_away_spread'].mean()
            }
        }
        
        with open(f'{output_dir}/efficient_comprehensive_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Second half results exported to: {output_dir}")
        print(f"  Comprehensive analysis: {output_dir}/efficient_comprehensive_analysis.csv")
        print(f"  Individual windows: {output_dir}/window_XXX/")
        print(f"  Comprehensive report: {output_dir}/efficient_comprehensive_report.json")


def main():
    """
    Main function to run the efficient second half analysis
    """
    print("Second Half Efficient Sliding Window TDA Analysis")
    print("=" * 50)
    
    # Configuration - same as first half for consistency
    data_file = "FieldTest/g2293068_SecondSpectrum_Data copy.txt"
    window_size = 3000    # 2 minutes at 25Hz
    step_size = 600       # 24 seconds step
    max_filtration = 1.5  # Same as first half
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return
    
    # Initialize analyzer
    analyzer = SecondHalfEfficientAnalyzer(
        data_file=data_file,
        window_size=window_size,
        step_size=step_size,
        max_filtration=max_filtration
    )
    
    # Create efficient windows for second half
    analyzer.create_second_half_windows()
    
    # Analyze all windows sequentially
    analyzer.analyze_all_windows_sequential()
    
    # Create comprehensive analysis
    analyzer.create_comprehensive_analysis()
    
    # Export results
    analyzer.export_results()
    
    print("\n=== Efficient Second Half Analysis Complete ===")
    print("Efficient second half analysis completed successfully!")
    print("Check the 'second_half_efficient_results' directory for detailed results.")


if __name__ == "__main__":
    main()
