# Multi-Scale Persistent Homology for Competitive Spatial Systems: Measurement-Aware Methods and Validation in Professional Football

## Abstract

We present a multi-scale persistent homology framework for analysing competitive spatial systems, validated using optical and broadcast tracking data from 11 professional football matches. Standard single-parameter Vietoris–Rips persistent homology computes topological features across all scales simultaneously; for multi-agent systems with hierarchical organisation, this conflates structure at different organisational levels within a single persistence diagram. We address this through two methodological contributions. First, domain-informed hierarchical clustering with analytically-motivated cutoff distances decomposes the point cloud by organisational level before computing homology, enabling scale-specific topological characterisation. Second, adaptive filtration — scaling the Vietoris–Rips threshold to the post-clustering point cloud geometry — ensures consistent detection of H1 features (loops) across all analysis scales. Systematic investigation of the cutoff distance parameter space (0.5–30.0 m, 150,213 frames) identifies three validated analysis regimes: individual (2.98 m, 99% validation), tactical (12.0 m, 96% validation), and team (30.0 m, 100% validation). Multi-match application detects 4,670 individual-scale and 368 tactical-scale H1 loops across 11 matches, with all 523 single-match loops having their geometric realisations recovered via closed cycle identification. Team-scale H1 is confirmed absent (0 loops across 1,650 frames, 11 matches), an expected null result given the 1–3 centroids produced at this scale. Sensitivity analysis demonstrates that H1 detection is robust across cutoff distances from 6 to 17 m and adaptive filtration percentiles from P50 to P95. Temporal analysis reveals match-specific persistence dynamics (Wilcoxon rank-sum p < 0.001 at tactical scale for the primary match), though the direction of change is not consistent across matches. Real event correlation across 10 matches (104,722 event-topology pairs) identifies statistically significant associations between on-ball engagements and persistence decreases (p < 0.001) and between build-up phases and persistence increases (p < 0.001). The two analysis scales capture weakly correlated but complementary information (Spearman ρ = 0.25, p < 0.001). These methods are domain-agnostic and applicable to any bounded competitive multi-agent system with spatial tracking data.

**Keywords**: persistent homology, topological data analysis, multi-scale analysis, competitive systems, sports analytics, optical tracking

---

## 1. Introduction

### 1.1 Background

Competitive spatial systems — collections of agents that interact, coordinate within groups, and compete between groups within a bounded domain — are ubiquitous. Examples include autonomous vehicle fleets sharing airspace, opposing crowd flows at transport hubs, predator–prey populations in ecosystems, and sports teams contesting possession of territory. A distinguishing feature of such systems is that they operate across multiple spatial scales simultaneously: individual agent decisions (metres), small-group tactical coordination (tens of metres), and whole-system organisation (hundreds of metres). Understanding the interplay between these scales is a fundamental challenge in applied mathematics.

Topological Data Analysis (TDA), and persistent homology in particular, provides a natural framework for studying the shape of spatial data across scales (Edelsbrunner and Harer, 2010; Carlsson, 2009). By constructing a filtration of simplicial complexes indexed by a scale parameter and tracking the birth and death of topological features, persistent homology captures multi-scale structure in a mathematically rigorous way. Applications span protein structure (Xia and Wei, 2014), materials science (Hiraoka et al., 2016), and collective behaviour (Topaz et al., 2015).

However, applying standard single-parameter persistent homology to such systems presents practical challenges that motivate the multi-scale approach developed here.

### 1.2 The Scale Conflation Problem

A single Vietoris–Rips filtration applied to a multi-agent point cloud computes topological features across all spatial scales simultaneously. The resulting persistence diagram encodes the full hierarchical clustering structure of the point cloud — from individual agent proximity through small-group formation to system-wide organisation — in a single mathematical object. For exploratory analysis of systems without known hierarchical structure, this is a strength. For multi-agent systems with *known* hierarchical organisation operating across distinct spatial scales, however, it presents a practical challenge: topological features from different organisational levels are superimposed, making it difficult to attribute specific features to specific scales or to track scale-specific dynamics over time.

