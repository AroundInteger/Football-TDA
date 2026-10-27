# Multi-Scale Persistent Homology for Competitive Collective Systems

> **Review source (9 September 2026).** Prose is edited in this file. `sections/*.tex` is synced to this pass for Overleaf (equations, tables, figures) and the arXiv upload.

**Authors:** Rowan Brown  
**Affiliation:** Swansea University  

**Target:** arXiv preprint now; journal refinement for *Journal of Applied and Computational Topology* (JACT).  
**Status:** Working manuscript in arXiv format (`arxiv.sty`). Not yet posted.

**This file.** Markdown review copy for Cursor. `main.tex` and `sections/*.tex` match this pass. Overleaf can take a one-shot upload of those files, plus `arxiv.sty`.

**Citations.** The Markdown review copy keeps author–year for readability. The compiled manuscript uses Vancouver numbers (`natbib` `numbers,sort&compress` + `unsrtnat`).

---



## Note for collaborators

**What this paper is.** A mathematics-first methods paper. It asks whether a multi-scale persistent homology pipeline is *sound* on a real, high-frequency, noisy multi-agent point cloud. Football is the validated testbed, not the audience.

**What it is not.** A football-analytics paper. Event interpretation, geometric baselines, bilateral (home/away) coupling, and predictive utility belong to a companion manuscript (Paper B, *Journal of Sports Sciences*, in preparation). Paper A treats event correlation only as a one-sentence construct-validity check (“not noise”).

**Headline claim.** Hierarchical clustering at recovered interaction lengths, then Vietoris–Rips persistence on the centroids out to the cloud diameter, resolves scale conflation in competitive collective systems. On ten professional matches, answering the four questions in turn: (Q1) three stable $H_0$ regimes are recovered from the data; (Q2) $H_1$ is detected at the individual and tactical levels, and every finite bar on the primary match has a simple-cycle representative, present at birth by construction; (Q3) the two $H_1$ levels carry distinct information; and (Q4) topological features track on-ball events, as construct validity only. A team-level loop needs four centroids. That count occurs in 141 of 436,648 frames, and those frames have $H_1=0$.

**Locked cutoffs (metres).** Individual $2.75$; tactical $11.75$; team $23.0$. Cardinality inversion on all complete frames of the ten Table S1 matches (436{,}648 frames). Operative tactical $H_1$ range: re-centre on $11.75$ m after the H1 cascade.

**Sample.** Ten A-League matches, SkillCorner open broadcast tracking at $10$ Hz. Persistent homology on $150$ uniformly spaced complete frames per match ($1{,}500$ frames in total). Primary match: SkillCorner ID $1996435$, $43{,}531$ complete $22$-player frames.

**Filtration lifetime (locked).** Presence: fraction of frames with at least one finite $H_1$ bar. Filtration lifetime $p$: death minus birth, in metres (bar length, not clock time). Total persistence: sum of $p$ in a frame. The 150-frame sample does not measure loop duration in seconds.

**Event $\Delta$ (locked).** Topology at $1$ Hz (every tenth complete frame), not $\tilde{T}$. Window: five $1$ Hz frames ($5$ s) either side of the event; the event frame is excluded.

**Open methodological questions (already flagged in the paper).** Linkage choice (single vs complete vs Ward changes tactical $H_1$ by nearly an order of magnitude); a more principled tactical cutoff; team-level loops on the typical two-centroid envelope would need a different representation.

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

**Shared wording (locked, abstract + §1).** Use these forms later, do not reinvent them. A level is named by how many groups it contains (cardinality). The cutoff $\delta$ is read from the *group-count curve*, not assumed from the class. Persistent homology records connected components ($H_0$) and loops ($H_1$) as a distance parameter grows. Bar *length* is a distance; it is not clock time. Metres appear only after positions are on a pitch.

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

Competitive collective systems, including sports teams contesting a pitch, organise at several named levels at once: individuals, small groups, and a system-wide envelope. Persistent homology records connected components ($H_0$) and loops ($H_1$) as a distance parameter grows. On the full point cloud those levels mix in one diagram, so a change cannot be assigned to a level. This paper asks whether the homology can be made scale-attributable: each diagram belonging to one organisational level.

Positions are recorded in metres on a standard football pitch. The levels are named by how many groups they contain, not by an assumed length. A cutoff sweep then recovers those distances from the group-count curve. Hierarchical clustering at those recovered lengths decomposes the cloud, and persistent homology is computed on the resulting centroids.

On ten professional football matches (broadcast tracking at 10 Hz, positions in metres), the named group-count targets are met at individual (2.75 m), tactical (11.75 m), and team (23.0 m). At the team cutoff, four centroids occur in 141 of 436,648 frames (a loop needs four vertices); none of those frames carries a loop. Loops appear at the individual level in $96.5\pm 1.5\%$ of frames (mean bar length 1.886 m) and at the tactical level in $18.8\pm 6.5\%$ of frames (mean bar length 3.411 m). On the primary match, every finite $H_1$ bar has a simple-cycle representative, present at birth by construction, and the two levels carry distinct information. Applying the pipeline to another bounded competitive system requires re-deriving the interaction lengths, which is not tested here.

**Keywords:** Vietoris–Rips filtration, topological data analysis, spatial tracking, hierarchical clustering, team sports

---



## 1. Introduction



### 1.1 Background

Collective systems of agents in space are typically hierarchically organised. Starling murmurations, fish shoals, and insect swarms, for example, show individuals, local groups, and a system-wide envelope at once (Sumpter, 2006). Understanding how those organisational levels interact is a standing challenge in applied mathematics, and one that high-frequency spatial tracking data is increasingly able to inform (Herbert-Read et al., 2011).

Competitive collective systems are a subset of that class: agents distributed in a bounded domain, coordinating internally while responding to an opponent. Examples that share this structure are autonomous vehicle fleets sharing road space, opposing crowd flows at transport hubs, predator–prey populations in an ecosystem, and sports teams contesting pitch or court territory.

