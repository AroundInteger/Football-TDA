# Multi-Scale Persistent Homology for Competitive Spatial Systems

**Authors:** Rowan Brown  
**Affiliation:** Swansea University  

**Target:** Journal of Applied and Computational Topology (JACT) / arXiv preprint  

**Source of truth:** `main.tex` + `sections/*.tex` (this Markdown is for discussion only; LaTeX remains authoritative for submission.)

---

## Abstract

Standard single-parameter Vietoris–Rips persistent homology applied to a multi-agent point cloud conflates topological features from distinct organisational levels into a single diagram. We present a multi-scale framework addressing this through two methodological contributions: domain-informed hierarchical clustering, with cutoff distances validated by independent clustering-quality metrics, that decomposes the point cloud by organisational level; and an adaptive Vietoris–Rips filtration, scaled to the post-clustering point cloud's geometry, that keeps *H*₁ (loop) detection consistent across scales. Validated on ten professional football matches (broadcast tracking at 10 Hz; 43,531 frames for the primary match), the framework identifies three stable *H*₀ (connected-component) regimes: individual (2.98 m), tactical (12.0 m), and team (30.0 m), and two *H*₁ regimes: individual-scale loops are frequent and transient (97.0% ± 1.5% frame presence across matches), tactical-scale loops are rarer but more persistent (19.3% ± 7.2%); team-scale *H*₁ is absent a priori as a structural consequence of the clustering. Both regime structures hold across matches and across wide ranges of the cutoff distance and the filtration's percentile parameter, and the two *H*₁ scales carry distinct rather than redundant information (Spearman *ρ* = 0.264 across 1,500 sampled frames). Geometric cycle representatives are recovered for every *H*₁ generator examined. A minimal association between persistence and match events, across ten matches and 104,722 event–topology pairs, confirms the detected features track genuine structure rather than measurement noise. The framework is domain-agnostic and intended for any bounded competitive multi-agent system with spatial tracking data; football serves as a validated testbed.

**Keywords:** persistent homology, multi-scale topology, Vietoris–Rips filtration, multi-agent systems, spatial tracking data, sports analytics

---

## 1. Introduction

### 1.1 Background

Competitive spatial systems, collections of agents that interact, coordinate within groups, and compete between groups within a bounded domain, are ubiquitous. Autonomous vehicle fleets sharing road space, opposing crowd flows at transport hubs, predator–prey populations in an ecosystem, and sports teams contesting territory all share this structure. Such systems characteristically operate across multiple spatial scales at once: individual agent decisions at the scale of metres, small-group coordination at tens of metres, and whole-system organisation at hundreds of metres. Understanding how these scales interact is a standing challenge in applied mathematics, and one that high-frequency spatial tracking data is increasingly able to inform.

Agents within such systems can arrange themselves in ring-like formations that enclose empty space: a pressing trap encircling a player in possession, or a gap between two organisational units that creates room to manoeuvre. These arrangements have a topological character: they are loops in the position data, and their persistence over time distinguishes deliberate structural organisation from transient clustering. Conventional geometric summaries, including convex-hull area, nearest-neighbour distance, and the range of agent positions along each axis, capture different aspects of spatial dispersion but do not directly quantify this loop structure.

Persistent homology, the central tool of topological data analysis, provides a principled way to detect and measure such formations across scale. A filtration of simplicial complexes indexed by a scale parameter tracks the birth and death of topological features, recovering multi-scale structure in a mathematically rigorous way; applications span protein structure, materials science, and collective behaviour. Applying standard single-parameter persistent homology directly to a multi-agent point cloud, however, presents a practical difficulty that motivates the framework developed here.

### 1.2 The Scale Conflation Problem

A single Vietoris–Rips filtration applied to a multi-agent point cloud computes topological features across all spatial scales simultaneously, encoding the full hierarchical clustering structure of the point cloud, from individual proximity through small-group formation to system-wide organisation, within a single persistence diagram. For exploratory analysis of a system with no known hierarchical structure, this is a strength: every scale is examined without prior commitment to which one matters. For a system with known hierarchical organisation across distinct spatial scales, it is instead a practical obstacle. Topological features from different organisational levels are superimposed in the same diagram, making it difficult to attribute a given feature to a given scale or to track scale-specific dynamics over time. This challenge is recognised in the topological data analysis literature, and Section 1.4 positions the present approach against it in detail.

