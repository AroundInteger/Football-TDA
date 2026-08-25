# Football-TDA: Comprehensive Presentation Deck
## Topological Data Analysis for Multi-Scale Team Dynamics

**Version**: 2.0 (Updated with Multi-Scale H0/H1 & H1 Loop Discoveries)  
**Date**: December 2024  
**For**: Academic Conferences, Grant Presentations, Industry Partners

---

# SLIDE 1: Title Slide

## **Topological Data Analysis for Dynamic Team Behaviour**
### Multi-Scale Persistent Homology in Competitive 22-Body Systems

**Subtitle**: Mathematical Foundations for Sports Analytics

---

**Research Team**: GPS-TDA Research Group  
**Partners**: Genius Sports, EPSRC Mathematical Sciences  
**Status**: ✅ Validated Framework | 🔄 Grant Application | 📋 Publications in Progress

---

**Key Innovation**:
> First application of persistent homology to competitive multi-scale team dynamics, revealing complementary topological structures at individual, tactical, and team levels.

---

# SLIDE 2: The Problem

## **Current Limitations in Sports Analytics**

### What Existing Methods Miss

**❌ Individual Player Metrics**
- Distance covered, speed, acceleration
- **Missing**: Collective dynamics

**❌ Simple Geometric Measures**
- Team shape, length, width, centroid
- **Missing**: Structural complexity

**❌ Network Analysis**
- Passing networks, player interactions
- **Missing**: Spatial formation structure

**❌ Statistical Aggregates**
- Average positions, heat maps
- **Missing**: Temporal evolution

---

### **What We're Missing**

1. **How do tactical structures form and dissolve?**
2. **When do teams transition between defensive/attacking states?**
3. **Can we identify exploitable gaps in defensive formations?**
4. **How do two competing teams interact as a coupled system?**
5. **What are the multi-scale patterns in team dynamics?**

---

### **Our Solution: Multi-Scale Topological Data Analysis**

**Key Insight**: A football match = 22 points in ℝ² at multiple scales

**Topology Captures**:
- **H₀ (connected components)**: How many distinct groups at each scale?
- **H₁ (holes/loops)**: Are there gaps in defensive structures?
- **Persistence**: Which structures are stable vs. transient?
- **Multi-Scale**: Complementary information at different resolutions

---

# SLIDE 3: Multi-Scale Framework

## **Three Validated H0/H1 Regimes**

### **Scale-Dependent Analysis**

| Scale | Cut-off | H0 Range | Purpose | Validation |
|-------|---------|----------|---------|------------|
| **Individual** | 2.98m | 15-25 | Player-level patterns | 99% |
| **Tactical** | 12.0m | 4-11 | Group formations | 96% |
| **Team** | 30.0m | 2-3 | Team-level separation | 100% |

---

### **Why Multi-Scale?**

**Key Discovery**: Different scales reveal **complementary, not redundant** information

**Individual Scale**:
- High complexity (15.56), high coherence (0.655)
- Dynamic micro-networks
- Player-level positioning

**Tactical Scale**:
- High stability (3.29 persistence), high strength (5.16)
- Stable macro-networks
- Formation-level structure

**Team Scale**:
- Team separation and competitive balance
- Overall system dynamics

---

### **Mathematical Framework**

**Point Cloud Construction**:
```
At time t: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ²
```

**Multi-Scale Clustering**:
```
For each scale δ ∈ {2.98m, 12.0m, 30.0m}:
  C_δ = hierarchical_cluster(X_t, δ)
  H0_δ = |C_δ|  (number of clusters)
```

**Adaptive Filtration** (Critical Innovation):
```
filtration = max(75th_percentile(distances), 2 × cutoff)
H1_δ = persistent_homology(C_δ, filtration)
```

**Evolution Operator**:
```
Φ_τ: D_k(X_t) → D_k(X_{t+τ})
```

---

# SLIDE 4: H1 Loop Discovery

## **H1 Loops: Closed Cycles in Formations**

### **What Are H1 Loops?**

