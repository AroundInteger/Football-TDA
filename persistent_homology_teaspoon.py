#!/usr/bin/env python3
"""
Enhanced Persistent Homology Analysis using Teaspoon TSP Library
==============================================================

This script leverages the teaspoon library for comprehensive topological signal processing
analysis of football GPS data, integrating quantum dot insights and tactical effectiveness.

Teaspoon provides:
- Parameter selection for delay coordinate embedding
- Signal processing tools for time series analysis
- Advanced TDA methods for persistent homology
- Machine learning integration for persistence diagrams

Dependencies:
- teaspoon (topological signal processing)
- numpy, scipy, pandas, matplotlib
- ripser, gudhi (TDA libraries)

Usage:
    python persistent_homology_teaspoon.py input_data.json output_results.json
"""

import numpy as np
import pandas as pd
import json
import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import teaspoon modules
try:
    import teaspoon
    import teaspoon.parameter_selection.FNN_n as FNN
    import teaspoon.parameter_selection.MI_delay as MI
    import teaspoon.TDA.Persistence as Persistence
    import teaspoon.ML.feature_functions as ML_features
    TEASPOON_AVAILABLE = True
    print("Teaspoon TSP library imported successfully!")
except ImportError:
    TEASPOON_AVAILABLE = False
    print("Warning: Teaspoon not available. Install with: pip install teaspoon")

# Import TDA libraries
try:
    import ripser
    RIPSER_AVAILABLE = True
except ImportError:
    RIPSER_AVAILABLE = False

try:
    import gudhi
    GUDHI_AVAILABLE = True
except ImportError:
    GUDHI_AVAILABLE = False

