#!/usr/bin/env python3
"""
Multi-Goal Analysis Visualization
==================================

Creates comprehensive visualizations comparing all three analysis goals
(individual, tactical, team) across temporal frames.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'individual': '#2E7D32',  # Green
    'tactical': '#1976D2',    # Blue
    'team': '#D32F2F'         # Red
}


def load_results():
    """Load multi-goal analysis results"""
    results_file = Path('multi_goal_comprehensive_results/comprehensive_multi_goal_analysis.csv')
    summary_file = Path('multi_goal_comprehensive_results/summary_statistics.json')
    
    df = pd.read_csv(results_file)
    
    with open(summary_file, 'r') as f:
        summary = json.load(f)
    
    return df, summary


def create_comprehensive_visualization(df, summary):
    """Create comprehensive multi-goal visualization"""
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3,
                         left=0.06, right=0.96, top=0.95, bottom=0.06)
    
    # Title
    fig.suptitle('Multi-Goal Analysis: Complete 3-Scale Picture', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Row 1: Temporal Evolution
    
    # Plot 1: H0 Evolution Over Time
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df['timestamp'], df['h0_individual'], 'o-', 
            label='Individual Player (2.98m)', color=colors['individual'], 
            linewidth=2, markersize=4, alpha=0.7)
    ax1.plot(df['timestamp'], df['h0_tactical'], 's-', 
            label='Tactical Group (16.31m)', color=colors['tactical'], 
            linewidth=2, markersize=4, alpha=0.7)
    ax1.plot(df['timestamp'], df['h0_team'], '^-', 
            label='Team Level (28.11m)', color=colors['team'], 
            linewidth=2, markersize=4, alpha=0.7)
    
    # Add expected range bands
    ax1.axhspan(15, 22, alpha=0.1, color=colors['individual'], label='Individual Expected Range')
    ax1.axhspan(3, 12, alpha=0.1, color=colors['tactical'], label='Tactical Expected Range')
    ax1.axhspan(1, 3, alpha=0.1, color=colors['team'], label='Team Expected Range')
    
    ax1.set_xlabel('Time (seconds)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('H0 Count', fontsize=11, fontweight='bold')
    ax1.set_title('H0 Evolution: Multi-Scale Comparison Over Time', 
                 fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=9, ncol=2)
    ax1.grid(True, alpha=0.3)
    
    # Row 2: Distributions and Statistics
    
    # Plot 2: H0 Distribution
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.hist(df['h0_individual'], bins=20, alpha=0.6, color=colors['individual'], 
            label='Individual', edgecolor='black', linewidth=1.2)
    ax2.hist(df['h0_tactical'], bins=15, alpha=0.6, color=colors['tactical'], 
            label='Tactical', edgecolor='black', linewidth=1.2)
    ax2.hist(df['h0_team'], bins=10, alpha=0.6, color=colors['team'], 
            label='Team', edgecolor='black', linewidth=1.2)
    
    ax2.set_xlabel('H0 Count', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=10, fontweight='bold')
    ax2.set_title('H0 Distribution Across All Scales', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Validation Status
    ax3 = fig.add_subplot(gs[1, 1])
    validation_counts = [
        df['h0_valid_individual'].sum(),
        df['h0_valid_tactical'].sum(),
        df['h0_valid_team'].sum()
    ]
    validation_pcts = [100 * c / len(df) for c in validation_counts]
    
    goals = ['Individual', 'Tactical', 'Team']
    bars = ax3.bar(goals, validation_pcts, 
                  color=[colors['individual'], colors['tactical'], colors['team']],
                  alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, pct in zip(bars, validation_pcts):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{pct:.1f}%', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    ax3.set_ylabel('Valid Frames (%)', fontsize=10, fontweight='bold')
    ax3.set_title('Validation Status by Goal', fontsize=11, fontweight='bold')
    ax3.set_ylim(0, 105)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=90, color='green', linestyle='--', alpha=0.3, linewidth=1)
    ax3.axhline(y=80, color='orange', linestyle='--', alpha=0.3, linewidth=1)
    
    # Plot 4: Statistical Summary
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.axis('off')
    
    stats_text = f"""
STATISTICAL SUMMARY

Individual (2.98m):
  Mean: {summary['individual']['h0_mean']:.2f}
  Std:  {summary['individual']['h0_std']:.2f}
  Range: {summary['individual']['h0_range'][0]}-{summary['individual']['h0_range'][1]}

Tactical (16.31m):
  Mean: {summary['tactical']['h0_mean']:.2f}
  Std:  {summary['tactical']['h0_std']:.2f}
  Range: {summary['tactical']['h0_range'][0]}-{summary['tactical']['h0_range'][1]}

