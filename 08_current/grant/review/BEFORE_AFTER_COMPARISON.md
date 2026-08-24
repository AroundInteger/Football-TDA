# SIDE-BY-SIDE BEFORE/AFTER COMPARISON

Shows exactly what changes in each problem, why, and the impact.

---

## PROBLEM 1: NOVELTY CLAIM

### BEFORE (Paul flagged this)

```
Topological Data Analysis has revolutionised complex data understanding but existing 
applications examine single scales, non-competitive scenarios, or static data. Our work 
demonstrate that competitive, hierarchical, time-evolving systems exhibit rich multiscale 
structure current methods cannot capture. established three validated analysis scales—
individual (3m), tactical (12m), team (30m), each revealing complementary system 
organisation information—developed adaptive methods enabling robust pattern detection 
across all scales, a technical advance over fixed-parameter approaches. This represents 
the first multi-scale persistent homology application to competitive, coupled, 
high-frequency dynamical systems, new directions in computational topology creating 
methods autonomous systems, crowd safety, traffic management, and biological conservation.
```

**Word count:** 100 words  
**Problems:** Vague "firstness" claim; grammatical errors ("Our work demonstrate"); scope creep (autonomous systems, crowd safety); no evidence/validation numbers

---

### AFTER (Paul's feedback integrated)

```
Topological Data Analysis has proven effective for characterising the shape of complex 
data, but existing applications examine systems at single scales, in non-competitive 
scenarios, or with static data. A standard Vietoris–Rips filtration on a multi-agent 
point cloud conflates topological features from different organisational levels into a 
single persistence diagram. This project advances computational topology through two 
methodological contributions: domain-informed hierarchical clustering to decompose point 
clouds by organisational level, and adaptive filtration ensuring consistent H₁ (loop) 
detection across all scales. These contributions are practical and necessary—a fixed 
Vietoris–Rips threshold appropriate at one organisational level produces null results at 
another. These methods are designed for hierarchical, competitive, time-evolving point 
clouds, advancing the state of the art in applied topology.

Validation across 10 professional football matches (1,500 analysis frames) confirms three 
robust H₀ analysis regimes—individual (3 m), tactical (12 m), and team (30 m)—with 
stability scores of 0.84–1.00. The framework detects two complementary H₁ regimes: 
individual-scale topology reveals frequent, transient loops (97.0% ± 1.5% presence rate), 
whilst tactical-scale topology reveals rarer but geometrically distinct loops (19.3% ± 
7.2% presence rate). Scale complementarity is quantified: Spearman ρ = 0.254, confirming 
that neither scale subsumes the other. Real event correlation across 10 matches (104,722 
event–topology pairs) demonstrates that topological features respond coherently to match 
dynamics.

The mathematical contribution goes beyond methodological development: a full Championship 
season yields an empirical distribution of topological invariants at a scale more typical 
of physics or materials science than applied topology—over 500 matches support estimation 
of means, variances, and correlations of H₀/H₁ counts and landscape norms at each 
analysis scale. Dynamics are central: a match is not a single diagram but a temporal 
trajectory t ↦ PD_δ(t), so the object of study includes continuity, jumps, and regime 
shifts in time, not only static formation fingerprints. Coupling topological trajectories 
to event streams and tactical descriptors tests whether barcode statistics are orthogonal 
to conventional performance metrics or recover complementary structure. This Small Grant 
scales from proof-of-concept (10 matches, Brown 2026) to full-season population analysis 
(~540 matches), establishing population-level statistics on topological invariants and 
developing persistence landscape methods for temporal dynamics—a novel contribution to 
computational topology with immediate methodological and applied value.

While demonstrated on football—where high-frequency tracking and clear tactical structure 
enable rigorous validation—the framework is in principle transferable to other bounded 
competitive systems with spatial tracking data and a validated hierarchy of interaction 
scales. Applications to autonomous coordination, ecological dynamics, and crowd monitoring 
represent future directions beyond the scope of this 12-month project.
```

