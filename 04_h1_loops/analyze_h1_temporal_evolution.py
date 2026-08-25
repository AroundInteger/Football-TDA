#!/usr/bin/env python3
"""
H1 Loops Temporal Evolution Analysis
====================================

Analyzes how H1 loops evolve over time:
- Loop birth/death timelines
- Persistence trends
- Scale interactions
- Formation stability metrics

Author: TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from scipy import stats
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class H1TemporalEvolutionAnalyzer:
    """Analyze temporal evolution of H1 loops"""
    
    def __init__(self, loops_data_file='h1_loop_analysis/h1_loops_full_data.json'):
        """Initialize analyzer with loop data"""
        with open(loops_data_file, 'r') as f:
            self.loops_data = json.load(f)
        
        self.df = pd.DataFrame(self.loops_data)
        self.output_dir = Path('h1_loop_analysis/temporal_analysis')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Loaded {len(self.df)} H1 loops")
        print(f"   Frames: {self.df['frame_idx'].min()} - {self.df['frame_idx'].max()}")
        print(f"   Scales: {self.df['scale'].unique().tolist()}")
    
    def analyze_persistence_over_time(self):
        """Analyze how loop persistence changes over time"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('H1 Loop Persistence Over Time', fontsize=16, fontweight='bold')
        
        scales = ['individual', 'tactical']
        colors = {'individual': 'blue', 'tactical': 'red'}
        
        for idx, scale in enumerate(scales):
            scale_data = self.df[self.df['scale'] == scale].copy()
            scale_data = scale_data.sort_values('frame_idx')
            
            # Plot 1: Persistence vs Frame
            ax1 = axes[idx, 0]
            ax1.scatter(scale_data['frame_idx'], scale_data['persistence'],
                       alpha=0.6, s=50, c=colors[scale], label=scale.capitalize())
            
            # Rolling average
            window = 10
            rolling_mean = scale_data.groupby('frame_idx')['persistence'].mean().rolling(window, center=True).mean()
            ax1.plot(rolling_mean.index, rolling_mean.values, 
                    color='black', linewidth=2, label=f'{window}-frame rolling mean')
            
            ax1.set_xlabel('Frame Index', fontsize=12)
            ax1.set_ylabel('Persistence', fontsize=12)
            ax1.set_title(f'{scale.capitalize()} Scale: Persistence Over Time', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Persistence distribution over time periods
            ax2 = axes[idx, 1]
            n_periods = 5
            period_size = len(scale_data) // n_periods + 1
            
            periods = []
            period_means = []
            for i in range(n_periods):
                period_data = scale_data.iloc[i*period_size:(i+1)*period_size]
                if len(period_data) > 0:
                    periods.append(f'Period {i+1}')
                    period_means.append(period_data['persistence'].mean())
            
            ax2.bar(periods, period_means, color=colors[scale], alpha=0.7)
            ax2.set_ylabel('Mean Persistence', fontsize=12)
            ax2.set_title(f'{scale.capitalize()} Scale: Persistence by Period', fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'persistence_over_time.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
    
    def analyze_loop_lifetimes(self):
        """Analyze loop birth/death patterns"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('H1 Loop Birth/Death Patterns', fontsize=16, fontweight='bold')
        
        scales = ['individual', 'tactical']
        colors = {'individual': 'blue', 'tactical': 'red'}
        
        for idx, scale in enumerate(scales):
            scale_data = self.df[self.df['scale'] == scale].copy()
            
            # Plot 1: Birth vs Death scatter
            ax1 = axes[idx, 0]
            ax1.scatter(scale_data['birth'], scale_data['death'],
                       alpha=0.6, s=50, c=colors[scale])
            
            # Diagonal line (persistence = death - birth)
            max_val = max(scale_data['birth'].max(), scale_data['death'].max())
            ax1.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Death = Birth')
            
            ax1.set_xlabel('Birth Time (filtration distance)', fontsize=12)
            ax1.set_ylabel('Death Time (filtration distance)', fontsize=12)
            ax1.set_title(f'{scale.capitalize()} Scale: Birth vs Death', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Persistence histogram
            ax2 = axes[idx, 1]
            ax2.hist(scale_data['persistence'], bins=30, color=colors[scale], 
                    alpha=0.7, edgecolor='black')
            ax2.axvline(scale_data['persistence'].mean(), color='black', 
                       linestyle='--', linewidth=2, label=f'Mean: {scale_data["persistence"].mean():.2f}')
            ax2.axvline(scale_data['persistence'].median(), color='red', 
                       linestyle='--', linewidth=2, label=f'Median: {scale_data["persistence"].median():.2f}')
            
            ax2.set_xlabel('Persistence', fontsize=12)
            ax2.set_ylabel('Frequency', fontsize=12)
            ax2.set_title(f'{scale.capitalize()} Scale: Persistence Distribution', fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'loop_lifetimes.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
    
    def analyze_loop_density_over_time(self):
        """Analyze number of loops per frame over time"""
        fig, axes = plt.subplots(2, 1, figsize=(16, 10))
        fig.suptitle('H1 Loop Density Over Time', fontsize=16, fontweight='bold')
        
        scales = ['individual', 'tactical']
        colors = {'individual': 'blue', 'tactical': 'red'}
        
        for idx, scale in enumerate(scales):
            scale_data = self.df[self.df['scale'] == scale].copy()
            
            # Count loops per frame
            loops_per_frame = scale_data.groupby('frame_idx').size()
            
            ax = axes[idx]
            ax.bar(loops_per_frame.index, loops_per_frame.values,
                  color=colors[scale], alpha=0.7, width=0.8)
            
            # Rolling average
            window = 10
            rolling_mean = loops_per_frame.rolling(window, center=True).mean()
            ax.plot(rolling_mean.index, rolling_mean.values,
                   color='black', linewidth=2, label=f'{window}-frame rolling mean')
            
            ax.set_xlabel('Frame Index', fontsize=12)
            ax.set_ylabel('Number of Loops', fontsize=12)
            ax.set_title(f'{scale.capitalize()} Scale: Loops Per Frame', fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'loop_density_over_time.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
    
    def analyze_scale_interactions(self):
        """Analyze how individual and tactical loops interact"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Get frames with loops at both scales
        individual_frames = set(self.df[self.df['scale'] == 'individual']['frame_idx'])
        tactical_frames = set(self.df[self.df['scale'] == 'tactical']['frame_idx'])
        
        frames_with_both = sorted(individual_frames & tactical_frames)
        frames_individual_only = sorted(individual_frames - tactical_frames)
        frames_tactical_only = sorted(tactical_frames - individual_frames)
        
        # Count loops per frame for each scale
        individual_counts = self.df[self.df['scale'] == 'individual'].groupby('frame_idx').size()
        tactical_counts = self.df[self.df['scale'] == 'tactical'].groupby('frame_idx').size()
        
        # Plot
        all_frames = sorted(individual_frames | tactical_frames)
        
        ind_values = [individual_counts.get(f, 0) for f in all_frames]
        tac_values = [tactical_counts.get(f, 0) for f in all_frames]
        
        x = np.arange(len(all_frames))
        width = 0.35
        
        ax.bar(x - width/2, ind_values, width, label='Individual', color='blue', alpha=0.7)
        ax.bar(x + width/2, tac_values, width, label='Tactical', color='red', alpha=0.7)
        
        ax.set_xlabel('Frame Index', fontsize=12)
        ax.set_ylabel('Number of Loops', fontsize=12)
        ax.set_title('H1 Loop Density: Individual vs Tactical Scales', fontweight='bold', fontsize=14)
        ax.set_xticks(x[::20])  # Show every 20th frame
        ax.set_xticklabels([all_frames[i] for i in range(0, len(all_frames), 20)])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'scale_interactions.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        # Statistics
        print(f"\n📊 Scale Interaction Statistics:")
        print(f"   Frames with both scales: {len(frames_with_both)}")
        print(f"   Frames with individual only: {len(frames_individual_only)}")
        print(f"   Frames with tactical only: {len(frames_tactical_only)}")
    
    def compute_formation_stability_metrics(self):
        """Compute formation stability metrics based on loop persistence"""
        metrics = {}
        
        for scale in ['individual', 'tactical']:
            scale_data = self.df[self.df['scale'] == scale].copy()
            
            # Frame-level metrics
            frame_metrics = scale_data.groupby('frame_idx').agg({
                'persistence': ['mean', 'std', 'max', 'min', 'count']
            }).reset_index()
            frame_metrics.columns = ['frame_idx', 'mean_persistence', 'std_persistence', 
                                   'max_persistence', 'min_persistence', 'loop_count']
            
            metrics[scale] = {
                'overall_mean_persistence': scale_data['persistence'].mean(),
                'overall_std_persistence': scale_data['persistence'].std(),
                'overall_max_persistence': scale_data['persistence'].max(),
                'total_loops': len(scale_data),
                'frames_with_loops': len(frame_metrics),
                'avg_loops_per_frame': len(scale_data) / max(1, len(frame_metrics)),
                'frame_metrics': frame_metrics
            }
        
        # Save metrics
        metrics_file = self.output_dir / 'formation_stability_metrics.json'
        with open(metrics_file, 'w') as f:
            # Convert DataFrame to dict for JSON serialization
            metrics_serializable = {}
            for scale, data in metrics.items():
                metrics_serializable[scale] = {
                    k: v for k, v in data.items() 
                    if k != 'frame_metrics'
                }
                if 'frame_metrics' in data:
                    metrics_serializable[scale]['frame_metrics'] = data['frame_metrics'].to_dict('records')
            
            json.dump(metrics_serializable, f, indent=2)
        
        print(f"✅ Saved: {metrics_file}")
        
        # Print summary
        print(f"\n📊 Formation Stability Metrics:")
        for scale in ['individual', 'tactical']:
            m = metrics[scale]
            print(f"\n{scale.upper()} Scale:")
            print(f"   Mean persistence: {m['overall_mean_persistence']:.3f} ± {m['overall_std_persistence']:.3f}")
            print(f"   Max persistence: {m['overall_max_persistence']:.3f}")
            print(f"   Total loops: {m['total_loops']}")
            print(f"   Avg loops/frame: {m['avg_loops_per_frame']:.2f}")
        
        return metrics
    
    def generate_temporal_summary_report(self):
        """Generate comprehensive temporal evolution report"""
        report = []
        report.append("="*70)
        report.append("H1 LOOPS TEMPORAL EVOLUTION ANALYSIS")
        report.append("="*70)
        report.append("")
        
        for scale in ['individual', 'tactical']:
            scale_data = self.df[self.df['scale'] == scale].copy()
            
            report.append(f"{scale.upper()} SCALE:")
            report.append("-" * 70)
            report.append(f"  Total loops: {len(scale_data)}")
            report.append(f"  Frames with loops: {len(scale_data['frame_idx'].unique())}")
            report.append(f"  Avg loops per frame: {len(scale_data) / max(1, len(scale_data['frame_idx'].unique())):.2f}")
            report.append(f"  Persistence range: {scale_data['persistence'].min():.3f} - {scale_data['persistence'].max():.3f}")
            report.append(f"  Mean persistence: {scale_data['persistence'].mean():.3f} ± {scale_data['persistence'].std():.3f}")
            report.append(f"  Median persistence: {scale_data['persistence'].median():.3f}")
            report.append("")
            
            # Temporal trends
            scale_data = scale_data.sort_values('frame_idx')
            first_half = scale_data[scale_data['frame_idx'] < scale_data['frame_idx'].median()]
            second_half = scale_data[scale_data['frame_idx'] >= scale_data['frame_idx'].median()]
            
            report.append(f"  Temporal Trends:")
            report.append(f"    First half: Mean persistence = {first_half['persistence'].mean():.3f}")
            report.append(f"    Second half: Mean persistence = {second_half['persistence'].mean():.3f}")
            report.append(f"    Change: {((second_half['persistence'].mean() - first_half['persistence'].mean()) / max(0.001, first_half['persistence'].mean()) * 100):+.1f}%")
            report.append("")
        
        report.append("="*70)
        
        report_text = "\n".join(report)
        report_file = self.output_dir / 'temporal_evolution_report.txt'
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Saved: {report_file}")
        print("\n" + report_text)
    
    def run_full_analysis(self):
        """Run all temporal evolution analyses"""
        print("\n" + "="*70)
        print("H1 LOOPS TEMPORAL EVOLUTION ANALYSIS")
        print("="*70)
        print()
        
        print("📈 Analyzing persistence over time...")
        self.analyze_persistence_over_time()
        
        print("\n📊 Analyzing loop lifetimes...")
        self.analyze_loop_lifetimes()
        
        print("\n📉 Analyzing loop density over time...")
        self.analyze_loop_density_over_time()
        
        print("\n🔗 Analyzing scale interactions...")
        self.analyze_scale_interactions()
        
        print("\n📏 Computing formation stability metrics...")
        self.compute_formation_stability_metrics()
        
        print("\n📝 Generating summary report...")
        self.generate_temporal_summary_report()
        
        print("\n" + "="*70)
        print("✅ TEMPORAL EVOLUTION ANALYSIS COMPLETE!")
        print("="*70)
        print(f"\n📁 Output directory: {self.output_dir}")


if __name__ == '__main__':
    analyzer = H1TemporalEvolutionAnalyzer()
    analyzer.run_full_analysis()