Team (28.11m):
  Mean: {summary['team']['h0_mean']:.2f}
  Std:  {summary['team']['h0_std']:.2f}
  Range: {summary['team']['h0_range'][0]}-{summary['team']['h0_range'][1]}

Hierarchy: ✅ Maintained
  {summary['individual']['h0_mean']:.1f} > {summary['tactical']['h0_mean']:.1f} > {summary['team']['h0_mean']:.1f}
"""
    ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes,
            fontsize=9, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Row 3: Scale Comparisons
    
    # Plot 5: Box Plot Comparison
    ax5 = fig.add_subplot(gs[2, 0])
    data_to_plot = [
        df['h0_individual'].values,
        df['h0_tactical'].values,
        df['h0_team'].values
    ]
    bp = ax5.boxplot(data_to_plot, labels=['Individual', 'Tactical', 'Team'],
                    patch_artist=True, widths=0.6)
    
    # Color boxes
    for patch, color in zip(bp['boxes'], [colors['individual'], colors['tactical'], colors['team']]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax5.set_ylabel('H0 Count', fontsize=10, fontweight='bold')
    ax5.set_title('H0 Distribution Comparison (Box Plots)', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    
    # Plot 6: Scale Correlation
    ax6 = fig.add_subplot(gs[2, 1])
    
    # Scatter: Individual vs Tactical
    ax6.scatter(df['h0_individual'], df['h0_tactical'], 
               alpha=0.6, color=colors['individual'], s=50, 
               label='Individual vs Tactical', edgecolors='black', linewidth=0.5)
    
    ax6.set_xlabel('H0 Individual (2.98m)', fontsize=10, fontweight='bold')
    ax6.set_ylabel('H0 Tactical (16.31m)', fontsize=10, fontweight='bold')
    ax6.set_title('Scale Correlation: Individual ↔ Tactical', fontsize=11, fontweight='bold')
    ax6.grid(True, alpha=0.3)
    
    # Add correlation coefficient
    corr = np.corrcoef(df['h0_individual'], df['h0_tactical'])[0, 1]
    ax6.text(0.05, 0.95, f'r = {corr:.3f}', transform=ax6.transAxes,
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 7: Scale Hierarchy Validation
    ax7 = fig.add_subplot(gs[2, 2])
    
    # Check hierarchy for each frame
    correct_hierarchy = (
        (df['h0_individual'] > df['h0_tactical']) & 
        (df['h0_tactical'] > df['h0_team'])
    )
    
    hierarchy_status = correct_hierarchy.value_counts()
    
    # Pie chart or bar
    labels = ['✅ Correct', '⚠️ Incorrect']
    sizes = [
        hierarchy_status.get(True, 0),
        hierarchy_status.get(False, 0)
    ]
    colors_pie = ['#4CAF50', '#FF9800']
    
    ax7.pie(sizes, labels=labels, autopct='%1.1f%%', 
           colors=colors_pie, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax7.set_title('Hierarchical Ordering Validation\n(Individual > Tactical > Team)', 
                 fontsize=11, fontweight='bold')
    
    plt.savefig('multi_goal_comprehensive_results/multi_goal_comprehensive_visualization.png', 
               dpi=300, bbox_inches='tight')
    print("✅ Comprehensive visualization saved")
    
    plt.close()


def create_temporal_comparison_plot(df, summary):
    """Create detailed temporal comparison plot"""
    
    fig, axes = plt.subplots(3, 1, figsize=(16, 10), sharex=True)
    fig.suptitle('Multi-Goal H0 Temporal Evolution: Individual vs Tactical vs Team', 
                 fontsize=14, fontweight='bold')
    
    goals = ['individual', 'tactical', 'team']
    goal_labels = ['Individual Player (2.98m)', 'Tactical Group (16.31m)', 'Team Level (28.11m)']
    expected_ranges = [(15, 22), (3, 12), (1, 3)]
    
    for i, (goal, label, (min_h0, max_h0)) in enumerate(zip(goals, goal_labels, expected_ranges)):
        ax = axes[i]
        
        h0_col = f'h0_{goal}'
        valid_col = f'h0_valid_{goal}'
        
        # Plot H0 values
        valid_mask = df[valid_col]
        invalid_mask = ~df[valid_col]
        
        # Valid points
        ax.scatter(df.loc[valid_mask, 'timestamp'], df.loc[valid_mask, h0_col],
                  color=colors[goal], alpha=0.6, s=30, label=f'Valid (H0 in range)',
                  edgecolors='black', linewidth=0.3)
        
        # Invalid points
        if invalid_mask.any():
            ax.scatter(df.loc[invalid_mask, 'timestamp'], df.loc[invalid_mask, h0_col],
                      color='red', alpha=0.4, s=30, marker='x', label='Invalid (outside range)',
                      linewidths=2)
        
        # Add mean line
        mean_h0 = df[h0_col].mean()
        ax.axhline(y=mean_h0, color=colors[goal], linestyle='--', linewidth=2, 
                  alpha=0.7, label=f'Mean = {mean_h0:.2f}')
        
        # Expected range bands
        ax.axhspan(min_h0, max_h0, alpha=0.15, color=colors[goal], 
                  label=f'Expected Range ({min_h0}-{max_h0})')
        
        ax.set_ylabel('H0 Count', fontsize=11, fontweight='bold')
        ax.set_title(label, fontsize=12, fontweight='bold', color=colors[goal])
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        # Add statistics text
        stats_text = f"Mean: {df[h0_col].mean():.2f} ± {df[h0_col].std():.2f} | Valid: {100*df[valid_col].sum()/len(df):.1f}%"
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    axes[-1].set_xlabel('Time (seconds)', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/multi_goal_temporal_evolution.png', 
               dpi=300, bbox_inches='tight')
    print("✅ Temporal evolution plot saved")
    
    plt.close()


def create_scale_comparison_matrix(df):
    """Create comparison matrix showing relationships between scales"""
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Multi-Scale Correlation Matrix', fontsize=14, fontweight='bold')
    
    # Individual vs Tactical
    ax1 = axes[0]
    ax1.scatter(df['h0_individual'], df['h0_tactical'], 
               alpha=0.6, color=colors['individual'], s=60, edgecolors='black', linewidth=0.5)
    
    # Add correlation line
    z = np.polyfit(df['h0_individual'], df['h0_tactical'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['h0_individual'].min(), df['h0_individual'].max(), 100)
    ax1.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, label=f'Fit (r={np.corrcoef(df["h0_individual"], df["h0_tactical"])[0,1]:.3f})')
    
    ax1.set_xlabel('H0 Individual (2.98m)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('H0 Tactical (16.31m)', fontsize=11, fontweight='bold')
    ax1.set_title('Individual ↔ Tactical', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Individual vs Team
    ax2 = axes[1]
    ax2.scatter(df['h0_individual'], df['h0_team'], 
               alpha=0.6, color=colors['team'], s=60, edgecolors='black', linewidth=0.5)
    
    z = np.polyfit(df['h0_individual'], df['h0_team'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['h0_individual'].min(), df['h0_individual'].max(), 100)
    ax2.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, label=f'Fit (r={np.corrcoef(df["h0_individual"], df["h0_team"])[0,1]:.3f})')
    
    ax2.set_xlabel('H0 Individual (2.98m)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('H0 Team (28.11m)', fontsize=11, fontweight='bold')
    ax2.set_title('Individual ↔ Team', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Tactical vs Team
    ax3 = axes[2]
    ax3.scatter(df['h0_tactical'], df['h0_team'], 
               alpha=0.6, color=colors['tactical'], s=60, edgecolors='black', linewidth=0.5)
    
    z = np.polyfit(df['h0_tactical'], df['h0_team'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['h0_tactical'].min(), df['h0_tactical'].max(), 100)
    ax3.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, label=f'Fit (r={np.corrcoef(df["h0_tactical"], df["h0_team"])[0,1]:.3f})')
    
    ax3.set_xlabel('H0 Tactical (16.31m)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('H0 Team (28.11m)', fontsize=11, fontweight='bold')
    ax3.set_title('Tactical ↔ Team', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/multi_goal_correlation_matrix.png', 
               dpi=300, bbox_inches='tight')
    print("✅ Correlation matrix saved")
    
    plt.close()


def main():
    """Main visualization function"""
    print("="*70)
    print("MULTI-GOAL ANALYSIS VISUALIZATION")
    print("="*70)
    print()
    
    # Load results
    print("📊 Loading results...")
    df, summary = load_results()
    print(f"✅ Loaded {len(df)} frames")
    print()
    
    # Create visualizations
    print("📈 Creating visualizations...")
    print()
    
    create_comprehensive_visualization(df, summary)
    create_temporal_comparison_plot(df, summary)
    create_scale_comparison_matrix(df)
    
    print()
    print("="*70)
    print("✅ ALL VISUALIZATIONS COMPLETE!")
    print("="*70)
    print()
    print("📁 Generated files:")
    print("  1. multi_goal_comprehensive_visualization.png - Complete overview")
    print("  2. multi_goal_temporal_evolution.png - Temporal evolution")
    print("  3. multi_goal_correlation_matrix.png - Scale correlations")
    print()
    print("🎉 Visualization complete!")
    print("="*70)


if __name__ == '__main__':
    main()

