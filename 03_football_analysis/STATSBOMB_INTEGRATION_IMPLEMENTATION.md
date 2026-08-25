# StatsBomb Integration Implementation Guide

## 🎯 **Overview**

This guide provides detailed implementation instructions for integrating StatsBomb event data with our GPS-TDA Quantum Football framework, creating a comprehensive analysis system that combines event data with topological insights.

**Status**: 🎯 **Ready for Implementation**  
**Timeline**: 6-8 weeks  
**Complexity**: Medium-High

---

## 📊 **StatsBomb Data Structure**

### **Event Data Format**
```json
{
    "id": 12345,
    "index": 1,
    "period": 1,
    "timestamp": "00:00:15.123",
    "minute": 1,
    "second": 15,
    "type": {
        "id": 30,
        "name": "Pass"
    },
    "possession": 1,
    "possession_team": {
        "id": 1,
        "name": "Team A"
    },
    "play_pattern": {
        "id": 1,
        "name": "Regular Play"
    },
    "team": {
        "id": 1,
        "name": "Team A"
    },
    "player": {
        "id": 1234,
        "name": "Player Name"
    },
    "position": {
        "id": 23,
        "name": "Left Wing"
    },
    "location": [45.2, 67.8],
    "duration": 2.1,
    "under_pressure": false,
    "out": false,
    "pass": {
        "recipient": {
            "id": 5678,
            "name": "Recipient Name"
        },
        "length": 12.5,
        "angle": 45.0,
        "height": {
            "id": 1,
            "name": "Ground Pass"
        },
        "end_location": [57.7, 67.8],
        "assisted_shot_id": null,
        "backheel": false,
        "deflected": false,
        "miscommunication": false,
        "cross": false,
        "cut_back": false,
        "switch": false,
        "shot_assist": false,
        "goal_assist": false,
        "body_part": {
            "id": 40,
            "name": "Right Foot"
        },
        "type": {
            "id": 65,
            "name": "Cross"
        },
        "outcome": {
            "id": 9,
            "name": "Incomplete"
        }
    }
}
```

---

## 🔧 **Implementation Architecture**

### **1. Data Loading and Preprocessing**

#### **StatsBomb Data Loader Class**
```python
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class StatsBombDataLoader:
    """
    Loads and preprocesses StatsBomb event data for TDA analysis
    """
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.events_data = None
        self.lineups_data = None
        self.matches_data = None
        
    def load_match_data(self, match_id: int) -> Dict:
        """
        Load complete match data including events, lineups, and match info
        
        Args:
            match_id: StatsBomb match ID
            
        Returns:
            Dictionary containing all match data
        """
        match_data = {}
        
        # Load events
        events_file = self.data_path / f"{match_id}.json"
        if events_file.exists():
            with open(events_file, 'r') as f:
                match_data['events'] = json.load(f)
        
        # Load lineups
        lineups_file = self.data_path / f"{match_id}_lineups.json"
        if lineups_file.exists():
            with open(lineups_file, 'r') as f:
                match_data['lineups'] = json.load(f)
        
        # Load match info
        matches_file = self.data_path / "matches.json"
        if matches_file.exists():
            with open(matches_file, 'r') as f:
                matches = json.load(f)
                match_data['match_info'] = next(
                    (m for m in matches if m['match_id'] == match_id), None
                )
        
        return match_data
    
    def extract_player_positions(self, events: List[Dict]) -> pd.DataFrame:
        """
        Extract player positions from event data
        
        Args:
            events: List of event dictionaries
            
        Returns:
            DataFrame with player positions over time
        """
        positions_data = []
        
        for event in events:
            if 'location' in event and event['location'] is not None:
                positions_data.append({
                    'timestamp': event['timestamp'],
                    'minute': event['minute'],
                    'second': event['second'],
                    'player_id': event['player']['id'],
                    'player_name': event['player']['name'],
                    'team_id': event['team']['id'],
                    'team_name': event['team']['name'],
                    'position_id': event['position']['id'],
                    'position_name': event['position']['name'],
                    'x': event['location'][0],
                    'y': event['location'][1],
                    'event_type': event['type']['name'],
                    'event_id': event['id']
                })
        
        return pd.DataFrame(positions_data)
    
    def create_time_series_data(self, positions_df: pd.DataFrame) -> np.ndarray:
        """
        Create time series data for TDA analysis
        
        Args:
            positions_df: DataFrame with player positions
            
        Returns:
            Numpy array suitable for TDA analysis
        """
        # Group by timestamp and create team position matrices
        time_series = []
        
        for timestamp, group in positions_df.groupby('timestamp'):
            # Separate home and away teams
            home_team = group[group['team_id'] == group['team_id'].iloc[0]]
            away_team = group[group['team_id'] != group['team_id'].iloc[0]]
            
            # Create position vectors (pad with zeros if players missing)
            home_positions = np.zeros((11, 2))  # 11 players max
            away_positions = np.zeros((11, 2))
            
            # Fill in actual positions
            for i, (_, player) in enumerate(home_team.iterrows()):
                if i < 11:
                    home_positions[i] = [player['x'], player['y']]
            
            for i, (_, player) in enumerate(away_team.iterrows()):
                if i < 11:
                    away_positions[i] = [player['x'], player['y']]
            
            # Combine into single vector
            combined_positions = np.concatenate([
                home_positions.flatten(),
                away_positions.flatten()
            ])
            
            time_series.append(combined_positions)
        
        return np.array(time_series)
```

