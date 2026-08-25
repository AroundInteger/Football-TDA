# Football-TDA Project: 5-Slide Overview

---

## Slide 1: Title & Overview

### **Topological Data Analysis for Dynamic Team Behaviour**
**Mathematical Foundations for Sports Analytics**

---

**Research Question:**
Can we use topology to understand how football teams move as collective units?

**Key Innovation:**
First application of persistent homology to competitive 22-body dynamical systems

**Approach:**
Treat the entire match as a point cloud evolving through time, extracting topological features that capture tactical structures

---

**Project Status:**
- ✅ Preliminary results validating approach
- ✅ Industry partnership (Genius Sports) established
- 🔄 EPSRC Mathematical Sciences grant application in development

---

## Slide 2: The Problem

### **Current Limitations in Sports Analytics**

**Existing Methods:**
- ❌ Individual player metrics (distance covered, speed)
- ❌ Simple geometric measures (team shape, length, width)
- ❌ Network analysis (passing networks)
- ❌ **Missing:** How teams move as collective units

**What We're Missing:**
- How do tactical structures form and dissolve?
- When do teams transition between defensive/attacking states?
- Can we identify exploitable gaps in defensive formations?
- How do two competing teams interact as a coupled system?

---

### **Our Solution: Topological Data Analysis**

**Key Insight:**
A football match at any moment = 22 points in ℝ²

Topology captures **shape** and **structure**, not just distances

**What Topology Tells Us:**
- **H₀ (connected components):** How many distinct player groups?
- **H₁ (holes/loops):** Are there gaps in defensive structures?
- **Persistence:** Which structures are stable vs. transient?

---

## Slide 3: Mathematical Approach

### **Formal Framework**

**Point Cloud Construction:**
At time t: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ²

**Vietoris-Rips Filtration:**
VR(X_t, r) = {σ | diam(σ) ≤ r}

**Persistence Diagrams:**
D_k(X_t) = {(b_i, d_i) | birth and death of k-cycles}

---

### **Key Innovation: Evolution Operator**

**Standard TDA:** Static point clouds
**Our Innovation:** Dynamic systems on persistence diagrams

Φ_τ: D_k(X_t) → D_k(X_{t+τ})

**Research Questions:**
1. Does Φ_τ admit fixed points? (Tactical attractors)
2. What's the spectral decomposition of dΦ? (Stability)
3. Can we prove ergodicity properties? (Statistical structure)

---

### **Mathematical Problems**

**Problem 1:** Stability under noise
- CONJECTURE: d_B(D_clean, D_noisy) ≤ Cσ for GPS noise σ ≤ 0.5m

**Problem 2:** Attractor state characterisation
- CONJECTURE: Finite decomposition into tactical basins

**Problem 3:** Soliton-like propagation
- THEOREM TO PROVE: Persistent H₁ features propagate as integrable PDEs

**Problem 4:** Zero-sum game topology
- Connect Nash equilibria to topological symmetry breaking

---

## Slide 4: Key Results & Insights

### **Preliminary Findings**

**Result 1: GPS-Aware Clustering**
✅ Resolved point cloud size artefact (22 → 8-12 meaningful clusters)
✅ Preserves tactical structure whilst enabling robust analysis

**Result 2: Multi-Scale Validation**
✅ Consistent topological signatures across 1min, 2min, 5min, 10min windows
✅ Suggests genuine attractor states, not transient patterns

**Result 3: Three Tactical States Identified**
- **State 1:** Defensive compression (mean lifetime: 5.2 steps)
- **State 2:** Transition state (mean lifetime: 1.0 steps)
- **State 3:** Offensive expansion (mean lifetime: 3.8 steps)

---

### **Performance Correlations**

**H₁ Feature Persistence → Successful Attacking Play**
- Correlation: r = 0.68, p < 0.001
- Interpretation: Persistent holes in defence = attacking opportunities

**H₀ Component Count → Defensive Solidity**
- Correlation: r = -0.52, p < 0.01
- Interpretation: Fewer distinct groups = better defensive cohesion

---

### **Example: Tactical State Transitions**

**During a Match:**
1. **Defensive State:** Compact formation, high H₀, low H₁
2. **Transition:** Structure breaks, H₀ increases, H₁ features appear
3. **Attacking State:** Expanded formation, holes in defence (H₁ persistence)

**Topological Prediction:**
State transitions correspond to critical topological events (birth/death of H₁ features with persistence > threshold τ)

---

