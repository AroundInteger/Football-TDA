# Multi-Scale Persistent Homology for Competitive Spatial Systems

> **Working copy (28 August 2026).** Edit here while Overleaf is unavailable; `**sections/*.tex` remains the submission source of truth**. After Results/Discussion edits settle, sync changes back into the `.tex` files (Results §3 updated this session).

**Authors:** Rowan Brown  
**Affiliation:** Swansea University  

**Target:** *Journal of Applied and Computational Topology* (JACT); arXiv preprint  
**Status:** Working manuscript. Not yet submitted. Results §3 below matches `sections/results.tex` after the 28 Aug review edits.

**This file.** Markdown working copy for read/edit/iterate in Cursor. Compile `Paper_A_collaborator.tex` or `main.tex` for a typeset PDF when needed.

**Citations** are author–year, matching the JACT manuscript (`natbib` name–year). They are not Vancouver numbers.

---

## Note for collaborators

**What this paper is.** A mathematics-first methods paper. It asks whether a multi-scale persistent homology pipeline is *sound* on a real, high-frequency, noisy multi-agent point cloud. Football is the validated testbed, not the audience.

**What it is not.** A football-analytics paper. Event interpretation, geometric baselines, bilateral (home/away) coupling, and predictive utility belong to a companion manuscript (Paper B, *Journal of Sports Sciences*, in preparation). Paper A treats event correlation only as a one-sentence construct-validity check (“not noise”).

**Headline claim.** Domain-informed hierarchical clustering plus a data-driven Vietoris–Rips truncation resolves scale conflation in competitive spatial systems. On ten professional matches the pipeline recovers three stable $H_0$ regimes and two $H_1$ regimes; the two $H_1$ scales carry distinct information; every examined $H_1$ feature has a geometric cycle representative.

**Locked cutoffs (metres).** Individual $2.98$; tactical $12.0$ (domain-informed, inside a metric-disagreement range); team $30.0$. Operative tactical $H_1$ range: $[6, 14]$ m.

**Sample.** Ten A-League matches, SkillCorner open broadcast tracking at $10$ Hz. Persistent homology on $150$ uniformly spaced complete frames per match ($1{,}500$ frames in total). Primary match: SkillCorner ID $1996435$, $43{,}531$ complete $22$-player frames.

**Open methodological questions (already flagged in the paper).** Linkage choice (single vs complete vs Ward changes tactical $H_1$ by nearly an order of magnitude); a more principled tactical cutoff; team-scale $H_1$ needs a different representation (centroids collapse to $k\in1,2$).

**Suggested first read.** Abstract → §1.2–1.3 → equation (1) → Tables 1–2 and the null table → §4.3 Limitations. Skip §2.7 and Declarations unless you are checking reproducibility.

---

## Abstract

Standard single-parameter Vietoris–Rips persistent homology applied to a multi-agent point cloud conflates topological features from distinct organisational levels into a single diagram. We present a multi-scale framework addressing this through two methodological contributions: domain-informed hierarchical clustering, with cutoff distances validated by independent clustering-quality metrics, that decomposes the point cloud by organisational level; and an adaptive Vietoris–Rips filtration, scaled to the post-clustering point cloud's geometry, that keeps $H_1$ (loop) detection consistent across scales. Validated on ten professional football matches (broadcast tracking at $10$ Hz), the framework identifies three stable $H_0$ (connected-component) regimes: individual ($2.98$ m), tactical ($12.0$ m), and team ($30.0$ m), and two $H_1$ regimes: individual-scale loops are frequent and transient ($97.0 \pm 1.5$ frame presence across matches), tactical-scale loops are rarer but more persistent ($19.3 \pm 7.2$); team-scale $H_1$ is absent a priori as a structural consequence of the clustering. Both regime structures hold across matches and across wide ranges of the cutoff distance and the filtration's percentile parameter, and the two $H_1$ scales carry distinct rather than redundant information (Spearman $\rho = 0.264$ across $1{,}500$ sampled frames). Geometric cycle representatives are recovered for every $H_1$ generator examined. A minimal association between persistence and match events confirms the detected features track genuine structure rather than measurement noise. The framework is domain-agnostic and intended for any bounded competitive multi-agent system with spatial tracking data; football serves as a validated testbed.

**Keywords:** persistent homology, multi-scale topology, Vietoris–Rips filtration, multi-agent systems, spatial tracking data, sports analytics

---

## 1. Introduction

### 1.1 Background

Competitive spatial systems, collections of agents that interact, coordinate within groups, and compete between groups within a bounded domain, are ubiquitous. Autonomous vehicle fleets sharing road space, opposing crowd flows at transport hubs, predator–prey populations in an ecosystem, and sports teams contesting territory all share this structure. Such systems characteristically operate across multiple spatial scales at once: individual agent decisions at the scale of metres, small-group coordination at tens of metres, and whole-system organisation at hundreds of metres. Understanding how these scales interact is a standing challenge in applied mathematics, and one that high-frequency spatial tracking data is increasingly able to inform.

Agents within such systems can arrange themselves in ring-like formations that enclose empty space: a pressing trap encircling a player in possession, or a gap between two organisational units that creates room to manoeuvre. These arrangements have a topological character: they are loops in the position data, and their persistence over time distinguishes deliberate structural organisation from transient clustering. Conventional geometric summaries, including convex-hull area, nearest-neighbour distance, and the range of agent positions along each axis, capture different aspects of spatial dispersion but do not directly quantify this loop structure.

