# Multi-Scale Persistent Homology for Competitive Collective Systems

> **Review source (7 September 2026).** Prose is edited in this file. `sections/*.tex` is frozen until the review settles; a TeX sweep will then be generated for Overleaf (equations, tables, figures) and the arXiv upload. Do not treat GitHub TeX as the live draft.

**Authors:** Rowan Brown  
**Affiliation:** Swansea University  

**Target:** *Journal of Applied and Computational Topology* (JACT); arXiv preprint  
**Status:** Working manuscript. Not yet submitted.

**This file.** Markdown review copy for Cursor. Local PDF checks can still use `main.tex`; Overleaf is a one-shot upload after the TeX sweep.

**Citations** are author–year, matching the JACT manuscript (`natbib` name–year). They are not Vancouver numbers.

---



## Note for collaborators

**What this paper is.** A mathematics-first methods paper. It asks whether a multi-scale persistent homology pipeline is *sound* on a real, high-frequency, noisy multi-agent point cloud. Football is the validated testbed, not the audience.

**What it is not.** A football-analytics paper. Event interpretation, geometric baselines, bilateral (home/away) coupling, and predictive utility belong to a companion manuscript (Paper B, *Journal of Sports Sciences*, in preparation). Paper A treats event correlation only as a one-sentence construct-validity check (“not noise”).

**Headline claim.** Domain-informed hierarchical clustering plus a data-driven Vietoris–Rips truncation resolves scale conflation in competitive collective systems. On ten professional matches the pipeline recovers three stable $H_0$ regimes and two $H_1$ regimes; the two $H_1$ scales carry distinct information; every examined $H_1$ feature has a geometric cycle representative.

**Locked cutoffs (metres).** Individual $2.98$; tactical $12.0$ (domain-informed, inside a metric-disagreement range); team $30.0$. Operative tactical $H_1$ range: $[6, 14]$ m.

**Sample.** Ten A-League matches, SkillCorner open broadcast tracking at $10$ Hz. Persistent homology on $150$ uniformly spaced complete frames per match ($1{,}500$ frames in total). Primary match: SkillCorner ID $1996435$, $43{,}531$ complete $22$-player frames.

**Open methodological questions (already flagged in the paper).** Linkage choice (single vs complete vs Ward changes tactical $H_1$ by nearly an order of magnitude); a more principled tactical cutoff; team-scale $H_1$ needs a different representation (centroids collapse to $k\in1,2$).

**Funnel (locked).** Four layers, wide to narrow. Check every paragraph against this; do not collapse them.

1. **Collective systems / hierarchically organised point clouds.** The TDA fact: single-parameter Vietoris–Rips mixes organisational levels in one diagram (scale conflation). Not special to competition. Topaz, Xia, Hiraoka, Gu live here.
2. **Competitive collective systems** (the class). Subset: agents in a bounded domain, coordinating internally while responding to an opponent. Named levels exist; mixing therefore blocks attribution. Metre values are recovered, not assumed. Paper A lives here.
3. **Bounded competitive systems** (transfer). Same pipeline once interaction lengths are re-derived. Abstract close and conclusion only.
4. **Football tracking** (measurement setting, not a class). 22 agents, 10 Hz, broadcast noise. Paper B owns interpretation.

**Intro transparency (locked).** For each quantity in the introduction, answer four questions in order, one job per sentence. Do not leave slogans (*recovered cutoff*, *data-driven*, *adaptive*).

1. What is the quantity?
2. What does it do to the data?
3. How is its value obtained (not assumed from the class)?
4. Which later section carries the numbers, formulae, and judgement calls?

Do not import Methods tables into the introduction. Football metres, $P_{75}$, and silhouette disagreement belong in §2.

**Level vs scale (locked).** Organisational *level*: named unit of the hierarchy. Metric *scale*: cutoff or filtration distance that selects that unit. *Scale-attributable*: the diagram belongs to one organisational level. Do not use the two words interchangeably. In prose: assign *level*; recover *cutoff*.

**Remainder of the paper (locked, from §1 revision).** Methods reports *what was done*; Results report *what was found*; Discussion interprets. Do not re-argue §1.2 in §2.

Carry forward:

