#!/usr/bin/env python3
"""
Persistent Homology Analysis for Football TDA
=============================================

This script performs persistent homology analysis using Python's robust TDA libraries,
integrating quantum dot insights from the football dynamics analysis.

Dependencies:
- numpy
- scipy
- gudhi (for persistent homology)
- ripser (alternative persistent homology library)
- pandas
- matplotlib
- json

Usage:
    python persistent_homology_python.py input_data.json output_results.json
"""

import numpy as np
import pandas as pd
import json
import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Try to import TDA libraries
try:
    import gudhi
    GUDHI_AVAILABLE = True
except ImportError:
    GUDHI_AVAILABLE = False
    print("Warning: Gudhi not available. Install with: pip install gudhi")

try:
    import ripser
    RIPSER_AVAILABLE = True
except ImportError:
    RIPSER_AVAILABLE = False
    print("Warning: Ripser not available. Install with: pip install ripser")

try:
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: SciPy not available. Install with: pip install scipy")


class PersistentHomologyAnalyzer:
    """
    Persistent homology analyzer using Python TDA libraries
    """
    
    def __init__(self, max_filtration=1.0, max_dimension=2):
        """
        Initialize the persistent homology analyzer
        
        Args:
            max_filtration (float): Maximum filtration value
            max_dimension (int): Maximum homology dimension to compute
        """
        self.max_filtration = max_filtration
        self.max_dimension = max_dimension
        self.results = {}
        
    def load_data_from_matlab(self, data_file):
        """
        Load data exported from MATLAB
        
        Args:
            data_file (str): Path to JSON file with MATLAB data
        """
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Extract point cloud data
        if 'stateVectors' in data:
            self.point_cloud = np.array(data['stateVectors'])
        elif 'coupledMetrics' in data:
            # Use coupled metrics as point cloud
            metrics = data['coupledMetrics']
            self.point_cloud = np.array([
                metrics['InterTeamDistance'],
                metrics['TeamAreaRatio'], 
                metrics['HomeMeanNOD'],
                metrics['AwayMeanNOD']
            ]).T
        else:
            raise ValueError("No suitable data found in input file")
        
        # Load quantum dot model data if available
        if 'quantumDotModel' in data:
            self.quantum_model = data['quantumDotModel']
        else:
            self.quantum_model = None
            
        print(f"Loaded point cloud: {self.point_cloud.shape}")
        
    def compute_persistent_homology_gudhi(self):
        """
        Compute persistent homology using Gudhi
        """
        if not GUDHI_AVAILABLE:
            raise ImportError("Gudhi not available")
            
        print("Computing persistent homology with Gudhi...")
        
        # Create Rips complex
        rips_complex = gudhi.RipsComplex(points=self.point_cloud, max_edge_length=self.max_filtration)
        
        # Create simplex tree
        simplex_tree = rips_complex.create_simplex_tree(max_dimension=self.max_dimension)
        
        # Compute persistence
        persistence = simplex_tree.persistence()
        
        # Organize results by dimension
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
                
        print(f"Gudhi computation complete. Found {len(persistence)} features.")
        
    def compute_persistent_homology_ripser(self):
        """
        Compute persistent homology using Ripser
        """
        if not RIPSER_AVAILABLE:
            raise ImportError("Ripser not available")
            
        print("Computing persistent homology with Ripser...")
        
        # Compute persistence diagrams
        ripser_results = ripser.ripser(self.point_cloud, maxdim=self.max_dimension, 
                                      thresh=self.max_filtration)
        
        # Organize results
        self.results['ripser'] = {}
        for dim in range(self.max_dimension + 1):
            if dim < len(ripser_results['dgms']):
                self.results['ripser'][f'H{dim}'] = ripser_results['dgms'][dim]
            else:
                self.results['ripser'][f'H{dim}'] = np.array([]).reshape(0, 2)
        
        print(f"Ripser computation complete. Found {sum(len(dgm) for dgm in ripser_results['dgms'])} features.")
        
    def extract_topological_features(self):
        """
        Extract topological features from persistence diagrams
        """
        print("Extracting topological features...")
        
        self.results['topological_features'] = {}
        
        # Use Ripser results if available, otherwise Gudhi
        if 'ripser' in self.results:
            diagrams = self.results['ripser']
        elif 'gudhi' in self.results:
            diagrams = self.results['gudhi']
        else:
            raise ValueError("No persistence diagrams available")
        
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
                        'max_persistence': np.max(persistence),
                        'mean_persistence': np.mean(persistence),
                        'std_persistence': np.std(persistence),
                        'total_persistence': np.sum(persistence),
                        'birth_times': finite_diagram[:, 0].tolist(),
                        'death_times': finite_diagram[:, 1].tolist(),
                        'persistence_values': persistence.tolist()
                    }
                else:
                    self.results['topological_features'][h_key] = {
                        'count': 0,
                        'max_persistence': 0,
                        'mean_persistence': 0,
                        'std_persistence': 0,
                        'total_persistence': 0,
                        'birth_times': [],
                        'death_times': [],
                        'persistence_values': []
                    }
            else:
                self.results['topological_features'][h_key] = {
                    'count': 0,
                    'max_persistence': 0,
                    'mean_persistence': 0,
                    'std_persistence': 0,
                    'total_persistence': 0,
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
            'point_cloud_dimensions': self.point_cloud.shape[1]
        }
        
        print(f"Topological features extracted. Total features: {total_features}")
        
    def analyze_quantum_topological_features(self):
        """
        Analyze topological features with quantum dot insights
        """
        if self.quantum_model is None:
            print("No quantum model available for quantum topological analysis")
            return
            
        print("Analyzing quantum topological features...")
        
        self.results['quantum_topological_features'] = {}
        
        # Get quantum dot state lifetimes
        if 'stateLifetimes' in self.quantum_model:
            quantum_lifetimes = np.array(self.quantum_model['stateLifetimes'])
            
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
                            correlation = 0
                        
                        # Classify as long-lived or short-lived based on quantum model
                        long_lived_threshold = np.percentile(quantum_lifetimes, 75)
                        short_lived_threshold = np.percentile(quantum_lifetimes, 25)
                        
                        long_lived_count = np.sum(topo_persistence > long_lived_threshold)
                        short_lived_count = np.sum(topo_persistence < short_lived_threshold)
                        
                        self.results['quantum_topological_features'][h_key] = {
                            'quantum_correlation': correlation,
                            'long_lived_count': int(long_lived_count),
                            'short_lived_count': int(short_lived_count),
                            'lifetime_ratio': long_lived_count / (short_lived_count + 1e-10),
                            'quantum_efficiency': (long_lived_count + 1) / (short_lived_count + 1)
                        }
                    else:
                        self.results['quantum_topological_features'][h_key] = {
                            'quantum_correlation': 0,
                            'long_lived_count': 0,
                            'short_lived_count': 0,
                            'lifetime_ratio': 0,
                            'quantum_efficiency': 0
                        }
        
        print("Quantum topological features analyzed")
        
    def analyze_tactical_effectiveness(self):
        """
        Analyze topological signatures of tactical effectiveness
        """
        print("Analyzing tactical effectiveness from topology...")
        
        self.results['tactical_effectiveness'] = {}
        
        # Link topological complexity to effectiveness
        if 'overall' in self.results['topological_features']:
            overall = self.results['topological_features']['overall']
            
            # Effectiveness based on complexity
            complexity = overall['complexity_index']
            self.results['tactical_effectiveness']['complexity_effectiveness'] = {
                'complexity_index': complexity,
                'is_effective': complexity > 0.1,  # Threshold
                'effectiveness_score': min(complexity * 10, 1.0)  # Normalize to [0,1]
            }
        
        # Analyze persistence balance
        h0_persistence = self.results['topological_features'].get('H0', {}).get('mean_persistence', 0)
        h1_persistence = self.results['topological_features'].get('H1', {}).get('mean_persistence', 0)
        
        persistence_balance = abs(h0_persistence - h1_persistence)
        self.results['tactical_effectiveness']['persistence_balance'] = {
            'h0_persistence': h0_persistence,
            'h1_persistence': h1_persistence,
            'balance': persistence_balance,
            'is_balanced': persistence_balance < 0.1  # Threshold
        }
        
        # Quantum effectiveness
        if 'quantum_topological_features' in self.results:
            quantum_feat = self.results['quantum_topological_features']
            quantum_efficiency = np.mean([feat.get('quantum_efficiency', 0) 
                                        for feat in quantum_feat.values()])
            
            self.results['tactical_effectiveness']['quantum_effectiveness'] = {
                'quantum_efficiency': quantum_efficiency,
                'is_quantum_effective': quantum_efficiency > 1.0,  # Threshold
                'quantum_score': min(quantum_efficiency, 2.0) / 2.0  # Normalize to [0,1]
            }
        
        print("Tactical effectiveness analysis complete")
        
    def save_results(self, output_file):
        """
        Save results to JSON file for MATLAB import
        
        Args:
            output_file (str): Path to output JSON file
        """
        print(f"Saving results to {output_file}")
        
        # Convert numpy arrays to lists for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        # Convert results
        json_results = convert_numpy(self.results)
        
        # Add metadata
        json_results['metadata'] = {
            'analysis_type': 'persistent_homology',
            'max_filtration': self.max_filtration,
            'max_dimension': self.max_dimension,
            'point_cloud_shape': self.point_cloud.shape,
            'libraries_used': {
                'gudhi': GUDHI_AVAILABLE,
                'ripser': RIPSER_AVAILABLE,
                'scipy': SCIPY_AVAILABLE
            }
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"Results saved successfully to {output_file}")


def main():
    """
    Main function to run persistent homology analysis
    """
    if len(sys.argv) != 3:
        print("Usage: python persistent_homology_python.py input_data.json output_results.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = PersistentHomologyAnalyzer(max_filtration=1.0, max_dimension=2)
    
    try:
        # Load data
        analyzer.load_data_from_matlab(input_file)
        
        # Compute persistent homology (try both libraries)
        if RIPSER_AVAILABLE:
            analyzer.compute_persistent_homology_ripser()
        elif GUDHI_AVAILABLE:
            analyzer.compute_persistent_homology_gudhi()
        else:
            print("Error: No persistent homology libraries available")
            print("Install with: pip install ripser gudhi")
            sys.exit(1)
        
        # Extract features
        analyzer.extract_topological_features()
        
        # Analyze quantum features
        analyzer.analyze_quantum_topological_features()
        
        # Analyze tactical effectiveness
        analyzer.analyze_tactical_effectiveness()
        
        # Save results
        analyzer.save_results(output_file)
        
        print("Persistent homology analysis completed successfully!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