Persistent homology, the central tool of topological data analysis, provides a principled way to detect and measure such formations across scale. A filtration of simplicial complexes indexed by a scale parameter tracks the birth and death of topological features, recovering multi-scale structure in a mathematically rigorous way; applications span protein structure, materials science, and collective behaviour. Applying standard single-parameter persistent homology directly to a multi-agent point cloud, however, presents a practical difficulty that motivates the framework developed here.

### 1.2 The Scale Conflation Problem

A single Vietoris–Rips filtration applied to a multi-agent point cloud computes topological features across all spatial scales simultaneously, encoding the full hierarchical clustering structure of the point cloud, from individual proximity through small-group formation to system-wide organisation, within a single persistence diagram. For exploratory analysis of a system with no known hierarchical structure, this is a strength: every scale is examined without prior commitment to which one matters. For a system with known hierarchical organisation across distinct spatial scales, it is instead a practical obstacle. Topological features from different organisational levels are superimposed in the same diagram, making it difficult to attribute a given feature to a given scale or to track scale-specific dynamics over time. This challenge is recognised in the topological data analysis literature, and Section 1.4 positions the present approach against it in detail.

We take a domain-informed path rather than developing new algebraic machinery: the point cloud is decomposed by organisational level through hierarchical clustering at validated cutoff distances, and scale-specific persistent homology is computed on each reduced point cloud in turn. This decomposition introduces a second problem that a single-scale analysis never encounters. Clustering changes the point cloud's geometry at each scale, so a fixed Vietoris–Rips threshold suitable at one organisational level produces null $H_1$ results at another. The adaptive filtration developed in Section 2.4 resolves this second problem.

### 1.3 Contributions

This paper makes four contributions, two methodological and two empirical.

**Methodologically**, it introduces domain-informed scale decomposition: a hierarchical clustering preprocessing step, with cutoff distances validated by independent clustering-quality metrics, that separates organisational levels and enables scale-specific topological analysis of a multi-agent point cloud. It also introduces an adaptive filtration: a data-driven maximum filtration scale that adjusts to the post-clustering point cloud's geometry, ensuring $H_1$ detection remains consistent across analysis scales rather than collapsing to zero at scales the original threshold was not designed for.

**Empirically**, it provides multi-match scale validation: a systematic sweep of the cutoff distance over $[0.5, 30.0]$ m identifies three stable analysis regimes, confirmed across ten independent matches rather than a single demonstration case. It also provides multi-scale topological characterisation: detection of $H_1$ loops at two of the three scales, geometric realisation demonstrated for every generator in the primary-match analysis, evidence that the two $H_1$ scales carry distinct rather than redundant information, and a minimal correlation with real match events confirming the detected features track genuine structure rather than measurement noise.

### 1.4 Related Work

Persistent homology was introduced by Edelsbrunner et al. (2002) and placed on firm computational foundations by Zomorodian and Carlsson (2005). Stability of persistence diagrams under perturbation was established by Cohen-Steiner et al. (2007), and efficient computation via the Vietoris–Rips filtration is provided by Bauer (2021). Persistence landscapes provide a functional representation suitable for statistical analysis (Bubenik, 2015).

Applications of persistent homology to collective behaviour include Topaz et al. (2015), who applied the method to biological aggregation models and visualised scale-dependent structure by plotting Betti numbers across both simulation time and filtration value. Gu et al. (2022) applied Vietoris–Rips persistent homology to multi-agent system snapshots for change-point detection, demonstrating the utility of topological features for temporal dynamics, though their analysis operates at a single scale rather than decomposing by organisational level. The multiparameter persistence literature, surveyed by Botnan and Lesnick (2023), provides a theoretical framework for genuinely simultaneous multi-scale analysis, but computational cost currently limits its application to point clouds much smaller than the $22$-agent, high-frequency case considered here. Schindler and Barahona (2023) address hierarchical decomposition directly, developing tools for analysing multiscale clusterings with persistent homology; the present work differs in providing an explicit mechanism, the adaptive filtration of Section 2.4, for keeping $H_1$ detection consistent as the clustering scale itself changes the point cloud's geometry, a coupling that arises specifically when clustering precedes single-parameter persistent homology, and in validating the resulting scale regimes empirically across ten independent real matches rather than within a single theoretical or simulated setting.

In sports analytics specifically, spatial analysis methods including pitch-control models and spatio-temporal pattern recognition are surveyed in Gudmundsson and Horton (2017). Related perspectives model teams as coordinated multi-agent systems and apply network metrics to passing and collective structure (Buldú et al., 2019; Grund, 2012); these approaches complement the present framework but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines domain-informed scale decomposition with persistent homology for a competitive, high-frequency spatial system, or validates the resulting scale regimes across multiple independent matches.

---

## 2. Methods

### 2.1 Data

The primary single-match analysis uses SkillCorner open broadcast tracking data, match ID $1996435$ (Sydney FC versus Adelaide United, A-League 2024/25), at $10$ frames per second. We retain only frames with complete $22$-player coverage, yielding $43{,}531$ frames, approximately $72$ minutes of play at this sampling rate; positions are $(x, y)$ coordinates in metres on a standard pitch model. Nine additional A-League matches, each comprising approximately $40{,}000$–$48{,}000$ frames, were obtained from the same repository to validate the framework's generalisability across teams, tactical systems, and competition contexts.