### **2. TDA Analysis Integration**

#### **StatsBomb TDA Analyzer**
```python
import ripser
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

class StatsBombTDAAnalyzer:
    """
    Applies TDA analysis to StatsBomb event data
    """
    
    def __init__(self, max_filtration: float = 1.0, max_dimension: int = 2):
        self.max_filtration = max_filtration
        self.max_dimension = max_dimension
        self.scaler = StandardScaler()
        
    def analyze_match_tda(self, time_series_data: np.ndarray) -> Dict:
        """
        Perform TDA analysis on match time series data
        
        Args:
            time_series_data: Time series of player positions
            
        Returns:
            Dictionary containing TDA results
        """
        # Normalize data
        normalized_data = self.scaler.fit_transform(time_series_data)
        
        # Compute persistent homology
        ripser_results = ripser.ripser(
            normalized_data,
            maxdim=self.max_dimension,
            thresh=self.max_filtration
        )
        
        # Extract persistence diagrams
        persistence_diagrams = {}
        for dim in range(self.max_dimension + 1):
            if dim < len(ripser_results['dgms']):
                persistence_diagrams[f'H{dim}'] = ripser_results['dgms'][dim]
            else:
                persistence_diagrams[f'H{dim}'] = np.array([]).reshape(0, 2)
        
        # Compute topological features
        topological_features = self._extract_topological_features(persistence_diagrams)
        
        return {
            'persistence_diagrams': persistence_diagrams,
            'topological_features': topological_features,
            'ripser_results': ripser_results
        }
    
    def _extract_topological_features(self, persistence_diagrams: Dict) -> Dict:
        """
        Extract meaningful topological features from persistence diagrams
        
        Args:
            persistence_diagrams: Dictionary of persistence diagrams
            
        Returns:
            Dictionary of topological features
        """
        features = {}
        
        for dim, diagram in persistence_diagrams.items():
            if len(diagram) > 0:
                # Basic statistics
                features[f'{dim}_count'] = len(diagram)
                features[f'{dim}_mean_persistence'] = np.mean(diagram[:, 1] - diagram[:, 0])
                features[f'{dim}_max_persistence'] = np.max(diagram[:, 1] - diagram[:, 0])
                features[f'{dim}_std_persistence'] = np.std(diagram[:, 1] - diagram[:, 0])
                
                # Birth and death statistics
                features[f'{dim}_mean_birth'] = np.mean(diagram[:, 0])
                features[f'{dim}_mean_death'] = np.mean(diagram[:, 1])
                
                # Persistence entropy
                persistences = diagram[:, 1] - diagram[:, 0]
                if np.sum(persistences) > 0:
                    normalized_persistences = persistences / np.sum(persistences)
                    features[f'{dim}_persistence_entropy'] = -np.sum(
                        normalized_persistences * np.log(normalized_persistences + 1e-10)
                    )
                else:
                    features[f'{dim}_persistence_entropy'] = 0
            else:
                # Handle empty diagrams
                features[f'{dim}_count'] = 0
                features[f'{dim}_mean_persistence'] = 0
                features[f'{dim}_max_persistence'] = 0
                features[f'{dim}_std_persistence'] = 0
                features[f'{dim}_mean_birth'] = 0
                features[f'{dim}_mean_death'] = 0
                features[f'{dim}_persistence_entropy'] = 0
        
        return features
```

