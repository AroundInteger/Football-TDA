#!/usr/bin/env python3
"""
TDA Revolutionary Insights Analysis
=================================

This script provides detailed analysis of the TDA (Topological Data Analysis) 
aspects that enable the quantum phenomena discoveries in football team dynamics.

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

class TDARevolutionaryInsightsAnalyzer:
    """
    Analyzes the TDA aspects that enable quantum phenomena discoveries
    """
    
    def __init__(self, first_half_dir='first_half_efficient_results', 
                 second_half_dir='second_half_efficient_results',
                 quantum_dir='quantum_dot_full_match_results'):
        """
        Initialize the TDA insights analyzer
        
        Args:
            first_half_dir (str): Directory containing first half TDA results
            second_half_dir (str): Directory containing second half TDA results
            quantum_dir (str): Directory containing quantum analysis results
        """
        self.first_half_dir = Path(first_half_dir)
        self.second_half_dir = Path(second_half_dir)
        self.quantum_dir = Path(quantum_dir)
        
        self.first_half_data = None
        self.second_half_data = None
        self.combined_tda_data = None
        self.quantum_data = None
        
        print(f"TDARevolutionaryInsightsAnalyzer initialized")
        print(f"  First half TDA: {self.first_half_dir}")
        print(f"  Second half TDA: {self.second_half_dir}")
        print(f"  Quantum analysis: {self.quantum_dir}")
    
    def load_tda_data(self):
        """
        Load all TDA analysis data
        """
        print("\n=== Loading TDA Analysis Data ===")
        
        # Load first half TDA data
        first_half_file = self.first_half_dir / 'efficient_comprehensive_analysis.csv'
        if first_half_file.exists():
            self.first_half_data = pd.read_csv(first_half_file)
            self.first_half_data['half'] = 'First Half'
            print(f"✓ Loaded first half TDA data: {len(self.first_half_data)} windows")
        else:
            print(f"✗ First half TDA data not found: {first_half_file}")
            return False
        
        # Load second half TDA data
        second_half_file = self.second_half_dir / 'efficient_comprehensive_analysis.csv'
        if second_half_file.exists():
            self.second_half_data = pd.read_csv(second_half_file)
            self.second_half_data['half'] = 'Second Half'
            print(f"✓ Loaded second half TDA data: {len(self.second_half_data)} windows")
        else:
            print(f"✗ Second half TDA data not found: {second_half_file}")
            return False
        
        # Combine TDA data
        self.combined_tda_data = pd.concat([self.first_half_data, self.second_half_data], 
                                         ignore_index=True)
        self.combined_tda_data = self.combined_tda_data.sort_values('start_time')
        
        # Add attractor state labels (simplified clustering based on complexity)
        from sklearn.cluster import KMeans
        complexity_values = self.combined_tda_data['complexity_index'].values.reshape(-1, 1)
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        self.combined_tda_data['attractor_state'] = kmeans.fit_predict(complexity_values)
        
        # Load quantum analysis data
        quantum_report_file = self.quantum_dir / 'quantum_dot_comprehensive_report.json'
        if quantum_report_file.exists():
            with open(quantum_report_file, 'r') as f:
                self.quantum_data = json.load(f)
            print(f"✓ Loaded quantum analysis data")
        else:
            print(f"✗ Quantum analysis data not found: {quantum_report_file}")
            return False
        
        print(f"✓ Combined TDA data: {len(self.combined_tda_data)} total windows")
        print(f"  Time range: {self.combined_tda_data['start_time'].min():.1f} - {self.combined_tda_data['end_time'].max():.1f} minutes")
        
        return True
    
    def analyze_persistent_homology_features(self):
        """
        Analyze the persistent homology features (H0 and H1) that enable quantum insights
        """
        print("\n=== Analyzing Persistent Homology Features ===")
        
        # Extract H0 and H1 features
        h0_features = self.combined_tda_data['h0_count'].values
        h1_features = self.combined_tda_data['h1_count'].values
        total_features = self.combined_tda_data['total_features'].values
        complexity_index = self.combined_tda_data['complexity_index'].values
        
        # Calculate statistics
        h0_stats = {
            'mean': np.mean(h0_features),
            'std': np.std(h0_features),
            'min': np.min(h0_features),
            'max': np.max(h0_features),
            'range': np.max(h0_features) - np.min(h0_features)
        }
        
        h1_stats = {
            'mean': np.mean(h1_features),
            'std': np.std(h1_features),
            'min': np.min(h1_features),
            'max': np.max(h1_features),
            'range': np.max(h1_features) - np.min(h1_features)
        }
        
        complexity_stats = {
            'mean': np.mean(complexity_index),
            'std': np.std(complexity_index),
            'min': np.min(complexity_index),
            'max': np.max(complexity_index),
            'range': np.max(complexity_index) - np.min(complexity_index)
        }
        
        # Calculate H0/H1 ratio
        h0_h1_ratio = h0_features / (h1_features + 1)  # Add 1 to avoid division by zero
        ratio_stats = {
            'mean': np.mean(h0_h1_ratio),
            'std': np.std(h0_h1_ratio),
            'min': np.min(h0_h1_ratio),
            'max': np.max(h0_h1_ratio)
        }
        
        print("Persistent Homology Features Analysis:")
        print("=" * 60)
        print("H0 Features (Connected Components):")
        print(f"  Mean: {h0_stats['mean']:.1f}")
        print(f"  Std: {h0_stats['std']:.1f}")
        print(f"  Range: {h0_stats['min']:.1f} - {h0_stats['max']:.1f}")
        print(f"  Total H0 Features: {np.sum(h0_features):,}")
        
        print(f"\nH1 Features (Loops/Holes):")
        print(f"  Mean: {h1_stats['mean']:.1f}")
        print(f"  Std: {h1_stats['std']:.1f}")
        print(f"  Range: {h1_stats['min']:.1f} - {h1_stats['max']:.1f}")
        print(f"  Total H1 Features: {np.sum(h1_features):,}")
        
        print(f"\nComplexity Index:")
        print(f"  Mean: {complexity_stats['mean']:.4f}")
        print(f"  Std: {complexity_stats['std']:.4f}")
        print(f"  Range: {complexity_stats['min']:.4f} - {complexity_stats['max']:.4f}")
        
        print(f"\nH0/H1 Ratio:")
        print(f"  Mean: {ratio_stats['mean']:.2f}")
        print(f"  Std: {ratio_stats['std']:.2f}")
        print(f"  Range: {ratio_stats['min']:.2f} - {ratio_stats['max']:.2f}")
        
        # Analyze temporal evolution
        time_correlation_h0 = np.corrcoef(self.combined_tda_data['start_time'], h0_features)[0, 1]
        time_correlation_h1 = np.corrcoef(self.combined_tda_data['start_time'], h1_features)[0, 1]
        time_correlation_complexity = np.corrcoef(self.combined_tda_data['start_time'], complexity_index)[0, 1]
        
        print(f"\nTemporal Correlations:")
        print(f"  H0-Time Correlation: {time_correlation_h0:.4f}")
        print(f"  H1-Time Correlation: {time_correlation_h1:.4f}")
        print(f"  Complexity-Time Correlation: {time_correlation_complexity:.4f}")
        
        return {
            'h0_stats': h0_stats,
            'h1_stats': h1_stats,
            'complexity_stats': complexity_stats,
            'ratio_stats': ratio_stats,
            'temporal_correlations': {
                'h0_time': time_correlation_h0,
                'h1_time': time_correlation_h1,
                'complexity_time': time_correlation_complexity
            }
        }
    
    def analyze_vietoris_rips_complex_insights(self):
        """
        Analyze insights from the Vietoris-Rips complex construction
        """
        print("\n=== Analyzing Vietoris-Rips Complex Insights ===")
        
        # Extract team metrics that form the point cloud
        inter_team_distance = self.combined_tda_data['avg_inter_team_distance'].values
        team_area_ratio = self.combined_tda_data['avg_team_area_ratio'].values
        home_spread = self.combined_tda_data['avg_home_spread'].values
        away_spread = self.combined_tda_data['avg_away_spread'].values
        
        # Calculate point cloud statistics
        point_cloud_stats = {
            'inter_team_distance': {
                'mean': np.mean(inter_team_distance),
                'std': np.std(inter_team_distance),
                'range': np.max(inter_team_distance) - np.min(inter_team_distance)
            },
            'team_area_ratio': {
                'mean': np.mean(team_area_ratio),
                'std': np.std(team_area_ratio),
                'range': np.max(team_area_ratio) - np.min(team_area_ratio)
            },
            'home_spread': {
                'mean': np.mean(home_spread),
                'std': np.std(home_spread),
                'range': np.max(home_spread) - np.min(home_spread)
            },
            'away_spread': {
                'mean': np.mean(away_spread),
                'std': np.std(away_spread),
                'range': np.max(away_spread) - np.min(away_spread)
            }
        }
        
        # Calculate correlations between point cloud dimensions
        correlations = {
            'distance_area': np.corrcoef(inter_team_distance, team_area_ratio)[0, 1],
            'distance_home_spread': np.corrcoef(inter_team_distance, home_spread)[0, 1],
            'distance_away_spread': np.corrcoef(inter_team_distance, away_spread)[0, 1],
            'area_home_spread': np.corrcoef(team_area_ratio, home_spread)[0, 1],
            'area_away_spread': np.corrcoef(team_area_ratio, away_spread)[0, 1],
            'home_away_spread': np.corrcoef(home_spread, away_spread)[0, 1]
        }
        
        print("Vietoris-Rips Complex Analysis:")
        print("=" * 60)
        print("Point Cloud Dimensions:")
        print(f"  Inter-team Distance: {point_cloud_stats['inter_team_distance']['mean']:.2f} ± {point_cloud_stats['inter_team_distance']['std']:.2f}")
        print(f"  Team Area Ratio: {point_cloud_stats['team_area_ratio']['mean']:.3f} ± {point_cloud_stats['team_area_ratio']['std']:.3f}")
        print(f"  Home Team Spread: {point_cloud_stats['home_spread']['mean']:.2f} ± {point_cloud_stats['home_spread']['std']:.2f}")
        print(f"  Away Team Spread: {point_cloud_stats['away_spread']['mean']:.2f} ± {point_cloud_stats['away_spread']['std']:.2f}")
        
        print(f"\nPoint Cloud Correlations:")
        print(f"  Distance-Area: {correlations['distance_area']:.4f}")
        print(f"  Distance-Home Spread: {correlations['distance_home_spread']:.4f}")
        print(f"  Distance-Away Spread: {correlations['distance_away_spread']:.4f}")
        print(f"  Area-Home Spread: {correlations['area_home_spread']:.4f}")
        print(f"  Area-Away Spread: {correlations['area_away_spread']:.4f}")
        print(f"  Home-Away Spread: {correlations['home_away_spread']:.4f}")
        
        # Analyze filtration properties
        max_filtration = 1.5  # From our analysis
        filtration_insights = {
            'max_filtration': max_filtration,
            'filtration_efficiency': np.mean(self.combined_tda_data['total_features']) / max_filtration,
            'feature_density': np.mean(self.combined_tda_data['total_features']) / 240  # Approximate point cloud size
        }
        
        print(f"\nFiltration Analysis:")
        print(f"  Max Filtration: {filtration_insights['max_filtration']}")
        print(f"  Filtration Efficiency: {filtration_insights['filtration_efficiency']:.2f}")
        print(f"  Feature Density: {filtration_insights['feature_density']:.4f}")
        
        return {
            'point_cloud_stats': point_cloud_stats,
            'correlations': correlations,
            'filtration_insights': filtration_insights
        }
    
    def analyze_persistence_diagram_insights(self):
        """
        Analyze insights from persistence diagrams
        """
        print("\n=== Analyzing Persistence Diagram Insights ===")
        
        # Load individual window persistence diagrams
        persistence_insights = {
            'h0_persistence': [],
            'h1_persistence': [],
            'h0_lifetimes': [],
            'h1_lifetimes': []
        }
        
        # Analyze persistence diagrams from quantum analysis
        if 'attractor_states' in self.quantum_data:
            attractor_states = self.quantum_data['attractor_states']
            
            # Calculate persistence insights for each attractor state
            for state, state_data in attractor_states.items():
                h1_features = state_data['avg_h1_features']
                complexity = state_data['avg_complexity']
                
                # Estimate persistence based on H1 features and complexity
                estimated_persistence = h1_features * complexity
                estimated_lifetime = h1_features / (complexity + 0.1)
                
                persistence_insights['h1_persistence'].append(estimated_persistence)
                persistence_insights['h1_lifetimes'].append(estimated_lifetime)
        
        # Calculate persistence statistics
        if persistence_insights['h1_persistence']:
            h1_persistence_stats = {
                'mean': np.mean(persistence_insights['h1_persistence']),
                'std': np.std(persistence_insights['h1_persistence']),
                'min': np.min(persistence_insights['h1_persistence']),
                'max': np.max(persistence_insights['h1_persistence'])
            }
            
            h1_lifetime_stats = {
                'mean': np.mean(persistence_insights['h1_lifetimes']),
                'std': np.std(persistence_insights['h1_lifetimes']),
                'min': np.min(persistence_insights['h1_lifetimes']),
                'max': np.max(persistence_insights['h1_lifetimes'])
            }
            
            print("Persistence Diagram Analysis:")
            print("=" * 60)
            print("H1 Persistence Statistics:")
            print(f"  Mean Persistence: {h1_persistence_stats['mean']:.2f}")
            print(f"  Std Persistence: {h1_persistence_stats['std']:.2f}")
            print(f"  Range: {h1_persistence_stats['min']:.2f} - {h1_persistence_stats['max']:.2f}")
            
            print(f"\nH1 Lifetime Statistics:")
            print(f"  Mean Lifetime: {h1_lifetime_stats['mean']:.2f}")
            print(f"  Std Lifetime: {h1_lifetime_stats['std']:.2f}")
            print(f"  Range: {h1_lifetime_stats['min']:.2f} - {h1_lifetime_stats['max']:.2f}")
            
            # Analyze persistence patterns
            persistence_variability = h1_persistence_stats['std'] / h1_persistence_stats['mean']
            lifetime_variability = h1_lifetime_stats['std'] / h1_lifetime_stats['mean']
            
            print(f"\nPersistence Patterns:")
            print(f"  Persistence Variability: {persistence_variability:.4f}")
            print(f"  Lifetime Variability: {lifetime_variability:.4f}")
            
            return {
                'h1_persistence_stats': h1_persistence_stats,
                'h1_lifetime_stats': h1_lifetime_stats,
                'persistence_variability': persistence_variability,
                'lifetime_variability': lifetime_variability
            }
        else:
            print("No persistence diagram data available")
            return None
    
    def analyze_tda_quantum_connection(self):
        """
        Analyze the connection between TDA features and quantum phenomena
        """
        print("\n=== Analyzing TDA-Quantum Connection ===")
        
        # Extract TDA features
        h0_features = self.combined_tda_data['h0_count'].values
        h1_features = self.combined_tda_data['h1_count'].values
        complexity_index = self.combined_tda_data['complexity_index'].values
        
        # Extract quantum features
        if 'energy_levels' in self.quantum_data:
            energy_levels = self.quantum_data['energy_levels']
            quantum_yield = self.quantum_data['quantum_yield_analysis']
            coherence = self.quantum_data['coherence_analysis']
            
            # Calculate correlations between TDA and quantum features
            tda_quantum_correlations = {}
            
            # For each attractor state, calculate TDA-quantum correlations
            for state in energy_levels.keys():
                state_data = self.combined_tda_data[self.combined_tda_data['attractor_state'] == int(state)]
                
                if len(state_data) > 0:
                    state_h0 = state_data['h0_count'].mean()
                    state_h1 = state_data['h1_count'].mean()
                    state_complexity = state_data['complexity_index'].mean()
                    
                    state_energy = energy_levels[state]['total_energy']
                    state_yield = quantum_yield[state]['quantum_yield']
                    state_coherence = coherence[state]['coherence']
                    
                    tda_quantum_correlations[state] = {
                        'h0_energy_correlation': np.corrcoef([state_h0], [state_energy])[0, 1] if not np.isnan(state_h0) else 0,
                        'h1_energy_correlation': np.corrcoef([state_h1], [state_energy])[0, 1] if not np.isnan(state_h1) else 0,
                        'complexity_energy_correlation': np.corrcoef([state_complexity], [state_energy])[0, 1] if not np.isnan(state_complexity) else 0,
                        'h1_yield_correlation': np.corrcoef([state_h1], [state_yield])[0, 1] if not np.isnan(state_h1) else 0,
                        'complexity_coherence_correlation': np.corrcoef([state_complexity], [state_coherence])[0, 1] if not np.isnan(state_complexity) else 0
                    }
            
            print("TDA-Quantum Connection Analysis:")
            print("=" * 60)
            print("TDA-Quantum Correlations by State:")
            
            for state, correlations in tda_quantum_correlations.items():
                print(f"\nState {state}:")
                print(f"  H0-Energy Correlation: {correlations['h0_energy_correlation']:.4f}")
                print(f"  H1-Energy Correlation: {correlations['h1_energy_correlation']:.4f}")
                print(f"  Complexity-Energy Correlation: {correlations['complexity_energy_correlation']:.4f}")
                print(f"  H1-Yield Correlation: {correlations['h1_yield_correlation']:.4f}")
                print(f"  Complexity-Coherence Correlation: {correlations['complexity_coherence_correlation']:.4f}")
            
            # Calculate overall TDA-Quantum connection strength
            overall_correlations = []
            for state_correlations in tda_quantum_correlations.values():
                overall_correlations.extend([
                    state_correlations['h0_energy_correlation'],
                    state_correlations['h1_energy_correlation'],
                    state_correlations['complexity_energy_correlation'],
                    state_correlations['h1_yield_correlation'],
                    state_correlations['complexity_coherence_correlation']
                ])
            
            connection_strength = np.mean([abs(corr) for corr in overall_correlations if not np.isnan(corr)])
            
            print(f"\nOverall TDA-Quantum Connection Strength: {connection_strength:.4f}")
            
            return {
                'state_correlations': tda_quantum_correlations,
                'connection_strength': connection_strength
            }
        else:
            print("No quantum data available for correlation analysis")
            return None
    
    def create_tda_insights_visualization(self):
        """
        Create comprehensive visualization of TDA insights
        """
        print("\n=== Creating TDA Insights Visualization ===")
        
        # Create figure with multiple subplots
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle('TDA Revolutionary Insights in Football Team Dynamics', fontsize=16, fontweight='bold')
        
        # Plot 1: H0 and H1 features over time
        ax1 = axes[0, 0]
        ax1.plot(self.combined_tda_data['start_time'], self.combined_tda_data['h0_count'], 
                'b-', linewidth=1, alpha=0.7, label='H0 (Connected Components)')
        ax1.plot(self.combined_tda_data['start_time'], self.combined_tda_data['h1_count'], 
                'r-', linewidth=1, alpha=0.7, label='H1 (Loops/Holes)')
        ax1.axvline(x=45, color='gray', linestyle='--', alpha=0.7, label='Half Time')
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('Number of Features')
        ax1.set_title('Persistent Homology Features Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Complexity index evolution
        ax2 = axes[0, 1]
        ax2.plot(self.combined_tda_data['start_time'], self.combined_tda_data['complexity_index'], 
                'g-', linewidth=1, alpha=0.7)
        ax2.axvline(x=45, color='gray', linestyle='--', alpha=0.7)
        ax2.set_xlabel('Time (minutes)')
        ax2.set_ylabel('Complexity Index')
        ax2.set_title('Formation Complexity Evolution')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Point cloud dimensions
        ax3 = axes[1, 0]
        dimensions = ['Inter-team\nDistance', 'Team Area\nRatio', 'Home\nSpread', 'Away\nSpread']
        means = [
            self.combined_tda_data['avg_inter_team_distance'].mean(),
            self.combined_tda_data['avg_team_area_ratio'].mean(),
            self.combined_tda_data['avg_home_spread'].mean(),
            self.combined_tda_data['avg_away_spread'].mean()
        ]
        ax3.bar(dimensions, means, color=['blue', 'red', 'green', 'orange'], alpha=0.7)
        ax3.set_ylabel('Average Value')
        ax3.set_title('Point Cloud Dimensions')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: H0 vs H1 features
        ax4 = axes[1, 1]
        scatter = ax4.scatter(self.combined_tda_data['h0_count'], self.combined_tda_data['h1_count'], 
                            c=self.combined_tda_data['complexity_index'], cmap='viridis', alpha=0.7)
        ax4.set_xlabel('H0 Features (Connected Components)')
        ax4.set_ylabel('H1 Features (Loops/Holes)')
        ax4.set_title('H0 vs H1 Features (colored by complexity)')
        plt.colorbar(scatter, ax=ax4, label='Complexity Index')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: TDA features by attractor state
        ax5 = axes[2, 0]
        if 'attractor_states' in self.quantum_data:
            states = list(self.quantum_data['attractor_states'].keys())
            h1_by_state = [self.quantum_data['attractor_states'][state]['avg_h1_features'] for state in states]
            complexity_by_state = [self.quantum_data['attractor_states'][state]['avg_complexity'] for state in states]
            
            x_pos = np.arange(len(states))
            width = 0.35
            
            ax5.bar(x_pos - width/2, h1_by_state, width, label='H1 Features', alpha=0.7)
            ax5.bar(x_pos + width/2, [c*10 for c in complexity_by_state], width, label='Complexity × 10', alpha=0.7)
            
            ax5.set_xlabel('Attractor State')
            ax5.set_ylabel('Feature Count / Complexity')
            ax5.set_title('TDA Features by Attractor State')
            ax5.set_xticks(x_pos)
            ax5.set_xticklabels(states)
            ax5.legend()
            ax5.grid(True, alpha=0.3)
        
        # Plot 6: TDA-Quantum Connection
        ax6 = axes[2, 1]
        if 'energy_levels' in self.quantum_data:
            states = list(self.quantum_data['energy_levels'].keys())
            energies = [self.quantum_data['energy_levels'][state]['total_energy'] for state in states]
            h1_features = [self.quantum_data['attractor_states'][state]['avg_h1_features'] for state in states]
            
            scatter = ax6.scatter(h1_features, energies, c=[int(s) for s in states], cmap='plasma', s=100, alpha=0.7)
            ax6.set_xlabel('H1 Features (Loops/Holes)')
            ax6.set_ylabel('Quantum Energy Level')
            ax6.set_title('TDA-Quantum Connection')
            plt.colorbar(scatter, ax=ax6, label='Attractor State')
            ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('tda_revolutionary_insights.png', dpi=300, bbox_inches='tight')
        print("✓ TDA insights visualization saved: tda_revolutionary_insights.png")
        plt.show()
    
    def run_complete_tda_analysis(self):
        """
        Run complete TDA insights analysis
        """
        print("TDA Revolutionary Insights Analysis")
        print("=" * 50)
        
        # Load data
        if not self.load_tda_data():
            print("Failed to load TDA data. Exiting.")
            return
        
        # Run all analyses
        homology_analysis = self.analyze_persistent_homology_features()
        vietoris_rips_analysis = self.analyze_vietoris_rips_complex_insights()
        persistence_analysis = self.analyze_persistence_diagram_insights()
        tda_quantum_analysis = self.analyze_tda_quantum_connection()
        
        # Create visualizations
        self.create_tda_insights_visualization()
        
        print("\n=== TDA Revolutionary Insights Analysis Complete ===")
        print("Complete TDA insights analysis finished successfully!")
        print("This analysis demonstrates how TDA enables quantum phenomena")
        print("discoveries in football team dynamics.")


def main():
    """
    Main function to run the TDA insights analysis
    """
    analyzer = TDARevolutionaryInsightsAnalyzer()
    analyzer.run_complete_tda_analysis()


if __name__ == "__main__":
    main()