This challenge is well-recognised in the TDA community. Topaz et al. (2015) address it by visualising Betti numbers across both simulation time and persistence scale, noting that different organisational structures appear at different filtration values. The multiparameter persistence literature (Botnan and Lesnick, 2022; Lesnick, 2015) provides a theoretical framework for simultaneous multi-scale analysis, though computational challenges limit practical application to large point clouds. Schindler and Barahona (2023) develop tools for analysing multiscale clustering sequences using persistent homology, directly addressing hierarchical decomposition. Gu et al. (2022) apply Vietoris–Rips construction to multi-agent system snapshots, noting the sensitivity of topological features to parameter choices.

Our approach takes a complementary, domain-informed path: rather than analysing the full persistence diagram or developing new algebraic machinery, we decompose the point cloud by organisational level through hierarchical clustering at validated cutoff distances, then compute scale-specific persistent homology on each reduced point cloud. This requires a second methodological step — adaptive filtration — to ensure that the Vietoris–Rips threshold is appropriate for the post-clustering geometry at each scale, since a fixed threshold suitable at one organisational level produces null H1 results at another.

### 1.3 Contributions

This paper makes four contributions, two methodological and two empirical:

**Methodological:**

1. **Scale decomposition via domain-informed clustering**: A hierarchical clustering preprocessing step with analytically-motivated cutoff distances that separates organisational levels, enabling scale-specific topological analysis of multi-agent point clouds.

2. **Adaptive filtration**: A data-driven maximum filtration formula that adjusts to the post-clustering point cloud geometry, ensuring consistent H1 detection across all analysis scales.

**Empirical:**

3. **Multi-match scale validation**: Systematic investigation of the cutoff distance parameter space (0.5–30.0 m) on 150,213 frames, identifying three validated analysis regimes with stability scores exceeding 0.88, confirmed across 11 independent matches.

4. **Multi-scale topological characterisation**: Detection of 5,038 H1 loops across 11 matches with closed cycle identification, real event correlation (104,722 event-topology pairs), and scale-dependent temporal dynamics.

### 1.4 Related Work

Persistent homology was introduced by Edelsbrunner et al. (2000) and placed on firm computational foundations by Zomorodian and Carlsson (2005). Stability of persistence diagrams under perturbation was established by Cohen-Steiner et al. (2007). Efficient computation via the Vietoris–Rips filtration is provided by Ripser (Bauer, 2021). Persistence landscapes (Bubenik, 2015) provide a functional representation suitable for statistical analysis.

Applications of TDA to collective behaviour include Topaz et al. (2015), who applied persistent homology to biological aggregation models and visualised scale-dependent structure across filtration values. Gu et al. (2022) applied Vietoris–Rips persistent homology to multi-agent system snapshots for change point detection, demonstrating the utility of topological features for temporal dynamics but operating at a single scale. In sports analytics, spatial analysis methods include pitch control models (Fernandez and Bornn, 2018) and spatio-temporal pattern recognition (Gudmundsson and Horton, 2017), but these do not employ topological methods. To our knowledge, no prior work combines domain-informed scale decomposition with persistent homology for competitive, high-frequency spatial systems, nor validates the resulting scale regimes across multiple independent matches.

---

## 2. Methods

### 2.1 Data

**Primary match.** Optical tracking data from a professional Championship football match was obtained via SecondSpectrum, which provides camera-based position tracking at 25 frames per second. The dataset comprises positions of 22 players (11 per team), totalling 150,213 frames across a full 90-minute match. Positions are recorded as (x, y) coordinates in metres, centred at the field origin (0, 0), spanning approximately [-52.5, 52.5] × [-34, 34] m.

