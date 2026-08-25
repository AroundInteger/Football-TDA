# Multi-Scale Persistent Homology for Competitive Spatial Systems: GPS-Aware Methods and Validation in Professional Football

## Abstract!

We present a multi-scale persistent homology framework for analysing competitive spatial systems, validated using high-frequency GPS tracking data from professional football. Standard single-parameter Vietoris–Rips persistent homology computes topological features across all scales simultaneously; for multi-agent systems with hierarchical organisation, this conflates structure at different organisational levels within a single persistence diagram. We address this through two methodological contributions. First, domain-informed hierarchical clustering with goal-dependent cutoff distances decomposes the point cloud by organisational level before computing homology, enabling scale-specific topological characterisation. Second, adaptive filtration — scaling the Vietoris–Rips threshold to the post-clustering point cloud geometry — ensures consistent detection of H1 features (loops) across all analysis scales, where a fixed threshold appropriate at one scale produces null results at another. Systematic investigation of the cutoff distance parameter space (0.5–30.0 m, 150,214 GPS frames) identifies three validated analysis regimes: individual (2.98 m, 99% validation), tactical (12.0 m, 96% validation), and team (30.0 m, 100% validation). Application of the framework to a full professional match detects 523 H1 loops across 149 analysis windows (470 individual-scale, 53 tactical-scale), with closed cycle identification recovering their geometric realisations. Temporal analysis reveals increasing topological persistence over match time (+8.5% individual, +18.8% tactical from first to second half), suggesting progressive stabilisation of formation structures. The two analysis scales capture complementary information: the individual scale exhibits high complexity and coherence (dynamic micro-networks), whilst the tactical scale exhibits high persistence and strength (stable macro-networks). These methods are domain-agnostic and applicable to any bounded competitive multi-agent system with spatial tracking data.

**Keywords**: persistent homology, topological data analysis, multi-scale analysis, competitive systems, sports analytics, GPS tracking

---

## 1. Introduction

### 1.1 Background

Competitive spatial systems — collections of agents that interact, coordinate within groups, and compete between groups within a bounded domain — are ubiquitous. Examples include autonomous vehicle fleets sharing airspace, opposing crowd flows at transport hubs, predator–prey populations in ecosystems, and sports teams contesting possession of territory. A distinguishing feature of such systems is that they operate across multiple spatial scales simultaneously: individual agent decisions (metres), small-group tactical coordination (tens of metres), and whole-system organisation (hundreds of metres). Understanding the interplay between these scales is a fundamental challenge in applied mathematics.

Topological Data Analysis (TDA), and persistent homology in particular, provides a natural framework for studying the shape of spatial data across scales (Edelsbrunner and Harer, 2010; Carlsson, 2009). By constructing a filtration of simplicial complexes indexed by a scale parameter and tracking the birth and death of topological features, persistent homology captures multi-scale structure in a mathematically rigorous way. Applications span protein structure (Xia and Wei, 2014), materials science (Hiraoka et al., 2016), and collective behaviour (Topaz et al., 2015).

However, applying standard single-parameter persistent homology to such systems presents practical challenges that motivate the multi-scale approach developed here.

### 1.2 The Scale Conflation Problem

A single Vietoris–Rips filtration applied to a multi-agent point cloud computes topological features across all spatial scales simultaneously. The resulting persistence diagram encodes the full hierarchical clustering structure of the point cloud — from individual agent proximity through small-group formation to system-wide organisation — in a single mathematical object. For exploratory analysis of systems without known hierarchical structure, this is a strength. For multi-agent systems with *known* hierarchical organisation operating across distinct spatial scales, however, it presents a practical challenge: topological features from different organisational levels are superimposed, making it difficult to attribute specific features to specific scales or to track scale-specific dynamics over time.

This challenge is well-recognised in the TDA community. Topaz et al. (2015) address it by visualising Betti numbers across both simulation time and persistence scale, noting that different organisational structures appear at different filtration values. The multiparameter persistence literature (Botnan and Lesnick, 2022; Lesnick, 2015) provides a theoretical framework for simultaneous multi-scale analysis, though computational challenges limit practical application to large point clouds. Jardine et al. (2023) develop tools for analysing multiscale clustering sequences using persistent homology, directly addressing hierarchical decomposition. Ulmer et al. (2022) apply Vietoris–Rips construction to multi-agent system snapshots, noting the sensitivity of topological features to parameter choices.

