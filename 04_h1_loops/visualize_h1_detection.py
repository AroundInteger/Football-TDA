#!/usr/bin/env python3
"""
H1 Detection Visualization
===========================

Visualizes H1 (loops/holes) detection across all three scales,
highlighting the adaptive filtration fix and expected results.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import LineCollection

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
    
    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        return None
    
    df = pd.read_csv(results_file)
    return df


def create_h1_temporal_evolution(df):
    """Create temporal evolution plot for H1 across all scales"""
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('H1 (Loops/Holes) Detection: Temporal Evolution Across Scales', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    scales = [
        ('individual', 'Individual Player Scale (2.98m)', colors['individual']),
        ('tactical', 'Tactical Group Scale (12.0m)', colors['tactical']),
        ('team', 'Team Level Scale (28.11m)', colors['team'])
    ]
    
    for idx, (scale, title, color) in enumerate(scales):
        ax = axes[idx]
        
        h1_col = f'h1_{scale}'
        h0_col = f'h0_{scale}'
        
        # Plot H1
        ax.plot(df['timestamp'], df[h1_col], 'o-', 
               color=color, linewidth=2, markersize=5, 
               alpha=0.7, label=f'H1 Count', zorder=3)
        
        # Add zero line for reference
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5, zorder=1)
        
        # Shade regions where H1 > 0 (if any)
        if df[h1_col].max() > 0:
            ax.fill_between(df['timestamp'], 0, df[h1_col], 
                          where=(df[h1_col] > 0), 
                          alpha=0.3, color=color, zorder=2,
                          label='H1 Detection Regions')
        
        # Add H0 in background for context (scaled)
        h0_scaled = df[h0_col] / df[h0_col].max() * df[h1_col].max() * 1.2 if df[h1_col].max() > 0 else df[h0_col] / df[h0_col].max() * 5
        ax_twin = ax.twinx()
        ax_twin.plot(df['timestamp'], df[h0_col], '--', 
                    color='gray', linewidth=1, alpha=0.3, label='H0 (scaled, background)')
        ax_twin.set_ylabel(f'H0 Count (background)', fontsize=9, color='gray')
        ax_twin.tick_params(axis='y', labelsize=8, labelcolor='gray')
        for label in ax_twin.get_yticklabels():
            label.set_alpha(0.5)
        
        # Statistics
        h1_mean = df[h1_col].mean()
        h1_max = df[h1_col].max()
        h1_nonzero = (df[h1_col] > 0).sum()
        h1_pct = 100 * h1_nonzero / len(df)
        
        # Title with statistics
        stat_text = f"Mean: {h1_mean:.2f} | Max: {h1_max:.0f} | Non-zero: {h1_nonzero}/{len(df)} ({h1_pct:.1f}%)"
        ax.set_title(f'{title}\n{stat_text}', fontsize=12, fontweight='bold', pad=10)
        
        ax.set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        ax.set_ylabel('H1 Count (Loops/Holes)', fontsize=10, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3, zorder=1)
        
        # Highlight if H1 = 0 everywhere
        if h1_max == 0:
            ax.text(0.5, 0.5, '⚠️ H1 = 0 (No loops detected)\n\nExpected: H1 > 0 after adaptive filtration fix',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=11, fontweight='bold', color='orange',
                   bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/h1_temporal_evolution.png', 
               dpi=300, bbox_inches='tight')
    print("✅ H1 temporal evolution saved")
    plt.close()


def create_h1_distribution_comparison(df):
    """Create distribution comparison of H1 across scales"""
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('H1 Distribution: Comparison Across Scales', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    scales = [
        ('individual', 'Individual Scale\n(2.98m cut-off)', colors['individual']),
        ('tactical', 'Tactical Scale\n(12.0m cut-off)', colors['tactical']),
        ('team', 'Team Scale\n(28.11m cut-off)', colors['team'])
    ]
    
    for idx, (scale, title, color) in enumerate(scales):
        ax = axes[idx]
        h1_col = f'h1_{scale}'
        
        # Histogram
        values = df[h1_col].values
        unique_vals, counts = np.unique(values, return_counts=True)
        
        bars = ax.bar(unique_vals, counts, color=color, alpha=0.7, 
                     edgecolor='black', linewidth=1.5, width=0.8)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}\n({100*count/len(df):.1f}%)',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Statistics text
        mean_val = values.mean()
        std_val = values.std()
        max_val = values.max()
        nonzero_pct = 100 * (values > 0).sum() / len(values)
        
        stat_text = f'Mean: {mean_val:.2f} ± {std_val:.2f}\nMax: {max_val:.0f}\nNon-zero: {nonzero_pct:.1f}%'
        
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        ax.set_xlabel('H1 Count', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add statistics box
        ax.text(0.98, 0.98, stat_text, transform=ax.transAxes,
               ha='right', va='top', fontsize=9,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor=color, linewidth=2))
        
        # Highlight if all zeros
        if max_val == 0:
            ax.text(0.5, 0.3, '⚠️ H1 = 0\n(All frames)\n\nFix: Adaptive filtration\nExpected: H1 > 0',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=10, fontweight='bold', color='orange',
                   bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/h1_distribution_comparison.png', 
               dpi=300, bbox_inches='tight')
    print("✅ H1 distribution comparison saved")
    plt.close()


def create_h0_h1_relationship(df):
    """Create H0-H1 relationship plots"""
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('H0-H1 Relationship: Understanding Formation Complexity', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    scales = [
        ('individual', 'Individual Scale', colors['individual']),
        ('tactical', 'Tactical Scale', colors['tactical']),
        ('team', 'Team Scale', colors['team'])
    ]
    
    for idx, (scale, title, color) in enumerate(scales):
        ax = axes[idx]
        
        h0_col = f'h0_{scale}'
        h1_col = f'h1_{scale}'
        
        # Scatter plot
        scatter = ax.scatter(df[h0_col], df[h1_col], 
                           alpha=0.6, color=color, s=60, 
                           edgecolors='black', linewidth=0.5, zorder=3)
        
        # Correlation
        correlation = np.corrcoef(df[h0_col], df[h1_col])[0, 1]
        
        # Theoretical relationship line (if H1 were non-zero)
        # H1 typically decreases as H0 increases (fewer components = more connectivity = more loops)
        if not np.isnan(correlation):
            z = np.polyfit(df[h0_col], df[h1_col], 1)
            p = np.poly1d(z)
            x_line = np.linspace(df[h0_col].min(), df[h0_col].max(), 100)
            ax.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, 
                   label=f'Linear fit (r={correlation:.3f})', zorder=2)
        
        ax.set_xlabel('H0 Count (Connected Components)', fontsize=10, fontweight='bold')
        ax.set_ylabel('H1 Count (Loops/Holes)', fontsize=10, fontweight='bold')
        ax.set_title(f'{title}\nCorrelation: r = {correlation:.3f}', 
                    fontsize=12, fontweight='bold', pad=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, zorder=1)
        
        # Highlight if H1 = 0 everywhere
        if df[h1_col].max() == 0:
            ax.text(0.5, 0.5, '⚠️ H1 = 0 (No relationship detectable)\n\nWith adaptive filtration:\nExpected inverse relationship\n(H1 decreases as H0 increases)',
                   transform=ax.transAxes, ha='center', va='center',
                   fontsize=10, fontweight='bold', color='orange',
                   bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/h0_h1_relationship.png', 
               dpi=300, bbox_inches='tight')
    print("✅ H0-H1 relationship plot saved")
    plt.close()


def create_h1_formation_examples():
    """Create schematic examples of H1 detection in formations"""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('H1 Detection: Formation Examples and Loop Visualization', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Row 1: Simple formations (H1 = 0)
    ax1 = axes[0, 0]
    ax1.set_xlim(-1, 11)
    ax1.set_ylim(-1, 11)
    ax1.set_aspect('equal')
    
    # Simple line formation (no loops)
    positions = np.array([[2, 5], [4, 5], [6, 5], [8, 5]])
    for i, (x, y) in enumerate(positions):
        circle = Circle((x, y), 0.4, color=colors['tactical'], alpha=0.8)
        ax1.add_patch(circle)
        ax1.text(x, y, f'G{i+1}', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Connect adjacent
    for i in range(len(positions)-1):
        ax1.plot([positions[i, 0], positions[i+1, 0]], 
                [positions[i, 1], positions[i+1, 1]], 
                'k-', linewidth=2, alpha=0.5)
    
    ax1.set_title('Simple Formation\n(H1 = 0: No loops)', fontsize=12, fontweight='bold')
    ax1.text(5, 1, 'Linear arrangement\n→ No enclosed regions', 
            ha='center', fontsize=10, color='green', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Row 1: Triangle formation (H1 = 1)
    ax2 = axes[0, 1]
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-1, 11)
    ax2.set_aspect('equal')
    
    # Triangular formation (1 loop)
    positions = np.array([[5, 7], [3, 4], [7, 4], [5, 2]])
    for i, (x, y) in enumerate(positions):
        circle = Circle((x, y), 0.4, color=colors['tactical'], alpha=0.8)
        ax2.add_patch(circle)
        ax2.text(x, y, f'G{i+1}', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Connect to form triangle + center
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
    for (i, j) in edges:
        ax2.plot([positions[i, 0], positions[j, 0]], 
                [positions[i, 1], positions[j, 1]], 
                'k-', linewidth=2, alpha=0.5)
    
    # Highlight loop
    triangle = Polygon(positions[:3], fill=True, alpha=0.2, color='red', edgecolor='red', linewidth=2)
    ax2.add_patch(triangle)
    
    ax2.set_title('Complex Formation\n(H1 = 1: One loop detected)', fontsize=12, fontweight='bold')
    ax2.text(5, 1, 'Triangular structure\n→ 1 enclosed region (loop)', 
            ha='center', fontsize=10, color='red', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    # Row 1: Multiple loops (H1 = 2)
    ax3 = axes[0, 2]
    ax3.set_xlim(-1, 11)
    ax3.set_ylim(-1, 11)
    ax3.set_aspect('equal')
    
    # Formation with multiple loops
    positions = np.array([[3, 8], [7, 8], [5, 6], [2, 4], [8, 4], [5, 2]])
    for i, (x, y) in enumerate(positions):
        circle = Circle((x, y), 0.4, color=colors['tactical'], alpha=0.8)
        ax3.add_patch(circle)
        ax3.text(x, y, f'G{i+1}', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Connect to form two triangles
    edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]
    for (i, j) in edges:
        ax3.plot([positions[i, 0], positions[j, 0]], 
                [positions[i, 1], positions[j, 1]], 
                'k-', linewidth=2, alpha=0.5)
    
    # Highlight loops
    triangle1 = Polygon(positions[:3], fill=True, alpha=0.2, color='red', edgecolor='red', linewidth=2)
    triangle2 = Polygon(positions[3:], fill=True, alpha=0.2, color='blue', edgecolor='blue', linewidth=2)
    ax3.add_patch(triangle1)
    ax3.add_patch(triangle2)
    
    ax3.set_title('Very Complex Formation\n(H1 = 2: Multiple loops)', fontsize=12, fontweight='bold')
    ax3.text(5, 1, 'Multiple enclosed regions\n→ 2 loops detected', 
            ha='center', fontsize=10, color='purple', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))
    ax3.set_xticks([])
    ax3.set_yticks([])
    
    # Row 2: Scale-dependent expectations
    for col_idx, (scale, title, color) in enumerate([
        ('individual', 'Individual Scale\n(2.98m cut-off)', colors['individual']),
        ('tactical', 'Tactical Scale\n(12.0m cut-off)', colors['tactical']),
        ('team', 'Team Scale\n(28.11m cut-off)', colors['team'])
    ]):
        ax = axes[1, col_idx]
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 11)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add text explaining expected H1
        if scale == 'tactical':
            text = f'{title}\n\nExpected H1: 1-5 loops\n\nOptimal scale for loop detection\n- Formation structures\n- Tactical groups\n- Midfield shapes'
            bg_color = 'lightblue'
            text_color = 'darkblue'
        elif scale == 'individual':
            text = f'{title}\n\nExpected H1: 0-2 loops\n\nFine-grained scale\n- Most players separate\n- Less loop formation\n- Rare closed structures'
            bg_color = 'lightgreen'
            text_color = 'darkgreen'
        else:  # team
            text = f'{title}\n\nExpected H1: 0-1 loops\n\nCoarse scale\n- Too few points\n- Teams/zones merged\n- Limited geometry'
            bg_color = 'lightcoral'
            text_color = 'darkred'
        
        ax.text(5, 5, text, ha='center', va='center',
               fontsize=11, fontweight='bold', color=text_color,
               bbox=dict(boxstyle='round,pad=1', facecolor=bg_color, alpha=0.8, edgecolor=color, linewidth=3))
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/h1_formation_examples.png', 
               dpi=300, bbox_inches='tight')
    print("✅ H1 formation examples saved")
    plt.close()


def create_adaptive_filtration_explanation(df):
    """Create visualization explaining the adaptive filtration fix"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Adaptive Filtration Fix: Why H1 Detection Failed and How It\'s Fixed', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Panel 1: The Problem
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    problem_text = """THE PROBLEM

Fixed max_filtration = 1.5m was TOO SMALL

After clustering with cut-offs:
• Individual (2.98m): Centroids ~2-3m apart
• Tactical (12.0m): Centroids ~10-15m apart  
• Team (28.11m): Centroids ~20-30m apart

To form loops (H1), filtration must be
LARGE ENOUGH to create triangles.

1.5m filtration → Can't form loops when
points are 10-30m apart!

Result: H1 = 0 at all scales ❌"""
    
    ax1.text(5, 5, problem_text, ha='center', va='center',
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightcoral', alpha=0.8, edgecolor='red', linewidth=3))
    
    ax1.set_title('Problem: Fixed 1.5m Filtration', fontsize=13, fontweight='bold', pad=15)
    
    # Panel 2: The Solution
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    solution_text = """THE SOLUTION

Adaptive Filtration:
• Uses 75th percentile of point cloud distances
• Scale-aware minimum: max(5.0, 2× cut-off)
• Matches previous implementation approach

Expected Filtration Values:
• Individual: ~6m minimum (2× 2.98m)
• Tactical: ~24m minimum (2× 12m) ✅
• Team: ~56m minimum (2× 28.11m)

Result: H1 detection should return! ✅"""
    
    ax2.text(5, 5, solution_text, ha='center', va='center',
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8, edgecolor='green', linewidth=3))
    
    ax2.set_title('Solution: Adaptive Filtration', fontsize=13, fontweight='bold', pad=15)
    
    # Panel 3: Current Results (Before Fix)
    ax3 = axes[1, 0]
    
    scales = ['Individual', 'Tactical', 'Team']
    current_h1 = [df['h1_individual'].mean(), 
                  df['h1_tactical'].mean(), 
                  df['h1_team'].mean()]
    
    bars = ax3.bar(scales, current_h1, color=[colors['individual'], colors['tactical'], colors['team']],
                   alpha=0.7, edgecolor='black', linewidth=2)
    
    for bar, val in zip(bars, current_h1):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{val:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax3.axhline(y=0, color='black', linewidth=1)
    ax3.set_ylabel('H1 Mean', fontsize=11, fontweight='bold')
    ax3.set_title('Current Results (Before Fix)\nH1 = 0 at all scales', 
                 fontsize=12, fontweight='bold', color='red')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Panel 4: Expected Results (After Fix) - Note: Code fixed but not yet re-run
    ax4 = axes[1, 1]
    
    # Check if we have actual results with H1 > 0 (i.e., after re-running with fix)
    has_actual_results = (df['h1_tactical'].max() > 0)
    
    if has_actual_results:
        # Show actual results if available
        actual_h1 = [df['h1_individual'].mean(), 
                     df['h1_tactical'].mean(), 
                     df['h1_team'].mean()]
        actual_std = [df['h1_individual'].std(), 
                      df['h1_tactical'].std(), 
                      df['h1_team'].std()]
        
        bars = ax4.bar(scales, actual_h1, color=[colors['individual'], colors['tactical'], colors['team']],
                       alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add error bars showing standard deviation
        ax4.errorbar(scales, actual_h1, yerr=actual_std, 
                    fmt='none', color='black', linewidth=2, capsize=5, capthick=2)
        
        for bar, val, std in zip(bars, actual_h1, actual_std):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + std + 0.2,
                    f'{val:.2f}\n±{std:.2f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold')
        
        ax4.set_title('Actual Results (After Fix)\nCode fixed and re-run ✅', 
                     fontsize=12, fontweight='bold', color='green')
    else:
        # Show expected results (code fixed but not yet re-run)
        expected_h1 = [0.5, 3.0, 0.2]  # Expected means: Individual (0-2), Tactical (1-5), Team (0-1)
        expected_ranges = [(0, 2), (1, 5), (0, 1)]
        
        bars = ax4.bar(scales, expected_h1, color=[colors['individual'], colors['tactical'], colors['team']],
                       alpha=0.5, edgecolor='black', linewidth=2, linestyle='--')
        
        # Add error bars showing expected ranges
        yerr_lower = [expected_h1[i] - expected_ranges[i][0] for i in range(3)]
        yerr_upper = [expected_ranges[i][1] - expected_h1[i] for i in range(3)]
        ax4.errorbar(scales, expected_h1, yerr=[yerr_lower, yerr_upper], 
                    fmt='none', color='orange', linewidth=2, capsize=5, capthick=2, linestyle='--')
        
        for bar, val, (min_val, max_val) in zip(bars, expected_h1, expected_ranges):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + max_val - val + 0.2,
                    f'{val:.1f}\n[{min_val}-{max_val}]', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold', color='orange')
        
        # Add note that results need to be re-run
        ax4.text(0.5, 0.95, '⚠️ Expected Results\n(Code fixed, analysis not yet re-run)\n\nTo get actual results:\nRun run_comprehensive_multi_goal_analysis.py',
                transform=ax4.transAxes, ha='center', va='top', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8, edgecolor='orange', linewidth=2))
        
        ax4.set_title('Expected Results (After Fix)\nCode fixed but analysis not yet re-run ⏳', 
                     fontsize=12, fontweight='bold', color='orange')
    
    ax4.axhline(y=0, color='black', linewidth=1)
    ax4.set_ylabel('H1 Mean', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('multi_goal_comprehensive_results/h1_adaptive_filtration_fix.png', 
               dpi=300, bbox_inches='tight')
    print("✅ Adaptive filtration explanation saved")
    plt.close()


def main():
    """Main visualization function"""
    print("="*70)
    print("H1 DETECTION VISUALIZATION")
    print("="*70)
    print()
    
    # Load results
    print("📊 Loading results...")
    df = load_results()
    
    if df is None:
        print("❌ Cannot proceed without results data")
        return
    
    print(f"✅ Loaded {len(df)} frames")
    print()
    
    # Create visualizations
    print("📈 Creating H1 visualizations...")
    print()
    
    create_h1_temporal_evolution(df)
    create_h1_distribution_comparison(df)
    create_h0_h1_relationship(df)
    create_h1_formation_examples()
    create_adaptive_filtration_explanation(df)
    
    print()
    print("="*70)
    print("✅ ALL H1 VISUALIZATIONS COMPLETE!")
    print("="*70)
    print()
    print("📁 Generated files:")
    print("  1. h1_temporal_evolution.png - H1 over time (all scales)")
    print("  2. h1_distribution_comparison.png - H1 distributions")
    print("  3. h0_h1_relationship.png - H0-H1 correlations")
    print("  4. h1_formation_examples.png - Schematic examples")
    print("  5. h1_adaptive_filtration_fix.png - Fix explanation")
    print()
    print("💡 Note: Current results show H1 = 0 (before fix)")
    print("   After re-running analysis with adaptive filtration,")
    print("   tactical scale should show H1 > 0 (expected: H1 ~ 3)")
    print()
    print("="*70)


if __name__ == '__main__':
    main()