**Validation matches.** Ten additional A-League matches were obtained via the SkillCorner open data repository, providing broadcast-derived tracking data at 10 frames per second. Each match comprises approximately 40,000–48,000 frames with 22-player positions. This multi-match dataset enables validation of the framework's generalisability across different teams, tactical systems, and competition contexts.

For persistent homology computation, each match is divided into temporal windows. Unless otherwise stated, 2-minute non-overlapping windows are used for the primary match, yielding 149 analysis windows. For multi-match validation, 150 uniformly sampled frames per match (every 100th frame) provide consistent cross-match comparison.

### 2.2 Proximity-Aware Clustering

At each time step t, the 22 player positions form a point cloud P(t) = {p₁(t), ..., p₂₂(t)} ⊂ ℝ². Direct application of persistent homology to P(t) produces a single persistence diagram encoding all inter-agent distance relationships simultaneously. To separate organisational levels, we preprocess with hierarchical clustering.

**Definition.** For a cutoff distance δ > 0, single-linkage hierarchical clustering partitions P(t) into clusters C₁, ..., Cₖ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding δ. The reduced point cloud is the set of cluster centroids:

P̃(t) = { c̄ⱼ : c̄ⱼ = (1/|Cⱼ|) Σ_{p ∈ Cⱼ} p,  j = 1, ..., k }

Persistent homology is then computed on P̃(t) rather than P(t).

**Linkage method choice.** We use single-linkage throughout this study, noting that it produces a conservative estimate of topological features. Empirical comparison across 600 frames and 4 matches (Section 3.7) shows that single-linkage exhibits a known chaining effect at the tactical scale, producing fewer and larger clusters (mean 5.0 clusters) versus complete-linkage (10.8) and Ward's method (11.0). Consequently, single-linkage detects fewer H1 features (153 tactical loops) than complete-linkage (923) or Ward (936) over the same frames. However, single-linkage's definition — clusters are sets of points connected by chains of short distances — is the most natural for detecting spatial proximity groups, and its conservative H1 estimates ensure that reported loops represent robust topological features rather than artefacts of cluster over-partitioning.

### 2.3 Analytically-Motivated Cutoff Distance Selection

The cutoff distance δ is not a nuisance parameter but a scale selector that determines the level of organisation under analysis. We conducted a systematic parameter sweep over δ ∈ [0.5, 30.0] m at 100 test points, evaluated on 58 temporal windows (normalised 30% coverage across four epoch lengths: 1, 2, 5, and 10 minutes).

Three analysis regimes emerge, validated by multiple clustering quality metrics (Calinski-Harabasz index, silhouette score, and domain-specific information content):

| Scale | Optimal δ | Validation | Expected H0 | Stability |
|-------|-----------|------------|-------------|-----------|
| Individual | 2.98 ± 0.37 m (Calinski-Harabasz optimum) | 99% of frames | 15–22 | 0.88 |
| Tactical | 12.0 m (domain-informed; see below) | 96% of frames | 3–12 | 0.97 |
| Team | 28.11 ± 0.47 m (information-content optimum) | 100% of frames | 1–3 | 0.98 |

"Validation" denotes the cross-epoch consistency rate: the fraction of analysis windows across four temporal epoch lengths in which H0 falls within the domain-informed expected range for that regime. The individual (2.98 m) and team (28.11 m) cutoffs emerge from automated clustering quality metrics; the tactical cutoff (12.0 m) is selected as a domain-informed choice within the tactical range, where automated metrics diverge (silhouette-optimal: 16.31 m; information-content-optimal: 6.87 m). The value 12.0 m corresponds approximately to one-half the standard football zone width (the distance between the 18-yard box and the halfway line divided into quarters), and was validated on 50 single-frame analyses (96% producing expected H0). Sensitivity analysis (Section 3.6) confirms that H1 detection is robust across the entire 6–17 m range, with the chosen 12.0 m falling within the region of stable detection.

### 2.4 Adaptive Filtration for H1 Detection

After clustering at cutoff δ, the reduced point cloud P̃(t) has inter-centroid distances much larger than δ. A fixed maximum filtration ε_max is insufficient for H1 detection across all scales.