We take a domain-informed path rather than developing new algebraic machinery: the point cloud is decomposed by organisational level through hierarchical clustering at validated cutoff distances, and scale-specific persistent homology is computed on each reduced point cloud in turn. This decomposition introduces a second problem that a single-scale analysis never encounters. Clustering changes the point cloud's geometry at each scale, so a fixed Vietoris–Rips threshold suitable at one organisational level produces null *H*₁ results at another. The adaptive filtration developed in Section 2.4 resolves this second problem.

### 1.3 Contributions

This paper makes four contributions, two methodological and two empirical.

**Methodologically**, it introduces domain-informed scale decomposition: a hierarchical clustering preprocessing step, with cutoff distances validated by independent clustering-quality metrics, that separates organisational levels and enables scale-specific topological analysis of a multi-agent point cloud. It also introduces an adaptive filtration: a data-driven maximum filtration scale that adjusts to the post-clustering point cloud's geometry, ensuring *H*₁ detection remains consistent across analysis scales rather than collapsing to zero at scales the original threshold was not designed for.

**Empirically**, it provides multi-match scale validation: a systematic sweep of the cutoff distance over [0.5, 30.0] m identifies three stable analysis regimes, confirmed across ten independent matches rather than a single demonstration case. It also provides multi-scale topological characterisation: detection of *H*₁ loops at two of the three scales, geometric realisation demonstrated for every generator in the primary-match analysis, evidence that the two *H*₁ scales carry distinct rather than redundant information, and a minimal correlation with real match events confirming the detected features track genuine structure rather than measurement noise.

### 1.4 Related Work

Persistent homology was introduced by Edelsbrunner et al. (2002) and placed on firm computational foundations by Zomorodian and Carlsson (2005). Stability of persistence diagrams under perturbation was established by Cohen-Steiner et al. (2007), and efficient computation via the Vietoris–Rips filtration is provided by Bauer (2021). Persistence landscapes provide a functional representation suitable for statistical analysis (Bubenik, 2015).

Applications of persistent homology to collective behaviour include Topaz et al. (2015), who applied the method to biological aggregation models and visualised scale-dependent structure by plotting Betti numbers across both simulation time and filtration value. Gu et al. (2022) applied Vietoris–Rips persistent homology to multi-agent system snapshots for change-point detection, demonstrating the utility of topological features for temporal dynamics, though their analysis operates at a single scale rather than decomposing by organisational level. The multiparameter persistence literature, surveyed by Botnan and Lesnick (2023), provides a theoretical framework for genuinely simultaneous multi-scale analysis, but computational cost currently limits its application to point clouds much smaller than the 22-agent, high-frequency case considered here. Schindler and Barahona (2023) address hierarchical decomposition directly, developing tools for analysing multiscale clusterings with persistent homology; the present work differs in providing an explicit mechanism, the adaptive filtration of Section 2.4, for keeping *H*₁ detection consistent as the clustering scale itself changes the point cloud's geometry, a coupling that arises specifically when clustering precedes single-parameter persistent homology, and in validating the resulting scale regimes empirically across ten independent real matches rather than within a single theoretical or simulated setting.

In sports analytics specifically, spatial analysis methods including pitch-control models and spatio-temporal pattern recognition are surveyed in Gudmundsson and Horton (2017). Related perspectives model teams as coordinated multi-agent systems and apply network metrics to passing and collective structure (Buldú et al., 2019; Grund, 2012); these approaches complement the present framework but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines domain-informed scale decomposition with persistent homology for a competitive, high-frequency spatial system, or validates the resulting scale regimes across multiple independent matches.

---

## 2. Methods

### 2.1 Data

The primary single-match analysis uses SkillCorner open broadcast tracking data, match ID 1996435 (Sydney FC versus Adelaide United, A-League 2024/25), at 10 frames per second. We retain only frames with complete 22-player coverage, yielding 43,531 frames, approximately 72 minutes of play at this sampling rate; positions are (*x*, *y*) coordinates in metres on a standard pitch model. Nine additional A-League matches, each comprising approximately 40,000–48,000 frames, were obtained from the same repository to validate the framework's generalisability across teams, tactical systems, and competition contexts.