Our approach takes a complementary, domain-informed path: rather than analysing the full persistence diagram or developing new algebraic machinery, we decompose the point cloud by organisational level through hierarchical clustering at validated cutoff distances, then compute scale-specific persistent homology on each reduced point cloud. This requires a second methodological step — adaptive filtration — to ensure that the Vietoris–Rips threshold is appropriate for the post-clustering geometry at each scale, since a fixed threshold suitable at one organisational level produces null H1 results at another.

### 1.3 Contributions

This paper makes four contributions:

1. **Scale decomposition via domain-informed clustering**: A hierarchical clustering preprocessing step with goal-dependent cutoff distances that separates organisational levels, enabling scale-specific topological analysis of multi-agent point clouds.

2. **Adaptive filtration**: A data-driven maximum filtration formula that adjusts to the post-clustering point cloud geometry, ensuring consistent H1 detection across all analysis scales.

3. **Scale validation**: Systematic investigation of the cutoff distance parameter space (0.5–30.0 m) on 150,214 GPS frames, identifying three validated analysis regimes with stability scores exceeding 0.88.

4. **Multi-scale H1 analysis**: Detection of 523 H1 loops across 149 match windows with closed cycle identification, temporal evolution analysis, and characterisation of scale-dependent topological dynamics.

### 1.4 Related Work

Persistent homology was introduced by Edelsbrunner et al. (2000) and placed on firm computational foundations by Zomorodian and Carlsson (2005). Stability of persistence diagrams under perturbation was established by Cohen-Steiner et al. (2007). Efficient computation via the Vietoris–Rips filtration is provided by Ripser (Bauer, 2021). Persistence landscapes (Bubenik, 2015) provide a functional representation suitable for statistical analysis.

Applications of TDA to collective behaviour include Topaz et al. (2015), who applied persistent homology to biological aggregation models and visualised scale-dependent structure across filtration values. Ulmer et al. (2022) applied Vietoris–Rips persistent homology to multi-agent system snapshots for change point detection, demonstrating the utility of topological features for temporal dynamics but operating at a single scale. In sports analytics, spatial analysis methods include pitch control models (Fernandez and Bornn, 2018) and spatio-temporal pattern recognition (Gudmundsson and Horton, 2017), but these do not employ topological methods. To our knowledge, no prior work combines domain-informed scale decomposition with persistent homology for competitive, high-frequency spatial systems, nor validates the resulting scale regimes systematically.

---

## 2. Methods

### 2.1 Data

GPS tracking data from a professional Championship football match was obtained via SecondSpectrum. The dataset comprises positions of 22 players (11 per team) at 25 Hz sampling rate, totalling 150,214 frames across a full 90-minute match. Positions are recorded as (x, y) coordinates in metres, centred at the field origin (0, 0), spanning approximately [-52.5, 52.5] × [-34, 34] m.

For persistent homology computation, the match is divided into overlapping temporal windows. Unless otherwise stated, 2-minute windows with 50% overlap are used, yielding 149 analysis windows per half.

### 2.2 GPS-Aware Clustering

At each time step t, the 22 player positions form a point cloud P(t) = {p₁(t), ..., p₂₂(t)} ⊂ ℝ². Direct application of persistent homology to P(t) produces a single persistence diagram encoding all inter-agent distance relationships simultaneously. To separate organisational levels, we preprocess with hierarchical clustering.

**Definition.** For a cutoff distance δ > 0, single-linkage hierarchical clustering partitions P(t) into clusters C₁, ..., Cₖ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding δ. The reduced point cloud is the set of cluster centroids:

P̃(t) = { c̄ⱼ : c̄ⱼ = (1/|Cⱼ|) Σ_{p ∈ Cⱼ} p,  j = 1, ..., k }

Persistent homology is then computed on P̃(t) rather than P(t).

**Implementation:**

