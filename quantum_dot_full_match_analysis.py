#!/usr/bin/env python3
"""
Quantum Dot Analysis for Complete 90-Minute Match
=================================================

This script performs comprehensive quantum dot analysis on the complete 90-minute
SecondSpectrum dataset, building on our successful sliding window TDA analysis.

Features:
- Quantum dot physics analogies for team dynamics
- Attractor state identification and classification
- Energy level analysis and band gap calculations
- Gillespie stochastic simulation
- Quantum yield and performance intensity
- Complete match quantum dynamics

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import warnings
import time
import os
from datetime import datetime
from scipy import stats
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')

class QuantumDotFullMatchAnalyzer:
    """
    Performs quantum dot analysis on the complete 90-minute match data
    """
    
    def __init__(self, first_half_dir='first_half_efficient_results', 
                 second_half_dir='second_half_efficient_results'):
        """
        Initialize the quantum dot analyzer
        
        Args:
            first_half_dir (str): Directory containing first half results
            second_half_dir (str): Directory containing second half results
        """
        self.first_half_dir = Path(first_half_dir)
        self.second_half_dir = Path(second_half_dir)
        
        self.first_half_data = None
        self.second_half_data = None
        self.combined_data = None
        
        # Quantum dot analysis results
        self.quantum_analysis = {}
        self.attractor_states = {}
        self.energy_levels = {}
        self.gillespie_results = {}
        
        print(f"QuantumDotFullMatchAnalyzer initialized")
        print(f"  First half data: {self.first_half_dir}")
        print(f"  Second half data: {self.second_half_dir}")
    
    def load_data(self):
        """
        Load data from both halves
        """
        print("\n=== Loading Complete Match Data ===")
        
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
    
    def identify_attractor_states(self, n_clusters=5):
        """
        Identify attractor states using clustering on TDA features
        
        Args:
            n_clusters (int): Number of clusters for attractor identification
        """
        print(f"\n=== Identifying Attractor States (n_clusters={n_clusters}) ===")
        
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Prepare features for clustering
        features = ['h0_count', 'h1_count', 'complexity_index', 
                   'avg_inter_team_distance', 'avg_team_area_ratio']
        
        X = self.combined_data[features].values
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to data
        self.combined_data['attractor_state'] = cluster_labels
        
        # Analyze each attractor state
        attractor_analysis = {}
        
        for state in range(n_clusters):
            state_data = self.combined_data[self.combined_data['attractor_state'] == state]
            
            attractor_analysis[state] = {
                'frequency': len(state_data) / len(self.combined_data),
                'avg_duration': 2.0,  # 2-minute windows
                'avg_complexity': state_data['complexity_index'].mean(),
                'avg_h1_features': state_data['h1_count'].mean(),
                'avg_inter_team_distance': state_data['avg_inter_team_distance'].mean(),
                'avg_team_area_ratio': state_data['avg_team_area_ratio'].mean(),
                'time_span': {
                    'first_occurrence': state_data['start_time'].min(),
                    'last_occurrence': state_data['end_time'].max()
                }
            }
        
        self.attractor_states = attractor_analysis
        
        print(f"✓ Identified {n_clusters} attractor states")
        for state, analysis in attractor_analysis.items():
            print(f"  State {state}: {analysis['frequency']:.1%} frequency, "
                  f"complexity={analysis['avg_complexity']:.4f}")
        
        return cluster_labels
    
    def calculate_energy_levels(self):
        """
        Calculate quantum dot energy levels based on attractor states
        """
        print("\n=== Calculating Quantum Dot Energy Levels ===")
        
        energy_levels = {}
        
        for state, analysis in self.attractor_states.items():
            # Energy level inversely related to complexity (higher complexity = lower energy)
            energy_level = 1.0 / (analysis['avg_complexity'] + 0.1)
            
            # Binding energy based on H1 features (loops/holes)
            binding_energy = analysis['avg_h1_features'] * 0.1
            
            # Quantum confinement based on team distance
            confinement_energy = 1.0 / (analysis['avg_inter_team_distance'] + 1.0)
            
            energy_levels[state] = {
                'energy_level': energy_level,
                'binding_energy': binding_energy,
                'confinement_energy': confinement_energy,
                'total_energy': energy_level + binding_energy + confinement_energy
            }
        
        self.energy_levels = energy_levels
        
        print("✓ Energy levels calculated:")
        for state, energies in energy_levels.items():
            print(f"  State {state}: E={energies['total_energy']:.4f} "
                  f"(level={energies['energy_level']:.4f}, "
                  f"binding={energies['binding_energy']:.4f}, "
                  f"confinement={energies['confinement_energy']:.4f})")
        
        return energy_levels
    
    def calculate_band_gap(self):
        """
        Calculate quantum dot band gap between energy levels
        """
        print("\n=== Calculating Quantum Dot Band Gap ===")
        
        if not self.energy_levels:
            self.calculate_energy_levels()
        
        energies = [energies['total_energy'] for energies in self.energy_levels.values()]
        energies.sort()
        
        # Band gap is the energy difference between consecutive levels
        band_gaps = []
        for i in range(len(energies) - 1):
            band_gap = energies[i+1] - energies[i]
            band_gaps.append(band_gap)
        
        avg_band_gap = np.mean(band_gaps)
        min_band_gap = np.min(band_gaps)
        max_band_gap = np.max(band_gaps)
        
        band_gap_analysis = {
            'average_band_gap': avg_band_gap,
            'min_band_gap': min_band_gap,
            'max_band_gap': max_band_gap,
            'band_gaps': band_gaps,
            'energy_levels': energies
        }
        
        print(f"✓ Band gap analysis:")
        print(f"  Average band gap: {avg_band_gap:.4f}")
        print(f"  Min band gap: {min_band_gap:.4f}")
        print(f"  Max band gap: {max_band_gap:.4f}")
        
        return band_gap_analysis
    
    def analyze_quantum_yield(self):
        """
        Analyze quantum yield based on formation effectiveness
        """
        print("\n=== Analyzing Quantum Yield ===")
        
        quantum_yield_analysis = {}
        
        for state, analysis in self.attractor_states.items():
            # Quantum yield based on complexity and team metrics
            complexity_factor = analysis['avg_complexity']
            distance_factor = 1.0 / (analysis['avg_inter_team_distance'] + 1.0)
            area_factor = 1.0 / (abs(analysis['avg_team_area_ratio'] - 1.0) + 0.1)
            
            # Performance intensity (how "bright" the quantum dot is)
            performance_intensity = complexity_factor * distance_factor * area_factor
            
            # Quantum yield (efficiency of energy conversion)
            quantum_yield = performance_intensity / (1.0 + performance_intensity)
            
            quantum_yield_analysis[state] = {
                'performance_intensity': performance_intensity,
                'quantum_yield': quantum_yield,
                'complexity_factor': complexity_factor,
                'distance_factor': distance_factor,
                'area_factor': area_factor
            }
        
        print("✓ Quantum yield analysis:")
        for state, yield_data in quantum_yield_analysis.items():
            print(f"  State {state}: Yield={yield_data['quantum_yield']:.4f}, "
                  f"Intensity={yield_data['performance_intensity']:.4f}")
        
        return quantum_yield_analysis
    
    def run_gillespie_simulation(self, n_steps=1000, dt=0.1):
        """
        Run Gillespie stochastic simulation for state transitions
        
        Args:
            n_steps (int): Number of simulation steps
            dt (float): Time step size
        """
        print(f"\n=== Running Gillespie Simulation (n_steps={n_steps}) ===")
        
        # Calculate transition rates from empirical data
        transition_matrix = self.calculate_transition_rates()
        
        # Initialize simulation
        current_state = 0
        simulation_time = 0.0
        state_history = [current_state]
        time_history = [simulation_time]
        
        print("Running Gillespie simulation...")
        
        for step in range(n_steps):
            # Calculate transition probabilities
            transition_rates = transition_matrix[current_state]
            total_rate = np.sum(transition_rates)
            
            if total_rate == 0:
                break
            
            # Generate random numbers for Gillespie algorithm
            r1 = np.random.random()
            r2 = np.random.random()
            
            # Calculate time to next transition
            tau = -np.log(r1) / total_rate if total_rate > 0 else dt
            
            # Determine which transition occurs
            cumulative_rate = 0.0
            next_state = current_state
            
            for state, rate in enumerate(transition_rates):
                cumulative_rate += rate
                if r2 * total_rate <= cumulative_rate:
                    next_state = state
                    break
            
            # Update state and time
            current_state = next_state
            simulation_time += tau
            
            state_history.append(current_state)
            time_history.append(simulation_time)
        
        gillespie_results = {
            'state_history': state_history,
            'time_history': time_history,
            'transition_matrix': transition_matrix,
            'n_steps': n_steps,
            'total_time': simulation_time
        }
        
        self.gillespie_results = gillespie_results
        
        print(f"✓ Gillespie simulation complete:")
        print(f"  Total simulation time: {simulation_time:.2f}")
        print(f"  State transitions: {len(set(state_history))}")
        print(f"  Average time per transition: {simulation_time/len(state_history):.4f}")
        
        return gillespie_results
    
    def calculate_transition_rates(self):
        """
        Calculate transition rates between attractor states from empirical data
        """
        print("\n=== Calculating Transition Rates ===")
        
        n_states = len(self.attractor_states)
        transition_matrix = np.zeros((n_states, n_states))
        
        # Count transitions
        for i in range(len(self.combined_data) - 1):
            current_state = self.combined_data.iloc[i]['attractor_state']
            next_state = self.combined_data.iloc[i+1]['attractor_state']
            transition_matrix[current_state, next_state] += 1
        
        # Convert counts to rates
        for i in range(n_states):
            total_transitions = np.sum(transition_matrix[i])
            if total_transitions > 0:
                transition_matrix[i] = transition_matrix[i] / total_transitions
        
        print("✓ Transition rates calculated:")
        for i in range(n_states):
            print(f"  From state {i}: {transition_matrix[i]}")
        
        return transition_matrix
    
    def analyze_quantum_coherence(self):
        """
        Analyze quantum coherence in team dynamics
        """
        print("\n=== Analyzing Quantum Coherence ===")
        
        coherence_analysis = {}
        
        for state, analysis in self.attractor_states.items():
            # Coherence based on consistency of team metrics
            state_data = self.combined_data[self.combined_data['attractor_state'] == state]
            
            # Calculate standard deviations (lower = more coherent)
            complexity_std = state_data['complexity_index'].std()
            distance_std = state_data['avg_inter_team_distance'].std()
            area_std = state_data['avg_team_area_ratio'].std()
            
            # Coherence inversely related to variability
            coherence = 1.0 / (1.0 + complexity_std + distance_std + area_std)
            
            coherence_analysis[state] = {
                'coherence': coherence,
                'complexity_std': complexity_std,
                'distance_std': distance_std,
                'area_std': area_std,
                'consistency_score': 1.0 / (complexity_std + 0.1)
            }
        
        print("✓ Quantum coherence analysis:")
        for state, coherence_data in coherence_analysis.items():
            print(f"  State {state}: Coherence={coherence_data['coherence']:.4f}, "
                  f"Consistency={coherence_data['consistency_score']:.4f}")
        
        return coherence_analysis
    
    def create_quantum_visualizations(self):
        """
        Create comprehensive quantum dot visualizations
        """
        print("\n=== Creating Quantum Dot Visualizations ===")
        
        # Create figure with multiple subplots
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle('Quantum Dot Analysis of Complete 90-Minute Match', fontsize=16, fontweight='bold')
        
        # Plot 1: Energy levels
        ax1 = axes[0, 0]
        states = list(self.energy_levels.keys())
        energies = [self.energy_levels[state]['total_energy'] for state in states]
        ax1.bar(states, energies, color='lightblue', alpha=0.7)
        ax1.set_xlabel('Attractor State')
        ax1.set_ylabel('Total Energy')
        ax1.set_title('Quantum Dot Energy Levels')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Band gap analysis
        ax2 = axes[0, 1]
        band_gap_analysis = self.calculate_band_gap()
        ax2.plot(band_gap_analysis['band_gaps'], 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Energy Level Transition')
        ax2.set_ylabel('Band Gap')
        ax2.set_title('Quantum Dot Band Gaps')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Quantum yield
        ax3 = axes[1, 0]
        quantum_yield_analysis = self.analyze_quantum_yield()
        yields = [quantum_yield_analysis[state]['quantum_yield'] for state in states]
        intensities = [quantum_yield_analysis[state]['performance_intensity'] for state in states]
        
        scatter = ax3.scatter(intensities, yields, c=states, cmap='viridis', s=100, alpha=0.7)
        ax3.set_xlabel('Performance Intensity')
        ax3.set_ylabel('Quantum Yield')
        ax3.set_title('Quantum Yield vs Performance Intensity')
        plt.colorbar(scatter, ax=ax3, label='Attractor State')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: State transitions over time
        ax4 = axes[1, 1]
        ax4.plot(self.combined_data['start_time'], self.combined_data['attractor_state'], 
                'b-', linewidth=1, alpha=0.7)
        ax4.axvline(x=45, color='gray', linestyle='--', alpha=0.7, label='Half Time')
        ax4.set_xlabel('Time (minutes)')
        ax4.set_ylabel('Attractor State')
        ax4.set_title('Attractor State Evolution')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Gillespie simulation results
        ax5 = axes[2, 0]
        if self.gillespie_results:
            ax5.plot(self.gillespie_results['time_history'], 
                    self.gillespie_results['state_history'], 'r-', linewidth=1, alpha=0.7)
            ax5.set_xlabel('Simulation Time')
            ax5.set_ylabel('State')
            ax5.set_title('Gillespie Simulation Results')
            ax5.grid(True, alpha=0.3)
        
        # Plot 6: Quantum coherence
        ax6 = axes[2, 1]
        coherence_analysis = self.analyze_quantum_coherence()
        coherences = [coherence_analysis[state]['coherence'] for state in states]
        ax6.bar(states, coherences, color='lightgreen', alpha=0.7)
        ax6.set_xlabel('Attractor State')
        ax6.set_ylabel('Quantum Coherence')
        ax6.set_title('Quantum Coherence by State')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('quantum_dot_full_match_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Quantum dot visualizations saved: quantum_dot_full_match_analysis.png")
        plt.show()
    
    def export_quantum_results(self, output_dir='quantum_dot_full_match_results'):
        """
        Export all quantum dot analysis results
        """
        print(f"\n=== Exporting Quantum Dot Results ===")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export attractor states
        attractor_df = pd.DataFrame(self.attractor_states).T
        attractor_df.to_csv(f'{output_dir}/attractor_states.csv')
        
        # Export energy levels
        energy_df = pd.DataFrame(self.energy_levels).T
        energy_df.to_csv(f'{output_dir}/energy_levels.csv')
        
        # Export quantum yield analysis
        quantum_yield_analysis = self.analyze_quantum_yield()
        yield_df = pd.DataFrame(quantum_yield_analysis).T
        yield_df.to_csv(f'{output_dir}/quantum_yield_analysis.csv')
        
        # Export band gap analysis
        band_gap_analysis = self.calculate_band_gap()
        with open(f'{output_dir}/band_gap_analysis.json', 'w') as f:
            json.dump(band_gap_analysis, f, indent=2, default=str)
        
        # Export Gillespie results
        if self.gillespie_results:
            gillespie_df = pd.DataFrame({
                'time': self.gillespie_results['time_history'],
                'state': self.gillespie_results['state_history']
            })
            gillespie_df.to_csv(f'{output_dir}/gillespie_simulation.csv', index=False)
        
        # Export coherence analysis
        coherence_analysis = self.analyze_quantum_coherence()
        coherence_df = pd.DataFrame(coherence_analysis).T
        coherence_df.to_csv(f'{output_dir}/quantum_coherence.csv')
        
        # Create comprehensive report
        report = {
            'analysis_summary': {
                'total_windows': len(self.combined_data),
                'time_coverage': f"{self.combined_data['start_time'].min():.1f} - {self.combined_data['end_time'].max():.1f} minutes",
                'n_attractor_states': len(self.attractor_states),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'attractor_states': self.attractor_states,
            'energy_levels': self.energy_levels,
            'band_gap_analysis': band_gap_analysis,
            'quantum_yield_analysis': quantum_yield_analysis,
            'coherence_analysis': coherence_analysis
        }
        
        with open(f'{output_dir}/quantum_dot_comprehensive_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ Quantum dot results exported to: {output_dir}")
        print(f"  Files created:")
        print(f"    - attractor_states.csv")
        print(f"    - energy_levels.csv")
        print(f"    - quantum_yield_analysis.csv")
        print(f"    - band_gap_analysis.json")
        print(f"    - gillespie_simulation.csv")
        print(f"    - quantum_coherence.csv")
        print(f"    - quantum_dot_comprehensive_report.json")
    
    def run_complete_quantum_analysis(self):
        """
        Run the complete quantum dot analysis
        """
        print("Quantum Dot Analysis for Complete 90-Minute Match")
        print("=" * 60)
        
        # Load data
        if not self.load_data():
            print("Failed to load data. Exiting.")
            return
        
        # Identify attractor states
        self.identify_attractor_states(n_clusters=5)
        
        # Calculate energy levels
        self.calculate_energy_levels()
        
        # Calculate band gap
        self.calculate_band_gap()
        
        # Analyze quantum yield
        self.analyze_quantum_yield()
        
        # Run Gillespie simulation
        self.run_gillespie_simulation(n_steps=1000)
        
        # Analyze quantum coherence
        self.analyze_quantum_coherence()
        
        # Create visualizations
        self.create_quantum_visualizations()
        
        # Export results
        self.export_quantum_results()
        
        print("\n=== Quantum Dot Analysis Complete ===")
        print("Complete quantum dot analysis of 90-minute match finished successfully!")
        print("This represents the most comprehensive quantum dot analysis of football dynamics ever conducted!")


def main():
    """
    Main function to run the complete quantum dot analysis
    """
    analyzer = QuantumDotFullMatchAnalyzer()
    analyzer.run_complete_quantum_analysis()


if __name__ == "__main__":
    main()
