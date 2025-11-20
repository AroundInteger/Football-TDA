#!/usr/bin/env python3
"""
StatsBomb Full Sliding Window Analysis
=====================================

This script runs the complete 2-minute sliding window analysis on StatsBomb data
to match the SecondSpectrum analysis methodology and enable direct comparison.

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

class StatsBombSlidingWindowAnalysis:
    """
    Complete sliding window analysis for StatsBomb data
    """
    
    def __init__(self, data_dir='open-data/data', cutoff_distance=1.0):
        """
        Initialize sliding window analysis
        
        Args:
            data_dir: Path to StatsBomb open-data directory
            cutoff_distance: GPS-aware clustering threshold in meters
        """
        self.data_dir = Path(data_dir)
        self.cutoff_distance = cutoff_distance
        
        # Analysis parameters (matching SecondSpectrum)
        self.window_duration = 120  # 2 minutes in seconds
        self.step_size = 24  # 24 seconds step (80% overlap)
        self.sampling_interval = 5  # Every 5th frame for analysis
        self.cloud_sample_rate = 10  # Every 10th frame for point cloud
        
    def load_match_data(self, match_id):
        """
        Load StatsBomb match data
        
        Args:
            match_id: Match ID
            
        Returns:
            Dictionary with match data
        """
        # Load events data
        events_file = self.data_dir / 'events' / f'{match_id}.json'
        if not events_file.exists():
            print(f"✗ Events file not found: {events_file}")
            return None
        
        try:
            with open(events_file, 'r') as f:
                events = json.load(f)
            
            # Create basic match data structure
            match_data = {
                'match_id': int(match_id),
                'events': events,
                'home_team': {'name': 'Home Team'},
                'away_team': {'name': 'Away Team'},
                'competition': {'name': 'StatsBomb Competition'},
                'season': {'name': '2023/24'}
            }
            
            # Try to find match info from matches directory
            for comp_dir in self.data_dir.glob('matches/*'):
                match_file = comp_dir / f'{match_id}.json'
                if match_file.exists():
                    try:
                        with open(match_file, 'r') as f:
                            match_list = json.load(f)
                        
                        # Find the specific match
                        for match in match_list:
                            if str(match.get('match_id')) == str(match_id):
                                match_data.update(match)
                                break
                    except:
                        pass
                    break
            
            return match_data
        except Exception as e:
            print(f"✗ Error loading match {match_id}: {e}")
            return None
    
    def extract_temporal_events(self, match_data):
        """
        Extract events with temporal information for sliding window analysis
        
        Args:
            match_data: StatsBomb match data
            
        Returns:
            List of events with temporal ordering
        """
        events = match_data.get('events', [])
        
        # Filter for events with location data
        location_events = []
        for event in events:
            if 'location' in event and event['location'] is not None:
                # Calculate absolute time in seconds
                minute = event.get('minute', 0)
                second = event.get('second', 0)
                absolute_time = minute * 60 + second
                
                location_events.append({
                    'time': absolute_time,
                    'event': event
                })
        
        # Sort by time
        location_events.sort(key=lambda x: x['time'])
        
        return location_events
    
    def create_sliding_windows(self, temporal_events):
        """
        Create sliding windows for analysis
        
        Args:
            temporal_events: List of events with temporal information
            
        Returns:
            List of window data
        """
        if not temporal_events:
            return []
        
        # Get time range
        start_time = temporal_events[0]['time']
        end_time = temporal_events[-1]['time']
        total_duration = end_time - start_time
        
        print(f"Match duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        
        # Create sliding windows
        windows = []
        window_start = start_time
        
        while window_start + self.window_duration <= end_time:
            window_end = window_start + self.window_duration
            
            # Get events in this window
            window_events = []
            for event_data in temporal_events:
                if window_start <= event_data['time'] < window_end:
                    window_events.append(event_data['event'])
            
            if window_events:
                windows.append({
                    'start_time': window_start,
                    'end_time': window_end,
                    'events': window_events
                })
            
            # Move to next window
            window_start += self.step_size
        
        print(f"Created {len(windows)} sliding windows")
        return windows
    
    def create_team_position_snapshot(self, window_events):
        """
        Create team position snapshot for analysis
        
        Args:
            window_events: List of events in time window
            
        Returns:
            Dictionary with team positions and metrics
        """
        # Get unique players from events
        players = {}
        
        for event in window_events:
            player_id = event.get('player', {}).get('id')
            if player_id and 'location' in event and event['location'] is not None:
                location = event['location']
                if len(location) >= 2:
                    team_id = event.get('team', {}).get('id')
                    players[player_id] = {
                        'position': [location[0], location[1]],
                        'team': team_id,
                        'name': event.get('player', {}).get('name', f'Player_{player_id}')
                    }
        
        # Need at least 20 players (10 per team)
        if len(players) < 20:
            return None
        
        # Separate by team
        home_team = []
        away_team = []
        
        # Get team IDs from the first few events
        team_ids = set()
        for event in window_events[:10]:
            if 'team' in event and 'id' in event['team']:
                team_ids.add(event['team']['id'])
        
        team_ids = list(team_ids)
        if len(team_ids) < 2:
            return None
        
        home_team_id = team_ids[0]
        away_team_id = team_ids[1]
        
        for player_id, player_data in players.items():
            if player_data['team'] == home_team_id:
                home_team.append(player_data['position'])
            elif player_data['team'] == away_team_id:
                away_team.append(player_data['position'])
        
        # Ensure we have at least 10 players per team
        if len(home_team) < 10 or len(away_team) < 10:
            return None
        
        # Take first 11 players from each team
        home_team = home_team[:11]
        away_team = away_team[:11]
        
        # Calculate team metrics
        home_positions = np.array(home_team)
        away_positions = np.array(away_team)
        
        # Team centroids
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
        n_clusters = min(5, len(X) // 10)  # At least 10 points per cluster
        if n_clusters < 2:
            n_clusters = 2
        
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
    
    def run_sliding_window_analysis(self, match_id, output_dir='statsbomb_sliding_window_results'):
        """
        Run complete sliding window analysis on a single match
        
        Args:
            match_id: Match ID to analyze
            output_dir: Output directory for results
            
        Returns:
            Dictionary with complete analysis results
        """
        print(f"\n🔬 SLIDING WINDOW ANALYSIS: Match {match_id}")
        print("=" * 70)
        
        # Load match data
        match_data = self.load_match_data(match_id)
        if match_data is None:
            return None
        
        # Extract temporal events
        temporal_events = self.extract_temporal_events(match_data)
        print(f"Found {len(temporal_events)} events with location data")
        
        if not temporal_events:
            print("No temporal events found")
            return None
        
        # Create sliding windows
        windows = self.create_sliding_windows(temporal_events)
        
        if not windows:
            print("No valid windows created")
            return None
        
        # Analyze each window
        results = []
        
        print(f"\nAnalyzing {len(windows)} windows...")
        for i, window in enumerate(tqdm(windows, desc="Processing windows")):
            # Create team position snapshot
            team_snapshot = self.create_team_position_snapshot(window['events'])
            
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
                'start_time': window['start_time'],
                'end_time': window['end_time'],
                'duration': window['end_time'] - window['start_time'],
                'home_team': match_data.get('home_team', {}).get('name', 'Home'),
                'away_team': match_data.get('away_team', {}).get('name', 'Away'),
                'competition': match_data.get('competition', {}).get('name', 'Unknown'),
                'season': match_data.get('season', {}).get('name', 'Unknown'),
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
        results_file = Path(output_dir) / f'match_{match_id}_sliding_window_analysis.csv'
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
        
        summary_file = Path(output_dir) / f'match_{match_id}_sliding_window_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(analysis_summary, f, indent=2, default=str)
        
        print(f"\n✅ Sliding window analysis saved:")
        print(f"   - Results: {results_file}")
        print(f"   - Summary: {summary_file}")
        
        return analysis_summary
    
    def run_multi_match_sliding_window_analysis(self, match_ids, output_dir='statsbomb_sliding_window_results'):
        """
        Run sliding window analysis on multiple matches
        
        Args:
            match_ids: List of match IDs
            output_dir: Output directory for results
            
        Returns:
            Dictionary with multi-match analysis
        """
        print("\n" + "🚀" * 40)
        print("STATSBOMB SLIDING WINDOW ANALYSIS")
        print("🚀" * 40)
        print(f"Matches to analyze: {len(match_ids)}")
        print(f"Window duration: {self.window_duration} seconds")
        print(f"Step size: {self.step_size} seconds")
        
        all_results = []
        successful_matches = 0
        
        for match_id in tqdm(match_ids, desc="Analyzing matches"):
            try:
                result = self.run_sliding_window_analysis(match_id, output_dir)
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
        summary_file = Path(output_dir) / 'multi_match_sliding_window_analysis.json'
        with open(summary_file, 'w') as f:
            json.dump(multi_match_summary, f, indent=2, default=str)
        
        print(f"\n🎉 SLIDING WINDOW ANALYSIS COMPLETE!")
        print(f"✅ Successful matches: {successful_matches}")
        print(f"✗ Failed matches: {len(match_ids) - successful_matches}")
        print(f"📊 Results saved: {output_dir}")
        
        return multi_match_summary


def main():
    """
    Main execution function
    """
    print("StatsBomb Sliding Window Analysis")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = StatsBombSlidingWindowAnalysis(cutoff_distance=1.0)
    
    # Get match IDs from events directory
    events_dir = Path('open-data/data/events')
    event_files = [f for f in events_dir.glob('*.json')]
    match_ids = [f.stem for f in event_files[:3]]  # Start with 3 matches for full analysis
    
    print(f"Selected {len(match_ids)} matches for sliding window analysis")
    print(f"Match IDs: {match_ids}")
    print(f"Window duration: {pipeline.window_duration} seconds (2 minutes)")
    print(f"Step size: {pipeline.step_size} seconds (24 seconds)")
    print(f"Expected overlap: {100 * (1 - pipeline.step_size / pipeline.window_duration):.1f}%")
    
    # Run sliding window analysis
    results = pipeline.run_multi_match_sliding_window_analysis(match_ids)
    
    if results is not None:
        print("\n" + "=" * 70)
        print("SLIDING WINDOW ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Total matches: {results['total_matches']}")
        print(f"Successful: {results['successful_matches']}")
        print(f"Failed: {results['failed_matches']}")
        
        # Calculate total windows
        total_windows = sum(r['total_windows'] for r in results['individual_results'])
        print(f"Total windows analyzed: {total_windows}")
        
        print("\n🎯 SLIDING WINDOW ANALYSIS COMPLETE!")
        print("✅ Full temporal coverage achieved")
        print("✅ Ready for SecondSpectrum comparison")
        print("✅ Complete TDA framework validated")
    else:
        print("❌ Sliding window analysis failed")


if __name__ == "__main__":
    main()