```python
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

distances = pdist(player_positions)
Z = linkage(distances, method='single')
labels = fcluster(Z, cutoff_distance, criterion='distance')
centroids = [positions[labels == j].mean(axis=0) for j in np.unique(labels)]
```

### 2.3 Goal-Dependent Cutoff Distance Selection

The cutoff distance δ is not a nuisance parameter but a scale selection that determines the level of organisation under analysis. We conducted a systematic parameter sweep over δ ∈ [0.5, 30.0] m at 100 test points, evaluated on 58 temporal windows (normalised 30% coverage across four epoch lengths: 1, 2, 5, and 10 minutes).

Three analysis regimes emerge, validated by multiple clustering quality metrics (Calinski-Harabasz index, silhouette score, and goal-specific information content):

| Scale | Optimal δ | Validation | Expected H0 | Stability |
|-------|-----------|------------|-------------|-----------|
| Individual | 2.98 ± 0.37 m | 99% of frames | 15–22 | 0.88 |
| Tactical | 12.0 m (silhouette-optimal range 8–15 m) | 96% of frames | 3–12 | 0.97 |
| Team | 28.11 ± 0.47 m (information-optimal range 15–25 m) | 100% of frames | 1–3 | 0.98 |

"Validation" denotes the fraction of analysis windows in which H0 falls within the expected range for that regime. "Stability" is the cross-epoch consistency score under normalised sampling.

### 2.4 Adaptive Filtration for H1 Detection

After clustering at cutoff δ, the reduced point cloud P̃(t) has inter-centroid distances much larger than δ. A fixed maximum filtration ε_max (e.g., 1.5 m) is insufficient for H1 detection at the tactical and team scales.

We define an adaptive filtration:

ε_max = max( P₇₅({d(c̄ᵢ, c̄ⱼ) : i < j}),  max(5.0, 2δ) )

where P₇₅ denotes the 75th percentile. The first term adapts to the actual geometry of the reduced point cloud; the second term ensures a minimum filtration proportional to the clustering scale.

Persistent homology is computed using Ripser (Bauer, 2021) with maxdim = 1 and thresh = ε_max:

```python
from ripser import ripser

point_distances = pdist(centroids)
adaptive = np.percentile(point_distances, 75)
min_filt = max(5.0, 2.0 * cutoff_distance)
epsilon_max = max(adaptive, min_filt)

diagrams = ripser(np.array(centroids), maxdim=1, thresh=epsilon_max)
```

### 2.5 Closed Cycle Identification

Each H1 feature in the persistence diagram corresponds to a topological loop — a 1-cycle in the Vietoris–Rips complex. To recover the geometric realisation, we construct the adjacency graph of edges with distances in the persistence interval [birth, death] and apply depth-first search (DFS) to identify closed cycles of length ≥ 3. Cycles are scored by representativeness (how well the cycle edges span the persistence interval) and the longest representative cycle is selected.

### 2.6 Temporal Analysis

For each analysis window, we compute H0 and H1 feature counts and persistence values at the individual and tactical scales. Temporal evolution is assessed by comparing mean persistence between match halves (first half: windows 1–74; second half: windows 75–149). Scale interactions are characterised by co-occurrence analysis (frames with loops at both scales versus one scale only).

---

## 3. Results

![]()

### 3.1 Scale-Specific Connected Components

Without clustering, H0 persistence diagrams for each frame encode the full 22-point hierarchical merging sequence. After scale decomposition, H0 at each level reflects organisation at that specific scale. At the individual scale (δ = 2.98 m), H0 = 17.85 ± 3.54 (mean ± s.d.), varying with local player proximity patterns. At the tactical scale (δ = 12.0 m), H0 = 7.67 ± 1.63, capturing the number of distinct tactical groups. This variation across frames — absent in the undecomposed H0 count at birth, which is always 22 — enables tracking of scale-specific connectivity dynamics over time.

### 3.2 H1 Loop Detection

Across 149 analysis windows, the framework detects 523 H1 loops:

