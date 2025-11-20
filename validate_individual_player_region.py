#!/usr/bin/env python3
"""
Validate Individual Player Region (0.5-3.0m Cut-off Range)
==========================================================

This script validates the individual player analysis region by running
a focused sweep in the 0.5-3.0m range with finer resolution to confirm
optimal cut-off distances for individual player identification.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from cutoff_distance_efficacy_investigation import CutoffDistanceEfficacyInvestigation


def validate_individual_player_region():
    """Validate individual player region with focused analysis"""
    
    print("="*70)
    print("INDIVIDUAL PLAYER REGION VALIDATION (0.5-3.0m)")
    print("="*70)
    
    # Initialize investigation with real GPS data
    investigator = CutoffDistanceEfficacyInvestigation(
        n_points=50,  # Finer resolution for focused range
        gps_data_file='FieldTest/g2293068_SecondSpectrum_Data.jsonl',
        use_real_data=True
    )
    
    # Load GPS data
    if investigator.load_gps_data() is None:
        print("❌ Failed to load GPS data")
        return
    
    # Get a sample window for detailed analysis
    total_frames = len(investigator.gps_data)
    sample_start = total_frames // 2  # Middle of match
    sample_end = sample_start + 3000  # 2-minute window
    
    print(f"\nAnalyzing sample window: frames {sample_start}-{sample_end}")
    
    # Extract positions
    positions = investigator.extract_window_positions(sample_start, sample_end)
    
    if positions is None or len(positions) < 10:
        print("❌ Insufficient data")
        return
    
    print(f"✅ Extracted {len(positions)} player positions")
    
    # Focused sweep in individual player region
    print("\nRunning focused sweep in 0.5-3.0m range...")
    
    sweep_results = investigator.sweep_cutoff_distances(
        positions, 
        cutoff_range=(0.5, 3.0)
    )
    
    # Analyze results
    print("\n" + "="*70)
    print("INDIVIDUAL PLAYER REGION ANALYSIS")
    print("="*70)
    
    # Find optima for individual player metric
    optima_individual = investigator.find_optimal_cutoff(
        sweep_results, 
        'information_content_individual'
    )
    
    optima_calinski = investigator.find_optimal_cutoff(
        sweep_results,
        'calinski_harabasz_score'
    )
    
    print(f"\nOptimal Cut-offs for Individual Player Analysis:")
    print(f"  Information Content (individual): {optima_individual['optimal_cutoff']:.3f}m")
    print(f"  Calinski-Harabasz Score: {optima_calinski['optimal_cutoff']:.3f}m")
    
    # Extract H0/H1 at optimal cut-offs
    optimal_row = sweep_results.loc[optima_individual['optimal_idx']]
    print(f"\nAt Optimal Cut-off ({optima_individual['optimal_cutoff']:.3f}m):")
    print(f"  H0 Count: {optimal_row['h0_count']:.0f}")
    print(f"  H1 Count: {optimal_row['h1_count']:.0f}")
    print(f"  N Clusters: {optimal_row['n_clusters']:.0f}")
    print(f"  Information Content: {optimal_row['information_content_individual']:.4f}")
    
    # Check H0 range
    h0_range = (sweep_results['h0_count'].min(), sweep_results['h0_count'].max())
    print(f"\nH0 Range in 0.5-3.0m region: {h0_range[0]:.0f} - {h0_range[1]:.0f}")
    
    # Validate expected range (15-22 for 22 players)
    original_size = len(positions)
    expected_range = (original_size * 0.5, original_size * 0.95)
    print(f"Expected H0 Range (50%-95% of {original_size}): {expected_range[0]:.0f} - {expected_range[1]:.0f}")
    
    # Check if we're in expected range
    in_range = expected_range[0] <= optimal_row['h0_count'] <= expected_range[1]
    print(f"\n✅ Validation: H0 in expected range = {in_range}")
    
    # Create focused visualization
    output_dir = Path('cutoff_efficacy_results/individual_player_validation')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Individual Player Region Validation (0.5-3.0m)', fontsize=14, fontweight='bold')
    
    # Plot 1: H0 vs Cut-off
    ax1 = axes[0, 0]
    ax1.plot(sweep_results['cutoff_distance'], sweep_results['h0_count'], 'b-', linewidth=2)
    ax1.axvline(optima_individual['optimal_cutoff'], color='g', linestyle='--', label='Optimal (info)')
    ax1.axvline(optima_calinski['optimal_cutoff'], color='orange', linestyle='--', label='Optimal (Calinski)')
    ax1.axhline(expected_range[0], color='r', linestyle=':', alpha=0.5, label='Expected min')
    ax1.axhline(expected_range[1], color='r', linestyle=':', alpha=0.5, label='Expected max')
    ax1.set_xlabel('Cut-off Distance (m)')
    ax1.set_ylabel('H0 Count')
    ax1.set_title('H0 vs Cut-off Distance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Information Content Metrics
    ax2 = axes[0, 1]
    ax2.plot(sweep_results['cutoff_distance'], sweep_results['information_content_individual'], 
             'g-', label='Individual Player', linewidth=2)
    ax2.plot(sweep_results['cutoff_distance'], sweep_results['information_content_tactical'], 
             'orange', label='Tactical Group', linewidth=2, alpha=0.7)
    ax2.plot(sweep_results['cutoff_distance'], sweep_results['information_content_team'], 
             'purple', label='Team Level', linewidth=2, alpha=0.7)
    ax2.axvline(optima_individual['optimal_cutoff'], color='g', linestyle='--')
    ax2.set_xlabel('Cut-off Distance (m)')
    ax2.set_ylabel('Information Content')
    ax2.set_title('Goal-Specific Information Content')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Calinski-Harabasz Score
    ax3 = axes[1, 0]
    ax3.plot(sweep_results['cutoff_distance'], sweep_results['calinski_harabasz_score'], 
             'purple', linewidth=2)
    ax3.axvline(optima_calinski['optimal_cutoff'], color='orange', linestyle='--')
    ax3.set_xlabel('Cut-off Distance (m)')
    ax3.set_ylabel('Calinski-Harabasz Score')
    ax3.set_title('Cluster Separation Quality')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: H1 Count
    ax4 = axes[1, 1]
    ax4.plot(sweep_results['cutoff_distance'], sweep_results['h1_count'], 'r-', linewidth=2)
    ax4.axvline(optima_individual['optimal_cutoff'], color='g', linestyle='--')
    ax4.set_xlabel('Cut-off Distance (m)')
    ax4.set_ylabel('H1 Count')
    ax4.set_title('Topological Complexity (H1)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'individual_player_region_validation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save results
    sweep_results.to_csv(output_dir / 'individual_player_sweep_results.csv', index=False)
    
    # Create summary
    summary = f"""# Individual Player Region Validation

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Range Analyzed**: 0.5-3.0m  
**Resolution**: 50 points