**Word count:** 370 words  
**Changes:**
- ✅ Fixes grammar ("has proven" not "revolutionised"; "Our work demonstrate" → proper construction)
- ✅ Specifies two methodological contributions clearly
- ✅ Includes ALL validation numbers: 0.84–1.00, 97.0% ± 1.5%, 19.3% ± 7.2%, ρ = 0.254, 104,722 pairs
- ✅ Tightens "firstness" to "advances state of the art" (defensible, not vague)
- ✅ Separates proof-of-concept (Brown 2026, 10 matches) from this grant's scope (540 matches)
- ✅ Moves broader applications to final paragraph explicitly marked as "future directions beyond this 12-month project"
- ✅ Adds mathematical perspective on dynamics (temporal trajectories, regime shifts)

**Paul's concerns addressed:** ✅ Scope clarity, ✅ Evidence included, ✅ Novelty tightened, ✅ Tone professional

---

## PROBLEM 2: PATHWAY SECTION

### BEFORE (Paul flagged this)

```
Pathway to Larger Research Programme: This rant critical stepping stone to aStandard 
Grant by generating robust multi-match validation, peer-reviewed publications demonstrating 
methodological validity, feasibility with diverse data, and validating industry partnerships. 
The focused scope provides contained but complete research arc, enabling expansion of 
theoretical frameworks (stability conditions, bifurcation analysis, predictive modelling), 
broader applications (autonomous systems, crowd dynamics, biological collectives), and 
real-time computational tools development. results will support Standard Grant submission 
within 18 months of project completion.
```

