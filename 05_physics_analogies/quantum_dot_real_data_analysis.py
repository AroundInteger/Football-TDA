#!/usr/bin/env python3
"""
Quantum Dot Analysis on Real Multi-Segment Data
==============================================

This script performs quantum dot-inspired analysis on the real multi-segment
TDA results, comparing attractor state dynamics to quantum dot physics.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import json
import os
from pathlib import Path
import warnings
import time
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

class QuantumDotRealDataAnalyzer:
    """
    Quantum dot-inspired analysis of real multi-segment TDA results
    """
    
    def __init__(self, results_dir='parallel_segment_results'):
        """
        Initialize the analyzer
        
        Args:
            results_dir (str): Directory containing parallel segment results
        """
        self.results_dir = results_dir
        self.segments = {}
        self.quantum_analysis = {}
        
        print(f"QuantumDotRealDataAnalyzer initialized")
        print(f"  Results directory: {results_dir}")
    
    def load_segment_results(self):
        """
        Load results from all segments
        """
        print("\n=== Loading Multi-Segment Results ===")
        
        # Load comparative analysis
        comparative_file = f'{self.results_dir}/comparative_analysis.csv'
        if os.path.exists(comparative_file):
            self.comparative_results = pd.read_csv(comparative_file)
            print(f"✓ Loaded comparative results: {len(self.comparative_results)} segments")
        else:
            print("✗ Comparative results not found")
            return False
        
        # Load individual segment results
        segment_names = ['First_Half_Start', 'First_Half_End', 'Second_Half_Start', 'Second_Half_End']
        
        for segment_name in segment_names:
            segment_dir = f'{self.results_dir}/{segment_name}'
            
            if os.path.exists(segment_dir):
                # Load TDA summary
                tda_summary_file = f'{segment_dir}/tda_summary.json'
                if os.path.exists(tda_summary_file):
                    with open(tda_summary_file, 'r') as f:
                        tda_summary = json.load(f)
                    
                    # Load team metrics
                    team_metrics_file = f'{segment_dir}/team_metrics.csv'
                    if os.path.exists(team_metrics_file):
                        team_metrics = pd.read_csv(team_metrics_file)
                        
                        # Load persistence diagrams
                        persistence_diagrams = {}
                        for i in range(3):  # H0, H1, H2
                            diagram_file = f'{segment_dir}/persistence_diagram_H{i}.csv'
                            if os.path.exists(diagram_file):
                                persistence_diagrams[f'H{i}'] = pd.read_csv(diagram_file)
                            else:
                                persistence_diagrams[f'H{i}'] = pd.DataFrame()
                        
                        self.segments[segment_name] = {
                            'tda_summary': tda_summary,
                            'team_metrics': team_metrics,
                            'persistence_diagrams': persistence_diagrams
                        }
                        
                        print(f"✓ Loaded {segment_name}: {tda_summary['total_features']} features")
                    else:
                        print(f"✗ Team metrics not found for {segment_name}")
                else:
                    print(f"✗ TDA summary not found for {segment_name}")
            else:
                print(f"✗ Segment directory not found: {segment_name}")
        
        print(f"✓ Loaded {len(self.segments)} segments successfully")
        return len(self.segments) > 0
    
    def identify_attractor_states(self):
        """
        Identify attractor states from team metrics using clustering
        """
        print("\n=== Identifying Attractor States ===")
        
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        for segment_name, segment_data in self.segments.items():
            print(f"Analyzing {segment_name}...")
            
            team_metrics = segment_data['team_metrics']
            
            # Prepare features for clustering
            features = np.column_stack([
                team_metrics['inter_team_distance'],
                team_metrics['team_area_ratio'],
                team_metrics['home_nod'],
                team_metrics['away_nod'],
                team_metrics['home_spread'],
                team_metrics['away_spread']
            ])
            
            # Remove NaN values
            valid_rows = ~np.isnan(features).any(axis=1)
            features_clean = features[valid_rows]
            
            if len(features_clean) < 10:
                print(f"  ✗ Not enough data for clustering in {segment_name}")
                continue
            
            # Standardize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features_clean)
            
            # Determine optimal number of clusters (3-5 for football)
            best_k = 3
            best_score = -np.inf
            
            for k in range(2, 6):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                kmeans.fit(features_scaled)
                score = -kmeans.inertia_  # Negative inertia as score
                if score > best_score:
                    best_score = score
                    best_k = k
            
            # Perform final clustering
            kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(features_scaled)
            
            # Calculate cluster characteristics
            cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
            
            # Calculate state lifetimes and transition rates
            state_lifetimes = self.calculate_state_lifetimes(cluster_labels)
            transition_matrix = self.calculate_transition_matrix(cluster_labels, best_k)
            
            # Store results
            segment_data['attractor_analysis'] = {
                'n_states': best_k,
                'cluster_labels': cluster_labels,
                'cluster_centers': cluster_centers,
                'state_lifetimes': state_lifetimes,
                'transition_matrix': transition_matrix,
                'features_scaled': features_scaled,
                'scaler': scaler
            }
            
            print(f"  ✓ Identified {best_k} attractor states")
            print(f"  ✓ Average lifetime: {np.mean(state_lifetimes):.1f} frames")
    
    def calculate_state_lifetimes(self, cluster_labels):
        """
        Calculate lifetimes of each state
        """
        lifetimes = []
        current_state = cluster_labels[0]
        current_lifetime = 1
        
        for i in range(1, len(cluster_labels)):
            if cluster_labels[i] == current_state:
                current_lifetime += 1
            else:
                lifetimes.append(current_lifetime)
                current_state = cluster_labels[i]
                current_lifetime = 1
        
        # Add the last lifetime
        lifetimes.append(current_lifetime)
        
        return np.array(lifetimes)
    
    def calculate_transition_matrix(self, cluster_labels, n_states):
        """
        Calculate transition matrix between states
        """
        transition_matrix = np.zeros((n_states, n_states))
        
        for i in range(len(cluster_labels) - 1):
            from_state = cluster_labels[i]
            to_state = cluster_labels[i + 1]
            transition_matrix[from_state, to_state] += 1
        
        # Normalize rows to get probabilities
        row_sums = transition_matrix.sum(axis=1)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        transition_matrix = transition_matrix / row_sums[:, np.newaxis]
        
        return transition_matrix
    
    def analyze_quantum_dot_analogies(self):
        """
        Analyze quantum dot analogies for each segment
        """
        print("\n=== Analyzing Quantum Dot Analogies ===")
        
        for segment_name, segment_data in self.segments.items():
            if 'attractor_analysis' not in segment_data:
                continue
            
            print(f"Analyzing quantum dot analogies for {segment_name}...")
            
            attractor_analysis = segment_data['attractor_analysis']
            tda_summary = segment_data['tda_summary']
            
            # Quantum dot physics parameters
            quantum_analysis = {}
            
            # 1. Team Formation = Quantum Dot Size
            # Formation compactness determines "quantum dot size"
            team_metrics = segment_data['team_metrics']
            formation_compactness = 1.0 / (team_metrics['home_spread'] + team_metrics['away_spread'])
            quantum_analysis['quantum_dot_size'] = {
                'mean': np.mean(formation_compactness),
                'std': np.std(formation_compactness),
                'min': np.min(formation_compactness),
                'max': np.max(formation_compactness)
            }
            
            # 2. Energy Levels = Attractor States
            # Map attractor states to energy levels
            n_states = attractor_analysis['n_states']
            state_lifetimes = attractor_analysis['state_lifetimes']
            
            # Energy levels based on state stability (longer lifetime = lower energy)
            energy_levels = np.zeros(n_states)
            cluster_labels = attractor_analysis['cluster_labels']
            
            for i in range(n_states):
                state_mask = cluster_labels == i
                if np.any(state_mask):
                    # Get lifetimes for this state
                    state_lifetimes_for_state = []
                    current_lifetime = 1
                    current_state = cluster_labels[0]
                    
                    for j in range(1, len(cluster_labels)):
                        if cluster_labels[j] == current_state:
                            current_lifetime += 1
                        else:
                            if current_state == i:
                                state_lifetimes_for_state.append(current_lifetime)
                            current_state = cluster_labels[j]
                            current_lifetime = 1
                    
                    # Add the last lifetime if it's for this state
                    if current_state == i:
                        state_lifetimes_for_state.append(current_lifetime)
                    
                    if state_lifetimes_for_state:
                        avg_lifetime = np.mean(state_lifetimes_for_state)
                        energy_levels[i] = 1.0 / (avg_lifetime + 1)  # Inverse relationship
            
            quantum_analysis['energy_levels'] = energy_levels.tolist()
            
            # 3. Band Gap = Energy difference between states
            if n_states > 1:
                band_gaps = []
                for i in range(n_states):
                    for j in range(i + 1, n_states):
                        band_gap = abs(energy_levels[i] - energy_levels[j])
                        band_gaps.append(band_gap)
                quantum_analysis['band_gap'] = {
                    'mean': np.mean(band_gaps),
                    'std': np.std(band_gaps),
                    'min': np.min(band_gaps),
                    'max': np.max(band_gaps)
                }
            else:
                quantum_analysis['band_gap'] = {'mean': 0, 'std': 0, 'min': 0, 'max': 0}
            
            # 4. Exciton Dynamics = Player Interactions
            # NOD represents binding energy (inverse relationship)
            home_nod = team_metrics['home_nod']
            away_nod = team_metrics['away_nod']
            
            # Binding energy (stronger interactions = lower NOD = higher binding energy)
            binding_energy = 1.0 / (home_nod + away_nod)
            
            quantum_analysis['exciton_dynamics'] = {
                'binding_energy_mean': np.mean(binding_energy),
                'binding_energy_std': np.std(binding_energy),
                'formation_rate': np.mean(1.0 / (home_nod + away_nod)),
                'decay_rate': np.std(home_nod + away_nod),
                'exciton_lifetime': np.mean(home_nod + away_nod)
            }
            
            # 5. Quantum Tunneling = State Transitions
            transition_matrix = attractor_analysis['transition_matrix']
            
            # Tunneling probability based on transition rates
            tunneling_rates = []
            for i in range(n_states):
                for j in range(n_states):
                    if i != j and transition_matrix[i, j] > 0:
                        tunneling_rates.append(transition_matrix[i, j])
            
            quantum_analysis['quantum_tunneling'] = {
                'tunneling_rates': tunneling_rates,
                'mean_tunneling_rate': np.mean(tunneling_rates) if tunneling_rates else 0,
                'tunneling_probability': np.sum(transition_matrix) - np.trace(transition_matrix)
            }
            
            # 6. Photoluminescence = Performance Emission
            # Use topological features as "performance emission"
            h1_count = tda_summary['h1_count']
            h2_count = tda_summary['h2_count']
            total_features = tda_summary['total_features']
            
            # Performance intensity based on topological complexity
            performance_intensity = (h1_count + h2_count) / total_features
            
            quantum_analysis['photoluminescence'] = {
                'intensity': performance_intensity,
                'lifetime': np.mean(state_lifetimes),
                'quantum_yield': h2_count / max(1, h1_count),  # H2/H1 ratio
                'emission_rate': total_features / tda_summary['time_span']
            }
            
            # 7. Quantum Confinement = Spatial Constraints
            # Field boundaries and team positioning constraints
            inter_team_dist = team_metrics['inter_team_distance']
            team_area_ratio = team_metrics['team_area_ratio']
            
            quantum_analysis['quantum_confinement'] = {
                'spatial_constraint': np.std(inter_team_dist),
                'confinement_energy': np.mean(inter_team_dist),
                'confinement_shift': np.std(team_area_ratio)
            }
            
            # 8. Quantum Coherence = State Transition Coherence
            # How "quantum-like" are the transitions
            coherence_metrics = []
            for i in range(len(attractor_analysis['cluster_labels']) - 1):
                current_state = attractor_analysis['cluster_labels'][i]
                next_state = attractor_analysis['cluster_labels'][i + 1]
                if current_state != next_state:
                    coherence_metrics.append(1.0)  # State change
                else:
                    coherence_metrics.append(0.0)  # No change
            
            quantum_analysis['quantum_coherence'] = {
                'coherence_time': np.mean(coherence_metrics),
                'decoherence_rate': 1.0 - np.mean(coherence_metrics),
                'coherence_length': np.std(coherence_metrics)
            }
            
            # Store quantum analysis
            self.quantum_analysis[segment_name] = quantum_analysis
            
            print(f"  ✓ Quantum dot analysis complete")
            print(f"    - Energy levels: {n_states}")
            print(f"    - Band gap: {quantum_analysis['band_gap']['mean']:.3f}")
            print(f"    - Binding energy: {quantum_analysis['exciton_dynamics']['binding_energy_mean']:.3f}")
            print(f"    - Performance intensity: {quantum_analysis['photoluminescence']['intensity']:.3f}")
    
    def run_gillespie_simulation(self):
        """
        Run Gillespie's algorithm simulation for each segment
        """
        print("\n=== Running Gillespie Simulations ===")
        
        for segment_name, segment_data in self.segments.items():
            if 'attractor_analysis' not in segment_data:
                continue
            
            print(f"Running Gillespie simulation for {segment_name}...")
            
            attractor_analysis = segment_data['attractor_analysis']
            n_states = attractor_analysis['n_states']
            transition_matrix = attractor_analysis['transition_matrix']
            
            # Convert transition matrix to rates
            # Assume average lifetime of 1 second (25 frames at 25Hz)
            transition_rates = transition_matrix * 25.0  # Convert to per-second rates
            
            # Run Gillespie simulation
            simulation_results = self.gillespie_algorithm(n_states, transition_rates, duration=300)  # 5 minutes
            
            # Store simulation results
            segment_data['gillespie_simulation'] = simulation_results
            
            print(f"  ✓ Simulation complete: {simulation_results['n_transitions']} transitions")
    
    def gillespie_algorithm(self, n_states, transition_rates, duration=300):
        """
        Gillespie's stochastic simulation algorithm
        """
        # Initialize
        current_state = 0
        current_time = 0.0
        state_history = [current_state]
        time_history = [current_time]
        transition_times = []
        
        while current_time < duration:
            # Calculate total transition rate from current state
            total_rate = np.sum(transition_rates[current_state, :])
            
            if total_rate == 0:
                break  # No transitions possible
            
            # Generate next transition time
            dt = -np.log(np.random.random()) / total_rate
            current_time += dt
            
            if current_time > duration:
                break
            
            # Choose next state
            probabilities = transition_rates[current_state, :] / total_rate
            next_state = np.random.choice(n_states, p=probabilities)
            
            # Record transition
            state_history.append(next_state)
            time_history.append(current_time)
            transition_times.append(dt)
            current_state = next_state
        
        return {
            'state_history': state_history,
            'time_history': time_history,
            'transition_times': transition_times,
            'n_transitions': len(transition_times),
            'final_state': current_state,
            'total_time': current_time
        }
    
    def create_comparative_quantum_analysis(self):
        """
        Create comparative analysis across segments
        """
        print("\n=== Creating Comparative Quantum Analysis ===")
        
        if len(self.quantum_analysis) == 0:
            print("No quantum analysis data to compare")
            return
        
        # Extract metrics for comparison
        comparison_data = []
        
        for segment_name, quantum_data in self.quantum_analysis.items():
            comparison_data.append({
                'segment': segment_name,
                'energy_levels': len(quantum_data['energy_levels']),
                'band_gap_mean': quantum_data['band_gap']['mean'],
                'binding_energy_mean': quantum_data['exciton_dynamics']['binding_energy_mean'],
                'tunneling_rate_mean': quantum_data['quantum_tunneling']['mean_tunneling_rate'],
                'performance_intensity': quantum_data['photoluminescence']['intensity'],
                'quantum_yield': quantum_data['photoluminescence']['quantum_yield'],
                'coherence_time': quantum_data['quantum_coherence']['coherence_time'],
                'confinement_energy': quantum_data['quantum_confinement']['confinement_energy']
            })
        
        self.quantum_comparison = pd.DataFrame(comparison_data)
        
        print("Quantum dot comparison created:")
        print(self.quantum_comparison[['segment', 'energy_levels', 'band_gap_mean', 'performance_intensity']].to_string(index=False))
    
    def export_results(self, output_dir='quantum_dot_real_analysis'):
        """
        Export all quantum dot analysis results
        """
        print(f"\n=== Exporting Quantum Dot Results to {output_dir} ===")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Export quantum comparison
        if hasattr(self, 'quantum_comparison'):
            self.quantum_comparison.to_csv(f'{output_dir}/quantum_comparison.csv', index=False)
        
        # Export individual segment quantum analysis
        for segment_name, quantum_data in self.quantum_analysis.items():
            with open(f'{output_dir}/{segment_name}_quantum_analysis.json', 'w') as f:
                json.dump(quantum_data, f, indent=2, default=str)
        
        # Export Gillespie simulation results
        for segment_name, segment_data in self.segments.items():
            if 'gillespie_simulation' in segment_data:
                simulation_data = segment_data['gillespie_simulation']
                # Convert numpy arrays to lists for JSON serialization
                json_simulation = {
                    'state_history': simulation_data['state_history'],
                    'time_history': simulation_data['time_history'],
                    'transition_times': simulation_data['transition_times'],
                    'n_transitions': simulation_data['n_transitions'],
                    'final_state': simulation_data['final_state'],
                    'total_time': simulation_data['total_time']
                }
                
                with open(f'{output_dir}/{segment_name}_gillespie_simulation.json', 'w') as f:
                    json.dump(json_simulation, f, indent=2, default=str)
        
        # Create comprehensive report
        report = f"""Quantum Dot Analysis on Real Multi-Segment Data
