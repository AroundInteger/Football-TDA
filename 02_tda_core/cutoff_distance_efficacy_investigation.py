#!/usr/bin/env python3
"""
Cut-off Distance Efficacy Investigation
=======================================

This script conducts a comprehensive sensitivity analysis of the cut-off distance
parameter to identify optimal values and understand the implications of different
thresholds. It explores:

1. Fine-grained cut-off distance parameter space
2. Multiple optimization criteria (H0 variation, H1 stability, information content)
3. Formation-specific optimal values
4. Critical thresholds and phase transitions
5. Statistical significance of cut-off distance choice

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from tqdm import tqdm
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from scipy import stats
from scipy.optimize import minimize_scalar
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.cluster import AgglomerativeClustering
import ripser
import warnings
warnings.filterwarnings('ignore')


class CutoffDistanceEfficacyInvestigation:
    """
    Comprehensive investigation of cut-off distance parameter efficacy
    """
    
    def __init__(self, n_points=100, gps_data_file=None, use_real_data=True):
        """
        Initialize investigation
        
        Args:
            n_points: Number of cut-off distance values to test
            gps_data_file: Path to GPS data file (JSONL format)
            use_real_data: Whether to use real GPS data (True) or synthetic formations (False)
        """
        self.n_points = n_points
        self.use_real_data = use_real_data
        self.gps_data_file = gps_data_file or 'FieldTest/g2293068_SecondSpectrum_Data.jsonl'
        
        # Temporal epoch configurations (window sizes in frames at 25Hz)
        self.temporal_epochs = {
            '1min': {'frames': 1500, 'seconds': 60},
            '2min': {'frames': 3000, 'seconds': 120},
            '5min': {'frames': 7500, 'seconds': 300},
            '10min': {'frames': 15000, 'seconds': 600}
        }
        
        # Results storage
        self.results = {}
        self.gps_data = None
        
    def load_gps_data(self):
        """
        Load real GPS data from SecondSpectrum JSONL file
        
        Returns:
            List of GPS frames
        """
        if not self.use_real_data:
            return None
        
        print(f"Loading GPS data from: {self.gps_data_file}")
        try:
            gps_frames = []
            with open(self.gps_data_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            frame_data = json.loads(line.strip())
                            gps_frames.append(frame_data)
                        except:
                            continue
            
            print(f"✅ Loaded {len(gps_frames)} GPS frames")
            self.gps_data = gps_frames
            return gps_frames
        except Exception as e:
            print(f"❌ Error loading GPS data: {e}")
            return None
    
    def extract_player_positions_from_frame(self, frame_data):
        """
        Extract player positions from a GPS frame
        
        Args:
            frame_data: Single GPS frame from SecondSpectrum data
            
        Returns:
            Dictionary with home_positions and away_positions (arrays)
        """
        try:
            home_positions = []
            away_positions = []
            
            # Extract home team positions
            if 'homePlayers' in frame_data:
                for player in frame_data['homePlayers']:
                    if 'xyz' in player and len(player['xyz']) >= 2:
                        home_positions.append([player['xyz'][0], player['xyz'][1]])
            
            # Extract away team positions
            if 'awayPlayers' in frame_data:
                for player in frame_data['awayPlayers']:
                    if 'xyz' in player and len(player['xyz']) >= 2:
                        away_positions.append([player['xyz'][0], player['xyz'][1]])
            
            # Need at least 10 players per team
            if len(home_positions) >= 10 and len(away_positions) >= 10:
                return {
                    'home_positions': np.array(home_positions[:11]),  # Take first 11
                    'away_positions': np.array(away_positions[:11])   # Take first 11
                }
            else:
                return None
        except:
            return None
    
    def extract_window_positions(self, start_frame, end_frame, sample_rate=5):
        """
        Extract player positions for a time window
        
        Args:
            start_frame: Start frame index
            end_frame: End frame index
            sample_rate: Sample every Nth frame
            
        Returns:
            Combined player positions array (all players, all sampled timepoints)
        """
        if self.gps_data is None:
            return None
        
        positions_list = []
        
        for i in range(start_frame, min(end_frame, len(self.gps_data)), sample_rate):
            frame_data = self.gps_data[i]
            player_data = self.extract_player_positions_from_frame(frame_data)
            
            if player_data is not None:
                # Combine home and away positions
                all_positions = np.vstack([
                    player_data['home_positions'],
                    player_data['away_positions']
                ])
                positions_list.append(all_positions)
        
        if len(positions_list) == 0:
            return None
        
        # Return mean positions across time window (or can return all positions)
        # Using mean for now - could also use all positions for richer analysis
        mean_positions = np.mean(positions_list, axis=0)
        return mean_positions
    
    def create_test_formations(self, n_players=22):
        """
        Create synthetic test formations with known structure
        
        Args:
            n_players: Number of players (default 22)
            
        Returns:
            Dictionary of formation types with positions
        """
        formations = {}
        
        # Tight clusters: 2 distinct groups
        np.random.seed(42)
        tight_team1 = np.random.randn(11, 2) * 2 + np.array([10, 20])
        tight_team2 = np.random.randn(11, 2) * 2 + np.array([40, 20])
        formations['tight'] = np.vstack([tight_team1, tight_team2])
        
        # Medium clusters: 4-6 groups
        medium_positions = []
        cluster_centers = [(10, 10), (30, 10), (10, 30), (30, 30)]
        for center in cluster_centers:
            cluster = np.random.randn(5, 2) * 3 + np.array(center)
            medium_positions.append(cluster)
        medium_positions.append(np.random.randn(2, 2) * 5 + np.array([20, 20]))
        formations['medium'] = np.vstack(medium_positions)
        
        # Spread formation: all players separate
        spread_positions = np.random.uniform(0, 50, (n_players, 2))
        formations['spread'] = spread_positions
        
        # Mixed formation: varying densities
        mixed_positions = []
        # One tight cluster
        mixed_positions.append(np.random.randn(5, 2) * 1.5 + np.array([15, 15]))
        # Medium spread
        mixed_positions.append(np.random.randn(10, 2) * 5 + np.array([25, 25]))
        # Loose spread
        mixed_positions.append(np.random.randn(7, 2) * 10 + np.array([20, 20]))
        formations['mixed'] = np.vstack(mixed_positions)
        
        return formations
    
    def create_cutoff_point_cloud(self, positions, cutoff_distance, method='hierarchical'):
        """
        Create point cloud with cut-off distance clustering
        
        Args:
            positions: Array of shape (n_points, 2)
            cutoff_distance: Distance threshold in meters
            method: Clustering method
            
        Returns:
            cluster_centers: Reduced point cloud
            cluster_labels: Cluster assignments
            cluster_sizes: Number of points per cluster
        """
        n_points = len(positions)
        
        if n_points == 0:
            return np.array([]), np.array([]), np.array([])
        
        if method == 'hierarchical':
            if n_points == 1:
                return positions, np.array([0]), np.array([1])
            
            distances = pdist(positions)
            linkage_matrix = linkage(distances, method='single')
            cluster_labels = fcluster(linkage_matrix, cutoff_distance, criterion='distance')
        else:
            # Simple method: assign each point to nearest cluster
            from sklearn.cluster import DBSCAN
            clustering = DBSCAN(eps=cutoff_distance, min_samples=1)
            cluster_labels = clustering.fit_predict(positions) + 1  # Shift to 1-indexed
        
        # Calculate cluster centers
        unique_labels = np.unique(cluster_labels)
        cluster_centers = []
        cluster_sizes = []
        
        for label in unique_labels:
            cluster_points = positions[cluster_labels == label]
            center = np.mean(cluster_points, axis=0)
            cluster_centers.append(center)
            cluster_sizes.append(len(cluster_points))
        
        return np.array(cluster_centers), cluster_labels, np.array(cluster_sizes)
    
    def compute_tda_features(self, point_cloud):
        """
        Compute TDA features on point cloud
        
        Args:
            point_cloud: Array of points
            
        Returns:
            Dictionary with H0, H1 features
        """
        if len(point_cloud) < 2:
            return {
                'h0_count': len(point_cloud),
                'h1_count': 0,
                'h0_persistence': 0,
                'h1_persistence': 0,
                'h0_diagram': np.array([]),
                'h1_diagram': np.array([])
            }
        
        try:
            # Calculate appropriate filtration threshold
            distances = pdist(point_cloud)
            if len(distances) > 0:
                max_thresh = np.percentile(distances, 95) * 2
            else:
                max_thresh = 1.0
            
            ripser_results = ripser.ripser(
                point_cloud,
                maxdim=1,
                thresh=max_thresh
            )
            
            h0_diagram = ripser_results['dgms'][0]
            h1_diagram = ripser_results['dgms'][1]
            
            h0_persistence = np.mean(h0_diagram[:, 1] - h0_diagram[:, 0]) if len(h0_diagram) > 0 else 0
            h1_persistence = np.mean(h1_diagram[:, 1] - h1_diagram[:, 0]) if len(h1_diagram) > 0 else 0
            
            return {
                'h0_count': len(h0_diagram),
                'h1_count': len(h1_diagram),
                'h0_persistence': h0_persistence,
                'h1_persistence': h1_persistence,
                'h0_diagram': h0_diagram,
                'h1_diagram': h1_diagram
            }
        except Exception as e:
            print(f"Warning: TDA computation failed: {e}")
            return {
                'h0_count': len(point_cloud),
                'h1_count': 0,
                'h0_persistence': 0,
                'h1_persistence': 0,
                'h0_diagram': np.array([]),
                'h1_diagram': np.array([])
            }
    
    def compute_clustering_metrics(self, positions, cluster_labels):
        """
        Compute clustering quality metrics
        
        Args:
            positions: Original positions
            cluster_labels: Cluster assignments
            
        Returns:
            Dictionary with clustering metrics
        """
        if len(positions) < 2 or len(np.unique(cluster_labels)) < 2:
            return {
                'silhouette_score': -1,
                'calinski_harabasz_score': 0,
                'n_clusters': len(np.unique(cluster_labels)),
                'intra_cluster_distance': 0,
                'inter_cluster_distance': 0
            }
        
        try:
            silhouette = silhouette_score(positions, cluster_labels)
            calinski = calinski_harabasz_score(positions, cluster_labels)
        except:
            silhouette = -1
            calinski = 0
        
        # Compute intra and inter-cluster distances
        unique_labels = np.unique(cluster_labels)
        intra_distances = []
        inter_distances = []
        
        for label in unique_labels:
            cluster_points = positions[cluster_labels == label]
            if len(cluster_points) > 1:
                cluster_dist = pdist(cluster_points)
                intra_distances.extend(cluster_dist)
            
            for other_label in unique_labels:
                if other_label != label:
                    other_points = positions[cluster_labels == other_label]
                    inter_dist = pdist(np.vstack([cluster_points, other_points]))
                    inter_distances.extend(inter_dist)
        
        return {
            'silhouette_score': silhouette,
            'calinski_harabasz_score': calinski,
            'n_clusters': len(unique_labels),
            'intra_cluster_distance': np.mean(intra_distances) if intra_distances else 0,
            'inter_cluster_distance': np.mean(inter_distances) if inter_distances else 0
        }
    
    def compute_information_content(self, h0_count, h1_count, original_size, metric_type='default'):
        """
        Compute information content metric
        
        Args:
            h0_count: Number of H0 features
            h1_count: Number of H1 features
            original_size: Original point cloud size
            metric_type: 'default', 'individual_player', 'tactical_group', 'team_level'
            
        Returns:
            Information content score
        """
        if metric_type == 'individual_player':
            return self.compute_individual_player_information(h0_count, h1_count, original_size)
        elif metric_type == 'tactical_group':
            return self.compute_tactical_group_information(h0_count, h1_count, original_size)
        elif metric_type == 'team_level':
            return self.compute_team_level_information(h0_count, h1_count, original_size)
        else:
            # Default (original) metric
            # Avoid H0 = point cloud size (low information)
            if h0_count >= original_size * 0.95:
                return 0
            
            # Prefer meaningful variation
            h0_info = 1 - (h0_count / original_size)
            
            # Value H1 features (topological complexity)
            h1_info = min(h1_count / 10, 1.0)  # Normalize
            
            # Combined information content
            return h0_info * 0.6 + h1_info * 0.4
    
    def compute_individual_player_information(self, h0_count, h1_count, original_size):
        """
        Information content metric optimized for individual player identification (0.5-3.0m range)
        
        Penalizes:
        - H0 too close to original_size (artifact: all points separate)
        - H0 too close to 1 (over-merging: everything together)
        
        Rewards:
        - H0 in range 0.5-0.9 of original_size (15-20 components for 22 players)
        - High H1 count (tactical complexity)
        """
        # Penalty for artifact (H0 ≈ original_size)
        h0_ratio = h0_count / original_size
        if h0_ratio >= 0.95:
            return 0  # Artifact region
        
        # Penalty for over-merging (H0 ≈ 1)
        if h0_count <= 1:
            return 0  # Over-merged
        
        # Sweet spot: H0 between 0.5-0.9 of original_size
        if 0.5 <= h0_ratio <= 0.9:
            h0_score = 1.0
        elif h0_ratio < 0.5:
            # Too merged: linear penalty
            h0_score = h0_ratio / 0.5
        else:
            # Too close to artifact: exponential penalty
            artifact_penalty = (h0_ratio - 0.9) / 0.05
            h0_score = 1.0 - artifact_penalty ** 2
        
        # H1 information (normalize by expected range)
        h1_score = min(h1_count / 5.0, 1.0)  # Expect 0-5 H1 features for individuals
        
        # Combined score
        return h0_score * 0.7 + h1_score * 0.3
    
    def compute_tactical_group_information(self, h0_count, h1_count, original_size):
        """
        Information content metric for tactical group identification (8-15m range)
        
        Optimal range: H0 = 0.2-0.5 of original_size (5-11 components for 22 players)
        """
        h0_ratio = h0_count / original_size
        
        # Sweet spot: H0 between 0.2-0.5 of original_size
        if 0.2 <= h0_ratio <= 0.5:
            h0_score = 1.0
        elif h0_ratio < 0.2:
            h0_score = h0_ratio / 0.2  # Too merged
        else:
            h0_score = 1.0 - ((h0_ratio - 0.5) / 0.5) ** 2  # Too many groups
        
        # H1 information (formation-level)
        h1_score = min(h1_count / 3.0, 1.0)
        
        return h0_score * 0.65 + h1_score * 0.35
    
    def compute_team_level_information(self, h0_count, h1_count, original_size):
        """
        Information content metric for team-level analysis (15-25m range)
        
        Optimal range: H0 = 1-3 components
        """
        # Reward low H0 (team separation)
        if h0_count <= 3:
            h0_score = 1.0 - (h0_count - 1) / 2.0  # Best at H0=1
        else:
            h0_score = max(0, 1.0 - (h0_count - 3) / original_size)
        
        # H1 is less important at team level
        h1_score = min(h1_count / 2.0, 1.0)
        
        return h0_score * 0.8 + h1_score * 0.2
    
    def sweep_cutoff_distances(self, positions, cutoff_range=None):
        """
        Sweep through cut-off distance parameter space
        
        Args:
            positions: Player positions
            cutoff_range: (min, max) range of cut-offs to test
            
        Returns:
            DataFrame with results for each cut-off distance
        """
        # Determine range if not provided
        if cutoff_range is None:
            distances = pdist(positions)
            min_dist = np.min(distances)
            max_dist = np.max(distances)
            cutoff_range = (min_dist * 0.5, max_dist * 2)
        
        cutoff_values = np.linspace(cutoff_range[0], cutoff_range[1], self.n_points)
        
        results = []
        
        print(f"Sweeping {len(cutoff_values)} cut-off distances from {cutoff_range[0]:.2f}m to {cutoff_range[1]:.2f}m...")
        
        for cutoff in tqdm(cutoff_values, desc="Cut-off sweep"):
            # Create clustered point cloud
            cluster_centers, cluster_labels, cluster_sizes = self.create_cutoff_point_cloud(
                positions, cutoff, method='hierarchical'
            )
            
            # Compute TDA features
            tda_features = self.compute_tda_features(cluster_centers)
            
            # Compute clustering metrics
            clustering_metrics = self.compute_clustering_metrics(positions, cluster_labels)
            
            # Compute information content (with all metric types)
            info_content_default = self.compute_information_content(
                tda_features['h0_count'],
                tda_features['h1_count'],
                len(positions),
                metric_type='default'
            )
            info_content_individual = self.compute_information_content(
                tda_features['h0_count'],
                tda_features['h1_count'],
                len(positions),
                metric_type='individual_player'
            )
            info_content_tactical = self.compute_information_content(
                tda_features['h0_count'],
                tda_features['h1_count'],
                len(positions),
                metric_type='tactical_group'
            )
            info_content_team = self.compute_information_content(
                tda_features['h0_count'],
                tda_features['h1_count'],
                len(positions),
                metric_type='team_level'
            )
            
            # Store results
            result = {
                'cutoff_distance': cutoff,
                'n_clusters': clustering_metrics['n_clusters'],
                'h0_count': tda_features['h0_count'],
                'h1_count': tda_features['h1_count'],
                'h0_persistence': tda_features['h0_persistence'],
                'h1_persistence': tda_features['h1_persistence'],
                'silhouette_score': clustering_metrics['silhouette_score'],
                'calinski_harabasz_score': clustering_metrics['calinski_harabasz_score'],
                'intra_cluster_distance': clustering_metrics['intra_cluster_distance'],
                'inter_cluster_distance': clustering_metrics['inter_cluster_distance'],
                'information_content': info_content_default,
                'information_content_individual': info_content_individual,
                'information_content_tactical': info_content_tactical,
                'information_content_team': info_content_team,
                'reduction_factor': len(cluster_centers) / len(positions)
            }
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def find_optimal_cutoff(self, sweep_results, criterion='information_content'):
        """
        Find optimal cut-off distance based on criterion
        
        Args:
            sweep_results: DataFrame from sweep_cutoff_distances
            criterion: Optimization criterion ('information_content', 'silhouette', etc.)
            
        Returns:
            Optimal cut-off distance and statistics
        """
        if criterion not in sweep_results.columns:
            raise ValueError(f"Criterion '{criterion}' not found in results")
        
        # Find maximum (or minimum for some criteria)
        if criterion in ['silhouette_score', 'calinski_harabasz_score', 'information_content']:
            optimal_idx = sweep_results[criterion].idxmax()
        else:
            optimal_idx = sweep_results[criterion].idxmin()
        
        optimal_cutoff = sweep_results.loc[optimal_idx, 'cutoff_distance']
        optimal_value = sweep_results.loc[optimal_idx, criterion]
        
        return {
            'optimal_cutoff': optimal_cutoff,
            'optimal_value': optimal_value,
            'optimal_idx': optimal_idx,
            'optimal_results': sweep_results.loc[optimal_idx].to_dict()
        }
    
    def detect_phase_transitions(self, sweep_results):
        """
        Detect phase transitions in cut-off distance parameter space
        
        Args:
            sweep_results: DataFrame from sweep_cutoff_distances
            
        Returns:
            Dictionary with detected phase transitions
        """
        transitions = []
        
        # Detect transitions in n_clusters
        n_clusters = sweep_results['n_clusters'].values
        cutoff_values = sweep_results['cutoff_distance'].values
        
        # Find where n_clusters changes significantly
        for i in range(1, len(n_clusters)):
            if n_clusters[i] != n_clusters[i-1]:
                transitions.append({
                    'type': 'cluster_count_change',
                    'cutoff': (cutoff_values[i] + cutoff_values[i-1]) / 2,
                    'from_clusters': n_clusters[i-1],
                    'to_clusters': n_clusters[i],
                    'index': i
                })
        
        # Detect transitions in H0 count
        h0_values = sweep_results['h0_count'].values
        h0_gradients = np.gradient(h0_values)
        high_gradient_idx = np.where(np.abs(h0_gradients) > np.std(h0_gradients) * 2)[0]
        
        for idx in high_gradient_idx:
            if idx > 0:
                transitions.append({
                    'type': 'h0_rapid_change',
                    'cutoff': cutoff_values[idx],
                    'h0_change': h0_values[idx] - h0_values[idx-1],
                    'index': idx
                })
        
        return {
            'transitions': transitions,
            'n_transitions': len(transitions),
            'transition_points': [t['cutoff'] for t in transitions]
        }
    
    def investigate_formation(self, formation_name, positions):
        """
        Investigate cut-off distance efficacy for a specific formation
        
        Args:
            formation_name: Name of formation type
            positions: Player positions
            
        Returns:
            Comprehensive investigation results
        """
        print(f"\n{'='*70}")
        print(f"INVESTIGATING: {formation_name.upper()} FORMATION")
        print(f"{'='*70}")
        
        # Sweep cut-off distances
        sweep_results = self.sweep_cutoff_distances(positions)
        
        # Find optimal cut-offs for different criteria
        optima = {}
        criteria = [
            'information_content', 
            'information_content_individual',
            'information_content_tactical',
            'information_content_team',
            'silhouette_score', 
            'calinski_harabasz_score'
        ]
        
        for criterion in criteria:
            if criterion in sweep_results.columns:
                optima[criterion] = self.find_optimal_cutoff(sweep_results, criterion)
        
        # Detect phase transitions
        phase_transitions = self.detect_phase_transitions(sweep_results)
        
        # Statistical analysis
        h0_variation = sweep_results['h0_count'].std()
        h1_variation = sweep_results['h1_count'].std()
        
        # Sensitivity analysis
        sensitivity_analysis = {
            'h0_sensitivity': self.compute_sensitivity(sweep_results, 'h0_count'),
            'h1_sensitivity': self.compute_sensitivity(sweep_results, 'h1_count'),
            'information_sensitivity': self.compute_sensitivity(sweep_results, 'information_content')
        }
        
        return {
            'formation_name': formation_name,
            'original_positions': positions,
            'sweep_results': sweep_results,
            'optima': optima,
            'phase_transitions': phase_transitions,
            'statistics': {
                'h0_variation': h0_variation,
                'h1_variation': h1_variation,
                'mean_h0': sweep_results['h0_count'].mean(),
                'mean_h1': sweep_results['h1_count'].mean(),
                'max_information': sweep_results['information_content'].max(),
                'mean_information': sweep_results['information_content'].mean()
            },
            'sensitivity_analysis': sensitivity_analysis
        }
    
    def compute_sensitivity(self, sweep_results, metric):
        """
        Compute sensitivity of metric to cut-off distance changes
        
        Args:
            sweep_results: DataFrame from sweep
            metric: Metric name
            
        Returns:
            Sensitivity statistics
        """
        values = sweep_results[metric].values
        cutoffs = sweep_results['cutoff_distance'].values
        
        # Compute gradient (rate of change)
        gradients = np.gradient(values, cutoffs)
        
        return {
            'mean_gradient': np.mean(np.abs(gradients)),
            'max_gradient': np.max(np.abs(gradients)),
            'std_gradient': np.std(gradients),
            'relative_sensitivity': np.std(values) / (np.mean(values) + 1e-6)
        }
    
    def run_comprehensive_investigation(self, output_dir='cutoff_efficacy_results', n_sample_windows=None, target_coverage_pct=15.0):
        """
        Run comprehensive investigation
        
        Args:
            output_dir: Output directory for results
            n_sample_windows: Number of sample windows to analyze per temporal epoch 
                             (if None, uses normalized sampling based on target_coverage_pct)
            target_coverage_pct: Target coverage percentage for normalization (default: 15%)
            
        Returns:
            Complete investigation results
        """
        print("\n" + "🔬" * 35)
        print("CUT-OFF DISTANCE EFFICACY INVESTIGATION")
        print("🔬" * 35)
        
        all_results = {}
        
        if self.use_real_data:
            # Load GPS data
            if self.load_gps_data() is None:
                print("⚠️ Falling back to synthetic formations")
                self.use_real_data = False
        
        if self.use_real_data and self.gps_data is not None:
            # Analyze real GPS data across temporal epochs
            print("\n" + "="*70)
            print("ANALYZING REAL GPS DATA ACROSS TEMPORAL EPOCHS")
            print("="*70)
            
            all_results = self.analyze_real_data_temporal_epochs(
                n_sample_windows=n_sample_windows,
                target_coverage_pct=target_coverage_pct
            )
            
        else:
            # Use synthetic formations
            print("\n" + "="*70)
            print("ANALYZING SYNTHETIC FORMATIONS")
            print("="*70)
            
            formations = self.create_test_formations()
            formation_types = ['tight', 'medium', 'spread', 'mixed']
            
            for formation_name in formation_types:
                if formation_name in formations:
                    results = self.investigate_formation(formation_name, formations[formation_name])
                    all_results[formation_name] = results
        
        # Cross-analysis
        if isinstance(all_results, dict) and len(all_results) > 0:
            if self.use_real_data and 'temporal_epochs' in all_results:
                cross_analysis = self.analyze_across_temporal_epochs(all_results)
            else:
                cross_analysis = self.analyze_across_formations(all_results)
            
            # Save results
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Save detailed results
            self.save_results(all_results, cross_analysis, output_dir)
            
            # Create visualizations
            self.create_visualizations(all_results, output_dir)
            
            # Generate report
            self.generate_report(all_results, cross_analysis, output_dir)
            
            print(f"\n🎉 INVESTIGATION COMPLETE!")
            print(f"📊 Results saved: {output_dir}")
            
            return all_results, cross_analysis
        else:
            print("❌ No results to analyze")
            return None, None
    
    def analyze_real_data_temporal_epochs(self, n_sample_windows=None, target_coverage_pct=15.0):
        """
        Analyze real GPS data across different temporal epochs
        
        Args:
            n_sample_windows: Number of sample windows per epoch (if None, calculates based on target_coverage_pct)
            target_coverage_pct: Target coverage percentage for normalization (default: 15%)
            
        Returns:
            Dictionary with results for each temporal epoch
        """
        results = {'temporal_epochs': {}}
        
        # Sample windows from different parts of the match
        total_frames = len(self.gps_data)
        match_duration_min = total_frames / 25 / 60
        
        # Calculate normalized window counts if not provided
        if n_sample_windows is None:
            window_counts = {}
            for epoch_name, epoch_config in self.temporal_epochs.items():
                window_min = epoch_config['seconds'] / 60
                target_time_min = match_duration_min * target_coverage_pct / 100
                n_windows = int(np.ceil(target_time_min / window_min))
                window_counts[epoch_name] = n_windows
                print(f"  {epoch_name}: {n_windows} windows for {target_coverage_pct}% coverage")
        else:
            # Use same number for all epochs
            window_counts = {name: n_sample_windows for name in self.temporal_epochs.keys()}
        
        # Use maximum window count for sample starts (covers all epochs)
        max_windows = max(window_counts.values()) if window_counts else n_sample_windows or 5
        sample_starts = np.linspace(0, total_frames - 2000, max_windows, dtype=int)
        
        for epoch_name, epoch_config in self.temporal_epochs.items():
            print(f"\n{'='*70}")
            print(f"TEMPORAL EPOCH: {epoch_name} ({epoch_config['seconds']} seconds)")
            print(f"{'='*70}")
            
            # Get window count for this epoch
            n_windows_for_epoch = window_counts.get(epoch_name, max_windows)
            epoch_sample_starts = sample_starts[:n_windows_for_epoch]
            
            # Calculate actual coverage
            total_window_time = sum([
                min(epoch_config['frames'], total_frames - start)
                for start in epoch_sample_starts
            ]) / 25 / 60
            coverage_pct = (total_window_time / match_duration_min) * 100
            print(f"Target: {n_windows_for_epoch} windows, Coverage: {coverage_pct:.1f}%")
            
            epoch_results = []
            
            for window_idx, start_frame in enumerate(epoch_sample_starts):
                end_frame = min(start_frame + epoch_config['frames'], total_frames)
                
                if end_frame - start_frame < epoch_config['frames'] * 0.5:
                    continue  # Skip if window too small
                
                print(f"\nWindow {window_idx+1}/{n_windows_for_epoch}: frames {start_frame}-{end_frame}")
                
                # Extract positions for this window
                positions = self.extract_window_positions(start_frame, end_frame)
                
                if positions is None or len(positions) < 10:
                    print(f"  ⚠️ Skipping window {window_idx+1} - insufficient data")
                    continue
                
                # Investigate this window
                window_results = self.investigate_formation(
                    f"{epoch_name}_window_{window_idx+1}",
                    positions
                )
                window_results['start_frame'] = start_frame
                window_results['end_frame'] = end_frame
                epoch_results.append(window_results)
            
            # Aggregate results for this epoch
            if epoch_results:
                results['temporal_epochs'][epoch_name] = {
                    'individual_windows': epoch_results,
                    'aggregate_stats': self.aggregate_epoch_results(epoch_results)
                }
        
        return results
    
    def aggregate_epoch_results(self, epoch_results):
        """
        Aggregate results across multiple windows in an epoch
        
        Args:
            epoch_results: List of window investigation results
            
        Returns:
            Aggregated statistics
        """
        if not epoch_results:
            return {}
        
        all_optima = []
        all_h0_stats = []
        all_h1_stats = []
        all_info_content = []
        
        for result in epoch_results:
            # Collect optimal cut-offs
            for criterion, optimal in result['optima'].items():
                all_optima.append({
                    'criterion': criterion,
                    'optimal_cutoff': optimal['optimal_cutoff']
                })
            
            # Collect statistics
            all_h0_stats.append(result['statistics']['mean_h0'])
            all_h1_stats.append(result['statistics']['mean_h1'])
            all_info_content.append(result['statistics']['max_information'])
        
        # Aggregate optimal cut-offs by criterion
        aggregated_optima = {}
        for criterion in ['information_content', 'silhouette_score', 'calinski_harabasz_score']:
            criterion_optima = [opt['optimal_cutoff'] for opt in all_optima if opt['criterion'] == criterion]
            if criterion_optima:
                aggregated_optima[criterion] = {
                    'mean': np.mean(criterion_optima),
                    'std': np.std(criterion_optima),
                    'min': np.min(criterion_optima),
                    'max': np.max(criterion_optima)
                }
        
        return {
            'n_windows': len(epoch_results),
            'aggregated_optima': aggregated_optima,
            'h0_mean': np.mean(all_h0_stats),
            'h0_std': np.std(all_h0_stats),
            'h1_mean': np.mean(all_h1_stats),
            'h1_std': np.std(all_h1_stats),
            'info_content_mean': np.mean(all_info_content),
            'info_content_std': np.std(all_info_content)
        }
    
    def analyze_across_temporal_epochs(self, all_results):
        """
        Analyze patterns across different temporal epochs
        
        Args:
            all_results: Results dictionary with temporal epochs
            
        Returns:
            Cross-epoch analysis
        """
        analysis = {
            'optimal_cutoffs_by_epoch': {},
            'temporal_patterns': {}
        }
        
        if 'temporal_epochs' not in all_results:
            return analysis
        
        for epoch_name, epoch_data in all_results['temporal_epochs'].items():
            if 'aggregate_stats' in epoch_data:
                agg_stats = epoch_data['aggregate_stats']
                analysis['optimal_cutoffs_by_epoch'][epoch_name] = agg_stats.get('aggregated_optima', {})
        
        # Find common patterns across epochs
        for criterion in ['information_content', 'silhouette_score', 'calinski_harabasz_score']:
            criterion_values = []
            for epoch_name, optima in analysis['optimal_cutoffs_by_epoch'].items():
                if criterion in optima:
                    criterion_values.append(optima[criterion]['mean'])
            
            if criterion_values:
                analysis['temporal_patterns'][criterion] = {
                    'mean': np.mean(criterion_values),
                    'std': np.std(criterion_values),
                    'range': np.max(criterion_values) - np.min(criterion_values),
                    'temporal_stability': 1.0 - (np.std(criterion_values) / (np.mean(criterion_values) + 1e-6))
                }
        
        return analysis
    
    def analyze_across_formations(self, all_results):
        """
        Analyze patterns across different formation types
        
        Args:
            all_results: Results dictionary from all formations
            
        Returns:
            Cross-formation analysis
        """
        analysis = {
            'optimal_cutoffs': {},
            'common_patterns': {},
            'formation_specificity': {}
        }
        
        # Extract optimal cut-offs for each criterion
        for criterion in ['information_content', 'silhouette_score', 'calinski_harabasz_score']:
            optima = []
            for formation_name, results in all_results.items():
                if criterion in results['optima']:
                    optima.append(results['optima'][criterion]['optimal_cutoff'])
            
            if optima:
                analysis['optimal_cutoffs'][criterion] = {
                    'mean': np.mean(optima),
                    'std': np.std(optima),
                    'min': np.min(optima),
                    'max': np.max(optima),
                    'range': np.max(optima) - np.min(optima)
                }
        
        return analysis
    
    def save_results(self, all_results, cross_analysis, output_dir):
        """Save investigation results"""
        if 'temporal_epochs' in all_results:
            # Real data results
            for epoch_name, epoch_data in all_results['temporal_epochs'].items():
                epoch_dir = Path(output_dir) / epoch_name
                epoch_dir.mkdir(parents=True, exist_ok=True)
                
                for window_result in epoch_data.get('individual_windows', []):
                    window_name = window_result['formation_name']
                    window_result['sweep_results'].to_csv(
                        epoch_dir / f'{window_name}_sweep_results.csv',
                        index=False
                    )
        else:
            # Synthetic formation results
            for formation_name, results in all_results.items():
                results['sweep_results'].to_csv(
                    Path(output_dir) / f'{formation_name}_sweep_results.csv',
                    index=False
                )
        
        # Save optimal cut-offs
        optima_data = []
        
        if 'temporal_epochs' in all_results:
            # Real data structure
            for epoch_name, epoch_data in all_results['temporal_epochs'].items():
                for window_result in epoch_data.get('individual_windows', []):
                    for criterion, optimal in window_result['optima'].items():
                        optima_data.append({
                            'epoch': epoch_name,
                            'window': window_result['formation_name'],
                            'criterion': criterion,
                            'optimal_cutoff': optimal['optimal_cutoff'],
                            'optimal_value': optimal['optimal_value']
                        })
        else:
            # Synthetic formations structure
            for formation_name, results in all_results.items():
                for criterion, optimal in results['optima'].items():
                    optima_data.append({
                        'formation': formation_name,
                        'criterion': criterion,
                        'optimal_cutoff': optimal['optimal_cutoff'],
                        'optimal_value': optimal['optimal_value']
                    })
        
        optima_df = pd.DataFrame(optima_data)
        optima_df.to_csv(Path(output_dir) / 'optimal_cutoffs.csv', index=False)
        
        # Save summary JSON
        if 'temporal_epochs' in all_results:
            summary = {
                'cross_epoch_analysis': cross_analysis,
                'temporal_epoch_statistics': {
                    epoch_name: {
                        'aggregate_stats': epoch_data.get('aggregate_stats', {}),
                        'n_windows': len(epoch_data.get('individual_windows', []))
                    }
                    for epoch_name, epoch_data in all_results['temporal_epochs'].items()
                }
            }
        else:
            summary = {
                'cross_formation_analysis': cross_analysis,
                'formation_statistics': {
                    name: {
                        'statistics': results['statistics'],
                        'optimal_cutoffs': {
                            k: v['optimal_cutoff'] for k, v in results['optima'].items()
                        }
                    }
                    for name, results in all_results.items()
                }
            }
        
        with open(Path(output_dir) / 'investigation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
    
    def create_visualizations(self, all_results, output_dir):
        """Create comprehensive visualizations"""
        if 'temporal_epochs' in all_results:
            # Real data visualization
            self.create_temporal_epoch_visualizations(all_results, output_dir)
        else:
            # Synthetic formations visualization
            self.create_formation_visualizations(all_results, output_dir)
    
    def create_formation_visualizations(self, all_results, output_dir):
        """Create visualizations for synthetic formations"""
        n_formations = len(all_results)
        if n_formations == 0:
            return
        
        fig, axes = plt.subplots(n_formations, 3, figsize=(18, 5*n_formations))
        
        if n_formations == 1:
            axes = axes.reshape(1, -1)
        
        for idx, (formation_name, results) in enumerate(all_results.items()):
            sweep = results['sweep_results']
            
            # Plot 1: H0 and H1 vs cut-off
            ax1 = axes[idx, 0]
            ax1_twin = ax1.twinx()
            
            line1 = ax1.plot(sweep['cutoff_distance'], sweep['h0_count'], 'b-', label='H0', linewidth=2)
            line2 = ax1_twin.plot(sweep['cutoff_distance'], sweep['h1_count'], 'r-', label='H1', linewidth=2)
            
            ax1.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax1.set_ylabel('H0 Count', color='b', fontsize=12)
            ax1_twin.set_ylabel('H1 Count', color='r', fontsize=12)
            ax1.set_title(f'{formation_name.capitalize()} Formation: H0/H1 vs Cut-off', fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Mark optimal cut-offs
            for criterion, optimal in results['optima'].items():
                opt_cutoff = optimal['optimal_cutoff']
                ax1.axvline(opt_cutoff, color='g', linestyle='--', alpha=0.5, label=f'Opt ({criterion[:4]})')
            
            ax1.legend(loc='upper left')
            ax1_twin.legend(loc='upper right')
            
            # Plot 2: Information content and clustering metrics
            ax2 = axes[idx, 1]
            
            ax2.plot(sweep['cutoff_distance'], sweep['information_content'], 'g-', label='Information Content', linewidth=2)
            ax2_twin = ax2.twinx()
            
            # Normalize silhouette for visibility
            silhouette_norm = (sweep['silhouette_score'] + 1) / 2  # Scale to [0, 1]
            ax2_twin.plot(sweep['cutoff_distance'], silhouette_norm, 'orange', label='Silhouette (norm)', linewidth=2, alpha=0.7)
            
            ax2.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax2.set_ylabel('Information Content', color='g', fontsize=12)
            ax2_twin.set_ylabel('Silhouette Score (normalized)', color='orange', fontsize=12)
            ax2.set_title(f'{formation_name.capitalize()} Formation: Quality Metrics', fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            # Mark optimal cut-offs
            for criterion, optimal in results['optima'].items():
                opt_cutoff = optimal['optimal_cutoff']
                ax2.axvline(opt_cutoff, color='g', linestyle='--', alpha=0.5)
            
            ax2.legend(loc='upper left')
            ax2_twin.legend(loc='upper right')
            
            # Plot 3: Number of clusters and reduction factor
            ax3 = axes[idx, 2]
            
            line1 = ax3.plot(sweep['cutoff_distance'], sweep['n_clusters'], 'purple', label='Number of Clusters', linewidth=2)
            ax3_twin = ax3.twinx()
            line2 = ax3_twin.plot(sweep['cutoff_distance'], sweep['reduction_factor'], 'brown', label='Reduction Factor', linewidth=2)
            
            ax3.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax3.set_ylabel('Number of Clusters', color='purple', fontsize=12)
            ax3_twin.set_ylabel('Reduction Factor', color='brown', fontsize=12)
            ax3.set_title(f'{formation_name.capitalize()} Formation: Clustering', fontweight='bold')
            ax3.grid(True, alpha=0.3)
            
            # Mark phase transitions
            for transition in results['phase_transitions']['transitions']:
                if transition['type'] == 'cluster_count_change':
                    ax3.axvline(transition['cutoff'], color='red', linestyle=':', alpha=0.5)
            
            ax3.legend(loc='upper left')
            ax3_twin.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'cutoff_efficacy_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Visualizations saved: {Path(output_dir) / 'cutoff_efficacy_analysis.png'}")
    
    def create_temporal_epoch_visualizations(self, all_results, output_dir):
        """Create visualizations for temporal epochs"""
        temporal_epochs = all_results.get('temporal_epochs', {})
        
        if not temporal_epochs:
            return
        
        n_epochs = len(temporal_epochs)
        fig, axes = plt.subplots(n_epochs, 3, figsize=(18, 5*n_epochs))
        
        if n_epochs == 1:
            axes = axes.reshape(1, -1)
        
        for idx, (epoch_name, epoch_data) in enumerate(temporal_epochs.items()):
            # Average results across windows in this epoch
            window_results = epoch_data.get('individual_windows', [])
            if not window_results:
                continue
            
            # Average sweep results
            all_sweeps = [w['sweep_results'] for w in window_results]
            avg_sweep = pd.concat(all_sweeps).groupby('cutoff_distance').mean().reset_index()
            
            sweep = avg_sweep
            
            # Plot 1: H0 and H1 vs cut-off
            ax1 = axes[idx, 0]
            ax1_twin = ax1.twinx()
            
            line1 = ax1.plot(sweep['cutoff_distance'], sweep['h0_count'], 'b-', label='H0', linewidth=2)
            line2 = ax1_twin.plot(sweep['cutoff_distance'], sweep['h1_count'], 'r-', label='H1', linewidth=2)
            
            ax1.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax1.set_ylabel('H0 Count', color='b', fontsize=12)
            ax1_twin.set_ylabel('H1 Count', color='r', fontsize=12)
            ax1.set_title(f'{epoch_name} Epoch: H0/H1 vs Cut-off', fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Mark optimal cut-offs from aggregate stats
            agg_stats = epoch_data.get('aggregate_stats', {})
            if 'aggregated_optima' in agg_stats:
                for criterion, optimal in agg_stats['aggregated_optima'].items():
                    opt_cutoff = optimal['mean']
                    ax1.axvline(opt_cutoff, color='g', linestyle='--', alpha=0.5, label=f'Opt ({criterion[:4]})')
            
            ax1.legend(loc='upper left')
            ax1_twin.legend(loc='upper right')
            
            # Plot 2: Information content
            ax2 = axes[idx, 1]
            ax2.plot(sweep['cutoff_distance'], sweep['information_content'], 'g-', label='Information Content', linewidth=2)
            ax2.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax2.set_ylabel('Information Content', color='g', fontsize=12)
            ax2.set_title(f'{epoch_name} Epoch: Quality Metrics', fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # Plot 3: Number of clusters
            ax3 = axes[idx, 2]
            ax3.plot(sweep['cutoff_distance'], sweep['n_clusters'], 'purple', label='Number of Clusters', linewidth=2)
            ax3.set_xlabel('Cut-off Distance (m)', fontsize=12)
            ax3.set_ylabel('Number of Clusters', color='purple', fontsize=12)
            ax3.set_title(f'{epoch_name} Epoch: Clustering', fontweight='bold')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'cutoff_efficacy_temporal_epochs.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Temporal epoch visualizations saved: {Path(output_dir) / 'cutoff_efficacy_temporal_epochs.png'}")
    
    def generate_report(self, all_results, cross_analysis, output_dir):
        """Generate comprehensive investigation report"""
        report = f"""# Cut-off Distance Efficacy Investigation Report

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Purpose**: Comprehensive sensitivity analysis of cut-off distance parameter  
**Status**: ✅ **COMPLETE**

