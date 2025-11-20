# Multi-Goal Analysis Framework - Usage Guide

**Date**: December 2024  
**Purpose**: Complete guide for using the unified multi-goal analysis framework  
**Status**: ✅ **READY FOR USE**

---

## Overview

The `MultiGoalAnalysis` class provides a unified framework for running GPS-aware TDA analysis across **all three validated goal-dependent regimes** simultaneously. This enables comprehensive multi-scale tactical analysis.

---

## Quick Start

### Basic Usage

```python
from multi_goal_analysis import MultiGoalAnalysis, analyze_all_goals
import numpy as np

# Create analyzer
analyzer = MultiGoalAnalysis()

# Player positions: array of shape (n_players, 2)
# Example: 22 players (11 home + 11 away)
player_positions = np.array([
    # Home team (11 players)
    [30.5, 25.3],
    [32.1, 27.8],
    # ... (all 22 players)
])

# Analyze all three goals simultaneously
results = analyzer.analyze_all_goals(player_positions)

# Access results
print(results['individual']['h0_count'])  # Individual player H0
print(results['tactical']['h0_count'])    # Tactical group H0
print(results['team']['h0_count'])        # Team-level H0
```

### Convenience Functions

```python
from multi_goal_analysis import analyze_all_goals, analyze_single_goal

# Analyze all goals at once
results = analyze_all_goals(player_positions)

# Analyze single goal
individual_results = analyze_single_goal(player_positions, goal='individual')
tactical_results = analyze_single_goal(player_positions, goal='tactical')
team_results = analyze_single_goal(player_positions, goal='team')
```

---

## Analysis Goals

### 1. Individual Player Analysis

**Cut-off**: 2.98m (validated)  
**Expected H0**: 15-22 components  
**Temporal Stability**: 0.88  

**Questions Answered**:
- How are individual players positioned?
- Which players form tight spatial clusters?
- Are there isolated players?

**Use Cases**:
- Player positioning analysis
- Individual movement patterns
- Small-group dynamics (2-3 players)

```python
individual = analyzer.analyze_single_goal(positions, goal='individual')
# Returns: h0_count (15-22), validation, interpretation
```

---

### 2. Tactical Group Analysis

**Cut-off**: 16.31m (validated)  
**Expected H0**: 3-12 components  
**Temporal Stability**: 0.97  

**Questions Answered**:
- How are players organized into tactical groups?
- What is the formation structure? (defense, midfield, attack)
- What is the tactical formation complexity?

**Use Cases**:
- Formation analysis (4-4-2, 4-3-3, etc.)
- Tactical positioning
- Zone control analysis

```python
tactical = analyzer.analyze_single_goal(positions, goal='tactical')
# Returns: h0_count (3-12), validation, interpretation
```

---

### 3. Team-Level Analysis

**Cut-off**: 28.11m (validated)  
**Expected H0**: 1-3 components  
**Temporal Stability**: 0.98  

**Questions Answered**:
- How are the two teams separated spatially?
- What is the overall field shape? (compact vs. spread)
- What are the major spatial zones?

**Use Cases**:
- Team separation analysis
- Macro-spatial patterns
- Overall formation shape
- Field control metrics

```python
team = analyzer.analyze_single_goal(positions, goal='team')
# Returns: h0_count (1-3), validation, interpretation
```

---

## Results Structure

### Single Goal Results

```python
{
    'goal': 'individual',              # Analysis goal
    'cutoff_distance': 2.98,          # Cut-off used
    'h0_count': 18,                   # Computed H0
    'h1_count': 2,                    # Computed H1
    'cluster_count': 18,              # Number of clusters
    'complexity_index': 1.11,         # (H0 + H1) / clusters
    'h0_valid': True,                 # H0 in expected range?
    'h0_expected_range': (15, 22),    # Expected H0 range
    'validation_message': 'H0=18 in expected range (15-22) ✅',
    'interpretation': 'Moderate player spread...',
    'n_players': 22                   # Number of players
}
```

### All Goals Results

```python
{
    'individual': { ... },            # Individual analysis results
    'tactical': { ... },              # Tactical analysis results
    'team': { ... },                  # Team analysis results
    'summary': {
        'n_players': 22,
        'all_valid': True,            # All H0 in expected ranges?
        'h0_range': {
            'individual': 18,
            'tactical': 5,
            'team': 2
        },
        'scale_comparison': '✅ Hierarchical ordering: Individual > Tactical > Team'
    }
}
```

---

## Batch Analysis

### Analyze Multiple Snapshots

```python
# List of player position arrays (one per timepoint)
position_snapshots = [
    positions_frame_1,  # Shape: (22, 2)
    positions_frame_2,  # Shape: (22, 2)
    positions_frame_3,  # Shape: (22, 2)
    # ...
]

# Analyze all goals for all snapshots
df = analyzer.analyze_batch(position_snapshots)

# Result: DataFrame with one row per snapshot per goal
# Columns: goal, h0_count, h1_count, validation, etc.

# Analyze single goal for all snapshots
df_individual = analyzer.analyze_batch(position_snapshots, goal='individual')
```

---

## Validation

### Automatic H0 Range Validation

The framework automatically validates that H0 falls within expected ranges:

```python
results = analyzer.analyze_all_goals(positions)

# Check validation status
for goal in ['individual', 'tactical', 'team']:
    r = results[goal]
    if r['h0_valid']:
        print(f"{goal}: ✅ Valid - {r['validation_message']}")
    else:
        print(f"{goal}: ⚠️ Warning - {r['validation_message']}")
```

### Hierarchical Ordering Check