1. Funnel. §2–3 are layer 4 (this corpus). The pipeline is for a competitive collective system; football nouns are instantiations, not a new class.
2. Order. Problem, then examples, then general-case methods, then the competitive gap, then *this* pipeline, then findings. Do not answer the scientific question inside the problem subsection.
3. Transparency. For each quantity: what it is, what it does to the data, how the value is obtained, where the numbers live. No slogans (*adaptive*, *data-driven*, *proximity-aware*, *scale-regime*) until that is on the page.
4. Level vs cutoff. Assign *organisational level*; recover *cutoff* $\delta$; filtration distance is $\varepsilon$. Do not write “individual scale” when the object is a level selected by a cutoff.
5. One job per sentence. Related-work citations sit at the funnel layer they belong to, not in a mixed dump.
6. Filtration novelty once (already §1.3). Competitive dependence once (already §1.1). Event correlation is construct validity only.

---

---



## Abstract

Standard single-parameter Vietoris–Rips persistent homology applied to a hierarchically organised point cloud mixes features from distinct organisational levels in one diagram. In a competitive collective system the hierarchy has named levels, so that mixing blocks scale attribution. The interaction lengths are not assumed: this paper recovers them by a cutoff sweep and asks whether persistent homology can then be made scale-attributable on a real, high-frequency, noisy point cloud. The point cloud is decomposed by hierarchical clustering at validated interaction lengths, and Vietoris–Rips homology is computed on the resulting centroids. Clustering changes the geometry, so a maximum filtration scale suited to one cutoff returns no $H_1$ (loops) at another. A data-driven truncation of the Vietoris–Rips parameter removes that obstruction. On ten professional football matches (broadcast tracking at 10 Hz), three stable $H_0$ (connected-component) regimes appear: individual (2.98 m), tactical (12.0 m), and team (30.0 m). Two $H_1$ regimes appear with them: individual-scale loops are frequent and transient ($97.0\pm1.5$ frame presence across matches); tactical-scale loops are rarer but more persistent ($19.3\pm7.2$); team-scale $H_1$ is absent a priori as a structural consequence of the clustering. These regime counts hold across matches and across wide ranges of both the cutoff and the truncation percentile. The two $H_1$ scales carry distinct rather than redundant information (Spearman $\rho=0.264$ across 1,500 sampled frames). Geometric cycle representatives are recovered for every $H_1$ feature examined. Football supplies the measurement setting; the same pipeline applies to other bounded competitive systems once interaction lengths are re-derived.

**Keywords:** persistent homology, multi-scale topology, Vietoris–Rips filtration, multi-agent systems, spatial tracking data, sports analytics

---



## 1. Introduction



### 1.1 Background

Collective systems of agents in space are typically hierarchically organised. Starling murmurations, fish shoals, and insect swarms, for example, show individuals, local groups, and a system-wide envelope occupying distinct spatial scales at once (Sumpter, 2006). Understanding how those scales interact is a standing challenge in applied mathematics, and one that high-frequency spatial tracking data is increasingly able to inform (Herbert-Read et al., 2011).

Competitive collective systems are a subset of that class: agents distributed in a bounded domain, coordinating internally while responding to an opponent. Examples that share this structure are autonomous vehicle fleets sharing road space, opposing crowd flows at transport hubs, predator–prey populations in an ecosystem, and sports teams contesting pitch or court territory.

Agents in such systems can arrange themselves in ring-like formations that enclose empty space: milling in a fish school, a vortex in a swarm, or, in the competitive subset, encirclement of an opponent. These arrangements are important to identify because enclosure is a distinct mode of organisation, not a change in density or alignment: a loop holds a region of space, whether that region is an empty core or the space denied to an opponent. Their persistence over time distinguishes stable structure from transient clustering. Conventional geometric summaries, including convex-hull area, nearest-neighbour distance, and polarisation, capture dispersion and alignment (Sumpter, 2006) but do not directly quantify this loop structure.

Persistent homology, a central tool of topological data analysis (TDA), provides a principled way to detect and measure such formations across a continuum of scales (Edelsbrunner et al., 2002; Edelsbrunner and Harer, 2010; Carlsson, 2009; Munch, 2017; Chazal and Michel, 2021). A filtration of simplicial complexes indexed by a scale parameter tracks the birth and death of topological features. Each feature is recorded as a bar: the interval from the scale at which it appears (birth) to the scale at which it disappears (death) (Ghrist, 2008). The collection of bars is the persistence diagram (Cohen-Steiner et al., 2007). Efficient computation via the Vietoris–Rips filtration is due to Bauer (2021); persistence landscapes provide a functional representation for later statistical analysis (Bubenik, 2015).