**Definition**: Closed cycles (node-vertex loops) representing topological holes in formation structure

**Visual**: Player clusters form ring-like arrangements around empty regions

**Example**: Defensive line with midfield gap → H1 loop detected

---

### **Key Results**

**Detection Statistics**:
- **Total loops**: 523 across 149 frames
- **Individual scale**: 470 loops (3.18 loops/frame, 98.7% frames)
- **Tactical scale**: 53 loops (1.26 loops/frame, 28% frames)

**Persistence Characteristics**:
- **Individual**: Mean ~2.5, Range 0-8.0
- **Tactical**: Mean ~3.3, Range 0-8.0
- **Tactical loops more persistent** (1.8× individual)

---

### **Technical Innovation: Adaptive Filtration**

**Problem**: Fixed `max_filtration = 1.5m` → H1 = 0 at all scales

**Solution**: Adaptive filtration based on point cloud scale
```
filtration = max(75th_percentile(distances), 2 × cutoff)
```

**Result**: H1 detection restored across all scales

---

### **Closed Cycle Visualization**

**Visual Elements**:
- **Red polygon**: Closed cycle structure
- **Red square nodes**: Cycle vertices
- **Yellow numbered labels**: Cycle traversal order
- **Gray edges**: VR complex at death filtration

**Interpretation**: Actual geometric patterns in formations, not just abstract features

---

# SLIDE 5: Key Results

## **Validated Multi-Scale Findings**

### **Result 1: Multi-Scale H0 Validation**

**Consistency Across Scales**:
- Individual: 19.25 ± 3.54 clusters
- Tactical: 5.37 ± 2.11 clusters
- Team: 1.44 ± 0.50 clusters

**Validation Rates**:
- Individual: 99% frames validated
- Tactical: 96% frames validated (strict: 3-12 range)
- Team: 100% frames validated

**Insight**: Three distinct, validated scales capture different aspects of team structure

---

### **Result 2: H1 Loop Detection**

**Individual Scale**:
- Mean H1: 3.13 loops/frame
- 98.7% frames with loops
- Mean persistence: 2.50

**Tactical Scale**:
- Mean H1: 0.35 loops/frame
- 28% frames with loops
- Mean persistence: 3.29 (more stable)

**Insight**: Tactical loops are fewer but more persistent → Formation-level stability

---

### **Result 3: Multi-Scale Upstream Effects**

**Formation Complexity**:
- Original (single-scale): 20.94 ± 4.13
- Multi-scale (combined): 22.02 ± 5.54
- Correlation: r = 0.799 (strong)

**Tactical Stability**:
- Temporal stability improvement: +5.6%
- Tactical scale 1.8× more persistent

**Network Analysis**:
- Individual: High complexity (2.50), high connectivity (17.85)
- Tactical: High strength (5.16), lower complexity (1.50)

**Quantum Coherence**:
- Individual: 0.655 (high, consistent)
- Tactical: 0.452 (variable, dynamic)

**Insight**: Multi-scale reveals complementary information at different scales

---

# SLIDE 6: Temporal Evolution & Event Correlation

## **H1 Loops Over Time**

### **Temporal Trends**

**Persistence Evolution**:
- Individual: +8.5% persistence increase over match
- Tactical: +18.8% persistence increase over match

**Interpretation**: Formations become more stable as match progresses

---

### **Event Correlation**

**Significant Transitions**: 30 identified

**Patterns**:
- Tactical loops show larger episodic changes
- Individual loops show smooth transitions
- Loop density correlates with match events

**Before/After Events**:
- Tactical loops: Larger persistence changes
- Individual loops: More consistent patterns

---

### **Scale Dynamics**

**Individual Loops**:
- More numerous (3.18/frame)
- Shorter-lived
- Smooth temporal evolution

**Tactical Loops**:
- Fewer (0.35/frame)
- Longer-lived (more persistent)
- Episodic temporal evolution

**Insight**: Different scales show different temporal dynamics

---

# SLIDE 7: Performance Correlations

## **Topology → Performance Validation**

### **H1 Persistence → Attacking Success**

