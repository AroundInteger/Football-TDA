# Multi-Scale Persistent Homology for Competitive Collective Systems

> **Review source (9 September 2026).** Prose is edited in this file. `sections/*.tex` is synced to this pass for Overleaf (equations, tables, figures) and the arXiv upload.

**Authors:** Rowan Brown  
**Affiliation:** Swansea University  

**Target:** *Journal of Applied and Computational Topology* (JACT); arXiv preprint  
**Status:** Working manuscript. Not yet submitted.

**This file.** Markdown review copy for Cursor. `main.tex` and `sections/*.tex` match this pass. Overleaf can take a one-shot upload of those files.

**Citations** are author–year, matching the JACT manuscript (`natbib` name–year). They are not Vancouver numbers.

---



## Note for collaborators

**What this paper is.** A mathematics-first methods paper. It asks whether a multi-scale persistent homology pipeline is *sound* on a real, high-frequency, noisy multi-agent point cloud. Football is the validated testbed, not the audience.

**What it is not.** A football-analytics paper. Event interpretation, geometric baselines, bilateral (home/away) coupling, and predictive utility belong to a companion manuscript (Paper B, *Journal of Sports Sciences*, in preparation). Paper A treats event correlation only as a one-sentence construct-validity check (“not noise”).

**Headline claim.** Hierarchical clustering at recovered interaction lengths, plus a truncation of the Vietoris–Rips parameter taken from the reduced cloud, resolves scale conflation in competitive collective systems. On ten professional matches, answering the four questions in turn: (Q1) three stable $H_0$ regimes are recovered from the data; (Q2) $H_1$ is detected at two of them, every feature realised as a loop in space and robust across a band of cutoffs and truncation percentiles; (Q3) the two $H_1$ levels carry distinct information; and (Q4) topological features track on-ball events, as construct validity only.

**Locked cutoffs (metres).** Individual $2.75$; tactical $11.75$; team $23.0$. Cardinality inversion on all complete frames of the ten Table S1 matches (436{,}648 frames). Operative tactical $H_1$ range: re-centre on $11.75$ m after the H1 cascade.

**Sample.** Ten A-League matches, SkillCorner open broadcast tracking at $10$ Hz. Persistent homology on $150$ uniformly spaced complete frames per match ($1{,}500$ frames in total). Primary match: SkillCorner ID $1996435$, $43{,}531$ complete $22$-player frames.

**Open methodological questions (already flagged in the paper).** Linkage choice (single vs complete vs Ward changes tactical $H_1$ by nearly an order of magnitude); a more principled tactical cutoff; team-level $H_1$ needs a different representation (centroids collapse to $k\in1,2$).

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

Standard single-parameter Vietoris–Rips persistent homology applied to a hierarchically organised point cloud mixes features from distinct organisational levels in one diagram. In a competitive collective system the hierarchy has named levels, so that mixing blocks scale attribution. The interaction lengths are not assumed: this paper recovers them by a cutoff sweep and asks whether persistent homology can then be made scale-attributable on a real, high-frequency, noisy point cloud. The point cloud is decomposed by hierarchical clustering at validated interaction lengths, and Vietoris–Rips homology is computed on the resulting centroids. Clustering changes the geometry, so a maximum filtration distance suited to one cutoff returns no $H_1$ (loops) at another. Truncating the Vietoris–Rips parameter from the pairwise distances of the reduced cloud removes that obstruction. On ten professional football matches (broadcast tracking at 10 Hz), three stable $H_0$ (connected-component) regimes appear: individual (2.75 m), tactical (11.75 m), and team (23.0 m). Two $H_1$ regimes appear with them: loops at the individual level are frequent and transient ($96.5\pm1.5\%$ frame presence across matches); loops at the tactical level are rarer but more persistent ($18.8\pm6.5\%$); team-level $H_1$ is absent on the sampled frames (most complete frames at $23.0$ m have $k\le 2$ centroids). These regime counts hold across matches and across wide ranges of both the cutoff and the truncation percentile. The two $H_1$ levels carry distinct rather than redundant information (Spearman $\rho=0.234$ across 1,500 sampled frames). Geometric cycle representatives are recovered for every $H_1$ feature examined. Football supplies the measurement setting; the same pipeline applies to other bounded competitive systems once interaction lengths are re-derived.

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