That representation has recovered cavities in protein atom clouds that mark flexibility and folding (Xia and Wei, 2014). It has identified medium-range order in amorphous solids that conventional crystallography does not resolve (Hiraoka et al., 2016). In biological aggregation models it has shown that distinct swarming organisations appear at different filtration values (Topaz et al., 2015). The same single-parameter construction, applied directly to a hierarchically organised multi-agent point cloud, raises the measurement difficulty treated in Section 1.2. This paper asks whether that homology can be attributed by organisational scale on a competitive collective system. Opposition couples successive positions (competitive dependence); that inference problem is not treated here.

### 1.2 The Scale Conflation Problem

A single-parameter Vietoris–Rips filtration on the full point cloud records features at many filtration values in one persistence diagram. Bars born at different distances therefore occupy the same object, whether they arise from local proximity, small-group arrangement, or system-wide organisation. If that mixing is not recognised, and the diagram is read as if the cloud had a single organisational level, features from distinct levels are treated as commensurate. A change in the diagram then cannot be assigned to a level: it may be a local rearrangement, a change in group structure, or a change in the system envelope, and those alternatives are not distinguished. Counts and persistence summaries inherit the same ambiguity.

Applied studies make that mixing visible without removing it. Betti numbers from biological aggregation models, plotted against simulation time and filtration value, show that distinct swarming organisations appear at different filtration values (Topaz et al., 2015). That display remains one mixed summary. A parallel construction computes Vietoris–Rips features on multi-agent snapshots and yields a topological time series at a chosen scale (Gu et al., 2022). That series can detect change points; it does not decompose the cloud by organisational level.

Responses for the general case exist, but they do not return a scale-attributable diagram. Multiparameter persistence treats several scales as simultaneous algebraic parameters (Botnan and Lesnick, 2023). The output is a module in several filtration parameters, not a single persistence diagram that names an organisational level. The construction is at present computationally feasible only on clouds far smaller, and sampled far more slowly, than a video-rate cloud of a few dozen agents. Persistent homology of multiscale clusterings, by contrast, analyses the hierarchy produced by the clustering itself (Schindler and Barahona, 2023). The output is a topological summary of how partitions merge as the cutoff varies, not a diagram of loops among units at one chosen level.

The methods above leave that mixing in place: a bar records when a loop closes, not which organisational level enclosed it. In a competitive collective system those levels are named (individual, small group, envelope), so a superimposed diagram cannot attribute an $H_1$ feature to a level or track that level through time.

### 1.3 Contributions

Section 1.2 leaves a concrete question: whether persistent homology can be made scale-attributable on a competitive collective system. This paper answers that question by changing the input rather than slicing bars of one diagram. The input is changed by a cutoff distance $\delta$: agents closer than $\delta$ are grouped, and each group is replaced by its centroid, so the reduced cloud represents one organisational level. That cutoff is not taken from the class definition. It is recovered by sweeping candidate distances and keeping those at which the partition is stable under independent clustering-quality metrics (Section 2.3). Vietoris–Rips homology is then computed on those centroids. Clustering stretches the cloud: inter-centroid distances are typically larger than $\delta$, so a filtration range fitted to one cutoff can return no $H_1$ at another. A maximum filtration distance is therefore taken from the pairwise distances of the reduced cloud itself, not from a global constant (Section 2.4). The output is a persistence diagram whose points are those centroids, so each bar is a feature among the units of one organisational level. Each $H_1$ bar is realised as a closed loop of centroids whose edge lengths lie in that bar's birth–death interval, so the feature is a loop in space and not only a pair of numbers (Section 2.5). Neither clustering nor the truncation is algebraically new (Carlsson and Mémoli, 2010; Schindler and Barahona, 2023); the content is that the combination survives a real, high-frequency, noisy point cloud.

When we apply this methodology to football broadcast data, four findings follow. Broadcast tracking records the positions of all 22 players at $10$ Hz from televised professional matches, as $(x,y)$ coordinates in metres on a standard pitch model; the corpus is ten A-League matches from the SkillCorner open repository (Section 2.1). A sweep of the cutoff over $[0.5, 30.0]$ m identifies three stable $H_0$ regimes across those matches, not a single demonstration case. $H_1$ is detected at two of the three organisational levels, with a geometric cycle representative for every feature in the primary-match analysis. The two $H_1$ levels carry complementary rather than redundant information. Event association is reported only as construct validity in Section 3.6. Spatial analysis of team sport, including pitch-control models and network metrics on passing and collective structure, is surveyed by Gudmundsson and Horton (2017) and by Buldú et al. (2019) and Grund (2012); those methods complement the present pipeline but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines cutoff-selected organisational levels with persistent homology for a competitive collective system, or validates the resulting regimes on high-frequency tracking across multiple independent recordings.