Persistent homology is computed on uniformly subsampled frames rather than on the full 10 Hz stream. For the primary match and for each of the nine additional matches, we retain 150 frames by taking every 290th complete 22-player frame, yielding a consistent cross-match sample of 1,500 frames.

### 2.2 Proximity-Aware Clustering

At each time step *t*, the 22 player positions form a point cloud *P*(*t*) = {*p*₁(*t*), …, *p*₂₂(*t*)} ⊂ ℝ². Computing persistent homology directly on *P*(*t*) produces a single diagram encoding inter-agent distance relationships at all scales simultaneously; to separate organisational levels before computing topology, we preprocess with hierarchical clustering.

For a cutoff distance *δ* > 0, single-linkage hierarchical clustering partitions *P*(*t*) into clusters *C*₁, …, *Cₖ* such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding *δ*. The reduced point cloud is the set of cluster centroids,

\[
\tilde{P}(t)=\left\{\bar{c}_j : \bar{c}_j=\frac{1}{|C_j|}\sum_{p\in C_j} p,\; j=1,\dots,k\right\},
\]

and persistent homology is computed on \(\tilde{P}(t)\) rather than on *P*(*t*) itself.

We use single-linkage throughout. Its definition, clusters as chains of points connected by short pairwise distances, is the most direct reading of spatial proximity, and it produces a conservative estimate of *H*₁ features: reported loops represent robust topological structure rather than artefacts of over-partitioning. Section 4.3 examines the consequences of this choice relative to complete-linkage and Ward's method.

The framework extends to labelled sub-populations by running the same pipeline independently on each label's point cloud rather than on the merged 22-player cloud; we use this here only to confirm the method is agnostic to such relabelling. The substantive application, decomposing by team identity and examining bilateral tactical coupling, is deferred to forthcoming work.

### 2.3 Domain-Informed Cutoff Distance Selection

The cutoff distance *δ* functions as a scale selector rather than a free parameter, since it determines which level of organisation the resulting point cloud represents. We swept *δ* over [0.5, 30.0] m at 100 test points, evaluated against 58 temporal windows sampled to give balanced coverage across four epoch lengths (1, 2, 5, and 10 minutes). Three candidate cutoff values were identified using three independent clustering-quality criteria: the Calinski–Harabasz index, the silhouette score, and a domain-specific information-content measure.

The individual-scale cutoff, 2.98 m, and the team-scale cutoff, 30.0 m, are the values selected by these automated metrics directly. The tactical-scale cutoff is selected differently, because the automated metrics disagree within the tactical range: the silhouette-optimal value is 16.31 m and the information-content-optimal value is 6.87 m. We select 12.0 m, corresponding to half the width of a standard football pitch zone, as a domain-informed value within this range rather than as the output of either metric. Section 3.5 reports the resulting sensitivity of *H*₁ detection to this choice.

### 2.4 Adaptive Filtration for *H*₁ Detection

Clustering at cutoff *δ* produces a reduced point cloud \(\tilde{P}(t)\) whose inter-centroid distances are typically much larger than *δ* itself, so a fixed maximum filtration scale *ε*_max that is appropriate at one cutoff is insufficient for *H*₁ detection at another. We define an adaptive filtration,

\[
\varepsilon_{\max} = \max\Big(P_{75}\{d(\bar c_i,\bar c_j) : i<j\},\; \max(5.0,\,2\delta)\Big),
\tag{1}
\]

where *P*₇₅ denotes the 75th percentile of pairwise inter-centroid distances. The first term adapts the filtration to the geometry of the reduced point cloud at each *δ*; the second term imposes a floor proportional to the clustering scale, preventing degenerate filtration at small *δ* and ensuring the filtration reaches at least the inter-cluster distance regime.

The *P*₇₅ percentile is chosen as a conventional upper-quartile summary of inter-centroid distances. Section 3.5 reports an ablation across *P*₅₀ through *P*₉₅, showing that every tested percentile returns identical *H*₁ totals and frame-presence rates; the choice of *P*₇₅ is therefore a reporting convention, not an optimisation.