### **3. Quantum Event Dynamics**

#### **Quantum Event Modeling**
```python
class QuantumEventDynamics:
    """
    Applies quantum analogies to StatsBomb event data
    """
    
    def __init__(self):
        self.quantum_parameters = {}
        
    def analyze_quantum_events(self, events_df: pd.DataFrame, 
                             topological_features: Dict) -> Dict:
        """
        Apply quantum analogies to event data
        
        Args:
            events_df: DataFrame of events
            topological_features: TDA topological features
            
        Returns:
            Dictionary of quantum event dynamics
        """
        quantum_analysis = {}
        
        # Quantum dot size from formation compactness
        quantum_analysis['quantum_dot_size'] = self._compute_quantum_dot_size(events_df)
        
        # Exciton dynamics from pass events
        quantum_analysis['exciton_dynamics'] = self._analyze_exciton_dynamics(events_df)
        
        # Quantum tunneling from formation changes
        quantum_analysis['quantum_tunneling'] = self._analyze_quantum_tunneling(events_df)
        
        # Photoluminescence from shot events
        quantum_analysis['photoluminescence'] = self._analyze_photoluminescence(events_df)
        
        # Quantum coherence from team coordination
        quantum_analysis['quantum_coherence'] = self._analyze_quantum_coherence(
            events_df, topological_features
        )
        
        return quantum_analysis
    
    def _compute_quantum_dot_size(self, events_df: pd.DataFrame) -> float:
        """
        Compute quantum dot size from formation compactness
        
        Args:
            events_df: DataFrame of events
            
        Returns:
            Quantum dot size parameter
        """
        # Calculate team spread at each timestamp
        team_spreads = []
        
        for timestamp, group in events_df.groupby('timestamp'):
            if len(group) >= 2:  # Need at least 2 players
                x_coords = group['x'].values
                y_coords = group['y'].values
                
                # Calculate spread (standard deviation of positions)
                x_spread = np.std(x_coords)
                y_spread = np.std(y_coords)
                total_spread = np.sqrt(x_spread**2 + y_spread**2)
                
                team_spreads.append(total_spread)
        
        if team_spreads:
            mean_spread = np.mean(team_spreads)
            # Quantum dot size inversely related to spread
            quantum_dot_size = 1.0 / (mean_spread + 1e-6)
        else:
            quantum_dot_size = 1.0
        
        return quantum_dot_size
    
    def _analyze_exciton_dynamics(self, events_df: pd.DataFrame) -> Dict:
        """
        Analyze exciton dynamics from pass events
        
        Args:
            events_df: DataFrame of events
            
        Returns:
            Dictionary of exciton dynamics
        """
        pass_events = events_df[events_df['event_type'] == 'Pass']
        
        if len(pass_events) == 0:
            return {
                'binding_energy': 0.0,
                'formation_rate': 0.0,
                'decay_rate': 0.0
            }
        
        # Calculate pass distances (exciton binding energy)
        pass_distances = []
        for _, pass_event in pass_events.iterrows():
            if 'pass' in pass_event and 'end_location' in pass_event['pass']:
                start_pos = [pass_event['x'], pass_event['y']]
                end_pos = pass_event['pass']['end_location']
                distance = np.sqrt(
                    (start_pos[0] - end_pos[0])**2 + 
                    (start_pos[1] - end_pos[1])**2
                )
                pass_distances.append(distance)
        
        if pass_distances:
            mean_distance = np.mean(pass_distances)
            # Exciton binding energy inversely related to distance
            binding_energy = 1.0 / (mean_distance + 1e-6)
            formation_rate = binding_energy
            decay_rate = mean_distance / 10.0
        else:
            binding_energy = 0.1
            formation_rate = 0.1
            decay_rate = 0.1
        
        return {
            'binding_energy': binding_energy,
            'formation_rate': formation_rate,
            'decay_rate': decay_rate
        }
    
    def _analyze_quantum_tunneling(self, events_df: pd.DataFrame) -> Dict:
        """
        Analyze quantum tunneling from formation changes
        
        Args:
            events_df: DataFrame of events
            
        Returns:
            Dictionary of quantum tunneling analysis
        """
        # Identify formation changes (simplified)
        formation_changes = 0
        total_events = len(events_df)
        
        # Count events that might indicate formation changes
        formation_change_events = ['Substitution', 'Formation Change', 'Tactical Change']
        for event_type in formation_change_events:
            formation_changes += len(events_df[events_df['event_type'] == event_type])
        
        # Quantum tunneling probability
        if total_events > 0:
            tunneling_probability = formation_changes / total_events
        else:
            tunneling_probability = 0.0
        
        return {
            'tunneling_probability': tunneling_probability,
            'formation_changes': formation_changes,
            'total_events': total_events
        }
    
    def _analyze_photoluminescence(self, events_df: pd.DataFrame) -> Dict:
        """
        Analyze photoluminescence from shot events
        
        Args:
            events_df: DataFrame of events
            
        Returns:
            Dictionary of photoluminescence analysis
        """
        shot_events = events_df[events_df['event_type'] == 'Shot']
        
        if len(shot_events) == 0:
            return {
                'intensity': 0.0,
                'lifetime': 0.0,
                'quantum_yield': 0.0
            }
        
        # Calculate shot effectiveness (simplified)
        successful_shots = 0
        total_shots = len(shot_events)
        
        for _, shot in shot_events.iterrows():
            if 'shot' in shot and 'outcome' in shot['shot']:
                outcome = shot['shot']['outcome']['name']
                if outcome in ['Goal', 'Saved']:  # Consider saved shots as effective
                    successful_shots += 1
        
        # Photoluminescence intensity from shot effectiveness
        if total_shots > 0:
            intensity = successful_shots / total_shots
            lifetime = 10.0  # Arbitrary lifetime
            quantum_yield = intensity / (intensity + 1.0)
        else:
            intensity = 0.0
            lifetime = 0.0
            quantum_yield = 0.0
        
        return {
            'intensity': intensity,
            'lifetime': lifetime,
            'quantum_yield': quantum_yield
        }
    
    def _analyze_quantum_coherence(self, events_df: pd.DataFrame, 
                                 topological_features: Dict) -> float:
        """
        Analyze quantum coherence from team coordination
        
        Args:
            events_df: DataFrame of events
            topological_features: TDA topological features
            
        Returns:
            Quantum coherence value
        """
        # Use H0 features as a proxy for team coherence
        h0_count = topological_features.get('H0_count', 0)
        h0_mean_persistence = topological_features.get('H0_mean_persistence', 0)
        
        # Quantum coherence based on topological connectivity
        if h0_count > 0:
            coherence = h0_mean_persistence / (h0_count + 1e-6)
        else:
            coherence = 0.5  # Default coherence
        
        return min(max(coherence, 0.0), 1.0)  # Clamp between 0 and 1
```