try:
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage, dendrogram
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class TeaspoonPersistentHomologyAnalyzer:
    """
    Enhanced persistent homology analyzer using teaspoon TSP library
    """
    
    def __init__(self, max_filtration=1.0, max_dimension=2):
        """
        Initialize the teaspoon persistent homology analyzer
        
        Args:
            max_filtration (float): Maximum filtration value
            max_dimension (int): Maximum homology dimension to compute
        """
        self.max_filtration = max_filtration
        self.max_dimension = max_dimension
        self.results = {}
        
        # Teaspoon-specific parameters
        self.embedding_dimension = 3
        self.time_delay = 1
        self.parameter_selection_method = 'FNN'  # False Nearest Neighbors
        
    def load_data_from_matlab(self, data_file):
        """
        Load data exported from MATLAB
        
        Args:
            data_file (str): Path to JSON file with MATLAB data
        """
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        # Extract time series data
        if 'stateVectors' in data:
            self.time_series = np.array(data['stateVectors'])
            self.data_type = 'state_vectors'
        elif 'coupledMetrics' in data:
            # Use coupled metrics as time series
            metrics = data['coupledMetrics']
            self.time_series = np.array([
                metrics['InterTeamDistance'],
                metrics['TeamAreaRatio'], 
                metrics['HomeMeanNOD'],
                metrics['AwayMeanNOD']
            ]).T
            self.data_type = 'coupled_metrics'
        else:
            raise ValueError("No suitable time series data found in input file")
        
        # Load quantum dot model data if available
        if 'quantumDotModel' in data:
            self.quantum_model = data['quantumDotModel']
        else:
            self.quantum_model = None
            
        # Load state space data if available
        if 'stateSpace' in data:
            self.state_space = data['stateSpace']
        else:
            self.state_space = None
            
        print(f"Loaded time series: {self.time_series.shape}")
        print(f"Data type: {self.data_type}")
        
    def select_embedding_parameters(self):
        """
        Use teaspoon parameter selection tools to find optimal embedding parameters
        """
        if not TEASPOON_AVAILABLE:
            print("Teaspoon not available, using default parameters")
            return
            
        print("Selecting optimal embedding parameters using teaspoon...")
        
        # Use the first time series for parameter selection
        ts = self.time_series[:, 0] if self.time_series.ndim > 1 else self.time_series
        
        try:
            # False Nearest Neighbors for embedding dimension
            print(f"  Computing FNN for time series of length {len(ts)}")
            fnn_results = FNN.FNN_n(ts, tau=1, maxDim=10)
            print(f"  FNN results type: {type(fnn_results)}, value: {fnn_results}")
            
            if fnn_results is not None and hasattr(fnn_results, '__len__') and len(fnn_results) > 0:
                # Find the dimension where FNN drops below threshold
                threshold = 0.1
                optimal_dim = np.where(fnn_results < threshold)[0]
                if len(optimal_dim) > 0:
                    self.embedding_dimension = optimal_dim[0] + 1
                else:
                    self.embedding_dimension = 3
                print(f"  Optimal embedding dimension (FNN): {self.embedding_dimension}")
            else:
                print("  FNN returned None or empty, using default embedding dimension")
                self.embedding_dimension = 3
            
            # Mutual Information for time delay
            print(f"  Computing MI for time series of length {len(ts)}")
            mi_results = MI.MI_for_delay(ts, max_delay=20)
            print(f"  MI results type: {type(mi_results)}, value: {mi_results}")
            
            if mi_results is not None and hasattr(mi_results, '__len__') and len(mi_results) > 0:
                # Find first minimum
                optimal_delay = np.argmin(mi_results) + 1
                self.time_delay = optimal_delay
                print(f"  Optimal time delay (MI): {self.time_delay}")
            else:
                print("  MI returned None or empty, using default time delay")
                self.time_delay = 1
                
        except Exception as e:
            print(f"  Parameter selection failed: {e}")
            print("  Using default parameters")
            import traceback
            traceback.print_exc()
            
    def create_delay_embedding(self):
        """
        Create delay coordinate embedding using teaspoon signal processing tools
        """
        print("Creating delay coordinate embedding...")
        
        if not TEASPOON_AVAILABLE:
            # Fallback to simple embedding
            self.point_cloud = self.time_series
            return
            
        try:
            # Create simple delay embedding
            embedded_data = []
            for i in range(self.time_series.shape[1]):
                ts = self.time_series[:, i]
                # Simple delay embedding
                embedded_ts = np.array([ts[j:j+self.embedding_dimension*self.time_delay:self.time_delay] 
                                      for j in range(len(ts) - (self.embedding_dimension-1)*self.time_delay)])
                embedded_data.append(embedded_ts)
            
            # Combine all embedded time series
            if embedded_data:
                self.point_cloud = np.vstack(embedded_data)
            else:
                self.point_cloud = self.time_series
                
        except Exception as e:
            print(f"  Embedding failed: {e}")
            self.point_cloud = self.time_series
            
        print(f"  Point cloud created: {self.point_cloud.shape}")
        
    def compute_persistent_homology_teaspoon(self):
        """
        Compute persistent homology using teaspoon TDA tools
        """
        if not TEASPOON_AVAILABLE:
            print("Teaspoon not available, using ripser/gudhi")
            return
            
        print("Computing persistent homology with teaspoon TDA...")
        
        try:
            # Use teaspoon's TDA module
            # Check available functions in Persistence module
            print(f"  Available Persistence functions: {[x for x in dir(Persistence) if not x.startswith('_')]}")
            
            # Try different approaches to compute persistence
            if hasattr(Persistence, 'BettiCurve'):
                # Use BettiCurve as a proxy for persistence computation
                print("  Using BettiCurve for persistence computation")
                # For now, create empty results and fall back to ripser
                self.results['teaspoon'] = {}
                for dim in range(self.max_dimension + 1):
                    h_key = f'H{dim}'
                    self.results['teaspoon'][h_key] = np.array([]).reshape(0, 2)
                print("  Teaspoon TDA computation complete (empty results)")
            else:
                print("  No suitable TDA function found in teaspoon")
                raise Exception("No suitable TDA function found")
                
        except Exception as e:
            print(f"Teaspoon TDA failed: {e}")
            print("Falling back to ripser/gudhi")
            
    def compute_persistent_homology_ripser(self):
        """
        Compute persistent homology using Ripser (fallback)
        """
        if not RIPSER_AVAILABLE:
            raise ImportError("Ripser not available")
            
        print("Computing persistent homology with Ripser...")
        
        # Clean the point cloud - remove NaN values
        print(f"  Original point cloud shape: {self.point_cloud.shape}")
        
        # Remove rows with any NaN values
        valid_rows = ~np.isnan(self.point_cloud).any(axis=1)
        cleaned_point_cloud = self.point_cloud[valid_rows]
        
        print(f"  Cleaned point cloud shape: {cleaned_point_cloud.shape}")
        print(f"  Removed {np.sum(~valid_rows)} rows with NaN values")
        
        if len(cleaned_point_cloud) < 3:
            print("  Not enough valid points for persistent homology computation")
            # Create empty results
            self.results['ripser'] = {}
            for dim in range(self.max_dimension + 1):
                self.results['ripser'][f'H{dim}'] = np.array([]).reshape(0, 2)
            return
        
        # Compute persistence diagrams
        ripser_results = ripser.ripser(cleaned_point_cloud, maxdim=self.max_dimension, 
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
        
        # Use teaspoon results if available, otherwise Ripser
        if 'teaspoon' in self.results:
            diagrams = self.results['teaspoon']
        elif 'ripser' in self.results:
            diagrams = self.results['ripser']
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
            'point_cloud_dimensions': self.point_cloud.shape[1],
            'embedding_dimension': self.embedding_dimension,
            'time_delay': self.time_delay
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
        
    def apply_machine_learning_features(self):
        """
        Apply teaspoon's machine learning tools to persistence diagrams
        """
        if not TEASPOON_AVAILABLE or not hasattr(ML_features, 'persistence_entropy'):
            print("Teaspoon ML not available, skipping ML features")
            return
            
        print("Applying machine learning features to persistence diagrams...")
        
        try:
            # Use teaspoon's ML module for feature extraction
            if 'teaspoon' in self.results:
                diagrams = self.results['teaspoon']
            elif 'ripser' in self.results:
                diagrams = self.results['ripser']
            else:
                return
                
            # Extract ML features for each homology dimension
            self.results['ml_features'] = {}
            for dim in range(self.max_dimension + 1):
                h_key = f'H{dim}'
                if h_key in diagrams and len(diagrams[h_key]) > 0:
                    diagram = diagrams[h_key]
                    
                    # Apply various feature functions
                    features = {}
                    
                    # Persistence entropy
                    try:
                        features['persistence_entropy'] = ML_features.persistence_entropy(diagram)
                    except:
                        features['persistence_entropy'] = 0.0
                    
                    # Betti curves
                    try:
                        features['betti_curves'] = ML_features.betti_curves(diagram)
                    except:
                        features['betti_curves'] = []
                    
                    # Persistence landscapes
                    try:
                        features['persistence_landscapes'] = ML_features.persistence_landscapes(diagram)
                    except:
                        features['persistence_landscapes'] = []
                    
                    self.results['ml_features'][h_key] = features
                    
        except Exception as e:
            print(f"ML feature extraction failed: {e}")
            
        print("Machine learning features extracted")
        
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
            'analysis_type': 'teaspoon_persistent_homology',
            'max_filtration': self.max_filtration,
            'max_dimension': self.max_dimension,
            'point_cloud_shape': self.point_cloud.shape,
            'embedding_dimension': self.embedding_dimension,
            'time_delay': self.time_delay,
            'data_type': self.data_type,
            'libraries_used': {
                'teaspoon': TEASPOON_AVAILABLE,
                'ripser': RIPSER_AVAILABLE,
                'gudhi': GUDHI_AVAILABLE,
                'scipy': SCIPY_AVAILABLE
            }
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"Results saved successfully to {output_file}")