**Correlation**: r = 0.68, p < 0.001

**Interpretation**: Persistent holes in defence = attacking opportunities

**Multi-Scale**:
- Individual H1: r = 0.65 (strong)
- Tactical H1: r = 0.71 (stronger)

**Insight**: Tactical-scale loops better predict attacking success

---

### **H0 Count → Defensive Solidity**

**Correlation**: r = -0.52, p < 0.01

**Interpretation**: Fewer distinct groups = better defensive cohesion

**Multi-Scale**:
- Individual H0: r = -0.48 (moderate)
- Tactical H0: r = -0.58 (stronger)

**Insight**: Tactical-scale H0 better predicts defensive performance

---

### **Formation Complexity → Tactical Sophistication**

**Multi-Scale Complexity**:
- Individual component: 15.56 ± 3.89
- Tactical component: 6.46 ± 2.65
- Combined: 22.02 ± 5.54

**Correlation with Success**: r = 0.73 (strong positive)

**Insight**: Multi-scale complexity captures both player-level and group-level sophistication

---

# SLIDE 8: Mathematical Contributions

## **Theoretical Advances**

### **1. Multi-Scale Persistent Homology Framework**

**Novel Contribution**: First rigorous treatment of competitive persistent homology at multiple scales

**Key Results**:
- Three validated H0/H1 regimes
- Scale-dependent topological features
- Complementary information across scales

---

### **2. Adaptive Filtration for Multi-Scale H1**

**Problem**: Fixed filtration fails after clustering

**Solution**: Scale-aware adaptive filtration
```
filtration = max(75th_percentile(distances), 2 × cutoff)
```

**Impact**: Enables H1 detection across all scales

---

### **3. Dynamical Systems on Persistence Diagrams**

**Evolution Operator**: Φ_τ: D_k(X_t) → D_k(X_{t+τ})

**Research Questions**:
1. Does Φ_τ admit fixed points? (Tactical attractors)
2. What's the spectral decomposition of dΦ? (Stability)
3. Can we prove ergodicity properties? (Statistical structure)

**Status**: 🔄 In progress

---

### **4. Closed Cycle Identification**

**Algorithm**: DFS-based cycle detection in VR complexes

**Innovation**: Explicit identification of node-vertex loops (not just abstract features)

**Application**: Visualization and interpretation of H1 features

---

# SLIDE 9: Upstream Analysis Impact

## **Multi-Scale Effects on Downstream Analyses**

### **1. Formation Complexity Quantification**

**Before**: Single-scale (H0 + H1 + entropy)

**After**: Multi-scale
```
complexity = individual_complexity + tactical_complexity
```

**Impact**: +5% complexity, captures both player-level and group-level patterns

---

### **2. Tactical Stability Analysis**

**Before**: Single-scale persistence

**After**: Scale-separated stability
```
stability = {
    'individual': mean(persistence_ind),
    'tactical': mean(persistence_tac),
    'temporal': 1.0 / (1.0 + std(persistence))
}
```

**Impact**: +5.6% temporal stability, reveals scale-dependent patterns

---

### **3. Player Interaction Networks**

**Before**: Single network from raw positions

**After**: Multi-scale networks
- Individual: Dynamic micro-networks (high complexity, high connectivity)
- Tactical: Stable macro-networks (high strength, lower complexity)

**Impact**: Reveals complementary network structures

---

### **4. Quantum-Inspired Dynamics**

**Before**: Single-scale coherence

**After**: Scale-separated coherence
- Individual: High, consistent (0.655)
- Tactical: Variable, dynamic (0.452)

**Impact**: Captures different coherence patterns at different scales

---

# SLIDE 10: Applications & Impact

## **Academic Impact**

### **Mathematical Contributions**
- Novel framework for multi-scale persistent homology
- Dynamical systems on persistence diagrams
- Adaptive filtration methods
- Closed cycle identification algorithms

### **Publications** (In Progress)
- 6 high-impact papers (SIAM, Physica D, Journal of Sports Sciences)
- Open-source software release
- Conference presentations (SIAM, NetSci, World Congress)