| Scale | Total loops | Frames with loops | Mean loops/frame | Mean persistence | Max persistence |
|-------|-------------|-------------------|-----------------|-----------------|-----------------|
| Individual (2.98 m) | 470 | 148/149 (99%) | 3.18 | 1.781 ± 1.455 | 7.971 |
| Tactical (12.0 m) | 53 | 42/149 (28%) | 1.26 | 3.285 ± 2.241 | 9.392 |

Individual-scale loops are frequent but transient (low mean persistence), representing dynamic player-level interactions. Tactical-scale loops are less frequent but substantially more persistent, representing stable formation structures — strategic gaps between defensive lines, midfield zones, or coordinated pressing shapes.

### 3.3 Closed Cycle Structures

Closed cycle identification recovers the geometric realisations of H1 generators. Individual-scale cycles typically comprise 4–6 nodes (cluster centroids), corresponding to small ring-like player arrangements. Tactical-scale cycles comprise 4–5 nodes with higher persistence, corresponding to larger-scale formation gaps.

Representative examples:
- **Individual, Frame 72**: 5-node cycle, persistence 7.97 — a tight pentagonal pressing arrangement
- **Tactical, Frame 73**: 5-node cycle, persistence 9.39 — the highest-persistence feature, corresponding to a stable gap between defensive and midfield lines

### 3.4 Temporal Evolution

Both scales show increasing persistence from first to second half:

| Scale | First half mean | Second half mean | Change |
|-------|----------------|------------------|--------|
| Individual | 1.708 | 1.853 | +8.5% |
| Tactical | 2.998 | 3.562 | +18.8% |

The tactical scale shows a substantially larger increase, suggesting that group-level formation structures stabilise more strongly over match time than individual-level patterns.

### 3.5 Scale Complementarity

The two scales capture distinct and complementary information:

| Property | Individual scale | Tactical scale |
|----------|-----------------|----------------|
| Loop frequency | High (3.18/frame) | Low (1.26/frame) |
| Persistence | Low (mean 1.78) | High (mean 3.29) |
| Network strength | 4.31 ± 3.31 | 5.16 ± 2.10 |
| Network complexity | 2.50 ± 1.15 | 1.50 ± 0.84 |
| Coherence | 0.655 ± 0.076 | 0.452 ± 0.259 |

The individual scale captures fine-grained, dynamic micro-networks with high complexity and coherence. The tactical scale captures coarse-grained, stable macro-networks with high persistence and strength. Combined, they provide a multi-resolution view of the competitive system's topological organisation.

### 3.6 Event Correlation Framework

Topological transitions around match events (analysed using synthetic event markers at early, mid, and late match) reveal distinct scale-dependent dynamics:

- **Individual scale**: Smooth, gradual transitions (typical persistence change ±0.5)
- **Tactical scale**: Sharp, episodic transitions (persistence changes up to ±7.9)

The five largest persistence transitions all occur at the tactical scale, with the largest being a -7.92 drop at frame 138 (tactical loop collapse) and a +6.98 formation event at frame 12. This suggests that tactical-scale H1 features may serve as indicators of significant formation changes — a hypothesis requiring validation against real match events (goals, substitutions, possession changes) in future work.

---

## 4. Discussion

### 4.1 Methodological Contributions

Our approach is complementary to ongoing theoretical work on multiparameter persistence (Botnan and Lesnick, 2022), which addresses scale conflation algebraically but faces computational barriers for large point clouds. We take a practical, domain-informed route: hierarchical clustering at validated cutoff distances decomposes the point cloud by organisational level before computing standard single-parameter persistent homology at each level. The key insight is that the cutoff distance is not a nuisance parameter to be optimised away, but a scale selector that defines the level of organisation under analysis. The three validated regimes (individual, tactical, team) emerge from systematic parameter sweep and reflect genuine hierarchical structure in the competitive system.

The adaptive filtration formula addresses a practical coupling between the clustering and filtration steps. After clustering, inter-centroid distances depend on the clustering scale; a fixed Vietoris–Rips threshold appropriate at one organisational level produces null H1 results at another. By scaling the maximum filtration to the post-clustering geometry, H1 detection becomes consistent across all analysis scales. This is a general solution applicable to any multi-scale TDA pipeline that uses clustering as a preprocessing step.

### 4.2 Multi-Scale Topological Structure