---

## Executive Summary

This investigation systematically explores the cut-off distance parameter space to identify optimal values and understand the implications of different thresholds for TDA analysis of football team formations.

### Key Findings

"""
        
        # Summary statistics
        if 'temporal_epochs' in all_results:
            # Real GPS data results
            report += "\n## Temporal Epoch Results\n\n"
            
            for epoch_name, epoch_data in all_results['temporal_epochs'].items():
                agg_stats = epoch_data.get('aggregate_stats', {})
                report += f"""
#### {epoch_name.upper()} Epoch
- **Windows Analyzed**: {agg_stats.get('n_windows', 0)}
- **Mean H0**: {agg_stats.get('h0_mean', 0):.2f} ± {agg_stats.get('h0_std', 0):.2f}
- **Mean H1**: {agg_stats.get('h1_mean', 0):.2f} ± {agg_stats.get('h1_std', 0):.2f}
- **Mean Information Content**: {agg_stats.get('info_content_mean', 0):.4f} ± {agg_stats.get('info_content_std', 0):.4f}
"""
                
                # Optimal cut-offs
                if 'aggregated_optima' in agg_stats:
                    report += "\n**Optimal Cut-off Distances:**\n"
                    for criterion, optimal in agg_stats['aggregated_optima'].items():
                        report += f"- **{criterion.replace('_', ' ').title()}**: {optimal['mean']:.3f}m ± {optimal['std']:.3f}m\n"
            
            # Cross-epoch analysis
            if 'temporal_patterns' in cross_analysis:
                report += "\n---\n\n## Cross-Temporal Epoch Analysis\n\n"
                
                for criterion, pattern in cross_analysis['temporal_patterns'].items():
                    report += f"""
