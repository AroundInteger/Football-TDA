# Football-TDA: Visual Diagrams for Keynote
## Step-by-Step Instructions for Recreating Diagrams

---

# DIAGRAM 1: Football Pitch with 22 Players (Slide 1 & 2)

## Purpose
Show basic point cloud representation: 22 players as points on a pitch

## Dimensions
- Pitch: 105m × 68m (standard football pitch proportions)
- Scale: Use a rectangle with aspect ratio approximately 1.54:1

## Layout Instructions

### Step 1: Draw Pitch Outline
- Draw rectangle: width 105 units, height 68 units
- Add centre line (vertical line at 52.5 units)
- Add centre circle (radius 9.15 units from centre)
- Optional: Add penalty areas and goal areas

### Step 2: Add Players
- **Team 1 (Red dots):** 11 players
  - Goalkeeper: Near left goal (x=5, y=34)
  - Defence: x=15-25, y=20-50 (4 players, spread vertically)
  - Midfield: x=35-45, y=15-55 (4 players)
  - Attack: x=55-65, y=25-45 (2 players)

- **Team 2 (Blue dots):** 11 players (mirrored on right side)
  - Goalkeeper: Near right goal (x=100, y=34)
  - Defence: x=80-90, y=20-50 (4 players)
  - Midfield: x=60-70, y=15-55 (4 players)
  - Attack: x=40-50, y=25-45 (2 players)

### Step 3: Add Labels
- Label: "22 points in ℝ²"
- Optional: Add player numbers (1-11 for each team)

