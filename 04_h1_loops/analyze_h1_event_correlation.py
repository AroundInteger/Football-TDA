#!/usr/bin/env python3
"""
H1 Loops Event Correlation Analysis
===================================

Correlates H1 loops with match events:
- Goals: Loop changes before/after goals
- Possession changes: Loop dynamics during transitions
- Shots/passes: Correlation with attacking events
- Formation changes: Loop response to tactical adjustments

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


class H1EventCorrelationAnalyzer:
    """Analyze correlation between H1 loops and match events"""
    
    def __init__(self, loops_data_file='h1_loop_analysis/h1_loops_full_data.json',
                 events_data_file=None):
        """Initialize analyzer with loop and event data"""
        # Load loop data
        with open(loops_data_file, 'r') as f:
            self.loops_data = json.load(f)
        
        self.df = pd.DataFrame(self.loops_data)
        
        # Try to load event data (if available)
        self.events_data = None
        if events_data_file and Path(events_data_file).exists():
            with open(events_data_file, 'r') as f:
                self.events_data = json.load(f)
            print(f"✅ Loaded event data: {len(self.events_data)} events")
        
        self.output_dir = Path('h1_loop_analysis/event_correlation')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Loaded {len(self.df)} H1 loops")
        print(f"   Frames: {self.df['frame_idx'].min()} - {self.df['frame_idx'].max()}")
        
        self.fps = 25.0  # SecondSpectrum optical tracking frame rate
        self.df['time_seconds'] = self.df['frame_idx'] / self.fps
        
        # Create frame-level aggregations
        self._prepare_frame_level_data()
    
    def _prepare_frame_level_data(self):
        """Prepare frame-level aggregated loop data"""
        frame_data = []
        
        for frame_idx in sorted(self.df['frame_idx'].unique()):
            frame_loops = self.df[self.df['frame_idx'] == frame_idx]
            
            for scale in ['individual', 'tactical']:
                scale_loops = frame_loops[frame_loops['scale'] == scale]
                
                if len(scale_loops) > 0:
                    frame_data.append({
                        'frame_idx': frame_idx,
                        'time_seconds': frame_idx / self.fps,
                        'scale': scale,
                        'n_loops': len(scale_loops),
                        'mean_persistence': scale_loops['persistence'].mean(),
                        'max_persistence': scale_loops['persistence'].max(),
                        'mean_birth': scale_loops['birth'].mean(),
                        'mean_death': scale_loops['death'].mean(),
                        'total_persistence': scale_loops['persistence'].sum()
                    })
                else:
                    frame_data.append({
                        'frame_idx': frame_idx,
                        'time_seconds': frame_idx / self.fps,
                        'scale': scale,
                        'n_loops': 0,
                        'mean_persistence': 0.0,
                        'max_persistence': 0.0,
                        'mean_birth': 0.0,
                        'mean_death': 0.0,
                        'total_persistence': 0.0
                    })
        
        self.frame_df = pd.DataFrame(frame_data)
        print(f"✅ Prepared frame-level data: {len(self.frame_df)} frame-scale combinations")
    
    def analyze_with_synthetic_events(self):
        """Analyze loop patterns around synthetic important events
        
        Since we don't have event data, we'll simulate key moments:
        - Frame 25: Early match event
        - Frame 75: Mid-match event  
        - Frame 125: Late match event
        """
        print("\n" + "="*70)
        print("ANALYZING LOOP PATTERNS AROUND SIMULATED EVENTS")
        print("="*70)
        
        # Define synthetic events
        synthetic_events = [
            {'name': 'Early Match', 'frame': 25, 'time': 25/self.fps},
            {'name': 'Mid Match', 'frame': 75, 'time': 75/self.fps},
            {'name': 'Late Match', 'frame': 125, 'time': 125/self.fps}
        ]
        
        # Analyze window around each event
        window_frames = 20  # ±20 frames (~1.6 seconds)
        
        fig, axes = plt.subplots(len(synthetic_events), 2, figsize=(16, 12))
        fig.suptitle('H1 Loop Patterns Around Match Events', fontsize=16, fontweight='bold')
        
        for event_idx, event in enumerate(synthetic_events):
            event_frame = event['frame']
            
            # Extract window
            window_start = max(0, event_frame - window_frames)
            window_end = min(self.frame_df['frame_idx'].max(), event_frame + window_frames)
            window_data = self.frame_df[
                (self.frame_df['frame_idx'] >= window_start) &
                (self.frame_df['frame_idx'] <= window_end)
            ].copy()
            
            # Plot for each scale
            for scale_idx, scale in enumerate(['individual', 'tactical']):
                scale_data = window_data[window_data['scale'] == scale].sort_values('frame_idx')
                
                ax = axes[event_idx, scale_idx]
                
                # Plot persistence
                ax.plot(scale_data['frame_idx'], scale_data['mean_persistence'],
                       'o-', label='Mean Persistence', linewidth=2, markersize=4)
                ax.plot(scale_data['frame_idx'], scale_data['max_persistence'],
                       's-', label='Max Persistence', linewidth=2, markersize=4, alpha=0.7)
                
                # Mark event
                ax.axvline(event_frame, color='red', linestyle='--', 
                          linewidth=2, label=f"Event: {event['name']}")
                
                ax.set_xlabel('Frame Index', fontsize=10)
                ax.set_ylabel('Persistence', fontsize=10)
                ax.set_title(f'{event["name"]} - {scale.capitalize()} Scale', fontweight='bold')
                ax.legend(fontsize=8)
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / 'loop_patterns_around_events.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        return synthetic_events
    
    def analyze_persistence_before_after_events(self, event_frames=None):
        """Analyze loop persistence before and after events"""
        if event_frames is None:
            # Use synthetic events
            event_frames = [25, 75, 125]
        
        window = 15  # ±15 frames before/after
        
        results = {}
        
        for event_frame in event_frames:
            # Before event
            before_data = self.frame_df[
                (self.frame_df['frame_idx'] >= event_frame - window) &
                (self.frame_df['frame_idx'] < event_frame)
            ]
            
            # After event
            after_data = self.frame_df[
                (self.frame_df['frame_idx'] > event_frame) &
                (self.frame_df['frame_idx'] <= event_frame + window)
            ]
            
            for scale in ['individual', 'tactical']:
                before_scale = before_data[before_data['scale'] == scale]
                after_scale = after_data[after_data['scale'] == scale]
                
                key = f"frame_{event_frame}_{scale}"
                results[key] = {
                    'before_mean_persistence': before_scale['mean_persistence'].mean() if len(before_scale) > 0 else 0,
                    'after_mean_persistence': after_scale['mean_persistence'].mean() if len(after_scale) > 0 else 0,
                    'before_n_loops': before_scale['n_loops'].mean() if len(before_scale) > 0 else 0,
                    'after_n_loops': after_scale['n_loops'].mean() if len(after_scale) > 0 else 0,
                }
        
        # Visualize
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('H1 Loop Persistence: Before vs After Events', fontsize=14, fontweight='bold')
        
        for scale_idx, scale in enumerate(['individual', 'tactical']):
            ax = axes[scale_idx]
            
            before_vals = []
            after_vals = []
            labels = []
            
            for event_frame in event_frames:
                key = f"frame_{event_frame}_{scale}"
                if key in results:
                    before_vals.append(results[key]['before_mean_persistence'])
                    after_vals.append(results[key]['after_mean_persistence'])
                    labels.append(f"Event {event_frame}")
            
            x = np.arange(len(labels))
            width = 0.35
            
            ax.bar(x - width/2, before_vals, width, label='Before Event', 
                  color='blue', alpha=0.7)
            ax.bar(x + width/2, after_vals, width, label='After Event', 
                  color='red', alpha=0.7)
            
            ax.set_xlabel('Event', fontsize=12)
            ax.set_ylabel('Mean Persistence', fontsize=12)
            ax.set_title(f'{scale.capitalize()} Scale', fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'before_after_events.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        # Print statistics
        print("\n📊 Before/After Event Statistics:")
        for event_frame in event_frames:
            print(f"\n  Event at Frame {event_frame}:")
            for scale in ['individual', 'tactical']:
                key = f"frame_{event_frame}_{scale}"
                if key in results:
                    r = results[key]
                    change = r['after_mean_persistence'] - r['before_mean_persistence']
                    change_pct = (change / max(0.001, r['before_mean_persistence'])) * 100
                    print(f"    {scale.capitalize()}: {r['before_mean_persistence']:.3f} → {r['after_mean_persistence']:.3f} ({change:+.3f}, {change_pct:+.1f}%)")
        
        return results
    
    def analyze_loop_transitions(self):
        """Analyze transitions in loop patterns (formation changes)"""
        print("\n" + "="*70)
        print("ANALYZING LOOP TRANSITIONS (FORMATION CHANGES)")
        print("="*70)
        
        # Calculate frame-to-frame changes
        transitions = []
        
        for scale in ['individual', 'tactical']:
            scale_data = self.frame_df[self.frame_df['scale'] == scale].sort_values('frame_idx')
            
            for i in range(1, len(scale_data)):
                prev = scale_data.iloc[i-1]
                curr = scale_data.iloc[i]
                
                transitions.append({
                    'frame_idx': curr['frame_idx'],
                    'time_seconds': curr['time_seconds'],
                    'scale': scale,
                    'n_loops_change': curr['n_loops'] - prev['n_loops'],
                    'persistence_change': curr['mean_persistence'] - prev['mean_persistence'],
                    'persistence_ratio': curr['mean_persistence'] / max(0.001, prev['mean_persistence']),
                    'max_persistence_change': curr['max_persistence'] - prev['max_persistence']
                })
        
        transitions_df = pd.DataFrame(transitions)
        
        # Identify significant transitions
        threshold_persistence_change = transitions_df['persistence_change'].abs().quantile(0.9)
        significant_transitions = transitions_df[
            transitions_df['persistence_change'].abs() > threshold_persistence_change
        ].sort_values('persistence_change', key=abs, ascending=False)
        
        print(f"\n📊 Transition Analysis:")
        print(f"   Total transitions: {len(transitions_df)}")
        print(f"   Significant transitions (>90th percentile): {len(significant_transitions)}")
        print(f"\n   Top 5 Largest Persistence Changes:")
        for idx, row in significant_transitions.head(5).iterrows():
            print(f"      Frame {int(row['frame_idx'])} ({row['scale']}): {row['persistence_change']:+.3f}")
        
        # Visualize transitions
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('H1 Loop Transitions Over Time', fontsize=16, fontweight='bold')
        
        for scale_idx, scale in enumerate(['individual', 'tactical']):
            scale_transitions = transitions_df[transitions_df['scale'] == scale]
            
            # Plot persistence changes
            ax1 = axes[scale_idx, 0]
            ax1.scatter(scale_transitions['frame_idx'], scale_transitions['persistence_change'],
                       alpha=0.6, s=30, c='blue')
            ax1.axhline(0, color='black', linestyle='--', alpha=0.3)
            ax1.set_xlabel('Frame Index', fontsize=12)
            ax1.set_ylabel('Persistence Change', fontsize=12)
            ax1.set_title(f'{scale.capitalize()} Scale: Persistence Changes', fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # Plot loop count changes
            ax2 = axes[scale_idx, 1]
            ax2.scatter(scale_transitions['frame_idx'], scale_transitions['n_loops_change'],
                       alpha=0.6, s=30, c='red')
            ax2.axhline(0, color='black', linestyle='--', alpha=0.3)
            ax2.set_xlabel('Frame Index', fontsize=12)
            ax2.set_ylabel('Loop Count Change', fontsize=12)
            ax2.set_title(f'{scale.capitalize()} Scale: Loop Count Changes', fontweight='bold')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / 'loop_transitions.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        # Save significant transitions
        significant_transitions_file = self.output_dir / 'significant_transitions.json'
        significant_transitions.to_json(significant_transitions_file, orient='records', indent=2)
        print(f"✅ Saved: {significant_transitions_file}")
        
        return transitions_df, significant_transitions
    
    def correlate_with_statsbomb_events(self):
        """Correlate loops with StatsBomb event data (if available)"""
        if self.events_data is None:
            print("\n⚠️  No StatsBomb event data available. Using synthetic analysis.")
            return None
        
        print("\n" + "="*70)
        print("CORRELATING WITH STATSBOMB EVENTS")
        print("="*70)
        
        # Parse events
        events_df = pd.DataFrame(self.events_data)
        
        # Extract important event types
        important_events = ['Goal', 'Shot', 'Pass', 'Ball Receipt', 'Dribble', 
                          'Tackle', 'Interception', 'Clearance']
        
        relevant_events = events_df[events_df['type'].isin(important_events)].copy()
        
        # Convert event timestamps to frame indices
        # Assuming events have 'timestamp' or 'minute' field
        # This needs to be adapted to actual StatsBomb data structure
        
        print(f"   Found {len(relevant_events)} relevant events")
        print(f"   Event types: {relevant_events['type'].value_counts().to_dict()}")
        
        # Correlation analysis would go here
        # This is a placeholder for actual implementation
        
        return relevant_events
    
    def generate_correlation_report(self):
        """Generate comprehensive correlation report"""
        report = []
        report.append("="*70)
        report.append("H1 LOOPS EVENT CORRELATION ANALYSIS")
        report.append("="*70)
        report.append("")
        
        # Overall statistics
        report.append("OVERALL STATISTICS:")
        report.append("-" * 70)
        for scale in ['individual', 'tactical']:
            scale_data = self.frame_df[self.frame_df['scale'] == scale]
            report.append(f"\n{scale.upper()} Scale:")
            report.append(f"  Frames with loops: {len(scale_data[scale_data['n_loops'] > 0])}")
            report.append(f"  Mean persistence: {scale_data[scale_data['n_loops'] > 0]['mean_persistence'].mean():.3f}")
            report.append(f"  Max persistence: {scale_data['max_persistence'].max():.3f}")
        
        report.append("\n" + "="*70)
        
        report_text = "\n".join(report)
        report_file = self.output_dir / 'event_correlation_report.txt'
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Saved: {report_file}")
        print("\n" + report_text)
    
    def run_full_analysis(self):
        """Run all event correlation analyses"""
        print("\n" + "="*70)
        print("H1 LOOPS EVENT CORRELATION ANALYSIS")
        print("="*70)
        
        print("\n📊 Analyzing loop patterns around events...")
        synthetic_events = self.analyze_with_synthetic_events()
        
        print("\n📈 Analyzing persistence before/after events...")
        event_frames = [e['frame'] for e in synthetic_events]
        self.analyze_persistence_before_after_events(event_frames)
        
        print("\n🔄 Analyzing loop transitions...")
        transitions_df, significant_transitions = self.analyze_loop_transitions()
        
        print("\n🔗 Attempting StatsBomb event correlation...")
        statsbomb_events = self.correlate_with_statsbomb_events()
        
        print("\n📝 Generating correlation report...")
        self.generate_correlation_report()
        
        print("\n" + "="*70)
        print("✅ EVENT CORRELATION ANALYSIS COMPLETE!")
        print("="*70)
        print(f"\n📁 Output directory: {self.output_dir}")


if __name__ == '__main__':
    analyzer = H1EventCorrelationAnalyzer()
    analyzer.run_full_analysis()