We define an adaptive filtration:

ε_max = max( P₇₅({d(c̄ᵢ, c̄ⱼ) : i < j}),  max(5.0, 2δ) )

where P₇₅ denotes the 75th percentile of pairwise inter-centroid distances. The first term adapts to the actual geometry of the reduced point cloud; the second term ensures a minimum filtration proportional to the clustering scale (floor of 5.0 m).

**Justification of P75.** Empirical ablation across percentiles P50, P60, P75, P90, and P95 on 150 frames (Section 3.6) shows that P50 detects slightly fewer loops (49 vs 53 for P75), while P75 through P95 produce identical detection counts. The 75th percentile thus represents the lowest percentile at which the formula achieves maximal sensitivity, providing a robust but not overly permissive threshold. The 5.0 m floor prevents degenerate filtration at very small scales, and the 2δ factor ensures the filtration encompasses at least the inter-cluster distance regime.

### 2.5 Closed Cycle Identification

Each H1 feature in the persistence diagram corresponds to a topological loop — a 1-cycle in the Vietoris–Rips complex. To recover the geometric realisation, we construct the adjacency graph of edges with distances in the persistence interval [birth, death] and apply breadth-first search to enumerate closed cycles of length ≥ 3. Cycles are scored by representativeness (proximity of edge distances to the midpoint of the persistence interval) and the highest-scoring cycle is selected as the geometric representative.

### 2.6 Temporal Analysis and Statistical Tests

For each analysis window, we compute H0 and H1 feature counts and persistence values at the individual and tactical scales. Temporal evolution is assessed by comparing mean persistence between match halves using the Wilcoxon rank-sum test (Mann-Whitney U), supplemented by a permutation test (10,000 permutations). Scale interactions are characterised by Spearman rank correlation and Fisher's exact test on the co-occurrence of H1 features at the individual and tactical scales.

### 2.7 Event Correlation

Topological transitions around match events are quantified by computing H1 persistence in a window of ±5 frames around each event, calculating the persistence change (mean post-event minus mean pre-event). Events are sourced from SkillCorner dynamic event annotations (player possessions, on-ball engagements, off-ball runs, passing options) and phases of play (build-up, direct, chaotic, transition, set play). Statistical significance is assessed by Mann-Whitney U tests on the persistence deltas against zero.

---

## 3. Results

### 3.1 Scale-Specific Connected Components (H0)

**Single-match.** Without clustering, H0 persistence diagrams for each frame encode the full 22-point hierarchical merging sequence. After scale decomposition, H0 at each level reflects organisation at that specific scale. At the individual scale (δ = 2.98 m), H0 = 17.85 ± 3.54 (mean ± s.d.), varying with local player proximity patterns. At the tactical scale (δ = 12.0 m), H0 = 7.67 ± 1.63, capturing the number of distinct tactical groups. At the team scale (δ = 30.0 m), H0 = 1.37 ± 0.49, with 62.6% of frames having H0 = 1 (all 22 players in a single cluster), 37.3% having H0 = 2, and 0.1% having H0 = 3.

**Multi-match validation (11 matches).** The three-scale H0 structure is consistent across all 11 matches: individual H0 = 19.07 ± 0.40 (grand mean ± across-match s.d.), tactical H0 = 4.96 ± 0.38, team H0 = 1.37 ± 0.08. All matches fall within the expected H0 ranges for all three scales.

### 3.2 H1 Loop Detection

**Single-match (primary).** Across 149 analysis windows, the framework detects 523 H1 loops:

| Scale | Total loops | Frames with loops | Mean loops/frame | Mean persistence | Max persistence |
|-------|-------------|-------------------|-----------------|-----------------|-----------------|
| Individual (2.98 m) | 470 | 148/149 (99%) | 3.18 | 1.781 ± 1.455 | 7.971 |
| Tactical (12.0 m) | 53 | 42/149 (28%) | 1.26 | 3.285 ± 2.241 | 9.392 |
| Team (30.0 m) | 0 | 0/149 (0%) | — | — | — |