Native tracking is $10$ Hz. Consecutive complete frames are highly autocorrelated, so pooling the full stream as independent draws would inflate precision. For prevalence and scale-regime analysis we therefore subsample. The operational rule is the same on every match: list complete $22$-player frames, set the stride to $\lfloor N/150\rfloor$, and retain $150$ frames. On the primary match $N = 43{,}531$, so the stride is $290$ frames ($\approx 29$ s). That yields a fixed-cardinality sample of $1{,}500$ frames across ten matches. The design limits temporal pseudo-replication; it does not establish statistical independence, and it does not resolve formation or dispersion of loops between samples. Event association uses the native-rate stream and is a construct-validity check, not a dynamical model. Supplementary Figure S1 reports autocorrelation of frame-level topological summaries on the primary match at $1$ Hz. Residual correlation is already weak by $10$--$20$ s, so the operational stride is conservative relative to that diagnostic. The autocorrelation plot does not choose the stride.

### 2.2 Proximity-Aware Clustering

Figure 1 summarises the pipeline of Sections 2.2--2.5. At each time step $t$, the $22$ player positions form a point cloud $P(t) = \{p_1(t), \dots, p_{22}(t)\} \subset \mathbb{R}^2$. Computing persistent homology directly on $P(t)$ produces a single diagram encoding inter-agent distance relationships at all scales simultaneously; to separate organisational levels before computing topology, we preprocess with hierarchical clustering.

> **Figure 1** (`figures/fig1_pipeline_schematic.pdf`). Methods schematic covering clustering (Section 2.2), adaptive Vietoris--Rips truncation (Section 2.4), and the graph-cycle proxy (Section 2.5). Toy geometry; homology is on centroids, not the raw 22-player cloud.

For a cutoff distance $\delta > 0$, single-linkage hierarchical clustering partitions $P(t)$ into clusters $C_1, \dots, C_k$ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding $\delta$. The reduced point cloud is the set of cluster centroids,

$ \tilde{P}(t)=\left\bar{c}_j : \bar{c}*j=\frac{1}{|C_j|}\sum*{p\in C_j} p, j=1,\dots,k\right, $

and persistent homology is computed on $\tilde{P}(t)$ rather than on $P(t)$ itself.

We use single-linkage throughout. Its definition, clusters as chains of points connected by short pairwise distances, is the most direct reading of spatial proximity, and it produces a conservative estimate of $H_1$ features: reported loops represent robust topological structure rather than artefacts of over-partitioning. Section 4.3 examines the consequences of this choice relative to complete-linkage and Ward's method.

The framework extends to labelled sub-populations by running the same pipeline independently on each label's point cloud rather than on the merged $22$-player cloud; we use this here only to confirm the method is agnostic to such relabelling. The substantive application, decomposing by team identity and examining bilateral tactical coupling, is deferred to forthcoming work.

### 2.3 Domain-Informed Cutoff Distance Selection

The cutoff distance $\delta$ functions as a scale selector rather than a free parameter, since it determines which level of organisation the resulting point cloud represents. We swept $\delta$ over $[0.5, 30.0]$ m at $100$ test points, evaluated against $58$ temporal windows sampled to give balanced coverage across four epoch lengths ($1$, $2$, $5$, and $10$ minutes). Three candidate cutoff values were identified using three independent clustering-quality criteria: the Calinski–Harabasz index, the silhouette score, and a domain-specific information-content measure.

To quantify how reproducible the resulting partition is across the temporal windows, we define the *cross-epoch stability* of a cutoff as follows. Pool every sweep evaluation whose cutoff lies within $0.5$ m of the selected value, take the median cluster count over that pool, and record the fraction of those evaluations whose cluster count lies within $\pm 2$ of the median. A score of $1$ means the partition is reproduced to within two clusters in every window at every epoch length; a low score means the cluster count is an artefact of the window chosen. At the adopted cutoffs, the individual scale scores $0.875$ at $2.98$ m, the tactical scale scores $0.836$ at $12.0$ m, and the team scale scores $1.000$ at $30.0$ m.

The individual-scale cutoff of $2.98$ m is carried over from an earlier normalised-coverage calibration on this dataset and is retained here because it places the expected $H_0$ count in the individual regime validated by the sweep ($15$–$22$ clusters). The sweep's Calinski–Harabasz optimum lies at $1.39$ m (stability $0.956$); we do not adopt it, because that finer partition sits below the validated individual $H_0$ band on average. The team-scale cutoff, $30.0$ m, is selected directly by the automated metrics. The tactical-scale cutoff is selected differently, because the automated metrics disagree within the tactical range: the silhouette-optimal value is $16.31$ m and the information-content-optimal value is $6.87$ m. We select $12.0$ m, corresponding to half the width of a standard football pitch zone, as a domain-informed value within this range rather than as the output of either metric. Section 3.5 reports the resulting sensitivity of $H_1$ detection to this choice.

### 2.4 Adaptive Filtration for $H_1$ Detection

Clustering at cutoff $\delta$ produces a reduced point cloud $\tilde{P}(t)$ whose inter-centroid distances are typically much larger than $\delta$ itself, so a fixed maximum filtration scale $\varepsilon_{\max}$ that is appropriate at one cutoff is insufficient for $H_1$ detection at another. We define an adaptive filtration,

$$
\varepsilon_{\max} = \max\Big(P_{75}d(\bar c_i,\bar c_j) : i<j, \max(5.0,2\delta)\Big),
\tag{1}
$$

where $P_{75}$ denotes the 75th percentile of pairwise inter-centroid distances. The first term adapts the filtration to the geometry of the reduced point cloud at each $\delta$; the second term imposes a floor proportional to the clustering scale, preventing degenerate filtration at small $\delta$ and ensuring the filtration reaches at least the inter-cluster distance regime.