---



## 2. Methods



### 2.1 Data

The primary single-match analysis uses SkillCorner open broadcast tracking data, match ID $1996435$ (Sydney FC versus Adelaide United, A-League 2024/25), at $10$ frames per second. We retain only frames with complete $22$-player coverage, yielding $43{,}531$ frames (approximately $72$ minutes at this sampling rate). Positions are $(x, y)$ coordinates in metres on a standard football pitch model. The multi-match sample comprises that match and nine further A-League matches from the same repository, each with approximately $40{,}000$–$48{,}000$ complete frames. SkillCorner match IDs and fixtures are listed in Supplementary Table S1.

Consecutive complete frames share nearly the same configuration, so the full stream is not treated as a sequence of independent snapshots. For prevalence and organisational-level summaries we subsample. The operational rule is the same on every match: list complete $22$-player frames, set the stride to $\lfloor N/150\rfloor$, and retain $150$ frames. On the primary match $N = 43{,}531$, so the stride is $290$ frames ($\approx 29$ s). That yields a fixed-cardinality sample of $1{,}500$ frames across ten matches. The design limits temporal pseudo-replication. It does not treat the competitive-dependence inference problem named in Section 1.1, and it does not resolve formation or dispersion of loops between samples. Event association uses the native-rate stream and is a construct-validity check, not a dynamical model. Supplementary Figure S1 is an autocorrelation diagnostic on the primary match at $1$ Hz; it does not choose the stride.

### 2.2 Hierarchical clustering

On this corpus the named organisational levels of Section 1.2 (individual, small group, envelope) are instantiated as individual, tactical, and team. The corresponding cutoffs $\delta$ are obtained by the sweep in Section 2.3; they are not assumed from the class definition.

Figure 1 summarises the pipeline of Sections 2.2--2.5. At each time step $t$, the $22$ player positions form a point cloud $P(t) = \{p_1(t), \dots, p_{22}(t)\} \subset \mathbb{R}^2$.

> **Figure 1** (`figures/fig1_pipeline_schematic.pdf`). Analysis pipeline (schematic geometry; each panel shows the step and its output). **(a)** Colour-coded local groups in $P(t)$ (left, 2×2 layout) with dashed $\delta$-disks and a representative gap $< \delta$; centroids in $\tilde{P}(t)$ (right column) linked by colour-matched dashed lines (Section 2.2). **(b)** Vietoris–Rips (VR) on $\tilde{P}(t)$ truncated at $\varepsilon_{\max}$ (equation (1); Section 2.4). **(c)** Finite $H_1$ birth–death pairs. **(d)** Graph-cycle proxy for an $H_1$ pair (Section 2.5). Figure 2 shows the cycle step on real tracking data.

For a cutoff distance $\delta > 0$, single-linkage hierarchical clustering partitions $P(t)$ into clusters $C_1, \dots, C_k$ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding $\delta$. The reduced point cloud is the set of cluster centroids

$$
\tilde{P}(t)=\left\{\bar{c}_j : \bar{c}_j=\frac{1}{|C_j|}\sum_{p\in C_j} p,\ j=1,\dots,k\right\},
$$

and persistent homology is computed on $\tilde{P}(t)$ rather than on $P(t)$.

We use single-linkage throughout: clusters are chains of points connected by pairwise distances at most $\delta$. Complete-linkage and Ward's method are not used; their effect on $H_1$ counts is examined in Section 4.3.

Team identity is not used as an input. The pipeline can be run independently on a labelled subset of $P(t)$; that decomposition is not performed here.

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

At the individual scale ($\delta = 2.98$ m), $H_0 = 19.02 \pm 2.47$ (mean $\pm$ s.d.; range $9$–$22$), reflecting how tightly players cluster locally. At the tactical scale ($\delta = 12.0$ m), $H_0 = 4.77 \pm 1.60$ (range $2$–$10$) counts distinct tactical groups. At the team scale ($\delta = 30.0$ m), the cloud usually collapses to one or two clusters: mean $1.44 \pm 0.50$, with all 22 players in a single cluster in $56.0$ of frames and split across two in $44.0$.

The same three-scale pattern holds in all ten matches. Grand means are individual $H_0 = 19.05 \pm 0.41$, tactical $H_0 = 4.92 \pm 0.36$, and team cluster count $1.38 \pm 0.08$ (mean $\pm$ s.d. across matches). Every match stays within the validated $H_0$ bands of Section 2.3.