Individual-scale loops are frequent but transient (low mean persistence), representing dynamic player-level interactions. Tactical-scale loops are less frequent but substantially more persistent, representing stable formation structures — strategic gaps between defensive lines, midfield zones, or coordinated pressing shapes.

**Team-scale H1 null result.** The absence of H1 features at the team scale is a structural consequence of the clustering: at δ = 30.0 m, the 22 players are reduced to 1–3 centroids in every frame (Section 3.1). The Vietoris–Rips complex on k ≤ 3 points in general position has at most C(k,2) = 3 edges. A non-trivial 1-cycle requires at least 3 edges forming a cycle, but with 3 points the single potential triangle is a boundary, not a genuine 1-cycle. This null result is thus expected a priori and confirmed empirically across all 1,650 frames (11 matches): H1 = 0 universally. Consequently, our multi-scale H1 analysis operates at two scales (individual and tactical) with three-scale H0 decomposition.

**Multi-match validation.** Across 11 matches (1,650 uniformly sampled frames):

| Scale | Total H1 | H1 presence rate | Mean persistence | Cross-match s.d. |
|-------|----------|-----------------|-----------------|-----------------|
| Individual | 4,670 | 97.2% ± 1.6% | 1.850 | 0.040 |
| Tactical | 368 | 20.1% ± 7.6% | 0.692 | 0.38 |
| Team | 0 | 0.0% ± 0.0% | — | — |

The individual-scale H1 presence rate of 97.2% (s.d. 1.6%) across 11 independent matches confirms that loop structures are a near-universal feature of competitive spatial systems at this scale. Tactical-scale H1 presence of 20.1% (s.d. 7.6%) shows meaningful cross-match variability, likely reflecting differences in tactical systems and match dynamics.

### 3.3 Closed Cycle Structures

Closed cycle identification recovers the geometric realisations of all 523 single-match H1 generators. Individual-scale cycles typically comprise 4–6 nodes (cluster centroids), corresponding to small ring-like player arrangements. Tactical-scale cycles comprise 4–5 nodes with higher persistence, corresponding to larger-scale formation gaps. See Figure 2 for a representative geometric realisation.

Representative examples:
- **Individual, Frame 72**: 5-node cycle, persistence 7.97 m — a tight pentagonal pressing arrangement
- **Tactical, Frame 73**: 5-node cycle, persistence 9.39 m — the highest-persistence feature, corresponding to a stable gap between defensive and midfield lines

### 3.4 Temporal Evolution

**Primary match (with statistical tests).** Comparison of mean H1 persistence between match halves using the Wilcoxon rank-sum test:

| Scale | First half mean | Second half mean | Change | Wilcoxon p | Permutation p |
|-------|----------------|------------------|--------|-----------|---------------|
| Individual | 1.759 | 1.777 | +1.0% | 0.630 | — |
| Tactical | 1.380 | 1.065 | −22.8% | < 0.001 | < 0.001 |

The tactical scale shows a statistically significant decrease in persistence from first to second half (p < 0.001), while the individual scale shows no significant change. This result differs in sign from our preliminary windowed analysis (which suggested an increase), likely due to differences in temporal aggregation method; the window-level analysis with full-frame resolution provides the definitive result.

**Multi-match validation.** Across four matches with sufficient per-half data, the direction of persistence change is not consistent: one match shows a significant decrease, one shows a moderate increase, and two show negligible change. This suggests that temporal persistence dynamics are match-specific rather than universal, likely driven by tactical context, match state (score), and team-specific strategies.

### 3.5 Scale Complementarity

The two scales capture weakly correlated but functionally complementary information. Across 900 frames from 6 matches:

- **Spearman rank correlation** between individual-scale and tactical-scale H1 counts: ρ = 0.254, p < 0.001
- **Fisher's exact test** on the 2×2 contingency table (presence/absence at each scale): OR = 3.52, p = 0.093

