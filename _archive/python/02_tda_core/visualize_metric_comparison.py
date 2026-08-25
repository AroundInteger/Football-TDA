#!/usr/bin/env python3
"""
Visualize Metric Comparison: Goal-Specific Information Content Metrics
=======================================================================

This script creates comprehensive visualizations comparing the three
refined information content metrics across different cut-off distance ranges.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from cutoff_distance_efficacy_investigation import CutoffDistanceEfficacyInvestigation
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300


def create_comprehensive_metric_comparison():
    """Create comprehensive comparison of all metric types"""
    
    print("="*70)
    print("METRIC COMPARISON VISUALIZATION")
    print("="*70)
    
    # Initialize investigation
    investigator = CutoffDistanceEfficacyInvestigation(
        n_points=200,  # High resolution for smooth curves
        gps_data_file='FieldTest/g2293068_SecondSpectrum_Data.jsonl',
        use_real_data=True
    )
    
    # Load GPS data
    if investigator.load_gps_data() is None:
        print("❌ Failed to load GPS data")
        return
    
    # Get multiple sample windows for robust analysis
    total_frames = len(investigator.gps_data)
    sample_windows = [
        (total_frames // 4, total_frames // 4 + 3000),
        (total_frames // 2, total_frames // 2 + 3000),
        (3 * total_frames // 4, 3 * total_frames // 4 + 3000),
    ]
    
    all_sweeps = []
    
    for i, (start, end) in enumerate(sample_windows):
        print(f"\nProcessing window {i+1}/{len(sample_windows)}: frames {start}-{end}")
        
        positions = investigator.extract_window_positions(start, end)
        
        if positions is None or len(positions) < 10:
            continue
        
        # Sweep full range
        sweep_results = investigator.sweep_cutoff_distances(
            positions,
            cutoff_range=(0.5, 30.0)  # Full range from individual to team level
        )
        
        sweep_results['window_id'] = i
        all_sweeps.append(sweep_results)
    
    if not all_sweeps:
        print("❌ No valid windows found")
        return
    
    # Combine and average across windows
    combined_sweep = pd.concat(all_sweeps, ignore_index=True)
    
    # Group by cut-off distance and average
    avg_sweep = combined_sweep.groupby('cutoff_distance').agg({
        'h0_count': 'mean',
        'h1_count': 'mean',
        'n_clusters': 'mean',
        'information_content': 'mean',
        'information_content_individual': 'mean',
        'information_content_tactical': 'mean',
        'information_content_team': 'mean',
        'silhouette_score': 'mean',
        'calinski_harabasz_score': 'mean',
    }).reset_index()
    
    # Create comprehensive visualization
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: All Information Content Metrics
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(avg_sweep['cutoff_distance'], avg_sweep['information_content'], 
             'b-', label='Default (Original)', linewidth=2.5, alpha=0.7)
    ax1.plot(avg_sweep['cutoff_distance'], avg_sweep['information_content_individual'], 
             'g-', label='Individual Player (0.5-3.0m)', linewidth=2.5)
    ax1.plot(avg_sweep['cutoff_distance'], avg_sweep['information_content_tactical'], 
             'orange', label='Tactical Group (8-15m)', linewidth=2.5)
    ax1.plot(avg_sweep['cutoff_distance'], avg_sweep['information_content_team'], 
             'purple', label='Team Level (15-25m)', linewidth=2.5)
    
    # Highlight optimal regions
    ax1.axvspan(0.5, 3.0, alpha=0.1, color='green', label='Individual Player Region')
    ax1.axvspan(8.0, 15.0, alpha=0.1, color='orange', label='Tactical Group Region')
    ax1.axvspan(15.0, 25.0, alpha=0.1, color='purple', label='Team Level Region')
    
    ax1.set_xlabel('Cut-off Distance (m)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Information Content Score', fontsize=12, fontweight='bold')
    ax1.set_title('Comparison of Goal-Specific Information Content Metrics', 
                  fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 30)
    
    # Plot 2: H0 Count vs Cut-off
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(avg_sweep['cutoff_distance'], avg_sweep['h0_count'], 'b-', linewidth=2.5)
    ax2.axvspan(0.5, 3.0, alpha=0.1, color='green')
    ax2.axvspan(8.0, 15.0, alpha=0.1, color='orange')
    ax2.axvspan(15.0, 25.0, alpha=0.1, color='purple')
    ax2.axhline(22, color='r', linestyle='--', alpha=0.5, label='Artifact (22 players)')
    ax2.axhline(11, color='gray', linestyle=':', alpha=0.5, label='50% threshold')
    ax2.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax2.set_ylabel('H0 Count', fontsize=11, fontweight='bold')
    ax2.set_title('H0 Components vs Cut-off', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 30)
    
    # Plot 3: H1 Count vs Cut-off
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(avg_sweep['cutoff_distance'], avg_sweep['h1_count'], 'r-', linewidth=2.5)
    ax3.axvspan(0.5, 3.0, alpha=0.1, color='green')
    ax3.axvspan(8.0, 15.0, alpha=0.1, color='orange')
    ax3.axvspan(15.0, 25.0, alpha=0.1, color='purple')
    ax3.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax3.set_ylabel('H1 Count', fontsize=11, fontweight='bold')
    ax3.set_title('H1 Features vs Cut-off', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 30)
    
    # Plot 4: Clustering Quality Metrics
    ax4 = fig.add_subplot(gs[1, 2])
    ax4_twin = ax4.twinx()
    
    # Normalize Calinski-Harabasz for visibility (divide by max)
    calinski_max = avg_sweep['calinski_harabasz_score'].max()
    calinski_norm = avg_sweep['calinski_harabasz_score'] / calinski_max if calinski_max > 0 else 0
    
    line1 = ax4.plot(avg_sweep['cutoff_distance'], avg_sweep['silhouette_score'], 
                     'purple', label='Silhouette Score', linewidth=2.5)
    line2 = ax4_twin.plot(avg_sweep['cutoff_distance'], calinski_norm, 
                          'brown', label='Calinski-Harabasz (norm)', linewidth=2.5)
    
    ax4.axvspan(0.5, 3.0, alpha=0.1, color='green')
    ax4.axvspan(8.0, 15.0, alpha=0.1, color='orange')
    ax4.axvspan(15.0, 25.0, alpha=0.1, color='purple')
    
    ax4.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax4.set_ylabel('Silhouette Score', fontsize=11, fontweight='bold', color='purple')
    ax4_twin.set_ylabel('Calinski-Harabasz (normalized)', fontsize=11, fontweight='bold', color='brown')
    ax4.set_title('Clustering Quality Metrics', fontsize=12, fontweight='bold')
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='upper right', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 30)
    
    # Plot 5: Individual Player Metric Zoom (0.5-5.0m)
    ax5 = fig.add_subplot(gs[2, 0])
    zoom_range = (avg_sweep['cutoff_distance'] >= 0.5) & (avg_sweep['cutoff_distance'] <= 5.0)
    zoom_data = avg_sweep[zoom_range]
    
    ax5.plot(zoom_data['cutoff_distance'], zoom_data['information_content_individual'], 
             'g-', linewidth=2.5, label='Individual Player Metric')
    ax5.plot(zoom_data['cutoff_distance'], zoom_data['calinski_harabasz_score'] / calinski_max, 
             'brown', linewidth=2.5, alpha=0.7, label='Calinski-Harabasz (norm)')
    
    # Find optimal
    optimal_idx = zoom_data['information_content_individual'].idxmax()
    optimal_cutoff = zoom_data.loc[optimal_idx, 'cutoff_distance']
    optimal_value = zoom_data.loc[optimal_idx, 'information_content_individual']
    ax5.axvline(optimal_cutoff, color='g', linestyle='--', alpha=0.7, 
                label=f'Optimal: {optimal_cutoff:.2f}m')
    
    ax5.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax5.set_ylabel('Score (normalized)', fontsize=11, fontweight='bold')
    ax5.set_title('Individual Player Region (0.5-5.0m)', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Tactical Group Metric Zoom (5.0-20.0m)
    ax6 = fig.add_subplot(gs[2, 1])
    zoom_range = (avg_sweep['cutoff_distance'] >= 5.0) & (avg_sweep['cutoff_distance'] <= 20.0)
    zoom_data = avg_sweep[zoom_range]
    
    ax6.plot(zoom_data['cutoff_distance'], zoom_data['information_content_tactical'], 
             'orange', linewidth=2.5, label='Tactical Group Metric')
    ax6.plot(zoom_data['cutoff_distance'], zoom_data['silhouette_score'], 
             'purple', linewidth=2.5, alpha=0.7, label='Silhouette Score')
    
    # Find optimal
    optimal_idx = zoom_data['information_content_tactical'].idxmax()
    optimal_cutoff = zoom_data.loc[optimal_idx, 'cutoff_distance']
    optimal_value = zoom_data.loc[optimal_idx, 'information_content_tactical']
    ax6.axvline(optimal_cutoff, color='orange', linestyle='--', alpha=0.7,
                label=f'Optimal: {optimal_cutoff:.2f}m')
    
    ax6.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax6.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax6.set_title('Tactical Group Region (5.0-20.0m)', fontsize=12, fontweight='bold')
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: Team Level Metric Zoom (15.0-30.0m)
    ax7 = fig.add_subplot(gs[2, 2])
    zoom_range = (avg_sweep['cutoff_distance'] >= 15.0) & (avg_sweep['cutoff_distance'] <= 30.0)
    zoom_data = avg_sweep[zoom_range]
    
    ax7.plot(zoom_data['cutoff_distance'], zoom_data['information_content_team'], 
             'purple', linewidth=2.5, label='Team Level Metric')
    ax7.plot(zoom_data['cutoff_distance'], zoom_data['information_content'], 
             'b-', linewidth=2.5, alpha=0.7, label='Default Metric')
    
    # Find optimal
    optimal_idx = zoom_data['information_content_team'].idxmax()
    optimal_cutoff = zoom_data.loc[optimal_idx, 'cutoff_distance']
    optimal_value = zoom_data.loc[optimal_idx, 'information_content_team']
    ax7.axvline(optimal_cutoff, color='purple', linestyle='--', alpha=0.7,
                label=f'Optimal: {optimal_cutoff:.2f}m')
    
    ax7.set_xlabel('Cut-off Distance (m)', fontsize=11)
    ax7.set_ylabel('Information Content', fontsize=11, fontweight='bold')
    ax7.set_title('Team Level Region (15.0-30.0m)', fontsize=12, fontweight='bold')
    ax7.legend(fontsize=9)
    ax7.grid(True, alpha=0.3)
    
    plt.suptitle('Goal-Specific Information Content Metrics: Comprehensive Comparison', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Save figure
    output_dir = Path('cutoff_efficacy_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'metric_comparison_comprehensive.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Also save the averaged data
    avg_sweep.to_csv(output_dir / 'metric_comparison_data.csv', index=False)
    
    print(f"\n✅ Visualization complete!")
    print(f"📊 Saved: {output_dir / 'metric_comparison_comprehensive.png'}")
    print(f"📊 Saved: {output_dir / 'metric_comparison_data.csv'}")
    
    # Print summary statistics
    print("\n" + "="*70)
    print("OPTIMAL CUT-OFF DISTANCES BY METRIC TYPE")
    print("="*70)
    
    for metric_type in ['information_content_individual', 'information_content_tactical', 
                        'information_content_team', 'calinski_harabasz_score', 'silhouette_score']:
        if metric_type in avg_sweep.columns:
            optimal_idx = avg_sweep[metric_type].idxmax()
            optimal_cutoff = avg_sweep.loc[optimal_idx, 'cutoff_distance']
            optimal_value = avg_sweep.loc[optimal_idx, metric_type]
            h0_at_optimal = avg_sweep.loc[optimal_idx, 'h0_count']
            
            print(f"\n{metric_type.replace('_', ' ').title()}:")
            print(f"  Optimal Cut-off: {optimal_cutoff:.3f}m")
            print(f"  Optimal Value: {optimal_value:.4f}")
            print(f"  H0 at Optimal: {h0_at_optimal:.1f}")


if __name__ == "__main__":
    create_comprehensive_metric_comparison()