Section 1.2 leaves a concrete question: whether persistent homology can be made scale-attributable on a competitive collective system. This paper answers that question by changing the input rather than slicing bars of one diagram. A cutoff distance $\delta$ groups nearby agents and replaces each group by its centroid, so the reduced cloud represents one organisational level named by cardinality; Vietoris–Rips homology is then computed on those centroids, with a maximum filtration distance taken from the reduced cloud itself and each $H_1$ bar realised as a closed loop in space (Sections 2.2–2.5). Neither clustering nor the truncation is algebraically new (Carlsson and Mémoli, 2010; Schindler and Barahona, 2023); the content is that the combination survives a real, high-frequency, noisy point cloud.

We test the pipeline on football broadcast tracking: the positions of all 22 players at $10$ Hz from televised professional matches, as $(x,y)$ coordinates in metres on a standard pitch model, for ten A-League matches from the SkillCorner open repository (Section 2.1). Four questions organise the results, and each is answered in turn:

1. **(Q1)** Can the organisational levels be recovered from the data rather than assumed in metres (Section 3.1)?
2. **(Q2)** Does scale-attributable persistent homology then detect $H_1$ loop structure at those levels, is every feature realised as a loop in space, and is detection robust to the cutoff and truncation choices (Sections 3.2 and 3.4)?
3. **(Q3)** Where loops appear at more than one level, do those levels carry distinct rather than redundant information (Section 3.5)?
4. **(Q4)** Do the topological features track on-ball match events, as a construct-validity check only (Section 3.6)?

Spatial analysis of team sport, including pitch-control models and network metrics on passing and collective structure, is surveyed by Gudmundsson and Horton (2017) and by Buldú et al. (2019) and Grund (2012); those methods complement the present pipeline but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines cutoff-selected organisational levels with persistent homology for a competitive collective system, or validates the resulting regimes on high-frequency tracking across multiple independent recordings.

---



## 2. Methods



### 2.1 Data

The primary single-match analysis uses SkillCorner open broadcast tracking data, match ID $1996435$ (Sydney FC versus Adelaide United, A-League 2024/25), at $10$ frames per second. We retain only frames with complete $22$-player coverage, yielding $43{,}531$ frames (approximately $72$ minutes at this sampling rate). Positions are $(x, y)$ coordinates in metres on a standard football pitch model. The multi-match sample comprises that match and nine further A-League matches from the same repository, each with approximately $40{,}000$–$48{,}000$ complete frames. SkillCorner match IDs and fixtures are listed in Supplementary Table S1.

Consecutive complete frames share nearly the same configuration, so the full stream is not treated as a sequence of independent snapshots. For prevalence and organisational-level summaries we subsample. Write $t$ for the time of a complete frame in the native stream. The operational rule is the same on every match: list complete $22$-player frames, set the stride to $\lfloor N/150\rfloor$, and retain $150$ frames. Write $\tilde{t}$ for a time retained by that rule, and $\tilde{T}$ for the set of such times on one match, so $|\tilde{T}|=150$. On the primary match $N = 43{,}531$, so the stride is $290$ frames ($\approx 29$ s). Across ten matches the sampled times give $1{,}500$ frames. The design limits temporal pseudo-replication. It does not treat the competitive-dependence inference problem named in Section 1.1, and it does not resolve formation or dispersion of loops between samples. Event association uses the native-rate stream $t$ and is a construct-validity check, not a dynamical model. Supplementary Figure S1 is an autocorrelation diagnostic on the primary match at $1$ Hz; it does not choose $\tilde{T}$.

### 2.2 Hierarchical clustering

On this corpus the named organisational levels of Section 1.2 (individual, small group, envelope) are instantiated as individual, tactical, and team. The corresponding cutoffs $\delta$ are obtained by the sweep in Section 2.3; they are not assumed from the class definition.

Figure 1 summarises the pipeline of Sections 2.2--2.5, applied at the sampled times $\tilde{t}\in\tilde{T}$ of Section 2.1. The input is the point cloud $P(\tilde{t}) = \{p_1(\tilde{t}), \dots, p_{22}(\tilde{t})\} \subset \mathbb{R}^2$.

> **Figure 1** (`figures/fig1_pipeline_schematic.pdf`). Analysis pipeline (schematic geometry; each panel shows the step and its output). **(a)** Colour-coded local groups in $P(\tilde{t})$ (left, 2×2 layout) with dashed $\delta$-disks and a representative gap $< \delta$; centroids in $\tilde{P}(\tilde{t})$ (right column) linked by colour-matched dashed lines (Section 2.2). **(b)** Vietoris–Rips (VR) on $\tilde{P}(\tilde{t})$ truncated at $\varepsilon_{\max}$ (equation (1); Section 2.4). **(c)** Finite $H_1$ birth–death pairs. **(d)** Graph-cycle proxy for an $H_1$ pair (Section 2.5). Figure 3 shows the cycle step on real tracking data.

