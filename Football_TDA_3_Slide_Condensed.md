# Football-TDA: Condensed 3-Slide Version
## For Shorter Presentations (2-3 minutes)

---

# SLIDE 1: Problem & Approach

## Title
**Topological Data Analysis for Dynamic Team Behaviour**

**Subtitle:** Understanding how football teams move as collective units

---

## Left Column: The Problem

**Current Limitations:**
- Individual player metrics only
- Simple geometric measures
- Network analysis misses spatial structure
- **Missing:** Collective dynamics and tactical structure

**What We're Missing:**
- How do teams form tactical structures?
- When do they transition between states?
- Can we identify exploitable gaps?

---

## Right Column: Our Solution

**Key Innovation:**
First application of persistent homology to competitive 22-body systems

**Topology Captures:**
- **H₀:** Connected components (player groups)
- **H₁:** Holes (gaps in defensive structures)
- **Persistence:** Stable vs. transient structures

**Mathematical Framework:**
- Point cloud: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ²
- Evolution operator: Φ_τ: D_k(X_t) → D_k(X_{t+τ})
- Analyse dynamical system on persistence diagrams

---

## Visual
**Top Diagram:** 22-player pitch showing point cloud
**Bottom Diagram:** Example showing H₀ clusters and H₁ hole

---

## Key Message
*"Topology captures shape and structure that distance metrics miss, enabling quantitative analysis of collective tactical dynamics."*

---

# SLIDE 2: Key Results

## Title
**Preliminary Findings & Validation**

---

## Three Key Results

### Result 1: GPS-Aware Clustering ✅
- Resolved point cloud size artefact
- 22 → 8-12 meaningful clusters
- Preserves tactical structure

### Result 2: Three Tactical States Identified
- **Defensive compression** (5.2 steps mean lifetime)
- **Transition state** (1.0 steps)
- **Offensive expansion** (3.8 steps)

### Result 3: Performance Correlations
- **H₁ persistence → Attacking success:** r = 0.68, p < 0.001
- **H₀ count → Defensive solidity:** r = -0.52, p < 0.01

---

## Visual Elements

**Top Section:**
- Three tactical state diagrams side by side
- Labeled: Defensive / Transition / Offensive

**Middle Section:**
- Scatter plot: H₁ persistence vs. attacking success
- Trend line showing positive correlation
- Statistics box: "r = 0.68, p < 0.001"

**Bottom Section:**
- Multi-scale validation: Line graph showing consistency across 1min, 2min, 5min, 10min windows

---

## Key Message
*"Strong correlations validate that topology captures genuine tactical effectiveness, not just positional patterns."*

---

# SLIDE 3: Impact & Next Steps

## Title
**Impact & Future Work**

---

## Three Impact Dimensions

### Academic Impact
**Mathematical Contributions:**
- Novel framework for dynamical systems on persistence diagrams
- First rigorous treatment of competitive persistent homology
- Theoretical foundations for topology in competitive systems

**Deliverables:**
- 6 high-impact publications (SIAM, Physica D, Journal of Sports Sciences)
- Open-source software release
- Conference presentations (SIAM, NetSci, World Congress)

---

### Industry & Commercial Impact
**Sports Analytics:**
- Real-time tactical analysis for professional clubs
- Performance optimisation through topological insights
- Enhanced fan engagement

**Partnerships:**
- Genius Sports: Commercial deployment pathway
- 3 Premier League club pilots
- Patent applications and licensing

---

### Broader Applications
**Beyond Football:**
- Swarm Robotics: Multi-robot coordination
- Crowd Dynamics: Stadium evacuation modelling
- Biological Systems: Collective animal behaviour

**Why Topology?**
*Captures shape and structure that distance metrics miss*

---

## Current Status

### ✅ Completed
- GPS-aware clustering framework
- Multi-scale temporal validation
- Performance correlation analysis
- Industry partnership established

### 🔄 In Progress
- Mathematical proof development
- Algorithm optimisation for real-time analysis
- EPSRC Mathematical Sciences grant application

### 📋 Future (36-month project)
- Commercial prototype development
- Cross-domain applications
- Educational resources

---

## Visual Layout

**Three-Column Structure:**
- Left: Academic (blue tones)
- Middle: Industry (green tones)
- Right: Broader (orange/purple tones)

**Status Indicators:**
- Colour-coded checkmarks and progress indicators
- Timeline showing past → present → future

---

## Key Message
*"This research delivers significant academic contributions, commercial applications, and cross-domain impact through novel mathematical methods for understanding collective dynamics."*