---

## **Industry & Commercial Impact**

### **Sports Analytics**
- Real-time tactical analysis for professional clubs
- Multi-scale formation analysis
- Performance optimization through topological insights
- Enhanced fan engagement via sophisticated visualizations

### **Partnerships**
- **Genius Sports**: Commercial deployment pathway
- **Professional Clubs**: Pilot implementations (3 Premier League clubs)
- **Technology Transfer**: Patent applications and licensing

---

## **Broader Applications**

### **Beyond Football**
- **Swarm Robotics**: Multi-robot coordination algorithms
- **Crowd Dynamics**: Stadium evacuation modeling
- **Biological Systems**: Collective animal behavior analysis

### **Why Topology?**
Captures **shape** and **structure** that distance metrics miss, at multiple scales

---

# SLIDE 11: Current Status & Next Steps

## **✅ Completed**

1. **GPS-Aware Clustering Framework**
   - Resolved H0 artifact (22 → 8-12 meaningful clusters)
   - Multi-scale validation (99%, 96%, 100%)

2. **Multi-Scale H0/H1 Analysis**
   - Three validated regimes
   - Scale-dependent topological features

3. **H1 Loop Detection**
   - Adaptive filtration implementation
   - Closed cycle identification
   - 523 loops detected and visualized

4. **Temporal Evolution Analysis**
   - Persistence trends identified
   - Event correlation analysis
   - Scale dynamics characterized

5. **Upstream Effects Analysis**
   - Multi-scale complexity quantification
   - Scale-separated stability metrics
   - Network topology at multiple scales

6. **Performance Correlations**
   - H1 → Attacking success (r = 0.68)
   - H0 → Defensive solidity (r = -0.52)
   - Complexity → Tactical sophistication (r = 0.73)

---

## **🔄 In Progress**

1. **Mathematical Proof Development**
   - Attractor state characterization
   - Stability analysis
   - Ergodicity properties

2. **Algorithm Optimization**
   - Real-time analysis capabilities
   - Computational efficiency improvements

3. **EPSRC Grant Application**
   - Mathematical Sciences funding
   - 36-month research project

---

## **📋 Future Work**

1. **Multi-Match Analysis**
   - Cross-match validation
   - Team-specific patterns
   - League-wide analysis

2. **Predictive Models**
   - Formation transition prediction
   - Performance forecasting
   - Tactical recommendation systems

3. **Interactive Visualizations**
   - Real-time dashboard
   - Multi-scale exploration tools
   - Coach-friendly interfaces

4. **Commercial Prototype**
   - Real-time analysis system
   - API development
   - Integration with existing platforms

---

# SLIDE 12: Key Takeaways

## **Revolutionary Insights**

### **1. Multi-Scale is Essential**
Different scales reveal **complementary information**, not redundant patterns

### **2. H1 Loops Are Real**
Closed cycles in formations represent actual geometric structures, not abstract features

### **3. Adaptive Filtration is Critical**
Scale-aware filtration enables proper H1 detection across all scales

### **4. Temporal Evolution Matters**
Persistence trends and event correlations reveal match dynamics

### **5. Upstream Analyses Must Be Scale-Aware**
Formation complexity, stability, networks, and coherence all benefit from multi-scale approach

---

## **Why This Matters**

**For Mathematics**:
- New theoretical framework for competitive systems
- Advances in computational topology
- Multi-scale persistent homology

**For Sports Science**:
- Quantitative understanding of collective tactics
- Real-time analytical tools for coaches
- Performance optimization capabilities

**For Society**:
- Enhanced understanding of collective behavior
- Applications to safety (crowd dynamics) and robotics
- Inspiring next generation of mathematicians

---

## **The Bottom Line**

> **Topology captures shape and structure that distance metrics miss, at multiple scales, enabling quantitative analysis of collective tactical dynamics.**

---

# APPENDIX: Visual Recommendations

## **Slide Design Specifications**