Persistence diagrams are computed with Ripser via Ripser.py (Bauer, 2021). We cross-checked all primary-match diagrams against GUDHI (The GUDHI Project, 2024) and giotto-tda (Tauzin et al., 2021), confirming identical birth–death pairs to within numerical tolerance (10⁻⁶ m); GUDHI is also used for the bottleneck-distance and landscape computations reported in Section 3.4.

### 2.5 Closed Cycle Identification

Each *H*₁ feature corresponds to a 1-cycle in the Vietoris–Rips complex. To recover its geometric realisation, we build the adjacency graph of edges whose distances fall within the feature's persistence interval [birth, death], then enumerate closed cycles of length at least 3 by breadth-first search from each vertex. If that graph yields no cycle, we fall back to edges with length in [½ birth, death]. Breadth-first search is used in preference to depth-first search because it prioritises shorter cycles, which correspond to minimal enclosing arrangements and are more directly interpretable as formation structures. Among the enumerated cycles, the one whose edge distances lie closest to the midpoint of the persistence interval is selected as the geometric representative.

### 2.6 Statistical Tests

Scale complementarity (Section 3.4) is assessed by Spearman rank correlation and Fisher's exact test on the frame-level co-occurrence of *H*₁ features at the individual and tactical scales, with 95% confidence intervals obtained by bootstrap resampling over matches (1,000 resamples). Bottleneck and landscape distances between the two scales' persistence diagrams are computed using GUDHI, as described in Section 2.4.

### 2.7 Software and Reproducibility

All analyses were performed in Python 3.11. Persistence diagrams are computed with Ripser.py 0.6.12 (Bauer, 2021; Tralie et al., 2018); bottleneck distances and landscape representations use GUDHI 3.11.0; giotto-tda 0.6.0 provided independent cross-checks. Supporting scientific Python packages match the pinned `requirements.txt` accompanying the manuscript: NumPy 2.0.2, SciPy 1.13.1, pandas 2.3.2, scikit-learn 1.6.1. Analysis code, pipeline configuration, and pinned dependencies are included with the manuscript materials and will be released in a public repository at arXiv posting (see Data Availability Statement).

---

## 3. Results

### 3.1 Scale-Specific Connected Components (*H*₀)

Without clustering, *H*₀ persistence diagrams encode the full 22-point hierarchical merging sequence in a single object; scale decomposition recovers organisation at each specific scale instead. At the individual scale (*δ* = 2.98 m), *H*₀ = 19.02 ± 2.47 (mean ± s.d.) varies with local player proximity. At the tactical scale (*δ* = 12.0 m), *H*₀ = 4.77 ± 1.60 counts the number of distinct tactical groups. At the team scale (*δ* = 30.0 m), clustering yields a mean of 1.44 ± 0.50 clusters: 56.0% of frames place all 22 players in a single cluster, 44.0% split them into two. This three-scale structure holds across all ten matches (individual *H*₀ = 19.05 ± 0.39, tactical *H*₀ = 4.92 ± 0.36, team cluster count 1.38 ± 0.08, grand means ± across-match s.d.), with every match falling inside the expected range at every scale.

### 3.2 *H*₁ Loop Detection

The framework detects 403 *H*₁ loops across the 150 analysis frames of the primary match (Table 1). Individual-scale loops are frequent and transient: they appear in 143 of 150 frames (95.3%) at a mean rate of 2.55 per frame, with low mean persistence (1.977 ± 1.128 m). Tactical-scale loops are rarer but substantially more persistent: they appear in 19 frames (12.7%) at a mean rate of 0.14 per frame, with mean persistence 3.797 ± 3.008 m and a maximum of 10.771 m. Team-scale loops never occur, with *H*₁ = 0 across all 1,500 frames in the multi-match sample.

**Table 1.** Single-match *H*₁ statistics (primary match, 150 frames).

| Scale | Total loops | Frames with loops | Mean loops/frame | Mean persistence | Max persistence |
|-------|-------------|-------------------|------------------|------------------|-----------------|
| Individual (2.98 m) | 382 | 143/150 (95.3%) | 2.55 | 1.977 ± 1.128 | 12.991 |
| Tactical (12.0 m) | 21 | 19/150 (12.7%) | 0.14 | 3.797 ± 3.008 | 10.771 |
| Team (30.0 m) | 0 | 0/150 (0%) | N/A | N/A | N/A |