The $P_{75}$ percentile is chosen as a conventional upper-quartile summary of inter-centroid distances. Section 3.5 reports an ablation across $P_{50}$ through $P_{95}$, showing that every tested percentile returns identical $H_1$ totals and frame-presence rates; the choice of $P_{75}$ is therefore a reporting convention, not an optimisation.

Persistence diagrams are computed with Ripser via Ripser.py (Bauer, 2021). We cross-checked all primary-match diagrams against GUDHI (The GUDHI Project, 2024) and giotto-tda (Tauzin et al., 2021), confirming identical birth–death pairs to within numerical tolerance ($10^{-6}$ m); GUDHI is also used for the bottleneck-distance and landscape computations reported in Section 3.4.

### 2.5 Closed Cycle Identification

Each $H_1$ feature corresponds to a 1-cycle in the Vietoris–Rips complex. To recover its geometric realisation, we build the adjacency graph of edges whose distances fall within the feature's persistence interval $[\text{birth}, \text{death}]$, then enumerate closed cycles of length at least $3$ by breadth-first search from each vertex. If that graph yields no cycle, we fall back to edges with length in $[\tfrac{1}{2}\text{birth}, \text{death}]$. Breadth-first search is used in preference to depth-first search because it prioritises shorter cycles, which correspond to minimal enclosing arrangements and are more directly interpretable as formation structures. Among the enumerated cycles, the one whose edge distances lie closest to the midpoint of the persistence interval is selected as the geometric representative.

### 2.6 Statistical Tests

To test whether $H_1$ detection reflects the arrangement of cluster centroids rather than merely their number, each frame is compared against a matched null. For a frame whose clustering yields $k$ centroids, the null draws $k$ points uniformly from the convex hull of those same centroids. The null therefore matches the frame on both cardinality and spatial envelope, and randomises only the arrangement. The adaptive filtration of equation (1) is recomputed on each null cloud, so nothing else differs between the two. We use $200$ null replicates per frame and report the excess of observed over null $H_1$ presence, with $95$ confidence intervals from bootstrap resampling over matches.

Scale complementarity (Section 3.4) is assessed by two frame-level tests comparing the individual and tactical scales. The Spearman rank correlation is computed on total $H_1$ persistence, the sum of death minus birth over all finite $H_1$ bars in a frame; we also report it on loop counts as a robustness check. Fisher's exact test is computed on the binary co-occurrence of $H_1$ presence at the two scales. Both statistics carry $95$ confidence intervals obtained by bootstrap resampling over matches ($1{,}000$ resamples), the match being the resampling unit. Bottleneck and landscape distances between the two scales' persistence diagrams are computed using GUDHI, as described in Section 2.4.

### 2.7 Software and Reproducibility

All analyses were performed in Python 3.11. Persistence diagrams are computed with Ripser.py 0.6.12 (Bauer, 2021; Tralie et al., 2018); bottleneck distances and landscape representations use GUDHI 3.11.0; giotto-tda 0.6.0 provided independent cross-checks. Supporting scientific Python packages match the pinned `requirements.txt` accompanying the manuscript: NumPy 2.0.2, SciPy 1.13.1, pandas 2.3.2, scikit-learn 1.6.1. Analysis code, pipeline configuration, and pinned dependencies are included with the manuscript materials and will be released in a public repository at arXiv posting (see Data Availability Statement).

---

## 3. Results

### 3.1 Scale-Specific Connected Components ($H_0$)

Applied to all 22 players at once, a single $H_0$ diagram encodes the full hierarchical merging sequence in one object. Clustering first separates organisational levels; the counts below then describe each level on its own. Throughout, $H_0$ is the number of cluster centroids, equivalently $\beta_0$ of the Vietoris–Rips complex on those centroids at filtration zero.

Primary-match figures come from the uniform 150-frame sample of match 1996435 (Section 2.1). Ten-match aggregates use the same sampling scheme in the validation pipeline (1,500 frames in total).

At the individual scale ($\delta = 2.98$ m), $H_0 = 19.02 \pm 2.47$ (mean $\pm$ s.d.; range $9$–$22$), reflecting how tightly players cluster locally. At the tactical scale ($\delta = 12.0$ m), $H_0 = 4.77 \pm 1.60$ (range $2$–$10$) counts distinct tactical groups. At the team scale ($\delta = 30.0$ m), the cloud usually collapses to one or two clusters: mean $1.44 \pm 0.50$, with all 22 players in a single cluster in $56.0\%$ of frames and split across two in $44.0\%$.

The same three-scale pattern holds in all ten matches. Grand means are individual $H_0 = 19.05 \pm 0.41$, tactical $H_0 = 4.92 \pm 0.36$, and team cluster count $1.38 \pm 0.08$ (mean $\pm$ s.d. across matches). Every match stays within the validated $H_0$ bands of Section 2.3.

### 3.2 $H_1$ Loop Detection

On the primary match, the pipeline detects $403$ $H_1$ loops across 150 uniformly sampled frames (Table 1). Individual-scale loops are frequent and short-lived: they appear in $143$ of $150$ frames ($95.3\%$), at a mean rate of $2.55$ per frame, with low mean persistence ($1.977 \pm 1.128$ m). Tactical-scale loops are rarer but last longer: $19$ frames ($12.7\%$), mean rate $0.14$ per frame, mean persistence $3.797 \pm 3.008$ m, maximum $10.771$ m. Team-scale loops never occur ($H_1 = 0$ across all $1{,}500$ frames in the ten-match sample).

**Table 1.** Single-match $H_1$ statistics (primary match, $150$ frames).


