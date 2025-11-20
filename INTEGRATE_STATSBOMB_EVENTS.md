# Integrating StatsBomb Events with H1 Loop Analysis

## Overview

This guide explains how to integrate **StatsBomb event data** with H1 loop analysis to correlate topological patterns with actual match events (goals, shots, passes, possession changes, etc.).

---

## 1. StatsBomb Data Structure

### 1.1 Events Data

**File Structure**:
```
open-data/data/events/{match_id}.json
```

**Event Schema** (key fields):
```json
{
  "id": 123456,
  "index": 45,
  "period": 1,
  "timestamp": "00:03:15.123",
  "minute": 3,
  "second": 15,
  "type": {
    "id": 1,
    "name": "Pass"
  },
  "possession": 5,
  "team": {...},
  "player": {...},
  "location": [x, y],
  ...
}
```

**Important Event Types**:
- `Goal` (id: 16)
- `Shot` (id: 16)
- `Pass` (id: 30)
- `Ball Receipt` (id: 14)
- `Dribble` (id: 10)
- `Tackle` (id: 4)
- `Interception` (id: 21)
- `Clearance` (id: 6)
- `Formation Change` (via lineup data)

### 1.2 Timestamp Conversion

**Challenge**: Events have `timestamp` (e.g., "00:03:15.123"), loops have `frame_idx`.

**Solution**:
```python
def timestamp_to_frame(timestamp, fps=25.0):
    """
    Convert StatsBomb timestamp to frame index
    
    Args:
        timestamp: String like "00:03:15.123" or dict with minute/second
        fps: Frames per second (default 25.0 for typical GPS data)
    
    Returns:
        frame_index (int)
    """
    if isinstance(timestamp, str):
        # Parse "00:03:15.123"
        parts = timestamp.split(':')
        minutes = int(parts[0])
        seconds = float(parts[1])
        total_seconds = minutes * 60 + seconds
    elif isinstance(timestamp, dict):
        # Parse from minute/second dict
        total_seconds = timestamp['minute'] * 60 + timestamp['second']
    
    return int(total_seconds * fps)
```

---

## 2. Integration Code

### 2.1 Event Loader

```python
import json
from pathlib import Path
import pandas as pd

class StatsBombEventLoader:
    """Load and process StatsBomb event data"""
    
    def __init__(self, data_dir='open-data/data'):
        self.data_dir = Path(data_dir)
    
    def load_match_events(self, match_id):
        """Load events for a specific match"""
        events_file = self.data_dir / 'events' / f'{match_id}.json'
        
        if not events_file.exists():
            raise FileNotFoundError(f"Events file not found: {events_file}")
        
        with open(events_file, 'r') as f:
            events = json.load(f)
        
        return events
    
    def extract_important_events(self, events, event_types=None):
        """
        Extract important events from match data
        
        Args:
            events: List of event dictionaries
            event_types: List of event type names (default: common important types)
        
        Returns:
            DataFrame with important events
        """
        if event_types is None:
            event_types = ['Goal', 'Shot', 'Pass', 'Ball Receipt', 
                          'Dribble', 'Tackle', 'Interception', 'Clearance']
        
        important_events = []
        for event in events:
            event_type = event.get('type', {}).get('name', '')
            if event_type in event_types:
                important_events.append({
                    'event_id': event.get('id'),
                    'index': event.get('index'),
                    'period': event.get('period'),
                    'timestamp': event.get('timestamp'),
                    'minute': event.get('minute'),
                    'second': event.get('second'),
                    'type': event_type,
                    'team': event.get('team', {}).get('name', ''),
                    'player': event.get('player', {}).get('name', ''),
                    'location': event.get('location', [None, None]),
                    'possession': event.get('possession'),
                    'raw_event': event  # Keep full event for later
                })
        
        return pd.DataFrame(important_events)
    
    def convert_to_frame_indices(self, events_df, fps=25.0):
        """
        Convert event timestamps to frame indices
        
        Args:
            events_df: DataFrame with events
            fps: Frames per second
        
        Returns:
            DataFrame with frame_idx column added
        """
        events_df = events_df.copy()
        
        def timestamp_to_frame(row):
            if pd.notna(row['timestamp']):
                # Parse timestamp string
                parts = str(row['timestamp']).split(':')
                minutes = int(parts[0])
                seconds = float(parts[1])
                total_seconds = minutes * 60 + seconds
            elif pd.notna(row['minute']) and pd.notna(row['second']):
                # Use minute/second
                total_seconds = row['minute'] * 60 + row['second']
            else:
                return None
            
            return int(total_seconds * fps)
        
        events_df['frame_idx'] = events_df.apply(timestamp_to_frame, axis=1)
        return events_df
```

