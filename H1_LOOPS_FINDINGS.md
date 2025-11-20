# H1 Loops in Football Formations: Findings and Methodology

## Executive Summary

We have successfully identified and visualized **H1 homology loops** (topological holes) in football formations using persistent homology. These loops represent **closed cycles** in the formation structure - actual geometric patterns where player clusters form ring-like arrangements around empty regions on the field.

**Key Discovery**: H1 loops are **closed cycles** (node-vertex loops), not just collections of edges. They represent topological holes in the formation structure.

---

## 1. Methodology

### 1.1 Multi-Scale Analysis Framework

We use a **goal-dependent cut-off distance** approach for multi-scale analysis:

- **Individual Scale**: Cut-off = 2.98m (validates ~99% of frames)
  - Focus: Individual player patterns
  - H0 range: 15-25 clusters (one per player)
  
- **Tactical Scale**: Cut-off = 12.0m (validates ~96% of frames)
  - Focus: Tactical group formations
  - H0 range: 4-11 clusters (group-level)
  
- **Team Scale**: Cut-off = 30.0m (validates ~100% of frames)
  - Focus: Team-level separation
  - H0 range: 2-3 clusters (team-based)

### 1.2 Adaptive Filtration for H1 Detection

**Critical Innovation**: After clustering with larger cut-offs, the point cloud scale increases. We implemented **adaptive filtration** that:

1. Calculates point cloud distances after clustering
2. Uses 75th percentile as base filtration
3. Ensures minimum filtration: `max(5.0, cutoff_distance * 2.0)`
4. Enables H1 detection at all scales (not just individual)

**Previous Problem**: Fixed `max_filtration = 1.5m` was too small after tactical/team clustering, resulting in `H1 = 0` at all scales.

**Solution**: Adaptive filtration dynamically adjusts based on point cloud scale, enabling proper H1 detection across all scales.

### 1.3 Closed Cycle Identification

**H1 loops are closed cycles**: A path `v₀ → v₁ → ... → vₖ → v₀` where all edges have distances in the `[birth, death]` persistence interval.

**Algorithm**:
1. Build adjacency graph from edges in birth-death range
2. Use DFS to find cycles starting from each node
3. Validate cycles have ≥3 nodes and return to start
4. Score cycles by how well they represent the persistence interval
5. Select longest/most representative cycle as the loop

### 1.4 Visualization Framework

**Field Coordinate System**:
- GPS coordinates are **centered at (0, 0)** (field center at origin)
- Field visualization spans `[-52.5, 52.5] × [-34, 34]` meters
- Coordinates match SecondSpectrum/StatsBomb format

**Visual Elements**:
- **Gray edges**: All VR complex edges at death filtration
- **Red polygon**: Closed cycle structure (the actual H1 loop)
- **Red square nodes**: Cycle vertices
- **Yellow numbered labels**: Cycle traversal order (1→2→3→...→1)
- **Red filled triangles**: Regions that fill/close the loop (causing death)

---

## 2. Results

### 2.1 H1 Loop Statistics

**Data Coverage**:
- **Total loops detected**: 523
- **Frames analyzed**: 149 (full match)
- **Individual scale**: 470 loops across 148 frames (avg 3.18 loops/frame)
- **Tactical scale**: 53 loops across 42 frames (avg 1.26 loops/frame)

**Persistence Ranges**:
- **Individual**: 0.000 - 7.971 (mean ~2.5)
- **Tactical**: 0.194 - 9.392 (mean ~5.0)

**Key Insight**: Tactical loops have **higher persistence** on average, indicating more stable formation structures at group level.

### 2.2 Closed Cycle Structures

**Individual Scale Examples**:
- Frame 72: Persistence 7.97 - 5-node closed cycle
- Frame 13: Persistence 7.17 - 4-node closed cycle
- Frame 136: Persistence 6.57 - 6-node closed cycle

**Tactical Scale Examples**:
- Frame 73: Persistence 9.39 - 5-node closed cycle (highest persistence)
- Frame 116: Persistence 8.48 - 4-node closed cycle
- Frame 137: Persistence 7.92 - 5-node closed cycle

**Observation**: Tactical scale loops often have fewer nodes but higher persistence, indicating they represent **strategic formation gaps** (e.g., between defensive lines, midfield zones).

### 2.3 Scale Comparison

| Metric | Individual | Tactical |
|--------|-----------|----------|
| Avg loops/frame | 3.18 | 1.26 |
| Max persistence | 7.97 | 9.39 |
| Min persistence | 0.00 | 0.19 |
| Frames with loops | 148/149 | 42/149 |
| Typical cycle length | 4-6 nodes | 4-5 nodes |

**Interpretation**:
- **Individual scale**: Many transient loops (low persistence), representing dynamic player interactions
- **Tactical scale**: Fewer but more persistent loops, representing stable formation structures

---

## 3. Interpretations

### 3.1 What Do H1 Loops Represent?