| Scale                 | Total loops | Frames with loops  | Mean loops/frame | Mean persistence  | Max persistence |
| --------------------- | ----------- | ------------------ | ---------------- | ----------------- | --------------- |
| Individual ($2.98$ m) | $382$       | $143/150$ ($95.3\%$) | $2.55$           | $1.977 \pm 1.128$ | $12.991$        |
| Tactical ($12.0$ m)   | $21$        | $19/150$ ($12.7\%$)  | $0.14$           | $3.797 \pm 3.008$ | $10.771$        |
| Team ($30.0$ m)       | $0$         | $0/150$ ($0\%$)      | N/A              | N/A               | N/A             |


> **Remark (Team-scale $H_1$ vanishes a priori).** At $\delta = 30.0$ m the 22 players reduce to $k \in \{1, 2\}$ centroids in every frame (Section 3.1). A Vietoris–Rips complex on at most three points cannot carry a non-trivial $1$-cycle: there are at most three edges, and any filled triangle bounds rather than generates a loop. So $H_1 = 0$ at every admissible filtration at this scale, regardless of the data. Team-scale loop structure would require a different representation (density fields or Delaunay triangulations, for example). Our $H_1$ analysis therefore runs at two scales—individual and tactical—against the three-scale $H_0$ decomposition above.

The two-scale $H_1$ pattern extends to all ten matches ($1{,}500$ uniformly sampled frames; Table 2). Individual-scale presence is $97.0\% \pm 1.5\%$ ($95\%$ CI $96.1$–$97.9\%$), between $95\%$ and $99\%$ in every match. Tactical presence is $19.3\% \pm 7.2\%$ ($95\%$ CI $15.3$–$23.7\%$), ranging from $12\%$ to $34\%$ across matches. The primary match ($12.7\%$ tactical) sits within one standard deviation of the ten-match mean. That match was chosen for broadcast quality and event annotation, not for its tactical $H_1$ rate.

**Table 2.** Multi-match $H_1$ statistics ($10$ matches). Presence = mean $\pm$ s.d. across matches; $95$ bootstrap CIs from $1{,}000$ resamples over matches.


| Scale      | Total $H_1$ | Presence rate  | $95$ CI       | Mean persistence | Cross-match s.d. |
| ---------- | ----------- | -------------- | ------------- | ---------------- | ---------------- |
| Individual | $4{,}200$   | $97.0 \pm 1.5$ | $96.1$–$97.9$ | $1.854$          | $0.163$          |
| Tactical   | $315$       | $19.3 \pm 7.2$ | $15.3$–$23.7$ | $0.666$          | $0.299$          |
| Team       | $0$         | $0.0 \pm 0.0$  | —             | N/A              | N/A              |


Mean persistence in Table 2 averages over all sampled frames, including those with no loop. The tactical entry is therefore lower than the primary-match mean in Table 1, which is taken only where loops appear.

Remark 1 explains why $H_1$ vanishes when clustering leaves at most three centroids; the tactical scale sits close to that floor. In the ten-match sample, $44\%$ of frames have four or fewer tactical centroids, and none of them carries a loop. Presence rate alone cannot tell formation geometry from cluster count. We separate the two with the matched null of Section 2.6, which fixes centroid number and spatial envelope and randomises only arrangement.

Table 3 summarises the result. Tactical observed presence is more than twice the null rate. Table 4 splits by centroid count $k$: presence is zero at $k \le 4$, as expected, then rises from $12.0\%$ at $k = 5$ to $75.0\%$ at $k = 8$, always above the null. At the individual scale the null already exceeds $91\%$—twenty points in a bounded region almost always close a cycle—so the observed excess is modest ($+5.8$ pp). Tactical $H_1$ carries information about how units are arranged; individual presence is near-saturated and reads better as background than as a discriminating signal.

**Table 3.** $H_1$ presence against a cardinality- and envelope-matched null ($10$ matches, $1{,}500$ frames, $200$ null replicates per frame). Excess is in percentage points, with $95$ bootstrap CIs over matches.


| Scale      | Observed | Null   | Excess  | $95$ CI         |
| ---------- | -------- | ------ | ------- | --------------- |
| Individual | $97.0\%$ | $91.2\%$ | $+5.8$  | $[+4.8, +6.9]$  |
| Tactical   | $19.3\%$ | $8.3\%$  | $+11.0$ | $[+8.0, +14.1]$ |


**Table 4.** Tactical-scale $H_1$ presence by centroid count $k$, against the matched null of Table 3 ($10$ matches, $1{,}500$ frames).


| $k$     | Frames | Observed | Null   | Excess  |
| ------- | ------ | -------- | ------ | ------- |
| $\le 4$ | $659$  | $0.0\%$  | $0.4\%$  | $-0.4$  |
| $5$     | $357$  | $12.0\%$ | $4.8\%$  | $+7.3$  |
| $6$     | $233$  | $33.5\%$ | $12.5\%$ | $+20.9$ |
| $7$     | $140$  | $56.4\%$ | $23.0\%$ | $+33.4$ |
| $8$     | $72$   | $75.0\%$ | $34.5\%$ | $+40.5$ |
| $\ge 9$ | $39$   | $92.3\%$ | $48.1\%$ | $+44.2$ |


### 3.3 Closed Cycle Structures

All $403$ primary-match $H_1$ features receive a geometric realisation via closed-cycle identification. The representative is the graph-cycle proxy of Section 2.5, not a generator from the reduction matrix. Individual-scale cycles form short rings of centroids (typically three to six nodes in the examples we inspected). Tactical cycles are similarly small (often four or five nodes) but span larger gaps and persist longer. Figure 2 shows the highest-persistence example at each scale: frame $141$ at individual scale ($p = 12.991$ m) and frame $97$ at tactical scale ($p = 10.771$ m).

