#!/usr/bin/env python3
"""
Multi-Segment Real Data TDA Analysis
====================================

This script analyzes multiple time segments of the real SecondSpectrum data:
- First 5 minutes of each half
- Last 5 minutes of each half
- Comparative analysis across segments

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


class MultiSegmentTDAAnalyzer:
    """
    TDA analysis across multiple time segments
    """
    
    def __init__(self, data_file, max_filtration=2.0):
        """
        Initialize the analyzer
        
        Args:
            data_file (str): Path to SecondSpectrum data file
            max_filtration (float): Maximum filtration value for TDA
        """
        self.data_file = data_file
        self.max_filtration = max_filtration
        self.segments = {}
        self.comparative_results = {}
        
        print(f"MultiSegmentTDAAnalyzer initialized")
        print(f"  Data file: {data_file}")
        print(f"  Max filtration: {max_filtration}")
    
    def define_segments(self):
        """
        Define the time segments to analyze
        """
        print("\n=== Defining Analysis Segments ===")
        
        # 5 minutes = 5 * 60 * 25 = 7,500 frames at 25Hz
        frames_per_5min = 5 * 60 * 25
        
        self.segment_definitions = {
            'First_Half_Start': {
                'start_frame': 0,
                'end_frame': frames_per_5min,
                'description': 'First 5 minutes of first half'
            },
            'First_Half_End': {
                'start_frame': 45 * 60 * 25 - frames_per_5min,  # Last 5 min of first half
                'end_frame': 45 * 60 * 25,
                'description': 'Last 5 minutes of first half'
            },
            'Second_Half_Start': {
                'start_frame': 45 * 60 * 25,  # Start of second half
                'end_frame': 45 * 60 * 25 + frames_per_5min,
                'description': 'First 5 minutes of second half'
            },
            'Second_Half_End': {
                'start_frame': 90 * 60 * 25 - frames_per_5min,  # Last 5 min of second half
                'end_frame': 90 * 60 * 25,
                'description': 'Last 5 minutes of second half'
            }
        }
        
        print("Segments defined:")
        for name, info in self.segment_definitions.items():
            print(f"  {name}: {info['description']}")
            print(f"    Frames: {info['start_frame']} - {info['end_frame']}")
    
    def load_segment_data(self, segment_name, start_frame, end_frame):
        """
        Load data for a specific segment
        """
        print(f"\nLoading segment: {segment_name}")
        print(f"  Frames: {start_frame} - {end_frame}")
        
        # Load data line by line
        frames = []
        frame_count = 0
        target_frames = end_frame - start_frame
        
        print(f"  Target: {target_frames} frames")
        print(f"  Progress: ", end="", flush=True)
        
        with open(self.data_file, 'r') as f:
            for line_num, line in enumerate(f):
                # Skip to start frame
                if line_num < start_frame:
                    continue
                
                # Stop at end frame
                if line_num >= end_frame:
                    break
                
                try:
                    frame = json.loads(line.strip())
                    frames.append(frame)
                    frame_count += 1
                    
                    # Progress indicator
                    if frame_count % 1000 == 0:
                        progress = (frame_count / target_frames) * 100
                        print(f"{progress:.0f}% ", end="", flush=True)
                        
                except json.JSONDecodeError:
                    continue
        
        print(f"\n  ✓ Loaded {len(frames)} frames")
        
        # Extract data for this segment
        segment_data = self.extract_segment_data(frames, segment_name)
        
        return segment_data
    
    def extract_segment_data(self, frames, segment_name):
        """
        Extract relevant data from frames for a segment
        """
        print(f"  Extracting data for {segment_name}...")
        
        n_frames = len(frames)
        
        # Initialize arrays
        game_clock = np.zeros(n_frames)
        frame_idx = np.zeros(n_frames, dtype=int)
        period = np.zeros(n_frames, dtype=int)
        
        # Player positions (11 players per team)
        home_positions = np.zeros((n_frames, 11, 2))  # x, y
        away_positions = np.zeros((n_frames, 11, 2))  # x, y
        ball_positions = np.zeros((n_frames, 2))  # x, y
        
        # Extract data from each frame
        for i, frame in enumerate(frames):
            game_clock[i] = frame.get('gameClock', 0.0)
            frame_idx[i] = frame.get('frameIdx', i)
            period[i] = frame.get('period', 1)
            
            # Extract home team positions
            home_players = frame.get('homePlayers', [])
            for j, player in enumerate(home_players[:11]):
                xyz = player.get('xyz', [0, 0, 0])
                home_positions[i, j, 0] = xyz[0]  # x
                home_positions[i, j, 1] = xyz[1]  # y
            
            # Extract away team positions
            away_players = frame.get('awayPlayers', [])
            for j, player in enumerate(away_players[:11]):
                xyz = player.get('xyz', [0, 0, 0])
                away_positions[i, j, 0] = xyz[0]  # x
                away_positions[i, j, 1] = xyz[1]  # y
            
            # Extract ball position
            ball = frame.get('ball', {})
            ball_xyz = ball.get('xyz', [0, 0, 0])
            ball_positions[i, 0] = ball_xyz[0]  # x
            ball_positions[i, 1] = ball_xyz[1]  # y
        
        # Calculate team metrics
        team_metrics = self.calculate_team_metrics(home_positions, away_positions, game_clock)
        
        segment_data = {
            'name': segment_name,
            'frames': frames,
            'n_frames': n_frames,
            'game_clock': game_clock,
            'frame_idx': frame_idx,
            'period': period,
            'home_positions': home_positions,
            'away_positions': away_positions,
            'ball_positions': ball_positions,
            'team_metrics': team_metrics
        }
        
        print(f"  ✓ Data extracted: {n_frames} frames, {game_clock[-1] - game_clock[0]:.1f}s")
        
        return segment_data
    
    def calculate_team_metrics(self, home_positions, away_positions, game_clock):
        """
        Calculate team-level metrics
        """
        n_frames = len(game_clock)
        
        # Team centroids
        home_centroids = np.mean(home_positions, axis=1)  # (n_frames, 2)
        away_centroids = np.mean(away_positions, axis=1)  # (n_frames, 2)
        
        # Inter-team distance
        inter_team_distance = np.linalg.norm(home_centroids - away_centroids, axis=1)
        
        # Team spreads
        home_spread = np.zeros(n_frames)
        away_spread = np.zeros(n_frames)
        
        for i in range(n_frames):
            # Home team spread
            home_distances = np.linalg.norm(home_positions[i] - home_centroids[i], axis=1)
            home_spread[i] = np.std(home_distances)
            
            # Away team spread
            away_distances = np.linalg.norm(away_positions[i] - away_centroids[i], axis=1)
            away_spread[i] = np.std(away_distances)
        
        # Team areas
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
        
        # Team area ratio
        team_area_ratio = home_areas / away_areas
        
        # NOD
        home_nod = np.zeros(n_frames)
        away_nod = np.zeros(n_frames)
        
        for i in range(n_frames):
            # Home team NOD
            home_nod_values = []
            for j in range(11):
                distances_to_away = np.linalg.norm(home_positions[i, j] - away_positions[i], axis=1)
                home_nod_values.append(np.min(distances_to_away))
            home_nod[i] = np.mean(home_nod_values)
            
            # Away team NOD
            away_nod_values = []
            for j in range(11):
                distances_to_home = np.linalg.norm(away_positions[i, j] - home_positions[i], axis=1)
                away_nod_values.append(np.min(distances_to_home))
            away_nod[i] = np.mean(away_nod_values)
        
        return {
            'inter_team_distance': inter_team_distance,
            'team_area_ratio': team_area_ratio,
            'home_spread': home_spread,
            'away_spread': away_spread,
            'home_areas': home_areas,
            'away_areas': away_areas,
            'home_nod': home_nod,
            'away_nod': away_nod
        }
    
    def prepare_point_cloud(self, segment_data):
        """
        Prepare point cloud data for TDA analysis
        """
        metrics = segment_data['team_metrics']
        
        # Create point cloud from team metrics
        point_cloud = np.column_stack([
            metrics['inter_team_distance'],
            metrics['team_area_ratio'],
            metrics['home_nod'],
            metrics['away_nod'],
            metrics['home_spread'],
            metrics['away_spread']
        ])
        
        # Remove NaN values
        valid_rows = ~np.isnan(point_cloud).any(axis=1)
        point_cloud = point_cloud[valid_rows]
        
        if len(point_cloud) < 3:
            raise ValueError(f"Not enough valid points for {segment_data['name']}")
        
        return point_cloud, valid_rows
    
    def compute_persistent_homology(self, point_cloud, segment_name):
        """
        Compute persistent homology for a segment
        """
        print(f"  Computing TDA for {segment_name}...")
        print(f"    Point cloud: {point_cloud.shape}")
        
        if not RIPSER_AVAILABLE:
            raise ImportError("Ripser not available")
        
        start_time = time.time()
        
        # Compute persistent homology
        diagrams = ripser(
            point_cloud,
            maxdim=2,  # Compute H0, H1, H2
            thresh=self.max_filtration,
            metric='euclidean'
        )
        
        computation_time = time.time() - start_time
        
        # Extract results
        persistence_diagrams = diagrams['dgms']
        
        # Count features
        h0_count = len(persistence_diagrams[0])
        h1_count = len(persistence_diagrams[1])
        h2_count = len(persistence_diagrams[2])
        
        print(f"    ✓ TDA complete: {computation_time:.1f}s")
        print(f"    ✓ Features: H0={h0_count}, H1={h1_count}, H2={h2_count}")
        
        return {
            'persistence_diagrams': persistence_diagrams,
            'h0_count': h0_count,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'total_features': h0_count + h1_count + h2_count,
            'computation_time': computation_time,
            'point_cloud_shape': point_cloud.shape
        }
    
    def analyze_all_segments(self):
        """
        Analyze all defined segments
        """
        print("\n=== Analyzing All Segments ===")
        
        self.define_segments()
        
        for segment_name, segment_info in self.segment_definitions.items():
            try:
                print(f"\n--- Analyzing {segment_name} ---")
                
                # Load segment data
                segment_data = self.load_segment_data(
                    segment_name,
                    segment_info['start_frame'],
                    segment_info['end_frame']
                )
                
                # Prepare point cloud
                point_cloud, valid_rows = self.prepare_point_cloud(segment_data)
                
                # Compute TDA
                tda_results = self.compute_persistent_homology(point_cloud, segment_name)
                
                # Store results
                self.segments[segment_name] = {
                    'data': segment_data,
                    'point_cloud': point_cloud,
                    'valid_rows': valid_rows,
                    'tda_results': tda_results,
                    'description': segment_info['description']
                }
                
                print(f"✓ {segment_name} analysis complete")
                
            except Exception as e:
                print(f"✗ {segment_name} analysis failed: {str(e)}")
                continue
        
        print(f"\n✓ Completed analysis of {len(self.segments)} segments")
    
    def create_comparative_analysis(self):
        """
        Create comparative analysis across segments
        """
        print("\n=== Creating Comparative Analysis ===")
        
        if len(self.segments) == 0:
            print("No segments to compare")
            return
        
        # Extract metrics for comparison
        comparison_data = []
        
        for segment_name, segment_info in self.segments.items():
            tda_results = segment_info['tda_results']
            team_metrics = segment_info['data']['team_metrics']
            
            comparison_data.append({
                'segment': segment_name,
                'description': segment_info['description'],
                'n_frames': segment_info['data']['n_frames'],
                'time_span': segment_info['data']['game_clock'][-1] - segment_info['data']['game_clock'][0],
                'h0_count': tda_results['h0_count'],
                'h1_count': tda_results['h1_count'],
                'h2_count': tda_results['h2_count'],
                'total_features': tda_results['total_features'],
                'computation_time': tda_results['computation_time'],
                'avg_inter_team_distance': np.mean(team_metrics['inter_team_distance']),
                'avg_team_area_ratio': np.nanmean(team_metrics['team_area_ratio']),
                'avg_home_nod': np.mean(team_metrics['home_nod']),
                'avg_away_nod': np.mean(team_metrics['away_nod']),
                'complexity_index': tda_results['total_features'] / tda_results['point_cloud_shape'][0]
            })
        
        self.comparative_results = pd.DataFrame(comparison_data)
        
        print("Comparative analysis created:")
        print(self.comparative_results[['segment', 'total_features', 'complexity_index', 'avg_inter_team_distance']].to_string(index=False))
    
    def export_results(self, output_dir='multi_segment_results'):
        """
        Export all results
        """
        print(f"\n=== Exporting Results to {output_dir} ===")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Export comparative results
        self.comparative_results.to_csv(f'{output_dir}/comparative_analysis.csv', index=False)
        
        # Export individual segment results
        for segment_name, segment_info in self.segments.items():
            segment_dir = f'{output_dir}/{segment_name}'
            os.makedirs(segment_dir, exist_ok=True)
            
            # Export team metrics
            team_metrics_df = pd.DataFrame(segment_info['data']['team_metrics'])
            team_metrics_df.to_csv(f'{segment_dir}/team_metrics.csv', index=False)
            
            # Export TDA results
            tda_results = segment_info['tda_results']
            tda_summary = {
                'segment': segment_name,
                'description': segment_info['description'],
                'n_frames': segment_info['data']['n_frames'],
                'time_span': segment_info['data']['game_clock'][-1] - segment_info['data']['game_clock'][0],
                'h0_count': tda_results['h0_count'],
                'h1_count': tda_results['h1_count'],
                'h2_count': tda_results['h2_count'],
                'total_features': tda_results['total_features'],
                'computation_time': tda_results['computation_time'],
                'point_cloud_shape': tda_results['point_cloud_shape']
            }
            
            with open(f'{segment_dir}/tda_summary.json', 'w') as f:
                json.dump(tda_summary, f, indent=2, default=str)
            
            # Export persistence diagrams
            for i, diagram in enumerate(tda_results['persistence_diagrams']):
                if len(diagram) > 0:
                    df = pd.DataFrame(diagram, columns=['birth', 'death'])
                    df.to_csv(f'{segment_dir}/persistence_diagram_H{i}.csv', index=False)
        
        # Create comprehensive report
        report = f"""Multi-Segment TDA Analysis Report