Results include automatic checking of expected hierarchical ordering:
- Individual H0 > Tactical H0 > Team H0

```python
summary = results['summary']
print(summary['scale_comparison'])
# "✅ Hierarchical ordering: Individual > Tactical > Team (expected)"
```

---

## Integration with Existing Scripts

### Example: Update `multi_scale_temporal_analysis.py`

```python
from multi_goal_analysis import MultiGoalAnalysis

class MultiScaleTemporalAnalysis:
    def __init__(self, ...):
        self.multi_goal_analyzer = MultiGoalAnalysis()
    
    def analyze_window(self, player_positions):
        # Run all three goals
        results = self.multi_goal_analyzer.analyze_all_goals(player_positions)
        
        # Store results
        return {
            'individual_h0': results['individual']['h0_count'],
            'tactical_h0': results['tactical']['h0_count'],
            'team_h0': results['team']['h0_count'],
            'all_results': results
        }
```

### Example: Update `statsbomb_validation_pipeline.py`

```python
from multi_goal_analysis import MultiGoalAnalysis

class StatsBombValidationPipeline:
    def __init__(self, ...):
        self.multi_goal_analyzer = MultiGoalAnalysis()
    
    def compute_gps_aware_h0(self, player_positions):
        # OLD: Single cut-off analysis
        # NEW: Multi-goal analysis
        results = self.multi_goal_analyzer.analyze_all_goals(player_positions)
        
        return {
            'individual': results['individual'],
            'tactical': results['tactical'],
            'team': results['team'],
            'all_valid': results['summary']['all_valid']
        }
```

---

## Custom Cut-off Distances

You can override validated cut-offs if needed:

```python
# Use custom cut-offs
custom_cutoffs = {
    'individual': 3.0,   # Slightly higher than validated
    'tactical': 15.0,    # Slightly lower than validated
    'team': 28.0         # Slightly lower than validated
}

results = analyzer.analyze_all_goals(positions, custom_cutoffs=custom_cutoffs)
```

**Note**: Overriding validated cut-offs should be done with caution. The validated values (2.98m, 16.31m, 28.11m) have high temporal stability (>0.88) and should be preferred unless you have specific reasons to deviate.

---

## Output Formatting

### Print Results Summary

```python
def print_results_summary(results):
    """Pretty print multi-goal analysis results"""
    print("="*70)
    print("MULTI-GOAL ANALYSIS RESULTS")
    print("="*70)
    
    for goal in ['individual', 'tactical', 'team']:
        r = results[goal]
        status = "✅" if r['h0_valid'] else "⚠️"
        
        print(f"\n{goal.upper()} ANALYSIS {status}")
        print(f"  Cut-off: {r['cutoff_distance']:.2f}m")
        print(f"  H0: {r['h0_count']} (expected: {r['h0_expected_range']})")
        print(f"  H1: {r['h1_count']}")
        print(f"  {r['validation_message']}")
        print(f"  {r['interpretation']}")
    
    print(f"\nSummary: {results['summary']['scale_comparison']}")
    print("="*70)
```

---

## Method Documentation

### Get Methodology Summary

```python
analyzer = MultiGoalAnalysis()
methodology = analyzer.get_methodology_summary()
print(methodology)
```

This prints:
- Validated cut-off distances
- Expected H0 ranges
- Temporal stability scores
- Use cases for each goal
- Validation methodology

---

## Examples

### Example 1: Single Snapshot Analysis

```python
from multi_goal_analysis import analyze_all_goals
import numpy as np

# Load player positions from your data source
player_positions = load_player_positions(frame_idx=1000)

# Analyze all goals
results = analyze_all_goals(player_positions)

# Access results
print(f"Individual H0: {results['individual']['h0_count']}")
print(f"Tactical H0: {results['tactical']['h0_count']}")
print(f"Team H0: {results['team']['h0_count']}")
```

### Example 2: Temporal Window Analysis

```python
from multi_goal_analysis import MultiGoalAnalysis

analyzer = MultiGoalAnalysis()

# Analyze each window
for window in temporal_windows:
    positions = extract_positions(window)
    results = analyzer.analyze_all_goals(positions)
    
    # Store or process results
    store_results(window.id, results)
```

### Example 3: Batch Processing

```python
from multi_goal_analysis import MultiGoalAnalysis

analyzer = MultiGoalAnalysis()

# Process all frames
all_positions = [extract_positions(f) for f in frames]

# Batch analyze
df_results = analyzer.analyze_batch(all_positions)

# Analyze results
print(df_results.groupby('goal')['h0_count'].describe())
```

---

## Benefits

### 1. Comprehensive Analysis
- Get insights at all three scales simultaneously
- Complete tactical picture (micro → meso → macro)

### 2. Validated Methodology
- Uses validated cut-off distances (high temporal stability)
- Automatic H0 range validation
- Built-in quality checks

### 3. Easy Integration
- Simple API
- Compatible with existing scripts
- Batch processing support

### 4. Publication Ready
- Validated methodology documented
- Clear interpretation guidelines
- Consistent with research standards

---

## References

- **Methodology**: `METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md`
- **Validation**: `cutoff_efficacy_results/investigation_summary.json`
- **Comparison**: `NORMALIZED_SAMPLING_RESULTS_COMPARISON.md`

---

## Next Steps

1. **Integrate into existing scripts**: Update `multi_scale_temporal_analysis.py`, `statsbomb_validation_pipeline.py`, etc.
2. **Re-analyze existing data**: Run all three goals on current datasets
3. **Create visualizations**: Compare results across all three scales
4. **Update documentation**: Include multi-goal results in publications

---

**Status**: ✅ **READY FOR PRODUCTION USE**