================================================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Segments Analyzed: {len(self.quantum_analysis)}

QUANTUM DOT COMPARISON:
{self.quantum_comparison.to_string(index=False) if hasattr(self, 'quantum_comparison') else 'No comparison data'}

KEY QUANTUM INSIGHTS:
"""
        
        if hasattr(self, 'quantum_comparison') and len(self.quantum_comparison) > 0:
            # Find most/least quantum-like segments
            most_quantum = self.quantum_comparison.loc[self.quantum_comparison['performance_intensity'].idxmax()]
            least_quantum = self.quantum_comparison.loc[self.quantum_comparison['performance_intensity'].idxmin()]
            
            report += f"""
• Most Quantum-Like Segment: {most_quantum['segment']} (Intensity: {most_quantum['performance_intensity']:.3f})
• Least Quantum-Like Segment: {least_quantum['segment']} (Intensity: {least_quantum['performance_intensity']:.3f})
• Average Band Gap: {self.quantum_comparison['band_gap_mean'].mean():.3f}
• Average Binding Energy: {self.quantum_comparison['binding_energy_mean'].mean():.3f}
• Average Quantum Yield: {self.quantum_comparison['quantum_yield'].mean():.3f}
"""
        
        report += "\nAnalysis Complete!"
        
        with open(f'{output_dir}/quantum_analysis_report.txt', 'w') as f:
            f.write(report)
        
        print(f"✓ Quantum dot results exported to {output_dir}/")
        print(f"  - Quantum comparison: {len(self.quantum_analysis)} segments")
        print(f"  - Individual quantum analyses")
        print(f"  - Gillespie simulations")
        print(f"  - Analysis report")
    
    def run_complete_analysis(self):
        """
        Run the complete quantum dot analysis
        """
        print("=== Quantum Dot Analysis on Real Multi-Segment Data ===")
        print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Load segment results
            if not self.load_segment_results():
                print("Failed to load segment results")
                return {'success': False, 'error': 'Failed to load segment results'}
            
            # Identify attractor states
            self.identify_attractor_states()
            
            # Analyze quantum dot analogies
            self.analyze_quantum_dot_analogies()
            
            # Run Gillespie simulations
            self.run_gillespie_simulation()
            
            # Create comparative analysis
            self.create_comparative_quantum_analysis()
            
            # Export results
            self.export_results()
            
            print(f"\n=== Quantum Dot Analysis Complete ===")
            print(f"Segments analyzed: {len(self.quantum_analysis)}")
            print(f"Total attractor states: {sum(len(seg['attractor_analysis']['energy_levels']) for seg in self.segments.values() if 'attractor_analysis' in seg)}")
            
            return {
                'success': True,
                'segments': len(self.quantum_analysis),
                'quantum_comparison': self.quantum_comparison if hasattr(self, 'quantum_comparison') else None
            }
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """
    Main function to run the quantum dot analysis
    """
    print("Quantum Dot Analysis on Real Multi-Segment Data")
    print("===============================================")
    
    # Initialize analyzer
    analyzer = QuantumDotRealDataAnalyzer()
    
    # Run analysis
    results = analyzer.run_complete_analysis()
    
    if results['success']:
        print("\n🎉 Quantum dot analysis completed successfully!")
        print(f"Analyzed {results['segments']} segments")
        if results['quantum_comparison'] is not None:
            print("Quantum dot comparison created")
    else:
        print(f"\n❌ Analysis failed: {results['error']}")


if __name__ == "__main__":
    main()