Agents in such systems can arrange themselves in ring-like formations that enclose empty space: milling in a fish school, a vortex in a swarm, or, in the competitive subset, encirclement of an opponent. These arrangements are important to identify because enclosure is a distinct mode of organisation, not a change in density or alignment. A loop holds a region of space, whether that region is an empty core or the space denied to an opponent. Conventional geometric summaries, including convex-hull area, nearest-neighbour distance, and polarisation, capture dispersion and alignment (Sumpter, 2006) but do not directly quantify this loop structure.

Persistent homology, a central tool of topological data analysis (TDA), records connected components ($H_0$) and loops ($H_1$) as a distance parameter grows (Edelsbrunner et al., 2002; Edelsbrunner and Harer, 2010; Carlsson, 2009; Munch, 2017; Chazal and Michel, 2021). A filtration of simplicial complexes indexed by that parameter tracks the birth and death of those features. Each feature is recorded as a bar: the interval from the distance at which it appears (birth) to the distance at which it disappears (death) (Ghrist, 2008). The length of the bar distinguishes a stable enclosure from a fleeting coincidence of positions. The collection of bars is the persistence diagram (Cohen-Steiner et al., 2007). Efficient computation via the Vietoris–Rips filtration is due to Bauer (2021); persistence landscapes provide a functional representation for later statistical analysis (Bubenik, 2015).

Persistent homology has recovered cavities in protein atom clouds that mark flexibility and folding (Xia and Wei, 2014). It has identified medium-range order in amorphous solids that conventional crystallography does not resolve (Hiraoka et al., 2016). In biological aggregation models it has shown that distinct swarming organisations appear at different filtration values (Topaz et al., 2015). The same single-parameter construction, applied directly to a hierarchically organised multi-agent point cloud, raises the measurement difficulty treated in Section 1.2. This paper asks whether that homology can be made scale-attributable on a competitive collective system: each diagram belonging to one organisational level.

### 1.2 The Scale Conflation Problem

A single-parameter Vietoris–Rips filtration on the full point cloud records features at many filtration values in one persistence diagram. Bars born at different distances therefore occupy the same object, whether they arise from local proximity, small-group arrangement, or system-wide organisation. If that mixing is not recognised, and the diagram is read as if the cloud had a single organisational level, features from distinct levels are treated as commensurate. A change in the diagram then cannot be assigned to a level: it may be a local rearrangement, a change in group structure, or a change in the system envelope, and those alternatives are not distinguished. Counts and persistence summaries inherit the same ambiguity.

Applied studies make that mixing visible without removing it. Component and loop counts (Betti numbers) from biological aggregation models, plotted against simulation time and filtration value, show that distinct swarming organisations appear at different filtration values (Topaz et al., 2015). That display remains one mixed summary. A parallel construction computes Vietoris–Rips features on multi-agent snapshots and yields a topological time series at a chosen scale (Gu et al., 2022). That series can detect change points; it does not decompose the cloud by organisational level.

Responses for the general case exist, but they do not return a scale-attributable diagram. Multiparameter persistence treats several scales as simultaneous algebraic parameters (Botnan and Lesnick, 2023). The output is a module in several filtration parameters, not a single persistence diagram that names an organisational level. The construction is at present computationally feasible only on clouds far smaller, and sampled far more slowly, than a video-rate cloud of a few dozen agents. Persistent homology of multiscale clusterings, by contrast, analyses the hierarchy produced by the clustering itself (Schindler and Barahona, 2023). The output is a topological summary of how partitions merge as the cutoff varies, not a diagram of loops among units at one chosen level.

The methods above leave that mixing in place: a bar records when a loop closes, not which organisational level enclosed it. In a competitive collective system those levels are named (individual, small group, envelope), so a superimposed diagram cannot attribute an $H_1$ feature to a named organisational level, or assign a change in the diagram to one level rather than another.

### 1.3 Contributions

Section 1.2 leaves a concrete question: whether persistent homology can be made scale-attributable on a competitive collective system. This paper answers that question by changing the input rather than slicing bars of one diagram.

A cutoff distance $\delta$ groups nearby agents and replaces each group by its centroid. The reduced cloud then represents one organisational level, named by how many groups it contains (its cardinality). The value of $\delta$ is not assumed from the class; it is read from the group-count curve (Section 2.3). Vietoris–Rips homology is then computed on those centroids, out to the diameter of the reduced cloud (Section 2.4). Each finite $H_1$ bar is assigned the 1-cycle returned by the boundary-matrix reduction, and that cycle is present at birth by construction (Section 2.5). Neither clustering nor the usual Vietoris–Rips filtration is algebraically new (Carlsson and Mémoli, 2010; Schindler and Barahona, 2023); the content is that the combination remains effective on a real, high-frequency, noisy point cloud.

We test the pipeline on football broadcast tracking: the positions of all 22 players at $10$ Hz from televised professional matches, as $(x,y)$ coordinates in metres on a standard pitch model, for ten A-League matches from the SkillCorner open repository (Section 2.1). Four questions organise the results, and each is answered in turn:

**(Q1)** Can the organisational levels be recovered from the group-count curve rather than assumed as lengths in metres (Section 3.1)?
**(Q2)** Does scale-attributable persistent homology then detect $H_1$ loop structure at those levels, does each finite bar on the primary match have a simple-cycle representative that can be drawn in space, and how does detection change with the cutoff (Sections 3.2–3.4)?
**(Q3)** Where loops appear at more than one level, do those levels carry distinct rather than redundant information (Section 3.5)?
**(Q4)** Do the topological features track on-ball match events, as a construct-validity check only (Section 3.6)?

Spatial analysis of team sport is surveyed by Gudmundsson and Horton (2017). Network approaches include Grund (2012) and Buldú et al. (2019). Together these cover pitch-control models and network metrics on passing and collective structure. They complement the present pipeline but do not quantify two-dimensional enclosure through persistent homology. To our knowledge, no prior work combines cutoff-selected organisational levels with persistent homology for a competitive collective system, or recovers the resulting regimes on high-frequency tracking across multiple independent recordings.

---



## 2. Methods



### 2.1 Data