### **4. Main Analysis Script**

#### **Complete StatsBomb Analysis**
```python
#!/usr/bin/env python3
"""
StatsBomb TDA Analysis Script
============================

This script performs comprehensive TDA and quantum analysis on StatsBomb event data.
"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    parser = argparse.ArgumentParser(description='Analyze StatsBomb data with TDA')
    parser.add_argument('--match_id', type=int, required=True, 
                       help='StatsBomb match ID')
    parser.add_argument('--data_path', type=str, required=True,
                       help='Path to StatsBomb data directory')
    parser.add_argument('--output_dir', type=str, default='./statsbomb_results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"Analyzing StatsBomb match {args.match_id}")
    print(f"Data path: {args.data_path}")
    print(f"Output directory: {output_dir}")
    
    # Load data
    loader = StatsBombDataLoader(args.data_path)
    match_data = loader.load_match_data(args.match_id)
    
    if 'events' not in match_data:
        print("Error: No events data found")
        return
    
    # Extract positions
    positions_df = loader.extract_player_positions(match_data['events'])
    print(f"Extracted {len(positions_df)} position records")
    
    # Create time series
    time_series_data = loader.create_time_series_data(positions_df)
    print(f"Created time series with shape: {time_series_data.shape}")
    
    # TDA Analysis
    tda_analyzer = StatsBombTDAAnalyzer()
    tda_results = tda_analyzer.analyze_match_tda(time_series_data)
    print("Completed TDA analysis")
    
    # Quantum Analysis
    quantum_analyzer = QuantumEventDynamics()
    quantum_results = quantum_analyzer.analyze_quantum_events(
        positions_df, tda_results['topological_features']
    )
    print("Completed quantum analysis")
    
    # Save results
    results = {
        'match_id': args.match_id,
        'tda_results': tda_results,
        'quantum_results': quantum_results,
        'topological_features': tda_results['topological_features']
    }
    
    # Save to JSON
    with open(output_dir / f"match_{args.match_id}_analysis.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save topological features to CSV
    features_df = pd.DataFrame([tda_results['topological_features']])
    features_df.to_csv(output_dir / f"match_{args.match_id}_features.csv", index=False)
    
    # Create visualizations
    create_visualizations(tda_results, quantum_results, output_dir, args.match_id)
    
    print(f"Analysis complete. Results saved to {output_dir}")

def create_visualizations(tda_results, quantum_results, output_dir, match_id):
    """
    Create visualizations for the analysis results
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'StatsBomb TDA Analysis - Match {match_id}', fontsize=16)
    
    # Plot 1: Persistence diagrams
    ax1 = axes[0, 0]
    for dim, diagram in tda_results['persistence_diagrams'].items():
        if len(diagram) > 0:
            ax1.scatter(diagram[:, 0], diagram[:, 1], label=dim, alpha=0.7)
    ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    ax1.set_xlabel('Birth')
    ax1.set_ylabel('Death')
    ax1.set_title('Persistence Diagrams')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Topological features
    ax2 = axes[0, 1]
    features = tda_results['topological_features']
    feature_names = [k for k in features.keys() if 'count' in k]
    feature_values = [features[k] for k in feature_names]
    ax2.bar(feature_names, feature_values)
    ax2.set_title('Topological Feature Counts')
    ax2.set_ylabel('Count')
    plt.setp(ax2.get_xticklabels(), rotation=45)
    
    # Plot 3: Quantum parameters
    ax3 = axes[1, 0]
    quantum_params = {
        'Quantum Dot Size': quantum_results['quantum_dot_size'],
        'Binding Energy': quantum_results['exciton_dynamics']['binding_energy'],
        'Tunneling Prob': quantum_results['quantum_tunneling']['tunneling_probability'],
        'Coherence': quantum_results['quantum_coherence']
    }
    ax3.bar(quantum_params.keys(), quantum_params.values())
    ax3.set_title('Quantum Parameters')
    ax3.set_ylabel('Value')
    plt.setp(ax3.get_xticklabels(), rotation=45)
    
    # Plot 4: Photoluminescence
    ax4 = axes[1, 1]
    photo_params = quantum_results['photoluminescence']
    ax4.bar(['Intensity', 'Lifetime', 'Quantum Yield'], 
            [photo_params['intensity'], photo_params['lifetime'], photo_params['quantum_yield']])
    ax4.set_title('Photoluminescence Analysis')
    ax4.set_ylabel('Value')
    
    plt.tight_layout()
    plt.savefig(output_dir / f"match_{match_id}_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
```