=====================================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data File: {self.data_file}
Segments Analyzed: {len(self.segments)}

SEGMENT COMPARISON:
{self.comparative_results.to_string(index=False)}

KEY INSIGHTS:
"""
        
        if len(self.segments) > 0:
            # Find most/least complex segments
            most_complex = self.comparative_results.loc[self.comparative_results['complexity_index'].idxmax()]
            least_complex = self.comparative_results.loc[self.comparative_results['complexity_index'].idxmin()]
            
            report += f"""
• Most Complex Segment: {most_complex['segment']} (Complexity: {most_complex['complexity_index']:.3f})
• Least Complex Segment: {least_complex['segment']} (Complexity: {least_complex['complexity_index']:.3f})
• Total Features Found: {self.comparative_results['total_features'].sum():,}
• Average Computation Time: {self.comparative_results['computation_time'].mean():.1f} seconds
"""
        
        report += "\nAnalysis Complete!"
        
        with open(f'{output_dir}/analysis_report.txt', 'w') as f:
            f.write(report)
        
        print(f"✓ Results exported to {output_dir}/")
        print(f"  - Comparative analysis: {len(self.segments)} segments")
        print(f"  - Individual segment results")
        print(f"  - Persistence diagrams")
        print(f"  - Analysis report")
    
    def run_complete_analysis(self):
        """
        Run the complete multi-segment analysis
        """
        print("=== Multi-Segment Real Data TDA Analysis ===")
        print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Analyze all segments
            self.analyze_all_segments()
            
            # Create comparative analysis
            self.create_comparative_analysis()
            
            # Export results
            self.export_results()
            
            print(f"\n=== Analysis Complete ===")
            print(f"Segments analyzed: {len(self.segments)}")
            print(f"Total features found: {self.comparative_results['total_features'].sum():,}")
            print(f"Average computation time: {self.comparative_results['computation_time'].mean():.1f} seconds")
            
            return {
                'success': True,
                'segments': len(self.segments),
                'total_features': self.comparative_results['total_features'].sum(),
                'comparative_results': self.comparative_results
            }
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """
    Main function to run the multi-segment analysis
    """
    # Configuration
    data_file = "FieldTest/g2293068_SecondSpectrum_Data copy.txt"
    max_filtration = 2.0
    
    print("Multi-Segment Real Data TDA Analysis")
    print("====================================")
    print(f"Data file: {data_file}")
    print(f"Max filtration: {max_filtration}")
    print("Segments: First & Last 5 minutes of each half")
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return
    
    # Initialize analyzer
    analyzer = MultiSegmentTDAAnalyzer(data_file, max_filtration)
    
    # Run analysis
    results = analyzer.run_complete_analysis()
    
    if results['success']:
        print("\n🎉 Multi-segment analysis completed successfully!")
        print(f"Analyzed {results['segments']} segments")
        print(f"Found {results['total_features']:,} total topological features")
    else:
        print(f"\n❌ Analysis failed: {results['error']}")


if __name__ == "__main__":
    main()