The primary single-match analysis uses SkillCorner open broadcast tracking data, match ID $1996435$ (Sydney FC versus Adelaide United, A-League 2024/25). Positions are recorded at $10$ frames per second as $(x, y)$ coordinates in metres on a standard football pitch model. Only frames with complete $22$-player coverage are retained, which yields $43{,}531$ frames (approximately $72$ minutes at this sampling rate). The multi-match sample comprises that match and nine further A-League matches from the same repository. Each match contributes approximately $39{,}000$–$49{,}000$ complete frames, and the ten matches together give $436{,}648$ frames. SkillCorner match IDs and fixtures are listed in Supplementary Table S1.

Consecutive complete frames share nearly the same configuration, so the full stream is not treated as a sequence of independent snapshots. Connected-component and loop summaries are estimated on a uniform subsample instead. Write $t$ for the time of a complete frame in the native stream. The same operational rule is used on every match: list the complete $22$-player frames, set the stride to $\lfloor N/150\rfloor$, and retain $150$ frames. Write $\tilde{t}$ for a time retained by that rule, and $\tilde{T}$ for the set of such times on one match, so $|\tilde{T}|=150$. On the primary match $N = 43{,}531$, so the stride is $290$ frames ($\approx 29$ s). Across ten matches the sampled times give $1{,}500$ frames.

This subsample limits temporal pseudo-replication but does not remove a second dependence: opposition couples successive positions (competitive dependence), an inference problem not treated here. Nor can the subsample resolve formation or dispersion of loops between samples. Event association is a construct-validity check, not a dynamical model, and it does not use $\tilde{T}$. Topology for that check is computed on every tenth complete frame ($1$ Hz). Supplementary Figure S1 records the autocorrelation of those $1$ Hz summaries on the primary match, as a diagnostic. The figure does not determine the subsample $\tilde{T}$.

### 2.2 Hierarchical clustering

On this corpus the named organisational levels of Section 1.2 (individual, small group, envelope) are instantiated as individual, tactical, and team. Each level is named by how many groups it contains. The cutoff $\delta$ that selects it is read from the group-count curve in Section 2.3.

Figure 1 summarises the pipeline of Sections 2.2--2.5. The pipeline is applied at the sampled times $\tilde{t}\in\tilde{T}$ of Section 2.1. The input is the point cloud $P(\tilde{t}) = \{p_1(\tilde{t}), \dots, p_{22}(\tilde{t})\} \subset \mathbb{R}^2$.

> **Figure 1** (`figures/fig1_pipeline_schematic.pdf`). Analysis pipeline on a bounded domain (schematic geometry on a football pitch). **(a)** Colour-coded local groups in $P(\tilde{t})$ with dashed $\delta$-disks and a representative gap $< \delta$ (Section 2.2). **(b)**–**(d)** Vietoris–Rips on the cluster centroids $\tilde{P}(\tilde{t})$ at three increasing $\varepsilon$, out to the diameter of the reduced cloud (Section 2.4). **(e)** Finite $H_1$ birth–death pairs. **(f)** The same pairs as a barcode. **(g)** The 1-cycle returned by the boundary-matrix reduction for an $H_1$ pair (Section 2.5); grey diagonals enter at death. Figure 3 shows the cycle step on real tracking data.

Single-linkage hierarchical clustering is applied at a cutoff distance $\delta > 0$. It partitions $P(\tilde{t})$ into clusters $C_1, \dots, C_k$ in which every pair of points is connected by a chain of pairwise distances not exceeding $\delta$. Each cluster is replaced by its centroid, giving the reduced point cloud

$$
\tilde{P}(\tilde{t})=\left\{\bar{c}_j : \bar{c}_j=\frac{1}{|C_j|}\sum_{p\in C_j} p,\ j=1,\dots,k\right\},
$$

and persistent homology is then computed on $\tilde{P}(\tilde{t})$ rather than on $P(\tilde{t})$.

Complete-linkage and Ward's method are not used for the headline analysis. Their effect on $H_1$ counts is examined in Section 4.5. Team identity is withheld as an input, so the partitions are spatial rather than labelled by side.

### 2.3 Cutoff selection

As the cutoff lengthens, nearby agents merge and the mean number of groups falls. Each organisational level takes its distance from the point on that curve where the group count named in Section 2.2 is reached.

A complete frame has $n=22$ agents. The sweep uses every complete 22-player frame of the ten matches in Supplementary Table S1 ($436{,}648$ frames). The grid is $\delta \in [0.25, 40.0]$ m at $0.25$ m steps (160 points). No random window is drawn, and epoch lengths are not mixed. Clustering is single-linkage, and team labels are unused.

Let $\overline{H_0}(\delta)$ denote that curve: the mean group count at cutoff $\delta$, pooled over those frames. Let $P(k \ge 4;\delta)$ be the fraction of frames with at least four groups. The three inversion rules are then as follows:

- individual: largest $\delta$ with $\overline{H_0}(\delta) \ge n-3=19$;
- tactical: $\delta$ minimising $|\overline{H_0}(\delta)-5|$, among candidates with $P(k \ge 4;\delta) \ge 0.5$;
- team: smallest $\delta$ with $\overline{H_0}(\delta) \le 2$.

Ties take the smaller $\delta$. The three targets are stated as group counts. The individual target $n-3=19$ is a mostly resolved set of agents. The tactical target $5$, with $k \ge 4$ still common, is a handful of coordinating groups. A loop needs at least four vertices, so the tactical rule keeps that count. The team target $2$ is at most two spatial envelopes.

On this corpus the inversion returns $2.75$ m, $11.75$ m, and $23.0$ m. Pooled mean group count at those cutoffs is $19.31$, $5.06$, and $1.98$. Inverting each match separately gives $2.80 \pm 0.20$ m, $11.80 \pm 0.35$ m, and $22.98 \pm 0.72$ m (mean $\pm$ s.d. across matches). Acceptance requires every match's mean $\overline{H_0}$ at the pooled cutoff to lie in $[15, 22]$, $[4, 10]$, and $[1, 2.5]$ respectively. All ten matches lie inside those bands.

The curve is asymmetric. Nearby agents merge quickly, at about $1.6$ groups per metre from $\overline{H_0}=19$ to $5$. Larger gaps then resist merging, at about $0.27$ groups per metre from $5$ to $2$. The remaining gaps are the large between-group distances. That flattening is why the team cutoff sits far out at $23.0$ m and still returns two spatial envelopes. Team labels are withheld, so the partition is spatial; agreement with the two sides was not tested.

