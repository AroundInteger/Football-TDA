#!/usr/bin/env python3
"""
SkillCorner Events-Based TDA Analysis
=====================================

This script performs TDA analysis using the available SkillCorner data:
- Dynamic events (passes, possessions, engagements, runs)
- Phases of play (attacking/defending phases)
- Match information

Since tracking data is not available due to LFS issues, we'll work with
the rich event and phase data to understand team dynamics.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# TDA libraries
try:
    import ripser
    from ripser import ripser
    RIPSER_AVAILABLE = True
except ImportError:
    RIPSER_AVAILABLE = False
    print("Warning: Ripser not available. Install with: pip install ripser")

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

class SkillCornerEventsTDAAnalyzer:
    def __init__(self, data_path, match_id):
        """
        Initialize the SkillCorner events-based TDA analyzer
        
        Args:
            data_path (str): Path to the SkillCorner data directory
            match_id (str): ID of the match to analyze
        """
        self.data_path = Path(data_path)
        self.match_id = match_id
        
        # Data storage
        self.match_info = {}
        self.events_data = None
        self.phases_data = None
        self.team_metrics = []
        self.point_clouds = []
        self.persistence_diagrams = []
        self.attractor_analysis = {}
        
        # Analysis parameters
        self.max_filtration = 2.0
        self.n_clusters = 3
        
    def load_match_data(self):
        """Load all available match data"""
        print(f"Loading data for match {self.match_id}...")
        
        # Load match information
        match_file = self.data_path / "matches" / str(self.match_id) / f"{self.match_id}_match.json"
        if match_file.exists():
            with open(match_file, 'r') as f:
                self.match_info = json.load(f)
            print(f"Loaded match info: {self.match_info.get('home_team', {}).get('name', 'Unknown')} vs {self.match_info.get('away_team', {}).get('name', 'Unknown')}")
        
        # Load events data
        events_file = self.data_path / "matches" / str(self.match_id) / f"{self.match_id}_dynamic_events.csv"
        if events_file.exists():
            self.events_data = pd.read_csv(events_file)
            print(f"Loaded {len(self.events_data)} events")
        
        # Load phases data
        phases_file = self.data_path / "matches" / str(self.match_id) / f"{self.match_id}_phases_of_play.csv"
        if phases_file.exists():
            self.phases_data = pd.read_csv(phases_file)
            print(f"Loaded {len(self.phases_data)} phases")
        
        return True
    
    def calculate_team_metrics_from_events(self):
        """Calculate team metrics from events data"""
        print("Calculating team metrics from events data...")
        
        if self.events_data is None:
            print("No events data available")
            return []
        
        # Group events by time windows (e.g., every 30 seconds)
        time_window = 30  # seconds
        
        # Parse time format (MM:SS.s)
        def parse_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                parts = str(time_str).split(':')
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = float(parts[1])
                    return minutes * 60 + seconds
                return np.nan
            except:
                return np.nan
        
        time_end_parsed = self.events_data['time_end'].apply(parse_time)
        max_time = time_end_parsed.max()
        
        if pd.isna(max_time):
            print("No valid time data found")
            return []
        
        metrics = []
        
        for start_time in np.arange(0, max_time, time_window):
            end_time = start_time + time_window
            
            # Filter events in this time window
            time_start_parsed = self.events_data['time_start'].apply(parse_time)
            window_events = self.events_data[
                (time_start_parsed >= start_time) & 
                (time_start_parsed < end_time)
            ]
            
            if len(window_events) == 0:
                continue
            
            # Calculate metrics for this window
            window_metrics = self.calculate_window_metrics(window_events, start_time)
            if window_metrics:
                metrics.append(window_metrics)
        
        self.team_metrics = metrics
        print(f"Calculated metrics for {len(metrics)} time windows")
        
        return metrics
    
    def calculate_window_metrics(self, window_events, start_time):
        """Calculate metrics for a specific time window"""
        try:
            # Get home and away team IDs
            home_team_id = self.match_info.get('home_team', {}).get('id')
            away_team_id = self.match_info.get('away_team', {}).get('id')
            
            if not home_team_id or not away_team_id:
                return None
            
            # Separate events by team
            home_events = window_events[window_events['team_id'] == home_team_id]
            away_events = window_events[window_events['team_id'] == away_team_id]
            
            # Calculate basic metrics
            home_event_count = len(home_events)
            away_event_count = len(away_events)
            
            # Calculate spatial metrics (using event positions)
            home_positions = home_events[['x_start', 'y_start']].dropna()
            away_positions = away_events[['x_start', 'y_start']].dropna()
            
            if len(home_positions) == 0 or len(away_positions) == 0:
                return None
            
            # Team centroids
            home_centroid = home_positions.mean()
            away_centroid = away_positions.mean()
            
            # Inter-team distance
            inter_team_distance = np.linalg.norm(home_centroid - away_centroid)
            
            # Team spreads
            home_spread = home_positions.std()
            away_spread = away_positions.std()
            
            # Event intensity (events per second)
            window_duration = 30  # seconds
            home_intensity = home_event_count / window_duration
            away_intensity = away_event_count / window_duration
            
            # Event type distribution
            home_event_types = home_events['event_type'].value_counts()
            away_event_types = away_events['event_type'].value_counts()
            
            # Calculate event diversity (entropy)
            home_diversity = self.calculate_entropy(home_event_types)
            away_diversity = self.calculate_entropy(away_event_types)
            
            metrics = {
                'start_time': start_time,
                'home_event_count': home_event_count,
                'away_event_count': away_event_count,
                'home_centroid_x': home_centroid['x_start'],
                'home_centroid_y': home_centroid['y_start'],
                'away_centroid_x': away_centroid['x_start'],
                'away_centroid_y': away_centroid['y_start'],
                'inter_team_distance': inter_team_distance,
                'home_spread_x': home_spread['x_start'],
                'home_spread_y': home_spread['y_start'],
                'away_spread_x': away_spread['x_start'],
                'away_spread_y': away_spread['y_start'],
                'home_intensity': home_intensity,
                'away_intensity': away_intensity,
                'home_diversity': home_diversity,
                'away_diversity': away_diversity,
                'total_events': home_event_count + away_event_count
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating window metrics: {e}")
            return None
    
    def calculate_entropy(self, value_counts):
        """Calculate entropy of a distribution"""
        if len(value_counts) == 0:
            return 0
        
        probabilities = value_counts / value_counts.sum()
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy
    
    def calculate_phase_metrics(self):
        """Calculate metrics from phases of play data"""
        print("Calculating phase-based metrics...")
        
        if self.phases_data is None:
            print("No phases data available")
            return []
        
        phase_metrics = []
        
        for _, phase in self.phases_data.iterrows():
            try:
                # Basic phase metrics
                duration = phase['duration']
                team_in_possession = phase['team_in_possession_shortname']
                
                # Spatial metrics
                x_start, y_start = phase['x_start'], phase['y_start']
                x_end, y_end = phase['x_end'], phase['y_end']
                
                # Team formation metrics
                home_width_start = phase['team_in_possession_width_start']
                home_length_start = phase['team_in_possession_length_start']
                away_width_start = phase['team_out_of_possession_width_start']
                away_length_start = phase['team_out_of_possession_length_start']
                
                # Calculate formation complexity
                formation_complexity = self.calculate_formation_complexity(
                    home_width_start, home_length_start,
                    away_width_start, away_length_start
                )
                
                phase_metric = {
                    'phase_index': phase['index'],
                    'start_time': phase['time_start'],
                    'duration': duration,
                    'team_in_possession': team_in_possession,
                    'x_start': x_start,
                    'y_start': y_start,
                    'x_end': x_end,
                    'y_end': y_end,
                    'home_width': home_width_start,
                    'home_length': home_length_start,
                    'away_width': away_width_start,
                    'away_length': away_length_start,
                    'formation_complexity': formation_complexity,
                    'phase_type': phase['team_in_possession_phase_type']
                }
                
                phase_metrics.append(phase_metric)
                
            except Exception as e:
                print(f"Error processing phase: {e}")
                continue
        
        print(f"Calculated {len(phase_metrics)} phase metrics")
        return phase_metrics
    
    def calculate_formation_complexity(self, home_w, home_l, away_w, away_l):
        """Calculate formation complexity from team dimensions"""
        # Simple complexity measure based on team shape ratios
        home_ratio = home_w / (home_l + 1e-6)
        away_ratio = away_w / (away_l + 1e-6)
        
        # Complexity increases with shape variation
        complexity = abs(home_ratio - away_ratio) + (home_w + away_w) / 100
        return complexity
    
    def create_point_clouds_from_metrics(self):
        """Create point clouds for TDA analysis from calculated metrics"""
        print("Creating point clouds for TDA analysis...")
        
        if not self.team_metrics:
            print("No team metrics available")
            return None
        
        # Convert metrics to numpy array
        metric_keys = ['inter_team_distance', 'home_spread_x', 'home_spread_y', 
                      'away_spread_x', 'away_spread_y', 'home_intensity', 
                      'away_intensity', 'home_diversity', 'away_diversity']
        
        metrics_array = []
        for metric in self.team_metrics:
            row = [metric.get(key, 0) for key in metric_keys]
            metrics_array.append(row)
        
        metrics_array = np.array(metrics_array)
        
        # Remove NaN values
        valid_indices = ~np.isnan(metrics_array).any(axis=1)
        metrics_clean = metrics_array[valid_indices]
        
        if len(metrics_clean) == 0:
            print("No valid metrics for point cloud creation")
            return None
        
        # Standardize the data
        scaler = StandardScaler()
        metrics_scaled = scaler.fit_transform(metrics_clean)
        
        self.point_clouds = metrics_scaled
        print(f"Created point cloud with {len(metrics_scaled)} points and {metrics_scaled.shape[1]} dimensions")
        
        return metrics_scaled
    
    def compute_persistent_homology(self):
        """Compute persistent homology using Ripser"""
        if not RIPSER_AVAILABLE:
            print("Ripser not available. Skipping persistent homology computation.")
            return None
        
        if len(self.point_clouds) == 0:
            print("No point clouds available")
            return None
        
        print("Computing persistent homology...")
        
        try:
            # Compute persistence diagrams
            diagrams = ripser(self.point_clouds, maxdim=2, thresh=self.max_filtration)
            
            self.persistence_diagrams = diagrams['dgms']
            
            print(f"Computed persistence diagrams:")
            for i, dgm in enumerate(self.persistence_diagrams):
                print(f"  H{i}: {len(dgm)} features")
            
            return diagrams
            
        except Exception as e:
            print(f"Error computing persistent homology: {e}")
            return None
    
    def identify_attractor_states(self):
        """Identify attractor states using k-means clustering"""
        print("Identifying attractor states...")
        
        if len(self.point_clouds) == 0:
            print("No point clouds available")
            return None
        
        # Determine optimal number of clusters
        silhouette_scores = []
        k_range = range(2, min(8, len(self.point_clouds) // 5))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(self.point_clouds)
            silhouette_avg = silhouette_score(self.point_clouds, cluster_labels)
            silhouette_scores.append(silhouette_avg)
        
        if not silhouette_scores:
            print("Not enough data for clustering")
            return None
        
        # Choose optimal k
        optimal_k = k_range[np.argmax(silhouette_scores)]
        print(f"Optimal number of clusters: {optimal_k} (silhouette score: {max(silhouette_scores):.3f})")
        
        # Final clustering
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(self.point_clouds)
        
        # Analyze attractor states
        attractor_analysis = {
            'n_states': optimal_k,
            'cluster_labels': cluster_labels.tolist(),
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'silhouette_score': max(silhouette_scores),
            'state_frequencies': np.bincount(cluster_labels).tolist()
        }
        
        self.attractor_analysis = attractor_analysis
        
        print(f"Identified {optimal_k} attractor states")
        print(f"State frequencies: {attractor_analysis['state_frequencies']}")
        
        return attractor_analysis
    
    def calculate_complexity_metrics(self):
        """Calculate formation complexity metrics"""
        print("Calculating complexity metrics...")
        
        if not self.persistence_diagrams:
            print("No persistence diagrams available")
            return None
        
        complexity_metrics = {}
        
        # Count topological features
        h0_count = len(self.persistence_diagrams[0]) if len(self.persistence_diagrams) > 0 else 0
        h1_count = len(self.persistence_diagrams[1]) if len(self.persistence_diagrams) > 1 else 0
        h2_count = len(self.persistence_diagrams[2]) if len(self.persistence_diagrams) > 2 else 0
        
        # Complexity index
        total_features = h0_count + h1_count + h2_count
        complexity_index = total_features / len(self.point_clouds) if len(self.point_clouds) > 0 else 0
        
        # Quantum yield (H2/H1 ratio)
        quantum_yield = h2_count / h1_count if h1_count > 0 else 0
        
        # Performance intensity
        performance_intensity = (h1_count + h2_count) / h0_count if h0_count > 0 else 0
        
        complexity_metrics = {
            'h0_features': h0_count,
            'h1_features': h1_count,
            'h2_features': h2_count,
            'total_features': total_features,
            'complexity_index': complexity_index,
            'quantum_yield': quantum_yield,
            'performance_intensity': performance_intensity
        }
        
        print(f"Complexity metrics:")
        print(f"  H0 features: {h0_count}")
        print(f"  H1 features: {h1_count}")
        print(f"  H2 features: {h2_count}")
        print(f"  Complexity index: {complexity_index:.4f}")
        print(f"  Quantum yield: {quantum_yield:.4f}")
        print(f"  Performance intensity: {performance_intensity:.4f}")
        
        return complexity_metrics
    
    def run_complete_analysis(self):
        """Run the complete TDA analysis pipeline"""
        print("=== SkillCorner Events-Based TDA Analysis ===")
        print(f"Match ID: {self.match_id}")
        print()
        
        # Load data
        self.load_match_data()
        
        # Calculate metrics
        self.calculate_team_metrics_from_events()
        
        if not self.team_metrics:
            print("No team metrics calculated. Analysis cannot proceed.")
            return None
        
        # Create point clouds
        self.create_point_clouds_from_metrics()
        
        if len(self.point_clouds) == 0:
            print("No point clouds created. Analysis cannot proceed.")
            return None
        
        # TDA analysis
        self.compute_persistent_homology()
        self.identify_attractor_states()
        complexity_metrics = self.calculate_complexity_metrics()
        
        # Compile results
        results = {
            'match_id': self.match_id,
            'match_info': self.match_info,
            'total_events': len(self.events_data) if self.events_data is not None else 0,
            'total_phases': len(self.phases_data) if self.phases_data is not None else 0,
            'time_windows': len(self.team_metrics),
            'point_cloud_size': len(self.point_clouds),
            'persistence_diagrams': self.persistence_diagrams,
            'attractor_analysis': self.attractor_analysis,
            'complexity_metrics': complexity_metrics,
            'team_metrics': self.team_metrics
        }
        
        print("\n=== Analysis Complete ===")
        print(f"Processed {len(self.team_metrics)} time windows")
        print(f"Identified {self.attractor_analysis.get('n_states', 0)} attractor states")
        print(f"Complexity index: {complexity_metrics.get('complexity_index', 0):.4f}")
        
        return results
    
    def export_results(self, output_dir="skillcorner_events_results"):
        """Export analysis results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export team metrics
        if self.team_metrics:
            metrics_df = pd.DataFrame(self.team_metrics)
            metrics_file = output_path / f"{self.match_id}_events_metrics.csv"
            metrics_df.to_csv(metrics_file, index=False)
            print(f"Exported team metrics to: {metrics_file}")
        
        # Export attractor analysis
        if self.attractor_analysis:
            attractor_file = output_path / f"{self.match_id}_events_attractor_analysis.json"
            with open(attractor_file, 'w') as f:
                json.dump(self.attractor_analysis, f, indent=2)
            print(f"Exported attractor analysis to: {attractor_file}")
        
        # Export complexity metrics
        if hasattr(self, 'complexity_metrics') and self.complexity_metrics:
            complexity_file = output_path / f"{self.match_id}_events_complexity_metrics.json"
            with open(complexity_file, 'w') as f:
                json.dump(self.complexity_metrics, f, indent=2)
            print(f"Exported complexity metrics to: {complexity_file}")

def main():
    """Main function to run the analysis"""
    # Example usage
    data_path = "opendata/data"
    match_id = 2017461  # Melbourne Victory vs Auckland FC
    
    analyzer = SkillCornerEventsTDAAnalyzer(data_path, match_id)
    
    try:
        results = analyzer.run_complete_analysis()
        if results:
            analyzer.export_results()
            print("\nAnalysis completed successfully!")
        else:
            print("Analysis failed - no results generated")
    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
