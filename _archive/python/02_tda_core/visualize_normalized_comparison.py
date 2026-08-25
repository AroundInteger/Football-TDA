#!/usr/bin/env python3
"""
Visualization: Normalized vs. Previous Sampling Comparison

Compares optimal cut-off distances from normalized (30% coverage) 
vs. previous (unequal coverage) sampling strategies.
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

# Previous (unequal coverage) results
previous_results = {
    '1min': {
        'information_content': {'mean': 22.01, 'std': 3.36},
        'silhouette_score': {'mean': 14.97, 'std': 6.02},
        'calinski_harabasz_score': {'mean': 2.81, 'std': 1.67}
    },
    '2min': {
        'information_content': {'mean': 25.68, 'std': 4.53},
        'silhouette_score': {'mean': 14.67, 'std': 3.91},
        'calinski_harabasz_score': {'mean': 2.13, 'std': 0.30}
    },
    '5min': {
        'information_content': {'mean': 22.02, 'std': 0.10},
        'silhouette_score': {'mean': 11.33, 'std': 5.67},
        'calinski_harabasz_score': {'mean': 3.24, 'std': 0.75}
    },
    '10min': {
        'information_content': {'mean': 24.79, 'std': 1.91},
        'silhouette_score': {'mean': 16.89, 'std': 6.77},
        'calinski_harabasz_score': {'mean': 2.89, 'std': 0.94}
    }
}

# Cross-epoch stability (previous)
previous_stability = {
    'information_content': {'mean': 23.62, 'std': 1.64, 'stability': 0.93},
    'silhouette_score': {'mean': 14.46, 'std': 2.00, 'stability': 0.86},
    'calinski_harabasz_score': {'mean': 2.77, 'std': 0.40, 'stability': 0.85}
}

# Load normalized (30% coverage) results
normalized_file = Path('cutoff_efficacy_results/investigation_summary.json')
with open(normalized_file, 'r') as f:
    normalized_data = json.load(f)

normalized_results = normalized_data['cross_epoch_analysis']['optimal_cutoffs_by_epoch']
normalized_stability = normalized_data['cross_epoch_analysis']['temporal_patterns']

# Epoch order
epochs = ['1min', '2min', '5min', '10min']
epoch_labels = ['1 min', '2 min', '5 min', '10 min']
metrics = ['information_content', 'silhouette_score', 'calinski_harabasz_score']
metric_labels = ['Information Content', 'Silhouette Score', 'Calinski-Harabasz']
metric_short = ['Info Content', 'Silhouette', 'Calinski-Harabasz']

# Create comprehensive comparison figure
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3, 
                      left=0.06, right=0.96, top=0.94, bottom=0.06)

# Color scheme
colors = {
    'previous': '#8B7355',  # Brownish
    'normalized': '#2E7D32',  # Green
    'stability': '#1976D2'  # Blue
}

# 1. Per-epoch comparison for each metric
for i, (metric, metric_label) in enumerate(zip(metrics, metric_labels)):
    ax = fig.add_subplot(gs[i, 0])
    
    # Previous values
    prev_means = [previous_results[ep][metric]['mean'] for ep in epochs]
    prev_stds = [previous_results[ep][metric]['std'] for ep in epochs]
    
    # Normalized values
    norm_means = [normalized_results[ep][metric]['mean'] for ep in epochs]
    norm_stds = [normalized_results[ep][metric]['std'] for ep in epochs]
    
    x = np.arange(len(epochs))
    width = 0.35
    
    # Plot bars
    bars1 = ax.bar(x - width/2, prev_means, width, yerr=prev_stds,
                   label='Previous (Unequal Coverage)', color=colors['previous'],
                   alpha=0.7, capsize=4)
    bars2 = ax.bar(x + width/2, norm_means, width, yerr=norm_stds,
                   label='Normalized (30% Coverage)', color=colors['normalized'],
                   alpha=0.7, capsize=4)
    
    ax.set_xlabel('Temporal Epoch', fontsize=10, fontweight='bold')
    ax.set_ylabel('Optimal Cut-off (m)', fontsize=10, fontweight='bold')
    ax.set_title(f'{metric_label}\nPer-Epoch Comparison', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(epoch_labels, fontsize=9)
    ax.legend(fontsize=8, loc='best')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=7)

# 2. Cross-epoch stability comparison
stability_ax = fig.add_subplot(gs[0, 1])
metrics_stability = ['information_content', 'silhouette_score', 'calinski_harabasz_score']

prev_stability_vals = [previous_stability[m]['stability'] for m in metrics_stability]
norm_stability_vals = [normalized_stability[m]['temporal_stability'] for m in metrics_stability]

x = np.arange(len(metric_short))
width = 0.35

bars1 = stability_ax.bar(x - width/2, prev_stability_vals, width,
                        label='Previous', color=colors['previous'], alpha=0.7)
bars2 = stability_ax.bar(x + width/2, norm_stability_vals, width,
                        label='Normalized', color=colors['normalized'], alpha=0.7)

stability_ax.set_xlabel('Metric', fontsize=10, fontweight='bold')
stability_ax.set_ylabel('Temporal Stability', fontsize=10, fontweight='bold')
stability_ax.set_title('Temporal Stability Comparison\n(Cross-Epoch Consistency)', 
                      fontsize=11, fontweight='bold')
stability_ax.set_xticks(x)
stability_ax.set_xticklabels(metric_short, fontsize=8, rotation=15, ha='right')
stability_ax.legend(fontsize=8)
stability_ax.set_ylim(0.75, 1.0)
stability_ax.grid(True, alpha=0.3, axis='y')
stability_ax.axhline(y=0.95, color='green', linestyle='--', alpha=0.3, linewidth=1)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        stability_ax.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.2f}', ha='center', va='bottom', fontsize=8)

# 3. Cross-epoch mean comparison
mean_ax = fig.add_subplot(gs[1, 1])
prev_means_cross = [previous_stability[m]['mean'] for m in metrics_stability]
prev_stds_cross = [previous_stability[m]['std'] for m in metrics_stability]
norm_means_cross = [normalized_stability[m]['mean'] for m in metrics_stability]
norm_stds_cross = [normalized_stability[m]['std'] for m in metrics_stability]

bars1 = mean_ax.bar(x - width/2, prev_means_cross, width, yerr=prev_stds_cross,
                   label='Previous', color=colors['previous'], alpha=0.7, capsize=4)
bars2 = mean_ax.bar(x + width/2, norm_means_cross, width, yerr=norm_stds_cross,
                   label='Normalized', color=colors['normalized'], alpha=0.7, capsize=4)

mean_ax.set_xlabel('Metric', fontsize=10, fontweight='bold')
mean_ax.set_ylabel('Mean Optimal Cut-off (m)', fontsize=10, fontweight='bold')
mean_ax.set_title('Cross-Epoch Mean Comparison\n(Tighter Confidence Intervals)', 
                 fontsize=11, fontweight='bold')
mean_ax.set_xticks(x)
mean_ax.set_xticklabels(metric_short, fontsize=8, rotation=15, ha='right')
mean_ax.legend(fontsize=8)
mean_ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        mean_ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=8)

# 4. Standard deviation comparison (variability)
std_ax = fig.add_subplot(gs[2, 1])
prev_stds_only = [previous_stability[m]['std'] for m in metrics_stability]
norm_stds_only = [normalized_stability[m]['std'] for m in metrics_stability]

bars1 = std_ax.bar(x - width/2, prev_stds_only, width,
                  label='Previous', color=colors['previous'], alpha=0.7)
bars2 = std_ax.bar(x + width/2, norm_stds_only, width,
                  label='Normalized', color=colors['normalized'], alpha=0.7)

std_ax.set_xlabel('Metric', fontsize=10, fontweight='bold')
std_ax.set_ylabel('Cross-Epoch Std Dev (m)', fontsize=10, fontweight='bold')
std_ax.set_title('Variability Reduction\n(Lower = More Consistent)', 
                fontsize=11, fontweight='bold')
std_ax.set_xticks(x)
std_ax.set_xticklabels(metric_short, fontsize=8, rotation=15, ha='right')
std_ax.legend(fontsize=8)
std_ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        std_ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}', ha='center', va='bottom', fontsize=8)

# 5. Sampling coverage comparison
coverage_ax = fig.add_subplot(gs[0, 2])
previous_windows = [5, 5, 4, 4]
normalized_windows = [31, 16, 7, 4]
previous_coverage = [5.0, 9.3, 20.0, 40.0]
normalized_coverage = [31.0, 32.0, 35.0, 39.9]

x_ep = np.arange(len(epoch_labels))
bars1 = coverage_ax.bar(x_ep - width/2, previous_coverage, width,
                       label='Previous', color=colors['previous'], alpha=0.7)
bars2 = coverage_ax.bar(x_ep + width/2, normalized_coverage, width,
                       label='Normalized', color=colors['normalized'], alpha=0.7)

coverage_ax.set_xlabel('Temporal Epoch', fontsize=10, fontweight='bold')
coverage_ax.set_ylabel('Coverage (%)', fontsize=10, fontweight='bold')
coverage_ax.set_title('Sampling Coverage Comparison\n(Normalized = Equal Coverage)', 
                     fontsize=11, fontweight='bold')
coverage_ax.set_xticks(x_ep)
coverage_ax.set_xticklabels(epoch_labels, fontsize=9)
coverage_ax.legend(fontsize=8)
coverage_ax.grid(True, alpha=0.3, axis='y')
coverage_ax.axhline(y=30, color='green', linestyle='--', alpha=0.3, linewidth=1, label='30% Target')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        coverage_ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=7)

# 6. Total windows comparison
windows_ax = fig.add_subplot(gs[1, 2])
total_prev = sum(previous_windows)
total_norm = sum(normalized_windows)

bars = windows_ax.bar(['Previous\n(Unequal)', 'Normalized\n(30% Coverage)'], 
                     [total_prev, total_norm],
                     color=[colors['previous'], colors['normalized']], alpha=0.7)

windows_ax.set_ylabel('Total Windows Analyzed', fontsize=10, fontweight='bold')
windows_ax.set_title('Sample Size Comparison\n(More Robust Validation)', 
                    fontsize=11, fontweight='bold')
windows_ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars:
    height = bar.get_height()
    windows_ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 7. Improvement summary
improve_ax = fig.add_subplot(gs[2, 2])
improve_ax.axis('off')

improvements = [
    ('Temporal Stability', 'Information Content', '0.93 → 0.98', '+5.4%'),
    ('Temporal Stability', 'Silhouette Score', '0.86 → 0.97', '+12.8%'),
    ('Temporal Stability', 'Calinski-Harabasz', '0.85 → 0.88', '+3.5%'),
    ('Cross-Epoch Std', 'Information Content', '±1.64m → ±0.47m', '-71%'),
    ('Cross-Epoch Std', 'Silhouette Score', '±2.00m → ±0.52m', '-74%'),
    ('Total Windows', 'Sample Size', '18 → 58', '+222%'),
]

text_y = 0.95
improve_ax.text(0.05, text_y, 'KEY IMPROVEMENTS', fontsize=12, fontweight='bold',
               transform=improve_ax.transAxes)
text_y -= 0.15

improve_ax.text(0.05, text_y, 'Metric', fontsize=9, fontweight='bold',
               transform=improve_ax.transAxes)
improve_ax.text(0.35, text_y, 'Change', fontsize=9, fontweight='bold',
               transform=improve_ax.transAxes)
improve_ax.text(0.70, text_y, 'Improvement', fontsize=9, fontweight='bold',
               transform=improve_ax.transAxes)
text_y -= 0.03
# Draw separator line
from matplotlib.patches import Rectangle
line = Rectangle((0.05, text_y-0.01), 0.90, 0.002, 
                transform=improve_ax.transAxes, 
                facecolor='black', edgecolor='none')
improve_ax.add_patch(line)
text_y -= 0.08

for category, metric, change, improvement in improvements:
    if category == 'Total Windows':
        improve_ax.text(0.05, text_y, metric, fontsize=8,
                       transform=improve_ax.transAxes, style='italic')
    else:
        improve_ax.text(0.05, text_y, f'{metric}', fontsize=8,
                       transform=improve_ax.transAxes)
    improve_ax.text(0.35, text_y, change, fontsize=8,
                   transform=improve_ax.transAxes, family='monospace')
    improve_ax.text(0.70, text_y, improvement, fontsize=8,
                   transform=improve_ax.transAxes, color='green', fontweight='bold')
    text_y -= 0.10

# Main title
fig.suptitle('Normalized vs. Previous Sampling: Comprehensive Comparison', 
            fontsize=14, fontweight='bold', y=0.98)

# Save figure
output_dir = Path('cutoff_efficacy_results')
output_dir.mkdir(exist_ok=True)
output_file = output_dir / 'normalized_vs_previous_comparison.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ Comparison visualization saved: {output_file}")

plt.close()