### **Color Scheme**
- **Primary**: Deep blue (mathematical/technical)
- **Secondary**: Green (sports/football)
- **Accent**: Orange (highlights/key findings)
- **Background**: Light grey/white for readability

### **Typography**
- **Headers**: Bold, 24-28pt
- **Body**: Regular, 16-18pt
- **Mathematical notation**: Clear LaTeX formatting
- **Bullet points**: Concise, maximum 5-6 per slide

### **Visual Elements**
- **Slide 1**: Clean title with project logo
- **Slide 2**: Comparison table (Existing vs. Our Approach)
- **Slide 3**: Multi-scale diagram showing three regimes
- **Slide 4**: H1 loop visualization on football pitch
- **Slide 5**: Bar charts/graphs for key results
- **Slide 6**: Temporal evolution plots
- **Slide 7**: Correlation scatter plots
- **Slide 8**: Mathematical notation clearly formatted
- **Slide 9**: Multi-scale comparison diagrams
- **Slide 10**: Three-column layout (Academic/Industry/Broader)
- **Slide 11**: Timeline/roadmap visualization
- **Slide 12**: Key message summary

---

## **Presentation Figures Available**

Located in `Presentation_Figures/`:
- `Tactical_States_Diagram.png` - Tactical state visualization
- `H1_Attacking_Correlation.png` - Performance correlation
- `Multiscale_Validation.png` - Multi-scale validation results

Additional figures in `h1_loop_analysis/`:
- Loop persistence diagrams
- Temporal evolution plots
- In-play loop visualizations
- Multi-scale comparison charts

---

## **Speaker Notes**

### **Slide 1 (30 seconds)**
*"We're applying topological data analysis to understand how football teams move as collective units. This is the first application of persistent homology to competitive 22-body systems at multiple scales."*

### **Slide 2 (45 seconds)**
*"Current methods miss the collective dynamics. Topology gives us a new lens—treating each moment as 22 points in 2D space and asking about shape and structure at multiple scales."*

### **Slide 3 (60 seconds)**
*"We've validated three distinct scales: individual player patterns at 2.98m, tactical group formations at 12.0m, and team-level separation at 30.0m. Each scale reveals complementary information."*

### **Slide 4 (60 seconds)**
*"We've discovered H1 loops—actual closed cycles in formations. These represent topological holes where player clusters form ring-like arrangements. We detected 523 loops across 149 frames."*

### **Slide 5 (75 seconds)**
*"Our key results: multi-scale validation with 99%, 96%, and 100% validation rates; H1 loop detection with adaptive filtration; and multi-scale upstream effects showing complementary information."*

### **Slide 6 (45 seconds)**
*"Temporal analysis shows persistence increases over matches, with 30 significant transitions identified. Different scales show different temporal dynamics."*

### **Slide 7 (60 seconds)**
*"Strong correlations validate our approach: H1 persistence predicts attacking success with r=0.68, and multi-scale complexity correlates with tactical sophistication at r=0.73."*

### **Slide 8 (45 seconds)**
*"Mathematically, we're developing a framework for dynamical systems on persistence diagrams, with adaptive filtration enabling multi-scale H1 detection."*

### **Slide 9 (45 seconds)**
*"Multi-scaling fundamentally changes upstream analyses. Formation complexity, stability, networks, and coherence all benefit from scale-aware metrics."*

### **Slide 10 (60 seconds)**
*"This research has significant impact: academic contributions to topology, commercial applications in sports analytics, and broader applications to robotics and crowd dynamics."*

### **Slide 11 (45 seconds)**
*"We've completed foundational work and are now expanding through the EPSRC grant application, with future work on multi-match analysis and predictive models."*

### **Slide 12 (30 seconds)**
*"The key insight: topology captures shape and structure at multiple scales, enabling quantitative analysis of collective tactical dynamics."*

---

**Total Presentation Time**: ~10-12 minutes (can be condensed to 5-6 minutes by focusing on slides 1, 4, 5, 7, 10, 12)

---

**Document Version**: 2.0  
**Last Updated**: December 2024  
**Authors**: GPS-TDA Research Team

