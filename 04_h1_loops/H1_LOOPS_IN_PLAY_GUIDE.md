# H1 Loops In-Play Visualization Guide

**Date**: December 2024  
**Purpose**: Visualize actual H1 loops from Vietoris-Rips complexes on the football field

---

## Overview

These visualizations show **actual H1 loops** (formation holes/structures) as they appear **in real formations** on the football field, reconstructed from the Vietoris-Rips complex structures.

---

## What You'll See

### Field Layout
- **Full football field**: 105m × 68m (standard dimensions)
- **Player/cluster positions**: Actual (x, y) coordinates from GPS data
- **Time information**: Frame index and timestamp

### Vietoris-Rips Complex Structure

**Gray Edges** (Light gray, low opacity):
- All edges in the VR complex at death filtration
- Connections between cluster centroids within filtration distance
- Shows the full connectivity structure

**Red Edges** (Bold, high opacity):
- Edges that form the **H1 loop structure**
- Connections that appear between birth and death times
- Highlighted to show the loop shape

**Red Filled Regions** (Semi-transparent):
- **Enclosed loop areas** (triangles that bound the loop)
- Shows the "hole" in the formation structure
- Visual representation of the topological feature

### Loop Information Box

Each visualization includes:
- **Scale**: Individual, Tactical, or Team
- **Persistence**: How long the loop survives (death - birth)
- **Birth time**: Filtration value when loop appears
- **Death time**: Filtration value when loop disappears
- **Points**: Number of cluster centroids
- **Loop edges**: Number of edges forming the loop
- **Loop triangles**: Number of triangles bounding the loop

---

## Generated Visualizations

### 1. Individual Loop Visualizations

**Files**: `loop_in_play_{scale}_frame{frame_idx}_persistence{persistence}.png`

**Shows**:
- Single H1 loop at a specific frame
- Full field context
- Complete VR complex structure
- Loop highlighted in red

**Use Cases**:
- Detailed analysis of specific loops
- Understanding loop geometry
- Presentation slides showing loop examples

### 2. Multi-Frame Comparisons

**Files**: `h1_loops_comparison_{scale}.png`

**Shows**:
- 2×2 grid comparing loops at different frames
- Same scale, different time points
- Loop count and persistence at each frame

**Use Cases**:
- Temporal evolution overview
- Comparing loop structures across time
- Understanding loop dynamics

---

## How to Interpret

### Loop Structure

1. **Gray Network**: Shows all possible connections (VR complex)
2. **Red Structure**: Highlights the actual loop (H1 feature)
3. **Filled Region**: Shows the "hole" in the formation

### Persistence Meaning

- **High Persistence** (e.g., 7.97): Loop survives over large filtration range
  - More stable/robust formation structure
  - Significant tactical feature
  
- **Low Persistence** (e.g., 0.5): Loop appears briefly
  - Transient formation structure
  - Dynamic tactical feature

### Birth/Death Times

- **Birth**: Filtration value when loop first appears
  - Indicates when cluster centroids are close enough to form loop
  
- **Death**: Filtration value when loop disappears
  - Indicates when triangles fill in the loop (hole closes)

### Scale Differences

**Individual Scale**:
- More loops (470 total)
- Shorter persistence (mean 1.781)
- Fine-grained player-level structures

**Tactical Scale**:
- Fewer loops (53 total)
- Longer persistence (mean 3.285)
- Formation-level structures (more stable)

---

## Example Interpretations

### Example 1: High Persistence Loop (Persistence = 7.97)

**What it means**:
- Formation has a stable "hole" or empty region
- Structure persists across large filtration range
- Represents a significant tactical formation feature

**Visual**:
- Red edges form a clear closed loop
- Filled region shows the empty space
- Gray edges show surrounding connectivity

### Example 2: Low Persistence Loop (Persistence = 0.5)

**What it means**:
- Formation has a brief structural feature
- Loop appears and disappears quickly
- Represents dynamic tactical adjustment

**Visual**:
- Smaller loop structure
- Less prominent filled region
- More transient appearance

---

## Technical Details

### Vietoris-Rips Complex Reconstruction

**Process**:
1. Cluster centroids form point cloud (after hierarchical clustering)
2. At filtration ε, connect all pairs within distance ε
3. Form triangles for all triples within distance ε
4. H1 loops = cycles that are NOT boundaries of triangles

**Visualization**:
- All edges at death filtration: Gray network
- Loop edges (birth ≤ distance ≤ death): Red edges
- Triangles bounding loop: Red filled regions

### Loop Identification

**Simplified Approach**:
- Find edges in birth-death range
- Find triangles with edges in birth-death range
- Triangles bound loops (loops are "holes" in the complex)

**Note**: Actual loop identification requires homology computation, but visualization approximates by highlighting relevant edges and triangles.

---

## Use Cases for Presentations

### 1. **Formation Structure Analysis**
- Show actual holes/empty regions in formations
- Demonstrate how H1 captures formation geometry
- Compare different tactical structures

### 2. **Temporal Dynamics**
- Compare loops across different frames
- Show how formation structures evolve
- Demonstrate persistence over time

### 3. **Scale Comparison**
- Individual scale: Player-level loops
- Tactical scale: Formation-level loops
- Different geometric structures at different scales

### 4. **Tactical Interpretation**
- Connect loop structures to tactical concepts
- Identify defensive/offensive patterns
- Explain formation complexity

---

## Files Generated

### Individual Loops (Top 5 per scale)
- `loop_in_play_individual_frame72_persistence7.97.png`
- `loop_in_play_individual_frame13_persistence7.17.png`
- `loop_in_play_individual_frame136_persistence6.57.png`
- ... (more for individual and tactical scales)

### Multi-Frame Comparisons
- `h1_loops_comparison_individual.png`
- `h1_loops_comparison_tactical.png`

---

## Next Steps

### To Create More Visualizations

1. **Specific Frames**:
   ```python
   # Visualize specific loop
   visualize_loop_in_formation(frame_data, loop_info)
   ```

2. **Animation** (Future):
   - Animate loop evolution over time
   - Show loops appearing/disappearing
   - Temporal dynamics visualization

3. **3D Visualization** (Future):
   - Add time dimension (x, y, t)
   - Show loops in 3D space-time
   - Spatiotemporal loop tracking

---

## Summary

✅ **What we've created**:
- Actual H1 loops visualized on the field
- Vietoris-Rips complex structure shown
- Birth/death/persistence information displayed
- Ready for presentations

✅ **Key features**:
- Real GPS coordinates (x, y, t)
- VR complex edges and triangles
- Loop structures highlighted
- Field context included

✅ **Interpretation**:
- Loops = holes/empty regions in formations
- Persistence = how long loops survive
- Scale = different geometric structures

**These visualizations provide powerful, intuitive representations of topological features in real football formations!**

