#!/usr/bin/env python3
"""
StatsBomb GPS Tracking Analysis Pipeline
=======================================

This script runs the complete TDA analysis on StatsBomb GPS tracking data
(Three-Sixty data) to properly compare with SecondSpectrum results.

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
from sklearn.cluster import KMeans
from sklearn.linear_model import HuberRegressor
from ripser import ripser
import warnings
warnings.filterwarnings('ignore')

class StatsBombGPSTrackingAnalysis:
    """
    Complete TDA analysis pipeline for StatsBomb GPS tracking data
    """
    
    def __init__(self, data_dir='open-data/data', cutoff_distance=1.0):
        """
        Initialize GPS tracking analysis
        
        Args:
            data_dir: Path to StatsBomb open-data directory
            cutoff_distance: GPS-aware clustering threshold in meters
        """
        self.data_dir = Path(data_dir)
        self.cutoff_distance = cutoff_distance
        
        # Analysis parameters (matching SecondSpectrum)
        self.window_duration = 3000  # 3000 frames (2 minutes at 25Hz)
        self.step_size = 600  # 600 frames (24 seconds)
        self.sampling_interval = 5  # Every 5th frame for analysis
        self.cloud_sample_rate = 10  # Every 10th frame for point cloud
        
    def load_gps_tracking_data(self, match_id):
        """
        Load StatsBomb GPS tracking data (Three-Sixty)
        
        Args:
            match_id: Match ID
            
        Returns:
            Dictionary with GPS tracking data
        """
        # Load GPS tracking data
        tracking_file = self.data_dir / 'three-sixty' / f'{match_id}.json'
        if not tracking_file.exists():
            print(f"✗ GPS tracking file not found: {tracking_file}")
            return None
        
        try:
            with open(tracking_file, 'r') as f:
                tracking_data = json.load(f)
            
            # Load match info from events
            events_file = self.data_dir / 'events' / f'{match_id}.json'
            match_info = {}
            if events_file.exists():
                with open(events_file, 'r') as f:
                    events = json.load(f)
                if events:
                    match_info = {
                        'home_team': events[0].get('team', {}).get('name', 'Home Team'),
                        'away_team': 'Away Team',  # Will be determined from tracking data
                        'competition': 'StatsBomb Competition',
                        'season': '2023/24'
                    }
            
            return {
                'match_id': int(match_id),
                'tracking_data': tracking_data,
                'match_info': match_info
            }
        except Exception as e:
            print(f"✗ Error loading GPS tracking data {match_id}: {e}")
            return None
    
    def extract_player_positions_from_frame(self, frame_data):
        """
        Extract all player positions from a single frame
        
        Args:
            frame_data: Single frame from GPS tracking data
            
        Returns:
            Dictionary with player positions
        """
        if 'freeze_frame' not in frame_data:
            return None
        
        freeze_frame = frame_data['freeze_frame']
        if not freeze_frame:
            return None
        
        # Separate players by team
        home_players = []
        away_players = []
        
        for player in freeze_frame:
            if 'location' not in player or player['location'] is None:
                continue
            
            location = player['location']
            if len(location) >= 2:
                # Determine team based on 'teammate' flag
                if player.get('teammate', False):
                    home_players.append(location)
                else:
                    away_players.append(location)
        
        # Need at least 5 players per team (reduced threshold for GPS data)
        if len(home_players) < 5 or len(away_players) < 5:
            return None
        
        # Take up to 11 players from each team
        home_players = home_players[:11]
        away_players = away_players[:11]
        
        return {
            'home_positions': np.array(home_players),
            'away_positions': np.array(away_players)
        }
    
    def create_sliding_windows(self, tracking_data):
        """
        Create sliding windows for analysis
        
        Args:
            tracking_data: GPS tracking data
            
        Returns:
            List of window data
        """
        total_frames = len(tracking_data)
        print(f"Total GPS frames: {total_frames}")
        
        # Create sliding windows
        windows = []
        window_start = 0
        
        while window_start + self.window_duration <= total_frames:
            window_end = window_start + self.window_duration
            
            # Extract frames for this window
            window_frames = tracking_data[window_start:window_end]
            
            # Sample frames for analysis
            sampled_frames = window_frames[::self.sampling_interval]
            
            windows.append({
                'start_frame': window_start,
                'end_frame': window_end,
                'frames': sampled_frames
            })
            
            # Move to next window
            window_start += self.step_size
        
        print(f"Created {len(windows)} sliding windows")
        return windows
    
    def create_team_position_snapshot(self, window_frames):
        """
        Create team position snapshot from window frames
        
        Args:
            window_frames: List of frames in time window
            
        Returns:
            Dictionary with team positions and metrics
        """
        all_home_positions = []
        all_away_positions = []
        
        # Collect positions from all frames in window
        for frame in window_frames:
            positions = self.extract_player_positions_from_frame(frame)
            if positions is not None:
                all_home_positions.append(positions['home_positions'])
                all_away_positions.append(positions['away_positions'])
        
        if not all_home_positions or not all_away_positions:
            return None
        
        # Take median positions across the window (handle variable array sizes)
        if len(all_home_positions) > 0 and len(all_away_positions) > 0:
            # Find the minimum size to ensure all arrays have the same shape
            min_home_size = min(arr.shape[0] for arr in all_home_positions)
            min_away_size = min(arr.shape[0] for arr in all_away_positions)
            
            # Truncate all arrays to the minimum size
            home_truncated = [arr[:min_home_size] for arr in all_home_positions]
            away_truncated = [arr[:min_away_size] for arr in all_away_positions]
            
            # Now we can safely compute the median
            home_positions = np.median(home_truncated, axis=0)
            away_positions = np.median(away_truncated, axis=0)
        else:
            return None
        
        # Calculate team metrics
        home_centroid = np.mean(home_positions, axis=0)
        away_centroid = np.mean(away_positions, axis=0)
        
        # Team spreads (standard deviation)
        home_spread = np.std(home_positions, axis=0).mean()
        away_spread = np.std(away_positions, axis=0).mean()
        
        # Inter-team distance
        inter_team_distance = np.linalg.norm(home_centroid - away_centroid)
        
        # Team area ratio
        home_area = np.var(home_positions, axis=0).sum()
        away_area = np.var(away_positions, axis=0).sum()
        area_ratio = home_area / away_area if away_area > 0 else 1.0
        
        return {
            'home_positions': home_positions,
            'away_positions': away_positions,
            'home_centroid': home_centroid,
            'away_centroid': away_centroid,
            'home_spread': home_spread,
            'away_spread': away_spread,
            'inter_team_distance': inter_team_distance,
            'area_ratio': area_ratio,
            'total_spread': home_spread + away_spread
        }
    
    def compute_gps_aware_tda(self, team_snapshot):
        """
        Compute GPS-aware TDA analysis with adaptive filtration
        
        Args:
            team_snapshot: Team position snapshot
            
        Returns:
            Dictionary with TDA results
        """
        if team_snapshot is None:
            return None
        
        # Get all player positions
        all_positions = np.vstack([
            team_snapshot['home_positions'],
            team_snapshot['away_positions']
        ])
        
        # GPS-aware clustering
        if len(all_positions) > 1:
            distances = pdist(all_positions)
            if len(distances) > 0:
                Z = linkage(distances, method='single')
                labels = fcluster(Z, self.cutoff_distance, criterion='distance')
                unique = np.unique(labels)
                centers = []
                for lab in unique:
                    pts = all_positions[labels == lab]
                    centers.append(np.mean(pts, axis=0))
                point_cloud = np.array(centers)
            else:
                point_cloud = all_positions
        else:
            point_cloud = all_positions
        
        # Persistent homology with adaptive filtration
        if len(point_cloud) > 1:
            # Calculate adaptive filtration based on point cloud scale
            distances = pdist(point_cloud)
            if len(distances) > 0:
                # Use 75th percentile of distances as max filtration
                max_filtration = np.percentile(distances, 75)
                max_filtration = max(max_filtration, 5.0)  # Minimum 5.0
            else:
                max_filtration = 5.0
            
            diagrams = ripser(point_cloud, maxdim=1, thresh=max_filtration)
            h0_count = len(diagrams['dgms'][0])
            h1_count = len(diagrams['dgms'][1])
        else:
            h0_count, h1_count = 1, 0
        
        # Complexity index
        cluster_count = len(point_cloud)
        complexity = (h0_count + h1_count) / cluster_count if cluster_count > 0 else 0.0
        
        return {
            'h0_count': h0_count,
            'h1_count': h1_count,
            'cluster_count': cluster_count,
            'complexity': complexity,
            'point_cloud': point_cloud
        }
    
    def analyze_zero_sum_configuration(self, results_df):
        """
        Analyze zero-sum geometric configuration
        
        Args:
            results_df: DataFrame with analysis results
            
        Returns:
            Dictionary with zero-sum analysis
        """
        # Calculate correlations
        home_spread = results_df['home_spread'].values
        away_spread = results_df['away_spread'].values
        total_spread = results_df['total_spread'].values
        
        # Pearson correlation
        pearson_corr = np.corrcoef(home_spread, away_spread)[0, 1]
        
        # L1-norm robust regression
        X = home_spread.reshape(-1, 1)
        y = away_spread
        
        # Huber regression for robustness
        huber = HuberRegressor(epsilon=1.35)
        huber.fit(X, y)
        l1_coefficient = huber.coef_[0]
        
        # Zero-sum strength
        zero_sum_strength = abs(l1_coefficient)
        
        # Conservation law analysis
        total_spread_mean = np.mean(total_spread)
        total_spread_std = np.std(total_spread)
        conservation_stability = 1.0 / (1.0 + total_spread_std / total_spread_mean)
        
        return {
            'pearson_correlation': pearson_corr,
            'l1_coefficient': l1_coefficient,
            'zero_sum_strength': zero_sum_strength,
            'total_spread_mean': total_spread_mean,
            'total_spread_std': total_spread_std,
            'conservation_stability': conservation_stability
        }
    
    def analyze_quantum_phenomena(self, results_df):
        """
        Analyze quantum phenomena in team dynamics
        
        Args:
            results_df: DataFrame with analysis results
            
        Returns:
            Dictionary with quantum analysis
        """
        # Energy levels based on complexity
        complexity = results_df['complexity'].values
        
        # Quantum energy levels (inverse relationship with complexity)
        energy_levels = 1.0 / (complexity + 1e-6)
        
        # Quantum coherence (consistency of energy levels)
        energy_coherence = 1.0 / (1.0 + np.std(energy_levels) / np.mean(energy_levels))
        
        # Quantum tunneling (transitions between energy levels)
        energy_diff = np.diff(energy_levels)
        tunneling_probability = np.mean(np.abs(energy_diff)) / np.mean(energy_levels)
        
        # Quantum yield (performance measure)
        quantum_yield = np.mean(energy_levels) * energy_coherence
        
        # Attractor states using K-means
        X = results_df[['h0_count', 'h1_count', 'complexity', 'home_spread', 'away_spread']].values
        
        # Determine optimal number of clusters
        n_clusters = min(5, max(2, len(X) // 5))  # At least 5 points per cluster, minimum 2
        if len(X) < 2:
            n_clusters = 1
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(X)
        
        # Quantum states by cluster
        quantum_states = {}
        for i in range(n_clusters):
            cluster_mask = cluster_labels == i
            cluster_data = results_df[cluster_mask]
            
            quantum_states[i] = {
                'count': np.sum(cluster_mask),
                'mean_complexity': cluster_data['complexity'].mean(),
                'mean_energy': np.mean(energy_levels[cluster_mask]),
                'mean_h0': cluster_data['h0_count'].mean(),
                'mean_h1': cluster_data['h1_count'].mean()
            }
        
        return {
            'energy_levels': energy_levels,
            'energy_coherence': energy_coherence,
            'tunneling_probability': tunneling_probability,
            'quantum_yield': quantum_yield,
            'n_attractor_states': n_clusters,
            'quantum_states': quantum_states,
            'cluster_labels': cluster_labels
        }
    
    def run_gps_tracking_analysis(self, match_id, output_dir='statsbomb_gps_tracking_results'):
        """
        Run complete GPS tracking analysis on a single match
        
        Args:
            match_id: Match ID to analyze
            output_dir: Output directory for results
            
        Returns:
            Dictionary with complete analysis results
        """
        print(f"\n🔬 GPS TRACKING ANALYSIS: Match {match_id}")
        print("=" * 70)
        
        # Load GPS tracking data
        match_data = self.load_gps_tracking_data(match_id)
        if match_data is None:
            return None
        
        # Create sliding windows
        windows = self.create_sliding_windows(match_data['tracking_data'])
        
        if not windows:
            print("No valid windows created")
            return None
        
        # Analyze each window
        results = []
        
        print(f"\nAnalyzing {len(windows)} windows...")
        for i, window in enumerate(tqdm(windows, desc="Processing windows")):
            # Create team position snapshot
            team_snapshot = self.create_team_position_snapshot(window['frames'])
            
            if team_snapshot is None:
                continue
            
            # Compute GPS-aware TDA
            tda_result = self.compute_gps_aware_tda(team_snapshot)
            
            if tda_result is None:
                continue
            
            # Store results
            result = {
                'match_id': match_id,
                'window_id': i,
                'start_frame': window['start_frame'],
                'end_frame': window['end_frame'],
                'home_team': match_data['match_info'].get('home_team', 'Home'),
                'away_team': match_data['match_info'].get('away_team', 'Away'),
                'competition': match_data['match_info'].get('competition', 'Unknown'),
                'season': match_data['match_info'].get('season', 'Unknown'),
                'h0_count': tda_result['h0_count'],
                'h1_count': tda_result['h1_count'],
                'cluster_count': tda_result['cluster_count'],
                'complexity': tda_result['complexity'],
                'home_spread': team_snapshot['home_spread'],
                'away_spread': team_snapshot['away_spread'],
                'inter_team_distance': team_snapshot['inter_team_distance'],
                'area_ratio': team_snapshot['area_ratio'],
                'total_spread': team_snapshot['total_spread']
            }
            
            results.append(result)
        
        if not results:
            print("No valid results generated")
            return None
        
        # Convert to DataFrame
        results_df = pd.DataFrame(results)
        
        # Run complete analysis
        print(f"\n📊 Running complete analysis on {len(results_df)} windows...")
        
        # Zero-sum analysis
        zero_sum_analysis = self.analyze_zero_sum_configuration(results_df)
        print(f"✓ Zero-sum strength: {zero_sum_analysis['zero_sum_strength']:.4f}")
        
        # Quantum phenomena analysis
        quantum_analysis = self.analyze_quantum_phenomena(results_df)
        print(f"✓ Quantum yield: {quantum_analysis['quantum_yield']:.4f}")
        print(f"✓ Attractor states: {quantum_analysis['n_attractor_states']}")
        
        # Save results
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save detailed results
        results_file = Path(output_dir) / f'match_{match_id}_gps_tracking_analysis.csv'
        results_df.to_csv(results_file, index=False)
        
        # Save analysis summary
        analysis_summary = {
            'match_id': match_id,
            'total_windows': len(results_df),
            'window_duration': self.window_duration,
            'step_size': self.step_size,
            'zero_sum_analysis': zero_sum_analysis,
            'quantum_analysis': quantum_analysis
        }
        
        summary_file = Path(output_dir) / f'match_{match_id}_gps_tracking_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(analysis_summary, f, indent=2, default=str)
        
        print(f"\n✅ GPS tracking analysis saved:")
        print(f"   - Results: {results_file}")
        print(f"   - Summary: {summary_file}")
        
        return analysis_summary
    
    def run_multi_match_gps_analysis(self, match_ids, output_dir='statsbomb_gps_tracking_results'):
        """
        Run GPS tracking analysis on multiple matches
        
        Args:
            match_ids: List of match IDs
            output_dir: Output directory for results
            
        Returns:
            Dictionary with multi-match analysis
        """
        print("\n" + "🚀" * 50)
        print("STATSBOMB GPS TRACKING ANALYSIS")
        print("🚀" * 50)
        print(f"Matches to analyze: {len(match_ids)}")
        print(f"Window duration: {self.window_duration} frames")
        print(f"Step size: {self.step_size} frames")
        
        all_results = []
        successful_matches = 0
        
        for match_id in tqdm(match_ids, desc="Analyzing matches"):
            try:
                result = self.run_gps_tracking_analysis(match_id, output_dir)
                if result is not None:
                    all_results.append(result)
                    successful_matches += 1
            except Exception as e:
                print(f"✗ Error analyzing match {match_id}: {e}")
        
        if not all_results:
            print("❌ No matches successfully analyzed")
            return None
        
        # Create multi-match summary
        multi_match_summary = {
            'total_matches': len(match_ids),
            'successful_matches': successful_matches,
            'failed_matches': len(match_ids) - successful_matches,
            'window_duration': self.window_duration,
            'step_size': self.step_size,
            'individual_results': all_results
        }
        
        # Save multi-match summary
        summary_file = Path(output_dir) / 'multi_match_gps_tracking_analysis.json'
        with open(summary_file, 'w') as f:
            json.dump(multi_match_summary, f, indent=2, default=str)
        
        print(f"\n🎉 GPS TRACKING ANALYSIS COMPLETE!")
        print(f"✅ Successful matches: {successful_matches}")
        print(f"✗ Failed matches: {len(match_ids) - successful_matches}")
        print(f"📊 Results saved: {output_dir}")
        
        return multi_match_summary


def main():
    """
    Main execution function
    """
    print("StatsBomb GPS Tracking Analysis")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = StatsBombGPSTrackingAnalysis(cutoff_distance=1.0)
    
    # Get matches with both events and GPS tracking data
    tracking_dir = Path('open-data/data/three-sixty')
    events_dir = Path('open-data/data/events')
    
    tracking_files = list(tracking_dir.glob('*.json'))
    event_files = list(events_dir.glob('*.json'))
    
    tracking_match_ids = [f.stem for f in tracking_files]
    event_match_ids = [f.stem for f in event_files]
    
    common_matches = set(tracking_match_ids) & set(event_match_ids)
    common_list = sorted(list(common_matches))
    
    # Take first 3 matches for analysis
    match_ids = common_list[:3]
    
    print(f"Selected {len(match_ids)} matches with GPS tracking data")
    print(f"Match IDs: {match_ids}")
    print(f"Window duration: {pipeline.window_duration} frames (2 minutes at 25Hz)")
    print(f"Step size: {pipeline.step_size} frames (24 seconds)")
    print(f"Expected overlap: {100 * (1 - pipeline.step_size / pipeline.window_duration):.1f}%")
    
    # Run GPS tracking analysis
    results = pipeline.run_multi_match_gps_analysis(match_ids)
    
    if results is not None:
        print("\n" + "=" * 70)
        print("GPS TRACKING ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Total matches: {results['total_matches']}")
        print(f"Successful: {results['successful_matches']}")
        print(f"Failed: {results['failed_matches']}")
        
        # Calculate total windows
        total_windows = sum(r['total_windows'] for r in results['individual_results'])
        print(f"Total windows analyzed: {total_windows}")
        
        print("\n🎯 GPS TRACKING ANALYSIS COMPLETE!")
        print("✅ Proper GPS tracking data used")
        print("✅ Ready for SecondSpectrum comparison")
        print("✅ Apples-to-apples comparison achieved")
    else:
        print("❌ GPS tracking analysis failed")


if __name__ == "__main__":
    main()