> **Figure 2** (`figures/fig2_cycle_geometry.pdf`; not embedded in this Markdown copy). Geometric realisation of maximal-persistence $H_1$ loops at individual ($\delta = 2.98$ m) and tactical ($\delta = 12.0$ m) scales for SkillCorner match $1996435$. Individual panel: sample frame $141$ ($p = 12.991$ m); tactical panel: sample frame $97$ ($p = 10.771$ m). Uniform sample, $n = 150$ frames, every $290$th complete frame (same rule as the ten-match analysis).

### 3.4 Scale Complementarity

The two $H_1$ scales carry related but largely distinct information. Over $1{,}500$ uniformly sampled frames, total individual and tactical $H_1$ persistence correlate weakly (Spearman $\rho = 0.264$, $p < 0.001$; $95\%$ bootstrap CI $[0.200, 0.314]$). The same holds for loop counts ($\rho = 0.211$, $p < 0.001$), so the finding does not depend on how persistence is summarised.

Co-occurrence exceeds chance (Fisher odds ratio $10.91$, $p < 0.001$; bootstrap CI $[2.59, 13.53]$), but Table 5 shows the asymmetry: $1{,}166$ frames carry individual loops without a tactical partner, and only one frame does the reverse. Weak rank correlation remains the main evidence for complementarity—joint presence need not mean the scales measure the same structure.

**Table 5.** Frame counts of $H_1$ presence at the two scales ($1{,}500$ frames).


|                          | Tactical $H_1$ present | Tactical $H_1$ absent |
| ------------------------ | ---------------------- | --------------------- |
| Individual $H_1$ present | $289$                  | $1{,}166$             |
| Individual $H_1$ absent  | $1$                    | $44$                  |


A TDA-native check agrees. Bottleneck distance between the two scales' diagrams has median $1.511$ m and $95$th-percentile tail $3.416$ m—on the order of typical tactical loop size on the primary match ($3.797$ m mean persistence where loops appear; Table 1). Landscape $L^2$ distance has median $5.671$. The scales differ by roughly as much as their features are large, not by a small perturbation of one shared pattern.

### 3.5 Sensitivity Analysis

Tactical $H_1$ counts fall monotonically as the cutoff widens. On the primary match's 150 frames, sweeping $\delta \in [6, 16]$ m gives $275$ loops ($87.3\%$ of frames) at $\delta = 6$ m and none at $\delta = 16$ m; the operative range is $[6, 14]$ m (Table 6). Our choice $\delta = 12.0$ m lies at the conservative end ($12.7\%$ frame presence), in line with single-linkage prioritising fewer, more robust loops over a larger noisy set.

**Table 6.** Tactical-scale cutoff sensitivity ($150$ frames, primary match).


| $\delta$ (m) | Total $H_1$ | Frame presence | Mean $H_0$ |
| ------------ | ----------- | -------------- | ---------- |
| $6$          | $275$       | $87.3\%$       | $13.4$     |
| $8$          | $162$       | $68.0\%$       | $9.8$      |
| $10$         | $78$        | $42.7\%$       | $7.0$      |
| $12$         | $21$        | $12.7\%$       | $4.8$      |
| $14$         | $5$         | $3.3\%$        | $3.5$      |
| $16$         | $0$         | $0.0\%$        | $2.8$      |


The adaptive truncation (equation 1) is likewise stable. At $\delta = 12.0$ m, every percentile from $P_{50}$ to $P_{95}$ yields the same $21$ loops and $12.7\%$ frame presence, even though $\varepsilon_{\max}$ spans $38.5$–$65.6$ m (Table 7).

**Table 7.** Adaptive filtration percentile ablation, $\delta = 12.0$ m.


| Percentile | Total $H_1$ | Frame presence | Max $\varepsilon_{\max}$ (m) |
| ---------- | ----------- | -------------- | ---------------------------- |
| $P_{50}$   | $21$        | $12.7\%$       | $38.5$                       |
| $P_{60}$   | $21$        | $12.7\%$       | $42.7$                       |
| $P_{75}$   | $21$        | $12.7\%$       | $50.3$                       |
| $P_{90}$   | $21$        | $12.7\%$       | $60.5$                       |
| $P_{95}$   | $21$        | $12.7\%$       | $65.6$                       |


### 3.6 Event Correlation

As a sanity check against measurement noise, we asked whether persistence moves with real match events (SkillCorner annotations; $104{,}722$ event–topology pairs across ten matches). Events that disrupt shape—on-ball engagements, quick breaks— tend to precede lower persistence; sustained build-up tends to precede higher persistence (Mann–Whitney $U$ on pre-specified classes; several nominal $p < 0.001$ at both scales). We treat this as construct validity only; multiple-testing control and football interpretation belong elsewhere.

---

## 4. Discussion

### 4.1 Methodological Contributions

Each component of this pipeline has precedent considered in isolation: hierarchical clustering before persistent homology underlies Schindler and Barahona's (2023) analysis of multiscale clusterings, and adapting a filtration threshold to local geometry is not new in principle. The contribution is empirical validation that the combination is robust enough for a real, high-frequency, noisy point cloud, which neither prior treatment establishes on its own. The result most relevant to a practitioner is the width of the pipeline's safe operating range: $H_1$ detection holds across cutoffs from $6$ to $14$ m and across every filtration percentile from $P_{50}$ to $P_{95}$ tested (Section 3.5). A method effective only at one finely-tuned parameter setting would be a substantially weaker contribution than one effective across a broad, empirically mapped range; this property is what makes the pipeline transferable to other multi-agent systems rather than a method tuned narrowly to this dataset.