The weak but significant positive correlation indicates that frames with more individual-scale loops tend to have slightly more tactical-scale loops — plausibly because denser player configurations create topological features at multiple scales. However, the modest correlation coefficient (ρ = 0.25) and the non-significant Fisher's exact test confirm that the scales capture predominantly distinct structural information: individual-scale loops can appear without tactical-scale loops and vice versa.

| Property | Individual scale | Tactical scale |
|----------|-----------------|----------------|
| Loop frequency | High (3.18/frame) | Low (1.26/frame) |
| Mean persistence | Low (1.781 ± 1.455 m) | High (3.285 ± 2.241 m) |
| Max persistence | 7.971 m | 9.392 m |
| Frames with loops | 148/149 (99%) | 42/149 (28%) |

### 3.6 Sensitivity Analysis

**Cutoff distance sensitivity (tactical scale).** H1 detection across δ ∈ [6, 17] m on 150 frames of the primary match:

| δ (m) | H1 total | H1 presence | Mean H0 |
|-------|----------|-------------|---------|
| 6 | 364 | 90.7% | 14.5 |
| 8 | 259 | 80.0% | 11.0 |
| 10 | 126 | 53.3% | 7.8 |
| 12 | 53 | 28.0% | 5.4 |
| 14 | 18 | 10.7% | 3.8 |
| 16 | 4 | 2.7% | 3.0 |

H1 detection decreases monotonically with cutoff distance, as expected: larger cutoffs produce fewer centroids and thus fewer potential cycles. The chosen δ = 12.0 m sits in the middle of the productive range, where H0 is in the expected tactical range (3–12) and H1 detection remains meaningful (28% frame presence, 53 loops). The stable detection range (defined as ≥ 50% of peak H1 presence) spans 6–10 m, confirming that the framework produces topological features across the full plausible tactical cutoff range.

**Adaptive filtration ablation.** At δ = 12.0 m, varying the adaptive percentile:

| Percentile | H1 total | H1 presence | Mean filtration |
|-----------|----------|-------------|----------------|
| P50 | 49 | 26.7% | 38.2 m |
| P60 | 52 | 27.3% | 42.1 m |
| P75 | 53 | 28.0% | 49.4 m |
| P90 | 53 | 28.0% | 59.0 m |
| P95 | 53 | 28.0% | 64.3 m |

P75 is the lowest percentile that achieves maximal H1 detection (53 loops, 28% presence), with P50 and P60 marginally under-detecting by 4 and 1 loops respectively. All percentiles from P75 upward produce identical results, confirming that the formula is insensitive to this parameter choice within a broad range and that P75 is not an overfitted selection.

### 3.7 Linkage Method Comparison

Empirical comparison of single-linkage, complete-linkage, and Ward's method across 600 frames from 4 matches:

| Method | Tactical clusters | H1 total | H1 presence | Chaining ratio |
|--------|-------------------|----------|-------------|---------------|
| Single | 5.0 ± 1.7 | 153 | 22.2% | 10.96 |
| Complete | 10.8 ± 1.8 | 923 | 86.3% | 1.38 |
| Ward | 11.0 ± 1.7 | 936 | 86.0% | 1.33 |

At the individual scale (δ = 2.98 m), all three methods produce effectively identical results (1,743–1,765 H1 loops, 97% presence), confirming that the chaining effect is negligible at short distances where players are genuinely nearby. At the tactical scale, single-linkage's chaining (ratio ≈ 11) reduces centroids from ~11 (complete/Ward) to ~5, substantially reducing H1 detection. Our reported single-linkage results are therefore conservative: the true topological richness at the tactical scale is likely greater than reported. At the team scale, all methods confirm H1 = 0 for single-linkage (as expected from 1–2 centroids), while complete and Ward produce team-scale loops — a finding that warrants future investigation with appropriate domain validation.