For a cutoff distance $\delta > 0$, single-linkage hierarchical clustering partitions $P(\tilde{t})$ into clusters $C_1, \dots, C_k$ such that every pair of points within a cluster is connected by a chain of pairwise distances not exceeding $\delta$. The reduced point cloud is the set of cluster centroids

$$
\tilde{P}(\tilde{t})=\left\{\bar{c}_j : \bar{c}_j=\frac{1}{|C_j|}\sum_{p\in C_j} p,\ j=1,\dots,k\right\},
$$

and persistent homology is computed on $\tilde{P}(\tilde{t})$ rather than on $P(\tilde{t})$.

Complete-linkage and Ward's method are not used; their effect on $H_1$ counts is examined in Section 4.3.

Team identity is not used as an input.

### 2.3 Cutoff selection

The class names the three organisational levels by cardinality. The sweep reads the metres from the pooled $H_0(\delta)$ curve on this corpus. Quality metrics are a check. They are not the selector.

Every complete 22-player frame of the ten Table S1 matches is used (436{,}648 frames). The grid is $\delta \in [0.25, 40.0]$ m at $0.25$ m. Single-linkage; team labels unused.

Selector: individual, largest $\delta$ with mean $H_0 \ge 19$; tactical, $\delta$ nearest mean $H_0 = 5$ among $P(k \ge 4) \ge 0.5$; team, smallest $\delta$ with mean $H_0 \le 2$. Ties take the smaller $\delta$.

On this corpus that returns $2.75$ m, $11.75$ m, and $23.0$ m. Per-match inversions are $2.80 \pm 0.20$ m, $11.80 \pm 0.35$ m, and $22.98 \pm 0.72$ m. All ten matches pass the acceptance bands. The curve is asymmetric: about $1.6$ clusters merge per metre from the individual to the tactical level, but only about $0.27$ per metre from the tactical to the team level, so the two envelopes persist over a wide band of $\delta$. Clustering-quality diagnostics (Calinski--Harabasz, silhouette, information-content) are reported in Supplementary Figure S2 and are not the selector. Figure 2 shows the estimator and its spatial realisation. Section 3.4 reports tactical $H_1$ sensitivity.

> **Figure 2** (`figures/fig2_cutoff_sweep.pdf`). Cutoff selection by cardinality inversion, on all complete frames of the ten SkillCorner matches (436{,}648 frames); not $\tilde{T}$. **(a)** Pooled mean $\overline{H_0}(\delta)$ (black) with the ten per-match curves (grey); targets are roster statements $\overline{H_0} = 19$ (most agents resolved), $5$ (a few coordinating groups, loop-feasible), and $2$ (two spatial envelopes, not the two teams). Circles mark the inversion at $2.75$, $11.75$, $23.0$ m (top axis); inset zooms the individual rule. **(b)** Per-frame $H_0$ distribution (median, interquartile, 5th--95th bands); brackets are the acceptance intervals $[15,22]$, $[4,10]$, $[1,2.5]$; orange dots are the ten per-match means, all inside. **(c)** Feasibility: $k$ is the per-frame cluster count and $P(k \ge 4)$ the fraction with at least four; the adopted $11.75$ m sits at $P = 0.80$, inside the feasible region ($\delta \le 13.5$ m). **(d--f)** The same cutoffs on primary-match sample frame 95 ($H_0 = 20, 7, 2$; one frame, near the pooled targets $19, 5, 2$). Coloured hulls are multi-player clusters, grey are singletons; colours distinguish separate topological components in this frame, not player teams. Clustering-quality diagnostics are in Supplementary Figure S2 and are not the selector.

### 2.4 Maximum filtration distance

Clustering at cutoff $\delta$ produces a reduced point cloud $\tilde{P}(\tilde{t})$. Inter-centroid distances on that cloud are typically larger than $\delta$. A maximum filtration distance $\varepsilon_{\max}$ fitted to one cutoff can then return no $H_1$ at another.

We do not modify the Vietoris–Rips complex. We truncate its parameter at

$$
\varepsilon_{\max} = \max\Big(P_{75}\{d(\bar c_i,\bar c_j) : i<j\},\; \max(5.0,\,2\delta)\Big).
\tag{1}
$$

Here $P_{75}$ is the 75th percentile of pairwise inter-centroid distances on $\tilde{P}(\tilde{t})$. The first term tracks the geometry of the reduced cloud at the current cutoff. The second term is a floor. It prevents a degenerate filtration at small $\delta$. It also ensures the filtration reaches at least the inter-cluster distance regime.

