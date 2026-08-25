#!/usr/bin/env python3
"""
SkillCorner TDA Analysis Script
==============================

This script adapts our existing TDA analysis pipeline for SkillCorner data format.
It processes the JSONL tracking data and performs topological data analysis.

Based on: https://github.com/SkillCorner/opendata
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

try:
    import gudhi
    GUDHI_AVAILABLE = True
except ImportError:
    GUDHI_AVAILABLE = False
    print("Warning: Gudhi not available. Install with: pip install gudhi")

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

class SkillCornerTDAAnalyzer:
    def __init__(self, data_path, match_id, max_frames=None):
        """
        Initialize the SkillCorner TDA analyzer
        
        Args:
            data_path (str): Path to the SkillCorner data directory
            match_id (str): ID of the match to analyze
            max_frames (int): Maximum number of frames to process (None for all)
        """
        self.data_path = Path(data_path)
        self.match_id = match_id
        self.max_frames = max_frames
        
        # Data storage
        self.tracking_data = []
        self.team_metrics = []
        self.point_clouds = []
        self.persistence_diagrams = []
        self.attractor_analysis = {}
        
        # Analysis parameters
        self.max_filtration = 2.0
        self.n_clusters = 3
        
    def load_tracking_data(self):
        """Load tracking data from JSONL file"""
        tracking_file = self.data_path / "matches" / self.match_id / f"{self.match_id}_tracking_extrapolated.jsonl"
        
        if not tracking_file.exists():
            raise FileNotFoundError(f"Tracking file not found: {tracking_file}")
        
        print(f"Loading tracking data from: {tracking_file}")
        
        frames = []
        with open(tracking_file, 'r') as f:
            for i, line in enumerate(f):
                if self.max_frames and i >= self.max_frames:
                    break
                frames.append(json.loads(line.strip()))
        
        self.tracking_data = frames
        print(f"Loaded {len(frames)} frames")
        
        return frames
    
    def extract_player_positions(self, frame):
        """Extract player positions from a frame"""
        player_data = frame.get('player_data', [])
        
        home_players = []
        away_players = []
        
        for player in player_data:
            x = player.get('x', np.nan)
            y = player.get('y', np.nan)
            player_id = player.get('player_id', '')
            is_detected = player.get('is_detected', False)
            
            # Determine team based on player_id (this may need adjustment based on actual data)
            # For now, assume even/odd player IDs indicate different teams
            if player_id and str(player_id).isdigit():
                if int(player_id) % 2 == 0:
                    home_players.append([x, y, player_id, is_detected])
                else:
                    away_players.append([x, y, player_id, is_detected])
        
        return np.array(home_players), np.array(away_players)
    
    def calculate_team_metrics(self, home_players, away_players):
        """Calculate team metrics from player positions"""
        metrics = {}
        
        # Filter out NaN positions
        home_valid = home_players[~np.isnan(home_players[:, 0])]
        away_valid = away_players[~np.isnan(away_players[:, 0])]
        
        if len(home_valid) == 0 or len(away_valid) == 0:
            return None
        
        # Team centroids
        home_centroid = np.mean(home_valid[:, :2], axis=0)
        away_centroid = np.mean(away_valid[:, :2], axis=0)
        
        # Inter-team distance
        inter_team_distance = np.linalg.norm(home_centroid - away_centroid)
        
        # Team spreads (standard deviation of positions)
        home_spread = np.std(home_valid[:, :2], axis=0)
        away_spread = np.std(away_valid[:, :2], axis=0)
        
        # Team areas (convex hull approximation)
        if len(home_valid) >= 3:
            home_area = self.calculate_convex_hull_area(home_valid[:, :2])
        else:
            home_area = 0
        
        if len(away_valid) >= 3:
            away_area = self.calculate_convex_hull_area(away_valid[:, :2])
        else:
            away_area = 0
        
        # Nearest opponent distances
        home_nod = self.calculate_nod(home_valid[:, :2], away_valid[:, :2])
        away_nod = self.calculate_nod(away_valid[:, :2], home_valid[:, :2])
        
        metrics = {
            'inter_team_distance': inter_team_distance,
            'home_centroid_x': home_centroid[0],
            'home_centroid_y': home_centroid[1],
            'away_centroid_x': away_centroid[0],
            'away_centroid_y': away_centroid[1],
            'home_spread_x': home_spread[0],
            'home_spread_y': home_spread[1],
            'away_spread_x': away_spread[0],
            'away_spread_y': away_spread[1],
            'home_area': home_area,
            'away_area': away_area,
            'area_ratio': home_area / (away_area + 1e-6),  # Avoid division by zero
            'home_nod': home_nod,
            'away_nod': away_nod,
            'mean_nod': (home_nod + away_nod) / 2
        }
        
        return metrics
    
    def calculate_convex_hull_area(self, points):
        """Calculate approximate convex hull area"""
        if len(points) < 3:
            return 0
        
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(points)
            return hull.volume  # For 2D, volume is area
        except ImportError:
            # Fallback: use bounding box area
            x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
            y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
            return (x_max - x_min) * (y_max - y_min)
    
    def calculate_nod(self, team_positions, opponent_positions):
        """Calculate nearest opponent distance for a team"""
        if len(team_positions) == 0 or len(opponent_positions) == 0:
            return np.nan
        
        distances = []
        for player in team_positions:
            player_distances = np.linalg.norm(opponent_positions - player, axis=1)
            distances.append(np.min(player_distances))
        
        return np.mean(distances)
    
    def process_all_frames(self):
        """Process all frames to calculate team metrics"""
        print("Processing frames to calculate team metrics...")
        
        for i, frame in enumerate(self.tracking_data):
            if i % 1000 == 0 and i > 0:
                print(f"  Processed {i}/{len(self.tracking_data)} frames...")
            
            home_players, away_players = self.extract_player_positions(frame)
            metrics = self.calculate_team_metrics(home_players, away_players)
            
            if metrics is not None:
                metrics['frame'] = i
                metrics['timestamp'] = frame.get('timestamp', i * 0.1)  # 10 FPS
                metrics['period'] = frame.get('period', 1)
                self.team_metrics.append(metrics)
        
        print(f"Calculated metrics for {len(self.team_metrics)} frames")
        
        return self.team_metrics
    
    def create_point_clouds(self):
        """Create point clouds for TDA analysis"""
        print("Creating point clouds for TDA analysis...")
        
        if not self.team_metrics:
            raise ValueError("No team metrics available. Run process_all_frames() first.")
        
        # Convert metrics to numpy array
        metrics_array = np.array([[m['inter_team_distance'], 
                                 m['home_spread_x'], m['home_spread_y'],
                                 m['away_spread_x'], m['away_spread_y'],
                                 m['mean_nod']] for m in self.team_metrics])
        
        # Remove NaN values
        valid_indices = ~np.isnan(metrics_array).any(axis=1)
        metrics_clean = metrics_array[valid_indices]
        
        if len(metrics_clean) == 0:
            raise ValueError("No valid metrics for point cloud creation")
        
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
            raise ValueError("No point clouds available. Run create_point_clouds() first.")
        
        # Determine optimal number of clusters
        silhouette_scores = []
        k_range = range(2, min(8, len(self.point_clouds) // 10))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(self.point_clouds)
            silhouette_avg = silhouette_score(self.point_clouds, cluster_labels)
            silhouette_scores.append(silhouette_avg)
        
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
            'state_frequencies': np.bincount(cluster_labels).tolist(),
            'state_lifetimes': self.calculate_state_lifetimes(cluster_labels)
        }
        
        self.attractor_analysis = attractor_analysis
        
        print(f"Identified {optimal_k} attractor states")
        print(f"State frequencies: {attractor_analysis['state_frequencies']}")
        
        return attractor_analysis
    
    def calculate_state_lifetimes(self, cluster_labels):
        """Calculate lifetimes of each attractor state"""
        lifetimes = [[] for _ in range(max(cluster_labels) + 1)]
        
        current_state = cluster_labels[0]
        current_lifetime = 1
        
        for i in range(1, len(cluster_labels)):
            if cluster_labels[i] == current_state:
                current_lifetime += 1
            else:
                lifetimes[current_state].append(current_lifetime)
                current_state = cluster_labels[i]
                current_lifetime = 1
        
        # Add the last lifetime
        lifetimes[current_state].append(current_lifetime)
        
        return lifetimes
    
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
        print("=== SkillCorner TDA Analysis ===")
        print(f"Match ID: {self.match_id}")
        print(f"Max frames: {self.max_frames or 'All'}")
        print()
        
        # Load and process data
        self.load_tracking_data()
        self.process_all_frames()
        self.create_point_clouds()
        
        # TDA analysis
        self.compute_persistent_homology()
        self.identify_attractor_states()
        complexity_metrics = self.calculate_complexity_metrics()
        
        # Compile results
        results = {
            'match_id': self.match_id,
            'total_frames': len(self.tracking_data),
            'processed_frames': len(self.team_metrics),
            'point_cloud_size': len(self.point_clouds),
            'persistence_diagrams': self.persistence_diagrams,
            'attractor_analysis': self.attractor_analysis,
            'complexity_metrics': complexity_metrics,
            'team_metrics': self.team_metrics
        }
        
        print("\n=== Analysis Complete ===")
        print(f"Processed {len(self.team_metrics)} frames")
        print(f"Identified {self.attractor_analysis.get('n_states', 0)} attractor states")
        print(f"Complexity index: {complexity_metrics.get('complexity_index', 0):.4f}")
        
        return results
    
    def export_results(self, output_dir="skillcorner_results"):
        """Export analysis results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export team metrics
        if self.team_metrics:
            metrics_df = pd.DataFrame(self.team_metrics)
            metrics_file = output_path / f"{self.match_id}_team_metrics.csv"
            metrics_df.to_csv(metrics_file, index=False)
            print(f"Exported team metrics to: {metrics_file}")
        
        # Export attractor analysis
        if self.attractor_analysis:
            attractor_file = output_path / f"{self.match_id}_attractor_analysis.json"
            with open(attractor_file, 'w') as f:
                json.dump(self.attractor_analysis, f, indent=2)
            print(f"Exported attractor analysis to: {attractor_file}")
        
        # Export complexity metrics
        complexity_file = output_path / f"{self.match_id}_complexity_metrics.json"
        with open(complexity_file, 'w') as f:
            json.dump(self.complexity_metrics, f, indent=2)
        print(f"Exported complexity metrics to: {complexity_file}")

def main():
    """Main function to run the analysis"""
    # Example usage
    data_path = "skillcorner_data/data"  # Adjust path as needed
    match_id = "example_match_id"  # Replace with actual match ID
    
    # For testing, limit to first 1000 frames
    analyzer = SkillCornerTDAAnalyzer(data_path, match_id, max_frames=1000)
    
    try:
        results = analyzer.run_complete_analysis()
        analyzer.export_results()
    except Exception as e:
        print(f"Analysis failed: {e}")
        print("Make sure to:")
        print("1. Clone the SkillCorner repository")
        print("2. Set the correct data_path")
        print("3. Use a valid match_id")

if __name__ == "__main__":
    main()