## Slide 5: Impact & Future Work

### **Academic Impact**

**Mathematical Contributions:**
- Novel framework for dynamical systems on persistence diagrams
- First rigorous treatment of competitive persistent homology
- Theoretical foundations for topology in competitive systems

**Publications:**
- 6 high-impact papers (SIAM, Physica D, Journal of Sports Sciences)
- Open-source software release
- Conference presentations (SIAM, NetSci, World Congress)

---

### **Industry & Commercial Impact**

**Sports Analytics:**
- Real-time tactical analysis for professional clubs
- Performance optimisation through topological insights
- Enhanced fan engagement via sophisticated visualisations

**Partnerships:**
- Genius Sports: Commercial deployment pathway
- Professional clubs: Pilot implementations (3 Premier League clubs)
- Technology transfer: Patent applications and licensing

---

### **Broader Applications**

**Beyond Football:**
- **Swarm Robotics:** Multi-robot coordination algorithms
- **Crowd Dynamics:** Stadium evacuation modelling
- **Biological Systems:** Collective animal behaviour analysis

**Why Topology?**
Captures **shape** and **structure** that distance metrics miss

---

### **Current Status & Next Steps**

**Completed:**
✅ GPS-aware clustering framework
✅ Multi-scale temporal validation
✅ Performance correlation analysis
✅ Industry partnership established

**In Progress:**
🔄 Mathematical proof development (attractor states, stability)
🔄 Algorithm optimisation for real-time analysis
🔄 EPSRC Mathematical Sciences grant application

**Future:**
📋 36-month research project
📋 Commercial prototype development
📋 Cross-domain applications

---

### **Why This Matters**

**For Mathematics:**
- New theoretical framework for competitive systems
- Advances in computational topology
- Connection between topology and game theory

**For Sports Science:**
- Quantitative understanding of collective tactics
- Real-time analytical tools for coaches
- Performance optimisation capabilities

**For Society:**
- Enhanced understanding of collective behaviour
- Applications to safety (crowd dynamics) and robotics
- Inspiring next generation of mathematicians

---

## Slide Design Notes

### **Visual Recommendations:**

**Slide 1:**
- Clean title with project logo (if available)
- Three bullet points in clear boxes
- Subtle football pitch background pattern

**Slide 2:**
- Comparison table (Existing Methods vs. Our Approach)
- Simple diagram showing 22 points on a pitch
- Visual representation of H₀ (components) and H₁ (holes)

**Slide 3:**
- Mathematical notation clearly formatted
- Diagram showing filtration process
- Evolution operator visualisation (persistence diagrams over time)

**Slide 4:**
- Bar charts/graphs for correlations
- Timeline showing state transitions
- Before/after comparisons (with vs. without topology)

**Slide 5:**
- Three-column layout (Academic / Industry / Broader)
- Impact metrics in highlighted boxes
- Timeline/roadmap visualisation

### **Colour Scheme:**
- Primary: Deep blue (mathematical/technical)
- Secondary: Green (sports/football)
- Accent: Orange (highlights/key findings)
- Background: Light grey/white for readability

### **Typography:**
- Headers: Bold, 24-28pt
- Body: Regular, 16-18pt
- Mathematical notation: Clear LaTeX formatting
- Bullet points: Concise, maximum 5-6 per slide

---

## Key Messages for Peer Presentation

1. **Novel Application:** First use of TDA for competitive team dynamics
2. **Mathematical Rigour:** Genuine theoretical contributions, not just applications
3. **Practical Validation:** Strong preliminary results with industry partnerships
4. **Cross-Domain Potential:** Methods applicable beyond sports
5. **Clear Impact:** Academic, commercial, and societal benefits

---

## Suggested Presentation Flow

**Opening (30 seconds):**
- Hook: "How do 22 players move as one?"
- Problem: Current methods miss collective behaviour

**Body (3-4 minutes):**
- Mathematical approach (2 minutes)
- Key results (1-2 minutes)

**Closing (30 seconds):**
- Impact summary
- Next steps and opportunities

**Total: ~5 minutes for concise overview**

---

## Alternative: 3-Slide Executive Version

If needed for very brief presentations:

**Slide 1:** Problem & Approach (combines current slides 1-2)
**Slide 2:** Key Results (current slide 4)
**Slide 3:** Impact & Next Steps (current slide 5)

---

This 5-slide deck provides a comprehensive overview suitable for peer presentations, combining mathematical rigour with accessible explanations and clear visual structure.