$P_{75}$ is a conventional upper-quartile summary. Section 3.4 reports an ablation across $P_{50}$ through $P_{95}$. Every tested percentile returns identical $H_1$ totals and frame-presence rates. The choice is therefore a reporting convention, not an optimisation.

Persistence diagrams are computed with Ripser via Ripser.py (Bauer, 2021), with coefficients in $\mathbb{F}_2$. We report finite $H_1$ bars. The $H_0$ counts reported in Section 3.1 are read from these diagrams at filtration zero. We cross-checked all primary-match diagrams against GUDHI (The GUDHI Project, 2024) and giotto-tda (Tauzin et al., 2021). Birth–death pairs agreed to within numerical tolerance ($10^{-6}$ m). GUDHI is also used for the bottleneck-distance and landscape computations reported in Section 3.5.

### 2.5 Closed cycle identification

Each $H_1$ feature corresponds to a 1-cycle in the Vietoris–Rips complex. To recover a geometric realisation, we build the adjacency graph of edges whose distances fall within the feature's persistence interval $[\text{birth}, \text{death}]$. We then enumerate closed cycles of length at least $3$ by breadth-first search from each vertex. If that graph yields no cycle, we fall back to edges with length in $[\tfrac{1}{2}\text{birth}, \text{death}]$. Breadth-first search is used in preference to depth-first search because it prioritises shorter cycles. Those cycles correspond to minimal enclosing arrangements. Among the enumerated cycles, the one whose edge distances lie closest to the midpoint of the persistence interval is selected as the geometric representative. This is a geometric proxy for the persistence pair, not a homology generator extracted from the matrix reduction.

### 2.6 Statistical tests

To test whether $H_1$ detection reflects the arrangement of cluster centroids rather than merely their number, each frame is compared against a matched null. For a frame whose clustering yields $k$ centroids, the null draws $k$ points uniformly from the convex hull of those same centroids. The null therefore matches the frame on both cardinality and spatial envelope. It randomises only the arrangement. The truncation of equation (1) is recomputed on each null cloud. Nothing else differs between the two. We use $200$ null replicates per frame. We report the excess of observed over null $H_1$ presence, with $95\%$ confidence intervals from bootstrap resampling over matches.

Complementarity of the two $H_1$ levels (Section 3.5) is assessed by two frame-level tests. The Spearman rank correlation is computed on total $H_1$ persistence: the sum of death minus birth over all finite $H_1$ bars in a frame. We also report it on loop counts as a robustness check. Fisher's exact test is computed on the binary co-occurrence of $H_1$ presence at the two levels. Both statistics carry $95\%$ confidence intervals obtained by bootstrap resampling over matches ($1{,}000$ resamples). The match is the resampling unit. Bottleneck and landscape distances between the two levels' persistence diagrams are computed using GUDHI, as described in Section 2.4.

### 2.7 Software and Reproducibility

All analyses were performed in Python 3.11. Persistence diagrams are computed with Ripser.py 0.6.12 (Bauer, 2021; Tralie et al., 2018); bottleneck distances and landscape representations use GUDHI 3.11.0; giotto-tda 0.6.0 provided independent cross-checks. Supporting scientific Python packages match the pinned `requirements.txt` accompanying the manuscript: NumPy 2.0.2, SciPy 1.13.1, pandas 2.3.2, scikit-learn 1.6.1. Analysis code, pipeline configuration, and pinned dependencies are included with the manuscript materials and will be released in a public repository at arXiv posting (see Data Availability Statement).

---



## 3. Results



### 3.1 Connected components ($H_0$)

Throughout, $H_0$ is the number of cluster centroids. Equivalently, it is $\beta_0$ of the Vietoris–Rips complex on those centroids at filtration zero. Primary-match figures come from the uniform 150-frame sample of match 1996435 (Section 2.1). Ten-match aggregates use the same sampling scheme ($1{,}500$ frames in total).

At the individual level ($\delta = 2.75$ m), $H_0 = 19.32 \pm 2.34$ (mean $\pm$ s.d.; range 10--22). At the tactical level ($\delta = 11.75$ m), $H_0 = 5.04 \pm 1.69$ (range 2--10). At the team level ($\delta = 23.0$ m), the cloud usually collapses to one or two clusters: mean $1.96 \pm 0.36$. All 22 players lie in a single cluster in 8.7\% of frames, split across two in 86.7\%, and across three in 4.7\%.