---

## 🚀 **Usage Instructions**

### **1. Installation Requirements**
```bash
# Install required Python packages
pip install pandas numpy scikit-learn ripser matplotlib seaborn

# Install StatsBomb data (if not already available)
# Download from: https://github.com/statsbomb/open-data
```

### **2. Running the Analysis**
```bash
# Basic usage
python analyze_statsbomb_tda.py --match_id 12345 --data_path ./statsbomb_data

# With custom output directory
python analyze_statsbomb_tda.py --match_id 12345 --data_path ./statsbomb_data --output_dir ./results
```

### **3. Expected Output**
- **JSON file**: Complete analysis results
- **CSV file**: Topological features for further analysis
- **PNG file**: Visualization plots
- **Log output**: Analysis progress and statistics

---

## 📊 **Integration with Existing Framework**

### **MATLAB Integration**
```matlab
% Import StatsBomb results to MATLAB
function importStatsBombResults(json_file_path, output_dir)
    % Load JSON results
    results = jsondecode(fileread(json_file_path));
    
    % Extract topological features
    topological_features = results.topological_features;
    
    % Extract quantum results
    quantum_results = results.quantum_results;
    
    % Save as MATLAB variables
    save(fullfile(output_dir, 'statsbomb_analysis.mat'), ...
         'topological_features', 'quantum_results');
    
    fprintf('StatsBomb results imported successfully\n');
end
```