**Formation Geometry**:
- **Empty regions** in the formation (holes)
- **Ring-like structures** formed by player clusters
- **Tactical gaps** between groups (defense-midfield, midfield-attack)

**Tactical Implications**:
- **Individual scale**: Player-level positioning creating small loops (e.g., triangular passing lanes)
- **Tactical scale**: Group-level structures (e.g., defensive lines creating gaps, midfield diamonds)

### 3.2 Persistence as Stability Metric

**High Persistence (7-9)**:
- **Stable formation structures**
- **Tactically significant gaps** (defensive lines, midfield zones)
- **Strategic positioning** that persists across multiple filtration levels

**Low Persistence (<2)**:
- **Transient formations**
- **Dynamic adjustments**
- **Short-lived tactical patterns**

### 3.3 Closed Cycle Structure

**Why Closed Cycles Matter**:
1. **Topological validity**: True H1 loops must be closed (cycle returning to start)
2. **Visual clarity**: Shows actual formation structure, not just edges
3. **Tactical interpretation**: Closed cycles represent actual "holes" in formation coverage

**Example**: A 5-node cycle `2→5→6→4→7→2` represents a pentagonal gap in the formation where players form a ring around an empty space.

---

## 4. Technical Innovations

### 4.1 Coordinate System Fix

**Problem**: GPS coordinates centered at (0,0), but field drawn from (0,0) corner.

**Solution**: Center field visualization at origin, span `[-52.5, 52.5] × [-34, 34]`.

### 4.2 Adaptive Filtration

**Problem**: Fixed filtration too small after clustering → H1 = 0.

**Solution**: Dynamic filtration based on point cloud scale:
```python
adaptive_filtration = max(
    np.percentile(point_distances, 75),
    max(5.0, cutoff_distance * 2.0)
)
```

### 4.3 Closed Cycle Detection

**Problem**: Previous visualization showed edges, not actual loops.

**Solution**: Graph-based cycle detection using DFS, ensuring closed paths.

---

## 5. Visualizations Generated

### 5.1 Individual Loop Visualizations

**Files**: `loop_in_play_individual_frame*.png`
- Top 5 most persistent loops per scale
- Shows closed cycle structure on field
- Includes persistence, birth/death times

### 5.2 Multi-Frame Comparisons

**Files**: `h1_loops_comparison_*.png`
- Sequence of frames showing loop evolution
- Temporal patterns in loop formation

### 5.3 Key Visual Elements

- **Field background**: Green field with center line, circles, penalty areas
- **Gray network**: VR complex edges (context)
- **Red polygon**: Closed cycle (H1 loop structure)
- **Red square nodes**: Cycle vertices
- **Numbered labels**: Cycle traversal path
- **Info box**: Loop metadata (persistence, birth, death, cycle path)

---

## 6. Future Directions

### 6.1 Temporal Evolution Analysis

- **Loop birth/death timelines**: When loops appear and disappear
- **Persistence trends**: How loop stability changes over time
- **Scale interactions**: How individual and tactical loops relate temporally

### 6.2 Event Correlation

- **Goals**: Do loops change before/after goals?
- **Possession changes**: Loop dynamics during transitions
- **Shots/passes**: Correlation with attacking events
- **Formation changes**: Loop response to tactical adjustments

### 6.3 Predictive Applications

- **Formation prediction**: Can loop patterns predict tactical changes?
- **Event anticipation**: Early warning from loop dynamics?
- **Performance metrics**: Loop persistence as formation quality metric

---

## 7. Files and Resources

### 7.1 Data Files

- `h1_loop_analysis/h1_loops_full_data.json`: Complete loop data (523 loops)
- `h1_loop_analysis/h1_loops_data.json`: Summary statistics

### 7.2 Visualization Files

- `h1_loop_analysis/in_play_visualizations/loop_in_play_*.png`: Individual loops
- `h1_loop_analysis/in_play_visualizations/h1_loops_comparison_*.png`: Multi-frame

### 7.3 Analysis Scripts

- `analyze_h1_loops.py`: Extract loop data from ripser output
- `visualize_h1_loops.py`: Persistence diagrams and lifetime timelines
- `visualize_h1_loops_in_play.py`: Field visualizations with closed cycles

---

## 8. Conclusions

**Key Achievements**:
1. ✅ Successfully detected H1 loops at multiple scales (individual, tactical)
2. ✅ Identified closed cycle structures (node-vertex loops)
3. ✅ Fixed coordinate system for accurate field visualization
4. ✅ Implemented adaptive filtration for multi-scale H1 detection
5. ✅ Created presentation-ready visualizations

**Scientific Contribution**:
- First application of persistent homology H1 to football formations with closed cycle identification
- Multi-scale framework revealing different loop structures at player vs. group level
- Temporal analysis potential for understanding formation dynamics

**Next Steps**:
- Temporal evolution analysis
- Event correlation studies
- Predictive modeling applications

---

**Document Version**: 1.0  
**Date**: December 2024  
**Authors**: GPS-TDA Research Team