### 3.2 $H_1$ Loop Detection

On the primary match, the pipeline detects $403$ $H_1$ loops across 150 uniformly sampled frames (Table 1). Individual-scale loops are frequent and short-lived: they appear in $143$ of $150$ frames ($95.3$), at a mean rate of $2.55$ per frame, with low mean persistence ($1.977 \pm 1.128$ m). Tactical-scale loops are rarer but last longer: $19$ frames ($12.7$), mean rate $0.14$ per frame, mean persistence $3.797 \pm 3.008$ m, maximum $10.771$ m. Team-scale loops never occur ($H_1 = 0$ across all $1{,}500$ frames in the ten-match sample).

**Table 1.** Single-match $H_1$ statistics (primary match, $150$ frames).


| Scale                 | Total loops | Frames with loops  | Mean loops/frame | Mean persistence  | Max persistence |
| --------------------- | ----------- | ------------------ | ---------------- | ----------------- | --------------- |
| Individual ($2.98$ m) | $382$       | $143/150$ ($95.3$) | $2.55$           | $1.977 \pm 1.128$ | $12.991$        |
| Tactical ($12.0$ m)   | $21$        | $19/150$ ($12.7$)  | $0.14$           | $3.797 \pm 3.008$ | $10.771$        |
| Team ($30.0$ m)       | $0$         | $0/150$ ($0$)      | N/A              | N/A               | N/A             |


> **Remark (Team-scale $H_1$ vanishes a priori).** At $\delta = 30.0$ m the 22 players reduce to $k \in 1, 2$ centroids in every frame (Section 3.1). A Vietoris–Rips complex on at most three points cannot carry a non-trivial $1$-cycle: there are at most three edges, and any filled triangle bounds rather than generates a loop. So $H_1 = 0$ at every admissible filtration at this scale, regardless of the data. Team-scale loop structure would require a different representation (density fields or Delaunay triangulations, for example). Our $H_1$ analysis therefore runs at two scales (individual and tactical) against the three-scale $H_0$ decomposition above.

The two-scale $H_1$ pattern extends to all ten matches ($1{,}500$ uniformly sampled frames; Table 2). Individual-scale presence is $97.0 \pm 1.5$ ($95$ CI $96.1$–$97.9$), between $95$ and $99$ in every match. Tactical presence is $19.3 \pm 7.2$ ($95$ CI $15.3$–$23.7$), ranging from $12$ to $34$ across matches. The primary match ($12.7$ tactical) sits within one standard deviation of the ten-match mean. That match was chosen for broadcast quality and event annotation, not for its tactical $H_1$ rate.

**Table 2.** Multi-match $H_1$ statistics ($10$ matches). Presence = mean $\pm$ s.d. across matches; $95$ bootstrap CIs from $1{,}000$ resamples over matches.


| Scale      | Total $H_1$ | Presence rate  | $95$ CI       | Mean persistence | Cross-match s.d. |
| ---------- | ----------- | -------------- | ------------- | ---------------- | ---------------- |
| Individual | $4{,}200$   | $97.0 \pm 1.5$ | $96.1$–$97.9$ | $1.854$          | $0.163$          |
| Tactical   | $315$       | $19.3 \pm 7.2$ | $15.3$–$23.7$ | $0.666$          | $0.299$          |
| Team       | $0$         | $0.0 \pm 0.0$  | —             | N/A              | N/A              |


Mean persistence in Table 2 averages over all sampled frames, including those with no loop. The tactical entry is therefore lower than the primary-match mean in Table 1, which is taken only where loops appear.

Remark 1 explains why $H_1$ vanishes when clustering leaves at most three centroids; the tactical scale sits close to that floor. In the ten-match sample, $44$ of frames have four or fewer tactical centroids, and none of them carries a loop. Presence rate alone cannot tell formation geometry from cluster count. We separate the two with the matched null of Section 2.6, which fixes centroid number and spatial envelope and randomises only arrangement.

Table 3 summarises the result. Tactical observed presence is more than twice the null rate. Table 4 splits by centroid count $k$: presence is zero at $k \le 4$, as expected, then rises from $12.0$ at $k = 5$ to $75.0$ at $k = 8$, always above the null. At the individual scale the null already exceeds $91$: twenty points in a bounded region almost always close a cycle, so the observed excess is modest ($+5.8$ pp). Tactical $H_1$ carries information about how units are arranged; individual presence is near-saturated and reads better as background than as a discriminating signal.