The same three-level pattern holds in all ten matches. Grand means are individual $H_0 = 19.31 \pm 0.31$, tactical $H_0 = 5.09 \pm 0.38$, and team cluster count $1.98 \pm 0.06$ (mean $\pm$ s.d. across matches). Every match stays within the validated $H_0$ bands of Section 2.3: the ten per-match means all fall inside the acceptance intervals $[15,22]$, $[4,10]$, $[1,2.5]$ (Figure 2b). Figure 2 records the sweep from which those cutoffs were taken. The pooled curve is asymmetric (about $1.6$ clusters merge per metre from the individual to the tactical level, but only $0.27$ per metre from the tactical to the team level), so the two envelopes persist over a wide band of $\delta$ (Figure 2a). The spatial realisation on one frame (Figure 2d--f) shows the same regimes: a near-atomic cloud at $2.75$ m, coordinating groups at $11.75$ m, and two spatial envelopes at $23.0$ m, which are topological components rather than the two teams.

### 3.2 $H_1$ loop detection

On the primary match, the pipeline detects $403$ $H_1$ loops across 150 uniformly sampled frames (Table 1). Loops at the individual level are frequent and short-lived. They appear in $144$ of $150$ frames ($96.0\%$), at a mean rate of $2.52$ per frame, with low mean persistence ($1.974 \pm 1.118$ m). Loops at the tactical level are rarer but last longer: $23$ frames ($15.3\%$), mean rate $0.17$ per frame, mean persistence $3.914 \pm 2.745$ m, maximum $10.771$ m. Loops at the team level never occur ($H_1 = 0$ across all $1{,}500$ frames in the ten-match sample).

**Table 1.** Single-match $H_1$ statistics (primary match, $150$ frames).


| Level                 | Total loops | Frames with loops    | Mean loops/frame | Mean persistence  | Max persistence |
| --------------------- | ----------- | -------------------- | ---------------- | ----------------- | --------------- |
| Individual ($2.75$ m) | $378$       | $144/150$ ($96.0\%$) | $2.52$           | $1.974 \pm 1.118$ | $12.991$        |
| Tactical ($11.75$ m)   | $25$        | $23/150$ ($15.3\%$)  | $0.17$           | $3.914 \pm 2.745$ | $10.771$        |
| Team ($23.0$ m)       | $0$         | $0/150$ ($0\%$)      | N/A              | N/A               | N/A             |


> **Remark (Team-level $H_1$ vanishes a priori).** At $\delta = 23.0$ m the 22 players reduce to $k\le 2$ centroids in 93.6\% of complete frames on the ten-match sweep (Section 2.3). A Vietoris–Rips complex on at most two points cannot carry a non-trivial 1-cycle. Frames with $k=3$ are 6.4\% of that sweep; they are the only team-level configurations in which a loop is possible. Our headline $H_1$ analysis therefore runs at two levels (individual and tactical) against the three-level $H_0$ decomposition above. Team-level loop structure on the typical envelope would require a different representation (density fields or Delaunay triangulations, for example).

The two-level $H_1$ pattern extends to all ten matches ($1{,}500$ uniformly sampled frames; Table 2). Individual-level presence is $96.5 \pm 1.5\%$ ($95\%$ CI $95.6$–$97.3$), between $94.7\%$ and $98.7\%$ in every match. Tactical presence is $18.8 \pm 6.5\%$ ($95\%$ CI $15.2$–$22.7$), ranging from $11.3\%$ to $31.3\%$ across matches. The primary match ($15.3\%$ tactical) sits within one standard deviation of the ten-match mean. That match was chosen for broadcast quality and event annotation, not for its tactical $H_1$ rate.

**Table 2.** Multi-match $H_1$ statistics ($10$ matches). Presence = mean $\pm$ s.d. across matches; $95\%$ bootstrap CIs from $1{,}000$ resamples over matches.


| Level      | Total $H_1$ | Presence rate    | $95\%$ CI     | Mean persistence | Cross-match s.d. |
| ---------- | ----------- | ---------------- | ------------- | ---------------- | ---------------- |
| Individual | $4{,}039$   | $96.5 \pm 1.5\%$ | $95.6$–$97.3$ | $1.885$          | $0.149$          |
| Tactical   | $306$       | $18.8 \pm 6.5\%$ | $15.2$–$22.7$ | $0.647$          | $0.229$          |
| Team       | $0$         | $0.0 \pm 0.0\%$  | N/A           | N/A              | N/A              |


Mean persistence in Table 2 averages over all sampled frames, including those with no loop. The tactical entry is therefore lower than the primary-match mean in Table 1, which is taken only where loops appear.

The tactical level sits close to that floor. In the ten-match sample, $40.6\%$ of frames have four or fewer tactical centroids, and none of them carries a loop. Presence rate alone cannot tell arrangement from cluster count. We separate the two with the matched null of Section 2.6, which fixes centroid number and spatial envelope and randomises only arrangement.

