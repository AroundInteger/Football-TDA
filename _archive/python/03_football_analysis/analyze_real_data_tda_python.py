#!/usr/bin/env python3
"""
Real SecondSpectrum Data TDA Analysis
=====================================

This script performs comprehensive TDA analysis on the real SecondSpectrum data
using Python and Ripser for efficient persistent homology computation.

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
    import gudhi
    GUDHI_AVAILABLE = True
    print("✓ Gudhi available")
except ImportError:
    GUDHI_AVAILABLE = False
    print("✗ Gudhi not available")

try:
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram
    from scipy.spatial import ConvexHull
    SCIPY_AVAILABLE = True
    print("✓ SciPy available")
except ImportError:
    SCIPY_AVAILABLE = False
    print("✗ SciPy not available")

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
    print("✓ Scikit-learn available")
except ImportError:
    SKLEARN_AVAILABLE = False
    print("✗ Scikit-learn not available")


class RealDataTDAAnalyzer:
    """
    Comprehensive TDA analysis of real SecondSpectrum data
    """
    
    def __init__(self, data_file, max_frames=10000, max_filtration=2.0):
        """
        Initialize the analyzer
        
        Args:
            data_file (str): Path to SecondSpectrum data file
            max_frames (int): Maximum number of frames to analyze
            max_filtration (float): Maximum filtration value for TDA
        """
        self.data_file = data_file
        self.max_frames = max_frames
        self.max_filtration = max_filtration
        self.results = {}
        self.computation_time = 0
        
        print(f"RealDataTDAAnalyzer initialized")
        print(f"  Data file: {data_file}")
        print(f"  Max frames: {max_frames}")
        print(f"  Max filtration: {max_filtration}")
    
    def load_real_data(self):
        """
        Load real SecondSpectrum data from JSONL file
        """
        print(f"\n=== Loading Real SecondSpectrum Data ===")
        print(f"File: {self.data_file}")
        
        # Check file size
        file_size_mb = os.path.getsize(self.data_file) / (1024 * 1024)
        print(f"File size: {file_size_mb:.1f} MB")
        
        # Load data line by line
        frames = []
        frame_count = 0
        
        print("Loading JSONL data...")
        print(f"  Target: {self.max_frames} frames")
        print(f"  Progress: ", end="", flush=True)
        
        with open(self.data_file, 'r') as f:
            for line in f:
                if frame_count >= self.max_frames:
                    break
                    
                try:
                    frame = json.loads(line.strip())
                    frames.append(frame)
                    frame_count += 1
                    
                    # Progress indicator
                    if frame_count % 500 == 0:
                        progress = (frame_count / self.max_frames) * 100
                        print(f"{progress:.0f}% ", end="", flush=True)
                        
                except json.JSONDecodeError:
                    continue
        
        print(f"\n  ✓ Successfully loaded {len(frames)} frames")
        
        print(f"Successfully loaded {len(frames)} frames")
        
        # Extract data
        self.extract_frame_data(frames)
        
        return frames
    
    def extract_frame_data(self, frames):
        """
        Extract relevant data from frames
        """
        print("\nExtracting frame data...")
        print(f"  Processing {len(frames)} frames...")
        
        n_frames = len(frames)
        
        # Initialize arrays
        self.game_clock = np.zeros(n_frames)
        self.frame_idx = np.zeros(n_frames, dtype=int)
        self.period = np.zeros(n_frames, dtype=int)
        
        # Player positions (11 players per team)
        self.home_positions = np.zeros((n_frames, 11, 2))  # x, y
        self.away_positions = np.zeros((n_frames, 11, 2))  # x, y
        self.ball_positions = np.zeros((n_frames, 2))  # x, y
        
        # Player speeds
        self.home_speeds = np.zeros((n_frames, 11))
        self.away_speeds = np.zeros((n_frames, 11))
        self.ball_speeds = np.zeros(n_frames)
        
        # Additional data
        self.live_status = np.zeros(n_frames, dtype=bool)
        self.last_touch = []
        
        # Extract data from each frame
        print("  Extracting player positions and ball data...")
        for i, frame in enumerate(frames):
            if i % 1000 == 0 and i > 0:
                print(f"    Processed {i}/{n_frames} frames...")
                
            self.game_clock[i] = frame.get('gameClock', 0.0)
            self.frame_idx[i] = frame.get('frameIdx', i)
            self.period[i] = frame.get('period', 1)
            
            # Extract home team positions
            home_players = frame.get('homePlayers', [])
            for j, player in enumerate(home_players[:11]):  # Limit to 11 players
                xyz = player.get('xyz', [0, 0, 0])
                self.home_positions[i, j, 0] = xyz[0]  # x
                self.home_positions[i, j, 1] = xyz[1]  # y
                self.home_speeds[i, j] = player.get('speed', 0.0)
            
            # Extract away team positions
            away_players = frame.get('awayPlayers', [])
            for j, player in enumerate(away_players[:11]):  # Limit to 11 players
                xyz = player.get('xyz', [0, 0, 0])
                self.away_positions[i, j, 0] = xyz[0]  # x
                self.away_positions[i, j, 1] = xyz[1]  # y
                self.away_speeds[i, j] = player.get('speed', 0.0)
            
            # Extract ball position
            ball = frame.get('ball', {})
            ball_xyz = ball.get('xyz', [0, 0, 0])
            self.ball_positions[i, 0] = ball_xyz[0]  # x
            self.ball_positions[i, 1] = ball_xyz[1]  # y
            self.ball_speeds[i] = ball.get('speed', 0.0)
            
            # Extract additional data
            self.live_status[i] = frame.get('live', False)
            self.last_touch.append(frame.get('lastTouch', 'unknown'))
        
        print("  ✓ Frame data extraction complete")
        
        # Calculate derived metrics
        print("  Calculating team metrics...")
        self.calculate_team_metrics()
        
        print(f"\n✓ Data extraction complete:")
        print(f"  Frames: {n_frames}")
        print(f"  Time span: {self.game_clock[-1] - self.game_clock[0]:.1f} seconds")
        print(f"  Sampling rate: {n_frames / (self.game_clock[-1] - self.game_clock[0]):.1f} Hz")
    
    def calculate_team_metrics(self):
        """
        Calculate team-level metrics
        """
        print("Calculating team metrics...")
        
        n_frames = len(self.game_clock)
        
        # Team centroids
        self.home_centroids = np.mean(self.home_positions, axis=1)  # (n_frames, 2)
        self.away_centroids = np.mean(self.away_positions, axis=1)  # (n_frames, 2)
        
        # Inter-team distance
        self.inter_team_distance = np.linalg.norm(
            self.home_centroids - self.away_centroids, axis=1
        )
        
        # Team spreads (standard deviation of player positions from centroid)
        self.home_spread = np.zeros(n_frames)
        self.away_spread = np.zeros(n_frames)
        
        for i in range(n_frames):
            # Home team spread
            home_distances = np.linalg.norm(
                self.home_positions[i] - self.home_centroids[i], axis=1
            )
            self.home_spread[i] = np.std(home_distances)
            
            # Away team spread
            away_distances = np.linalg.norm(
                self.away_positions[i] - self.away_centroids[i], axis=1
            )
            self.away_spread[i] = np.std(away_distances)
        
        # Team areas (convex hull areas)
        self.home_areas = np.zeros(n_frames)
        self.away_areas = np.zeros(n_frames)
        
        for i in range(n_frames):
            try:
                # Home team area
                home_hull = ConvexHull(self.home_positions[i])
                self.home_areas[i] = home_hull.volume  # 2D volume = area
            except:
                self.home_areas[i] = np.nan
            
            try:
                # Away team area
                away_hull = ConvexHull(self.away_positions[i])
                self.away_areas[i] = away_hull.volume  # 2D volume = area
            except:
                self.away_areas[i] = np.nan
        
        # Team area ratio
        self.team_area_ratio = self.home_areas / self.away_areas
        
        # Nearest Opponent Distance (NOD)
        self.home_nod = np.zeros(n_frames)
        self.away_nod = np.zeros(n_frames)
        
        for i in range(n_frames):
            # Home team NOD
            home_nod_values = []
            for j in range(11):
                distances_to_away = np.linalg.norm(
                    self.home_positions[i, j] - self.away_positions[i], axis=1
                )
                home_nod_values.append(np.min(distances_to_away))
            self.home_nod[i] = np.mean(home_nod_values)
            
            # Away team NOD
            away_nod_values = []
            for j in range(11):
                distances_to_home = np.linalg.norm(
                    self.away_positions[i, j] - self.home_positions[i], axis=1
                )
                away_nod_values.append(np.min(distances_to_home))
            self.away_nod[i] = np.mean(away_nod_values)
        
        print("  ✓ Team metrics calculated")
    
    def prepare_point_cloud_data(self):
        """
        Prepare point cloud data for TDA analysis
        """
        print("\nPreparing point cloud data for TDA...")
        
        # Create point cloud from team metrics
        # Each point represents a time frame with multiple features
        point_cloud = np.column_stack([
            self.inter_team_distance,
            self.team_area_ratio,
            self.home_nod,
            self.away_nod,
            self.home_spread,
            self.away_spread
        ])
        
        # Remove NaN values
        valid_rows = ~np.isnan(point_cloud).any(axis=1)
        point_cloud = point_cloud[valid_rows]
        
        print(f"  ✓ Point cloud prepared: {point_cloud.shape}")
        print(f"  ✓ Removed {np.sum(~valid_rows)} rows with NaN values")
        
        if len(point_cloud) < 3:
            raise ValueError("Not enough valid points for TDA analysis")
        
        self.point_cloud = point_cloud
        self.valid_indices = valid_rows
        
        return point_cloud
    
    def compute_persistent_homology(self):
        """
        Compute persistent homology using Ripser
        """
        print(f"\nComputing persistent homology...")
        print(f"Point cloud shape: {self.point_cloud.shape}")
        print(f"Max filtration: {self.max_filtration}")
        
        if not RIPSER_AVAILABLE:
            raise ImportError("Ripser not available")
        
        start_time = time.time()
        
        # Compute persistent homology
        diagrams = ripser(
            self.point_cloud,
            maxdim=2,  # Compute H0, H1, H2
            thresh=self.max_filtration,
            metric='euclidean'
        )
        
        self.computation_time = time.time() - start_time
        
        print(f"  ✓ Persistent homology computed in {self.computation_time:.2f} seconds")
        
        # Extract results
        self.persistence_diagrams = diagrams['dgms']
        # Note: 'birth_death_pairs' may not be available in all Ripser versions
        
        # Count features
        self.h0_count = len(self.persistence_diagrams[0])
        self.h1_count = len(self.persistence_diagrams[1])
        self.h2_count = len(self.persistence_diagrams[2])
        
        print(f"\n✓ Topological features found:")
        print(f"  H0 (connected components): {self.h0_count}")
        print(f"  H1 (loops): {self.h1_count}")
        print(f"  H2 (voids): {self.h2_count}")
        
        return diagrams
    
    def extract_topological_features(self):
        """
        Extract quantitative features from persistence diagrams
        """
        print("\nExtracting topological features...")
        
        features = {}
        
        # H0 features
        if len(self.persistence_diagrams[0]) > 0:
            h0_persistence = self.persistence_diagrams[0][:, 1] - self.persistence_diagrams[0][:, 0]
            features['h0_count'] = len(self.persistence_diagrams[0])
            features['h0_max_persistence'] = np.max(h0_persistence)
            features['h0_mean_persistence'] = np.mean(h0_persistence)
            features['h0_std_persistence'] = np.std(h0_persistence)
            features['h0_total_persistence'] = np.sum(h0_persistence)
        else:
            features['h0_count'] = 0
            features['h0_max_persistence'] = 0
            features['h0_mean_persistence'] = 0
            features['h0_std_persistence'] = 0
            features['h0_total_persistence'] = 0
        
        # H1 features
        if len(self.persistence_diagrams[1]) > 0:
            h1_persistence = self.persistence_diagrams[1][:, 1] - self.persistence_diagrams[1][:, 0]
            features['h1_count'] = len(self.persistence_diagrams[1])
            features['h1_max_persistence'] = np.max(h1_persistence)
            features['h1_mean_persistence'] = np.mean(h1_persistence)
            features['h1_std_persistence'] = np.std(h1_persistence)
            features['h1_total_persistence'] = np.sum(h1_persistence)
        else:
            features['h1_count'] = 0
            features['h1_max_persistence'] = 0
            features['h1_mean_persistence'] = 0
            features['h1_std_persistence'] = 0
            features['h1_total_persistence'] = 0
        
        # H2 features
        if len(self.persistence_diagrams[2]) > 0:
            h2_persistence = self.persistence_diagrams[2][:, 1] - self.persistence_diagrams[2][:, 0]
            features['h2_count'] = len(self.persistence_diagrams[2])
            features['h2_max_persistence'] = np.max(h2_persistence)
            features['h2_mean_persistence'] = np.mean(h2_persistence)
            features['h2_std_persistence'] = np.std(h2_persistence)
            features['h2_total_persistence'] = np.sum(h2_persistence)
        else:
            features['h2_count'] = 0
            features['h2_max_persistence'] = 0
            features['h2_mean_persistence'] = 0
            features['h2_std_persistence'] = 0
            features['h2_total_persistence'] = 0
        
        # Overall features
        features['total_features'] = features['h0_count'] + features['h1_count'] + features['h2_count']
        features['complexity_index'] = features['total_features'] / len(self.point_cloud)
        
        self.topological_features = features
        
        print("✓ Topological features extracted:")
        for key, value in features.items():
            print(f"  {key}: {value}")
        
        return features
    
    def analyze_tactical_effectiveness(self):
        """
        Analyze tactical effectiveness using topological features
        """
        print("\nAnalyzing tactical effectiveness...")
        
        # Create effectiveness metrics based on topological features
        effectiveness = {}
        
        # Complexity effectiveness (more features = more complex formations)
        effectiveness['complexity_effectiveness'] = min(1.0, self.topological_features['complexity_index'] * 10)
        
        # Persistence balance (balanced H0 and H1 features)
        if self.topological_features['h0_count'] > 0 and self.topological_features['h1_count'] > 0:
            h0_h1_ratio = self.topological_features['h0_count'] / self.topological_features['h1_count']
            effectiveness['persistence_balance'] = 1.0 / (1.0 + abs(h0_h1_ratio - 1.0))
        else:
            effectiveness['persistence_balance'] = 0.0
        
        # Overall effectiveness
        effectiveness['overall_effectiveness'] = (
            effectiveness['complexity_effectiveness'] + 
            effectiveness['persistence_balance']
        ) / 2.0
        
        self.tactical_effectiveness = effectiveness
        
        print("✓ Tactical effectiveness analyzed:")
        for key, value in effectiveness.items():
            print(f"  {key}: {value:.3f}")
        
        return effectiveness
    
    def export_results(self, output_dir='real_data_tda_results'):
        """
        Export results to files
        """
        print(f"\nExporting results to {output_dir}...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export persistence diagrams
        for i, diagram in enumerate(self.persistence_diagrams):
            if len(diagram) > 0:
                df = pd.DataFrame(diagram, columns=['birth', 'death'])
                df.to_csv(f'{output_dir}/persistence_diagram_H{i}.csv', index=False)
        
        # Export topological features
        features_df = pd.DataFrame([self.topological_features])
        features_df.to_csv(f'{output_dir}/topological_features.csv', index=False)
        
        # Export tactical effectiveness
        effectiveness_df = pd.DataFrame([self.tactical_effectiveness])
        effectiveness_df.to_csv(f'{output_dir}/tactical_effectiveness.csv', index=False)
        
        # Export team metrics
        team_metrics = pd.DataFrame({
            'frame_idx': self.frame_idx[self.valid_indices],
            'game_clock': self.game_clock[self.valid_indices],
            'inter_team_distance': self.inter_team_distance[self.valid_indices],
            'team_area_ratio': self.team_area_ratio[self.valid_indices],
            'home_nod': self.home_nod[self.valid_indices],
            'away_nod': self.away_nod[self.valid_indices],
            'home_spread': self.home_spread[self.valid_indices],
            'away_spread': self.away_spread[self.valid_indices]
        })
        team_metrics.to_csv(f'{output_dir}/team_metrics.csv', index=False)
        
        # Export comprehensive results
        comprehensive_results = {
            'data_info': {
                'data_file': self.data_file,
                'max_frames': self.max_frames,
                'actual_frames': len(self.game_clock),
                'time_span': self.game_clock[-1] - self.game_clock[0],
                'sampling_rate': len(self.game_clock) / (self.game_clock[-1] - self.game_clock[0]),
                'field_dimensions': {
                    'x_min': np.min([np.min(self.home_positions[:, :, 0]), np.min(self.away_positions[:, :, 0])]),
                    'x_max': np.max([np.max(self.home_positions[:, :, 0]), np.max(self.away_positions[:, :, 0])]),
                    'y_min': np.min([np.min(self.home_positions[:, :, 1]), np.min(self.away_positions[:, :, 1])]),
                    'y_max': np.max([np.max(self.home_positions[:, :, 1]), np.max(self.away_positions[:, :, 1])])
                }
            },
            'tda_parameters': {
                'max_filtration': self.max_filtration,
                'computation_time': self.computation_time,
                'point_cloud_shape': self.point_cloud.shape
            },
            'topological_features': self.topological_features,
            'tactical_effectiveness': self.tactical_effectiveness
        }
        
        with open(f'{output_dir}/comprehensive_results.json', 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
        
        # Create analysis report
        report = f"""Real SecondSpectrum Data TDA Analysis Report