> **Remark (Team-scale *H*₁ vanishes a priori).** At *δ* = 30.0 m the 22 players reduce to *k* ∈ {1, 2} centroids in every frame (Section 3.1). The Vietoris–Rips complex on *k* ≤ 3 points has at most 3 edges, and any filled triangle at *k* = 3 bounds rather than generates a non-trivial 1-cycle. Hence *H*₁ = 0 for every admissible filtration at this scale, independently of the data. Effective team-scale *H*₁ analysis would instead require an alternative representation, such as spatial density fields or Delaunay triangulations. Our *H*₁ analysis therefore operates at two scales, individual and tactical, set against the three-scale *H*₀ decomposition of Section 3.1.

This two-scale structure holds across all ten matches (1,500 uniformly sampled frames; Table 2). Individual-scale *H*₁ presence holds at 97.0% ± 1.5% (95% CI 96.1–97.9%), confirming that loop structures are a near-universal feature of this system at the individual scale. Tactical-scale *H*₁ presence holds at 19.3% ± 7.2% (95% CI 15.3–23.7%), with meaningful variation between matches. The primary match's tactical rate (12.7%) sits within one standard deviation of this ten-match mean; the primary match was selected for broadcast quality and complete event annotation, not for its tactical *H*₁ rate.

**Table 2.** Multi-match *H*₁ statistics (10 matches). Presence rates given with 95% bootstrap CIs (1,000 resamples over matches).

| Scale | Total *H*₁ | Presence rate | 95% CI | Mean persistence | Cross-match s.d. |
|-------|------------|---------------|--------|------------------|------------------|
| Individual | 4,200 | 97.0% ± 1.5% | 96.1–97.9% | 1.854 | 0.163 |
| Tactical | 315 | 19.3% ± 7.2% | 15.3–23.7% | 0.666 | 0.299 |
| Team | 0 | 0.0% ± 0.0% | – | N/A | N/A |

Mean persistence in Table 2 averages over all sampled frames, including frames with no *H*₁ feature, so the tactical value is lower than the primary-match mean in Table 1, which is computed only over detected loops.

### 3.3 Closed Cycle Structures

Closed-cycle identification recovers a geometric realisation for every one of the 403 single-match *H*₁ generators. Individual-scale cycles typically comprise 3–6 nodes (cluster centroids), forming small ring-like player arrangements. Tactical-scale cycles comprise 4–5 nodes at higher persistence, forming larger-scale formation gaps. Figure 1 shows the highest-persistence cycle at each scale for the primary-match 150-frame sample: sample frame 141 at the individual scale (persistence 12.991 m) and sample frame 97 at the tactical scale (persistence 10.771 m).

> **Figure 1** (`figures/fig2_cycle_geometry.pdf`). Geometric realisation of maximal-persistence *H*₁ loops at individual (*δ* = 2.98 m) and tactical (*δ* = 12.0 m) scales for SkillCorner match 1996435. Individual panel: sample frame 141 (*p* = 12.991 m); tactical panel: sample frame 97 (*p* = 10.771 m). Uniform sample, *n* = 150 frames, every 290th complete frame.

### 3.4 Scale Complementarity

The two *H*₁ scales are weakly correlated but capture largely distinct topological information. Across all 1,500 uniformly sampled frames from the ten matches, individual-scale and tactical-scale *H*₁ counts correlate weakly (Spearman *ρ* = 0.264, *p* < 0.001; 95% match-level bootstrap CI [0.200, 0.314]). Presence of *H*₁ at the two scales co-occurs more often than chance: Fisher's exact test gives an odds ratio of 10.91 (*p* < 0.001), with match-level bootstrap CI [2.59, 13.53] reflecting heterogeneity between matches. The weak rank correlation remains the primary evidence of complementarity: above-chance co-occurrence does not imply that the two scales measure the same structure.