Table 3 summarises the result. Tactical observed presence is more than twice the null rate. Table 4 splits by centroid count $k$. Presence is zero at $k \le 4$, as expected. It then rises from $9.3\%$ at $k = 5$ to $67.0\%$ at $k = 8$, always above the null. At the individual level the null already exceeds $91\%$: twenty points in a bounded region almost always close a cycle. The observed excess is therefore modest ($+5.1$ pp). Tactical $H_1$ exceeds the null once $k \ge 5$. Individual presence is already high under the null.

**Table 3.** $H_1$ presence against a cardinality- and envelope-matched null ($10$ matches, $1{,}500$ frames, $200$ null replicates per frame). Excess is in percentage points, with $95\%$ bootstrap CIs over matches.


| Level      | Observed | Null   | Excess  | $95\%$ CI       |
| ---------- | -------- | ------ | ------- | --------------- |
| Individual | $96.5\%$ | $91.4\%$ | $+5.1$  | $[+3.9, +6.1]$  |
| Tactical   | $18.8\%$ | $9.1\%$  | $+9.7$ | $[+7.3, +12.2]$ |


**Table 4.** Tactical-level $H_1$ presence by centroid count $k$, against the matched null of Table 3 ($10$ matches, $1{,}500$ frames).


| $k$     | Frames | Observed | Null    | Excess  |
| ------- | ------ | -------- | ------- | ------- |
| $\le 4$ | $609$  | $0.0\%$  | $0.4\%$ | $-0.4$  |
| $5$     | $344$  | $9.3\%$  | $4.1\%$ | $+5.2$  |
| $6$     | $252$  | $26.6\%$ | $12.0\%$ | $+14.5$ |
| $7$     | $149$  | $51.0\%$ | $21.7\%$ | $+29.3$ |
| $8$     | $94$   | $67.0\%$ | $33.4\%$ | $+33.6$ |
| $\ge 9$ | $52$   | $84.6\%$ | $49.0\%$ | $+35.6$ |




### 3.3 Closed cycle structures

All $403$ primary-match $H_1$ features receive a geometric realisation via closed-cycle identification. The representative is the graph-cycle proxy of Section 2.5, not a generator from the reduction matrix. Cycles at the individual level form short rings of centroids (typically three to six nodes in the examples we inspected). Tactical cycles are similarly small (often four or five nodes) but span larger gaps and persist longer. Figure 3 shows the same sample frame at both levels, with the cutoff and the filtration drawn as separate panels (sample frame 95). The left column is the vertex set after clustering. The right column is the longest-lived $H_1$ cycle on that set. At $\delta = 2.75$ m the vertices are four nearby players and the cycle edges are $17.8$–$19.2$ m ($p = 6.540$ m). At $\delta = 11.75$ m the vertices are four groups, one of them a $14$-player single-linkage cluster, and the cycle edges are $21.1$–$28.8$ m ($p = 9.942$ m). The two cycles are not the same bar at two resolutions. The persistence maxima in Table 1 are not used for the figure: the individual-level maximum (frame 141) is a near-collinear sliver.

> **Figure 3** (`figures/fig3_cycle_geometry.pdf`; not embedded in this Markdown copy). Cutoff versus filtration on one sample frame of SkillCorner match $1996435$ (sample frame 95). Left: vertex set after clustering at $\delta$. Gold markers belong to this row's cycle clusters; the hull in (c) is the $14$-player single-linkage cluster; dashed circles have radius $\delta$ on the cycle vertices only. Right: longest-lived $H_1$ representative on those vertices ($p = 6.540$ m and $p = 9.942$ m). Cycle edges are filtration distances ($17.8$–$19.2$ m in (b); $21.1$–$28.8$ m in (d)), not the cutoff. Panel (d) draws centroids, not the absorbed players. Compact four-cycles at both levels, not the persistence maximum. A 10 m scale bar is shown on each panel. Uniform sample, $n = 150$ frames, every $290$th complete frame (same rule as the ten-match analysis).



### 3.4 Sensitivity analysis

Tactical $H_1$ counts fall monotonically as the cutoff widens. On the primary match's 150 frames, sweeping $\delta \in [6, 16]$ m gives $275$ loops ($87.3\%$ of frames) at $\delta = 6$ m and none at $\delta = 16$ m. The operative range is $[6, 14]$ m (Table 6). The adopted cutoff $\delta = 11.75$ m lies at the conservative end of that range ($15.3\%$ frame presence).

**Table 6.** Tactical-level cutoff sensitivity ($150$ frames, primary match).


