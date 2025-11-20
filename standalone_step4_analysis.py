#!/usr/bin/env python3
"""
Standalone Step 4 Analysis: Persistent Homology with Quantum Dot Insights
========================================================================

This standalone Python script performs comprehensive persistent homology analysis
for the GPS-TDA football project, integrating quantum dot insights and tactical
effectiveness analysis.

Features:
- Loads MATLAB data from JSON files
- Uses robust TDA libraries (ripser, gudhi)
- Implements quantum dot-inspired analysis
- Computes tactical effectiveness metrics
- Exports comprehensive results to CSV/JSON

Usage:
    python standalone_step4_analysis.py [input_dir] [output_dir]

If no arguments provided, uses default directories:
    input_dir: ./step1_coupled_variables_results, ./step2_state_space_results, etc.
    output_dir: ./step4_standalone_results
"""

import numpy as np
import pandas as pd
import json
import sys
import os
from pathlib import Path
import warnings
import time
from datetime import datetime
warnings.filterwarnings('ignore')

# Import TDA libraries
try:
    import ripser
    RIPSER_AVAILABLE = True
    print("✓ Ripser available")
except ImportError:
    RIPSER_AVAILABLE = False
    print("✗ Ripser not available")

try:
    import gudhi
    GUDHI_AVAILABLE = True
    print("✓ Gudhi available")
except ImportError:
    GUDHI_AVAILABLE = False
    print("✗ Gudhi not available")

try:
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram
    SCIPY_AVAILABLE = True
    print("✓ SciPy available")
except ImportError:
    SCIPY_AVAILABLE = False
    print("✗ SciPy not available")

# Try to import teaspoon (optional)
try:
    import teaspoon
    import teaspoon.parameter_selection.FNN_n as FNN
    import teaspoon.parameter_selection.MI_delay as MI
    TEASPOON_AVAILABLE = True
    print("✓ Teaspoon available")
except ImportError:
    TEASPOON_AVAILABLE = False
    print("✗ Teaspoon not available")