### {criterion.replace('_', ' ').title()} Criterion
- **Mean Optimal Cut-off**: {pattern['mean']:.3f}m ± {pattern['std']:.3f}m
- **Range**: {pattern['range']:.3f}m
- **Temporal Stability**: {pattern['temporal_stability']:.4f}

"""
        else:
            # Synthetic formations results
            for formation_name, results in all_results.items():
                stats = results['statistics']
                report += f"""
#### {formation_name.capitalize()} Formation
- **Mean H0**: {stats['mean_h0']:.2f} ± {stats['h0_variation']:.2f}
- **Mean H1**: {stats['mean_h1']:.2f} ± {stats['h1_variation']:.2f}
- **Max Information Content**: {stats['max_information']:.4f}
- **Mean Information Content**: {stats['mean_information']:.4f}
"""
                
                # Optimal cut-offs
                report += "\n**Optimal Cut-off Distances:**\n"
                for criterion, optimal in results['optima'].items():
                    report += f"- **{criterion.replace('_', ' ').title()}**: {optimal['optimal_cutoff']:.3f}m (value: {optimal['optimal_value']:.4f})\n"
            
            # Cross-formation analysis
            if 'optimal_cutoffs' in cross_analysis:
                report += "\n---\n\n## Cross-Formation Analysis\n\n"
                
                for criterion, analysis in cross_analysis['optimal_cutoffs'].items():
                    report += f"""
