# Football-TDA Project: Keynote Presentation Guide
## 5-Slide Overview for Peer Presentations

---

# SLIDE 1: Title & Overview

## Slide Title
**Topological Data Analysis for Dynamic Team Behaviour**

**Subtitle:** Mathematical Foundations for Sports Analytics

---

## Content Blocks

### Left Column (60% width)

**Main Question:**
```
Can we use topology to understand 
how football teams move as 
collective units?
```

**Key Innovation:**
```
First application of persistent 
homology to competitive 
22-body dynamical systems
```

### Right Column (40% width)

**Visual:**
- Football pitch silhouette
- 22 dots representing players (11 per team)
- Connecting lines showing potential topological structures

---

## Key Points (Bullet Format)

- **Research Question:** Can we use topology to understand how football teams move as collective units?
- **Key Innovation:** First application of persistent homology to competitive 22-body dynamical systems
- **Approach:** Treat the entire match as a point cloud evolving through time, extracting topological features that capture tactical structures

---

## Project Status Indicators

### ✅ Completed
- Preliminary results validating approach
- Industry partnership (Genius Sports) established

### 🔄 In Progress
- EPSRC Mathematical Sciences grant application in development

---

## Design Specifications

**Background:**
- Subtle gradient: Deep blue (#1E3A8A) to lighter blue (#3B82F6)
- Optional: Very faint football pitch grid pattern (10% opacity)

**Text:**
- Title: 44pt, Bold, White
- Subtitle: 28pt, Regular, Light grey (#E5E7EB)
- Body text: 20pt, Regular, White

**Accent Colour:**
- Green (#10B981) for checkmarks and highlights

**Visual Elements:**
- Small football pitch diagram in top right corner
- Project logo (if available) in bottom left

---

## Speaker Notes

*"Good morning/afternoon. Today I'll be presenting our research on using topological data analysis to understand how football teams move as collective units. This represents the first application of persistent homology to competitive 22-body dynamical systems. We've already validated our approach with preliminary results and established an industry partnership with Genius Sports. We're currently developing an EPSRC grant application to expand this work."*

**Timing:** 30-45 seconds

---

# SLIDE 2: The Problem

## Slide Title
**Current Limitations in Sports Analytics**

---

## Content Structure

### Left Side: Existing Methods (50% width)

**Header:** "What We Have Now"

**Bullet Points:**
- ❌ Individual player metrics (distance covered, speed)
- ❌ Simple geometric measures (team shape, length, width)
- ❌ Network analysis (passing networks)
- ❌ **Missing:** How teams move as collective units

**Visual:** Icons for each method (player silhouette, geometric shapes, network diagram)

---

### Right Side: Our Solution (50% width)

**Header:** "What Topology Adds"

**Key Insight:**
```
A football match at any moment 
= 22 points in ℝ²
```

**What Topology Tells Us:**
- **H₀ (connected components):** How many distinct player groups?
- **H₁ (holes/loops):** Are there gaps in defensive structures?
- **Persistence:** Which structures are stable vs. transient?

**Visual:** 
- Diagram showing 22 points on pitch
- H₀: Coloured clusters (red team, blue team, mid-field cluster)
- H₁: Annotated "hole" in defensive formation

---

## Key Questions Addressed

**What We're Missing:**
- How do tactical structures form and dissolve?
- When do teams transition between defensive/attacking states?
- Can we identify exploitable gaps in defensive formations?
- How do two competing teams interact as a coupled system?

---

## Design Specifications

**Background:**
- Split design: Left side darker (#1F2937), Right side lighter (#F9FAFB)
- Clear visual separation with vertical divider

**Colour Scheme:**
- Existing methods: Red accents (#EF4444) for limitations
- Our solution: Green accents (#10B981) for opportunities
- Mathematical notation: Blue (#3B82F6)

**Typography:**
- Title: 36pt, Bold
- Headers: 24pt, Semi-bold
- Body: 18pt, Regular
- Mathematical notation: 20pt, Regular (italic for variables)

**Visual Elements:**
- Comparison icons (left: traditional methods, right: topological approach)
- Simple pitch diagram with topological annotations

---

## Speaker Notes

*"Current sports analytics focus on individual metrics or simple geometric measures. They tell us how far a player ran or what shape the team made, but they miss the collective dynamics—how teams actually move together. Topology gives us a completely different perspective. We treat each moment as 22 points in 2D space and ask: What's the shape? Are there holes? Which structures persist? This captures the tactical essence that geometric measures miss."*

**Timing:** 1-1.5 minutes

---

# SLIDE 3: Mathematical Approach

## Slide Title
**Formal Framework & Innovation**

---

## Content Structure

### Top Section: Formal Framework

**Point Cloud Construction:**
```
At time t: X_t = {x₁(t),...,x₂₂(t)} ⊂ ℝ²
```

**Vietoris-Rips Filtration:**
```
VR(X_t, r) = {σ | diam(σ) ≤ r}
```

**Persistence Diagrams:**
```
D_k(X_t) = {(b_i, d_i) | birth and death of k-cycles}
```

**Visual:** 
- Animated sequence showing: Points → Filtration → Persistence diagram
- OR static diagram with three panels

---

### Middle Section: Key Innovation

**Evolution Operator:**
```
Φ_τ: D_k(X_t) → D_k(X_{t+τ})
```

**Standard TDA:** Static point clouds
**Our Innovation:** Dynamic systems on persistence diagrams

**Visual:**
- Timeline showing persistence diagrams at t, t+τ, t+2τ
- Evolution operator arrows connecting diagrams
- Highlight showing how structure changes over time

---

### Bottom Section: Research Questions

**Three Key Questions:**
1. Does Φ_τ admit fixed points? (Tactical attractors)
2. What's the spectral decomposition of dΦ? (Stability)
3. Can we prove ergodicity properties? (Statistical structure)

---

### Side Panel: Mathematical Problems

**Problem 1:** Stability under noise
- CONJECTURE: d_B(D_clean, D_noisy) ≤ Cσ

**Problem 2:** Attractor state characterisation
- CONJECTURE: Finite decomposition into tactical basins

**Problem 3:** Soliton-like propagation
- THEOREM TO PROVE: Persistent H₁ features propagate as integrable PDEs

**Problem 4:** Zero-sum game topology
- Connect Nash equilibria to topological symmetry breaking

---

## Design Specifications

**Background:**
- Clean white or very light grey (#F9FAFB)
- Subtle mathematical grid pattern (5% opacity)

**Colour Scheme:**
- Mathematical notation: Deep blue (#1E40AF)
- Innovation highlight: Green (#10B981)
- Problem statements: Orange accents (#F59E0B)

**Typography:**
- Title: 32pt, Bold
- Mathematical notation: 18pt, Regular (use LaTeX-style formatting)
- Research questions: 20pt, Semi-bold
- Problem statements: 16pt, Regular

**Layout:**
- Three-column or two-column layout
- Mathematical expressions in highlighted boxes
- Visual diagrams integrated throughout

---

## Speaker Notes

*"Let me outline the formal mathematical framework. At each time t, we have 22 player positions—this is our point cloud. We construct a Vietoris-Rips filtration, which connects players as we increase the distance threshold. This gives us persistence diagrams showing when topological features appear and disappear. The key innovation is that instead of analysing static point clouds, we study the evolution operator on persistence diagrams—essentially asking how the topology changes over time. This leads to fundamental questions about fixed points, stability, and statistical structure that we're working to answer."*

**Timing:** 2-2.5 minutes

---

# SLIDE 4: Key Results & Insights

## Slide Title
**Preliminary Findings & Performance Correlations**

---

## Content Structure

### Top Section: Key Results (Three Columns)

**Result 1: GPS-Aware Clustering**
- ✅ Resolved point cloud size artefact
- 22 → 8-12 meaningful clusters
- Preserves tactical structure

**Visual:** Before/after diagram showing clustering improvement

**Result 2: Multi-Scale Validation**
- ✅ Consistent signatures across time scales
- 1min, 2min, 5min, 10min windows
- Suggests genuine attractor states

**Visual:** Line graph showing persistence across different window sizes

**Result 3: Three Tactical States**
- State 1: Defensive compression (5.2 steps)
- State 2: Transition state (1.0 steps)
- State 3: Offensive expansion (3.8 steps)

**Visual:** Three distinct pitch formations with state labels

---

### Middle Section: Performance Correlations

**Large Highlight Box:**

**H₁ Feature Persistence → Successful Attacking Play**
```
Correlation: r = 0.68, p < 0.001
```
*Interpretation: Persistent holes in defence = attacking opportunities*

**Visual:** Scatter plot with correlation line

---

**Second Highlight Box:**

**H₀ Component Count → Defensive Solidity**
```
Correlation: r = -0.52, p < 0.01
```
*Interpretation: Fewer distinct groups = better defensive cohesion*

**Visual:** Bar chart or scatter plot

---

### Bottom Section: Tactical State Transitions

**Example Timeline:**

**During a Match:**
1. **Defensive State:** Compact formation, high H₀, low H₁
2. **Transition:** Structure breaks, H₀ increases, H₁ features appear
3. **Attacking State:** Expanded formation, holes in defence (H₁ persistence)

**Visual:** Annotated timeline with pitch diagrams at each stage

**Topological Prediction:**
*State transitions correspond to critical topological events (birth/death of H₁ features with persistence > threshold τ)*

---

## Design Specifications

**Background:**
- White or very light grey
- Optional: Subtle pitch pattern at 3% opacity

**Colour Scheme:**
- Result boxes: Light blue (#DBEAFE) with blue borders (#3B82F6)
- Correlation highlights: Green (#10B981) for positive, Orange (#F59E0B) for emphasis
- State diagrams: Red team (#EF4444), Blue team (#3B82F6)

**Typography:**
- Title: 32pt, Bold
- Result headers: 20pt, Semi-bold
- Statistics: 24pt, Bold (correlations)
- Interpretations: 16pt, Regular, Italic

**Visual Elements:**
- Graphs and charts clearly labelled
- Pitch diagrams with clear annotations
- Success indicators (checkmarks) prominently displayed

---

## Speaker Notes

*"Our preliminary results are very encouraging. First, we've resolved a critical artefact in the point cloud analysis through GPS-aware clustering, reducing noise whilst preserving tactical structure. Second, our multi-scale analysis shows consistent patterns across different time windows, suggesting we're capturing genuine attractor states rather than transient patterns. We've identified three distinct tactical states with characteristic lifetimes. Most importantly, we're seeing strong correlations between topological features and actual performance—persistent holes in defences correlate with successful attacks, and fewer connected components correlate with better defensive cohesion. This validates that topology captures something real about tactical effectiveness."*

**Timing:** 1.5-2 minutes

---

# SLIDE 5: Impact & Future Work

## Slide Title
**Impact & Next Steps**

---

## Content Structure

### Three-Column Layout

**Column 1: Academic Impact (33% width)**

**Mathematical Contributions:**
- Novel framework for dynamical systems on persistence diagrams
- First rigorous treatment of competitive persistent homology
- Theoretical foundations for topology in competitive systems

**Publications:**
- 6 high-impact papers (SIAM, Physica D, Journal of Sports Sciences)
- Open-source software release
- Conference presentations

**Visual:** Journal logos or icons

---

**Column 2: Industry & Commercial Impact (33% width)**

**Sports Analytics:**
- Real-time tactical analysis for professional clubs
- Performance optimisation through topological insights
- Enhanced fan engagement

**Partnerships:**
- Genius Sports: Commercial deployment
- Professional clubs: 3 Premier League pilots
- Technology transfer: Patent applications

**Visual:** Industry partner logos or collaboration diagram

---

**Column 3: Broader Applications (33% width)**

**Beyond Football:**
- Swarm Robotics: Multi-robot coordination
- Crowd Dynamics: Stadium evacuation modelling
- Biological Systems: Collective animal behaviour

**Why Topology?**
*Captures shape and structure that distance metrics miss*

**Visual:** Icons representing each application area

---

### Bottom Section: Current Status & Timeline

**Status Indicators:**

**Completed:**
- ✅ GPS-aware clustering framework
- ✅ Multi-scale temporal validation
- ✅ Performance correlation analysis
- ✅ Industry partnership established

**In Progress:**
- 🔄 Mathematical proof development
- 🔄 Algorithm optimisation for real-time analysis
- 🔄 EPSRC Mathematical Sciences grant application

**Future (36-month project):**
- 📋 Commercial prototype development
- 📋 Cross-domain applications
- 📋 Educational resources

**Visual:** Timeline or roadmap graphic

---

### Why This Matters Section

**Three Key Points:**

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

## Design Specifications

**Background:**
- Gradient: Deep blue (#1E3A8A) at top, lighter at bottom (#F9FAFB)
- Subtle geometric patterns

**Colour Scheme:**
- Academic: Blue tones (#3B82F6)
- Industry: Green tones (#10B981)
- Broader: Orange/Purple accents (#F59E0B, #8B5CF6)

**Typography:**
- Title: 32pt, Bold, White (if on dark background)
- Column headers: 20pt, Semi-bold
- Body text: 16pt, Regular
- Status indicators: 14pt, Regular

**Layout:**
- Clear three-column structure with equal widths
- Status timeline at bottom
- "Why This Matters" as callout box or footer

**Visual Elements:**
- Icons for each impact area
- Partner logos (if available)
- Timeline/roadmap graphic
- Visual connection lines showing relationships

---

## Speaker Notes

*"In summary, this research has significant potential across three dimensions. Academically, we're developing new mathematical theory for competitive systems that will be published in top journals. Industrially, we're working with Genius Sports and professional clubs to deploy real-time analytical tools. And the methods have broader applications to robotics, crowd safety, and biological systems. We've already completed foundational work and validated our approach. Our next steps include developing the mathematical proofs, optimising algorithms for real-time use, and expanding through the EPSRC grant. The key insight is that topology captures shape and structure in ways that traditional metrics simply cannot—and that has applications far beyond football."*

**Timing:** 1.5-2 minutes

---

# KEYNOTE DESIGN TEMPLATE

## Master Slide Settings

**Theme:** Modern, clean, professional
**Aspect Ratio:** 16:9 (widescreen)

## Colour Palette

**Primary Colours:**
- Deep Blue: `#1E3A8A` (backgrounds, headers)
- Medium Blue: `#3B82F6` (accents, links)
- Light Blue: `#DBEAFE` (highlights)

**Secondary Colours:**
- Green: `#10B981` (success, positive results)
- Orange: `#F59E0B` (emphasis, highlights)
- Red: `#EF4444` (contrast, warnings)

**Neutral Colours:**
- Dark Grey: `#1F2937` (text on light backgrounds)
- Light Grey: `#F9FAFB` (light backgrounds)
- White: `#FFFFFF` (text on dark backgrounds)

## Typography

**Font Family:** System fonts (San Francisco on Mac, Segoe UI on Windows)

**Titles:**
- Size: 32-44pt
- Weight: Bold
- Colour: White (on dark) or Dark Grey (on light)

**Headers:**
- Size: 20-24pt
- Weight: Semi-bold
- Colour: Primary blue or dark grey

**Body Text:**
- Size: 16-18pt
- Weight: Regular
- Colour: Dark grey or white (depending on background)

**Mathematical Notation:**
- Size: 18-20pt
- Weight: Regular
- Style: Italic for variables
- Use proper mathematical notation (subscripts, superscripts)

## Visual Elements

**Icons:**
- Use consistent icon style (outline or filled)
- Size: 24-32pt for emphasis
- Colour: Match theme colours

**Diagrams:**
- Clean, minimal football pitch diagrams
- Clear player positions (dots or silhouettes)
- Topological features clearly annotated
- Use consistent colour coding

**Charts and Graphs:**
- Professional styling
- Clear axis labels
- Legend if needed
- Highlighted key data points

**Transitions:**
- Subtle fade or slide transitions
- No distracting animations
- Maintain professional tone

---

# SPEAKER NOTES SUMMARY

## Total Presentation Time: 5-6 minutes

**Slide 1:** 30-45 seconds
- Introduction and positioning

**Slide 2:** 1-1.5 minutes
- Problem statement and topology introduction

**Slide 3:** 2-2.5 minutes
- Mathematical framework (longest slide)

**Slide 4:** 1.5-2 minutes
- Results and validation

**Slide 5:** 1.5-2 minutes
- Impact and future work

## Key Messages to Emphasize

1. **Novel Application:** First use of TDA for competitive team dynamics
2. **Mathematical Rigour:** Genuine theoretical contributions
3. **Practical Validation:** Strong preliminary results with real correlations
4. **Cross-Domain Potential:** Applications beyond sports
5. **Clear Impact:** Academic, commercial, and societal benefits

## Handling Questions

**Potential Questions & Responses:**

Q: *"How does this differ from network analysis?"*
A: "Network analysis focuses on relationships and connections. Topology captures shape and structure—the actual geometric arrangement. A network might tell you who passes to whom, but topology tells you about the spatial holes and voids that create tactical opportunities."

Q: *"Why is this better than existing methods?"*
A: "Existing methods miss the collective dynamics. Individual metrics don't capture how teams move together, and geometric measures miss the topological structure—the holes and gaps that are tactically significant. Topology gives us a new lens for understanding collective behaviour."

Q: *"How do you handle the computational complexity?"*
A: "With 22 points, standard TDA is computationally feasible. We're developing optimised algorithms using GPU acceleration, sparse filtrations, and temporal coherence to enable real-time analysis. Our preliminary results show we can process a frame in under 2 seconds."

Q: *"What if the theoretical proofs are difficult?"*
A: "We have a clear risk mitigation strategy. We'll identify which theorems are essential vs. nice-to-have early on. If some proofs prove intractable, we'll pivot to computational validation whilst maintaining mathematical rigour. The key is we're not just applying existing methods—we're developing new theory."

---

# CREATING THE KEYNOTE PRESENTATION

## Step-by-Step Instructions

1. **Open Keynote** and create a new presentation
2. **Choose Theme:** Select a clean, modern theme (or start with blank)
3. **Apply Master Styles:** Use the colour palette and typography specifications above
4. **Create 5 Slides:** Follow the content structure for each slide
5. **Add Visuals:** 
   - Create simple football pitch diagrams
   - Add icons from Keynote's icon library
   - Import any existing project graphics
6. **Format Mathematical Notation:**
   - Use Keynote's equation editor where possible
   - Or use LaTeX and convert to images
   - Ensure proper formatting for subscripts/superscripts
7. **Add Speaker Notes:** Copy speaker notes into Keynote's presenter notes section
8. **Review and Polish:**
   - Check consistency across slides
   - Ensure readability
   - Test on presentation screen if possible

## Quick Tips

- **Keep It Simple:** Don't overcrowd slides
- **Visual Hierarchy:** Use size and colour to guide attention
- **Consistency:** Maintain same style throughout
- **Practice:** Time yourself to stay within 5-6 minutes
- **Backup:** Have detailed notes ready for questions

---

This comprehensive guide provides everything needed to create a professional Keynote presentation that effectively communicates the Football-TDA research to peers. The structure balances mathematical rigour with accessible explanations, making it suitable for both mathematical and interdisciplinary audiences.