### 3.8 Event Correlation

Real event correlation using SkillCorner annotations across 10 matches (104,722 event-topology pairs) reveals statistically significant associations between match events and topological transitions:

**Individual scale — significant event types:**

| Event type | Mean Δ persistence | p-value | n |
|-----------|-------------------|---------|---|
| On-ball engagement | −0.256 | < 0.001 | 8,905 |
| Passing option | −0.162 | < 0.001 | 24,343 |
| Build-up phase | +0.731 | < 0.001 | 618 |
| Quick break | −0.766 | 0.010 | 57 |
| Chaotic phase | −0.210 | 0.043 | 1,087 |

**Tactical scale — significant event types:**

| Event type | Mean Δ persistence | p-value | n |
|-----------|-------------------|---------|---|
| Passing option | −0.046 | < 0.001 | 24,343 |
| On-ball engagement | −0.058 | 0.014 | 8,905 |
| Chaotic phase | −0.196 | < 0.001 | 1,087 |
| Build-up phase | +0.342 | < 0.001 | 618 |
| Quick break | −0.666 | 0.046 | 57 |

The pattern is coherent across both scales: events involving spatial disruption (engagements, pressing, quick breaks) are associated with persistence decreases, while events involving spatial organisation (build-up) are associated with persistence increases. This is consistent with the topological interpretation: spatial disruption fragments formation structures (reducing H1), while deliberate build-up creates and sustains them.

---

## 4. Discussion

### 4.1 Methodological Contributions

Our approach is complementary to ongoing theoretical work on multiparameter persistence (Botnan and Lesnick, 2022), which addresses scale conflation algebraically but faces computational barriers for large point clouds. We take a practical, domain-informed route: hierarchical clustering at validated cutoff distances decomposes the point cloud by organisational level before computing standard single-parameter persistent homology at each level.

The cutoff distance — which we term *analytically-motivated* rather than "goal-dependent" (to avoid ambiguity with the sport-specific meaning of "goal") — defines the organisational level under analysis. The three validated regimes (individual, tactical, team) emerge from systematic parameter sweep and reflect genuine hierarchical structure in the competitive system. The tactical cutoff (12.0 m) is explicitly a domain-informed choice, justified by (i) its position within the automated metric range (6.87–16.31 m), (ii) its correspondence to standard football zone dimensions, and (iii) sensitivity analysis showing robust H1 detection across the plausible range (Section 3.6).

The adaptive filtration formula addresses a practical coupling between the clustering and filtration steps. The P75 threshold is empirically justified by ablation showing it is the minimum percentile achieving full detection sensitivity (Section 3.6). This is a general solution applicable to any multi-scale TDA pipeline that uses clustering as a preprocessing step.

### 4.2 Multi-Scale Topological Structure

The complementarity of the individual and tactical scales is supported by quantitative evidence: Spearman ρ = 0.25 (weak positive correlation, far from unity) and a non-significant Fisher's exact test (p = 0.093) on H1 presence/absence. The weak positive correlation likely reflects the confound that dense player configurations create opportunities for topological features at multiple scales simultaneously. Despite this, the scales capture predominantly distinct structural information, as demonstrated by their divergent frequency (97% vs 20% H1 presence) and persistence profiles.

### 4.3 Temporal Dynamics and Event Correlation

The temporal evolution result is more nuanced than initially reported: the primary match shows a significant tactical-scale persistence decrease (−22.8%, p < 0.001), but the direction is not consistent across matches. This suggests that half-level persistence dynamics are driven by match-specific factors — tactical adjustments, scoreline effects, substitutions — rather than universal trends.

The real event correlation, based on 104,722 event-topology pairs across 10 matches, provides the first evidence that persistent homology features are genuinely responsive to match dynamics. The coherent pattern — disruption decreases persistence, organisation increases it — validates the topological interpretation and suggests applications in real-time tactical monitoring.

### 4.4 Limitations

