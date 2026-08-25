# Multi-Scale Persistent Homology for Competitive Spatial Systems

*Measurement-Aware Methods and Validation in Professional Football*

<!-- LaTeX (`main.tex`) uses Vancouver referencing: numbered citations in order of appearance. This Markdown uses author–year for readability; for final numbering, compile the LaTeX and follow the PDF. -->

## Abstract

Standard single-parameter Vietoris–Rips persistent homology on multi-agent point clouds conflates topological features from distinct organisational levels into a single diagram. We present a multi-scale framework addressing this through two methodological contributions: domain-informed hierarchical clustering with validated cutoff distances, decomposing the point cloud by organisational level, and an adaptive Vietoris–Rips filtration scaled to the post-clustering geometry, so that H1 (loop) features are detected consistently across scales. Validation on 10 professional football matches (SkillCorner broadcast tracking, 10 Hz; 43,531 frames for the primary match) identifies three H0 regimes, individual (2.98 m), tactical (12.0 m), and team (30.0 m), with 96–100% cross-epoch validation, and two H1 regimes: individual-scale loops are frequent and transient (97.0% ± 1.5% frame presence), tactical-scale loops are rarer but geometrically persistent (19.3% ± 7.2%); team-scale H1 is absent *a priori* from the clustering. Sensitivity analyses confirm robust tactical H1 detection for primary-match cutoffs δ from 6 m to 14 m (zero by δ = 16 m), insensitivity of headline counts to adaptive percentiles P50–P95, and recovery of geometric cycle representatives for every H1 generator. Across 10 matches (104,722 event–topology pairs) topological change correlates coherently with match dynamics: on-ball engagements (*p* < 0.001) and quick breaks (*p* ≤ 0.046) are associated with persistence decreases, and build-up phases (*p* < 0.001) with increases. The two scales capture weakly correlated but complementary information (Spearman ρ = 0.254). The framework is domain-agnostic and applies to any bounded competitive multi-agent system with spatial tracking data.

**Keywords**: persistent homology, topological data analysis, multi-scale analysis, competitive systems, sports analytics, broadcast tracking

---

## 1. Introduction

### 1.1 Background

Competitive spatial systems, collections of agents that interact, coordinate within groups, and compete between groups within a bounded domain, are ubiquitous. Examples include autonomous vehicle fleets sharing airspace, opposing crowd flows at transport hubs, predator–prey populations in ecosystems, and sports teams contesting possession of territory. A distinguishing feature of such systems is that they operate across multiple spatial scales simultaneously: individual agent decisions (metres), small-group tactical coordination (tens of metres), and whole-system organisation (hundreds of metres). Understanding the interplay between these scales is a fundamental challenge in applied mathematics. Systematic reviews document how wearable and broadcast tracking data now underpin load monitoring and tactical performance analysis in field sports (Cummins et al., 2013; Memmert et al., 2017), motivating geometric summaries of collective positioning.

From a spatial perspective, agents can arrange themselves in ring-like formations that enclose empty space, for example, a pressing trap encircling a player in possession, or a gap between defensive and midfield lines that creates tactical options. Such arrangements have a topological character: they are *loops* in the position data, and their stability over time (measured by persistence) distinguishes deliberate structural organisation from transient clustering. Conventional metrics such as convex hull area, nearest-neighbour distance, or team length and width derived from player positions (Folgado et al., 2014) capture different aspects of spatial dispersion but do not directly quantify this multi-agent loop structure. Persistent homology provides a principled way to detect and measure these formations across scale.

Topological Data Analysis (TDA), and persistent homology in particular, provides a natural framework for studying the shape of spatial data across scales (Edelsbrunner and Harer, 2010; Carlsson, 2009). By constructing a filtration of simplicial complexes indexed by a scale parameter and tracking the birth and death of topological features, persistent homology captures multi-scale structure in a mathematically rigorous way. Applications span protein structure (Xia and Wei, 2014), materials science (Hiraoka et al., 2016), and collective behaviour (Topaz et al., 2015).

However, applying standard single-parameter persistent homology to such systems presents practical challenges that motivate the multi-scale approach developed here.

### 1.2 The Scale Conflation Problem

A single Vietoris–Rips filtration applied to a multi-agent point cloud computes topological features across all spatial scales simultaneously. The resulting persistence diagram encodes the full hierarchical clustering structure of the point cloud, from individual agent proximity through small-group formation to system-wide organisation, in a single mathematical object. For exploratory analysis of systems without known hierarchical structure, this is a strength. For multi-agent systems with *known* hierarchical organisation operating across distinct spatial scales, however, it presents a practical challenge: topological features from different organisational levels are superimposed, making it difficult to attribute specific features to specific scales or to track scale-specific dynamics over time.

This challenge is well-recognised in the TDA community. Topaz et al. (2015) address it by visualising Betti numbers across both simulation time and persistence scale, noting that different organisational structures appear at different filtration values. The multiparameter persistence literature (Botnan and Lesnick, 2022; Lesnick, 2015) provides a theoretical framework for simultaneous multi-scale analysis, though computational challenges limit practical application to large point clouds. Schindler and Barahona (2023) develop tools for analysing multiscale clusterings with persistent homology, directly addressing hierarchical decomposition. Gu et al. (2022) apply Vietoris–Rips construction to multi-agent system snapshots, noting the sensitivity of topological features to parameter choices.

Our approach takes a complementary, domain-informed path: rather than analysing the full persistence diagram or developing new algebraic machinery, we decompose the point cloud by organisational level through hierarchical clustering at validated cutoff distances, then compute scale-specific persistent homology on each reduced point cloud. This requires a second methodological step, adaptive filtration, to ensure that the Vietoris–Rips threshold is appropriate for the post-clustering point cloud geometry at each scale, since a fixed threshold suitable at one organisational level produces null H1 results at another.

### 1.3 Contributions

This paper makes four contributions, two methodological and two empirical:

**Methodological:**

1. **Scale decomposition via domain-informed clustering**: A hierarchical clustering preprocessing step with domain-informed cutoff distances that separates organisational levels, enabling scale-specific topological analysis of multi-agent point clouds.

2. **Adaptive filtration**: A data-driven maximum filtration formula that adjusts to the post-clustering point cloud geometry, ensuring consistent H1 detection across all analysis scales.

**Empirical:**

3. **Multi-match scale validation**: Systematic investigation of the cutoff distance parameter space (0.5–30.0 m) on 43,531 frames, identifying three validated analysis regimes with stability scores of 0.84–1.00, confirmed across 10 independent matches.

4. **Multi-scale topological characterisation**: Detection of 4,515 H1 loops across 10 matches with closed cycle identification, real event correlation (104,722 event-topology pairs), and scale-dependent temporal dynamics.

### 1.4 Related Work

Persistent homology was introduced by Edelsbrunner et al. (2000) and placed on firm computational foundations by Zomorodian and Carlsson (2005). Stability of persistence diagrams under perturbation was established by Cohen-Steiner et al. (2007). Efficient computation via the Vietoris–Rips filtration is provided by Ripser (Bauer, 2021). Persistence landscapes (Bubenik, 2015) provide a functional representation suitable for statistical analysis.