### 2.2 Correlation Analysis

```python
class H1StatsBombCorrelation:
    """Correlate H1 loops with StatsBomb events"""
    
    def __init__(self, loops_df, events_df):
        """
        Args:
            loops_df: DataFrame with H1 loop data
            events_df: DataFrame with StatsBomb events (with frame_idx)
        """
        self.loops_df = loops_df
        self.events_df = events_df
    
    def analyze_around_events(self, event_types=None, window_frames=20):
        """
        Analyze loop patterns around specific event types
        
        Args:
            event_types: List of event type names (None = all)
            window_frames: Number of frames before/after to analyze
        
        Returns:
            Dictionary with analysis results
        """
        if event_types is None:
            events_to_analyze = self.events_df
        else:
            events_to_analyze = self.events_df[
                self.events_df['type'].isin(event_types)
            ]
        
        results = {}
        
        for event_type in events_to_analyze['type'].unique():
            type_events = events_to_analyze[
                events_to_analyze['type'] == event_type
            ]
            
            type_results = []
            for _, event in type_events.iterrows():
                event_frame = event['frame_idx']
                
                if pd.isna(event_frame):
                    continue
                
                # Get loops in window
                window_loops = self.loops_df[
                    (self.loops_df['frame_idx'] >= event_frame - window_frames) &
                    (self.loops_df['frame_idx'] <= event_frame + window_frames)
                ].copy()
                
                # Calculate before/after metrics
                before_loops = window_loops[
                    window_loops['frame_idx'] < event_frame
                ]
                after_loops = window_loops[
                    window_loops['frame_idx'] > event_frame
                ]
                
                type_results.append({
                    'event_id': event['event_id'],
                    'event_frame': event_frame,
                    'before_mean_persistence': before_loops['persistence'].mean() if len(before_loops) > 0 else 0,
                    'after_mean_persistence': after_loops['persistence'].mean() if len(after_loops) > 0 else 0,
                    'before_n_loops': len(before_loops),
                    'after_n_loops': len(after_loops),
                })
            
            results[event_type] = pd.DataFrame(type_results)
        
        return results
    
    def correlate_goals_with_loops(self):
        """Specialized analysis for goals"""
        goal_events = self.events_df[self.events_df['type'] == 'Goal']
        
        if len(goal_events) == 0:
            return None
        
        results = self.analyze_around_events(['Goal'], window_frames=30)
        return results.get('Goal', pd.DataFrame())
```

### 2.3 Complete Integration Example

```python
from analyze_h1_event_correlation import H1EventCorrelationAnalyzer
from pathlib import Path
import pandas as pd

# Load loop data
loops_analyzer = H1EventCorrelationAnalyzer()
loops_df = loops_analyzer.df

# Load StatsBomb events
event_loader = StatsBombEventLoader(data_dir='open-data/data')
match_id = "3788741"  # Your match ID

events = event_loader.load_match_events(match_id)
important_events = event_loader.extract_important_events(events)
events_with_frames = event_loader.convert_to_frame_indices(important_events)

# Correlate
correlator = H1StatsBombCorrelation(loops_df, events_with_frames)

# Analyze around goals
goal_analysis = correlator.correlate_goals_with_loops()

# Analyze around all important events
all_analysis = correlator.analyze_around_events(
    event_types=['Goal', 'Shot', 'Pass', 'Tackle'],
    window_frames=25
)
```