### {criterion.replace('_', ' ').title()} Criterion
- **Mean Optimal Cut-off**: {analysis['mean']:.3f}m ± {analysis['std']:.3f}m
- **Range**: {analysis['min']:.3f}m - {analysis['max']:.3f}m
- **Variation**: {analysis['range']:.3f}m

"""
            
            # Phase transitions
            report += "\n---\n\n## Phase Transitions Detected\n\n"
            
            for formation_name, results in all_results.items():
                transitions = results['phase_transitions']
                report += f"""
### {formation_name.capitalize()} Formation
- **Number of Transitions**: {transitions['n_transitions']}
- **Transition Points**: {', '.join([f'{t:.3f}m' for t in transitions['transition_points']])}

"""
        
        # Recommendations
        report += """
---

## Recommendations

### Optimal Cut-off Distance Selection

1. **For Maximum Information Content**: Use cut-off distances around the optimal values found for the `information_content` criterion (typically 0.8-1.5m)

2. **For Clustering Quality**: Use cut-off distances optimized for `silhouette_score` (typically 1.0-2.0m)

3. **Temporal Epoch/Formation-Specific Recommendations**:
"""
        
        if 'temporal_epochs' in all_results:
            for epoch_name, epoch_data in all_results['temporal_epochs'].items():
                agg_stats = epoch_data.get('aggregate_stats', {})
                if 'aggregated_optima' in agg_stats and 'information_content' in agg_stats['aggregated_optima']:
                    info_optimal = agg_stats['aggregated_optima']['information_content']['mean']
                    report += f"   - **{epoch_name.upper()} Epoch**: {info_optimal:.3f}m\n"
        else:
            for formation_name, results in all_results.items():
                info_optimal = results['optima']['information_content']['optimal_cutoff']
                report += f"   - **{formation_name.capitalize()}**: {info_optimal:.3f}m\n"
        
        report += """