class StandaloneStep4Analyzer:
    """
    Standalone analyzer for Step 4: Persistent Homology with Quantum Dot Insights
    """
    
    def __init__(self, max_filtration=1.0, max_dimension=2):
        """
        Initialize the standalone analyzer
        
        Args:
            max_filtration (float): Maximum filtration value
            max_dimension (int): Maximum homology dimension to compute
        """
        self.max_filtration = max_filtration
        self.max_dimension = max_dimension
        self.results = {}
        self.computation_time = 0
        
        # Data containers
        self.coupled_metrics = None
        self.state_space = None
        self.zero_sum_analysis = None
        self.quantum_dot_model = None
        
        print(f"StandaloneStep4Analyzer initialized")
        print(f"  Max filtration: {max_filtration}")
        print(f"  Max dimension: {max_dimension}")
        
    def load_matlab_data(self, input_dir):
        """
        Load data from MATLAB analysis results
        
        Args:
            input_dir (str): Directory containing MATLAB results
        """
        print(f"\nLoading MATLAB data from: {input_dir}")
        
        # Load Step 1: Coupled Variables
        step1_file = os.path.join(input_dir, 'step1_coupled_variables_results', 'coupled_analysis.mat')
        if os.path.exists(step1_file):
            print("  Loading Step 1: Coupled Variables...")
            # For now, we'll load from JSON if available, or use synthetic data
            json_file = os.path.join(input_dir, 'step1_coupled_variables_results', 'coupled_metrics.json')
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    self.coupled_metrics = json.load(f)
                print(f"    Loaded coupled metrics: {len(self.coupled_metrics.get('InterTeamDistance', []))} time points")
            else:
                print("    JSON file not found, will generate synthetic data")
        
        # Load Step 2: State Space Reconstruction
        step2_file = os.path.join(input_dir, 'step2_state_space_results', 'state_space_analysis.mat')
        if os.path.exists(step2_file):
            print("  Loading Step 2: State Space Reconstruction...")
            json_file = os.path.join(input_dir, 'step2_state_space_results', 'state_vectors.json')
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    self.state_space = json.load(f)
                print(f"    Loaded state vectors: {len(self.state_space.get('stateVectors', []))} vectors")
            else:
                print("    JSON file not found, will generate synthetic data")
        
        # Load Step 3: Zero-Sum Analysis
        step3_file = os.path.join(input_dir, 'step3_zero_sum_symmetry_results', 'zero_sum_symmetry_analysis.mat')
        if os.path.exists(step3_file):
            print("  Loading Step 3: Zero-Sum Analysis...")
            json_file = os.path.join(input_dir, 'step3_zero_sum_symmetry_results', 'zero_sum_metrics.json')
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    self.zero_sum_analysis = json.load(f)
                print("    Loaded zero-sum analysis")
            else:
                print("    JSON file not found, will generate synthetic data")
        
        # Load Quantum Dot Model
        quantum_file = os.path.join(input_dir, 'quantum_dot_model_results', 'quantum_dot_model.mat')
        if os.path.exists(quantum_file):
            print("  Loading Quantum Dot Model...")
            json_file = os.path.join(input_dir, 'quantum_dot_model_results', 'quantum_model.json')
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    self.quantum_dot_model = json.load(f)
                print("    Loaded quantum dot model")
            else:
                print("    JSON file not found, will generate synthetic data")
        
        # Generate synthetic data if needed
        self._generate_synthetic_data_if_needed()
        
    def _generate_synthetic_data_if_needed(self):
        """
        Generate synthetic data if real data is not available
        """
        print("\nGenerating synthetic data for missing components...")
        
        # Generate synthetic coupled metrics
        if self.coupled_metrics is None:
            print("  Generating synthetic coupled metrics...")
            n_points = 1000
            self.coupled_metrics = {
                'InterTeamDistance': np.random.normal(25, 5, n_points).tolist(),
                'TeamAreaRatio': np.random.uniform(0.5, 2.0, n_points).tolist(),
                'HomeMeanNOD': np.random.normal(8, 2, n_points).tolist(),
                'AwayMeanNOD': np.random.normal(8, 2, n_points).tolist()
            }
        
        # Generate synthetic state space
        if self.state_space is None:
            print("  Generating synthetic state space...")
            n_vectors = 1000
            self.state_space = {
                'stateVectors': np.random.randn(n_vectors, 4).tolist(),
                'embeddingDimension': 3,
                'timeDelay': 1
            }
        
        # Generate synthetic quantum dot model
        if self.quantum_dot_model is None:
            print("  Generating synthetic quantum dot model...")
            n_states = 3
            self.quantum_dot_model = {
                'stateLifetimes': np.random.exponential(10, n_states).tolist(),
                'quantumDotAnalogy': {
                    'lifetimeRatio': 4.93
                }
            }
        
        # Generate synthetic zero-sum analysis
        if self.zero_sum_analysis is None:
            print("  Generating synthetic zero-sum analysis...")
            self.zero_sum_analysis = {
                'competitiveBalance': {
                    'overallBalance': 0.75
                }
            }
    
    def prepare_point_cloud_data(self):
        """
        Prepare point cloud data for persistent homology analysis
        """
        print("\nPreparing point cloud data...")
        
        # Use state vectors if available, otherwise use coupled metrics
        if self.state_space and 'stateVectors' in self.state_space:
            self.point_cloud = np.array(self.state_space['stateVectors'])
            print(f"  Using state vectors: {self.point_cloud.shape}")
        else:
            # Create point cloud from coupled metrics
            metrics = self.coupled_metrics
            self.point_cloud = np.array([
                metrics['InterTeamDistance'],
                metrics['TeamAreaRatio'],
                metrics['HomeMeanNOD'],
                metrics['AwayMeanNOD']
            ]).T
            print(f"  Using coupled metrics: {self.point_cloud.shape}")
        
        # Clean the data - remove NaN values
        valid_rows = ~np.isnan(self.point_cloud).any(axis=1)
        self.point_cloud = self.point_cloud[valid_rows]
        
        print(f"  Cleaned point cloud: {self.point_cloud.shape}")
        print(f"  Removed {np.sum(~valid_rows)} rows with NaN values")
        
        if len(self.point_cloud) < 3:
            raise ValueError("Not enough valid points for persistent homology computation")
    
    def compute_persistent_homology(self):
        """
        Compute persistent homology using available TDA libraries
        """
        print("\nComputing persistent homology...")
        
        if not RIPSER_AVAILABLE and not GUDHI_AVAILABLE:
            raise ImportError("No TDA libraries available. Install ripser or gudhi.")
        
        # Try ripser first (usually faster)
        if RIPSER_AVAILABLE:
            print("  Using Ripser...")
            try:
                ripser_results = ripser.ripser(self.point_cloud, maxdim=self.max_dimension, 
                                              thresh=self.max_filtration)
                
                # Organize results
                self.results['ripser'] = {}
                for dim in range(self.max_dimension + 1):
                    if dim < len(ripser_results['dgms']):
                        self.results['ripser'][f'H{dim}'] = ripser_results['dgms'][dim]
                    else:
                        self.results['ripser'][f'H{dim}'] = np.array([]).reshape(0, 2)
                
                total_features = sum(len(dgm) for dgm in ripser_results['dgms'])
                print(f"    Ripser complete: {total_features} features found")
                
            except Exception as e:
                print(f"    Ripser failed: {e}")
                self.results['ripser'] = {}
        
        # Try gudhi as backup
        if GUDHI_AVAILABLE and not self.results.get('ripser'):
            print("  Using Gudhi...")
            try:
                # Create Rips complex
                rips_complex = gudhi.RipsComplex(points=self.point_cloud, max_edge_length=self.max_filtration)
                
                # Create simplex tree
                simplex_tree = rips_complex.create_simplex_tree(max_dimension=self.max_dimension)
                
                # Compute persistence
                persistence = simplex_tree.persistence()
                
                # Organize results
                self.results['gudhi'] = {}
                for dim in range(self.max_dimension + 1):
                    self.results['gudhi'][f'H{dim}'] = []
                
                for (dim, (birth, death)) in persistence:
                    if dim <= self.max_dimension:
                        self.results['gudhi'][f'H{dim}'].append([birth, death])
                
                # Convert to numpy arrays
                for dim in range(self.max_dimension + 1):
                    if self.results['gudhi'][f'H{dim}']:
                        self.results['gudhi'][f'H{dim}'] = np.array(self.results['gudhi'][f'H{dim}'])
                    else:
                        self.results['gudhi'][f'H{dim}'] = np.array([]).reshape(0, 2)
                
                print(f"    Gudhi complete: {len(persistence)} features found")
                
            except Exception as e:
                print(f"    Gudhi failed: {e}")
                self.results['gudhi'] = {}
        
        if not self.results:
            raise RuntimeError("All TDA computations failed")
    
    def extract_topological_features(self):
        """
        Extract topological features from persistence diagrams
        """
        print("\nExtracting topological features...")
        
        # Use the first available results
        if 'ripser' in self.results:
            diagrams = self.results['ripser']
            library_used = 'ripser'
        elif 'gudhi' in self.results:
            diagrams = self.results['gudhi']
            library_used = 'gudhi'
        else:
            raise ValueError("No persistence diagrams available")
        
        print(f"  Using {library_used} results")
        
        self.results['topological_features'] = {}
        
        for dim in range(self.max_dimension + 1):
            h_key = f'H{dim}'
            if h_key in diagrams and len(diagrams[h_key]) > 0:
                diagram = diagrams[h_key]
                
                # Remove infinite death times
                finite_diagram = diagram[diagram[:, 1] != np.inf]
                
                if len(finite_diagram) > 0:
                    # Compute persistence (death - birth)
                    persistence = finite_diagram[:, 1] - finite_diagram[:, 0]
                    
                    self.results['topological_features'][h_key] = {
                        'count': len(finite_diagram),
                        'max_persistence': float(np.max(persistence)),
                        'mean_persistence': float(np.mean(persistence)),
                        'std_persistence': float(np.std(persistence)),
                        'total_persistence': float(np.sum(persistence)),
                        'birth_times': finite_diagram[:, 0].tolist(),
                        'death_times': finite_diagram[:, 1].tolist(),
                        'persistence_values': persistence.tolist()
                    }
                else:
                    self.results['topological_features'][h_key] = {
                        'count': 0,
                        'max_persistence': 0.0,
                        'mean_persistence': 0.0,
                        'std_persistence': 0.0,
                        'total_persistence': 0.0,
                        'birth_times': [],
                        'death_times': [],
                        'persistence_values': []
                    }
            else:
                self.results['topological_features'][h_key] = {
                    'count': 0,
                    'max_persistence': 0.0,
                    'mean_persistence': 0.0,
                    'std_persistence': 0.0,
                    'total_persistence': 0.0,
                    'birth_times': [],
                    'death_times': [],
                    'persistence_values': []
                }
        
        # Overall complexity metrics
        total_features = sum(feat['count'] for feat in self.results['topological_features'].values())
        self.results['topological_features']['overall'] = {
            'total_features': total_features,
            'complexity_index': total_features / len(self.point_cloud),
            'point_cloud_size': len(self.point_cloud),
            'point_cloud_dimensions': self.point_cloud.shape[1],
            'library_used': library_used
        }
        
        print(f"  Topological features extracted: {total_features} total features")
    
    def analyze_quantum_topological_features(self):
        """
        Analyze topological features with quantum dot insights
        """
        print("\nAnalyzing quantum topological features...")
        
        if self.quantum_dot_model is None:
            print("  No quantum model available, skipping quantum analysis")
            return
        
        self.results['quantum_topological_features'] = {}
        
        # Get quantum dot state lifetimes
        if 'stateLifetimes' in self.quantum_dot_model:
            quantum_lifetimes = np.array(self.quantum_dot_model['stateLifetimes'])
            
            # Map topological persistence to quantum lifetimes
            for dim in range(self.max_dimension + 1):
                h_key = f'H{dim}'
                if h_key in self.results['topological_features']:
                    topo_feat = self.results['topological_features'][h_key]
                    
                    if topo_feat['count'] > 0:
                        # Correlate topological persistence with quantum lifetimes
                        topo_persistence = np.array(topo_feat['persistence_values'])
                        
                        # Pad or truncate to match lengths
                        min_len = min(len(topo_persistence), len(quantum_lifetimes))
                        if min_len > 1:
                            correlation = np.corrcoef(topo_persistence[:min_len], 
                                                    quantum_lifetimes[:min_len])[0, 1]
                        else:
                            correlation = 0.0
                        
                        # Classify as long-lived or short-lived based on quantum model
                        long_lived_threshold = np.percentile(quantum_lifetimes, 75)
                        short_lived_threshold = np.percentile(quantum_lifetimes, 25)
                        
                        long_lived_count = np.sum(topo_persistence > long_lived_threshold)
                        short_lived_count = np.sum(topo_persistence < short_lived_threshold)
                        
                        self.results['quantum_topological_features'][h_key] = {
                            'quantum_correlation': float(correlation),
                            'long_lived_count': int(long_lived_count),
                            'short_lived_count': int(short_lived_count),
                            'lifetime_ratio': float(long_lived_count / (short_lived_count + 1e-10)),
                            'quantum_efficiency': float((long_lived_count + 1) / (short_lived_count + 1))
                        }
                    else:
                        self.results['quantum_topological_features'][h_key] = {
                            'quantum_correlation': 0.0,
                            'long_lived_count': 0,
                            'short_lived_count': 0,
                            'lifetime_ratio': 0.0,
                            'quantum_efficiency': 0.0
                        }
        
        print("  Quantum topological features analyzed")
    
    def analyze_tactical_effectiveness(self):
        """
        Analyze topological signatures of tactical effectiveness
        """
        print("\nAnalyzing tactical effectiveness...")
        
        self.results['tactical_effectiveness'] = {}
        
        # Link topological complexity to effectiveness
        if 'overall' in self.results['topological_features']:
            overall = self.results['topological_features']['overall']
            
            # Effectiveness based on complexity
            complexity = overall['complexity_index']
            self.results['tactical_effectiveness']['complexity_effectiveness'] = {
                'complexity_index': float(complexity),
                'is_effective': complexity > 0.1,
                'effectiveness_score': float(min(complexity * 10, 1.0))
            }
        
        # Analyze persistence balance
        h0_persistence = self.results['topological_features'].get('H0', {}).get('mean_persistence', 0)
        h1_persistence = self.results['topological_features'].get('H1', {}).get('mean_persistence', 0)
        
        persistence_balance = abs(h0_persistence - h1_persistence)
        self.results['tactical_effectiveness']['persistence_balance'] = {
            'h0_persistence': float(h0_persistence),
            'h1_persistence': float(h1_persistence),
            'balance': float(persistence_balance),
            'is_balanced': persistence_balance < 0.1
        }
        
        # Quantum effectiveness
        if 'quantum_topological_features' in self.results:
            quantum_feat = self.results['quantum_topological_features']
            quantum_efficiency = np.mean([feat.get('quantum_efficiency', 0) 
                                        for feat in quantum_feat.values()])
            
            self.results['tactical_effectiveness']['quantum_effectiveness'] = {
                'quantum_efficiency': float(quantum_efficiency),
                'is_quantum_effective': quantum_efficiency > 1.0,
                'quantum_score': float(min(quantum_efficiency, 2.0) / 2.0)
            }
        
        print("  Tactical effectiveness analysis complete")
    
    def export_results(self, output_dir):
        """
        Export results to CSV and JSON files
        
        Args:
            output_dir (str): Directory to save results
        """
        print(f"\nExporting results to: {output_dir}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export persistence diagrams to CSV
        for library in ['ripser', 'gudhi']:
            if library in self.results:
                for dim in range(self.max_dimension + 1):
                    h_key = f'H{dim}'
                    if h_key in self.results[library]:
                        diagram = self.results[library][h_key]
                        if len(diagram) > 0:
                            df = pd.DataFrame(diagram, columns=['Birth', 'Death'])
                            df.to_csv(os.path.join(output_dir, f'{library}_persistence_diagram_{h_key}.csv'), index=False)
        
        # Export topological features to CSV
        if 'topological_features' in self.results:
            features = self.results['topological_features']
            
            # Create summary table
            summary_data = []
            for dim in range(self.max_dimension + 1):
                h_key = f'H{dim}'
                if h_key in features:
                    feat = features[h_key]
                    summary_data.append({
                        'Homology_Dimension': h_key,
                        'Feature_Count': feat['count'],
                        'Max_Persistence': feat['max_persistence'],
                        'Mean_Persistence': feat['mean_persistence'],
                        'Std_Persistence': feat['std_persistence'],
                        'Total_Persistence': feat['total_persistence']
                    })
            
            # Add overall metrics
            if 'overall' in features:
                overall = features['overall']
                summary_data.append({
                    'Homology_Dimension': 'Overall',
                    'Feature_Count': overall['total_features'],
                    'Max_Persistence': 0.0,
                    'Mean_Persistence': 0.0,
                    'Std_Persistence': 0.0,
                    'Total_Persistence': 0.0
                })
            
            df = pd.DataFrame(summary_data)
            df.to_csv(os.path.join(output_dir, 'topological_features_summary.csv'), index=False)
        
        # Export quantum features to CSV
        if 'quantum_topological_features' in self.results:
            quantum_data = []
            for dim in range(self.max_dimension + 1):
                h_key = f'H{dim}'
                if h_key in self.results['quantum_topological_features']:
                    feat = self.results['quantum_topological_features'][h_key]
                    quantum_data.append({
                        'Homology_Dimension': h_key,
                        'Quantum_Correlation': feat['quantum_correlation'],
                        'Long_Lived_Count': feat['long_lived_count'],
                        'Short_Lived_Count': feat['short_lived_count'],
                        'Lifetime_Ratio': feat['lifetime_ratio'],
                        'Quantum_Efficiency': feat['quantum_efficiency']
                    })
            
            df = pd.DataFrame(quantum_data)
            df.to_csv(os.path.join(output_dir, 'quantum_topological_features.csv'), index=False)
        
        # Export tactical effectiveness to CSV
        if 'tactical_effectiveness' in self.results:
            tact_data = []
            tact_eff = self.results['tactical_effectiveness']
            
            if 'complexity_effectiveness' in tact_eff:
                tact_data.append({
                    'Metric': 'Complexity_Effectiveness',
                    'Score': tact_eff['complexity_effectiveness']['effectiveness_score'],
                    'Is_Effective': tact_eff['complexity_effectiveness']['is_effective']
                })
            
            if 'persistence_balance' in tact_eff:
                tact_data.append({
                    'Metric': 'Persistence_Balance',
                    'Score': float(tact_eff['persistence_balance']['is_balanced']),
                    'Is_Effective': tact_eff['persistence_balance']['is_balanced']
                })
            
            if 'quantum_effectiveness' in tact_eff:
                tact_data.append({
                    'Metric': 'Quantum_Effectiveness',
                    'Score': tact_eff['quantum_effectiveness']['quantum_score'],
                    'Is_Effective': tact_eff['quantum_effectiveness']['is_quantum_effective']
                })
            
            df = pd.DataFrame(tact_data)
            df.to_csv(os.path.join(output_dir, 'tactical_effectiveness.csv'), index=False)
        
        # Export complete results to JSON
        json_file = os.path.join(output_dir, 'step4_complete_results.json')
        
        # Convert numpy arrays to lists for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        # Convert results
        json_results = convert_numpy(self.results)
        
        with open(json_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        # Create analysis report
        self._create_analysis_report(output_dir)
        
        print(f"  Results exported successfully")
        print(f"  Files created:")
        print(f"    - step4_complete_results.json")
        print(f"    - topological_features_summary.csv")
        print(f"    - quantum_topological_features.csv")
        print(f"    - tactical_effectiveness.csv")
        print(f"    - step4_analysis_report.txt")
    
    def _create_analysis_report(self, output_dir):
        """
        Create a comprehensive analysis report
        """
        report_file = os.path.join(output_dir, 'step4_analysis_report.txt')
        
        with open(report_file, 'w') as f:
            f.write("Step 4: Persistent Homology Analysis with Quantum Dot Insights\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Computation Time: {self.computation_time:.2f} seconds\n\n")
            
            # Topological features summary
            if 'topological_features' in self.results:
                features = self.results['topological_features']
                f.write("Topological Features Summary:\n")
                f.write("-" * 30 + "\n")
                
                for dim in range(self.max_dimension + 1):
                    h_key = f'H{dim}'
                    if h_key in features:
                        feat = features[h_key]
                        f.write(f"{h_key} Features: {feat['count']}\n")
                        f.write(f"  Max Persistence: {feat['max_persistence']:.3f}\n")
                        f.write(f"  Mean Persistence: {feat['mean_persistence']:.3f}\n")
                        f.write(f"  Total Persistence: {feat['total_persistence']:.3f}\n")
                
                if 'overall' in features:
                    overall = features['overall']
                    f.write(f"\nOverall Complexity Index: {overall['complexity_index']:.3f}\n")
                    f.write(f"Point Cloud Size: {overall['point_cloud_size']}\n")
                    f.write(f"Library Used: {overall['library_used']}\n")
            
            # Quantum features summary
            if 'quantum_topological_features' in self.results:
                f.write("\n\nQuantum Topological Features:\n")
                f.write("-" * 35 + "\n")
                
                quantum_feat = self.results['quantum_topological_features']
                for dim in range(self.max_dimension + 1):
                    h_key = f'H{dim}'
                    if h_key in quantum_feat:
                        feat = quantum_feat[h_key]
                        f.write(f"{h_key} Quantum Analysis:\n")
                        f.write(f"  Quantum Correlation: {feat['quantum_correlation']:.3f}\n")
                        f.write(f"  Long-lived Features: {feat['long_lived_count']}\n")
                        f.write(f"  Short-lived Features: {feat['short_lived_count']}\n")
                        f.write(f"  Lifetime Ratio: {feat['lifetime_ratio']:.3f}\n")
                        f.write(f"  Quantum Efficiency: {feat['quantum_efficiency']:.3f}\n")
            
            # Tactical effectiveness summary
            if 'tactical_effectiveness' in self.results:
                f.write("\n\nTactical Effectiveness Analysis:\n")
                f.write("-" * 35 + "\n")
                
                tact_eff = self.results['tactical_effectiveness']
                
                if 'complexity_effectiveness' in tact_eff:
                    comp_eff = tact_eff['complexity_effectiveness']
                    f.write(f"Complexity Effectiveness: {comp_eff['effectiveness_score']:.3f}\n")
                    f.write(f"Is Effective: {comp_eff['is_effective']}\n")
                
                if 'persistence_balance' in tact_eff:
                    pers_bal = tact_eff['persistence_balance']
                    f.write(f"Persistence Balance: {pers_bal['balance']:.3f}\n")
                    f.write(f"Is Balanced: {pers_bal['is_balanced']}\n")
                
                if 'quantum_effectiveness' in tact_eff:
                    quant_eff = tact_eff['quantum_effectiveness']
                    f.write(f"Quantum Effectiveness: {quant_eff['quantum_score']:.3f}\n")
                    f.write(f"Is Quantum Effective: {quant_eff['is_quantum_effective']}\n")
            
            f.write("\n\nAnalysis Complete!\n")
    
    def run_complete_analysis(self, input_dir, output_dir):
        """
        Run the complete Step 4 analysis
        
        Args:
            input_dir (str): Directory containing MATLAB results
            output_dir (str): Directory to save results
        """
        start_time = time.time()
        
        print("=" * 70)
        print("Step 4: Standalone Persistent Homology Analysis")
        print("=" * 70)
        
        try:
            # Load data
            self.load_matlab_data(input_dir)
            
            # Prepare point cloud
            self.prepare_point_cloud_data()
            
            # Compute persistent homology
            self.compute_persistent_homology()
            
            # Extract features
            self.extract_topological_features()
            
            # Analyze quantum features
            self.analyze_quantum_topological_features()
            
            # Analyze tactical effectiveness
            self.analyze_tactical_effectiveness()
            
            # Export results
            self.export_results(output_dir)
            
            self.computation_time = time.time() - start_time
            
            print("\n" + "=" * 70)
            print("Step 4 Analysis Complete!")
            print("=" * 70)
            print(f"Total computation time: {self.computation_time:.2f} seconds")
            print(f"Results saved to: {output_dir}")
            
        except Exception as e:
            print(f"\nError during analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


def main():
    """
    Main function to run standalone Step 4 analysis
    """
    # Parse command line arguments
    if len(sys.argv) >= 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        # Use default directories
        input_dir = "."
        output_dir = "./step4_standalone_results"
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Initialize analyzer
    analyzer = StandaloneStep4Analyzer(max_filtration=1.0, max_dimension=2)
    
    # Run complete analysis
    analyzer.run_complete_analysis(input_dir, output_dir)


if __name__ == "__main__":
    main()