The cutoff distance functions as a scale selector rather than a parameter to be optimised away. The three validated regimes, individual, tactical, and team, emerge from a systematic sweep over $\delta \in [0.5, 30.0]$ m, are validated by independent clustering-quality metrics, and recur across all ten matches. The tactical cutoff sits within a range where automated metrics disagree ($6.87$–$16.31$ m); its value is accordingly a domain-informed choice rather than an automatically optimal one, and the sensitivity analysis demonstrates that this choice does not compromise robustness.

The adaptive filtration formula addresses a coupling between the clustering and filtration steps: clustering alters the point cloud's geometry, so a fixed filtration threshold suitable at one scale produces null $H_1$ results at another. The $P_{75}$ percentile is a reporting convention: all tested percentiles from $P_{50}$ to $P_{95}$ return identical $H_1$ totals and presence rates. The same formula applies to any multi-scale pipeline that uses clustering as a preprocessing step before persistent homology, independent of the application domain.

### 4.2 Multi-Scale Topological Structure

The weak correlation and the divergent presence rates reported in Section 3.4 together support the same conclusion: the two scales are not measuring the same underlying structure at different resolutions, but capturing structurally distinct phenomena. If the tactical-scale signal were simply a coarsened version of the individual-scale signal, the two would be expected to co-occur far more consistently than the data show, and the bottleneck and landscape distances would be small relative to each scale's own persistence values rather than comparable to or exceeding them. Decomposing by scale before computing persistent homology is therefore not merely a convenience for separating noise; the decomposition recovers two informationally distinct objects, supporting the methodological case made in Section 2.4 that the clustering step does genuine analytical work rather than relabelling structure already visible in the undecomposed point cloud.

### 4.3 Limitations

Linkage selection is a substantive methodological choice rather than a matter of conservative versus liberal estimation. Across a $600$-frame, four-match comparison sample, single-linkage detects $153$ tactical-scale $H_1$ loops, against $923$ for complete-linkage and $936$ for Ward's method, a difference of almost an order of magnitude, large enough to change which scientific picture the data support rather than merely the precision of one estimate. We retain single-linkage here because its definition, clusters as chains of short pairwise distances, is the most natural reading of spatial proximity and is robust against over-partitioning artefacts, but we treat the gap with the other two methods as an open question rather than a settled one. A more principled selection criterion would come from the dynamical system itself rather than from clustering-quality metrics alone. The appropriate criterion is the linkage method under which a governing equation for a persistence functional, specifically the landscape $L^2$ norm or the tactical $H_1$ total-persistence sequence, admits the sparsest representation in the sense of sparse identification of nonlinear dynamics. Operationalising this criterion would require three things: choosing the dynamical state, defending the sparsity of the recovered library against AIC, BIC, or cross-validation baselines, and confirming that the resulting persistence sequence is genuinely lower-dimensional under the selected linkage. We defer this to the forthcoming full-season work, where a population-sized sample of match sequences makes the sparsity comparison meaningful.

The tactical cutoff of $12.0$ m is a domain-informed choice situated within, rather than derived from, an automated-metric range: the silhouette-optimal value is $16.31$ m and the information-content-optimal value is $6.87$ m, with $12.0$ m falling between them. The justification given in Section 2.3, namely correspondence to half a standard football zone width, is domain-reasonable but ultimately a judgement call. The sensitivity analysis in Section 3.5 reports the resulting operative range, $[6, 14]$ m, as an empirical property rather than a derivation of the chosen value. A more principled criterion would select the cutoff minimising the variation of the persistence landscape path under small perturbations of $\delta$. This is computable with the same landscape infrastructure used in Section 3.4, but the relevant sample size for estimating that variance is the number of matches, not the number of frames, so evaluating it on the present ten-match sample would be premature. We defer this to the persistence-landscape companion work and treat $12.0$ m as a domain-informed reference point within the validated $[6, 14]$ m range rather than an optimised value.

The framework identifies three $H_0$ regimes but only two $H_1$ regimes. The absence of team-scale $H_1$ is a structural consequence of the clustering reducing the point cloud to one or two centroids at $\delta = 30.0$ m, not a limitation of the persistent homology computation itself. Detecting team-scale loop structure would require an alternative representation, such as spatial density fields or Delaunay triangulations, rather than a centroid-based point cloud at any cutoff.

All data analysed here are broadcast-derived tracking at $10$ Hz. Broadcast tracking typically offers lower spatial precision than higher-frequency optical systems, which may affect the magnitude of persistence values reported. The structural findings, namely the three scale regimes, the $H_1$ presence rates, and the sensitivity profiles, are expected to be robust across tracking technologies, since they depend on relative rather than absolute spatial precision. A direct comparison of persistence magnitudes against optical tracking data remains for future work.

### 4.4 Outlook

Two extensions of this work are in progress, and a third output sits alongside it rather than ahead of it. The ten-match evidence base presented here is being scaled to a full season of Championship matches to characterise population-level distributions of $H_0$ and $H_1$ counts, barcode lengths, and landscape norms, and to test tactical-fingerprint classification at population scale; this is also the setting in which the SINDy-based linkage criterion proposed above becomes evaluable, since recovering a sparse governing equation for a persistence functional requires the population-sized sample of match sequences that a single season provides. Separately, persistence landscape dynamics are being developed to treat each match as a path through landscape space, which is the setting in which the landscape-stability cutoff criterion can itself be evaluated, since its resampling unit is the match-level landscape rather than the per-frame summary used throughout the present analysis.