**Table 3.** $H_1$ presence against a cardinality- and envelope-matched null ($10$ matches, $1{,}500$ frames, $200$ null replicates per frame). Excess is in percentage points, with $95$ bootstrap CIs over matches.


| Scale      | Observed | Null   | Excess  | $95$ CI         |
| ---------- | -------- | ------ | ------- | --------------- |
| Individual | $97.0$   | $91.2$ | $+5.8$  | $[+4.8, +6.9]$  |
| Tactical   | $19.3$   | $8.3$  | $+11.0$ | $[+8.0, +14.1]$ |


**Table 4.** Tactical-scale $H_1$ presence by centroid count $k$, against the matched null of Table 3 ($10$ matches, $1{,}500$ frames).


| $k$     | Frames | Observed | Null   | Excess  |
| ------- | ------ | -------- | ------ | ------- |
| $\le 4$ | $659$  | $0.0$    | $0.4$  | $-0.4$  |
| $5$     | $357$  | $12.0$   | $4.8$  | $+7.3$  |
| $6$     | $233$  | $33.5$   | $12.5$ | $+20.9$ |
| $7$     | $140$  | $56.4$   | $23.0$ | $+33.4$ |
| $8$     | $72$   | $75.0$   | $34.5$ | $+40.5$ |
| $\ge 9$ | $39$   | $92.3$   | $48.1$ | $+44.2$ |




### 3.3 Closed Cycle Structures

All $403$ primary-match $H_1$ features receive a geometric realisation via closed-cycle identification. The representative is the graph-cycle proxy of Section 2.5, not a generator from the reduction matrix. Individual-scale cycles form short rings of centroids (typically three to six nodes in the examples we inspected). Tactical cycles are similarly small (often four or five nodes) but span larger gaps and persist longer. Figure 2 shows the highest-persistence example at each scale: frame $141$ at individual scale ($p = 12.991$ m) and frame $97$ at tactical scale ($p = 10.771$ m).

> **Figure 2** (`figures/fig2_cycle_geometry.pdf`; not embedded in this Markdown copy). Geometric realisation of maximal-persistence $H_1$ loops at individual ($\delta = 2.98$ m) and tactical ($\delta = 12.0$ m) scales for SkillCorner match $1996435$. Individual panel: sample frame $141$ ($p = 12.991$ m); tactical panel: sample frame $97$ ($p = 10.771$ m). Uniform sample, $n = 150$ frames, every $290$th complete frame (same rule as the ten-match analysis).



### 3.4 Scale Complementarity

The two $H_1$ scales carry related but largely distinct information. Over $1{,}500$ uniformly sampled frames, total individual and tactical $H_1$ persistence correlate weakly (Spearman $\rho = 0.264$, $p < 0.001$; $95$ bootstrap CI $[0.200, 0.314]$). The same holds for loop counts ($\rho = 0.211$, $p < 0.001$), so the finding does not depend on how persistence is summarised.

Co-occurrence exceeds chance (Fisher odds ratio $10.91$, $p < 0.001$; bootstrap CI $[2.59, 13.53]$), but Table 5 shows the asymmetry: $1{,}166$ frames carry individual loops without a tactical partner, and only one frame does the reverse. Weak rank correlation remains the main evidence for complementarity: joint presence need not mean the scales measure the same structure.

**Table 5.** Frame counts of $H_1$ presence at the two scales ($1{,}500$ frames).


|                          | Tactical $H_1$ present | Tactical $H_1$ absent |
| ------------------------ | ---------------------- | --------------------- |
| Individual $H_1$ present | $289$                  | $1{,}166$             |
| Individual $H_1$ absent  | $1$                    | $44$                  |


A TDA-native check agrees. Bottleneck distance between the two scales' diagrams has median $1.511$ m and $95$th-percentile tail $3.416$ m: on the order of typical tactical loop size on the primary match ($3.797$ m mean persistence where loops appear; Table 1). Landscape $L^2$ distance has median $5.671$. The scales differ by roughly as much as their features are large, not by a small perturbation of one shared pattern.

### 3.5 Sensitivity Analysis

Tactical $H_1$ counts fall monotonically as the cutoff widens. On the primary match's 150 frames, sweeping $\delta \in [6, 16]$ m gives $275$ loops ($87.3$ of frames) at $\delta = 6$ m and none at $\delta = 16$ m; the operative range is $[6, 14]$ m (Table 6). Our choice $\delta = 12.0$ m lies at the conservative end ($12.7$ frame presence), in line with single-linkage prioritising fewer, more robust loops over a larger noisy set.

