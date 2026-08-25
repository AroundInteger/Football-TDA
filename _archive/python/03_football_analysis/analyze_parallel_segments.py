#!/usr/bin/env python3
"""
Parallel Multi-Segment Real Data TDA Analysis
============================================

This script analyzes multiple time segments in parallel:
- First 5 minutes of each half
- Last 5 minutes of each half
- Parallel processing for efficiency

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


def analyze_single_segment(args):
    """
    Analyze a single segment - designed for parallel processing
    """
    data_file, segment_name, start_frame, end_frame, max_filtration = args
    
    print(f"[{segment_name}] Starting analysis...")
    
    try:
        # Load segment data
        frames = []
        frame_count = 0
        target_frames = end_frame - start_frame
        
        print(f"[{segment_name}] Loading {target_frames} frames...")
        
        with open(data_file, 'r') as f:
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
                        
                except json.JSONDecodeError:
                    continue
        
        print(f"[{segment_name}] Loaded {len(frames)} frames")
        
        # Extract data
        n_frames = len(frames)
        game_clock = np.zeros(n_frames)
        frame_idx = np.zeros(n_frames, dtype=int)
        period = np.zeros(n_frames, dtype=int)
        
        # Player positions
        home_positions = np.zeros((n_frames, 11, 2))
        away_positions = np.zeros((n_frames, 11, 2))
        ball_positions = np.zeros((n_frames, 2))
        
        print(f"[{segment_name}] Extracting player data...")
        
        for i, frame in enumerate(frames):
            game_clock[i] = frame.get('gameClock', 0.0)
            frame_idx[i] = frame.get('frameIdx', i)
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
        
        print(f"[{segment_name}] Calculating team metrics...")
        
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
        
        print(f"[{segment_name}] Preparing point cloud...")
        
        # Create point cloud
        point_cloud = np.column_stack([
            inter_team_distance,
            team_area_ratio,
            home_nod,
            away_nod,
            home_spread,
            away_spread
        ])
        
        # Remove NaN values
        valid_rows = ~np.isnan(point_cloud).any(axis=1)
        point_cloud = point_cloud[valid_rows]
        
        if len(point_cloud) < 3:
            raise ValueError(f"Not enough valid points for {segment_name}")
        
        print(f"[{segment_name}] Computing TDA...")
        
        # Compute persistent homology
        start_time = time.time()
        
        diagrams = ripser(
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
        
        print(f"[{segment_name}] TDA complete: {computation_time:.1f}s, Features: H0={h0_count}, H1={h1_count}, H2={h2_count}")
        
        # Prepare results
        results = {
            'segment_name': segment_name,
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
        
        print(f"[{segment_name}] Analysis complete!")
        return results
        
    except Exception as e:
        print(f"[{segment_name}] Analysis failed: {str(e)}")
        return {
            'segment_name': segment_name,
            'error': str(e),
            'success': False
        }


class ParallelMultiSegmentAnalyzer:
    """
    Parallel TDA analysis across multiple time segments
    """
    
    def __init__(self, data_file, max_filtration=2.0, max_workers=None):
        """
        Initialize the analyzer
        
        Args:
            data_file (str): Path to SecondSpectrum data file
            max_filtration (float): Maximum filtration value for TDA
            max_workers (int): Maximum number of parallel workers
        """
        self.data_file = data_file
        self.max_filtration = max_filtration
        self.max_workers = max_workers or min(4, mp.cpu_count())
        self.segments = {}
        self.comparative_results = {}
        
        print(f"ParallelMultiSegmentAnalyzer initialized")
        print(f"  Data file: {data_file}")
        print(f"  Max filtration: {max_filtration}")
        print(f"  Max workers: {self.max_workers}")
    
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
                'start_frame': 45 * 60 * 25 - frames_per_5min,
                'end_frame': 45 * 60 * 25,
                'description': 'Last 5 minutes of first half'
            },
            'Second_Half_Start': {
                'start_frame': 45 * 60 * 25,
                'end_frame': 45 * 60 * 25 + frames_per_5min,
                'description': 'First 5 minutes of second half'
            },
            'Second_Half_End': {
                'start_frame': 90 * 60 * 25 - frames_per_5min,
                'end_frame': 90 * 60 * 25,
                'description': 'Last 5 minutes of second half'
            }
        }
        
        print("Segments defined:")
        for name, info in self.segment_definitions.items():
            print(f"  {name}: {info['description']}")
            print(f"    Frames: {info['start_frame']} - {info['end_frame']}")
    
    def analyze_all_segments_parallel(self):
        """
        Analyze all segments in parallel
        """
        print(f"\n=== Analyzing All Segments in Parallel ===")
        print(f"Using {self.max_workers} parallel workers")
        
        self.define_segments()
        
        # Prepare arguments for parallel processing
        segment_args = []
        for segment_name, segment_info in self.segment_definitions.items():
            args = (
                self.data_file,
                segment_name,
                segment_info['start_frame'],
                segment_info['end_frame'],
                self.max_filtration
            )
            segment_args.append(args)
        
        # Run parallel analysis
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_segment = {
                executor.submit(analyze_single_segment, args): args[1] 
                for args in segment_args
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_segment):
                segment_name = future_to_segment[future]
                try:
                    result = future.result()
                    if 'error' not in result:
                        self.segments[segment_name] = result
                        print(f"✓ {segment_name} completed successfully")
                    else:
                        print(f"✗ {segment_name} failed: {result['error']}")
                except Exception as e:
                    print(f"✗ {segment_name} failed with exception: {str(e)}")
        
        total_time = time.time() - start_time
        
        print(f"\n✓ Parallel analysis complete!")
        print(f"  Total time: {total_time:.1f} seconds")
        print(f"  Segments completed: {len(self.segments)}")
        print(f"  Average time per segment: {total_time / len(self.segments):.1f} seconds")
    
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
            comparison_data.append({
                'segment': segment_name,
                'description': self.segment_definitions[segment_name]['description'],
                'n_frames': segment_info['n_frames'],
                'time_span': segment_info['time_span'],
                'h0_count': segment_info['h0_count'],
                'h1_count': segment_info['h1_count'],
                'h2_count': segment_info['h2_count'],
                'total_features': segment_info['total_features'],
                'computation_time': segment_info['computation_time'],
                'avg_inter_team_distance': segment_info['avg_inter_team_distance'],
                'avg_team_area_ratio': segment_info['avg_team_area_ratio'],
                'avg_home_nod': segment_info['avg_home_nod'],
                'avg_away_nod': segment_info['avg_away_nod'],
                'complexity_index': segment_info['complexity_index']
            })
        
        self.comparative_results = pd.DataFrame(comparison_data)
        
        print("Comparative analysis created:")
        print(self.comparative_results[['segment', 'total_features', 'complexity_index', 'computation_time']].to_string(index=False))
    
    def export_results(self, output_dir='parallel_segment_results'):
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
            team_metrics_df = pd.DataFrame(segment_info['team_metrics'])
            team_metrics_df.to_csv(f'{segment_dir}/team_metrics.csv', index=False)
            
            # Export TDA summary
            tda_summary = {
                'segment': segment_name,
                'description': self.segment_definitions[segment_name]['description'],
                'n_frames': segment_info['n_frames'],
                'time_span': segment_info['time_span'],
                'h0_count': segment_info['h0_count'],
                'h1_count': segment_info['h1_count'],
                'h2_count': segment_info['h2_count'],
                'total_features': segment_info['total_features'],
                'computation_time': segment_info['computation_time'],
                'point_cloud_shape': segment_info['point_cloud_shape']
            }
            
            with open(f'{segment_dir}/tda_summary.json', 'w') as f:
                json.dump(tda_summary, f, indent=2, default=str)
            
            # Export persistence diagrams
            for i, diagram in enumerate(segment_info['persistence_diagrams']):
                if len(diagram) > 0:
                    df = pd.DataFrame(diagram, columns=['birth', 'death'])
                    df.to_csv(f'{segment_dir}/persistence_diagram_H{i}.csv', index=False)
        
        # Create comprehensive report
        report = f"""Parallel Multi-Segment TDA Analysis Report