Alongside these extensions, a companion paper (Brown, Powathil, and Kilduff, in preparation) interprets the present ten-match findings for a football-analytics readership: event correlation as a central result rather than a brief validity check, a comparison against standard geometric descriptors, bilateral home-and-away coupling, and a cross-validated test of predictive utility for phase-of-play classification. That paper depends methodologically on the framework validated here but answers a different question, asking what these topological measures reveal about football specifically rather than whether the framework itself is sound.

---

## 5. Conclusion

This paper introduces a multi-scale persistent homology framework for competitive multi-agent point clouds, validated on ten professional football matches. Two methodological contributions, domain-informed scale decomposition and an adaptive Vietoris–Rips filtration, resolve the scale-conflation problem that arises when a single filtration is applied directly to a hierarchically organised point cloud. The resulting three $H_0$ regimes and two $H_1$ regimes are stable across independent matches and across wide ranges of the framework's two free parameters, and the two $H_1$ scales carry complementary rather than redundant information. Football served here only as a validated testbed; the framework itself is intended for any bounded competitive multi-agent system with spatial tracking data.

---

## Declarations

### Competing Interests

The authors have no relevant financial or non-financial interests to disclose.

### Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors; it was conceived and conducted independently by the authors.

### Data Availability Statement

Positional tracking data were provided by SkillCorner under an open-data licence ([https://github.com/SkillCorner/opendata](https://github.com/SkillCorner/opendata)). Analysis code, pipeline configuration, pinned `requirements.txt`, and the result files used for the figures and tables in this paper are included with the manuscript materials and will be released in a dedicated public repository at arXiv posting, deposited in the Swansea University Zenodo community.

### Use of Large Language Models

Large language model (LLM) tools were used during the preparation of this manuscript to assist with prose structuring and copy-editing. All scientific content, analyses, interpretations, and conclusions are the sole responsibility of the authors. No LLM tool was used to generate novel scientific claims or to conduct or interpret statistical analyses.

---

## References (compact)

Author–year list matching the manuscript bibliography. Full BibTeX is in `references.bib`.

1. Bauer U. Ripser: efficient computation of Vietoris–Rips persistence barcodes. *J Appl Comput Topology*. 2021;5(3):391–423.
2. Botnan MB, Lesnick M. An introduction to multiparameter persistence. In: *Representations of Algebras and Related Structures*. EMS Press; 2023. p. 77–150. arXiv:2203.14289.
3. Bubenik P. Statistical topological data analysis using persistence landscapes. *J Mach Learn Res*. 2015;16(1):77–102.
4. Buldú JM, Busquets J, Echegoyen I, Seirulò F. Defining a historic football team: using network science to analyse Guardiola's FC Barcelona. *Sci Rep*. 2019;9:13602.
5. Carlsson G, Mémoli F. Characterization, stability and convergence of hierarchical clustering methods. *J Mach Learn Res*. 2010;11:1425–1470.
6. Cohen-Steiner D, Edelsbrunner H, Harer J. Stability of persistence diagrams. *Discrete Comput Geom*. 2007;37(1):103–120.
7. Edelsbrunner H, Letscher D, Zomorodian A. Topological persistence and simplification. *Discrete Comput Geom*. 2002;28(4):511–533.
8. Gu K, Yan L, Li X, Duan X, Liang J. Change point detection in multi-agent systems based on higher-order features. *Chaos*. 2022;32(11):113117.
9. Gudmundsson J, Horton M. Spatio-temporal analysis of team sports. *ACM Comput Surv*. 2017;50(2):22:1–22:34.
10. Grund TU. Network structure and team performance: The case of English Premier League soccer teams. *Soc Networks*. 2012;34(4):682–690.
11. Schindler J, Barahona M. Analysing multiscale clusterings with persistent homology. 2023. arXiv:2305.04281. doi:10.48550/arXiv.2305.04281.
12. SkillCorner. SkillCorner open broadcast tracking data. 2024. [https://github.com/SkillCorner/opendata](https://github.com/SkillCorner/opendata)
13. Tauzin G, et al. giotto-tda: A topological data analysis toolkit for machine learning and data exploration. *J Mach Learn Res*. 2021;22(39):1–6.
14. The GUDHI Project. GUDHI User and Reference Manual. Version 3.11.0. 2024. [https://gudhi.inria.fr/](https://gudhi.inria.fr/)
15. Topaz CM, Ziegelmeier L, Halverson T. Topological data analysis of biological aggregation models. *PLoS ONE*. 2015;10(5):e0126383.
16. Tralie C, Saul N, Bar-On R. Ripser.py: A lean persistent homology library for Python. *J Open Source Softw*. 2018;3(29):925.
17. Zomorodian A, Carlsson G. Computing persistent homology. *Discrete Comput Geom*. 2005;33(2):249–274.

Companion (Outlook only; not a Paper A result): Brown R, Powathil G, Kilduff L. What persistent homology reveals about football: event correlation, geometric baselines, and predictive utility. 2026. In preparation.

---

## Supplement: temporal autocorrelation

Headline tables use the uniform 150-frame rule of Section 2.1. Supplementary Figure S1 (`figures/figS1_acf.pdf`) is a diagnostic on the primary match at 1 Hz; it does not choose the stride. Generate with `pipeline/steps/09_acf_supplement.py`.