**Table 6.** Tactical-scale cutoff sensitivity ($150$ frames, primary match).


| $\delta$ (m) | Total $H_1$ | Frame presence | Mean $H_0$ |
| ------------ | ----------- | -------------- | ---------- |
| $6$          | $275$       | $87.3$         | $13.4$     |
| $8$          | $162$       | $68.0$         | $9.8$      |
| $10$         | $78$        | $42.7$         | $7.0$      |
| $12$         | $21$        | $12.7$         | $4.8$      |
| $14$         | $5$         | $3.3$          | $3.5$      |
| $16$         | $0$         | $0.0$          | $2.8$      |


The adaptive truncation (equation 1) is likewise stable. At $\delta = 12.0$ m, every percentile from $P_{50}$ to $P_{95}$ yields the same $21$ loops and $12.7$ frame presence, even though $\varepsilon_{\max}$ spans $38.5$–$65.6$ m (Table 7).

**Table 7.** Adaptive filtration percentile ablation, $\delta = 12.0$ m.


| Percentile | Total $H_1$ | Frame presence | Max $\varepsilon_{\max}$ (m) |
| ---------- | ----------- | -------------- | ---------------------------- |
| $P_{50}$   | $21$        | $12.7$         | $38.5$                       |
| $P_{60}$   | $21$        | $12.7$         | $42.7$                       |
| $P_{75}$   | $21$        | $12.7$         | $50.3$                       |
| $P_{90}$   | $21$        | $12.7$         | $60.5$                       |
| $P_{95}$   | $21$        | $12.7$         | $65.6$                       |




### 3.6 Event Correlation

As a sanity check against measurement noise, we asked whether persistence moves with real match events (SkillCorner annotations; $104{,}722$ event–topology pairs across ten matches). Events that disrupt shape (on-ball engagements, quick breaks) tend to precede lower persistence; sustained build-up tends to precede higher persistence (Mann–Whitney $U$ on pre-specified classes; several nominal $p < 0.001$ at both scales). We treat this as construct validity only; multiple-testing control and football interpretation belong elsewhere.

---



## 4. Discussion



### 4.1 Methodological Contributions

Each component of this pipeline has precedent considered in isolation: hierarchical clustering before persistent homology underlies Schindler and Barahona's (2023) analysis of multiscale clusterings, and adapting a filtration threshold to local geometry is not new in principle. The contribution is empirical validation that the combination is robust enough for a real, high-frequency, noisy point cloud, which neither prior treatment establishes on its own. The result most relevant to a practitioner is the width of the pipeline's safe operating range: $H_1$ detection holds across cutoffs from $6$ to $14$ m and across every filtration percentile from $P_{50}$ to $P_{95}$ tested (Section 3.5). A method effective only at one finely-tuned parameter setting would be a substantially weaker contribution than one effective across a broad, empirically mapped range; this property is what makes the pipeline transferable to other bounded competitive systems once interaction lengths are re-derived, rather than a method tuned narrowly to this dataset.

The cutoff distance functions as a scale selector rather than a parameter to be optimised away. The three validated regimes, individual, tactical, and team, emerge from a systematic sweep over $\delta \in [0.5, 30.0]$ m, are validated by independent clustering-quality metrics, and recur across all ten matches. The tactical cutoff sits within a range where automated metrics disagree ($6.87$–$16.31$ m); its value is accordingly a domain-informed choice rather than an automatically optimal one, and the sensitivity analysis demonstrates that this choice does not compromise robustness.

The adaptive filtration formula addresses a coupling between the clustering and filtration steps: clustering alters the point cloud's geometry, so a fixed filtration threshold suitable at one scale produces null $H_1$ results at another. The $P_{75}$ percentile is a reporting convention: all tested percentiles from $P_{50}$ to $P_{95}$ return identical $H_1$ totals and presence rates. The same truncation formula applies whenever clustering precedes single-parameter persistent homology. Paper A's transfer claim is narrower: other bounded competitive systems, once interaction lengths are re-derived.

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