A TDA-native comparison, independent of these rank-based summaries, confirms the same picture. Across all 1,500 sampled frames, the bottleneck distance between the individual-scale and tactical-scale persistence diagrams has median 1.511 m and a 95th-percentile tail of 7.994 m, comparable to the tactical scale's own mean persistence (3.797 m, Table 1), while the landscape *L*² distance has median 5.671. Both distances are large relative to the scales' own persistence values, confirming the two diagrams are typically far apart in the relevant metric. Individual-scale loops can and frequently do occur without a co-occurring tactical-scale loop, and vice versa: the two scales are complementary, not redundant, views of the same point cloud.

### 3.5 Sensitivity Analysis

*H*₁ detection responds monotonically to the tactical-scale cutoff: across *δ* ∈ [6, 16] m on the 150 frames of the primary match, total *H*₁ count and frame presence fall from 275 loops (87.3% of frames) at *δ* = 6 m to zero at *δ* = 16 m, with the effective operative range therefore [6, 14] m (Table 3). The chosen *δ* = 12.0 m sits at the conservative end of this range, at 12.7% frame presence, consistent with the single-linkage philosophy of prioritising fewer but more robust loops over a larger but noisier set.

**Table 3.** Tactical-scale cutoff sensitivity (150 frames, primary match).

| *δ* (m) | Total *H*₁ | Frame presence | Mean *H*₀ |
|---------|------------|----------------|-----------|
| 6 | 275 | 87.3% | 13.4 |
| 8 | 162 | 68.0% | 9.8 |
| 10 | 78 | 42.7% | 7.0 |
| 12 | 21 | 12.7% | 4.8 |
| 14 | 5 | 3.3% | 3.5 |
| 16 | 0 | 0.0% | 2.8 |

The adaptive filtration formula (equation 1) is insensitive to its percentile parameter: at *δ* = 12.0 m, every percentile from *P*₅₀ to *P*₉₅ returns identical results: 21 loops at 12.7% frame presence. The corresponding maximum filtration scale ranges from 38.5 m to 65.6 m (Table 4), but *H*₁ detection is entirely insensitive to this variation.

**Table 4.** Adaptive filtration percentile ablation, *δ* = 12.0 m.

| Percentile | Total *H*₁ | Frame presence | Max *ε*_max (m) |
|------------|------------|----------------|-----------------|
| *P*₅₀ | 21 | 12.7% | 38.5 |
| *P*₆₀ | 21 | 12.7% | 42.7 |
| *P*₇₅ | 21 | 12.7% | 50.3 |
| *P*₉₀ | 21 | 12.7% | 60.5 |
| *P*₉₅ | 21 | 12.7% | 65.6 |

### 3.6 Event Correlation

As a check that the detected *H*₁ features reflect genuine spatial structure rather than measurement noise, we tested for association between persistence and real match events using SkillCorner's annotations across all ten matches (104,722 event–topology pairs). Directionally, events that disrupt team shape, including on-ball engagements and quick breaks, are followed by a fall in persistence, while sustained build-up play is followed by a rise (Mann–Whitney *U* on pre-specified event classes; several contrasts have nominal *p* < 0.001 at both scales). We treat this only as a construct-validity check: full multiple-testing control and football-specific interpretation are deferred to forthcoming work.

---

## 4. Discussion

### 4.1 Methodological Contributions

Each component of this pipeline has precedent considered in isolation: hierarchical clustering before persistent homology underlies Schindler and Barahona's (2023) analysis of multiscale clusterings, and adapting a filtration threshold to local geometry is not new in principle. The contribution is empirical validation that the combination is robust enough for a real, high-frequency, noisy point cloud, which neither prior treatment establishes on its own. The result most relevant to a practitioner is the width of the pipeline's safe operating range: *H*₁ detection holds across cutoffs from 6 to 14 m and across every filtration percentile from *P*₅₀ to *P*₉₅ tested (Section 3.5). A method effective only at one finely-tuned parameter setting would be a substantially weaker contribution than one effective across a broad, empirically mapped range; this property is what makes the pipeline transferable to other multi-agent systems rather than a method tuned narrowly to this dataset.