Clustering-quality diagnostics (Calinski--Harabasz, silhouette, and Shannon entropy of cluster sizes) are recorded on a deterministic $1$ Hz subset (every 10th complete frame). Silhouette is omitted when $k=1$; it is not coded as $0$. Those curves are alternatives, not adopted cutoffs, and are reported in Supplementary Figure S2. Figure 2 shows the estimator and its spatial realisation. Section 3.4 reports how tactical $H_1$ detection responds to the cutoff choice.

> **Figure 2** (`figures/fig2_cutoff_sweep.pdf`). Cutoff selection from the group-count curve, on all complete frames of the ten SkillCorner matches (436{,}648 frames); not $\tilde{T}$. **(a)** Pooled mean group-count curve $\overline{H_0}(\delta)$ (black) with the ten per-match curves (grey); targets are group counts $\overline{k} = 19$ (most agents resolved), $5$ (a few coordinating groups; a loop needs four vertices), and $2$ (two spatial envelopes; team labels withheld, agreement with sides not tested). Circles mark the inversion at $2.75$, $11.75$, $23.0$ m (top axis); inset zooms the individual rule. **(b)** Per-frame $H_0$ distribution (median, interquartile, 5th--95th bands); brackets are the acceptance intervals $[15,22]$, $[4,10]$, $[1,2.5]$; orange dots are the ten per-match means, all inside. **(c)** Feasibility: $k$ is the per-frame group count and $P(k \ge 4)$ the fraction with at least four; the adopted $11.75$ m sits at $P = 0.80$, inside the feasible region ($\delta \le 13.5$ m). **(d--f)** The same cutoffs on primary-match sample frame 95 ($H_0 = 20, 7, 2$; one frame, near the pooled targets $19, 5, 2$). Coloured hulls are multi-player clusters, grey are singletons; colours distinguish separate topological components in this frame, not player teams. Clustering-quality diagnostics are in Supplementary Figure S2 and are not the selector.

### 2.4 Filtration extent on reduced clouds

The Vietoris–Rips complex is computed in the usual way on the reduced cloud. Each reduced cloud has at most 22 centroids, so the full filtration is inexpensive and is run to the diameter: the maximum pairwise distance between centroids. At that extent the complex is a full simplex, so every $H_1$ class on this corpus is finite.

Persistence diagrams are computed with Ripser via Ripser.py (Bauer, 2021), with coefficients in $\mathbb{F}_2$. We report finite $H_1$ bars. The Results use three summaries of those bars. *Presence* is the fraction of frames with at least one finite $H_1$ bar. *Filtration lifetime* $p$ is death minus birth: the length of a bar, in metres on the Vietoris–Rips parameter. *Total persistence* is the sum of $p$ over the finite bars in a frame. It is the Spearman input in Section 3.5. None of these summaries is a duration in seconds, and the 150-frame subsample of Section 2.1 does not measure how long a loop lasts on the clock. The $H_0$ counts reported in Section 3.1 are read from these diagrams at filtration zero. We cross-checked all primary-match diagrams against GUDHI (The GUDHI Project, 2024) and giotto-tda (Tauzin et al., 2021). Birth–death pairs agreed to within numerical tolerance ($10^{-6}$ m). GUDHI is also used for the bottleneck-distance and landscape computations reported in Section 3.5.

### 2.5 Closed cycle identification

Each finite $H_1$ bar is assigned the 1-cycle returned by column reduction of the Vietoris–Rips boundary matrix over $\mathbb{F}_2$. Because the filtration runs to the diameter, the complex contains every edge and every triangle on the centroid cloud. The reduction pairs the edge that creates the class with the triangle that destroys it. The representative is the reduced boundary of that triangle. Every edge of the cycle has length at most the birth value, and the longest edge is the creating edge, so the cycle is present in the complex at birth. A triangle cannot represent a bar (Section 2.3). On the primary match the representative is a simple cycle for all 403 finite bars (Section 3.3). Birth–death values from the reduction match the Ripser diagrams to within $10^{-5}$ m; the looser tolerance relative to the GUDHI check ($10^{-6}$ m) is stored float32 precision in the Ripser diagrams.

### 2.6 Statistical tests

$H_1$ detection could reflect the number of centroids rather than their arrangement. Each frame is therefore compared against a matched null. For a frame whose clustering yields $k$ centroids, the null holds $k$ fixed and draws $k$ points uniformly from the convex hull of those same centroids. The null points therefore lie inside the observed hull; the hull vertices are not kept. Only the arrangement is randomised. The same filtration extent (cloud diameter) is used on each null cloud. We use $200$ null replicates per frame. The reported statistic is the excess of observed over null $H_1$ presence, with $95\%$ confidence intervals from bootstrap resampling over matches.

Complementarity of the two $H_1$ levels (Section 3.5) is assessed by two frame-level tests. The Spearman rank correlation is computed on total $H_1$ persistence: the sum of death minus birth over all finite $H_1$ bars in a frame. The same correlation is also reported on loop counts, as a robustness check. Fisher's exact test is computed on the binary co-occurrence of $H_1$ presence at the two levels. Both statistics carry $95\%$ confidence intervals obtained by bootstrap resampling over matches ($1{,}000$ resamples), with the match as the resampling unit. Bottleneck and landscape distances between the two levels' persistence diagrams are computed using GUDHI, as described in Section 2.4.

The construct-validity check in Section 3.6 uses a two-sided Wilcoxon signed-rank test of $\Delta$ against zero. Exact zeros are discarded before ranking (SciPy `zero_method='wilcox'`). For these sample sizes the $p$-value is SciPy's asymptotic approximation (`method='auto'`, SciPy 1.13.1). The individual engagement and build-up classes have no exact zeros. The tactical classes do, and those zeros are discarded before ranking. The means include them. Topology is evaluated on every tenth complete frame ($1$ Hz), not on $\tilde{T}$. For each annotated event, $\Delta$ is the change in mean total persistence from the five $1$ Hz frames immediately before the event to the five immediately after it. The window is five seconds either side of the event; the event frame itself is excluded. Event classes are pre-specified, and the $p$-values are nominal.