### **Integration with Existing Classes**
```matlab
% Extend existing classes for StatsBomb data
classdef StatsBombTDAIntegration < PersistentHomologyAnalysis
    methods
        function obj = StatsBombTDAIntegration(statsbomb_results)
            % Initialize with StatsBomb results
            obj.topological_features = statsbomb_results.topological_features;
            obj.quantum_results = statsbomb_results.quantum_results;
        end
        
        function obj = compareWithGPSData(obj, gps_results)
            % Compare StatsBomb results with GPS data
            % Implementation here
        end
    end
end
```

---

## 🎯 **Next Steps**

### **Immediate Implementation (Week 1-2)**
1. **Set up development environment**
2. **Implement data loader class**
3. **Test with sample StatsBomb data**
4. **Implement basic TDA analysis**

### **Core Development (Week 3-4)**
1. **Complete TDA analyzer**
2. **Implement quantum event dynamics**
3. **Create visualization functions**
4. **Test with multiple matches**

### **Integration and Testing (Week 5-6)**
1. **Integrate with existing MATLAB framework**
2. **Performance optimization**
3. **Comprehensive testing**
4. **Documentation completion**

### **Deployment (Week 7-8)**
1. **Final testing and validation**
2. **User documentation**
3. **Example notebooks**
4. **Release preparation**

---

## 📋 **Success Metrics**

### **Technical Metrics**
- **Data Processing**: Successfully load and process StatsBomb data
- **TDA Analysis**: Generate meaningful topological features
- **Quantum Analysis**: Apply quantum analogies to event data
- **Integration**: Seamless integration with existing framework

### **Performance Metrics**
- **Processing Time**: <30 seconds for full match analysis
- **Memory Usage**: <500MB for typical match
- **Accuracy**: Consistent results across different matches
- **Scalability**: Handle multiple matches efficiently

### **Validation Metrics**
- **Topological Features**: Meaningful and interpretable features
- **Quantum Parameters**: Physically reasonable values
- **Correlations**: Strong correlations with match outcomes
- **Reproducibility**: Consistent results across runs

---

This implementation guide provides a comprehensive roadmap for integrating StatsBomb data with our GPS-TDA framework, creating a powerful analysis system that combines event data with topological insights and quantum analogies.