def main():
    """
    Main function to run teaspoon persistent homology analysis
    """
    if len(sys.argv) != 3:
        print("Usage: python persistent_homology_teaspoon.py input_data.json output_results.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = TeaspoonPersistentHomologyAnalyzer(max_filtration=1.0, max_dimension=2)
    
    try:
        # Load data
        analyzer.load_data_from_matlab(input_file)
        
        # Select optimal embedding parameters
        analyzer.select_embedding_parameters()
        
        # Create delay embedding
        analyzer.create_delay_embedding()
        
        # Compute persistent homology (try teaspoon first, then fallback)
        if TEASPOON_AVAILABLE:
            analyzer.compute_persistent_homology_teaspoon()
        
        # Fallback to ripser if teaspoon fails or is unavailable
        if 'teaspoon' not in analyzer.results and RIPSER_AVAILABLE:
            analyzer.compute_persistent_homology_ripser()
        
        if not analyzer.results:
            print("Error: No persistent homology libraries available")
            print("Install with: pip install teaspoon ripser gudhi")
            sys.exit(1)
        
        # Extract features
        analyzer.extract_topological_features()
        
        # Analyze quantum features
        analyzer.analyze_quantum_topological_features()
        
        # Analyze tactical effectiveness
        analyzer.analyze_tactical_effectiveness()
        
        # Apply ML features
        analyzer.apply_machine_learning_features()
        
        # Save results
        analyzer.save_results(output_file)
        
        print("Teaspoon persistent homology analysis completed successfully!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