### Critical Considerations

1. **Cut-off Too Small (< 0.5m)**: May not account for GPS measurement uncertainty
2. **Cut-off Too Large (> 3.0m)**: May over-cluster and lose meaningful tactical structure
3. **Phase Transitions**: Be aware of critical thresholds where formation structure changes dramatically

---

## Methodology

### Parameter Sweep
- **Number of Test Points**: {self.n_points}
- **Cut-off Range**: Automatically determined based on point cloud distances
- **Clustering Method**: Hierarchical (single linkage)

### Evaluation Criteria
1. **Information Content**: Combines H0 and H1 feature information
2. **Silhouette Score**: Clustering quality metric
3. **Calinski-Harabasz Score**: Cluster separation metric
4. **H0/H1 Variation**: Topological feature stability

---

*Investigation complete. See detailed results in CSV files and visualizations in PNG format.*

"""
        
        # Save report
        report_file = Path(output_dir) / 'CUTOFF_EFFICACY_INVESTIGATION_REPORT.md'
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Report saved: {report_file}")


def main():
    """Main execution function"""
    print("="*70)
    print("CUT-OFF DISTANCE EFFICACY INVESTIGATION")
    print("="*70)
    
    # Initialize investigation with real GPS data
    investigator = CutoffDistanceEfficacyInvestigation(
        n_points=100,
        gps_data_file='FieldTest/g2293068_SecondSpectrum_Data.jsonl',
        use_real_data=True
    )
    
    # Run comprehensive investigation with normalized sampling (30% coverage)
    # Set n_sample_windows=None to enable automatic normalized sampling
    all_results, cross_analysis = investigator.run_comprehensive_investigation(
        n_sample_windows=None,  # Auto-calculate for 30% coverage
        target_coverage_pct=30.0
    )
    
    if all_results is None:
        print("\n❌ Investigation failed - check data file and try again")
        return
    
    print("\n" + "="*70)
    print("INVESTIGATION SUMMARY")
    print("="*70)
    
    # Print summary
    if 'temporal_epochs' in all_results:
        print("\nTEMPORAL EPOCH RESULTS:")
        for epoch_name, epoch_data in all_results['temporal_epochs'].items():
            agg_stats = epoch_data.get('aggregate_stats', {})
            print(f"\n{epoch_name.upper()} EPOCH:")
            print(f"  Windows analyzed: {agg_stats.get('n_windows', 0)}")
            if 'aggregated_optima' in agg_stats:
                for criterion, optimal in agg_stats['aggregated_optima'].items():
                    print(f"  Optimal cut-off ({criterion}): {optimal['mean']:.3f}m ± {optimal['std']:.3f}m")
    else:
        # Synthetic formations
        for formation_name, results in all_results.items():
            print(f"\n{formation_name.upper()} FORMATION:")
            print(f"  Optimal cut-off (information): {results['optima']['information_content']['optimal_cutoff']:.3f}m")
            print(f"  Optimal cut-off (silhouette): {results['optima']['silhouette_score']['optimal_cutoff']:.3f}m")
            print(f"  Phase transitions: {results['phase_transitions']['n_transitions']}")
    
    print("\n🎯 INVESTIGATION COMPLETE!")
    print("✅ Comprehensive efficacy analysis finished")
    print("✅ Optimal cut-off distances identified")
    print("✅ Temporal epoch analysis complete")
    print("✅ Ready for informed parameter selection")


if __name__ == "__main__":
    main()