| $\delta$ (m) | Total $H_1$ | Frame presence | Mean $H_0$ |
| ------------ | ----------- | -------------- | ---------- |
| $6$          | $275$       | $87.3\%$       | $13.4$     |
| $8$          | $162$       | $68.0\%$       | $9.8$      |
| $10$         | $78$        | $42.7\%$       | $7.0$      |
| $11.75$      | $25$        | $15.3\%$       | $5.0$      |
| $12$         | $21$        | $12.7\%$       | $4.8$      |
| $14$         | $5$         | $3.3\%$        | $3.5$      |
| $16$         | $0$         | $0.0\%$        | $2.8$      |


The truncation in equation (1) is likewise stable. At $\delta = 11.75$ m, every percentile from $P_{50}$ to $P_{95}$ yields the same $25$ loops and $15.3\%$ frame presence, even though mean $\varepsilon_{\max}$ spans $37.6$–$65.3$ m (Table 7).

**Table 7.** Filtration-percentile ablation, $\delta = 11.75$ m.


| Percentile | Total $H_1$ | Frame presence | Mean $\varepsilon_{\max}$ (m) |
| ---------- | ----------- | -------------- | ----------------------------- |
| $P_{50}$   | $25$        | $15.3\%$       | $37.6$                        |
| $P_{60}$   | $25$        | $15.3\%$       | $41.8$                        |
| $P_{75}$   | $25$        | $15.3\%$       | $49.6$                        |
| $P_{90}$   | $25$        | $15.3\%$       | $60.0$                        |
| $P_{95}$   | $25$        | $15.3\%$       | $65.3$                        |




### 3.5 Complementarity of the two $H_1$ levels

The two $H_1$ levels carry related but largely distinct information. Over $1{,}500$ uniformly sampled frames, total individual and tactical $H_1$ persistence correlate weakly (Spearman $\rho = 0.234$, $p < 0.001$; $95\%$ bootstrap CI $[0.181, 0.276]$). The same holds for loop counts ($\rho = 0.205$, $p < 0.001$). The finding does not depend on how persistence is summarised.

Co-occurrence exceeds chance (Fisher odds ratio $6.12$, $p = 0.002$; bootstrap CI $[2.32, 16.33]$). Table 5 shows the asymmetry: $1{,}167$ frames carry individual loops without a tactical partner, and only two frames do the reverse. Weak rank correlation remains the main evidence for complementarity. Joint presence need not mean the two levels measure the same structure.

**Table 5.** Frame counts of $H_1$ presence at the two levels ($1{,}500$ frames).


|                          | Tactical $H_1$ present | Tactical $H_1$ absent |
| ------------------------ | ---------------------- | --------------------- |
| Individual $H_1$ present | $280$                  | $1{,}167$             |
| Individual $H_1$ absent  | $2$                    | $51$                  |


A TDA-native check agrees. Bottleneck distance between the two levels' diagrams has median $1.456$ m and $95$th-percentile tail $3.556$ m. That is on the order of typical tactical loop size on the primary match ($3.914$ m mean persistence where loops appear; Table 1). Landscape $L^2$ distance has median $5.477$. The levels differ by roughly as much as their features are large, not by a small perturbation of one shared pattern.

### 3.6 Event correlation

As a sanity check against measurement noise, we asked whether persistence moves with real match events (SkillCorner annotations; $103{,}856$ event–topology pairs across ten matches). Events that disrupt shape (on-ball engagements, quick breaks) tend to precede lower persistence. Sustained build-up tends to precede higher persistence (Mann–Whitney $U$ on pre-specified classes; several nominal $p < 0.001$ at both levels). We treat this as construct validity only. Multiple-testing control and football interpretation belong elsewhere.

---



## 4. Discussion



### 4.1 Operating range

The result that matters for use is the width of the operating range. $H_1$ detection holds across a band of cutoffs and across every truncation percentile tested (Section 3.4). A pipeline that works only at one finely tuned setting would not travel. This one does, once interaction lengths are re-derived on a new domain.

The three $H_0$ regimes are the cardinality targets of Section 2.3, read from the pooled $H_0(\delta)$ curve on every complete frame of the ten matches (Figure 2). Their persistence across that band, rather than a spike at the adopted cutoffs, is what makes the regimes usable.

### 4.2 Distinct structure at two levels

The two levels are not measuring the same structure at different resolutions. If the tactical signal were a coarsened version of the individual signal, the two would co-occur far more consistently than Table 5 shows. The bottleneck and landscape distances would also be small relative to each level's own persistence values (Section 3.5). Clustering before persistent homology is therefore not a convenience for separating noise. It produces two informationally distinct objects.

### 4.3 Limitations