Applications of TDA to collective behaviour include Topaz et al. (2015), who applied persistent homology to biological aggregation models and visualised scale-dependent structure across filtration values. Gu et al. (2022) applied Vietoris–Rips persistent homology to multi-agent system snapshots for change point detection, demonstrating the utility of topological features for temporal dynamics but operating at a single scale. In sports analytics, spatial analysis methods include pitch control models (Fernandez and Bornn, 2018) and spatio-temporal pattern recognition (Gudmundsson and Horton, 2017). Related perspectives model teams as coordinated multi-agent systems (Duarte et al., 2012) and apply network metrics to passing and collective structure (Clemente et al., 2015; Buldú et al., 2019); these approaches complement ours but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines domain-informed scale decomposition with persistent homology for competitive, high-frequency spatial systems, nor validates the resulting scale regimes across multiple independent matches.

---

## 2. Methods

### 2.1 Data

**Primary match.** The principal single-match analysis uses **SkillCorner open data** ([SkillCorner/opendata](https://github.com/SkillCorner/opendata)), match ID **1996435** (Sydney FC vs Adelaide United, A-League 2024/25). Broadcast-derived player tracking is provided at **10 frames per second**; we retain frames with complete 22-player coverage (43,531 frames; approximately 72 minutes of play at this sampling rate). Positions are (x, y) coordinates in metres on a standard pitch model. The same pipeline reproduces cutoff sweeps, regime identification, temporal windows, and sensitivity outputs in `results/primary_skillcorner/` (see `03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py`).

**Validation matches.** Nine additional A-League matches from the SkillCorner repository provide broadcast-derived tracking at 10 frames per second. Together with the primary match, this yields **10** SkillCorner matches for multi-match validation. Each match comprises approximately 40,000–48,000 frames with 22-player positions. This dataset enables validation of the framework's generalisability across different teams, tactical systems, and competition contexts. (An earlier draft used a separate optical-tracking primary match from a commercial provider; figures and statistics in this version are aligned with the SkillCorner open-data cohort unless explicitly labelled otherwise.)

For persistent homology computation, temporal structure is summarised in two ways. Unless otherwise stated, **2-minute non-overlapping windows** are used for the primary match (36 windows for match 1996435 at 10 Hz with complete 22-player coverage), including the half-time comparisons in Section 3.4. **Uniform frame sampling** (every 100th complete frame) gives 150 primary-match frames for scale-specific H1 tabulations, cutoff and filtration sensitivity tables, and linkage comparisons; the same 150-frame rule applies to each validation match unless noted.

### 2.2 Proximity-Aware Clustering

Figure 1 summarises the full analysis pipeline. At each time step t, the 22 player positions form a point cloud P(t) = {p₁(t), ..., p₂₂(t)} ⊂ ℝ². Direct application of persistent homology to P(t) produces a single persistence diagram encoding all inter-agent distance relationships simultaneously. To separate organisational levels, we preprocess with hierarchical clustering.

![Figure 1: Multi-scale TDA analysis pipeline (SkillCorner match 1996435 as primary demonstrator; schematic applies to all 10 matches). Blue band: scale decomposition by single-linkage hierarchical clustering at validated cutoffs δ ∈ {2.98, 12.0, 30.0} m, reducing the 22-player cloud to cluster centroids P̃_δ(t). Amber band: adaptive Vietoris–Rips filtration ε ≤ ε_max per equation (1), with schematic H1 persistence diagram (inset). Downstream: closed-cycle identification and geometric realisation on the pitch.](figures/fig1_pipeline_schematic.png)

**Definition.** For a cutoff distance δ > 0, single-linkage hierarchical clustering partitions P(t) into clusters C₁, ..., Cₖ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding δ. The reduced point cloud is the set of cluster centroids:

P̃(t) = { c̄ⱼ : c̄ⱼ = (1/|Cⱼ|) Σ_{p ∈ Cⱼ} p, j = 1, ..., k }

Persistent homology is then computed on P̃(t) rather than P(t).

**Linkage method choice.** We use single-linkage throughout this study, noting that it produces a conservative estimate of topological features. Empirical comparison across 600 frames and 4 matches (Section 3.7) shows that single-linkage exhibits a known chaining effect at the tactical scale, producing fewer and larger clusters (mean 5.0 clusters) versus complete-linkage (10.8) and Ward's method (11.0). Consequently, single-linkage detects fewer H1 features (153 tactical loops) than complete-linkage (923) or Ward (936) over the same frames. However, single-linkage's definition, clusters are sets of points connected by chains of short distances, is the most natural for detecting spatial proximity groups, and its conservative H1 estimates ensure that reported loops represent robust topological features rather than artefacts of cluster over-partitioning.

**Bilateral decomposition.** In addition to the 22-player analysis described above, we run the full pipeline (clustering at δ = 12.0 m, adaptive Vietoris–Rips filtration) independently on each team's 11-player sub-cloud, using the home/away player labels supplied with the SkillCorner data. This bilateral analysis is the natural use of team identity: the 22-player merge discards the labelling that distinguishes attacking and defending coordination, whereas the 11+11 split treats each team as a separate competitive agent and lets us quantify per-team tactical H1 and the cross-team coupling between the two persistence sequences. Results are reported in Section 3.10.

### 2.3 Domain-Informed Cutoff Distance Selection

The cutoff distance δ is not a nuisance parameter but a scale selector that determines the level of organisation under analysis. We conducted a systematic parameter sweep over δ ∈ [0.5, 30.0] m at 100 test points, evaluated on 58 temporal windows (normalised 30% coverage across four epoch lengths: 1, 2, 5, and 10 minutes).

Three analysis regimes emerge, validated by multiple clustering quality metrics (Calinski-Harabasz index, silhouette score, and domain-specific information content):

| Scale | Optimal δ | Validation | Expected H0 | Stability |
|-------|-----------|------------|-------------|-----------|
| Individual | 2.98 ± 0.37 m (Calinski-Harabasz optimum) | 99% of frames | 15–22 | 0.88 |
| Tactical | 12.0 m (domain-informed; see below) | 96% of frames | 3–12 | 0.97 |
| Team | 30.0 m (information-content optimum) | 100% of frames | 1–2 | 1.00 |

"Validation" denotes the cross-epoch consistency rate: the fraction of analysis windows across four temporal epoch lengths in which H0 falls within the domain-informed expected range for that regime. The individual (2.98 m) and team (30.0 m) cutoffs emerge from automated clustering quality metrics; the tactical cutoff (12.0 m) is selected as a domain-informed choice within the tactical range, where automated metrics diverge (silhouette-optimal: 16.31 m; information-content-optimal: 6.87 m). The value 12.0 m corresponds approximately to one-half the standard football zone width (the distance between the 18-yard box and the halfway line divided into quarters), and was validated on 50 single-frame analyses (96% producing expected H0). Sensitivity analysis (Section 3.6) confirms non-zero tactical H1 on the primary-match grid for δ from 6 m up to 14 m (zero by δ = 16 m on the 150-frame sample), with the chosen 12.0 m in the interior of the non-zero range.

### 2.4 Adaptive Filtration for H1 Detection

After clustering at cutoff δ, the reduced point cloud P̃(t) has inter-centroid distances much larger than δ. A fixed maximum filtration ε_max is insufficient for H1 detection across all scales.

We define an adaptive filtration:

ε_max = max( P₇₅({d(c̄ᵢ, c̄ⱼ) : i < j}), max(5.0, 2δ) )

where P₇₅ denotes the 75th percentile of pairwise inter-centroid distances. The first term adapts to the actual geometry of the reduced point cloud; the second term ensures a minimum filtration proportional to the clustering scale (floor of 5.0 m).

**Justification of P75.** Empirical ablation across percentiles P50, P60, P75, P90, and P95 on 150 frames (Section 3.6) yields identical tactical-scale H1 totals and frame-presence rates for all percentiles tested. We report P75 as a conventional upper-quartile summary of inter-centroid distances; the insensitivity of headline counts to this choice is documented in the adaptive-percentile table (Section 3.6). The 5.0 m floor prevents degenerate filtration at very small scales, and the 2δ factor ensures the filtration encompasses at least the inter-cluster distance regime. The persistence diagram, plotting (birth, death) coordinates of H1 features above the diagonal, is produced at this stage; Figure 1 shows a schematic H1 diagram (inset) at this step.

**Software stack and cross-checks.** Persistence diagrams are computed with Ripser via Ripser.py (Bauer, 2021; Tralie et al., 2018). As a cross-check, all primary-match diagrams are recomputed with GUDHI and giotto-tda (Tauzin et al., 2021), confirming identical birth–death pairs to within numerical tolerance (10⁻⁶ m). GUDHI is additionally used for the bottleneck distance and landscape representations reported in Sections 3.6–3.7.

### 2.5 Closed Cycle Identification

Each H1 feature in the persistence diagram corresponds to a topological loop, a 1-cycle in the Vietoris–Rips complex. To recover the geometric realisation, we construct the adjacency graph of edges with distances in the persistence interval [birth, death] and apply breadth-first search (BFS) to enumerate closed cycles of length ≥ 3. We use BFS rather than depth-first search to prioritise shorter cycles, which correspond to minimal enclosing arrangements and are more interpretable as formation structures. Cycles are enumerated via BFS from each vertex; the highest-scoring cycle (by edge-distance proximity to the persistence interval midpoint) is selected as the geometric representative.

### 2.6 Temporal Analysis and Statistical Tests

For each analysis window, we compute H0 and H1 feature counts and persistence values at the individual and tactical scales. Temporal evolution is assessed by comparing mean persistence between match halves using the Wilcoxon rank-sum test (Mann-Whitney U), supplemented by a permutation test (10,000 permutations). Scale interactions are characterised by Spearman rank correlation and Fisher's exact test on the co-occurrence of H1 features at the individual and tactical scales.

### 2.7 Event Correlation

Topological transitions around match events are quantified by computing H1 persistence in a window of ±5 frames around each event (at 10 Hz for SkillCorner, ±0.5 s), calculating the persistence change (mean post-event minus mean pre-event). This window captures immediate topological responses to discrete events while minimising contamination from unrelated dynamics. Events are sourced from SkillCorner dynamic event annotations (player possessions, on-ball engagements, off-ball runs, passing options) and phases of play (build-up, direct, chaotic, transition, set play). Statistical significance is assessed by Mann-Whitney U tests on the persistence deltas against zero.

---

## 3. Results

### 3.1 Scale-Specific Connected Components (H0)

**Single-match.** Without clustering, H0 persistence diagrams for each frame encode the full 22-point hierarchical merging sequence. After scale decomposition, H0 at each level reflects organisation at that specific scale. At the individual scale (δ = 2.98 m), H0 = 19.02 ± 2.47 (mean ± s.d.), varying with local player proximity patterns. At the tactical scale (δ = 12.0 m), H0 = 4.77 ± 1.60, capturing the number of distinct tactical groups. At the team scale (δ = 30.0 m), H0 = 1.44 ± 0.50, with 56.0% of frames having H0 = 1 (all 22 players in a single cluster), 44.0% having H0 = 2.

**Multi-match validation (10 matches).** The three-scale H0 structure is consistent across all 10 matches: individual H0 = 19.05 ± 0.39 (grand mean ± across-match s.d.), tactical H0 = 4.92 ± 0.36, team H0 = 1.38 ± 0.08. All matches fall within the expected H0 ranges for all three scales.

### 3.2 H1 Loop Detection

**Single-match (primary).** Across 150 analysis frames, the framework detects 403 H1 loops:

| Scale | Total loops | Frames with loops | Mean loops/frame | Mean persistence | Max persistence |
|-------|-------------|-------------------|-----------------|-----------------|-----------------|
| Individual (2.98 m) | 382 | 143/150 (95.3%) | 2.55 | 1.977 ± 1.128 | 12.991 |
| Tactical (12.0 m) | 21 | 19/150 (12.7%) | 0.14 | 3.797 ± 3.008 | 10.771 |
| Team (30.0 m) | 0 | 0/150 (0%) | N/A | N/A | N/A |

Individual-scale loops are frequent but transient (low mean persistence), representing dynamic player-level interactions. Tactical-scale loops are less frequent but substantially more persistent, representing stable formation structures, strategic gaps between defensive lines, midfield zones, or coordinated pressing shapes.

The team-scale H1 null result is an *a priori* combinatorial consequence of the clustering (see **Remark 3.2.1** below), confirmed empirically (H1 = 0 across all 1,500 frames); our multi-scale H1 analysis therefore operates at two scales (individual and tactical) with three-scale H0 decomposition.

> **Remark 3.2.1 (Team-scale H1 is zero *a priori*).** At δ = 30.0 m the 22 players are reduced to *k* ∈ {1, 2} centroids in every frame (Section 3.1). The Vietoris–Rips complex on *k* ≤ 3 points in general position has at most C(*k*, 2) = 3 edges, and any filled triangle at *k* = 3 is a boundary rather than a non-trivial 1-cycle. Hence H1 = 0 for every admissible filtration, independently of the data, and effective team-scale H1 analysis would require an alternative representation (e.g. spatial density fields or Delaunay triangulations).

**Multi-match validation.** Across 10 matches (1,500 uniformly sampled frames):

| Scale | Total H1 | H1 presence rate | 95% CI (matches) | Mean persistence | Cross-match s.d. |
|-------|----------|-----------------|------------------|-----------------|-----------------|
| Individual | 4,200 | 97.0% ± 1.5% | 96.1%–97.9% | 1.854 | 0.163 |
| Tactical | 315 | 19.3% ± 7.2% | 15.3%–23.7% | 0.666 | 0.299 |
| Team | 0 | 0.0% ± 0.0% | — | N/A | N/A |

*95% CIs are match-level bootstrap intervals (1,000 resamples; `03_football_analysis/paper_v5_revisions/bootstrap_multi_match_ci.py`).* The individual-scale H1 presence rate of 97.0% (s.d. 1.5%; 95% CI over matches 96.1%–97.9%) across 10 independent matches confirms that loop structures are a near-universal feature of competitive spatial systems at this scale. Tactical-scale H1 presence of 19.3% (s.d. 7.2%; 95% CI over matches 15.3%–23.7%) shows meaningful cross-match variability, likely reflecting differences in tactical systems and match dynamics.

### 3.3 Closed Cycle Structures

Closed cycle identification recovers the geometric realisations of all 403 single-match H1 generators. Individual-scale cycles typically comprise 4–6 nodes (cluster centroids), corresponding to small ring-like player arrangements. Tactical-scale cycles comprise 4–5 nodes with higher persistence, corresponding to larger-scale formation gaps. See Figure 2 for a representative geometric realisation.

Representative examples:
- **Individual, Frame 50**: 5-node cycle, persistence 12.99 m, a tight pentagonal pressing arrangement
- **Tactical, Frame 50**: 4-node cycle, persistence 10.77 m, the highest-persistence feature, corresponding to a stable gap between defensive and midfield lines

![Figure 2: Geometric realisation of representative H1 loops at the individual (δ = 2.98 m) and tactical (δ = 12.0 m) scales for SkillCorner match 1996435, frame 50. Individual: 5-node cycle, persistence 12.99 m; tactical: 4-node cycle, persistence 10.77 m. Cycles recovered from the adaptive filtration ε_max per equation (1); single-match sample n = 150 analysis frames (uniform, every 100th).](figures/fig2_cycle_geometry.png)

### 3.4 Temporal Evolution

**Primary match (with statistical tests).** Comparison of mean H1 persistence between match halves using the Wilcoxon rank-sum test:

| Scale | First half mean | Second half mean | Change | Wilcoxon p | Permutation p |
|-------|----------------|------------------|--------|-----------|---------------|
| Individual | 1.890 | 2.069 | +9.5% | 0.506 | N/A |
| Tactical | 2.765 | 4.945 | +78.8% | 0.066 | N/A |

Neither scale shows a statistically significant change between halves at the conventional α = 0.05 level. The tactical scale shows a large but non-significant increase (+78.8%, p = 0.066), whilst the individual scale shows a small non-significant increase (+9.5%, p = 0.506). This result is consistent with the multi-match finding (below) that temporal persistence dynamics are match-specific rather than universal.

**Multi-match validation.** Across four matches with sufficient per-half data, the direction of persistence change is not consistent: one match shows a significant decrease, one shows a moderate increase, and two show negligible change. This suggests that temporal persistence dynamics are match-specific rather than universal, likely driven by tactical context, match state (score), and team-specific strategies.

**Formal test: linear mixed model.** To substitute a statistic for this informal statement, we fit a linear mixed model across all 10 matches to per-window tactical-scale H1 persistence with match as a random intercept and "half" as both a fixed effect and a random slope:

$$
\text{persistence}_{mw} = \beta_0 + \beta_1 \cdot \text{half}_{w} + u_{0m} + u_{1m} \cdot \text{half}_{w} + \varepsilon_{mw}.
$$

A significant random-slope variance (Var(*u₁*)) indicates between-match heterogeneity of the half effect, formalising the "match-specific dynamics" claim. A stratified permutation test (10,000 permutations of the half label within match) complements the parametric fit (LMM fitted in `statsmodels`; `03_football_analysis/paper_v5_revisions/half_level_random_effects.py`):

- Fixed effect β̂₁ (half): −0.081 (95% CI [−0.172, 0.0093], LMM *p* = 0.079).
- Random-slope variance V̂ar(*u₁*): 0.00101.
- Stratified permutation *p*: 0.051.

We deliberately retain the coarse binary `half` factor here so that the LMM is directly comparable to the single-match Wilcoxon test above (§3.4 Table). A finer-grained treatment — continuous time-in-match, or phase-of-play covariates from the SkillCorner annotations — is deferred to the functional persistence-landscape analysis planned in Objective 3 of the companion grant, where each match is an element *t ↦ λ_δ(t)* of landscape space and regime transitions are the natural object of inference rather than half-averages.

![Figure 3: Temporal evolution of mean H1 persistence across 2-minute non-overlapping windows for SkillCorner match 1996435 (primary). Individual scale (δ = 2.98 m) and tactical scale (δ = 12.0 m) are shown separately; n = 36 windows (10 Hz, complete 22-player frames). Shaded bands indicate the half-time division used for the Wilcoxon rank-sum test reported in Section 3.4.](figures/fig3_temporal_evolution.png)

### 3.5 Scale Complementarity

The two scales capture weakly correlated but functionally complementary information. Across 900 frames from 6 matches:

- **Spearman rank correlation** between individual-scale and tactical-scale H1 counts: ρ = 0.254, p < 0.001; 95% match-level bootstrap CI [0.200, 0.314] (1,000 resamples over the six matches contributing to this block).
- **Fisher's exact test** on the 2×2 contingency table (presence/absence at each scale): OR = 3.52, p = 0.093; 95% match-level bootstrap CI [2.59, 13.53] (1,000 resamples over the same six matches).

The weak but significant positive correlation indicates that frames with more individual-scale loops tend to have slightly more tactical-scale loops, plausibly because denser player configurations create topological features at multiple scales. The scales show moderate positive co-occurrence (OR = 3.52) that falls short of conventional significance at this sample size (p = 0.093). The Spearman ρ = 0.254 provides the primary quantitative evidence that the scales capture predominantly distinct structural information: individual-scale loops can appear without tactical-scale loops and vice versa.

| Property | Individual scale | Tactical scale |
|----------|-----------------|----------------|
| Loop frequency | High (2.55/frame) | Low (0.14/frame) |
| Mean persistence | Low (1.977 ± 1.128 m) | High (3.797 ± 3.008 m) |
| Max persistence | 12.991 m | 10.771 m |
| Frames with loops | 143/150 (95.3%) | 19/150 (12.7%) |

**TDA-native distance between scales.** The Spearman/Fisher summary above is based on scalar counts. As a TDA-native supplement, we compute per frame the bottleneck distance *d_B*(*D*_ind, *D*_tac) between the individual-scale and tactical-scale H1 persistence diagrams, and the landscape *L²* distance ‖*λ*_ind − *λ*_tac‖_{*L²*} (Bubenik, 2015) using GUDHI (Tauzin et al., 2021) (`03_football_analysis/paper_v5_revisions/tda_native_distances.py`):

| Metric | Median | IQR | Max |
|---|---|---|---|
| Bottleneck *d_B*(*D*_ind, *D*_tac) (m) | 1.511 | 1.324 | 7.994 |
| Landscape *L²* ‖*λ*_ind − *λ*_tac‖ | 5.671 | 6.949 | 51.565 |

Large median distances would corroborate the complementarity claim in a TDA-native metric, independent of the Spearman/Fisher rank-based summaries above. These distances quantify *within-frame* complementarity between the individual-scale and tactical-scale persistence diagrams; *between-tactical-class* distances (relevant to the companion grant's Objective 2 landscape-*L*² power calculation) are a distinct quantity not examined here.

### 3.6 Sensitivity Analysis

**Cutoff distance sensitivity (tactical scale).** H1 detection on a tactical-cutoff grid δ ∈ {6, 8, 10, 12, 14, 16} m (150 frames of the primary match):

| δ (m) | H1 total | H1 presence | Mean H0 |
|-------|----------|-------------|---------|
| 6 | 275 | 87.3% | 13.4 |
| 8 | 162 | 68.0% | 9.8 |
| 10 | 78 | 42.7% | 7.0 |
| 12 | 21 | 12.7% | 4.8 |
| 14 | 5 | 3.3% | 3.5 |
| 16 | 0 | 0.0% | 2.8 |

H1 detection decreases monotonically with cutoff distance on this grid, as expected: larger cutoffs produce fewer centroids and thus fewer potential cycles. The chosen δ = 12.0 m is deliberately at the conservative end of the range where tactical H1 is non-zero (12.7% frame presence vs 87.3% at δ = 6 m; zero by δ = 16 m in this sample), prioritising fewer but more robust tactical loops, consistent with our single-linkage philosophy and domain-informed H0 validation.

**Adaptive filtration ablation.** At δ = 12.0 m, varying the adaptive percentile:

| Percentile | H1 total | H1 presence | Mean filtration |
|-----------|----------|-------------|----------------|
| P50 | 21 | 12.7% | 38.5 m |
| P60 | 21 | 12.7% | 42.7 m |
| P75 | 21 | 12.7% | 50.3 m |
| P90 | 21 | 12.7% | 60.5 m |
| P95 | 21 | 12.7% | 65.6 m |

All percentiles from P50 to P95 produce identical results (21 loops, 12.7% presence), confirming that the adaptive filtration formula is insensitive to this parameter choice across the full tested range.

### 3.7 Linkage Method Comparison

Empirical comparison of single-linkage, complete-linkage, and Ward's method across 600 frames from 4 matches:

| Method | Tactical clusters | H1 total | H1 presence | Chaining ratio (mean cluster size / n clusters) |
|--------|-------------------|----------|-------------|---------------|
| Single | 5.0 ± 1.7 | 153 | 22.2% | 10.96 |
| Complete | 10.8 ± 1.8 | 923 | 86.3% | 1.38 |
| Ward | 11.0 ± 1.7 | 936 | 86.0% | 1.33 |

At the individual scale (δ = 2.98 m), all three methods produce effectively identical results (1,743–1,765 H1 loops, 97% presence), confirming that the chaining effect is negligible at short distances where players are genuinely nearby. At the tactical scale, single-linkage's chaining (ratio ≈ 11, measuring tendency to merge into elongated chains) reduces centroids from ~11 (complete/Ward) to ~5, substantially reducing H1 detection. Our reported single-linkage results are therefore conservative: the true topological richness at the tactical scale is likely greater than reported. At the team scale, all methods confirm H1 = 0 for single-linkage (as expected from 1–2 centroids), while complete and Ward produce team-scale loops, a finding that warrants future investigation with appropriate domain validation.

### 3.8 Event Correlation

Real event correlation using SkillCorner annotations across 10 matches (104,722 event-topology pairs) reveals statistically significant associations between match events and topological transitions (Figure 4):

**Individual scale, significant event types:**

| Event type | Mean Δ persistence | p-value | n |
|-----------|-------------------|---------|---|
| On-ball engagement | −0.256 | < 0.001 | 8,905 |
| Passing option | −0.162 | < 0.001 | 24,343 |
| Build-up phase | +0.731 | < 0.001 | 618 |
| Quick break | −0.766 | 0.010 | 57 |
| Chaotic phase | −0.210 | 0.043 | 1,087 |

**Tactical scale, significant event types:**

| Event type | Mean Δ persistence | p-value | n |
|-----------|-------------------|---------|---|
| Passing option | −0.046 | < 0.001 | 24,343 |
| On-ball engagement | −0.058 | 0.014 | 8,905 |
| Chaotic phase | −0.196 | < 0.001 | 1,087 |
| Build-up phase | +0.342 | < 0.001 | 618 |
| Quick break | −0.666 | 0.046 | 57 |

The pattern is coherent across both scales: events involving spatial disruption (engagements, pressing, quick breaks) are associated with persistence decreases, while events involving spatial organisation (build-up) are associated with persistence increases. This is consistent with the topological interpretation: spatial disruption fragments formation structures (reducing H1), while deliberate build-up creates and sustains them.

**Sensitivity to event-window half-width.** To confirm that the headline event-type effects are not an artefact of the ±5-frame (±0.5 s) window, we re-ran the analysis at ±{5, 10, 20, 50} frames (±{0.5, 1, 2, 5} s); results below give the sign of mean Δ persistence at the **tactical** scale (`03_football_analysis/paper_v5_revisions/event_window_sensitivity.py`).

| Event type (tactical scale) | ±0.5 s | ±1 s | ±2 s | ±5 s |
|---|---|---|---|---|
| On-ball engagement | − | − | − | − |
| Passing option | − | − | − | − |
| Build-up phase | + | + | + | + |
| Quick break | − | − | − | − |
| Chaotic phase | − | − | − | − |

*The corresponding per-window mean Δ persistence magnitudes (at both individual and tactical scales) are produced alongside this sign table by `03_football_analysis/paper_v5_revisions/event_window_sensitivity.py` and ship in the code-release supplementary for readers wishing to check magnitude stability against the ±0.5 s headline values reported in §3.8 above.*

![Figure 4: Mean change in H1 persistence (post-event minus pre-event, ±5 frames at 10 Hz, i.e. ±0.5 s) by match-event type for the individual (δ = 2.98 m) and tactical (δ = 12.0 m) scales. Source: 10 SkillCorner matches, 104,722 event–topology pairs; significance from Mann–Whitney U tests against zero, FDR-corrected. Error bars are 95% CIs.](figures/fig4_event_correlation.png)

### 3.9 Baseline Comparison: Topology vs Geometric Descriptors

To test whether tactical-scale H1 persistence carries information beyond standard football-analytics geometric descriptors, we computed per frame across all 10 matches: team length (range of *x*-coordinates), team width (range of *y*), convex-hull area, and Voronoi dispersion entropy (Folgado et al., 2014; Fernandez and Bornn, 2018), alongside the tactical-scale H1 total persistence. Spearman rank correlation and partial *R²* (topological variable entered after the geometric baseline block, by linear regression) quantify the added information.

| Baseline descriptor | Spearman ρ | *p* | Partial *R²* (topology residual) |
|---|---|---|---|
| Team length (m) | −0.005 | 0.857 | 0.025 |
| Team width (m) | 0.356 | < 10⁻⁴⁰ | 0.036 |
| Convex-hull area (m²) | 0.431 | < 10⁻⁶⁵ | 0.091 |
| Voronoi dispersion entropy | 0.126 | 9.9 × 10⁻⁷ | 0.004 |

*From `03_football_analysis/paper_v5_revisions/baseline_vs_topology.py` (1,500 frames).* Geometric descriptors and tactical-scale H1 persistence are weakly to moderately associated (Spearman |ρ| up to 0.43 for hull area); the partial *R²* values show that topology explains non-negligible residual variance in the baselines after controlling for the other three (hull area 0.091; width 0.036), in line with the Objective 2 criterion in the companion grant.

Issue 9 (multiple testing and large-N versus effect size) applies here. With four Spearman tests, a Bonferroni-adjusted threshold of *α*/4 = 0.0125 leaves team width, convex-hull area, and Voronoi dispersion entropy significant at the corrected level, and team length (*p* = 0.857) non-significant; the qualitative picture is unchanged. The extremely small *p*-values for width (< 10⁻⁴⁰) and hull area (< 10⁻⁶⁵) are driven by the large per-frame sample size (*N* = 1,500 frames pooled across 10 matches), not by large effect sizes: Spearman |ρ| is at most 0.43 and the largest partial *R²* is 0.091, so the geometric and topological descriptors are not redundant but are also not strongly coupled on a per-frame basis. Section 3.11 converts this correlational statement into a cross-validated predictive-utility claim on held-out matches.

### 3.10 Bilateral Topological Coupling

The 22-player analyses reported above merge home and away players into a single point cloud, which discards team identity. Here we run the tactical-scale pipeline (δ = 12.0 m, adaptive Vietoris–Rips filtration) independently on each team's 11-player sub-cloud and report per-team H1 statistics and the per-frame cross-team coupling across the 10-match uniform sample (1,500 frames; `03_football_analysis/paper_v5_revisions/bilateral_topology.py`).

| Sub-cloud | Mean tactical clusters | H1 presence rate | Mean H1 total persistence | Mean H1 persistence (when present) |
|---|---|---|---|---|
| Home (11 players) | 5.27 ± 2.28 | 36.1% | 1.535 | 3.597 |
| Away (11 players) | 5.21 ± 2.39 | 36.4% | 1.552 | 3.522 |
| 22-player merged *(reference)* | 4.92 ± 0.36 | 19.3% ± 7.2% | — | — |

The per-team tactical-H1 presence rate of ≈ 36% is roughly twice the 22-player merged rate (Table in §3.2), indicating that bilateral decomposition exposes per-team formation structure that the merger obscures: single-linkage at δ = 12.0 m produces ≈ 5 tactical clusters in the merged cloud and also ≈ 5 clusters *per team* in the bilateral cloud, so the 11+11 view operates on roughly twice as many centroids in total and gives the Vietoris–Rips complex correspondingly more opportunity for a 1-cycle.

| Quantity | Value | 95% CI |
|---|---|---|
| Cross-team Spearman ρ (lag 0) | 0.037 | [−0.018, 0.087] |
| Cross-team Spearman ρ (lag ±1 frames) | ∈ [−0.048, −0.013] | — |
| Cross-team Spearman ρ (lag ±5 frames) | ∈ [−0.057, −0.040] | — |
| Cross-team Spearman ρ (lag ±10 frames) | ∈ [−0.023, +0.033] | — |
| Co-occurrence P(both teams H1 > 0) | 14.7% | — |
| Co-occurrence P(exactly one team H1 > 0) | 43.2% (home only 21.5%; away only 21.7%) | — |
| Co-occurrence P(neither team) | 42.1% | — |
| Bottleneck *d_B*(*D*_home, *D*_away) (m), finite only | median 0.58; IQR 2.13; max 6.35 | — |
| Landscape *L²* ‖*λ*_home − *λ*_away‖ | median 1.11; IQR 8.61; max 49.6 | — |

*Match-level bootstrap CIs (1,000 resamples) for the lag-0 cross-team Spearman ρ are weighted by within-match frame count; lag values are reported as ranges over the negative and positive lags at each magnitude.*

The cross-team Spearman ρ at lag 0 is small (0.037) with a 95% match-level bootstrap CI of [−0.018, 0.087] that contains zero; the same picture holds at every tested lag from ±1 to ±10 frames (|ρ| ≤ 0.06). The two teams' tactical persistence sequences therefore evolve close to independently at this temporal resolution. The co-occurrence table is consistent with this: under independence P(both) would equal P(home) × P(away) ≈ 0.131; the observed 0.147 gives an odds ratio of 1.32, a modest positive co-occurrence in the same direction as the small positive ρ, but not a strong dependence. The median cross-team bottleneck distance (finite-only) of 0.58 m is small compared with the mean tactical-scale H1 persistence reported in §3.2 (3.797 m), so when both teams have tactical H1 the two persistence diagrams are typically close; the heavier landscape *L²* tail (IQR 8.61) reflects the small number of frames where the diagrams differ in essential features.

### 3.11 Predictive Incremental Utility on Held-Out Matches

The partial-*R²* statement in Section 3.9 is correlational: topology explains residual variance in each baseline descriptor after controlling for the other three. To convert that statement into a predictive claim, we ask whether tactical-scale H1 carries information for an out-of-sample classification task on top of the same geometric baselines. The label is the binary frame indicator **1**[*frame t lies in a build-up phase*] constructed from the SkillCorner `team_in_possession_phase_type` annotation; the build-up class is the largest of the positively-signed event types in Section 3.8 and yields a balanced-enough target across the 10-match cohort (prevalence 13.7% of frames). Two feature blocks are compared:

- Block A (baselines): team length, team width, convex-hull area, Voronoi dispersion entropy.
- Block B: block A plus tactical-scale H1 total persistence (δ = 12.0 m).

L₂-regularised logistic regression (sklearn default *C* = 1.0; features standardised within each fold) is fit under `GroupKFold(n_splits=10)` over `match_id`, so every fold's test set consists entirely of held-out matches. We report out-of-fold AUC, log-loss, and Brier score, plus the block-B-minus-block-A deltas with match-level bootstrap 95% CIs (1,000 resamples) and a stratified within-match permutation *p*-value (2,000 permutations) on ΔAUC (`03_football_analysis/paper_v5_revisions/predictive_utility.py`).

| Topology summary added | AUC (B / A) | ΔAUC [95% CI] | Δlog-loss [95% CI] | Permutation *p* |
|---|---|---|---|---|
| Tactical H1 total persistence | 0.687 / 0.693 | −0.005 [−0.015, +0.001] | +0.0017 [−0.0004, +0.0049] | 1.00 |
| Tactical H1 count | 0.689 / 0.693 | −0.004 [−0.010, +0.0004] | +0.0014 [+0.0001, +0.0036] | 1.00 |
| Tactical H1 max persistence | 0.687 / 0.693 | −0.006 [−0.016, +0.001] | +0.0020 [−0.0002, +0.0056] | 1.00 |
| *Robustness target:* **1**[*chaotic phase*] (prevalence 7.0%) | | | | |
| Tactical H1 total persistence | 0.716 / 0.719 | −0.002 [−0.005, +0.0006] | +0.0005 [+0.00001, +0.0011] | 1.00 |

*GroupKFold over `match_id`; out-of-fold metrics on pooled test predictions. Δ is block B minus block A; positive values would indicate that tactical H1 helps. Match-level bootstrap CIs resample the 10 matches with replacement and recompute Δ on the resampled out-of-fold predictions.*

The geometric baseline block A already achieves AUC ≈ 0.69 for build-up and AUC ≈ 0.72 for chaotic phases, so the task is not trivial but well-served by the four geometric descriptors. Across all three tactical-H1 summaries (total persistence, count, max persistence) and both targets, the point estimate of ΔAUC is small and slightly negative, the match-level bootstrap CIs contain zero or are centred just below zero, and the stratified permutation *p* is 1.0 (the observed ΔAUC is at the lower end of the permutation null). The log-loss and Brier deltas are small in absolute terms; the log-loss tightening with the count and chaotic-target specifications reflects a small calibration penalty, not a discrimination gain. The conclusion is that on the present 10-match cohort with the four-feature geometric baseline already in place, tactical-scale H1 total persistence carries no detectable incremental predictive utility for held-out-match phase classification. Section 4.2 reconciles this null finding with the partial-*R²* statement of Section 3.9.

---

## 4. Discussion

### 4.1 Methodological Contributions

Our approach is complementary to ongoing theoretical work on multiparameter persistence (Botnan and Lesnick, 2022), which addresses scale conflation algebraically but faces computational barriers for large point clouds. We take a practical, domain-informed route: hierarchical clustering at validated cutoff distances decomposes the point cloud by organisational level before computing standard single-parameter persistent homology at each level.

The cutoff distance, which we term *domain-informed* rather than "goal-dependent" (to avoid ambiguity with the sport-specific meaning of "goal"), defines the organisational level under analysis. The three validated regimes (individual, tactical, team) emerge from systematic parameter sweep and reflect genuine hierarchical structure in the competitive system. The tactical cutoff (12.0 m) is explicitly a domain-informed choice, justified by (i) its position within the automated metric range (6.87–16.31 m), (ii) its correspondence to standard football zone dimensions, and (iii) sensitivity analysis showing non-zero tactical H1 on the primary-match grid from 6 m to 14 m (Section 3.6).

The adaptive filtration formula addresses a practical coupling between the clustering and filtration steps. Empirical percentile ablation (Section 3.6) yields identical tactical-scale H1 counts for P50–P95 on the primary 150-frame sample; we adopt P75 as a conventional robust summary of inter-centroid distances. This construction is a general recipe for any multi-scale TDA pipeline that uses clustering as a preprocessing step.

### 4.2 Multi-Scale Topological Structure

The complementarity of the individual and tactical scales is supported by quantitative evidence (Section 3.5): **Spearman** rank correlation between individual-scale and tactical-scale H1 (count-based) *ρ* = 0.254, *p* < 0.001; 95% match-level bootstrap CI [0.200, 0.314] (1,000 resamples over matches). **Fisher’s exact test** on the 2×2 presence/absence table gives OR = 3.52, *p* = 0.093, with 95% match-level bootstrap CI [2.59, 13.53]. Spearman *ρ* remains the primary summary for scale complementarity. The weak positive correlation likely reflects the confound that dense player configurations create opportunities for topological features at multiple scales simultaneously. Despite this, the scales capture predominantly distinct structural information, as demonstrated by divergent multi-match frame *H*₁ presence rates (97.0% vs 19.3%) and persistence profiles.

**Baseline versus topology — non-redundancy without held-out predictive utility.** Two complementary statements characterise the relationship between tactical H1 total persistence and the four geometric baselines (length, width, convex-hull area, Voronoi dispersion entropy). *Non-redundancy (correlational; Section 3.9).* Spearman *ρ* is −0.005, 0.356, 0.431, and 0.126 (*p* = 0.857, *p* < 10⁻⁴⁰, *p* < 10⁻⁶⁵, *p* = 9.9 × 10⁻⁷), and the partial *R²* of tactical-scale H1 after the other three baselines is 0.025, 0.036, 0.091, 0.004; these values, in particular the 0.091 for hull area, demonstrate that tactical H1 explains residual variance in the geometric block that the geometric features themselves do not account for. *Predictive utility (cross-validated; Section 3.11).* The natural follow-up question — whether that residual variance translates into incremental predictive performance on held-out matches — is answered negatively at the present sample size: a GroupKFold-over-matches logistic regression for the binary build-up-phase label yields AUC = 0.693 for the baseline block and AUC = 0.687 for the baseline-plus-tactical-H1 block, ΔAUC = −0.005 with match-level bootstrap 95% CI [−0.015, +0.001] and stratified permutation *p* = 1.0. The same null finding holds when tactical-H1 total persistence is replaced by H1 count or max-persistence and when the target is replaced by the chaotic-phase indicator (table in Section 3.11). The two statements are not in contradiction. Non-redundancy is a variance-decomposition property of the within-sample regression, whereas predictive utility on held-out matches additionally requires that the residual variance generalises between matches with only 10 training units to estimate the topology's regression coefficient. With the baseline block already achieving an AUC near 0.7 on this task, the marginal slot available for tactical H1 is small, and the present 10-match cohort does not have the statistical power to fill it.

The honest reading is therefore that tactical H1 carries non-redundant geometric information at the per-frame level on this sample (Section 3.9) but that the present 10-match cohort is not large enough to convert that into a detectable held-out predictive gain for phase classification (Section 3.11); the fully-specified ANCOVA with topology as the tested block at full-season scale is the definitive test of incremental predictive utility, and the present null is the effect-size benchmark a population-scale replication needs to beat. As noted in §3.9, the extremely small *p*-values for width and hull area are driven by the large per-frame sample (*N* = 1,500) rather than by large effect sizes, and a Bonferroni correction for the four Spearman tests (*α*/4 = 0.0125) does not change the qualitative picture.

### 4.3 Temporal Dynamics and Event Correlation

The temporal evolution result is more nuanced than initially reported: the primary match shows a large but non-significant tactical-scale persistence increase (+78.8%, *p* = 0.066), but the direction is not consistent across matches. The non-significant result for the primary match, despite a large effect size, reflects the low statistical power inherent in single-match half-level comparisons (*n* = 10 and 9 windows with non-zero tactical persistence per half). Half-level persistence dynamics appear driven by match-specific factors such as tactical adjustments, scoreline effects, and substitutions, rather than universal trends.

**Multi-match formal test (Section 3.4).** A linear mixed model on per-window **tactical-scale** H1 persistence over all 10 matches (*n* = 354 two-minute windows) with match as a grouping factor and “half” as a fixed and random-slope effect gives: fixed effect *β̂*₁ (second half) = −0.081, 95% CI [−0.172, 0.0093], LMM *p* = 0.079; estimated random-slope variance *V̂*ar(*u*₁) = 0.00101; stratified permutation *p* = 0.051 (10,000 within-match permutations of the half label). These results align the informal “match-specific dynamics” phrasing with estimates that are borderline at *α* = 0.05, rather than a uniform half effect across matches.

The real event correlation, based on 104,722 event–topology pairs across 10 matches, provides the first evidence that persistent homology features are genuinely responsive to match dynamics. The coherent pattern is that disruption decreases persistence whilst organisation increases it; this validates the topological interpretation and suggests applications in real-time tactical monitoring. Event-window sensitivity (Section 3.8) shows the same sign for the five headline tactical-scale event types from ±0.5 s to ±5 s (Table in Section 3.8).

### 4.3b Bilateral Coupling

The bilateral decomposition (Section 3.10, Tables therein) makes the team identity that the 22-player analysis discards an explicit object of inference. Two findings are worth highlighting. First, per-team tactical H1 presence rate (≈ 36% for each of home and away) is roughly twice the 22-player merged rate (19.3% ± 7.2%; Section 3.2); the merge therefore obscures formation structure that is recovered cleanly by splitting on team identity, and the per-team rate is symmetric between home and away to within 0.3 percentage points (a sanity check that the framework treats the two teams identically). Second, the per-frame cross-team coupling is small in every metric we examined: Spearman ρ = 0.037 at lag 0 with 95% match-level bootstrap CI [−0.018, 0.087] (i.e. not distinguishable from zero); odds ratio for joint H1 presence 1.32 (only marginally above the independence value of 1); and lagged ρ staying below 0.06 in absolute value out to ±10 frames. The two teams' tactical persistence sequences therefore evolve close to independently at frame resolution within these 1,500 frames. This is itself a non-trivial finding — it sets the per-frame bilateral coupling at zero as a null reference, against which any later evidence for a tactical-context-dependent coupling (during pressing sequences, during sustained possession, around set plays) can be tested. The bilateral coupling statistic is the first quantitative anchor for the bilateral topological-coupling hypothesis that motivates the population-scale extensions (Brown et al., in preparation); the present null result is precisely the kind of effect-size benchmark the full-season analysis needs to power.

### 4.4 Limitations

**Linkage selection is a substantive methodological choice.** The chaining effect at the tactical scale (Section 3.7) yields 153 tactical H1 loops under single-linkage versus 923 (complete-linkage) and 936 (Ward's method) over the same 600-frame, 4-match comparison sample. This is nearly an order of magnitude and is large enough that the linkage choice changes the scientific picture rather than merely the precision of a conservative estimate; we should therefore treat it as a methodological decision, not a conservatism preference. We retain single-linkage in this paper for the domain reason given in Section 3.7 (clusters as chain-connected proximity groups, robust against partition artefacts), but we regard the order-of-magnitude gap as an open scientific question rather than a settled one.

A principled criterion for linkage selection should come from the dynamical system rather than from clustering quality metrics alone. A natural candidate is to choose the linkage method under which the discovered governing equation for a persistence functional — for example the landscape \(L^2\) norm \(t \mapsto \|\lambda_\delta(t)\|_{L^2}\) or the tactical H1 total-persistence sequence — is most sparse, in the sense of sparse identification of nonlinear dynamics (SINDy; Brunton et al., 2016). Under this view, the correct linkage is the one for which the post-clustering point cloud is the most natural coordinate system for the underlying dynamics, with sparsity of the recovered library acting as an information-theoretic selection criterion. Operationalising this criterion (i.e. choosing the dynamical state, defending sparsity-of-library against AIC/BIC/cross-validation baselines, and confirming that the chosen linkage's persistence sequence is genuinely lower-dimensional) is beyond the scope of the present validation paper and is deferred to the forthcoming full-season work (Brown et al., in preparation). The 600-frame linkage table in Section 3.7 should be read as setting up this question, not resolving it.

**Tactical cutoff is a domain-informed choice within an automated-metric range.** The silhouette-optimal cutoff (16.31 m) and the information-content-optimal cutoff (6.87 m) bracket the chosen 12.0 m. The half-zone-width justification (Section 2.3) is domain-reasonable but ultimately subjective, and Section 3.6 reports the operative range (δ ∈ [6, 14] m) on the 150-frame primary-match sample as an empirical sensitivity rather than a derivation of δ. A more principled criterion would replace the domain heuristic with a stability property of the dynamical persistence sequence: the most stable tactical cutoff is the one minimising the variation of the persistence landscape path under small perturbations of δ,

\[
\delta^{\star} = \arg\min_{\delta}\; \mathrm{Var}_{\epsilon}\bigl\|\,\lambda_{\delta+\epsilon}(\cdot) - \lambda_{\delta}(\cdot)\,\bigr\|_{L^{2}},
\]

where ε ranges over a small neighbourhood of zero and \(\lambda_\delta(\cdot)\) is the per-match persistence landscape path \(t\mapsto\lambda_\delta(t)\) (Bubenik, 2015). This is a computable quantity given the GUDHI landscape infrastructure already used in Section 3.5 (Tauzin et al., 2021) and is the natural successor to the present domain-informed choice. Evaluating it on a single match would be premature — the sample size for landscape variance estimation is the number of matches, not the number of frames — so we defer evaluation to the persistence-landscape companion paper flagged in Section 4.5, treating the 12.0 m value reported here as a domain-informed reference within the empirically-validated [6, 14] m range.

**Two-scale H1, not three.** Our multi-scale framework identifies three H0 regimes but only two H1 regimes. Team-scale H1 absence is a structural consequence of the 1–2 centroids produced at δ = 30.0 m, not a methodological limitation. Effective team-scale H1 analysis would require alternative representations (e.g., spatial density fields or Delaunay triangulations) rather than centroid-based point clouds.

**Broadcast tracking resolution.** All data in this study are broadcast-derived (SkillCorner, 10 Hz). Surveys of tracking in team sports highlight trade-offs among sampling rate, spatial precision, and deployment cost (Cummins et al., 2013; Aughey, 2011); broadcast products typically offer lower spatial precision than higher-frequency optical systems (e.g. 25 Hz), which may affect persistence magnitude estimates. The framework's structural findings (scale regimes, H1 presence rates, sensitivity profiles) are expected to be robust across tracking technologies, but direct persistence magnitude comparison with optical data remains for future work.

### 4.5 Outlook

Two extensions of this work are under active development, and each directly resolves one of the methodological limitations of Section 4.4. First, the 10-match evidence base presented here is being scaled to a full Championship season (~540 matches) to characterise population-level distributions of H0/H1 counts, barcode lengths, and landscape norms, and to test tactical-fingerprint classification at population scale (Brown et al., in preparation); this is the natural setting for the SINDy-on-persistence linkage criterion of Section 4.4, because sparse identification of a governing equation for \(t \mapsto \|\lambda_\delta(t)\|_{L^2}\) requires the population-sized sample of sequences that a full season provides. Second, persistence landscape dynamics (Bubenik, 2015; Chazal et al., 2014) are being developed to treat each match as a path *t ↦ λ_δ(t)* in landscape space, enabling stability-regime characterisation and change-point detection within and across matches; this is the natural setting in which the landscape-stability cutoff criterion stated in Section 4.4 can be evaluated, since the resampling unit for \(\mathrm{Var}_\epsilon\|\lambda_{\delta+\epsilon}-\lambda_\delta\|_{L^2}\) is the match-level landscape rather than the per-frame summary. These extensions address the main open questions emerging from the present results: whether tactical-scale H1 presence is a population-stable feature, whether SINDy-recovered governing equations select between candidate linkage methods, and whether functional representations of persistence dynamics recover tactical structure beyond what static diagrams capture.

---

## 5. Conclusion

We have presented a multi-scale persistent homology framework for competitive spatial systems that addresses the scale conflation problem through two practical contributions: domain-informed clustering for scale decomposition and adaptive filtration for scale-consistent H1 detection. Validation across 10 professional football matches identifies three H0 analysis regimes and two H1 regimes with distinct and complementary topological signatures, demonstrates robust H1 detection across a broad cutoff parameter range, and establishes the first real event-topology correlations in sports analytics (104,722 pairs, 10 matches). The framework is ready for cross-domain application to any bounded competitive multi-agent system with spatial tracking data.

---

## Code and Data Availability

**Data.** All tracking data are from the SkillCorner open broadcast tracking repository (SkillCorner, 2024; <https://github.com/SkillCorner/opendata>). The ten match IDs analysed in this paper are: primary match **1996435** (Sydney FC vs Adelaide United, A-League 2024/25), plus 1886347, 1899585, 1925299, 1953632, 2006229, 2011166, 2013725, 2015213, and 2017461. Dynamic event annotations and phase-of-play labels are from the same repository.

**Code.** Implementation, analysis pipelines and figure generation scripts are available at `https://github.com/<user>/Football-TDA` (commit hash `<to be inserted at submission>`). The multi-match validation pipeline corresponds to `03_football_analysis/multi_match_validation.py` with the `--skillcorner-only` flag; event correlation is reproduced by `real_event_correlation.py`. The Paper v5 revision additions are reproduced by the scripts in `03_football_analysis/paper_v5_revisions/`: `bootstrap_multi_match_ci.py` (Section 3.5 bootstrap CIs), `tda_native_distances.py` (Section 3.5 bottleneck/landscape distances), `half_level_random_effects.py` (Section 3.4 LMM), `event_window_sensitivity.py` (Section 3.8 sensitivity), `baseline_vs_topology.py` (Section 3.9 partial *R²*), `bilateral_topology.py` (Section 3.10 bilateral coupling), and `predictive_utility.py` (Section 3.11 held-out-match predictive utility).

**Software stack.** Python 3.11; Ripser.py 0.6.4 (Tralie et al., 2018); GUDHI 3.9 (bottleneck distance, landscapes); giotto-tda 0.6 (Tauzin et al., 2021) for cross-checks; NumPy 1.26, SciPy 1.12, pandas 2.1, scikit-learn 1.4, statsmodels 0.14. An Apptainer/Docker container with pinned versions accompanies the release.

**Synthetic exemplar.** A synthetic 22-agent swarm with seeded ring formations is included in the code release to enable teaching and reproduction without proprietary tracking data. Acceptance criterion: individual-scale H1 presence rate within ±3 pp of the primary match (95.3%), tactical-scale H1 presence rate within ±5 pp of 12.7%, and at least one H1 generator per frame recovered by closed-cycle identification for all frames with non-zero H1. A pass/fail test implementing these checks ships in the code release.

---

## Acknowledgements

We thank SkillCorner for broadcast tracking open data. Computations were performed using Ripser (Bauer, 2021) via Ripser.py (Tralie et al., 2018).

---

## References

Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423.

Botnan, M.B. and Lesnick, M. (2022). An introduction to multiparameter persistence. In *Representations of Algebras and Related Structures*, EMS Press, pp. 77–150. arXiv:2203.14289.

Brown, R. et al. (in preparation). Full-season topological fingerprinting of EFL Championship 2023/24. Manuscript in preparation.

Brunton, S.L., Proctor, J.L. and Kutz, J.N. (2016). Discovering governing equations from data by sparse identification of nonlinear dynamical systems. *Proceedings of the National Academy of Sciences*, 113(15), 3932–3937.

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
**Status**: Draft v5, team cutoff 30.0 m (SkillCorner-derived); all numbers updated to SkillCorner uniform 150-frame analysis