On ten professional football matches, clustering at recovered interaction lengths and a data-driven Vietoris–Rips truncation produced three stable $H_0$ regimes and two $H_1$ regimes. The two $H_1$ scales carry complementary rather than redundant information. Those findings answer whether persistent homology can be made scale-attributable on a competitive collective system. Scale conflation is the underlying TDA fact: a single filtration on a hierarchically organised point cloud mixes organisational levels. Football was the measurement setting; the same pipeline applies to other bounded competitive systems once interaction lengths are re-derived.

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
5. Carlsson G. Topology and data. *Bull Amer Math Soc*. 2009;46(2):255–308.
6. Carlsson G, Mémoli F. Characterization, stability and convergence of hierarchical clustering methods. *J Mach Learn Res*. 2010;11:1425–1470.
7. Cohen-Steiner D, Edelsbrunner H, Harer J. Stability of persistence diagrams. *Discrete Comput Geom*. 2007;37(1):103–120.
8. Edelsbrunner H, Harer J. *Computational Topology: An Introduction*. Providence, RI: American Mathematical Society; 2010.
9. Edelsbrunner H, Letscher D, Zomorodian A. Topological persistence and simplification. *Discrete Comput Geom*. 2002;28(4):511–533.
10. Gu K, Yan L, Li X, Duan X, Liang J. Change point detection in multi-agent systems based on higher-order features. *Chaos*. 2022;32(11):113117.
11. Gudmundsson J, Horton M. Spatio-temporal analysis of team sports. *ACM Comput Surv*. 2017;50(2):22:1–22:34.
12. Grund TU. Network structure and team performance: The case of English Premier League soccer teams. *Soc Networks*. 2012;34(4):682–690.
13. Hiraoka Y, Nakamura T, Hirata A, Escolar EG, Matsue K, Nishiura Y. Hierarchical structures of amorphous solids characterized by persistent homology. *Proc Natl Acad Sci USA*. 2016;113(26):7035–7040.
14. Schindler J, Barahona M. Analysing multiscale clusterings with persistent homology. 2023. arXiv:2305.04281. doi:10.48550/arXiv.2305.04281.
15. SkillCorner. SkillCorner open broadcast tracking data. 2024. [https://github.com/SkillCorner/opendata](https://github.com/SkillCorner/opendata)
16. Tauzin G, et al. giotto-tda: A topological data analysis toolkit for machine learning and data exploration. *J Mach Learn Res*. 2021;22(39):1–6.
17. The GUDHI Project. GUDHI User and Reference Manual. Version 3.11.0. 2024. [https://gudhi.inria.fr/](https://gudhi.inria.fr/)
18. Topaz CM, Ziegelmeier L, Halverson T. Topological data analysis of biological aggregation models. *PLoS ONE*. 2015;10(5):e0126383.
19. Tralie C, Saul N, Bar-On R. Ripser.py: A lean persistent homology library for Python. *J Open Source Softw*. 2018;3(29):925.
20. Xia K, Wei GW. Persistent homology analysis of protein structure, flexibility and folding. *Int J Numer Methods Biomed Eng*. 2014;30(8):814–844.
21. Zomorodian A, Carlsson G. Computing persistent homology. *Discrete Comput Geom*. 2005;33(2):249–274.

Companion (Outlook only; not a Paper A result): Brown R, Powathil G, Kilduff L. What persistent homology reveals about football: event correlation, geometric baselines, and predictive utility. 2026. In preparation.

---



## Supplement

### Table S1. SkillCorner match identifiers

Ten A-League matches from the SkillCorner open repository. Home and away names are those recorded in the tracking files. The primary match is used for single-match $H_1$ tables, cycle geometry, and Figure S1.

| SkillCorner ID | Home | Away | Role |
| --- | --- | --- | --- |
| $1886347$ | Auckland FC | Newcastle | multi-match |
| $1899585$ | Auckland FC | Wellington P FC | multi-match |
| $1925299$ | Brisbane FC | Perth Glory | multi-match |
| $1953632$ | CC Mariners | Melbourne City | multi-match |
| $1996435$ | Sydney FC | Adelaide United | primary |
| $2006229$ | Melbourne City | Macarthur FC | multi-match |
| $2011166$ | Wellington P FC | Melbourne V FC | multi-match |
| $2013725$ | Western United | Sydney FC | multi-match |
| $2015213$ | Western United | Auckland FC | multi-match |
| $2017461$ | Melbourne V FC | Auckland FC | multi-match |

### Temporal autocorrelation

Headline tables use the uniform 150-frame rule of Section 2.1. Supplementary Figure S1 (`figures/figS1_acf.pdf`) is a diagnostic on the primary match at 1 Hz; it does not choose the stride. Generate with `pipeline/steps/09_acf_supplement.py`.