---

# CONDENSED PRESENTATION GUIDE

## Timing Breakdown

**Slide 1 (Problem & Approach):** 45-60 seconds
- Quick problem statement
- Introduce topology concept
- Show mathematical framework

**Slide 2 (Key Results):** 60-75 seconds
- Three key findings
- Emphasise correlations
- Show visual evidence

**Slide 3 (Impact & Next Steps):** 45-60 seconds
- Three impact dimensions
- Current status
- Forward-looking statements

**Total Time:** 2.5-3 minutes

---

## Key Messages to Emphasize

1. **Novel Application:** First use of TDA for competitive team dynamics
2. **Validated Approach:** Strong correlations prove practical value
3. **Multi-Dimensional Impact:** Academic, commercial, and broader applications

---

## Simplified Speaker Notes

### Slide 1: Problem & Approach
*"Current sports analytics miss the collective dynamics of how teams move together. Topology gives us a new lens—treating each moment as 22 points in 2D space and asking about shape and structure. Our innovation is analysing how these topological features evolve over time, creating a dynamical system on persistence diagrams."*

### Slide 2: Key Results
*"We've validated our approach through three key results. First, we resolved critical technical challenges through GPS-aware clustering. Second, we've identified three distinct tactical states with characteristic lifetimes. Most importantly, we're seeing strong correlations—persistent holes in defences correlate with successful attacks, proving topology captures something real about tactical effectiveness."*

### Slide 3: Impact & Next Steps
*"This research has significant potential across three dimensions. Academically, we're developing new mathematical theory that will be published in top journals. Industrially, we're working with Genius Sports and professional clubs to deploy real-time analytical tools. And the methods have broader applications to robotics, crowd safety, and biological systems. We've completed foundational work and are now expanding through the EPSRC grant application."*

---

# DESIGN SPECIFICATIONS FOR 3-SLIDE VERSION

## Slide Layout

**Slide 1:**
- Split design: Problem (left) vs. Solution (right)
- Visual: Combined pitch diagram showing both concepts
- Emphasis: Clear contrast between "what's missing" and "our innovation"

**Slide 2:**
- Three-column results layout
- Large visual: Correlation scatter plot (centre focus)
- Supporting diagrams: Tactical states, multi-scale validation
- Emphasis: Validation and proof of concept

**Slide 3:**
- Three-column impact layout
- Status indicators at bottom
- Visual hierarchy: Impact dimensions (top), Status (bottom)
- Emphasis: Multi-dimensional value and forward momentum

---

## Visual Recommendations

**Slide 1:**
- Use side-by-side comparison (traditional vs. topological)
- Keep mathematical notation clear but not overwhelming
- Focus on intuitive explanation before deep mathematics

**Slide 2:**
- Make correlation plot the visual centrepiece
- Use colours effectively: Green for success, blue for methodology
- Show progression: Technical solution → States → Validation

**Slide 3:**
- Balance three impact columns equally
- Use icons to quickly communicate each dimension
- Status timeline creates sense of momentum and progress

---

## Quick Comparison: 5-Slide vs. 3-Slide

### When to Use 5-Slide Version:
- Academic conferences
- Detailed technical presentations
- Audiences familiar with TDA
- 5-6 minute time slots
- Need for comprehensive coverage

### When to Use 3-Slide Version:
- Quick introductions
- Mixed audiences (technical + non-technical)
- Poster sessions or lightning talks
- 2-3 minute time slots
- Need for high-level overview

---

# TRANSITION TIPS FOR 3-SLIDE VERSION

## Smooth Transitions

**Between Slides:**
- Slide 1 → 2: *"So with that framework, here's what we've found..."*
- Slide 2 → 3: *"These results open up significant opportunities..."*

**Within Slides:**
- Use consistent language and terminology
- Build narrative: Problem → Solution → Evidence → Impact
- Maintain visual consistency across slides

---

# ADAPTING CONTENT

## If Time is Very Limited (1-2 minutes):
- Focus on Slide 2 (Results)
- Briefly mention problem and impact
- Use one powerful visual (correlation plot)

## If Audience Needs More Detail:
- Expand Slide 1 mathematical framework
- Add more statistical detail to Slide 2
- Elaborate on impact dimensions in Slide 3

## If Audience is Non-Technical:
- Simplify mathematical notation
- Focus on intuitive explanations
- Emphasise practical applications and impact

---

This condensed 3-slide version provides a concise yet comprehensive overview suitable for shorter presentations whilst maintaining all key messages and impact potential.