================================================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data File: {self.data_file}
Max Frames: {self.max_frames}
Actual Frames: {len(self.game_clock)}
Time Span: {self.game_clock[-1] - self.game_clock[0]:.1f} seconds ({self.game_clock[-1] - self.game_clock[0]/60:.1f} minutes)
Sampling Rate: {len(self.game_clock) / (self.game_clock[-1] - self.game_clock[0]):.1f} Hz

TDA Analysis:
Max Filtration: {self.max_filtration}
Computation Time: {self.computation_time:.2f} seconds
Point Cloud Shape: {self.point_cloud.shape}

Topological Features:
H0 Features (Connected Components): {self.topological_features['h0_count']}
H1 Features (Loops): {self.topological_features['h1_count']}
H2 Features (Voids): {self.topological_features['h2_count']}
Total Features: {self.topological_features['total_features']}
Complexity Index: {self.topological_features['complexity_index']:.6f}

Tactical Effectiveness:
Complexity Effectiveness: {self.tactical_effectiveness['complexity_effectiveness']:.3f}
Persistence Balance: {self.tactical_effectiveness['persistence_balance']:.3f}
Overall Effectiveness: {self.tactical_effectiveness['overall_effectiveness']:.3f}

Analysis Complete!
"""
        
        with open(f'{output_dir}/analysis_report.txt', 'w') as f:
            f.write(report)
        
        print(f"\n✓ Results exported to {output_dir}/")
        print(f"  - Persistence diagrams: H0, H1, H2")
        print(f"  - Topological features: {self.topological_features['total_features']} features")
        print(f"  - Tactical effectiveness: {self.tactical_effectiveness['overall_effectiveness']:.3f}")
        print(f"  - Team metrics: {len(team_metrics)} time points")
        print(f"  - Comprehensive results: JSON format")
        print(f"  - Analysis report: Text format")
    
    def run_complete_analysis(self):
        """
        Run the complete TDA analysis pipeline
        """
        print("=== Real SecondSpectrum Data TDA Analysis ===")
        print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Load data
            frames = self.load_real_data()
            
            # Prepare point cloud
            point_cloud = self.prepare_point_cloud_data()
            
            # Compute persistent homology
            diagrams = self.compute_persistent_homology()
            
            # Extract features
            features = self.extract_topological_features()
            
            # Analyze effectiveness
            effectiveness = self.analyze_tactical_effectiveness()
            
            # Export results
            self.export_results()
            
            print(f"\n=== Analysis Complete ===")
            print(f"Total computation time: {self.computation_time:.2f} seconds")
            print(f"Topological features found: {features['total_features']}")
            print(f"Overall effectiveness: {effectiveness['overall_effectiveness']:.3f}")
            
            return {
                'success': True,
                'features': features,
                'effectiveness': effectiveness,
                'computation_time': self.computation_time
            }
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """
    Main function to run the analysis
    """
    # Configuration - Start with a small sample
    data_file = "FieldTest/g2293068_SecondSpectrum_Data copy.txt"
    max_frames = 3000  # Analyze first 3,000 frames (2 minutes at 25Hz)
    max_filtration = 2.0  # Maximum filtration value
    
    print("Real SecondSpectrum Data TDA Analysis")
    print("=====================================")
    print(f"Data file: {data_file}")
    print(f"Max frames: {max_frames}")
    print(f"Max filtration: {max_filtration}")
    
    # Check if data file exists
    if not os.path.exists(data_file):
        print(f"Error: Data file not found: {data_file}")
        return
    
    # Initialize analyzer
    analyzer = RealDataTDAAnalyzer(data_file, max_frames, max_filtration)
    
    # Run analysis
    results = analyzer.run_complete_analysis()
    
    if results['success']:
        print("\n🎉 Analysis completed successfully!")
        print(f"Found {results['features']['total_features']} topological features")
        print(f"Overall effectiveness: {results['effectiveness']['overall_effectiveness']:.3f}")
    else:
        print(f"\n❌ Analysis failed: {results['error']}")


if __name__ == "__main__":
    main()