## Visual Style
- Pitch: Light green fill (#90EE90) with white lines
- Players: Coloured dots (8-10pt circles)
- Team 1: Red (#FF0000)
- Team 2: Blue (#0000FF)
- Keep it simple and clean

---

# DIAGRAM 2: H₀ Connected Components (Slide 2)

## Purpose
Illustrate how H₀ counts distinct player groups/clusters

## Layout Instructions

### Step 1: Start with Diagram 1
- Use the 22-player pitch layout from Diagram 1

### Step 2: Add Cluster Boundaries
- Draw circles around groups of nearby players
- **Cluster 1:** Defence line (4-5 players grouped)
- **Cluster 2:** Midfield group (3-4 players)
- **Cluster 3:** Attack group (2-3 players)
- **Cluster 4:** Midfield battle (players from both teams)
- Use dashed circles with different colours

### Step 3: Label Components
- Add label: "H₀ = 4 connected components"
- Use arrows pointing to each cluster
- Use matching colours for cluster circles and labels

### Step 4: Add Legend
- H₀: "Number of distinct player groups"
- Show: "Fewer groups = better team cohesion"

## Visual Style
- Cluster circles: Dashed lines, semi-transparent (30% opacity)
- Each cluster different colour: Red, Blue, Green, Orange
- Labels: Bold, 14pt, matching cluster colours
- Keep player dots visible but make clusters prominent

---

# DIAGRAM 3: H₁ Holes in Defence (Slide 2)

## Purpose
Show how H₁ detects gaps/holes in defensive formations

## Layout Instructions

### Step 1: Create Defensive Formation
- Draw 4 defenders in a line: positions (x=20, y=20), (x=20, y=30), (x=20, y=40), (x=20, y=50)
- Draw goalkeeper at (x=5, y=34)
- Draw 2 midfielders ahead: (x=35, y=25), (x=35, y=45)

### Step 2: Show the "Hole"
- Draw a shaded region between defenders showing exploitable gap
- Position: Between middle defenders (approximately x=20-35, y=30-40)
- Use lighter shade to show the void/empty space

### Step 3: Connect Players
- Draw lines connecting nearby defenders to form boundary
- Connect: goalkeeper to defender 1, defender 1 to 2, defender 2 to 3, defender 3 to 4, defender 4 back to goalkeeper
- This creates a loop around the pitch area

### Step 4: Highlight the Hole
- Add arrow pointing to the gap: "H₁ hole - exploitable space"
- Label: "H₁ = 1 (one hole in defensive structure)"
- Use contrasting colour (e.g., yellow or orange) for the hole

### Step 5: Add Attacker
- Place attacking player near the hole: (x=40, y=35)
- Add arrow: "Attacking opportunity"

## Visual Style
- Defenders: Larger dots, blue (#0000FF), connected with solid lines
- Hole: Semi-transparent yellow/orange fill (#FFD700, 40% opacity)
- Attacker: Red dot (#FF0000), larger than defenders
- Labels: Bold, 16pt, clear and readable

---

# DIAGRAM 4: Vietoris-Rips Filtration Process (Slide 3)

## Purpose
Illustrate how the filtration parameter r creates different simplicial complexes

## Layout Instructions

### Step 1: Create Three Panels (Side by Side)

**Panel 1: r = 5m (small)**
- Use 8-10 players in close formation
- Draw small circles (radius 5m) around each player
- Show only direct connections (no triangles)
- Label: "r = 5m: No connections"

**Panel 2: r = 15m (medium)**
- Same player positions
- Draw larger circles (radius 15m) around players
- Draw lines connecting overlapping circles
- Show some triangles formed
- Label: "r = 15m: Some connections, triangles appear"

**Panel 3: r = 30m (large)**
- Same player positions
- Draw very large circles (radius 30m)
- Show dense network of connections
- Many triangles and higher-order simplices
- Label: "r = 30m: Fully connected"

### Step 2: Add Persistence Diagram
- Below the three panels, show a persistence diagram
- X-axis: Birth (b_i)
- Y-axis: Death (d_i)
- Show dots representing features:
  - H₀ features: On diagonal (birth = death)
  - H₁ features: Above diagonal (death > birth)
- Label: "Persistence Diagram D_k(X_t)"

### Step 3: Add Arrows
- Show progression: Panel 1 → Panel 2 → Panel 3 → Persistence Diagram
- Use arrows to show the filtration process

## Visual Style
- Panels: Bordered boxes, clean white background
- Player dots: Small, consistent size
- Circles: Dashed lines, light grey (#CCCCCC)
- Connections: Solid lines, blue (#0000FF)
- Persistence diagram: Clean, with clear axes and labels

---

# DIAGRAM 5: Evolution Operator Φ_τ (Slide 3)

## Purpose
Show how persistence diagrams evolve over time

## Layout Instructions

### Step 1: Create Timeline Layout
- Horizontal timeline at bottom: t → t+τ → t+2τ → t+3τ
- Mark time points with vertical lines

### Step 2: Persistence Diagrams at Each Time
- **At t:** Draw persistence diagram with 3 H₁ features
  - Feature 1: Birth=10, Death=20 (long persistence)
  - Feature 2: Birth=15, Death=18 (short persistence)
  - Feature 3: Birth=12, Death=25 (long persistence)
  
- **At t+τ:** Draw persistence diagram
  - Feature 1: Moved slightly (Birth=11, Death=21)
  - Feature 2: Disappeared (was short-lived)
  - Feature 3: Still present (Birth=13, Death=26)
  - New Feature 4: Appeared (Birth=16, Death=19)

- **At t+2τ:** Draw persistence diagram
  - Feature 1: Still present, shifted
  - Feature 3: Still present
  - Feature 4: Gone
  - New Feature 5: Appeared

### Step 3: Connect Features Across Time
- Draw arrows showing which features persist
- Use different colours for different features
- Show that some features are stable (persist across time)

### Step 4: Add Evolution Operator Symbol
- Large arrow labeled: "Φ_τ: D_k(X_t) → D_k(X_{t+τ})"
- Show it connecting diagrams across time

### Step 5: Highlight Stable Features
- Circle or highlight features that persist across multiple time steps
- Label: "Persistent features = Tactical attractors"

## Visual Style
- Timeline: Clean horizontal line with clear markers
- Persistence diagrams: Consistent style, clear axes
- Evolution arrows: Bold, curved, different colours
- Persistent features: Highlighted with glow or thicker outline
- Use consistent colour coding for features across time

---

# DIAGRAM 6: Three Tactical States (Slide 4)

## Purpose
Illustrate the three identified tactical states with pitch formations

## Layout Instructions

### Step 1: Create Three Panels (Side by Side)

**Panel 1: Defensive Compression**
- 11 players (one team only, red)
- Compact formation: players in small area
- Positions clustered around own half
- Goalkeeper deep, defence line at x=15, midfield at x=25
- Label: "State 1: Defensive Compression"
- Sub-label: "Mean lifetime: 5.2 steps"

**Panel 2: Transition State**
- 11 players (red team)
- Disorganised/mixed formation
- Players spread across field
- Some gaps, some clusters
- Label: "State 2: Transition State"
- Sub-label: "Mean lifetime: 1.0 steps"

**Panel 3: Offensive Expansion**
- 11 players (red team)
- Expanded formation
- Players spread wide and forward
- Attack line at x=70, midfield at x=50, defence at x=30
- Label: "State 3: Offensive Expansion"
- Sub-label: "Mean lifetime: 3.8 steps"

### Step 2: Add Topological Features
- Panel 1: Show high H₀ count (many small clusters), low H₁
- Panel 2: Show mixed H₀/H₁ values
- Panel 3: Show low H₀ (fewer groups), high H₁ (holes appearing)

### Step 3: Add Arrows Between States
- Show transitions: State 1 → State 2 → State 3 → (cycle back)
- Label arrows: "State transition"

## Visual Style
- Each panel: Bordered, clean background
- Players: Coloured dots (red for team)
- Formation lines: Light dashed lines connecting nearby players
- Labels: Bold headers, smaller sub-labels
- Use colour coding: Defensive=blue tones, Transition=yellow, Offensive=red tones

---

# DIAGRAM 7: Correlation Scatter Plot (Slide 4)

## Purpose
Show the correlation between H₁ persistence and attacking success

## Layout Instructions

### Step 1: Create Axes
- X-axis: "H₁ Feature Persistence" (0 to 30)
- Y-axis: "Attacking Success Rate" (0% to 100%)
- Label axes clearly
- Add grid lines for readability

### Step 2: Plot Data Points
- Create 20-30 data points
- Main trend: Positive correlation (points going up and right)
- Some scatter around the trend line
- Distribution: More points in middle range, fewer at extremes

### Step 3: Add Trend Line
- Draw best-fit line through points
- Line should slope upward (positive correlation)
- Make line bold, contrasting colour (e.g., red #FF0000)

### Step 4: Add Statistics
- Add text box: "r = 0.68, p < 0.001"
- Position in top right corner
- Make statistics prominent

### Step 5: Add Interpretation
- Text box: "Persistent holes in defence = Attacking opportunities"
- Position below graph or in corner

## Visual Style
- Axes: Clean lines, clear labels, consistent font
- Data points: Medium-sized circles (6-8pt), blue (#0000FF), semi-transparent (70% opacity)
- Trend line: Bold, red (#FF0000), 3pt width
- Grid: Light grey (#E0E0E0), subtle
- Statistics: Bold, large font (18-20pt)

---

# DIAGRAM 8: Tactical State Timeline (Slide 4)

## Purpose
Show how states transition during a match

## Layout Instructions

### Step 1: Create Horizontal Timeline
- Draw horizontal line across slide
- Mark time points: 0min, 15min, 30min, 45min, 60min, 75min, 90min
- Label time points

### Step 2: Add State Blocks
- Colour-coded blocks above timeline
- **Blue blocks:** Defensive compression state
- **Yellow blocks:** Transition state (thin, short)
- **Red blocks:** Offensive expansion state
- Show blocks changing throughout the match
- Typical pattern: Blue → Yellow → Red → Yellow → Blue (cycles)

### Step 3: Add Pitch Diagrams
- Below key time points, add small pitch diagrams
- Show player formations at: 10min, 30min, 50min, 70min
- Match formations to the state blocks above

### Step 4: Add H₀/H₁ Values
- Above each state block, show topological values
- Example: "H₀=6, H₁=0" for defensive state
- Example: "H₀=4, H₁=2" for offensive state

### Step 5: Highlight Critical Transitions
- Mark transitions with vertical lines or arrows
- Label: "Critical topological event"
- Show where H₁ features appear/disappear

## Visual Style
- Timeline: Clean horizontal line, clear markers
- State blocks: Solid colours, clearly separated
- Pitch diagrams: Small, simplified, consistent style
- Labels: Clear, readable, consistent font size
- Use colour coding throughout for consistency

---

# DIAGRAM 9: Impact Roadmap (Slide 5)

## Purpose
Show the three impact dimensions and timeline

## Layout Instructions

### Step 1: Create Three Vertical Columns

**Column 1: Academic Impact**
- Header: "Academic"
- Icons: Graduation cap, book, microscope
- Bullet points:
  • 6 publications
  • Open-source software
  • Conference presentations
- Colours: Blue tones

**Column 2: Industry Impact**
- Header: "Industry"
- Icons: Factory, handshake, chart
- Bullet points:
  • 3 pilot deployments
  • Patent applications
  • Commercial partnerships
- Colours: Green tones

**Column 3: Broader Applications**
- Header: "Broader"
- Icons: Robot, crowd, DNA helix
- Bullet points:
  • Swarm robotics
  • Crowd dynamics
  • Biological systems
- Colours: Orange/Purple tones

### Step 2: Add Timeline Below
- Horizontal timeline: Year 1 → Year 2 → Year 3
- Show milestones for each column
- Use colour-coded markers matching columns

### Step 3: Add Connection Lines
- Show how academic work feeds into industry
- Show how both feed into broader applications
- Use curved arrows connecting columns

### Step 4: Add Key Metrics
- Large numbers at top:
  - "6" publications (academic)
  - "3" pilots (industry)
  - "3+" domains (broader)

## Visual Style
- Columns: Equal width, clearly separated
- Icons: Consistent style (outline or filled)
- Timeline: Clean, professional
- Connection arrows: Subtle, curved
- Metrics: Large, bold, eye-catching

---

# DIAGRAM 10: Project Status Dashboard (Slide 5)

## Purpose
Show current project status and next steps

## Layout Instructions

### Step 1: Create Three Sections

**Section 1: Completed (Green background)**
- Header: "✅ Completed"
- Checkmark icons
- Items:
  • GPS-aware clustering framework
  • Multi-scale temporal validation
  • Performance correlation analysis
  • Industry partnership established

**Section 2: In Progress (Yellow/Orange background)**
- Header: "🔄 In Progress"
- Spinning/circular arrow icons
- Items:
  • Mathematical proof development
  • Algorithm optimisation
  • EPSRC grant application

**Section 3: Future (Blue background)**
- Header: "📋 Future (36-month project)"
- Calendar/roadmap icons
- Items:
  • Commercial prototype
  • Cross-domain applications
  • Educational resources

### Step 2: Add Progress Bars
- For "In Progress" section, show progress bars
- Mathematical proofs: 40% complete
- Algorithm optimisation: 60% complete
- Grant application: 80% complete

### Step 3: Add Timeline
- Small timeline showing: Past → Present → Future
- Mark current position clearly

## Visual Style
- Sections: Distinct background colours, bordered
- Icons: Consistent style throughout
- Progress bars: Professional, colour-coded
- Clean, dashboard-like appearance
- Use cards/boxes for each item

---

# GENERAL DESIGN GUIDELINES FOR ALL DIAGRAMS

## Consistency
- Use same colour palette throughout all slides
- Maintain consistent player/pitch representation
- Use same font family and sizes for labels
- Keep diagram style consistent (realistic vs. schematic)

## Simplicity
- Don't overcrowd diagrams
- Focus on one key message per diagram
- Use white space effectively
- Remove unnecessary elements

## Readability
- Labels should be clear and readable from a distance
- Use contrasting colours for text and backgrounds
- Ensure diagrams work in both light and dark presentation modes
- Test on actual presentation screen if possible

## Professional Appearance
- Clean lines, no unnecessary decorations
- Consistent arrow styles
- Professional colour choices (avoid bright neon colours)
- Polished, academic tone

---

# QUICK REFERENCE: DIAGRAM CHECKLIST

Use this when building your Keynote presentation:

- [ ] Diagram 1: 22-player pitch layout
- [ ] Diagram 2: H₀ connected components
- [ ] Diagram 3: H₁ holes in defence
- [ ] Diagram 4: Vietoris-Rips filtration (3 panels)
- [ ] Diagram 5: Evolution operator timeline
- [ ] Diagram 6: Three tactical states
- [ ] Diagram 7: Correlation scatter plot
- [ ] Diagram 8: Tactical state timeline
- [ ] Diagram 9: Impact roadmap (3 columns)
- [ ] Diagram 10: Project status dashboard

**Estimated Time:** 2-3 hours to create all diagrams (depending on Keynote experience)
