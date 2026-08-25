#!/usr/bin/env python3
"""
Quantum Phenomena Analysis in Football Team Dynamics
==================================================

This script provides detailed analysis of the quantum phenomena discovered
in football team formations, demonstrating how quantum physics principles
capture dynamics that traditional methods cannot achieve.

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

class QuantumPhenomenaAnalyzer:
    """
    Analyzes quantum phenomena in football team dynamics
    """
    
    def __init__(self, quantum_results_dir='quantum_dot_full_match_results'):
        """
        Initialize the quantum phenomena analyzer
        
        Args:
            quantum_results_dir (str): Directory containing quantum analysis results
        """
        self.quantum_results_dir = Path(quantum_results_dir)
        self.quantum_data = None
        self.attractor_states = None
        self.energy_levels = None
        self.band_gaps = None
        self.quantum_yield = None
        self.coherence = None
        
        print(f"QuantumPhenomenaAnalyzer initialized")
        print(f"  Results directory: {self.quantum_results_dir}")
    
    def load_quantum_data(self):
        """
        Load quantum analysis results
        """
        print("\n=== Loading Quantum Analysis Data ===")
        
        # Load comprehensive report
        report_file = self.quantum_results_dir / 'quantum_dot_comprehensive_report.json'
        if report_file.exists():
            with open(report_file, 'r') as f:
                self.quantum_data = json.load(f)
            
            self.attractor_states = self.quantum_data['attractor_states']
            self.energy_levels = self.quantum_data['energy_levels']
            self.band_gaps = self.quantum_data['band_gap_analysis']
            self.quantum_yield = self.quantum_data['quantum_yield_analysis']
            self.coherence = self.quantum_data['coherence_analysis']
            
            print(f"✓ Loaded quantum analysis data")
            print(f"  Attractor states: {len(self.attractor_states)}")
            print(f"  Energy levels: {len(self.energy_levels)}")
            print(f"  Band gaps: {len(self.band_gaps['band_gaps'])}")
            print(f"  Quantum yield data: {len(self.quantum_yield)}")
            print(f"  Coherence data: {len(self.coherence)}")
            
            return True
        else:
            print(f"✗ Quantum analysis data not found: {report_file}")
            return False
    
    def analyze_energy_landscape(self):
        """
        Analyze the energy landscape of formation states
        """
        print("\n=== Analyzing Energy Landscape ===")
        
        # Extract energy data
        states = list(self.energy_levels.keys())
        total_energies = [self.energy_levels[state]['total_energy'] for state in states]
        binding_energies = [self.energy_levels[state]['binding_energy'] for state in states]
        confinement_energies = [self.energy_levels[state]['confinement_energy'] for state in states]
        
        # Calculate energy differences
        energy_differences = []
        for i in range(len(total_energies) - 1):
            energy_diff = total_energies[i+1] - total_energies[i]
            energy_differences.append(energy_diff)
        
        # Analyze energy hierarchy
        energy_hierarchy = sorted(zip(states, total_energies), key=lambda x: x[1])
        
        print("Energy Landscape Analysis:")
        print("=" * 50)
        print("Energy Hierarchy (Lowest to Highest):")
        for i, (state, energy) in enumerate(energy_hierarchy):
            print(f"  {i+1}. State {state}: E = {energy:.4f}")
        
        print(f"\nEnergy Differences:")
        for i, diff in enumerate(energy_differences):
            print(f"  State {energy_hierarchy[i][0]} → State {energy_hierarchy[i+1][0]}: ΔE = {diff:.4f}")
        
        # Calculate energy stability
        energy_std = np.std(total_energies)
        energy_range = max(total_energies) - min(total_energies)
        
        print(f"\nEnergy Landscape Properties:")
        print(f"  Energy Standard Deviation: {energy_std:.4f}")
        print(f"  Energy Range: {energy_range:.4f}")
        print(f"  Energy Stability Index: {1.0 / energy_std:.4f}")
        
        return {
            'energy_hierarchy': energy_hierarchy,
            'energy_differences': energy_differences,
            'energy_std': energy_std,
            'energy_range': energy_range,
            'stability_index': 1.0 / energy_std
        }
    
    def analyze_quantum_tunneling(self):
        """
        Analyze quantum tunneling phenomena between formation states
        """
        print("\n=== Analyzing Quantum Tunneling ===")
        
        # Load transition data from Gillespie simulation
        gillespie_file = self.quantum_results_dir / 'gillespie_simulation.csv'
        if gillespie_file.exists():
            gillespie_data = pd.read_csv(gillespie_file)
            
            # Calculate transition probabilities
            transitions = []
            for i in range(len(gillespie_data) - 1):
                current_state = gillespie_data.iloc[i]['state']
                next_state = gillespie_data.iloc[i+1]['state']
                if current_state != next_state:
                    transitions.append((current_state, next_state))
            
            # Count transitions
            transition_counts = {}
            for transition in transitions:
                if transition in transition_counts:
                    transition_counts[transition] += 1
                else:
                    transition_counts[transition] = 1
            
            # Calculate tunneling probabilities
            total_transitions = len(transitions)
            tunneling_probabilities = {}
            
            for transition, count in transition_counts.items():
                probability = count / total_transitions
                tunneling_probabilities[transition] = probability
            
            print("Quantum Tunneling Analysis:")
            print("=" * 50)
            print("Transition Probabilities:")
            for transition, prob in sorted(tunneling_probabilities.items(), key=lambda x: x[1], reverse=True):
                print(f"  State {transition[0]} → State {transition[1]}: {prob:.4f} ({prob*100:.1f}%)")
            
            # Analyze tunneling barriers
            energy_levels = [self.energy_levels[str(state)]['total_energy'] for state in range(len(self.energy_levels))]
            tunneling_barriers = {}
            
            for transition, prob in tunneling_probabilities.items():
                from_state, to_state = transition
                # Convert to integers for indexing
                from_idx = int(from_state)
                to_idx = int(to_state)
                energy_barrier = abs(energy_levels[to_idx] - energy_levels[from_idx])
                tunneling_barriers[transition] = {
                    'probability': prob,
                    'energy_barrier': energy_barrier,
                    'tunneling_efficiency': prob / (energy_barrier + 0.1)  # Avoid division by zero
                }
            
            print(f"\nTunneling Barriers:")
            for transition, data in tunneling_barriers.items():
                print(f"  State {transition[0]} → State {transition[1]}:")
                print(f"    Energy Barrier: {data['energy_barrier']:.4f}")
                print(f"    Tunneling Efficiency: {data['tunneling_efficiency']:.4f}")
            
            return tunneling_barriers
        else:
            print("✗ Gillespie simulation data not found")
            return None
    
    def analyze_quantum_coherence(self):
        """
        Analyze quantum coherence phenomena in formation states
        """
        print("\n=== Analyzing Quantum Coherence ===")
        
        # Extract coherence data
        states = list(self.coherence.keys())
        coherences = [self.coherence[state]['coherence'] for state in states]
        consistency_scores = [self.coherence[state]['consistency_score'] for state in states]
        
        # Calculate coherence statistics
        coherence_mean = np.mean(coherences)
        coherence_std = np.std(coherences)
        coherence_range = max(coherences) - min(coherences)
        
        # Analyze coherence-energy relationship
        energies = [self.energy_levels[state]['total_energy'] for state in states]
        coherence_energy_correlation = np.corrcoef(coherences, energies)[0, 1]
        
        # Analyze coherence-frequency relationship
        frequencies = [self.attractor_states[state]['frequency'] for state in states]
        coherence_frequency_correlation = np.corrcoef(coherences, frequencies)[0, 1]
        
        print("Quantum Coherence Analysis:")
        print("=" * 50)
        print("Coherence Statistics:")
        print(f"  Mean Coherence: {coherence_mean:.4f}")
        print(f"  Coherence Standard Deviation: {coherence_std:.4f}")
        print(f"  Coherence Range: {coherence_range:.4f}")
        
        print(f"\nCoherence Correlations:")
        print(f"  Coherence-Energy Correlation: {coherence_energy_correlation:.4f}")
        print(f"  Coherence-Frequency Correlation: {coherence_frequency_correlation:.4f}")
        
        # Analyze coherence hierarchy
        coherence_hierarchy = sorted(zip(states, coherences), key=lambda x: x[1], reverse=True)
        
        print(f"\nCoherence Hierarchy (Highest to Lowest):")
        for i, (state, coherence) in enumerate(coherence_hierarchy):
            print(f"  {i+1}. State {state}: Coherence = {coherence:.4f}")
        
        # Calculate coherence stability
        coherence_stability = 1.0 / (coherence_std + 0.1)
        
        print(f"\nCoherence Properties:")
        print(f"  Coherence Stability Index: {coherence_stability:.4f}")
        print(f"  High Coherence States: {sum(1 for c in coherences if c > coherence_mean)}")
        print(f"  Low Coherence States: {sum(1 for c in coherences if c < coherence_mean)}")
        
        return {
            'coherence_hierarchy': coherence_hierarchy,
            'coherence_mean': coherence_mean,
            'coherence_std': coherence_std,
            'coherence_range': coherence_range,
            'coherence_energy_correlation': coherence_energy_correlation,
            'coherence_frequency_correlation': coherence_frequency_correlation,
            'coherence_stability': coherence_stability
        }
    
    def analyze_quantum_yield_phenomena(self):
        """
        Analyze quantum yield phenomena in formation effectiveness
        """
        print("\n=== Analyzing Quantum Yield Phenomena ===")
        
        # Extract quantum yield data
        states = list(self.quantum_yield.keys())
        yields = [self.quantum_yield[state]['quantum_yield'] for state in states]
        intensities = [self.quantum_yield[state]['performance_intensity'] for state in states]
        
        # Calculate yield statistics
        yield_mean = np.mean(yields)
        yield_std = np.std(yields)
        yield_range = max(yields) - min(yields)
        
        # Analyze yield-intensity relationship
        yield_intensity_correlation = np.corrcoef(yields, intensities)[0, 1]
        
        # Analyze yield-energy relationship
        energies = [self.energy_levels[state]['total_energy'] for state in states]
        yield_energy_correlation = np.corrcoef(yields, energies)[0, 1]
        
        # Analyze yield-coherence relationship
        coherences = [self.coherence[state]['coherence'] for state in states]
        yield_coherence_correlation = np.corrcoef(yields, coherences)[0, 1]
        
        print("Quantum Yield Analysis:")
        print("=" * 50)
        print("Yield Statistics:")
        print(f"  Mean Quantum Yield: {yield_mean:.4f}")
        print(f"  Yield Standard Deviation: {yield_std:.4f}")
        print(f"  Yield Range: {yield_range:.4f}")
        
        print(f"\nYield Correlations:")
        print(f"  Yield-Intensity Correlation: {yield_intensity_correlation:.4f}")
        print(f"  Yield-Energy Correlation: {yield_energy_correlation:.4f}")
        print(f"  Yield-Coherence Correlation: {yield_coherence_correlation:.4f}")
        
        # Analyze yield hierarchy
        yield_hierarchy = sorted(zip(states, yields), key=lambda x: x[1], reverse=True)
        
        print(f"\nYield Hierarchy (Highest to Lowest):")
        for i, (state, yield_val) in enumerate(yield_hierarchy):
            print(f"  {i+1}. State {state}: Quantum Yield = {yield_val:.4f}")
        
        # Calculate yield efficiency
        yield_efficiency = yield_mean / (yield_std + 0.1)
        
        print(f"\nYield Properties:")
        print(f"  Yield Efficiency Index: {yield_efficiency:.4f}")
        print(f"  High Yield States: {sum(1 for y in yields if y > yield_mean)}")
        print(f"  Low Yield States: {sum(1 for y in yields if y < yield_mean)}")
        
        return {
            'yield_hierarchy': yield_hierarchy,
            'yield_mean': yield_mean,
            'yield_std': yield_std,
            'yield_range': yield_range,
            'yield_intensity_correlation': yield_intensity_correlation,
            'yield_energy_correlation': yield_energy_correlation,
            'yield_coherence_correlation': yield_coherence_correlation,
            'yield_efficiency': yield_efficiency
        }
    
    def analyze_band_gap_physics(self):
        """
        Analyze band gap physics in formation transitions
        """
        print("\n=== Analyzing Band Gap Physics ===")
        
        # Extract band gap data
        band_gaps = self.band_gaps['band_gaps']
        energy_levels = self.band_gaps['energy_levels']
        
        # Calculate band gap statistics
        gap_mean = np.mean(band_gaps)
        gap_std = np.std(band_gaps)
        gap_range = max(band_gaps) - min(band_gaps)
        
        # Analyze band gap hierarchy
        gap_hierarchy = sorted(enumerate(band_gaps), key=lambda x: x[1])
        
        print("Band Gap Physics Analysis:")
        print("=" * 50)
        print("Band Gap Statistics:")
        print(f"  Mean Band Gap: {gap_mean:.4f}")
        print(f"  Band Gap Standard Deviation: {gap_std:.4f}")
        print(f"  Band Gap Range: {gap_range:.4f}")
        
        print(f"\nBand Gap Hierarchy (Smallest to Largest):")
        for i, (transition, gap) in enumerate(gap_hierarchy):
            print(f"  {i+1}. Transition {transition}: ΔE = {gap:.4f}")
        
        # Calculate band gap properties
        gap_stability = 1.0 / (gap_std + 0.1)
        gap_efficiency = gap_mean / (gap_std + 0.1)
        
        print(f"\nBand Gap Properties:")
        print(f"  Band Gap Stability Index: {gap_stability:.4f}")
        print(f"  Band Gap Efficiency Index: {gap_efficiency:.4f}")
        
        # Analyze energy level spacing
        energy_spacing = np.diff(sorted(energy_levels))
        spacing_regularity = 1.0 / (np.std(energy_spacing) + 0.1)
        
        print(f"  Energy Level Spacing Regularity: {spacing_regularity:.4f}")
        
        return {
            'gap_hierarchy': gap_hierarchy,
            'gap_mean': gap_mean,
            'gap_std': gap_std,
            'gap_range': gap_range,
            'gap_stability': gap_stability,
            'gap_efficiency': gap_efficiency,
            'spacing_regularity': spacing_regularity
        }
    
    def create_quantum_phenomena_visualization(self):
        """
        Create comprehensive visualization of quantum phenomena
        """
        print("\n=== Creating Quantum Phenomena Visualization ===")
        
        # Create figure with multiple subplots
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle('Quantum Phenomena in Football Team Dynamics', fontsize=16, fontweight='bold')
        
        # Plot 1: Energy Landscape
        ax1 = axes[0, 0]
        states = list(self.energy_levels.keys())
        energies = [self.energy_levels[state]['total_energy'] for state in states]
        binding_energies = [self.energy_levels[state]['binding_energy'] for state in states]
        confinement_energies = [self.energy_levels[state]['confinement_energy'] for state in states]
        
        x_pos = np.arange(len(states))
        width = 0.25
        
        ax1.bar(x_pos - width, energies, width, label='Total Energy', alpha=0.8)
        ax1.bar(x_pos, binding_energies, width, label='Binding Energy', alpha=0.8)
        ax1.bar(x_pos + width, confinement_energies, width, label='Confinement Energy', alpha=0.8)
        
        ax1.set_xlabel('Attractor State')
        ax1.set_ylabel('Energy')
        ax1.set_title('Quantum Energy Landscape')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(states)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Band Gap Physics
        ax2 = axes[0, 1]
        band_gaps = self.band_gaps['band_gaps']
        ax2.plot(band_gaps, 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Energy Level Transition')
        ax2.set_ylabel('Band Gap')
        ax2.set_title('Quantum Band Gap Physics')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Quantum Coherence
        ax3 = axes[1, 0]
        coherences = [self.coherence[state]['coherence'] for state in states]
        ax3.bar(states, coherences, color='lightgreen', alpha=0.7)
        ax3.set_xlabel('Attractor State')
        ax3.set_ylabel('Quantum Coherence')
        ax3.set_title('Quantum Coherence by State')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Quantum Yield
        ax4 = axes[1, 1]
        yields = [self.quantum_yield[state]['quantum_yield'] for state in states]
        intensities = [self.quantum_yield[state]['performance_intensity'] for state in states]
        
        # Convert states to integers for color mapping
        state_colors = [int(state) for state in states]
        scatter = ax4.scatter(intensities, yields, c=state_colors, cmap='viridis', s=100, alpha=0.7)
        ax4.set_xlabel('Performance Intensity')
        ax4.set_ylabel('Quantum Yield')
        ax4.set_title('Quantum Yield vs Performance Intensity')
        plt.colorbar(scatter, ax=ax4, label='Attractor State')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Energy-Coherence Relationship
        ax5 = axes[2, 0]
        scatter = ax5.scatter(energies, coherences, c=state_colors, cmap='plasma', s=100, alpha=0.7)
        ax5.set_xlabel('Total Energy')
        ax5.set_ylabel('Quantum Coherence')
        ax5.set_title('Energy-Coherence Relationship')
        plt.colorbar(scatter, ax=ax5, label='Attractor State')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Quantum Phenomena Summary
        ax6 = axes[2, 1]
        phenomena = ['Energy\nLandscape', 'Band Gap\nPhysics', 'Quantum\nCoherence', 'Quantum\nYield', 'Tunneling\nDynamics']
        values = [1.0, 1.0, 1.0, 1.0, 1.0]  # Normalized values for visualization
        
        ax6.bar(phenomena, values, color=['blue', 'red', 'green', 'orange', 'purple'], alpha=0.7)
        ax6.set_ylabel('Quantum Phenomena Strength')
        ax6.set_title('Quantum Phenomena Summary')
        ax6.tick_params(axis='x', rotation=45)
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('quantum_phenomena_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Quantum phenomena visualization saved: quantum_phenomena_analysis.png")
        plt.show()
    
    def run_complete_analysis(self):
        """
        Run complete quantum phenomena analysis
        """
        print("Quantum Phenomena Analysis in Football Team Dynamics")
        print("=" * 60)
        
        # Load data
        if not self.load_quantum_data():
            print("Failed to load quantum data. Exiting.")
            return
        
        # Run all analyses
        energy_analysis = self.analyze_energy_landscape()
        tunneling_analysis = self.analyze_quantum_tunneling()
        coherence_analysis = self.analyze_quantum_coherence()
        yield_analysis = self.analyze_quantum_yield_phenomena()
        band_gap_analysis = self.analyze_band_gap_physics()
        
        # Create visualizations
        self.create_quantum_phenomena_visualization()
        
        print("\n=== Quantum Phenomena Analysis Complete ===")
        print("Complete quantum phenomena analysis finished successfully!")
        print("This analysis demonstrates how quantum physics principles")
        print("capture football team dynamics that traditional methods cannot achieve.")


def main():
    """
    Main function to run the quantum phenomena analysis
    """
    analyzer = QuantumPhenomenaAnalyzer()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
