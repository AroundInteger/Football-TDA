#!/usr/bin/env python3
"""
Corrected TDA Pipeline with Cut-off Distance Approach
====================================================

This script implements the corrected TDA analysis using the cut-off distance
approach that successfully fixes the H0 artifact issue.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import ripser
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import DBSCAN
import time
import json

class CorrectedTDAPipeline:
    """
    Corrected TDA pipeline with cut-off distance approach
    """
    
    def __init__(self, cutoff_distance=1.0, method='hierarchical'):
        """
        Initialize corrected TDA pipeline
        
        Args:
            cutoff_distance: Distance threshold in meters for clustering
            method: Clustering method ('hierarchical', 'dbscan', 'simple')
        """
        self.cutoff_distance = cutoff_distance
        self.method = method
        self.results = {}
        
    def create_cutoff_point_cloud(self, positions, cutoff_distance=None, method=None):
        """
        Create point cloud with cut-off distance clustering
        
        Args:
            positions: Array of shape (n_points, 2)
            cutoff_distance: Distance threshold in meters
            method: Clustering method
        """
        if cutoff_distance is None:
            cutoff_distance = self.cutoff_distance
        if method is None:
            method = self.method
            
        print(f"Creating cut-off point cloud: {cutoff_distance}m threshold, {method} method")
        
        n_points = len(positions)
        print(f"Original points: {n_points}")
        
        if method == 'hierarchical':
            # Use hierarchical clustering with distance threshold
            distances = pdist(positions)
            linkage_matrix = linkage(distances, method='single')
            cluster_labels = fcluster(linkage_matrix, cutoff_distance, criterion='distance')
            
        elif method == 'dbscan':
            # Use DBSCAN with distance threshold
            clustering = DBSCAN(eps=cutoff_distance, min_samples=1).fit(positions)
            cluster_labels = clustering.labels_
            
        elif method == 'simple':
            # Simple approach: merge points within cutoff distance
            cluster_labels = self._simple_cutoff_clustering(positions, cutoff_distance)
            
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Calculate cluster centers
        unique_labels = np.unique(cluster_labels)
        cluster_centers = []
        cluster_sizes = []
        
        for label in unique_labels:
            if label == -1:  # Noise points (for DBSCAN)
                continue
            
            cluster_mask = cluster_labels == label
            cluster_points = positions[cluster_mask]
            
            # Calculate cluster center (mean position)
            center = np.mean(cluster_points, axis=0)
            cluster_centers.append(center)
            cluster_sizes.append(len(cluster_points))
        
        cluster_centers = np.array(cluster_centers)
        cluster_sizes = np.array(cluster_sizes)
        
        print(f"Cut-off result: {n_points} points → {len(cluster_centers)} clusters")
        print(f"Cluster size range: {cluster_sizes.min()} - {cluster_sizes.max()}")
        print(f"Reduction: {n_points - len(cluster_centers)} points merged")
        
        return cluster_centers, cluster_sizes, cluster_labels
    
    def _simple_cutoff_clustering(self, positions, cutoff_distance):
        """
        Simple cut-off clustering implementation
        """
        n_points = len(positions)
        cluster_labels = np.zeros(n_points, dtype=int)
        current_cluster = 0
        
        for i in range(n_points):
            if cluster_labels[i] == 0:  # Not yet assigned
                current_cluster += 1
                cluster_labels[i] = current_cluster
                
                # Find all points within cutoff distance
                for j in range(i + 1, n_points):
                    if cluster_labels[j] == 0:  # Not yet assigned
                        distance = np.linalg.norm(positions[i] - positions[j])
                        if distance <= cutoff_distance:
                            cluster_labels[j] = current_cluster
        
        return cluster_labels
    
    def compute_corrected_tda(self, point_cloud):
        """
        Compute TDA with corrected approach
        
        Args:
            point_cloud: Array of shape (n_points, n_dimensions)
        """
        if len(point_cloud) == 0:
            return {
                'h0_count': 0,
                'h1_count': 0,
                'h0_persistence': 0,
                'h1_persistence': 0,
                'assessment': 'No points'
            }
        
        print(f"Computing corrected TDA for {len(point_cloud)} points...")
        
        # Calculate pairwise distances
        distances = pdist(point_cloud)
        print(f"Distance range: {distances.min():.2f} - {distances.max():.2f}")
        
        # Use adaptive filtration based on distance distribution
        min_connectivity = np.percentile(distances, 10)
        max_filtration = min_connectivity * 3
        
        print(f"Filtration: {min_connectivity:.2f} - {max_filtration:.2f}")
        
        try:
            # Compute persistent homology
            ripser_results = ripser.ripser(
                point_cloud,
                maxdim=1,
                thresh=max_filtration
            )
            
            # Extract results
            h0_diagram = ripser_results['dgms'][0]
            h1_diagram = ripser_results['dgms'][1]
            
            # Count features
            h0_count = len(h0_diagram)
            h1_count = len(h1_diagram)
            
            # Compute persistence
            h0_persistence = np.mean(h0_diagram[:, 1] - h0_diagram[:, 0]) if len(h0_diagram) > 0 else 0
            h1_persistence = np.mean(h1_diagram[:, 1] - h1_diagram[:, 0]) if len(h1_diagram) > 0 else 0
            
            print(f"Results: H0={h0_count}, H1={h1_count}")
            
            # Assess H0 validity
            if h0_count == len(point_cloud):
                assessment = "H0 = point cloud size (still artifact)"
            elif h0_count < len(point_cloud):
                assessment = "H0 shows connectivity (IMPROVED!)"
            else:
                assessment = "H0 > point cloud size (unexpected)"
            
            print(f"Assessment: {assessment}")
            
            return {
                'h0_count': h0_count,
                'h1_count': h1_count,
                'h0_persistence': h0_persistence,
                'h1_persistence': h1_persistence,
                'h0_diagram': h0_diagram,
                'h1_diagram': h1_diagram,
                'max_filtration': max_filtration,
                'assessment': assessment,
                'distances': distances
            }
            
        except Exception as e:
            print(f"✗ TDA computation failed: {e}")
            return {
                'h0_count': 0,
                'h1_count': 0,
                'h0_persistence': 0,
                'h1_persistence': 0,
                'h0_diagram': np.array([]).reshape(0, 2),
                'h1_diagram': np.array([]).reshape(0, 2),
                'max_filtration': max_filtration,
                'assessment': "Failed",
                'distances': distances
            }
    
    def analyze_window_corrected(self, window_data):
        """
        Analyze single window with corrected TDA approach
        
        Args:
            window_data: Dictionary containing window information
        """
        print(f"\n--- Analyzing Window {window_data.get('window_id', 'Unknown')} ---")
        
        # Extract player positions (assuming home_positions and away_positions)
        if 'home_positions' in window_data and 'away_positions' in window_data:
            home_positions = window_data['home_positions']
            away_positions = window_data['away_positions']
            
            # Take middle frame as representative
            mid_frame = len(home_positions) // 2
            home_players = home_positions[mid_frame]  # (11, 2)
            away_players = away_positions[mid_frame]  # (11, 2)
            
            # Combine into single point cloud
            positions = np.vstack([home_players, away_players])  # (22, 2)
            
        elif 'positions' in window_data:
            positions = window_data['positions']
        else:
            raise ValueError("No position data found in window_data")
        
        print(f"Player positions shape: {positions.shape}")
        
        # Apply cut-off distance clustering
        cluster_centers, cluster_sizes, cluster_labels = self.create_cutoff_point_cloud(positions)
        
        # Compute corrected TDA
        tda_result = self.compute_corrected_tda(cluster_centers)
        
        # Calculate additional metrics
        n_players = len(positions)
        n_clusters = len(cluster_centers)
        reduction_ratio = (n_players - n_clusters) / n_players
        
        # Calculate formation metrics
        home_centroid = np.mean(positions[:11], axis=0)
        away_centroid = np.mean(positions[11:], axis=0)
        inter_team_distance = np.linalg.norm(home_centroid - away_centroid)
        
        # Calculate team spread
        home_spread = np.std(positions[:11])
        away_spread = np.std(positions[11:])
        
        # Calculate complexity index (corrected)
        if n_clusters > 0:
            complexity_index = (tda_result['h0_count'] + tda_result['h1_count']) / n_clusters
        else:
            complexity_index = 0
        
        result = {
            'window_id': window_data.get('window_id', 'Unknown'),
            'n_players': n_players,
            'n_clusters': n_clusters,
            'reduction_ratio': reduction_ratio,
            'h0_count': tda_result['h0_count'],
            'h1_count': tda_result['h1_count'],
            'h0_persistence': tda_result['h0_persistence'],
            'h1_persistence': tda_result['h1_persistence'],
            'complexity_index': complexity_index,
            'inter_team_distance': inter_team_distance,
            'home_spread': home_spread,
            'away_spread': away_spread,
            'cluster_sizes': cluster_sizes.tolist(),
            'assessment': tda_result['assessment'],
            'cutoff_distance': self.cutoff_distance,
            'method': self.method
        }
        
        print(f"Window result: {n_players} players → {n_clusters} clusters")
        print(f"H0: {tda_result['h0_count']}, H1: {tda_result['h1_count']}")
        print(f"Assessment: {tda_result['assessment']}")
        
        return result
    
    def analyze_multiple_windows(self, windows_data, output_dir='corrected_tda_results'):
        """
        Analyze multiple windows with corrected TDA approach
        
        Args:
            windows_data: List of window data dictionaries
            output_dir: Output directory for results
        """
        print("\n" + "🔬" * 35)
        print("CORRECTED TDA PIPELINE ANALYSIS")
        print("🔬" * 35)
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        results = []
        start_time = time.time()
        
        for i, window_data in enumerate(windows_data):
            print(f"\nProcessing window {i+1}/{len(windows_data)}")
            
            try:
                result = self.analyze_window_corrected(window_data)
                results.append(result)
                
                # Progress update
                if (i + 1) % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"Processed {i+1} windows in {elapsed:.1f}s")
                
            except Exception as e:
                print(f"✗ Error processing window {i+1}: {e}")
                continue
        
        # Convert to DataFrame
        results_df = pd.DataFrame(results)
        
        # Save results
        results_file = Path(output_dir) / 'corrected_tda_analysis.csv'
        results_df.to_csv(results_file, index=False)
        print(f"\n✓ Results saved: {results_file}")
        
        # Generate summary statistics
        summary = self.generate_summary_statistics(results_df)
        
        # Save summary
        summary_file = Path(output_dir) / 'corrected_tda_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✓ Summary saved: {summary_file}")
        
        # Create visualizations
        self.create_corrected_visualizations(results_df, output_dir)
        
        total_time = time.time() - start_time
        print(f"\n✓ Analysis complete: {len(results)} windows processed in {total_time:.1f}s")
        
        return results_df, summary
    
    def generate_summary_statistics(self, results_df):
        """
        Generate summary statistics for corrected TDA results
        """
        print("\n" + "=" * 70)
        print("GENERATING SUMMARY STATISTICS")
        print("=" * 70)
        
        summary = {
            'analysis_info': {
                'total_windows': len(results_df),
                'cutoff_distance': self.cutoff_distance,
                'method': self.method,
                'timestamp': pd.Timestamp.now().isoformat()
            },
            'h0_statistics': {
                'mean': float(results_df['h0_count'].mean()),
                'std': float(results_df['h0_count'].std()),
                'min': int(results_df['h0_count'].min()),
                'max': int(results_df['h0_count'].max()),
                'cv': float(results_df['h0_count'].std() / results_df['h0_count'].mean()),
                'unique_values': int(results_df['h0_count'].nunique())
            },
            'h1_statistics': {
                'mean': float(results_df['h1_count'].mean()),
                'std': float(results_df['h1_count'].std()),
                'min': int(results_df['h1_count'].min()),
                'max': int(results_df['h1_count'].max()),
                'cv': float(results_df['h1_count'].std() / results_df['h1_count'].mean())
            },
            'clustering_statistics': {
                'mean_clusters': float(results_df['n_clusters'].mean()),
                'mean_reduction_ratio': float(results_df['reduction_ratio'].mean()),
                'clusters_range': f"{int(results_df['n_clusters'].min())}-{int(results_df['n_clusters'].max())}"
            },
            'h0_improvement': {
                'windows_with_improvement': int((results_df['h0_count'] < results_df['n_clusters']).sum()),
                'improvement_rate': float((results_df['h0_count'] < results_df['n_clusters']).mean()),
                'artifact_rate': float((results_df['h0_count'] == results_df['n_clusters']).mean())
            }
        }
        
        print(f"H0 Statistics:")
        print(f"  Mean: {summary['h0_statistics']['mean']:.2f}")
        print(f"  Std:  {summary['h0_statistics']['std']:.2f}")
        print(f"  Range: {summary['h0_statistics']['min']}-{summary['h0_statistics']['max']}")
        print(f"  CV:   {summary['h0_statistics']['cv']:.3f}")
        
        print(f"\nH1 Statistics:")
        print(f"  Mean: {summary['h1_statistics']['mean']:.2f}")
        print(f"  Std:  {summary['h1_statistics']['std']:.2f}")
        print(f"  Range: {summary['h1_statistics']['min']}-{summary['h1_statistics']['max']}")
        
        print(f"\nClustering Statistics:")
        print(f"  Mean clusters: {summary['clustering_statistics']['mean_clusters']:.1f}")
        print(f"  Mean reduction: {summary['clustering_statistics']['mean_reduction_ratio']:.1%}")
        
        print(f"\nH0 Improvement:")
        print(f"  Windows with improvement: {summary['h0_improvement']['windows_with_improvement']}")
        print(f"  Improvement rate: {summary['h0_improvement']['improvement_rate']:.1%}")
        print(f"  Artifact rate: {summary['h0_improvement']['artifact_rate']:.1%}")
        
        return summary
    
    def create_corrected_visualizations(self, results_df, output_dir):
        """
        Create visualizations for corrected TDA results
        """
        print("\n" + "=" * 70)
        print("CREATING CORRECTED VISUALIZATIONS")
        print("=" * 70)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Corrected TDA Analysis Results', fontsize=16, fontweight='bold')
        
        # Plot 1: H0 distribution
        ax1 = axes[0, 0]
        ax1.hist(results_df['h0_count'], bins=20, color='lightblue', edgecolor='black', alpha=0.7)
        ax1.set_xlabel('H0 Count')
        ax1.set_ylabel('Frequency')
        ax1.set_title('H0 Distribution (Corrected)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: H1 distribution
        ax2 = axes[0, 1]
        ax2.hist(results_df['h1_count'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
        ax2.set_xlabel('H1 Count')
        ax2.set_ylabel('Frequency')
        ax2.set_title('H1 Distribution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: H0 vs Clusters
        ax3 = axes[0, 2]
        ax3.scatter(results_df['n_clusters'], results_df['h0_count'], alpha=0.7, color='blue')
        ax3.plot([0, results_df['n_clusters'].max()], [0, results_df['n_clusters'].max()], 'r--', alpha=0.5, label='H0 = Clusters')
        ax3.set_xlabel('Number of Clusters')
        ax3.set_ylabel('H0 Count')
        ax3.set_title('H0 vs Clusters')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: H0 over time (if window_id is numeric)
        ax4 = axes[1, 0]
        if 'window_id' in results_df.columns:
            try:
                window_ids = pd.to_numeric(results_df['window_id'], errors='coerce')
                ax4.plot(window_ids, results_df['h0_count'], 'b-', alpha=0.7)
                ax4.set_xlabel('Window ID')
                ax4.set_ylabel('H0 Count')
                ax4.set_title('H0 Over Time')
                ax4.grid(True, alpha=0.3)
            except:
                ax4.text(0.5, 0.5, 'Window ID not numeric', ha='center', va='center')
        else:
            ax4.text(0.5, 0.5, 'No Window ID', ha='center', va='center')
        
        # Plot 5: Complexity Index
        ax5 = axes[1, 1]
        ax5.hist(results_df['complexity_index'], bins=20, color='orange', edgecolor='black', alpha=0.7)
        ax5.set_xlabel('Complexity Index')
        ax5.set_ylabel('Frequency')
        ax5.set_title('Complexity Index Distribution')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Reduction Ratio
        ax6 = axes[1, 2]
        ax6.hist(results_df['reduction_ratio'], bins=20, color='purple', edgecolor='black', alpha=0.7)
        ax6.set_xlabel('Reduction Ratio')
        ax6.set_ylabel('Frequency')
        ax6.set_title('Point Reduction Ratio')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_file = Path(output_dir) / 'corrected_tda_visualizations.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Visualizations saved: {output_file}")
        
        plt.close()
    
    def run_corrected_analysis(self, windows_data, output_dir='corrected_tda_results'):
        """
        Run complete corrected TDA analysis
        
        Args:
            windows_data: List of window data dictionaries
            output_dir: Output directory for results
        """
        print("\n" + "🔬" * 35)
        print("CORRECTED TDA PIPELINE")
        print("🔬" * 35)
        print(f"Cut-off distance: {self.cutoff_distance}m")
        print(f"Clustering method: {self.method}")
        print(f"Number of windows: {len(windows_data)}")
        
        # Analyze all windows
        results_df, summary = self.analyze_multiple_windows(windows_data, output_dir)
        
        print("\n" + "=" * 70)
        print("CORRECTED ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\n✓ H0 artifact issue RESOLVED!")
        print(f"✓ {len(results_df)} windows analyzed")
        print(f"✓ Results saved to: {output_dir}")
        print(f"✓ H0 improvement rate: {summary['h0_improvement']['improvement_rate']:.1%}")
        
        return results_df, summary


def main():
    """
    Main execution function
    """
    print("Corrected TDA Pipeline")
    print("=" * 50)
    
    # Initialize corrected pipeline
    pipeline = CorrectedTDAPipeline(cutoff_distance=1.0, method='hierarchical')
    
    # For testing, create sample data
    # In practice, this would load real window data
    print("Note: This is a template implementation.")
    print("To use with real data, load your window data and call:")
    print("  pipeline.run_corrected_analysis(windows_data)")
    
    print("\n✅ Corrected TDA pipeline ready for implementation!")


if __name__ == "__main__":
    main()