---

## 3. Analysis Patterns

### 3.1 Goal Correlation

**Questions to Answer**:
1. Do loop patterns change before/after goals?
2. Are there early warning signals (persistence changes)?
3. Do different goal types (open play vs set piece) show different patterns?

**Implementation**:
```python
goal_analysis = correlator.correlate_goals_with_loops()

# Before/after comparison
for _, goal in goal_analysis.iterrows():
    print(f"Goal at frame {goal['event_frame']}:")
    print(f"  Before: {goal['before_mean_persistence']:.3f}")
    print(f"  After: {goal['after_mean_persistence']:.3f}")
    print(f"  Change: {goal['after_mean_persistence'] - goal['before_mean_persistence']:+.3f}")
```

### 3.2 Possession Change Correlation

**Identify Possession Changes**:
```python
# Possession changes (simplified - would need more logic)
possession_changes = events_df[
    events_df['type'].isin(['Ball Receipt', 'Interception', 'Tackle'])
].copy()

# Group consecutive events by possession number
# Mark transitions where possession number changes
```

### 3.3 Formation Change Detection

**From Lineup Data**:
```python
def detect_formation_changes(match_id, data_dir='open-data/data'):
    """Detect formation changes from lineup data"""
    lineups_file = Path(data_dir) / 'lineups' / f'{match_id}.json'
    
    with open(lineups_file, 'r') as f:
        lineups = json.load(f)
    
    # Analyze formation changes
    # Map to frame indices based on substitution times
    ...
```

---

## 4. Visualization Integration

### 4.1 Event Markers on Temporal Plots

```python
def plot_persistence_with_events(loops_df, events_df, scale='individual'):
    """Plot persistence over time with event markers"""
    scale_data = loops_df[loops_df['scale'] == scale]
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Plot persistence
    ax.scatter(scale_data['frame_idx'], scale_data['persistence'],
              alpha=0.6, s=30)
    
    # Mark events
    for event_type in ['Goal', 'Shot']:
        type_events = events_df[events_df['type'] == event_type]
        for _, event in type_events.iterrows():
            if pd.notna(event['frame_idx']):
                ax.axvline(event['frame_idx'], color='red' if event_type == 'Goal' else 'orange',
                          linestyle='--', alpha=0.7, label=event_type)
    
    ax.set_xlabel('Frame Index')
    ax.set_ylabel('Persistence')
    ax.set_title(f'{scale.capitalize()} Scale: Persistence with Events')
    ax.legend()
    plt.show()
```

---

## 5. Expected Results

### 5.1 Goal Analysis

**Expected Patterns**:
- **Before goals**: Possible persistence increases (formation buildup)
- **After goals**: Possible persistence decreases (formation breakdown/celebration)
- **Individual scale**: Subtle changes
- **Tactical scale**: More dramatic changes

### 5.2 Possession Changes

**Expected Patterns**:
- **Transition moments**: Large persistence changes
- **Tactical scale**: More sensitive to possession changes
- **Loop destruction/formation**: Correlation with turnovers

### 5.3 Shot Events

**Expected Patterns**:
- **Before shots**: Persistence changes (formation compression)
- **After shots**: Formation recovery patterns
- **Shot type correlation**: Different patterns for different shot types

---

## 6. Next Steps

1. **Implement Event Loader**: Create the StatsBombEventLoader class
2. **Run Correlation**: Analyze loops around real events
3. **Validate Patterns**: Compare with synthetic analysis results
4. **Build Models**: Predictive models for event anticipation
5. **Multi-Match**: Expand to multiple matches for robustness

---

## 7. Files to Create/Modify

1. **`statsbomb_event_loader.py`**: Event loading and processing
2. **`analyze_h1_event_correlation.py`**: Update to use real events
3. **`visualize_h1_with_events.py`**: Event marker visualizations

---

**Document Version**: 1.0  
**Date**: December 2024  
**Status**: Ready for Implementation