### 2.7 Software and reproducibility

All analyses were performed in Python 3.11. Persistence diagrams are computed with Ripser.py 0.6.12 (Bauer, 2021; Tralie et al., 2018). Bottleneck distances and landscape representations use GUDHI 3.11.0. giotto-tda 0.6.0 provided independent cross-checks. Supporting scientific Python packages match the pinned `requirements.txt` accompanying the manuscript: NumPy 2.0.2, SciPy 1.13.1, pandas 2.3.2, scikit-learn 1.6.1. Analysis code, pipeline configuration, and pinned dependencies are included with the manuscript materials. They will be released in a public repository at arXiv posting (see Data Availability Statement).

---



## 3. Results



### 3.1 Connected components ($H_0$)

Addressing Q1, the homology sample confirms the three organisational levels read from the group-count curve in Section 2.3. At filtration zero, $H_0$ equals the group count $k$ by construction, so the check is that the subsample matches the full-sweep counts. Those levels are individual ($\delta = 2.75$ m), tactical ($\delta = 11.75$ m), and team ($\delta = 23.0$ m). Primary-match figures come from the uniform 150-frame sample of match 1996435 (Section 2.1). Ten-match aggregates use the same sampling scheme ($1{,}500$ frames in total).

At the individual level, $H_0 = 19.32 \pm 2.34$ (mean $\pm$ s.d.; range 10--22). At the tactical level, $H_0 = 5.04 \pm 1.69$ (range 2--10). At the team level, the cloud usually collapses to one or two groups: mean $1.96 \pm 0.36$. All 22 players lie in a single group in 8.7\% of frames, split across two in 86.7\%, and across three in 4.7\%.

The same three-level pattern holds in all ten matches. Grand means are individual $H_0 = 19.31 \pm 0.31$, tactical $H_0 = 5.09 \pm 0.38$, and team $H_0 = 1.98 \pm 0.06$ (mean $\pm$ s.d. across matches). Every match stays within the acceptance intervals of Section 2.3: the ten per-match means all fall inside $[15,22]$, $[4,10]$, $[1,2.5]$ (Figure 2b). Figure 2 records the sweep from which those cutoffs were taken. The pooled curve is asymmetric (about $1.6$ groups merge per metre from the individual to the tactical level, but only $0.27$ per metre from the tactical to the team level), so the two envelopes remain over a wide band of $\delta$ (Figure 2a). The spatial realisation on one frame (Figure 2d--f) shows the same regimes: a mostly resolved set of agents at $2.75$ m, a handful of coordinating groups at $11.75$ m, and two spatial envelopes at $23.0$ m (topological components; agreement with the two sides was not tested).

### 3.2 $H_1$ loop detection

For Q2, scale-attributable homology detects loop structure at two of the three recovered levels. On the primary match, the pipeline detects $403$ $H_1$ loops across 150 uniformly sampled frames (Table 1). Loops at the individual level are frequent. They appear in $144$ of $150$ frames ($96.0\%$), at a mean rate of $2.52$ per frame, with short filtration lifetime ($\bar{p}=1.931 \pm 1.735$ m). Loops at the tactical level are rarer: $23$ frames ($15.3\%$), mean rate $0.17$ per frame, with longer filtration lifetime ($\bar{p}=3.778 \pm 2.723$ m, maximum $10.771$ m). Loops at the team level never occur ($H_1 = 0$ across all $1{,}500$ frames in the ten-match sample).

**Table 1.** Single-match $H_1$ statistics (primary match, $150$ frames). $\bar{p}$ is the mean of death minus birth over loops, in metres on the Vietoris–Rips parameter, not a duration in time.


| Level                 | Total loops | Frames with loops    | Mean loops/frame | Mean filtration lifetime $\bar{p}$ (m) | Max $p$ (m) |
| --------------------- | ----------- | -------------------- | ---------------- | ----------------- | --------------- |
| Individual ($2.75$ m) | $378$       | $144/150$ ($96.0\%$) | $2.52$           | $1.931 \pm 1.735$ | $12.991$        |
| Tactical ($11.75$ m)   | $25$        | $23/150$ ($15.3\%$)  | $0.17$           | $3.778 \pm 2.723$ | $10.771$        |
| Team ($23.0$ m)       | $0$         | $0/150$ ($0\%$)      | N/A              | N/A               | N/A             |


> **Remark (Team-level $H_1$ needs four centroids).** A Vietoris–Rips complex is a flag complex. On three or fewer points the triangle enters with the last edge, so no non-trivial $H_1$ class can survive. At $\delta = 23.0$ m, $k \le 2$ in 93.6% of the 436,648 complete frames, $k = 3$ in 6.4%, and $k = 4$ in 141 frames (0.032%). No frame has $k > 4$. Those 141 frames have $H_1 = 0$. The 1,500-frame sample contains one of them and also has no team-level loop. The headline $H_1$ analysis therefore runs at two levels (individual and tactical). Team-level loop structure on the typical two-centroid envelope would require a different representation (density fields or Delaunay triangulations, for example).

The two-level $H_1$ pattern extends to all ten matches ($1{,}500$ uniformly sampled frames; Table 2). Individual-level presence is $96.5 \pm 1.5\%$ ($95\%$ CI $95.6$–$97.3$), between $94.7\%$ and $98.7\%$ in every match. Tactical presence is $18.8 \pm 6.5\%$ ($95\%$ CI $15.2$–$22.7$), ranging from $11.3\%$ to $31.3\%$ across matches. The primary match ($15.3\%$ tactical) sits within one standard deviation of the ten-match mean. That match was chosen for broadcast quality and event annotation, not for its tactical $H_1$ rate. Conditional mean filtration lifetime on the ten-match sample is $1.886$ m at the individual level and $3.411$ m at the tactical level, the same ordering as Table 1.

**Table 2.** Multi-match $H_1$ statistics ($10$ matches). Presence = mean $\pm$ s.d. across matches; $95\%$ bootstrap CIs from $1{,}000$ resamples over matches. $\bar{p}$ is mean filtration lifetime over loops ($\sum p / \sum H_1$), not the per-frame average that includes zeros. The s.d. column is the standard deviation of the ten per-match conditional means.