============================================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data File: {self.data_file}
Segments Analyzed: {len(self.segments)}
Max Workers: {self.max_workers}

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
• Parallel Efficiency: {self.comparative_results['computation_time'].sum() / (self.comparative_results['computation_time'].max() * len(self.segments)):.1f}x speedup
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
        Run the complete parallel multi-segment analysis
        """
        print("=== Parallel Multi-Segment Real Data TDA Analysis ===")
        print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Analyze all segments in parallel
            self.analyze_all_segments_parallel()
            
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
    Main function to run the parallel multi-segment analysis
    """
    # Configuration
    data_file = "FieldTest/g2293068_SecondSpectrum_Data copy.txt"
    max_filtration = 2.0
    max_workers = 4  # Use 4 workers for 4 segments
    
    print("Parallel Multi-Segment Real Data TDA Analysis")
    print("=============================================")
    print(f"Data file: {data_file}")
    print(f"Max filtration: {max_filtration}")
    print(f"Max workers: {max_workers}")
    print("Segments: First & Last 5 minutes of each half")
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return
    
    # Initialize analyzer
    analyzer = ParallelMultiSegmentAnalyzer(data_file, max_filtration, max_workers)
    
    # Run analysis
    results = analyzer.run_complete_analysis()
    
    if results['success']:
        print("\n🎉 Parallel multi-segment analysis completed successfully!")
        print(f"Analyzed {results['segments']} segments")
        print(f"Found {results['total_features']:,} total topological features")
    else:
        print(f"\n❌ Analysis failed: {results['error']}")


if __name__ == "__main__":
    main()