The cutoff distance functions as a scale selector rather than a parameter to be optimised away. The three validated regimes, individual, tactical, and team, emerge from a systematic sweep over *δ* ∈ [0.5, 30.0] m, are validated by independent clustering-quality metrics, and recur across all ten matches. The tactical cutoff sits within a range where automated metrics disagree (6.87–16.31 m); its value is accordingly a domain-informed choice rather than an automatically optimal one, and the sensitivity analysis demonstrates that this choice does not compromise robustness.

The adaptive filtration formula addresses a coupling between the clustering and filtration steps: clustering alters the point cloud's geometry, so a fixed filtration threshold suitable at one scale produces null *H*₁ results at another. The *P*₇₅ percentile is a reporting convention: all tested percentiles from *P*₅₀ to *P*₉₅ return identical *H*₁ totals and presence rates. The same formula applies to any multi-scale pipeline that uses clustering as a preprocessing step before persistent homology, independent of the application domain.

### 4.2 Multi-Scale Topological Structure

The weak correlation and the divergent presence rates reported in Section 3.4 together support the same conclusion: the two scales are not measuring the same underlying structure at different resolutions, but capturing structurally distinct phenomena. If the tactical-scale signal were simply a coarsened version of the individual-scale signal, the two would be expected to co-occur far more consistently than the data show, and the bottleneck and landscape distances would be small relative to each scale's own persistence values rather than comparable to or exceeding them. Decomposing by scale before computing persistent homology is therefore not merely a convenience for separating noise; the decomposition recovers two informationally distinct objects, supporting the methodological case made in Section 2.4 that the clustering step does genuine analytical work rather than relabelling structure already visible in the undecomposed point cloud.

### 4.3 Limitations

Linkage selection is a substantive methodological choice rather than a matter of conservative versus liberal estimation. Across a 600-frame, four-match comparison sample, single-linkage detects 153 tactical-scale *H*₁ loops, against 923 for complete-linkage and 936 for Ward's method, a difference of almost an order of magnitude, large enough to change which scientific picture the data support rather than merely the precision of one estimate. We retain single-linkage here because its definition, clusters as chains of short pairwise distances, is the most natural reading of spatial proximity and is robust against over-partitioning artefacts, but we treat the gap with the other two methods as an open question rather than a settled one. A more principled selection criterion would come from the dynamical system itself rather than from clustering-quality metrics alone. The appropriate criterion is the linkage method under which a governing equation for a persistence functional, specifically the landscape *L*² norm or the tactical *H*₁ total-persistence sequence, admits the sparsest representation in the sense of sparse identification of nonlinear dynamics. Operationalising this criterion would require three things: choosing the dynamical state, defending the sparsity of the recovered library against AIC, BIC, or cross-validation baselines, and confirming that the resulting persistence sequence is genuinely lower-dimensional under the selected linkage. We defer this to the forthcoming full-season work, where a population-sized sample of match sequences makes the sparsity comparison meaningful.

The tactical cutoff of 12.0 m is a domain-informed choice situated within, rather than derived from, an automated-metric range: the silhouette-optimal value is 16.31 m and the information-content-optimal value is 6.87 m, with 12.0 m falling between them. The justification given in Section 2.3, namely correspondence to half a standard football zone width, is domain-reasonable but ultimately a judgement call. The sensitivity analysis in Section 3.5 reports the resulting operative range, [6, 14] m, as an empirical property rather than a derivation of the chosen value. A more principled criterion would select the cutoff minimising the variation of the persistence landscape path under small perturbations of *δ*. This is computable with the same landscape infrastructure used in Section 3.4, but the relevant sample size for estimating that variance is the number of matches, not the number of frames, so evaluating it on the present ten-match sample would be premature. We defer this to the persistence-landscape companion work and treat 12.0 m as a domain-informed reference point within the validated [6, 14] m range rather than an optimised value.

The framework identifies three *H*₀ regimes but only two *H*₁ regimes. The absence of team-scale *H*₁ is a structural consequence of the clustering reducing the point cloud to one or two centroids at *δ* = 30.0 m, not a limitation of the persistent homology computation itself. Detecting team-scale loop structure would require an alternative representation, such as spatial density fields or Delaunay triangulations, rather than a centroid-based point cloud at any cutoff.