**Word count:** 80 words  
**Problems:** Typos ("This rant," "aStandard"); scope creep (expansion of frameworks, broader applications sound like this grant's deliverables); vague timeline

---

### AFTER (Paul's feedback integrated)

```
Research objectives and pathway to larger research programme: Building on the validated 
framework, this project pursues three research objectives over 12 months, with a fourth 
strategic output.

(1) Scale the analysis pipeline to a full Championship season (~540 matches), 
stress-testing the framework and establishing population-level topological statistics.

(2) Characterise pattern formation by developing baseline topological fingerprints for 
different tactical systems, quantifying formation times and distinguishing between tactical 
configurations in persistence space.

(3) Develop persistence landscape methods for temporal dynamics, classifying stability 
regimes and characterising transitions within and across matches.

(4) Synthesise full-season results into a Standard Grant application. The Standard Grant 
will extend the framework to broader competitive systems (autonomous coordination, 
ecological dynamics, crowd monitoring), leveraging the validated methods and evidence base 
from this Small Grant as foundation. Standard Grant preparation begins in Month 9, 
incorporating full-season results for submission within 12 months of project completion.
```

**Word count:** 130 words  
**Changes:**
- ✅ Removes typos ("This rant" → "Building on the validated framework")
- ✅ Four-part structure: Clear objectives (1), (2), (3) + strategic output (4)
- ✅ Each objective is concrete and testable
- ✅ Objective 4 explicitly frames Standard Grant as *separate project*, not part of this grant
- ✅ "The Standard Grant will extend..." — makes clear boundary between 12-month and 36-month projects
- ✅ Concrete timeline: "Month 9" and "within 12 months of project completion"
- ✅ Moves "autonomous systems, crowd dynamics, biological collectives" explicitly to Standard Grant scope

**Paul's concerns addressed:** ✅ Scope clarity, ✅ No scope creep, ✅ Concrete timeline, ✅ Professional tone

---

## PROBLEM 3: VISION/OPENING SECTION

### BEFORE (Paul flagged this)

```
From autonomous drone swarms navigating disaster zones to crowds flowing through transport 
hubs, understanding how groups coordinate and compete is fundamental to critical societal 
challenges. Current mathematical methods for analysing these systems have a practical 
limitation: they examine behaviour at a single spatial scale, missing the hierarchical 
organisation, individual decisions triggering tactical responses that shape system-wide 
patterns, characteristic of most real-world competitive multi-agent systems.
```

**Word count:** 60 words  
**Problems:** Starts with abstract speculation (drones, crowds); doesn't ground in football or research; doesn't explain why this research matters NOW

---

### AFTER (Paul's feedback integrated)

```
This research develops new mathematical frameworks for multi-scale topological analysis 
of competitive collective systems. Understanding how hierarchical organisation emerges 
from individual decisions and tactical responses—where individual agents, tactical groups, 
and team-wide strategy create nested but distinct organisational levels—is fundamental to 
competitive dynamics. Current methods examine behaviour at a single spatial scale, missing 
this hierarchical structure. Professional football provides an ideal testbed: high-quality 
tracking data (10–25 Hz), well-structured competitive system, domain-interpretable 
hierarchy (individual players ↔ tactical units ↔ team), and detailed event annotations. 
This Small Grant develops and validates topological methods on football data at full-season 
scale; the framework, by design, is transferable to other bounded competitive multi-agent 
systems with domain-validated interaction scales.
```

**Word count:** 120 words  
**Changes:**
- ✅ Opens with concrete research goal: "This research develops frameworks..."
- ✅ Grounds in football immediately
- ✅ Explains why football is ideal (tracking quality, hierarchy, events)
- ✅ Makes testbed role explicit: "develops on football; transferable to other systems"
- ✅ Removes abstract speculation about drones and crowds
- ✅ Explains hierarchical structure clearly (individual ↔ tactical ↔ team)

**Paul's concerns addressed:** ✅ Concrete focus, ✅ Football as testbed, ✅ Professional framing, ✅ No speculation

---

## PROBLEM 4: TIMELINESS SECTION

### BEFORE (Paul flagged this)

```
Computational advances in TDA libraries (Ripser, GUDHI) enable real-time computation on 
large point clouds. This makes now the right time. Industry demand is demonstrated 
through established partnerships with Genius Sports and championship clubs.
```

**Word count:** 35 words  
**Problems:** Weak; timeliness is about library availability, not research novelty; doesn't explain why this research matters theoretically

---

### AFTER (Paul's feedback integrated)

```
Timeliness. This research addresses foundational open questions in computational topology 
for hierarchical, time-evolving systems. The full-season analysis establishes population-
level statistical foundations: whether topological signatures are stable, reproducible 
features across a championship season, or exhibit meaningful distributional variation 
stratified by match context (phase-of-play, opponent strength, venue). The grant develops 
three new theoretical and methodological contributions: (1) persistence landscape methods 
for temporal dynamics, characterising stability regimes and regime shifts within and across 
matches (not only static snapshots); (2) comparison geometry in persistence space, 
enabling tactical fingerprinting—discriminating between tactical systems via landscape 
distances; (3) empirical distributional theory on topological invariants at championship 
scale, supporting hypothesis tests against match-level covariates. These contributions 
advance the mathematical foundations of applied topology directly. Computational advances 
in TDA libraries (Ripser, GUDHI) now enable full-season multi-scale analysis; high-quality 
tracking data (10–25 Hz) from professional football provides the ideal testbed for rigorous 
validation. Industry partnerships with championship clubs demonstrate real demand for 
systematic spatial analysis tools.
```

**Word count:** 170 words  
**Changes:**
- ✅ Opens with research novelty: "foundational open questions in computational topology"
- ✅ Lists three explicit methodological contributions: landscape dynamics, fingerprinting, empirical distributions
- ✅ Focuses on theoretical advance, not computational convenience
- ✅ Positions football as validation testbed, not application
- ✅ Includes computational/data/partnership context but doesn't lead with it
- ✅ Names the three contributions Paul wants to see

**Paul's concerns addressed:** ✅ Theoretical novelty, ✅ Specific contributions, ✅ Professional framing, ✅ Testbed clarified

---

## PROBLEM 5: TEAM STRUCTURE UPFRONT

### BEFORE (Team buried mid-document)

```
[No upfront team description. Team details scattered throughout document or mentioned 
vaguely mid-Approach section.]
```

**Issue:** Reviewers don't immediately know who's doing the work, for how long, or in what roles.

---

### AFTER (Team upfront at start of Approach section)

```
Project Structure and Team

This 12-month project involves: (i) the Principal Investigator (PI, 0.2 FTE), responsible 
for framework development, analysis oversight, and publication; (ii) two Co-Investigators 
(combined 0.25 FTE) contributing statistical expertise and ethical safeguarding; (iii) a 
Research Associate (0.8 FTE, 9 months, Months 2–10), responsible for data pipeline 
implementation, full-season analysis, and landscape methods development; (iv) partnership 
with Swansea City AFC and StatsBomb, providing secured access to Championship tracking 
data and formation labels. The project is structured around four integrated Objectives 
(three research objectives + one strategic output).
```

**Word count:** 95 words (new addition)  
**Changes:**
- ✅ Appears immediately at start of Approach section
- ✅ States clearly: who (PI, Co-Is, RA), what FTE (0.2, 0.25, 0.8), what timeline (9 months, Months 2–10)
- ✅ Names roles explicitly (framework development, oversight, publication; statistical expertise; pipeline/analysis; partnerships)
- ✅ Reviewers immediately understand team capacity

**Paul's concerns addressed:** ✅ Transparency, ✅ Clarity on capacity, ✅ Professional structure, ✅ Upfront commitment

---

## PROBLEM 6: SELF-CONGRATULATORY TONE

### BEFORE (Problem phrases)

Examples Paul flagged throughout the document:

```
"This lean structure ensures efficient resource use while maintaining rigor."
→ PROBLEM: Claims "lean" and "efficient" without evidence; "maintaining rigor" is defensive

"Combined infrastructure, partnership networks, institutional support, and strategic team 
structure create optimal conditions for achieving all four objectives within 12-month 
timeline."
→ PROBLEM: Superlatives ("optimal"); lets reviewers decide if conditions are adequate

"The framework has pioneering applications to autonomous systems and crowd safety."
→ PROBLEM: "Pioneering" is superlative; overstates scope

"Our strong track record in computational topology..."
→ PROBLEM: "Strong" is self-promotional; let outputs speak for themselves
```

---

### AFTER (Direct, factual language)

```
[Delete the entire phrase. Replace if needed with:]

"The project timeline spans four integrated objectives with secured data partnerships 
and institutional computational resources."
→ BETTER: States facts without self-promotion

[Or simply delete and let the preceding sentences stand alone.]

"The framework is transferable to other bounded competitive multi-agent systems with 
domain-validated interaction scales. Applications to autonomous systems, ecological 
monitoring, and crowd safety represent future directions beyond the scope of this 
12-month project."
→ BETTER: Acknowledges potential without claiming it or being defensive

[Delete: "Our strong track record"]
[Replace with: "The team has delivered [specific, cited output]"]
→ BETTER: Evidence-based, not promotional
```

**Pattern:**
- ❌ Avoid: "ensure," "optimal," "pioneering," "strategic," "strong," "world-leading"
- ✅ Use: "The framework," "The project," "The team has," "Risk is mitigated by..."

**Paul's concerns addressed:** ✅ Professional tone, ✅ Factual not promotional, ✅ Confidence without overselling

---

## SUMMARY: CHANGES AT A GLANCE

| Problem | Old Length | New Length | Word Change | Key Change |
|---------|-----------|-----------|-------------|-----------|
| 1. Novelty | 100 | 370 | +270 | Validation numbers added; "firstness" tightened; scope moved to future |
| 2. Pathway | 80 | 130 | +50 | Four objectives listed; Standard Grant scope explicit |
| 3. Vision | 60 | 120 | +60 | Grounded in football; removes abstract speculation |
| 4. Timeliness | 35 | 170 | +135 | Three contributions listed; reframes to theory not libraries |
| 5. Team | 0 (missing) | 95 (new) | +95 | Upfront statement; clarity on FTE and timeline |
| 6. Tone | varies | varies | –50 | Self-congratulatory language removed throughout |

---

## IMPACT: BEFORE vs. AFTER

### Before: What Paul saw

> "This document is vague about novelty, overpromises broader applications, doesn't explain why now matters, buries the team, and uses promotional language. Scope boundaries aren't clear. I can't assess feasibility."

### After: What Paul sees

> "This research scales a validated framework from 10 matches to 540 matches. I see the exact validation numbers, the three methodological contributions, the clear team structure, the concrete timeline. Standard Grant is explicitly separate. This is solid, focused work."

---

## CONFIDENCE CHECK

After seeing these before/after comparisons:

- ✅ Do the changes feel substantive and defensible?
- ✅ Are the validation numbers now visible (previously hidden)?
- ✅ Is the scope boundary clear (football this grant, broader domains Standard Grant)?
- ✅ Is the team capacity transparent (0.2 PI + 0.8 RA for 9 months)?
- ✅ Does the tone feel professional, not promotional?

If you answered YES to all, you're ready to integrate these changes into your document.

---

## Next Step

Open `/home/claude/STEP_BY_STEP_IMPLEMENTATION.md` and follow the checklist sequentially.

Each step tells you exactly what to search for, what to delete, and what to paste.

You've got this! 💪