| Level      | Total $H_1$ | Presence rate    | $95\%$ CI     | $\bar{p}$ (m) | s.d. |
| ---------- | ----------- | ---------------- | ------------- | ---------------- | ---------------- |
| Individual | $4{,}039$   | $96.5 \pm 1.5\%$ | $95.6$–$97.3$ | $1.886$          | $0.145$          |
| Tactical   | $306$       | $18.8 \pm 6.5\%$ | $15.2$–$22.7$ | $3.411$          | $0.419$          |
| Team       | $0$         | $0.0 \pm 0.0\%$  | N/A           | N/A              | N/A              |


The tactical level sits close to a group-count floor. In the ten-match sample, $40.6\%$ of frames have four or fewer tactical groups. None of those frames carries a loop.

Presence alone cannot separate arrangement from group count. The matched null of Section 2.6 holds $k$ fixed and draws points uniformly inside the observed convex hull (hull vertices are not kept), so only the arrangement is randomised.

Table 3 gives the comparison. Tactical presence is $18.8\%$, against a null rate of $9.1\%$, an excess of $+9.7$ percentage points. Table 4 splits the same comparison by group count. Presence is zero for $k \le 4$. It then rises from $9.3\%$ at $k = 5$ to $67.0\%$ at $k = 8$, and remains above the null at every such $k$.

At the individual level the null rate is already $91.4\%$. Twenty points in a bounded region almost always close a cycle, so the observed excess is modest ($+5.1$ percentage points).

**Table 3.** $H_1$ presence against a group-count- and hull-matched null ($10$ matches, $1{,}500$ frames, $200$ null replicates per frame). Excess is in percentage points, with $95\%$ bootstrap CIs over matches.


| Level      | Observed | Null   | Excess  | $95\%$ CI       |
| ---------- | -------- | ------ | ------- | --------------- |
| Individual | $96.5\%$ | $91.4\%$ | $+5.1$  | $[+3.9, +6.1]$  |
| Tactical   | $18.8\%$ | $9.1\%$  | $+9.7$ | $[+7.3, +12.2]$ |


**Table 4.** Tactical-level $H_1$ presence by group count $k$, against the matched null of Table 3 ($10$ matches, $1{,}500$ frames).


| $k$     | Frames | Observed | Null    | Excess  |
| ------- | ------ | -------- | ------- | ------- |
| $\le 4$ | $609$  | $0.0\%$  | $0.4\%$ | $-0.4$  |
| $5$     | $344$  | $9.3\%$  | $4.1\%$ | $+5.2$  |
| $6$     | $252$  | $26.6\%$ | $12.0\%$ | $+14.5$ |
| $7$     | $149$  | $51.0\%$ | $21.7\%$ | $+29.3$ |
| $8$     | $94$   | $67.0\%$ | $33.4\%$ | $+33.6$ |
| $\ge 9$ | $52$   | $84.6\%$ | $49.0\%$ | $+35.6$ |




### 3.3 Closed cycle structures

All 403 primary-match $H_1$ bars have a simple-cycle representative from the reduction in Section 2.5. The cycle is present at birth by construction: its longest edge is the birth value. The cycles have four to thirteen vertices, and 352 of the 403 have four, five, or six. Figure 3 shows sample frame 95 at both levels. The left column is the vertex set after clustering. The right column is the representative of largest $p$ on that set. At $\delta = 2.75$ m the cycle has eight vertices, seven of them singleton clusters and one a pair, and the edges run from $6.9$ to $15.6$ m ($p = 6.540$ m). At $\delta = 11.75$ m the cycle has six groups, one a 14-player single-linkage cluster, and the edges run from $14.6$ to $22.1$ m ($p = 9.942$ m). The two cycles are not the same bar: they use different vertices and are born at $15.6$ m and $22.1$ m. Figure 4 shows those bars on the persistence diagram, together with every finite $H_1$ bar on the primary match. The bars of largest $p$ in Table 1 are not used for the figure: the individual-level bar of largest $p$ (frame 141) is a near-collinear sliver.

> **Figure 3** (`figures/fig3_cycle_geometry.pdf`; not embedded in this Markdown copy). Cutoff versus filtration on one sample frame of SkillCorner match $1996435$ (sample frame 95). Left: vertex set after clustering at $\delta$. Gold markers belong to this row's cycle clusters; the hull in (c) is the 14-player single-linkage cluster; dashed circles have radius $\delta$ on the cycle vertices only. Right: $H_1$ representative of largest $p$ on those vertices ($p = 6.540$ m and $p = 9.942$ m). Cycle edges are filtration distances ($6.9$–$15.6$ m in (b); $14.6$–$22.1$ m in (d)). The longest edge is the birth value. Panel (d) draws centroids, not the absorbed players. These are the longest bars on frame 95, not the longest on the match; the cycles have eight vertices in (b) and six in (d). A 10 m scale bar is shown on each panel. Uniform sample, $n = 150$ frames, every 290th complete frame (same rule as the ten-match analysis).

> **Figure 4** (`figures/fig4_h1_diagrams.pdf`). Finite $H_1$ bars at two organisational levels on the primary match. **(a)** Individual and **(b)** tactical persistence diagrams for sample frame 95 (same frame as Figure 3); the marked pair is the bar of largest $p$ on that frame ($p = 6.540$ m and $p = 9.942$ m). **(c)** Every finite bar on the primary match, one track per organisational level (378 individual, 25 tactical). The dashed ticks are Table 1's $\bar{p}$: the mean of these bar lengths. The two levels are not superimposed: that would recreate the mixing of Section 1.2. The individual-level bar of largest $p$ in Table 1 (frame 141) is a near-collinear sliver and is not the cycle shown in Figure 3.



### 3.4 Sensitivity analysis

Detection is not confined to the adopted cutoff. Tactical $H_1$ counts fall monotonically as the cutoff widens. On the primary match's 150 frames, sweeping $\delta \in [6, 16]$ m gives $275$ loops ($87.3\%$ of frames) at $\delta = 6$ m and none at $\delta = 16$ m. The operative range is $[6, 14]$ m (Table 5). The adopted cutoff $\delta = 11.75$ m lies at the conservative end of that range ($15.3\%$ frame presence).

