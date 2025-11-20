#!/usr/bin/env python3
"""
Multi-Scale H0/H1 Effects on Upstream Analyses
==============================================

Investigates how the multi-scale H0/H1 regime affects:
1. Formation Complexity Quantification
2. Tactical Stability Analysis  
3. Player Interaction Networks
4. Quantum-Inspired Dynamics

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')


class MultiScaleUpstreamAnalyzer:
    """Analyze effects of multi-scale H0/H1 on upstream analyses"""
    
    # Validated multi-scale cut-offs
    VALIDATED_CUTOFFS = {
        'individual': 2.98,  # Individual player patterns
        'tactical': 12.0,    # Tactical group formations (single-frame)
        'team': 30.0         # Team-level separation
    }
    
    def __init__(self, loops_data_file='h1_loop_analysis/h1_loops_full_data.json',
                 comprehensive_results_file=None):
        """Initialize with loop data and optional comprehensive results"""
        # Load H1 loop data
        with open(loops_data_file, 'r') as f:
            self.loops_data = json.load(f)
        
        self.loops_df = pd.DataFrame(self.loops_data)
        
        # Load comprehensive multi-goal analysis if available
        self.comprehensive_data = None
        if comprehensive_results_file and Path(comprehensive_results_file).exists():
            with open(comprehensive_results_file, 'r') as f:
                self.comprehensive_data = json.load(f)
        
        self.output_dir = Path('h1_loop_analysis/multiscale_upstream_effects')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Loaded {len(self.loops_df)} H1 loops")
        print(f"   Scales available: {sorted(self.loops_df['scale'].unique())}")
        
        # Prepare frame-level multi-scale data
        self._prepare_multiscale_frame_data()
    
    def _prepare_multiscale_frame_data(self):
        """Prepare frame-level data aggregated by scale"""
        frame_data = []
        
        for frame_idx in sorted(self.loops_df['frame_idx'].unique()):
            frame_loops = self.loops_df[self.loops_df['frame_idx'] == frame_idx]
            
            for scale in ['individual', 'tactical']:
                scale_loops = frame_loops[frame_loops['scale'] == scale]
                
                frame_data.append({
                    'frame_idx': frame_idx,
                    'scale': scale,
                    'h0_count': scale_loops['h0_count'].iloc[0] if len(scale_loops) > 0 else 0,
                    'h1_count': len(scale_loops),  # Number of loops = H1 features
                    'mean_persistence': scale_loops['persistence'].mean() if len(scale_loops) > 0 else 0,
                    'max_persistence': scale_loops['persistence'].max() if len(scale_loops) > 0 else 0,
                    'total_persistence': scale_loops['persistence'].sum() if len(scale_loops) > 0 else 0,
                    'mean_birth': scale_loops['birth'].mean() if len(scale_loops) > 0 else 0,
                    'mean_death': scale_loops['death'].mean() if len(scale_loops) > 0 else 0,
                    'cutoff': scale_loops['cutoff'].iloc[0] if len(scale_loops) > 0 else self.VALIDATED_CUTOFFS.get(scale, 0)
                })
        
        self.multiscale_df = pd.DataFrame(frame_data)
        print(f"✅ Prepared multi-scale frame data: {len(self.multiscale_df)} frame-scale combinations")
    
    def analyze_formation_complexity(self):
        """
        Analyze Formation Complexity Quantification
        
        Original: formation_complexity = H0_features + H1_features + persistence_entropy
        Multi-scale: Need to combine across scales appropriately
        """
        print("\n" + "="*70)
        print("1. FORMATION COMPLEXITY QUANTIFICATION")
        print("="*70)
        
        complexity_results = []
        
        for frame_idx in sorted(self.multiscale_df['frame_idx'].unique()):
            frame_data = self.multiscale_df[self.multiscale_df['frame_idx'] == frame_idx]
            
            # Original single-scale approach (using individual scale)
            individual_data = frame_data[frame_data['scale'] == 'individual'].iloc[0] if len(frame_data[frame_data['scale'] == 'individual']) > 0 else None
            tactical_data = frame_data[frame_data['scale'] == 'tactical'].iloc[0] if len(frame_data[frame_data['scale'] == 'tactical']) > 0 else None
            
            if individual_data is None:
                continue
            
            # Original complexity (individual scale only)
            h0_features_orig = individual_data['h0_count']
            h1_features_orig = individual_data['h1_count']
            persistence_orig = individual_data['mean_persistence']
            persistence_entropy_orig = -np.log(max(persistence_orig, 0.001)) * persistence_orig  # Simplified entropy
            complexity_original = h0_features_orig + h1_features_orig + persistence_entropy_orig
            
            # Multi-scale complexity approaches
            if tactical_data is not None:
                h0_tactical = tactical_data['h0_count']
                h1_tactical = tactical_data['h1_count']
                persistence_tactical = tactical_data['mean_persistence']
                
                # Approach 1: Weighted sum (individual + tactical)
                complexity_weighted = (
                    0.6 * (h0_features_orig + h1_features_orig + persistence_entropy_orig) +
                    0.4 * (h0_tactical + h1_tactical + (-np.log(max(persistence_tactical, 0.001)) * persistence_tactical))
                )
                
                # Approach 2: Multi-scale entropy
                persistence_entropy_multiscale = (
                    -np.log(max(persistence_orig, 0.001)) * persistence_orig +
                    -np.log(max(persistence_tactical, 0.001)) * persistence_tactical
                )
                complexity_multiscale = (
                    h0_features_orig + h1_features_orig +  # Individual topology
                    h0_tactical + h1_tactical +           # Tactical topology
                    persistence_entropy_multiscale        # Multi-scale persistence entropy
                )
                
                # Approach 3: Scale-separated (capture different aspects)
                complexity_separated = {
                    'individual_complexity': h0_features_orig + h1_features_orig + persistence_entropy_orig,
                    'tactical_complexity': h0_tactical + h1_tactical + (-np.log(max(persistence_tactical, 0.001)) * persistence_tactical),
                    'combined_complexity': complexity_multiscale
                }
            else:
                complexity_weighted = complexity_original
                complexity_multiscale = complexity_original
                complexity_separated = {
                    'individual_complexity': complexity_original,
                    'tactical_complexity': 0,
                    'combined_complexity': complexity_original
                }
            
            complexity_results.append({
                'frame_idx': frame_idx,
                'complexity_original': complexity_original,
                'complexity_weighted': complexity_weighted,
                'complexity_multiscale': complexity_multiscale,
                'complexity_individual': complexity_separated['individual_complexity'],
                'complexity_tactical': complexity_separated['tactical_complexity'],
                'h0_individual': individual_data['h0_count'],
                'h1_individual': individual_data['h1_count'],
                'h0_tactical': tactical_data['h0_count'] if tactical_data is not None else 0,
                'h1_tactical': tactical_data['h1_count'] if tactical_data is not None else 0,
            })
        
        complexity_df = pd.DataFrame(complexity_results)
        
        # Statistics
        print("\n📊 Complexity Comparison:")
        print(f"   Original (single-scale): {complexity_df['complexity_original'].mean():.3f} ± {complexity_df['complexity_original'].std():.3f}")
        print(f"   Multi-scale (combined): {complexity_df['complexity_multiscale'].mean():.3f} ± {complexity_df['complexity_multiscale'].std():.3f}")
        print(f"   Individual complexity: {complexity_df['complexity_individual'].mean():.3f} ± {complexity_df['complexity_individual'].std():.3f}")
        print(f"   Tactical complexity: {complexity_df['complexity_tactical'].mean():.3f} ± {complexity_df['complexity_tactical'].mean():.3f}")
        
        # Correlation
        corr_orig_multiscale = complexity_df['complexity_original'].corr(complexity_df['complexity_multiscale'])
        corr_individual_tactical = complexity_df['complexity_individual'].corr(complexity_df['complexity_tactical'])
        
        print(f"\n   Correlation (original vs multi-scale): {corr_orig_multiscale:.3f}")
        print(f"   Correlation (individual vs tactical): {corr_individual_tactical:.3f}")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Formation Complexity: Single-Scale vs Multi-Scale', fontsize=16, fontweight='bold')
        
        # Plot 1: Time series comparison
        ax1 = axes[0, 0]
        ax1.plot(complexity_df['frame_idx'], complexity_df['complexity_original'],
                'b-', label='Original (Individual)', linewidth=2, alpha=0.7)
        ax1.plot(complexity_df['frame_idx'], complexity_df['complexity_multiscale'],
                'r-', label='Multi-Scale (Combined)', linewidth=2, alpha=0.7)
        ax1.set_xlabel('Frame Index', fontsize=12)
        ax1.set_ylabel('Formation Complexity', fontsize=12)
        ax1.set_title('Complexity Over Time', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Scatter comparison
        ax2 = axes[0, 1]
        ax2.scatter(complexity_df['complexity_original'], complexity_df['complexity_multiscale'],
                   alpha=0.6, s=50)
        max_val = max(complexity_df['complexity_original'].max(), complexity_df['complexity_multiscale'].max())
        ax2.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='y=x')
        ax2.set_xlabel('Original Complexity', fontsize=12)
        ax2.set_ylabel('Multi-Scale Complexity', fontsize=12)
        ax2.set_title(f'Correlation: {corr_orig_multiscale:.3f}', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Scale separation
        ax3 = axes[1, 0]
        ax3.plot(complexity_df['frame_idx'], complexity_df['complexity_individual'],
                'b-', label='Individual Scale', linewidth=2, alpha=0.7)
        ax3.plot(complexity_df['frame_idx'], complexity_df['complexity_tactical'],
                'r-', label='Tactical Scale', linewidth=2, alpha=0.7)
        ax3.set_xlabel('Frame Index', fontsize=12)
        ax3.set_ylabel('Formation Complexity', fontsize=12)
        ax3.set_title('Scale-Separated Complexity', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Distribution comparison
        ax4 = axes[1, 1]
        ax4.hist(complexity_df['complexity_original'], bins=30, alpha=0.6, label='Original', color='blue')
        ax4.hist(complexity_df['complexity_multiscale'], bins=30, alpha=0.6, label='Multi-Scale', color='red')
        ax4.set_xlabel('Formation Complexity', fontsize=12)
        ax4.set_ylabel('Frequency', fontsize=12)
        ax4.set_title('Complexity Distributions', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'formation_complexity_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        return complexity_df
    
    def analyze_tactical_stability(self):
        """
        Analyze Tactical Stability Analysis
        
        Original: tactical_stability = mean(persistence_diagrams.H0(:,2) - persistence_diagrams.H0(:,1))
        Multi-scale: Scale-specific stability, or combined metric?
        """
        print("\n" + "="*70)
        print("2. TACTICAL STABILITY ANALYSIS")
        print("="*70)
        
        stability_results = []
        
        for frame_idx in sorted(self.multiscale_df['frame_idx'].unique()):
            frame_data = self.multiscale_df[self.multiscale_df['frame_idx'] == frame_idx]
            
            individual_data = frame_data[frame_data['scale'] == 'individual']
            tactical_data = frame_data[frame_data['scale'] == 'tactical']
            
            # Original stability (H0 persistence: death - birth)
            # We approximate using H1 persistence as proxy (actual H0 persistence would need birth/death times)
            if len(individual_data) > 0:
                ind = individual_data.iloc[0]
                # Stability from persistence (death - birth)
                stability_original = ind['mean_persistence']  # Simplified: mean persistence
                stability_individual_h0 = ind['h0_count']  # H0 count as stability proxy
                stability_individual_h1 = ind['mean_persistence']  # H1 persistence
            else:
                stability_original = 0
                stability_individual_h0 = 0
                stability_individual_h1 = 0
            
            if len(tactical_data) > 0:
                tac = tactical_data.iloc[0]
                stability_tactical_h0 = tac['h0_count']
                stability_tactical_h1 = tac['mean_persistence']
            else:
                stability_tactical_h0 = 0
                stability_tactical_h1 = 0
            
            # Multi-scale stability
            stability_multiscale = (
                0.6 * stability_individual_h1 +  # Individual persistence
                0.4 * stability_tactical_h1      # Tactical persistence
            )
            
            stability_results.append({
                'frame_idx': frame_idx,
                'stability_original': stability_original,
                'stability_multiscale': stability_multiscale,
                'stability_individual_h0': stability_individual_h0,
                'stability_individual_h1': stability_individual_h1,
                'stability_tactical_h0': stability_tactical_h0,
                'stability_tactical_h1': stability_tactical_h1,
            })
        
        stability_df = pd.DataFrame(stability_results)
        
        # Temporal stability (consistency over time)
        window = 10
        stability_df['stability_original_rolling'] = stability_df['stability_original'].rolling(window, center=True).std()
        stability_df['stability_multiscale_rolling'] = stability_df['stability_multiscale'].rolling(window, center=True).std()
        
        # Lower std = more stable
        temporal_stability_original = 1.0 / (1.0 + stability_df['stability_original_rolling'].mean())
        temporal_stability_multiscale = 1.0 / (1.0 + stability_df['stability_multiscale_rolling'].mean())
        
        print("\n📊 Stability Comparison:")
        print(f"   Original (mean persistence): {stability_df['stability_original'].mean():.3f} ± {stability_df['stability_original'].std():.3f}")
        print(f"   Multi-scale (combined): {stability_df['stability_multiscale'].mean():.3f} ± {stability_df['stability_multiscale'].std():.3f}")
        print(f"   Temporal stability (original): {temporal_stability_original:.3f}")
        print(f"   Temporal stability (multi-scale): {temporal_stability_multiscale:.3f}")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Tactical Stability: Single-Scale vs Multi-Scale', fontsize=16, fontweight='bold')
        
        # Plot 1: Stability over time
        ax1 = axes[0, 0]
        ax1.plot(stability_df['frame_idx'], stability_df['stability_original'],
                'b-', label='Original (Individual)', linewidth=2, alpha=0.7)
        ax1.plot(stability_df['frame_idx'], stability_df['stability_multiscale'],
                'r-', label='Multi-Scale', linewidth=2, alpha=0.7)
        ax1.set_xlabel('Frame Index', fontsize=12)
        ax1.set_ylabel('Stability (Persistence)', fontsize=12)
        ax1.set_title('Stability Over Time', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Scale comparison
        ax2 = axes[0, 1]
        ax2.plot(stability_df['frame_idx'], stability_df['stability_individual_h1'],
                'b-', label='Individual H1', linewidth=2, alpha=0.7)
        ax2.plot(stability_df['frame_idx'], stability_df['stability_tactical_h1'],
                'r-', label='Tactical H1', linewidth=2, alpha=0.7)
        ax2.set_xlabel('Frame Index', fontsize=12)
        ax2.set_ylabel('Persistence Stability', fontsize=12)
        ax2.set_title('Scale-Separated Stability', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Temporal stability (rolling std)
        ax3 = axes[1, 0]
        ax3.plot(stability_df['frame_idx'], stability_df['stability_original_rolling'],
                'b-', label='Original Variability', linewidth=2, alpha=0.7)
        ax3.plot(stability_df['frame_idx'], stability_df['stability_multiscale_rolling'],
                'r-', label='Multi-Scale Variability', linewidth=2, alpha=0.7)
        ax3.set_xlabel('Frame Index', fontsize=12)
        ax3.set_ylabel('Rolling Std Dev', fontsize=12)
        ax3.set_title('Temporal Stability (Lower = More Stable)', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: H0 vs H1 stability
        ax4 = axes[1, 1]
        ax4.scatter(stability_df['stability_individual_h0'], stability_df['stability_individual_h1'],
                   alpha=0.6, s=50, label='Individual', color='blue')
        ax4.scatter(stability_df['stability_tactical_h0'], stability_df['stability_tactical_h1'],
                   alpha=0.6, s=50, label='Tactical', color='red')
        ax4.set_xlabel('H0 Count (Connectivity)', fontsize=12)
        ax4.set_ylabel('H1 Persistence (Stability)', fontsize=12)
        ax4.set_title('H0 vs H1 Stability Relationship', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / 'tactical_stability_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        return stability_df
    
    def analyze_interaction_networks(self):
        """
        Analyze Player Interaction Networks
        
        Original: buildPlayerInteractionNetwork(player_positions)
        Multi-scale: Networks at different scales reveal different interaction patterns
        """
        print("\n" + "="*70)
        print("3. PLAYER INTERACTION NETWORKS")
        print("="*70)
        
        # For network analysis, we need point cloud data
        # Use loop data to extract network structures
        network_results = []
        
        for frame_idx in sorted(self.loops_df['frame_idx'].unique())[:20]:  # Sample first 20 frames
            frame_loops = self.loops_df[self.loops_df['frame_idx'] == frame_idx]
            
            for scale in ['individual', 'tactical']:
                scale_loops = frame_loops[frame_loops['scale'] == scale]
                
                if len(scale_loops) == 0:
                    continue
                
                # Extract network from loop structures
                # Each loop represents a cycle in the network
                n_loops = len(scale_loops)
                total_persistence = scale_loops['persistence'].sum()
                mean_persistence = scale_loops['persistence'].mean()
                
                # Network strength from loop structures
                # More loops, higher persistence = stronger network
                network_strength = n_loops * mean_persistence
                
                # Network connectivity (from H0)
                h0_count = scale_loops['h0_count'].iloc[0] if len(scale_loops) > 0 else 0
                
                # Network complexity (from H1 loops)
                network_complexity = n_loops
                
                network_results.append({
                    'frame_idx': frame_idx,
                    'scale': scale,
                    'network_strength': network_strength,
                    'network_complexity': network_complexity,
                    'network_connectivity': h0_count,
                    'n_loops': n_loops,
                    'mean_persistence': mean_persistence,
                })
        
        network_df = pd.DataFrame(network_results)
        
        # Aggregate by scale
        network_stats = network_df.groupby('scale').agg({
            'network_strength': ['mean', 'std'],
            'network_complexity': ['mean', 'std'],
            'network_connectivity': ['mean', 'std']
        })
        
        print("\n📊 Network Analysis by Scale:")
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale]
            if len(scale_data) > 0:
                print(f"\n   {scale.upper()} Scale:")
                print(f"      Network strength: {scale_data['network_strength'].mean():.3f} ± {scale_data['network_strength'].std():.3f}")
                print(f"      Network complexity: {scale_data['network_complexity'].mean():.3f} ± {scale_data['network_complexity'].std():.3f}")
                print(f"      Network connectivity: {scale_data['network_connectivity'].mean():.3f} ± {scale_data['network_connectivity'].std():.3f}")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Player Interaction Networks: Multi-Scale Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Network strength by scale
        ax1 = axes[0, 0]
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale].sort_values('frame_idx')
            ax1.plot(scale_data['frame_idx'], scale_data['network_strength'],
                    'o-', label=f'{scale.capitalize()}', linewidth=2, markersize=4, alpha=0.7)
        ax1.set_xlabel('Frame Index', fontsize=12)
        ax1.set_ylabel('Network Strength', fontsize=12)
        ax1.set_title('Network Strength Over Time', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Network complexity
        ax2 = axes[0, 1]
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale].sort_values('frame_idx')
            ax2.plot(scale_data['frame_idx'], scale_data['network_complexity'],
                    'o-', label=f'{scale.capitalize()}', linewidth=2, markersize=4, alpha=0.7)
        ax2.set_xlabel('Frame Index', fontsize=12)
        ax2.set_ylabel('Network Complexity (H1 Loops)', fontsize=12)
        ax2.set_title('Network Complexity Over Time', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Connectivity vs Complexity
        ax3 = axes[1, 0]
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale]
            ax3.scatter(scale_data['network_connectivity'], scale_data['network_complexity'],
                       alpha=0.6, s=50, label=f'{scale.capitalize()}')
        ax3.set_xlabel('Network Connectivity (H0)', fontsize=12)
        ax3.set_ylabel('Network Complexity (H1)', fontsize=12)
        ax3.set_title('Connectivity vs Complexity', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Scale comparison distribution
        ax4 = axes[1, 1]
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale]
            ax4.hist(scale_data['network_strength'], bins=20, alpha=0.6, label=f'{scale.capitalize()}')
        ax4.set_xlabel('Network Strength', fontsize=12)
        ax4.set_ylabel('Frequency', fontsize=12)
        ax4.set_title('Network Strength Distribution', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_file = self.output_dir / 'interaction_networks_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        return network_df
    
    def analyze_quantum_coherence(self):
        """
        Analyze Quantum-Inspired Dynamics
        
        Original: quantum_coherence = measureQuantumCoherence(team_dynamics)
        Multi-scale: Coherence at different scales, or combined multi-scale coherence?
        """
        print("\n" + "="*70)
        print("4. QUANTUM-INSPIRED DYNAMICS")
        print("="*70)
        
        # Quantum coherence from persistence consistency
        coherence_results = []
        
        window = 10  # Rolling window for coherence calculation
        
        for scale in ['individual', 'tactical']:
            scale_data = self.multiscale_df[self.multiscale_df['scale'] == scale].sort_values('frame_idx')
            
            # Coherence from persistence consistency (lower variance = higher coherence)
            rolling_mean = scale_data['mean_persistence'].rolling(window, center=True).mean()
            rolling_std = scale_data['mean_persistence'].rolling(window, center=True).std()
            
            # Quantum coherence: inverse relationship with variance
            coherence = 1.0 / (1.0 + rolling_std / (rolling_mean + 1e-6))
            
            for idx, row in scale_data.iterrows():
                frame_idx = row['frame_idx']
                coherence_results.append({
                    'frame_idx': frame_idx,
                    'scale': scale,
                    'coherence': coherence.loc[idx] if idx in coherence.index else 0,
                    'persistence': row['mean_persistence'],
                    'persistence_std': rolling_std.loc[idx] if idx in rolling_std.index else 0,
                })
        
        coherence_df = pd.DataFrame(coherence_results)
        
        # Multi-scale coherence
        frame_coherence = []
        for frame_idx in sorted(coherence_df['frame_idx'].unique()):
            frame_data = coherence_df[coherence_df['frame_idx'] == frame_idx]
            ind_coherence = frame_data[frame_data['scale'] == 'individual']['coherence'].values
            tac_coherence = frame_data[frame_data['scale'] == 'tactical']['coherence'].values
            
            if len(ind_coherence) > 0 and len(tac_coherence) > 0:
                # Combined coherence
                multiscale_coherence = 0.6 * ind_coherence[0] + 0.4 * tac_coherence[0]
            elif len(ind_coherence) > 0:
                multiscale_coherence = ind_coherence[0]
            elif len(tac_coherence) > 0:
                multiscale_coherence = tac_coherence[0]
            else:
                continue
            
            frame_coherence.append({
                'frame_idx': frame_idx,
                'coherence_multiscale': multiscale_coherence,
                'coherence_individual': ind_coherence[0] if len(ind_coherence) > 0 else 0,
                'coherence_tactical': tac_coherence[0] if len(tac_coherence) > 0 else 0,
            })
        
        coherence_frames_df = pd.DataFrame(frame_coherence)
        
        print("\n📊 Quantum Coherence Comparison:")
        print(f"   Individual scale: {coherence_frames_df['coherence_individual'].mean():.3f} ± {coherence_frames_df['coherence_individual'].std():.3f}")
        print(f"   Tactical scale: {coherence_frames_df['coherence_tactical'].mean():.3f} ± {coherence_frames_df['coherence_tactical'].std():.3f}")
        print(f"   Multi-scale (combined): {coherence_frames_df['coherence_multiscale'].mean():.3f} ± {coherence_frames_df['coherence_multiscale'].std():.3f}")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Quantum Coherence: Multi-Scale Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Coherence over time
        ax1 = axes[0, 0]
        ax1.plot(coherence_frames_df['frame_idx'], coherence_frames_df['coherence_individual'],
                'b-', label='Individual', linewidth=2, alpha=0.7)
        ax1.plot(coherence_frames_df['frame_idx'], coherence_frames_df['coherence_tactical'],
                'r-', label='Tactical', linewidth=2, alpha=0.7)
        ax1.plot(coherence_frames_df['frame_idx'], coherence_frames_df['coherence_multiscale'],
                'g-', label='Multi-Scale', linewidth=2, alpha=0.7)
        ax1.set_xlabel('Frame Index', fontsize=12)
        ax1.set_ylabel('Quantum Coherence', fontsize=12)
        ax1.set_title('Coherence Over Time', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Scale comparison
        ax2 = axes[0, 1]
        ax2.scatter(coherence_frames_df['coherence_individual'], coherence_frames_df['coherence_tactical'],
                   alpha=0.6, s=50)
        max_val = max(coherence_frames_df['coherence_individual'].max(), coherence_frames_df['coherence_tactical'].max())
        ax2.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='y=x')
        ax2.set_xlabel('Individual Coherence', fontsize=12)
        ax2.set_ylabel('Tactical Coherence', fontsize=12)
        ax2.set_title('Individual vs Tactical Coherence', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Multi-scale coherence distribution
        ax3 = axes[1, 0]
        ax3.hist(coherence_frames_df['coherence_individual'], bins=30, alpha=0.6, label='Individual', color='blue')
        ax3.hist(coherence_frames_df['coherence_tactical'], bins=30, alpha=0.6, label='Tactical', color='red')
        ax3.hist(coherence_frames_df['coherence_multiscale'], bins=30, alpha=0.6, label='Multi-Scale', color='green')
        ax3.set_xlabel('Quantum Coherence', fontsize=12)
        ax3.set_ylabel('Frequency', fontsize=12)
        ax3.set_title('Coherence Distributions', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Coherence relationship with persistence
        ax4 = axes[1, 1]
        individual_data = coherence_df[coherence_df['scale'] == 'individual']
        tactical_data = coherence_df[coherence_df['scale'] == 'tactical']
        ax4.scatter(individual_data['persistence'], individual_data['coherence'],
                   alpha=0.6, s=50, label='Individual', color='blue')
        ax4.scatter(tactical_data['persistence'], tactical_data['coherence'],
                   alpha=0.6, s=50, label='Tactical', color='red')
        ax4.set_xlabel('Persistence', fontsize=12)
        ax4.set_ylabel('Quantum Coherence', fontsize=12)
        ax4.set_title('Coherence vs Persistence', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_file = self.output_dir / 'quantum_coherence_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {output_file}")
        
        return coherence_df, coherence_frames_df
    
    def generate_comprehensive_report(self, complexity_df, stability_df, network_df, coherence_df):
        """Generate comprehensive report on multi-scale effects"""
        report = []
        report.append("="*70)
        report.append("MULTI-SCALE H0/H1 EFFECTS ON UPSTREAM ANALYSES")
        report.append("="*70)
        report.append("")
        
        report.append("SUMMARY OF FINDINGS:")
        report.append("-" * 70)
        report.append("")
        
        report.append("1. FORMATION COMPLEXITY:")
        report.append(f"   Original (single-scale): {complexity_df['complexity_original'].mean():.3f} ± {complexity_df['complexity_original'].std():.3f}")
        report.append(f"   Multi-scale (combined): {complexity_df['complexity_multiscale'].mean():.3f} ± {complexity_df['complexity_multiscale'].std():.3f}")
        report.append(f"   Correlation: {complexity_df['complexity_original'].corr(complexity_df['complexity_multiscale']):.3f}")
        report.append("")
        
        report.append("2. TACTICAL STABILITY:")
        report.append(f"   Original: {stability_df['stability_original'].mean():.3f} ± {stability_df['stability_original'].std():.3f}")
        report.append(f"   Multi-scale: {stability_df['stability_multiscale'].mean():.3f} ± {stability_df['stability_multiscale'].std():.3f}")
        report.append("")
        
        report.append("3. INTERACTION NETWORKS:")
        for scale in ['individual', 'tactical']:
            scale_data = network_df[network_df['scale'] == scale]
            if len(scale_data) > 0:
                report.append(f"   {scale.capitalize()} Scale:")
                report.append(f"      Network strength: {scale_data['network_strength'].mean():.3f}")
                report.append(f"      Network complexity: {scale_data['network_complexity'].mean():.3f}")
        report.append("")
        
        report.append("4. QUANTUM COHERENCE:")
        individual_coherence = coherence_df[coherence_df['scale'] == 'individual']['coherence'].mean()
        tactical_coherence = coherence_df[coherence_df['scale'] == 'tactical']['coherence'].mean()
        report.append(f"   Individual: {individual_coherence:.3f}")
        report.append(f"   Tactical: {tactical_coherence:.3f}")
        report.append("")
        
        report.append("="*70)
        
        report_text = "\n".join(report)
        report_file = self.output_dir / 'multiscale_effects_report.txt'
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        print(f"✅ Saved: {report_file}")
        print("\n" + report_text)
    
    def run_full_analysis(self):
        """Run all upstream effect analyses"""
        print("\n" + "="*70)
        print("MULTI-SCALE H0/H1 EFFECTS ON UPSTREAM ANALYSES")
        print("="*70)
        
        print("\n🔍 Analyzing Formation Complexity...")
        complexity_df = self.analyze_formation_complexity()
        
        print("\n🔍 Analyzing Tactical Stability...")
        stability_df = self.analyze_tactical_stability()
        
        print("\n🔍 Analyzing Interaction Networks...")
        network_df = self.analyze_interaction_networks()
        
        print("\n🔍 Analyzing Quantum Coherence...")
        coherence_df, coherence_frames_df = self.analyze_quantum_coherence()
        
        print("\n📝 Generating comprehensive report...")
        self.generate_comprehensive_report(complexity_df, stability_df, network_df, coherence_df)
        
        print("\n" + "="*70)
        print("✅ MULTI-SCALE UPSTREAM EFFECTS ANALYSIS COMPLETE!")
        print("="*70)
        print(f"\n📁 Output directory: {self.output_dir}")


if __name__ == '__main__':
    analyzer = MultiScaleUpstreamAnalyzer()
    analyzer.run_full_analysis()