Linkage selection is a substantive methodological choice. Across a $600$-frame, four-match comparison sample, single-linkage detects $106$ tactical-level $H_1$ loops. Complete-linkage detects $802$. Ward's method detects $822$. That is a difference of almost an order of magnitude. The gap is large enough to change which scientific picture the data support, not merely the precision of one estimate. We retain single-linkage because its definition is the most natural reading of spatial proximity. It is also robust against over-partitioning artefacts. We treat the gap with the other two methods as an open question.

A more principled selection criterion would come from the dynamical system itself, rather than from clustering-quality metrics alone. One candidate is the linkage under which a governing equation for a persistence functional admits the sparsest representation, in the sense of sparse identification of nonlinear dynamics. The functional would be the landscape $L^2$ norm or the tactical $H_1$ total-persistence sequence. Operationalising this would require three things. First, choose the dynamical state. Second, defend the sparsity of the recovered library against AIC, BIC, or cross-validation baselines. Third, confirm that the resulting persistence sequence is genuinely lower-dimensional under the selected linkage. We defer this to the forthcoming full-season work. A population-sized sample of match sequences is what makes the sparsity comparison meaningful.

The tactical cutoff is the inversion of a named cardinality (mean $H_0$ nearest 5, with $k \ge 4$ still common; Figure 2c). On the 1 Hz diagnostic subset the only interior silhouette local maximum is at $7.0$ m, a small-group alternative that keeps rising into the two-envelope regime once $k=1$ frames are dropped (Supplementary Figure S2). Those features are characteristic separations, not adopted cutoffs. A landscape-path stability criterion remains a future estimator. We defer it to the persistence-landscape companion work.

The pipeline identifies three $H_0$ regimes but only two $H_1$ regimes: at the team level the reduced cloud almost never has enough centroids to close a loop (see the team-level Remark in Section 3.2). Recovering team-level loop structure on the typical envelope would require a different representation, such as spatial density fields or Delaunay triangulations.

All data analysed here are broadcast-derived tracking at $10$ Hz. Broadcast tracking typically offers lower spatial precision than higher-frequency optical systems. That may affect the magnitude of persistence values reported. The structural findings (the three $H_0$ regimes, the $H_1$ presence rates, and the sensitivity profiles) depend on relative rather than absolute spatial precision. They are therefore expected to be robust across tracking technologies. A direct comparison of persistence magnitudes against optical tracking data remains for future work.

### 4.4 Outlook

Two extensions are in progress. The ten-match evidence base is being scaled to a full season of Championship matches. That sample will characterise population-level distributions of $H_0$ and $H_1$ counts, barcode lengths, and landscape norms, and will test tactical-fingerprint classification at population scale. It is also the setting in which the linkage criterion proposed above becomes evaluable. Recovering a sparse governing equation for a persistence functional requires the population-sized sample of match sequences that a single season provides. Separately, persistence landscape dynamics are being developed to treat each match as a path through landscape space. That is the setting in which the landscape-stability cutoff criterion can itself be evaluated. Its resampling unit is the match-level landscape, not the per-frame summary used here.


---



## 5. Conclusion

On ten professional football matches, clustering at recovered interaction lengths and a truncation of the Vietoris–Rips parameter produced three stable $H_0$ regimes and two $H_1$ regimes. The two $H_1$ levels carry complementary rather than redundant information. Those findings answer whether persistent homology can be made scale-attributable on a competitive collective system. Scale conflation is the underlying TDA fact: a single filtration on a hierarchically organised point cloud mixes organisational levels. Football was the measurement setting. The same pipeline applies to other bounded competitive systems once interaction lengths are re-derived.

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

### Clustering-quality diagnostics

The cutoffs are fixed by cardinality inversion, not by a quality score. For completeness, Supplementary Figure S2 (`figures/figS2_cutoff_diagnostics.pdf`) records the Calinski--Harabasz index, mean silhouette, and information-content on the 1 Hz subset (each min-max scaled). Silhouette is undefined at $k=1$ and those frames are omitted, not coded as 0. The silhouette rise at large $\delta$ is an artefact of the shrinking $k \ge 2$ subsample; the only interior local maximum is at $7.0$ m, a small-group alternative we report but do not adopt. None of these curves selects the adopted cutoffs. Generate with `pipeline/steps/10_cutoff_sweep_figure.py`.

### Temporal autocorrelation

Headline tables use the uniform 150-frame rule of Section 2.1. Supplementary Figure S1 (`figures/figS1_acf.pdf`) is a diagnostic on the primary match at 1 Hz; it does not choose the stride. Generate with `pipeline/steps/09_acf_supplement.py`.