All data analysed here are broadcast-derived tracking at 10 Hz. Broadcast tracking typically offers lower spatial precision than higher-frequency optical systems, which may affect the magnitude of persistence values reported. The structural findings, namely the three scale regimes, the *H*₁ presence rates, and the sensitivity profiles, are expected to be robust across tracking technologies, since they depend on relative rather than absolute spatial precision. A direct comparison of persistence magnitudes against optical tracking data remains for future work.

### 4.4 Outlook

Two extensions of this work are in progress, and a third output sits alongside it rather than ahead of it. The ten-match evidence base presented here is being scaled to a full season of Championship matches to characterise population-level distributions of *H*₀ and *H*₁ counts, barcode lengths, and landscape norms, and to test tactical-fingerprint classification at population scale; this is also the setting in which the SINDy-based linkage criterion proposed above becomes evaluable, since recovering a sparse governing equation for a persistence functional requires the population-sized sample of match sequences that a single season provides. Separately, persistence landscape dynamics are being developed to treat each match as a path through landscape space, which is the setting in which the landscape-stability cutoff criterion can itself be evaluated, since its resampling unit is the match-level landscape rather than the per-frame summary used throughout the present analysis.

Alongside these extensions, a companion paper (Brown et al., forthcoming / Paper B) interprets the present ten-match findings for a football-analytics readership: event correlation as a central result rather than a brief validity check, a comparison against standard geometric descriptors, bilateral home-and-away coupling, and a cross-validated test of predictive utility for phase-of-play classification. That paper depends methodologically on the framework validated here but answers a different question, asking what these topological measures reveal about football specifically rather than whether the framework itself is sound.

---

## 5. Conclusion

This paper introduces a multi-scale persistent homology framework for competitive multi-agent point clouds, validated on ten professional football matches. Two methodological contributions, domain-informed scale decomposition and an adaptive Vietoris–Rips filtration, resolve the scale-conflation problem that arises when a single filtration is applied directly to a hierarchically organised point cloud. The resulting three *H*₀ regimes and two *H*₁ regimes are stable across independent matches and across wide ranges of the framework's two free parameters, and the two *H*₁ scales carry complementary rather than redundant information. Football served here only as a validated testbed; the framework itself is intended for any bounded competitive multi-agent system with spatial tracking data.

---

## Declarations

### Competing Interests

The authors have no relevant financial or non-financial interests to disclose.

### Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors; it was conceived and conducted independently by the authors.

### Data Availability Statement

Positional tracking data were provided by SkillCorner under an open-data licence (<https://github.com/SkillCorner/opendata>). Analysis code, pipeline configuration, pinned `requirements.txt`, and the result files used for the figures and tables in this paper are included with the manuscript materials and will be released in a dedicated public repository at arXiv posting.

### Use of Large Language Models

Large language model (LLM) tools were used during the preparation of this manuscript to assist with prose structuring and copy-editing. All scientific content, analyses, interpretations, and conclusions are the sole responsibility of the authors. No LLM tool was used to generate novel scientific claims or to conduct or interpret statistical analyses.

---

## Discussion checklist (flagged while converting)

1. ~~**Authorship (S4)**~~ — **Confirmed:** Rowan Brown sole author.
2. ~~**Spearman *ρ* (C3)**~~ — **Resolved:** 0.264 on all 1,500 frames; Fisher OR 10.91.
3. ~~**Dockerfile / versions (C4)**~~ — **Resolved:** no Dockerfile claim; Methods pins match `requirements.txt`; public repo URL deferred to arXiv posting.
4. ~~**Sampling (C2)**~~ — **Resolved:** every 290th complete frame.
5. ~~**Figure PDF (S5)**~~ — **Resolved:** frames 141 / 97 (Table 1 maxima); regenerate via `pipeline/steps/06_figures.py`.
6. ~~**Team cluster count (S1)**~~ — **Resolved:** team scale reported as mean cluster count 1.44 ± 0.50 (56%/44%), not the Ripser `h0_team` field (0.88).
7. ~~**Table 1 vs 2 persistence (S2)**~~ — **Resolved:** clarifying clause added after Table 2.
8. ~~**Event FDR (S6)**~~ — **Resolved:** construct-validity framing; FDR deferred to Paper B.