## Results

### Optimal Cut-offs
- **Information Content (Individual)**: {optima_individual['optimal_cutoff']:.3f}m
- **Calinski-Harabasz Score**: {optima_calinski['optimal_cutoff']:.3f}m

### H0 Characteristics at Optimal Cut-off
- **H0 Count**: {optimal_row['h0_count']:.0f}
- **H1 Count**: {optimal_row['h1_count']:.0f}
- **N Clusters**: {optimal_row['n_clusters']:.0f}
- **H0 Ratio**: {optimal_row['h0_count']/original_size:.2f} ({optimal_row['h0_count']/original_size*100:.0f}% of {original_size} players)

### Validation
- **Expected H0 Range**: {expected_range[0]:.0f}-{expected_range[1]:.0f} ({expected_range[0]/original_size:.0%}-{expected_range[1]/original_size:.0%} of players)
- **H0 in Expected Range**: {'✅ YES' if in_range else '❌ NO'}
- **Actual H0 Range in Region**: {h0_range[0]:.0f}-{h0_range[1]:.0f}

## Conclusion

{'✅ VALIDATED: Individual player region (0.5-3.0m) produces H0 in expected range' if in_range else '⚠️ REVIEW NEEDED: H0 outside expected range'}

**Recommended Cut-off for Individual Player Analysis**: {optima_individual['optimal_cutoff']:.2f}m - {optima_calinski['optimal_cutoff']:.2f}m

"""
    
    with open(output_dir / 'validation_summary.md', 'w') as f:
        f.write(summary)
    
    print(f"\n✅ Validation complete!")
    print(f"📊 Results saved: {output_dir}")
    print(f"\n{'✅ VALIDATED' if in_range else '⚠️ REVIEW NEEDED'}: Individual player region produces expected H0 range")


if __name__ == "__main__":
    validate_individual_player_region()

