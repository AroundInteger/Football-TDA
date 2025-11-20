#!/usr/bin/env python3
"""
Full Match Temporal Analysis Visualization
=========================================

This script creates comprehensive visualizations comparing first and second half
TDA results to analyze formation evolution throughout the complete 90-minute match.

Features:
- Temporal evolution of TDA features
- First vs second half comparisons
- Formation complexity analysis
- Team metrics evolution
- Transition detection

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')

class FullMatchTemporalVisualizer:
    """
    Creates comprehensive visualizations for full match temporal analysis
    """
    
    def __init__(self, first_half_dir='first_half_efficient_results', 
                 second_half_dir='second_half_efficient_results'):
        """
        Initialize the visualizer
        
        Args:
            first_half_dir (str): Directory containing first half results
            second_half_dir (str): Directory containing second half results
        """
        self.first_half_dir = Path(first_half_dir)
        self.second_half_dir = Path(second_half_dir)
        
        self.first_half_data = None
        self.second_half_data = None
        self.combined_data = None
        
        print(f"FullMatchTemporalVisualizer initialized")
        print(f"  First half data: {self.first_half_dir}")
        print(f"  Second half data: {self.second_half_dir}")
    
    def load_data(self):
        """
        Load data from both halves
        """
        print("\n=== Loading Data ===")
        
        # Load first half data
        first_half_file = self.first_half_dir / 'efficient_comprehensive_analysis.csv'
        if first_half_file.exists():
            self.first_half_data = pd.read_csv(first_half_file)
            self.first_half_data['half'] = 'First Half'
            print(f"✓ Loaded first half data: {len(self.first_half_data)} windows")
        else:
            print(f"✗ First half data not found: {first_half_file}")
            return False
        
        # Load second half data
        second_half_file = self.second_half_dir / 'efficient_comprehensive_analysis.csv'
        if second_half_file.exists():
            self.second_half_data = pd.read_csv(second_half_file)
            self.second_half_data['half'] = 'Second Half'
            print(f"✓ Loaded second half data: {len(self.second_half_data)} windows")
        else:
            print(f"✗ Second half data not found: {second_half_file}")
            return False
        
        # Combine data
        self.combined_data = pd.concat([self.first_half_data, self.second_half_data], 
                                     ignore_index=True)
        self.combined_data = self.combined_data.sort_values('start_time')
        
        print(f"✓ Combined data: {len(self.combined_data)} total windows")
        print(f"  Time range: {self.combined_data['start_time'].min():.1f} - {self.combined_data['end_time'].max():.1f} minutes")
        
        return True
    
    def create_temporal_evolution_plot(self):
        """
        Create temporal evolution plot showing TDA features over time
        """
        print("\n=== Creating Temporal Evolution Plot ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('TDA Features Evolution Throughout Full Match', fontsize=16, fontweight='bold')
        
        # Plot 1: H0 and H1 features over time
        ax1 = axes[0, 0]
        ax1.plot(self.combined_data['start_time'], self.combined_data['h0_count'], 
                'b-', linewidth=2, label='H0 (Connected Components)', alpha=0.8)
        ax1.plot(self.combined_data['start_time'], self.combined_data['h1_count'], 
                'r-', linewidth=2, label='H1 (Loops/Holes)', alpha=0.8)
        ax1.axvline(x=45, color='gray', linestyle='--', alpha=0.7, label='Half Time')
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Number of Features')
        ax1.set_title('Topological Features Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Complexity index over time
        ax2 = axes[0, 1]
        ax2.plot(self.combined_data['start_time'], self.combined_data['complexity_index'], 
                'g-', linewidth=2, alpha=0.8)
        ax2.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax2.set_xlabel('Time (minutes)')
        ax2.set_ylabel('Complexity Index')
        ax2.set_title('Formation Complexity Over Time')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Inter-team distance over time
        ax3 = axes[1, 0]
        ax3.plot(self.combined_data['start_time'], self.combined_data['avg_inter_team_distance'], 
                'purple', linewidth=2, alpha=0.8)
        ax3.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Time (minutes)')
        ax3.set_ylabel('Inter-team Distance (m)')
        ax3.set_title('Team Separation Over Time')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Team area ratio over time
        ax4 = axes[1, 1]
        ax4.plot(self.combined_data['start_time'], self.combined_data['avg_team_area_ratio'], 
                'orange', linewidth=2, alpha=0.8)
        ax4.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax4.set_xlabel('Time (minutes)')
        ax4.set_ylabel('Team Area Ratio')
        ax4.set_title('Team Formation Area Ratio Over Time')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('full_match_temporal_evolution.png', dpi=300, bbox_inches='tight')
        print("✓ Temporal evolution plot saved: full_match_temporal_evolution.png")
        plt.show()
    
    def create_half_comparison_plot(self):
        """
        Create comparison plot between first and second halves
        """
        print("\n=== Creating Half Comparison Plot ===")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('First Half vs Second Half Comparison', fontsize=16, fontweight='bold')
        
        # Prepare data for comparison
        first_half_metrics = self.first_half_data[['h0_count', 'h1_count', 'total_features', 
                                                  'complexity_index', 'avg_inter_team_distance', 
                                                  'avg_team_area_ratio']]
        second_half_metrics = self.second_half_data[['h0_count', 'h1_count', 'total_features', 
                                                    'complexity_index', 'avg_inter_team_distance', 
                                                    'avg_team_area_ratio']]
        
        metrics = ['h0_count', 'h1_count', 'total_features', 'complexity_index', 
                  'avg_inter_team_distance', 'avg_team_area_ratio']
        titles = ['H0 Features', 'H1 Features', 'Total Features', 'Complexity Index', 
                 'Inter-team Distance', 'Team Area Ratio']
        
        for i, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[i//3, i%3]
            
            # Create box plots
            data_to_plot = [first_half_metrics[metric].values, second_half_metrics[metric].values]
            bp = ax.boxplot(data_to_plot, labels=['First Half', 'Second Half'], patch_artist=True)
            
            # Color the boxes
            bp['boxes'][0].set_facecolor('lightblue')
            bp['boxes'][1].set_facecolor('lightcoral')
            
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            
            # Add statistical comparison
            first_mean = first_half_metrics[metric].mean()
            second_mean = second_half_metrics[metric].mean()
            ax.text(0.5, 0.95, f'First: {first_mean:.2f}\nSecond: {second_mean:.2f}', 
                   transform=ax.transAxes, verticalalignment='top', 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('first_vs_second_half_comparison.png', dpi=300, bbox_inches='tight')
        print("✓ Half comparison plot saved: first_vs_second_half_comparison.png")
        plt.show()
    
    def create_formation_complexity_analysis(self):
        """
        Create detailed formation complexity analysis
        """
        print("\n=== Creating Formation Complexity Analysis ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Formation Complexity Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Complexity distribution by half
        ax1 = axes[0, 0]
        first_complexity = self.first_half_data['complexity_index']
        second_complexity = self.second_half_data['complexity_index']
        
        ax1.hist(first_complexity, bins=20, alpha=0.7, label='First Half', color='lightblue', density=True)
        ax1.hist(second_complexity, bins=20, alpha=0.7, label='Second Half', color='lightcoral', density=True)
        ax1.set_xlabel('Complexity Index')
        ax1.set_ylabel('Density')
        ax1.set_title('Complexity Distribution by Half')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Complexity vs H1 features
        ax2 = axes[0, 1]
        scatter = ax2.scatter(self.combined_data['h1_count'], self.combined_data['complexity_index'], 
                            c=self.combined_data['start_time'], cmap='viridis', alpha=0.7)
        ax2.set_xlabel('H1 Features (Loops/Holes)')
        ax2.set_ylabel('Complexity Index')
        ax2.set_title('Complexity vs H1 Features (colored by time)')
        plt.colorbar(scatter, ax=ax2, label='Time (minutes)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Team metrics correlation
        ax3 = axes[1, 0]
        scatter = ax3.scatter(self.combined_data['avg_inter_team_distance'], 
                            self.combined_data['avg_team_area_ratio'], 
                            c=self.combined_data['complexity_index'], cmap='plasma', alpha=0.7)
        ax3.set_xlabel('Inter-team Distance (m)')
        ax3.set_ylabel('Team Area Ratio')
        ax3.set_title('Team Metrics vs Complexity')
        plt.colorbar(scatter, ax=ax3, label='Complexity Index')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Rolling average complexity
        ax4 = axes[1, 1]
        window_size = 10
        rolling_complexity = self.combined_data['complexity_index'].rolling(window=window_size, center=True).mean()
        ax4.plot(self.combined_data['start_time'], rolling_complexity, 'b-', linewidth=2, alpha=0.8)
        ax4.axvline(x=45, color='gray', linestyle='--', alpha=0.7, label='Half Time')
        ax4.set_xlabel('Time (minutes)')
        ax4.set_ylabel(f'Rolling Average Complexity (window={window_size})')
        ax4.set_title('Smoothed Complexity Evolution')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('formation_complexity_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Formation complexity analysis saved: formation_complexity_analysis.png")
        plt.show()
    
    def create_transition_detection_plot(self):
        """
        Create plot to detect formation transitions
        """
        print("\n=== Creating Transition Detection Plot ===")
        
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))
        fig.suptitle('Formation Transition Detection', fontsize=16, fontweight='bold')
        
        # Calculate differences between consecutive windows
        complexity_diff = np.abs(self.combined_data['complexity_index'].diff())
        h1_diff = np.abs(self.combined_data['h1_count'].diff())
        distance_diff = np.abs(self.combined_data['avg_inter_team_distance'].diff())
        
        # Plot 1: Complexity transitions
        ax1 = axes[0]
        ax1.plot(self.combined_data['start_time'][1:], complexity_diff[1:], 'b-', linewidth=1, alpha=0.8)
        ax1.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax1.set_ylabel('Complexity Change')
        ax1.set_title('Formation Complexity Transitions')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: H1 feature transitions
        ax2 = axes[1]
        ax2.plot(self.combined_data['start_time'][1:], h1_diff[1:], 'r-', linewidth=1, alpha=0.8)
        ax2.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax2.set_ylabel('H1 Features Change')
        ax2.set_title('Topological Structure Transitions')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Team distance transitions
        ax3 = axes[2]
        ax3.plot(self.combined_data['start_time'][1:], distance_diff[1:], 'g-', linewidth=1, alpha=0.8)
        ax3.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Time (minutes)')
        ax3.set_ylabel('Inter-team Distance Change')
        ax3.set_title('Team Positioning Transitions')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('formation_transition_detection.png', dpi=300, bbox_inches='tight')
        print("✓ Transition detection plot saved: formation_transition_detection.png")
        plt.show()
    
    def create_summary_statistics(self):
        """
        Create summary statistics table
        """
        print("\n=== Creating Summary Statistics ===")
        
        # Calculate summary statistics
        summary_stats = {
            'Metric': ['Total Windows', 'Time Coverage (min)', 'Avg H0 Features', 'Avg H1 Features', 
                      'Avg Complexity', 'Avg Inter-team Distance', 'Avg Team Area Ratio',
                      'Max Complexity', 'Min Complexity', 'Complexity Std'],
            'First Half': [
                len(self.first_half_data),
                f"{self.first_half_data['start_time'].min():.1f} - {self.first_half_data['end_time'].max():.1f}",
                f"{self.first_half_data['h0_count'].mean():.1f}",
                f"{self.first_half_data['h1_count'].mean():.1f}",
                f"{self.first_half_data['complexity_index'].mean():.4f}",
                f"{self.first_half_data['avg_inter_team_distance'].mean():.2f}",
                f"{self.first_half_data['avg_team_area_ratio'].mean():.3f}",
                f"{self.first_half_data['complexity_index'].max():.4f}",
                f"{self.first_half_data['complexity_index'].min():.4f}",
                f"{self.first_half_data['complexity_index'].std():.4f}"
            ],
            'Second Half': [
                len(self.second_half_data),
                f"{self.second_half_data['start_time'].min():.1f} - {self.second_half_data['end_time'].max():.1f}",
                f"{self.second_half_data['h0_count'].mean():.1f}",
                f"{self.second_half_data['h1_count'].mean():.1f}",
                f"{self.second_half_data['complexity_index'].mean():.4f}",
                f"{self.second_half_data['avg_inter_team_distance'].mean():.2f}",
                f"{self.second_half_data['avg_team_area_ratio'].mean():.3f}",
                f"{self.second_half_data['complexity_index'].max():.4f}",
                f"{self.second_half_data['complexity_index'].min():.4f}",
                f"{self.second_half_data['complexity_index'].std():.4f}"
            ],
            'Full Match': [
                len(self.combined_data),
                f"{self.combined_data['start_time'].min():.1f} - {self.combined_data['end_time'].max():.1f}",
                f"{self.combined_data['h0_count'].mean():.1f}",
                f"{self.combined_data['h1_count'].mean():.1f}",
                f"{self.combined_data['complexity_index'].mean():.4f}",
                f"{self.combined_data['avg_inter_team_distance'].mean():.2f}",
                f"{self.combined_data['avg_team_area_ratio'].mean():.3f}",
                f"{self.combined_data['complexity_index'].max():.4f}",
                f"{self.combined_data['complexity_index'].min():.4f}",
                f"{self.combined_data['complexity_index'].std():.4f}"
            ]
        }
        
        summary_df = pd.DataFrame(summary_stats)
        
        # Save to CSV
        summary_df.to_csv('full_match_summary_statistics.csv', index=False)
        print("✓ Summary statistics saved: full_match_summary_statistics.csv")
        
        # Display summary
        print("\n" + "="*80)
        print("FULL MATCH TDA ANALYSIS SUMMARY")
        print("="*80)
        print(summary_df.to_string(index=False))
        print("="*80)
        
        return summary_df
    
    def run_complete_analysis(self):
        """
        Run the complete temporal analysis
        """
        print("Full Match Temporal Analysis Visualization")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            print("Failed to load data. Exiting.")
            return
        
        # Create all visualizations
        self.create_temporal_evolution_plot()
        self.create_half_comparison_plot()
        self.create_formation_complexity_analysis()
        self.create_transition_detection_plot()
        
        # Create summary statistics
        summary_df = self.create_summary_statistics()
        
        print("\n=== Analysis Complete ===")
        print("All visualizations and analysis completed successfully!")
        print("Generated files:")
        print("  - full_match_temporal_evolution.png")
        print("  - first_vs_second_half_comparison.png")
        print("  - formation_complexity_analysis.png")
        print("  - formation_transition_detection.png")
        print("  - full_match_summary_statistics.csv")


def main():
    """
    Main function to run the complete temporal analysis
    """
    visualizer = FullMatchTemporalVisualizer()
    visualizer.run_complete_analysis()


if __name__ == "__main__":
    main()