**Table 5.** Tactical-level cutoff sensitivity ($150$ frames, primary match).


| $\delta$ (m) | Total $H_1$ | Frame presence | Mean $H_0$ |
| ------------ | ----------- | -------------- | ---------- |
| $6$          | $275$       | $87.3\%$       | $13.4$     |
| $8$          | $162$       | $68.0\%$       | $9.8$      |
| $10$         | $78$        | $42.7\%$       | $7.0$      |
| $11.75$      | $25$        | $15.3\%$       | $5.0$      |
| $12$         | $21$        | $12.7\%$       | $4.8$      |
| $14$         | $5$         | $3.3\%$        | $3.5$      |
| $16$         | $0$         | $0.0\%$        | $2.8$      |


Finite bars are unchanged when the filtration is stopped at an upper quartile of the inter-centroid distances rather than at the diameter. At $\delta = 11.75$ m, every percentile from $P_{50}$ to $P_{95}$ yields the same $25$ loops and $15.3\%$ frame presence, even though mean $\varepsilon_{\max}$ spans $37.6$–$65.3$ m (Table 6). The reported filtration is the diameter.

**Table 6.** Filtration-percentile ablation, $\delta = 11.75$ m.


| Percentile | Total $H_1$ | Frame presence | Mean $\varepsilon_{\max}$ (m) |
| ---------- | ----------- | -------------- | ----------------------------- |
| $P_{50}$   | $25$        | $15.3\%$       | $37.6$                        |
| $P_{60}$   | $25$        | $15.3\%$       | $41.8$                        |
| $P_{75}$   | $25$        | $15.3\%$       | $49.6$                        |
| $P_{90}$   | $25$        | $15.3\%$       | $60.0$                        |
| $P_{95}$   | $25$        | $15.3\%$       | $65.3$                        |




### 3.5 Complementarity of the two $H_1$ levels

The two $H_1$ levels carry distinct rather than redundant information. Over $1{,}500$ uniformly sampled frames, total individual and tactical $H_1$ persistence correlate weakly (Spearman $\rho = 0.234$, $p < 0.001$; $95\%$ bootstrap CI $[0.181, 0.276]$). The same holds for loop counts ($\rho = 0.205$, $p < 0.001$). The finding does not depend on whether the comparison uses total persistence or loop counts.

Co-occurrence exceeds chance (Fisher odds ratio $6.12$, $p = 0.002$; bootstrap CI $[2.32, 16.33]$). Table 7 shows the asymmetry: $1{,}167$ frames carry individual loops without a tactical partner, and only two frames do the reverse. Weak rank correlation remains the main evidence for complementarity. Joint presence need not mean the two levels measure the same structure.

**Table 7.** Frame counts of $H_1$ presence at the two levels ($1{,}500$ frames).


|                          | Tactical $H_1$ present | Tactical $H_1$ absent |
| ------------------------ | ---------------------- | --------------------- |
| Individual $H_1$ present | $280$                  | $1{,}167$             |
| Individual $H_1$ absent  | $2$                    | $51$                  |


Bottleneck distance between the two levels' diagrams has median $1.456$ m and $95$th-percentile tail $3.556$ m. That is on the order of typical tactical filtration lifetime on the primary match ($3.778$ m mean bar length where loops appear; Table 1). Landscape $L^2$ distance has median $5.477$. The levels differ by roughly as much as their features are large, not by a small perturbation of one shared pattern.

### 3.6 Event correlation

Addressing question Q4, total persistence moves with on-ball events. The comparison is a construct-validity check against measurement noise. It uses $103{,}856$ SkillCorner event–topology pairs from the ten matches.

For each event, $\Delta$ is the change in mean total persistence from the five $1$ Hz frames before the event to the five after it (Section 2.6). At the individual level, an on-ball engagement is followed by a drop. The mean change is $\Delta=-0.253$ m ($n=8{,}927$, Wilcoxon signed-rank $p<10^{-13}$). Build-up is followed by a rise. The mean change is $\Delta=+0.700$ m ($n=618$, Wilcoxon signed-rank $p<10^{-7}$). At the tactical level the mean changes are $\Delta=-0.056$ m for engagement ($n=8{,}927$, of which $3{,}738$ are exact zeros; Wilcoxon signed-rank $p=0.013$ on the remainder) and $\Delta=+0.339$ m for build-up ($n=618$, of which $153$ are exact zeros; $p<10^{-5}$).

The event classes were specified in advance, and the $p$-values are nominal. Multiple-testing control and a football reading of these shifts belong to a companion manuscript.

---



## 4. Discussion



### 4.1 Recovered organisational levels

The three $H_0$ regimes (individual, tactical, and team) are the named group-count targets of Section 2.3, read from the pooled group-count curve on every complete frame of the ten matches (Figure 2). Those regimes remain over a range of $\delta$ rather than appearing only at the adopted cutoffs. The metre values are specific to this corpus. Another domain still requires the interaction lengths to be re-derived.

The tactical distance is the point on that curve where the mean group count lies nearest five, and where frames with at least four groups are still common (Figure 2c). On the 1 Hz diagnostic subset, the silhouette score has one interior local maximum, at $7.0$ m. That distance is a small-group alternative. Once frames that have collapsed to a single group are omitted, the score rises again through the two-envelope regime (Supplementary Figure S2). We record that curve and keep the group-count cutoff.

### 4.2 Two $H_1$ regimes

Scale-attributable homology detects loops at two of the three recovered levels. Individual-level loops are frequent; tactical-level loops are rarer and have longer filtration lifetime (Tables 1–2; Figure 4). Filtration lifetime is the bar length (death minus birth, in metres). It is not how long a loop lasts on the clock. The 150-frame subsample does not resolve formation or dispersion of loops between samples (Section 2.1).

On the primary match, every finite $H_1$ bar has a simple-cycle representative, present at birth by construction (Figure 3). Detection is not confined to the adopted cutoff (Section 3.4). Tactical $H_1$ is detected on the band $[6, 14]$ m, not only at an isolated optimum.