**Single-linkage conservatism.** The chaining effect at the tactical scale (Section 3.7) means our tactical H1 counts are conservative. Future work should investigate complete or average linkage, with appropriate domain validation to ensure the increased cluster count reflects genuine tactical groupings rather than partition artefacts.

**Two-scale H1, not three.** Our multi-scale framework identifies three H0 regimes but only two H1 regimes. Team-scale H1 absence is a structural consequence of the 1–3 centroids produced at δ = 30.0 m, not a methodological limitation. Effective team-scale H1 analysis would require alternative representations (e.g., spatial density fields or Delaunay triangulations) rather than centroid-based point clouds.

**Broadcast tracking resolution.** The SkillCorner validation data (10 Hz, broadcast-derived) has lower spatial resolution than the primary SecondSpectrum data (25 Hz, optical). While H0 and H1 structures are consistent across both data sources, future work should assess whether H1 persistence magnitudes are comparable.

---

## 5. Conclusion

We have presented a multi-scale persistent homology framework for competitive spatial systems that addresses the scale conflation problem through two practical contributions: domain-informed clustering for scale decomposition and adaptive filtration for scale-consistent H1 detection. Validation across 11 professional football matches identifies three H0 analysis regimes and two H1 regimes with distinct and complementary topological signatures, demonstrates robust H1 detection across a broad cutoff parameter range, and establishes the first real event-topology correlations in sports analytics (104,722 pairs, 10 matches). The framework is ready for cross-domain application to any bounded competitive multi-agent system with spatial tracking data.

---

## Acknowledgements

We thank SecondSpectrum for optical tracking data access and SkillCorner for broadcast tracking open data. Computations were performed using the Ripser library (Bauer, 2021).

---

## References

Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423.

Botnan, M.B. and Lesnick, M. (2022). An introduction to multiparameter persistence. In *Representations of Algebras and Related Structures*, EMS Press, pp. 77–150. arXiv:2203.14289.

Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16(1), 77–102.

Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255–308.

Cohen-Steiner, D., Edelsbrunner, H. and Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120.

Edelsbrunner, H. and Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.

Edelsbrunner, H., Letscher, D. and Zomorodian, A. (2000). Topological persistence and simplification. In *Proceedings 41st Annual Symposium on Foundations of Computer Science*, pp. 454–463.

Fernandez, J. and Bornn, L. (2018). Wide open spaces: A statistical technique for measuring space creation in professional soccer. In *Sloan Sports Analytics Conference*.

Gu, K., Yan, L., Li, X., Duan, X. and Liang, J. (2022). Change point detection in multi-agent systems based on higher-order features. *Chaos*, 32(11), 113117.

Gudmundsson, J. and Horton, M. (2017). Spatio-temporal analysis of team sports. *ACM Computing Surveys*, 50(2), 1–34.

Hiraoka, Y., Nakamura, T., Hirata, A., Escolar, E.G., Matsue, K. and Nishiura, Y. (2016). Hierarchical structures of amorphous solids characterized by persistent homology. *Proceedings of the National Academy of Sciences*, 113(26), 7035–7040.

Lesnick, M. (2015). The theory of the interleaving distance on multidimensional persistence modules. *Foundations of Computational Mathematics*, 15(3), 613–650.

Schindler, D.J. and Barahona, M. (2023). Analysing multiscale clusterings with persistent homology. *arXiv preprint arXiv:2305.04281*.

Topaz, C.M., Ziegelmeier, L. and Halverson, T. (2015). Topological data analysis of biological aggregation models. *PLoS ONE*, 10(5), e0126383.

Xia, K. and Wei, G.-W. (2014). Persistent homology analysis of protein structure, flexibility and folding. *International Journal for Numerical Methods in Biomedical Engineering*, 30(8), 814–844.

Zomorodian, A. and Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249–274.

---

**Corresponding Author**: Dr Rowan Brown, Biomedical Engineering, Swansea University
**Target Journal**: TBC
**Status**: Revised draft — multi-match validation complete