The complementarity of the individual and tactical scales is a central finding. It demonstrates that competitive spatial systems exhibit rich multi-scale topological structure that cannot be captured by analysis at any single scale. The individual scale reveals the moment-to-moment dynamics of agent interactions; the tactical scale reveals the slower-evolving structural organisation of agent groups.

The temporal evolution result — progressive persistence increase, stronger at the tactical scale — is consistent with the intuition that teams settle into formation patterns over match time. Whether this reflects genuine coordination improvement, fatigue-related reduction in tactical variability, or match-state effects (e.g., protecting a lead) requires multi-match investigation.

### 4.3 Limitations

This study validates the framework on a single professional match. Multi-match analysis is needed to establish whether the three-scale structure, persistence magnitudes, and temporal trends generalise across different teams, formations, and match contexts.

The event correlation analysis uses synthetic event markers. Integration with match event data (e.g., from StatsBomb) is needed to test whether tactical-scale H1 transitions predict or respond to specific match events.

No validated performance correlation has been established. The relationship between topological features and team performance (attacking effectiveness, territorial control, goal-scoring) is a hypothesis for future investigation, requiring careful operationalisation of the dependent variable and multi-match statistical power.

### 4.4 Broader Applicability

The methods are domain-agnostic. GPS-aware clustering, adaptive filtration, and multi-scale analysis apply to any bounded competitive multi-agent system with spatial tracking data. Potential applications include autonomous vehicle coordination (where agents compete for space), crowd dynamics (where opposing flows create topological structure), and biological systems (where predator–prey interactions generate multi-scale spatial organisation). Preliminary cross-domain application to armed conflict event data (Brown et al., in preparation) suggests that the three-scale structure may transfer across domains with appropriate scale calibration.

---

## 5. Conclusion

We have presented a multi-scale persistent homology framework for competitive spatial systems that addresses the scale conflation problem through two practical contributions: domain-informed clustering for scale decomposition and adaptive filtration for scale-consistent H1 detection. Validation on professional football GPS data identifies three analysis regimes with distinct topological signatures and demonstrates rich multi-scale structure that single-scale analysis cannot separate. The framework is ready for multi-match validation and cross-domain application.

---

## Acknowledgements

We thank SecondSpectrum for GPS tracking data access and StatsBomb for event data. Computations were performed on [institutional HPC resource].

---

## References

Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423.

Botnan, M.B. and Lesnick, M. (2022). An introduction to multiparameter persistence. In *Proceedings of the International Congress of Mathematicians*, pp. 4290–4310.

Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16(1), 77–102.

Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255–308.

Cohen-Steiner, D., Edelsbrunner, H. and Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120.

Edelsbrunner, H. and Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.

Edelsbrunner, H., Letscher, D. and Zomorodian, A. (2000). Topological persistence and simplification. In *Proceedings 41st Annual Symposium on Foundations of Computer Science*, pp. 454–463.

Fernandez, J. and Bornn, L. (2018). Wide open spaces: A statistical technique for measuring space creation in professional soccer. In *Sloan Sports Analytics Conference*.

Gudmundsson, J. and Horton, M. (2017). Spatio-temporal analysis of team sports. *ACM Computing Surveys*, 50(2), 1–34.

Jardine, N., Mukherjee, S. and Turner, K. (2023). Analysing multiscale clusterings with persistent homology. *arXiv preprint arXiv:2305.04281*.

Lesnick, M. (2015). The theory of the interleaving distance on multidimensional persistence modules. *Foundations of Computational Mathematics*, 15(3), 613–650.

Topaz, C.M., Ziegelmeier, L. and Halverson, T. (2015). Topological data analysis of biological aggregation models. *PLoS ONE*, 10(5), e0126383.

Ulmer, M., Ziegelmeier, L. and Topaz, C.M. (2022). Change point detection in multi-agent systems based on higher-order features. *Chaos*, 32(1), 013117.

Zomorodian, A. and Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249–274.

---

**Corresponding Author**: Dr Rowan Brown, Biomedical Engineering, Swansea University
**Target Journal**: Journal of Applied and Computational Topology
**Status**: Draft — pending multi-match validation results
