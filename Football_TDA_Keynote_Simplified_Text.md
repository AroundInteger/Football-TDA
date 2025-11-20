# Football-TDA: Simplified Text Template for Keynote
## Copy-Paste Ready Content

---

# SLIDE 1: TITLE & OVERVIEW

## Title
**Topological Data Analysis for Dynamic Team Behaviour**
Mathematical Foundations for Sports Analytics

## Main Content (3 bullet points)

• **Research Question:** Can we use topology to understand how football teams move as collective units?

• **Key Innovation:** First application of persistent homology to competitive 22-body dynamical systems

• **Approach:** Treat the entire match as a point cloud evolving through time, extracting topological features that capture tactical structures

## Status Indicators

✅ Preliminary results validating approach
✅ Industry partnership (Genius Sports) established
🔄 EPSRC Mathematical Sciences grant application in development

---

# SLIDE 2: THE PROBLEM

## Title
**Current Limitations in Sports Analytics**

## Left Column: Existing Methods

**What We Have Now:**

❌ Individual player metrics (distance covered, speed)
❌ Simple geometric measures (team shape, length, width)
❌ Network analysis (passing networks)
❌ **Missing:** How teams move as collective units

## Right Column: Our Solution

**What Topology Adds:**

**Key Insight:** A football match at any moment = 22 points in ℝ²

**What Topology Tells Us:**
• **H₀ (connected components):** How many distinct player groups?
• **H₁ (holes/loops):** Are there gaps in defensive structures?
• **Persistence:** Which structures are stable vs. transient?

## Key Questions

**What We're Missing:**
• How do tactical structures form and dissolve?
• When do teams transition between defensive/attacking states?
• Can we identify exploitable gaps in defensive formations?
• How do two competing teams interact as a coupled system?

---

# SLIDE 3: MATHEMATICAL APPROACH

## Title
**Formal Framework & Innovation**

## Top Section: Formal Framework

**Point Cloud Construction:**
At time t: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ²

**Vietoris-Rips Filtration:**
VR(X_t, r) = {σ | diam(σ) ≤ r}

**Persistence Diagrams:**
D_k(X_t) = {(b_i, d_i) | birth and death of k-cycles}

## Middle Section: Key Innovation

**Evolution Operator:**
Φ_τ: D_k(X_t) → D_k(X_{t+τ})

**Standard TDA:** Static point clouds
**Our Innovation:** Dynamic systems on persistence diagrams

## Research Questions

1. Does Φ_τ admit fixed points? (Tactical attractors)
2. What's the spectral decomposition of dΦ? (Stability)
3. Can we prove ergodicity properties? (Statistical structure)

## Side Panel: Mathematical Problems

**Problem 1:** Stability under noise
CONJECTURE: d_B(D_clean, D_noisy) ≤ Cσ

**Problem 2:** Attractor state characterisation
CONJECTURE: Finite decomposition into tactical basins

**Problem 3:** Soliton-like propagation
THEOREM TO PROVE: Persistent H₁ features propagate as integrable PDEs

**Problem 4:** Zero-sum game topology
Connect Nash equilibria to topological symmetry breaking

---

# SLIDE 4: KEY RESULTS & INSIGHTS

## Title
**Preliminary Findings & Performance Correlations**

## Three Key Results

**Result 1: GPS-Aware Clustering**
✅ Resolved point cloud size artefact
22 → 8-12 meaningful clusters
Preserves tactical structure

**Result 2: Multi-Scale Validation**
✅ Consistent signatures across time scales
1min, 2min, 5min, 10min windows
Suggests genuine attractor states

**Result 3: Three Tactical States**
• State 1: Defensive compression (5.2 steps)
• State 2: Transition state (1.0 steps)
• State 3: Offensive expansion (3.8 steps)

## Performance Correlations (Large Highlight Boxes)

**H₁ Feature Persistence → Successful Attacking Play**
Correlation: r = 0.68, p < 0.001
*Interpretation: Persistent holes in defence = attacking opportunities*

**H₀ Component Count → Defensive Solidity**
Correlation: r = -0.52, p < 0.01
*Interpretation: Fewer distinct groups = better defensive cohesion*

## Tactical State Transitions

**During a Match:**
1. **Defensive State:** Compact formation, high H₀, low H₁
2. **Transition:** Structure breaks, H₀ increases, H₁ features appear
3. **Attacking State:** Expanded formation, holes in defence (H₁ persistence)

**Topological Prediction:**
State transitions correspond to critical topological events (birth/death of H₁ features with persistence > threshold τ)

---

# SLIDE 5: IMPACT & FUTURE WORK

## Title
**Impact & Next Steps**

## Three Columns

### Column 1: Academic Impact

**Mathematical Contributions:**
• Novel framework for dynamical systems on persistence diagrams
• First rigorous treatment of competitive persistent homology
• Theoretical foundations for topology in competitive systems

**Publications:**
• 6 high-impact papers (SIAM, Physica D, Journal of Sports Sciences)
• Open-source software release
• Conference presentations

### Column 2: Industry & Commercial Impact

**Sports Analytics:**
• Real-time tactical analysis for professional clubs
• Performance optimisation through topological insights
• Enhanced fan engagement

**Partnerships:**
• Genius Sports: Commercial deployment
• Professional clubs: 3 Premier League pilots
• Technology transfer: Patent applications

### Column 3: Broader Applications

**Beyond Football:**
• Swarm Robotics: Multi-robot coordination
• Crowd Dynamics: Stadium evacuation modelling
• Biological Systems: Collective animal behaviour

**Why Topology?**
*Captures shape and structure that distance metrics miss*

## Current Status

**Completed:**
✅ GPS-aware clustering framework
✅ Multi-scale temporal validation
✅ Performance correlation analysis
✅ Industry partnership established

**In Progress:**
🔄 Mathematical proof development
🔄 Algorithm optimisation for real-time analysis
🔄 EPSRC Mathematical Sciences grant application

**Future (36-month project):**
📋 Commercial prototype development
📋 Cross-domain applications
📋 Educational resources

## Why This Matters

**For Mathematics:** New theoretical framework for competitive systems
**For Sports Science:** Quantitative understanding of collective tactics
**For Society:** Enhanced understanding of collective behaviour

---

# QUICK COPY-PASTE CHECKLIST

Use this template to quickly build your Keynote slides:

1. Copy each slide's title into Keynote
2. Copy bullet points into text boxes
3. Format mathematical notation using Keynote's equation editor
4. Add icons/visuals from Keynote's library
5. Apply consistent formatting (fonts, colours, sizes)

**Estimated Build Time:** 30-45 minutes

---

# TEXT FORMATTING NOTES

**Mathematical Notation:**
- Use Keynote's equation editor (Insert → Equation)
- Or use LaTeX syntax and convert to images
- Ensure proper subscript/superscript formatting

**Emphasised Text:**
- **Bold** for key terms
- *Italic* for interpretations
- Use colours for different sections (blue for academic, green for industry)

**Bullet Points:**
- Use consistent bullet style throughout
- Keep to 5-6 points per slide maximum
- Use sub-bullets for nested information