The pipeline therefore reports three $H_0$ regimes and two $H_1$ regimes. A team-level loop needs four centroids. Four centroids occur in 141 of 436,648 frames, and none of those frames has a loop (see the team-level Remark in Section 3.2). Recovering team-level loop structure on the typical two-centroid envelope would require a different representation, such as spatial density fields or Delaunay triangulations. Linkage choice changes tactical $H_1$ counts by nearly an order of magnitude; that caveat is taken up in Section 4.5.

### 4.3 Distinct structure at two levels

The two $H_1$ levels carry distinct rather than redundant information (Section 3.5): Spearman $\rho=0.234$ on total persistence, one-sided co-occurrence (Table 7), and bottleneck distance on the order of the tactical mean bar. These statistics do not test whether the tactical diagram is a coarsening of the individual diagram.

### 4.4 Construct validity

Total persistence moves with on-ball events (Section 3.6). At the individual level, an engagement is followed by a mean drop of $0.253$ m, and build-up by a mean rise of $0.700$ m. At the tactical level, both classes move in the same directions as at the individual level. That movement is the construct-validity check against measurement noise. Multiple-testing control and a football reading of the shifts belong to a companion manuscript.

### 4.5 Limitations

Linkage selection is a substantive methodological choice. Across a $600$-frame, four-match comparison sample, single linkage detects $106$ tactical-level $H_1$ loops. Complete linkage detects $802$. Ward's method detects $822$. That is a difference of almost an order of magnitude. The gap is large enough to change which scientific picture the data support, not merely the precision of one estimate. We retain single linkage because its definition is the most direct reading of spatial proximity. Its tendency to chain is a likely source of the gap with complete linkage and Ward's method; resolving that gap is left open.

A more principled selection criterion would come from the dynamical system itself, rather than from clustering-quality metrics alone. One candidate is the linkage under which a governing equation for a persistence functional admits the sparsest representation, in the sense of sparse identification of nonlinear dynamics. The functional would be the landscape $L^2$ norm or the tactical $H_1$ total-persistence sequence. Operationalising this would require three things. First, choose the dynamical state. Second, defend the sparsity of the recovered library against the Akaike information criterion (AIC), the Bayesian information criterion (BIC), or cross-validation baselines. Third, confirm that the resulting persistence sequence is genuinely lower-dimensional under the selected linkage. We defer this to the forthcoming full-season work. A population-sized sample of match sequences is what makes the sparsity comparison meaningful.

A landscape-path stability criterion (minimise variation of the persistence landscape under small perturbations of $\delta$) remains a future estimator of the tactical cutoff. It is computable with the landscape infrastructure of Section 3.5. We defer it to the persistence-landscape companion work. Section 3.4 reports the $[6, 14]$ m tactical $H_1$ band as an empirical property around the adopted $11.75$ m.

All data analysed here are broadcast-derived tracking at $10$ Hz. Broadcast tracking typically offers lower spatial precision than higher-frequency optical systems. That may affect the magnitude of filtration lifetimes reported. The structural findings (the three $H_0$ regimes, the $H_1$ presence rates, and the sensitivity profiles) depend on relative rather than absolute spatial precision. We expect, but have not tested, that they are robust across tracking technologies. A direct comparison of filtration lifetimes against optical tracking data remains for future work.

### 4.6 Outlook

Two extensions are in progress. The ten-match evidence base is being scaled to a full season of Championship matches. That sample will characterise population-level distributions of $H_0$ and $H_1$ counts, filtration lifetimes, and landscape norms, and will test whether matches carry a stable tactical signature at population scale. It is also the setting in which the linkage criterion proposed above becomes evaluable. Recovering a sparse governing equation for a persistence functional requires the population-sized sample of match sequences that a single season provides. Separately, persistence landscape dynamics are being developed to treat each match as a path through landscape space. That is the setting in which the landscape-stability cutoff criterion can itself be evaluated. Its resampling unit is the match-level landscape, not the per-frame summary used here.


---



## 5. Conclusion

By construction, each diagram is computed on the centroids of one organisational level. On this corpus the named group-count targets are met at 2.75 m, 11.75 m, and 23.0 m, and all ten match means lie in the acceptance bands. On the primary match, every finite $H_1$ bar has a simple-cycle representative, present at birth by construction. Tactical loops exceed the group-count-matched null of Section 2.6 by 9.7 percentage points (Section 3.2). The two loop-bearing levels are associated at Spearman $\rho=0.234$, co-occur one-sidedly, and have bottleneck distance on the order of the tactical mean bar (Section 3.5). Football was the measurement setting. Applying the pipeline to another bounded competitive system requires re-deriving the interaction lengths, which is not tested here.

---



## Declarations



### Competing Interests

The authors have no competing interests to declare.

### Acknowledgements

The authors thank SkillCorner for use of the open broadcast tracking dataset.

### Funding

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors; it was conceived and conducted independently by the authors.

### Data Availability Statement

Positional tracking data were provided by SkillCorner under an open-data licence ([https://github.com/SkillCorner/opendata](https://github.com/SkillCorner/opendata)). Analysis code, pipeline configuration, pinned `requirements.txt`, and the result files used for the figures and tables in this paper are included with the manuscript materials and will be released in a dedicated public repository at arXiv posting, deposited in the Swansea University Zenodo community.

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

The cutoffs are read from the group-count curve, not from a quality score. For completeness, Supplementary Figure S2 (`figures/figS2_cutoff_diagnostics.pdf`) records the Calinski--Harabasz index, mean silhouette, and information-content on the 1 Hz subset (each min-max scaled). Silhouette is undefined at $k=1$ and those frames are omitted, not coded as 0. The silhouette rise at large $\delta$ is an artefact of the shrinking $k \ge 2$ subsample; the only interior local maximum is at $7.0$ m, a small-group alternative we report but do not adopt. None of these curves selects the adopted cutoffs. Generate with `pipeline/steps/10_cutoff_sweep_figure.py`.

### Temporal autocorrelation

Headline tables use the uniform 150-frame rule of Section 2.1. Supplementary Figure S1 (`figures/figS1_acf.pdf`) is a diagnostic on the primary match at 1 Hz; it does not choose the stride. Generate with `pipeline/steps/09_acf_supplement.py`.