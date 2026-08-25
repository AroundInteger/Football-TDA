# Foundation

**Statistical topology of competitive collective systems.** EPSRC Mathematical Sciences Small Grant, Swansea University.

**Status: normative.** Where this file disagrees with any other document in the repository, this file wins and the other document is corrected. Written 24 August 2026. UK English throughout.

This document exists because the project's knowledge was spread across five partial foundations that had drifted apart. It replaces none of them; it governs them. Its test is operational: if we are funded, an incoming Research Associate should be able to read this file alone and know what to do in week one, and why.

**The rule that shapes every table below.** Each entry carries three fields: *what it is*, *why it is that way*, and *what it obliges someone to do*. An entry that cannot fill the third field is background reading, and belongs in a citation rather than a row.

**Citation convention.** Author–year throughout, because the compiled `[n]` numbering churns with every revision and a stale number here would propagate. The prior-art ledger (§3) carries the current Vision and Approach number in its own column, and is the sync source for that numbering.

**Path convention.** Paths beginning `grant/` are relative to this directory. Pipeline paths are shortened from these two roots:

- `PAPERS/` = `08_current/Paper Updated/3-Paper Paradigm/`
- `ANALYSIS/` = `03_football_analysis/` (repository root)

---

## 0. Precedence and scope

| Rank | File | Governs |
|---|---|---|
| 1 | **This file** | Object definition, parameters, tiers, rulings |
| 2 | `CANONICAL_NUMBERS.md` | Headline statistics, subordinate to §2 and §4 here |
| 3 | `live/02_Vision_and_Approach_REV3.md` | Submitted narrative |
| 4 | `live/T1_T2_Six_Registers.md` | Audience-specific wording of T1 and T2 |
| 5 | `live/REVISION_DISCIPLINE.md` | Revision process |
| 6 | `evidence/toy_models/AdversarialTDA_Specification.md` | The synthetic system |
| 7 | `../Paper Updated/3-Paper Paradigm/working_foundations.md` | Publication strategy |

Rank 7 has a specific hazard: its grant-alignment table was checked on 23 June 2026 and predates the 6 July pipeline recompute. Two of its instructions are wrong and are overturned in §9.

---

## 1. The object of study

### 1.1 Definition

Fix a compact convex domain $\Omega \subset \mathbb{R}^2$ with diameter $D_\Omega = \operatorname{diam}(\Omega)$. (Diameter is $D_\Omega$ throughout; $D_\delta(t)$ is always a persistence diagram.) A **competitive collective system** on $\Omega$ is a pair of finite agent sets

$$A(t) = \{a_1(t),\dots,a_{N_A}(t)\} \subset \Omega, \qquad B(t) = \{b_1(t),\dots,b_{N_B}(t)\} \subset \Omega,$$

observed at a fixed rate $f$, in which each agent's motion depends on the current configuration of *both* sets. Write $P(t) = A(t) \cup B(t)$ for the merged cloud and $N = N_A + N_B$.

Three properties define the class, and each one is load-bearing.

**Boundedness.** $\Omega$ is compact. This is not a modelling convenience: with $N$ fixed, compactness bounds the cardinality and the total persistence of every diagram, which is what supplies the integrability hypothesis in T1 and makes the stability constant in T2 explicit in $N$ and $D_\Omega$. Remove boundedness and both theorems lose their hypotheses.

**Binary adversarial coupling.** Exactly two sets, mutually responsive. This is what makes successive observations non-exchangeable, and non-exchangeability is the gap the project exists to close. A single collective, or two co-located but non-interacting populations, is a different and much better-served problem.

**Multi-scale organisation.** Structure exists simultaneously at several characteristic interaction lengths. This is what makes a single filtration over the full agent set insufficient, and it is an empirical property of a given system, not an axiom. Whether a new system has it is a question, not an assumption; see the O1 gate in §2.3.

### 1.2 The derived chain

Every quantity in this project is one of five objects, produced in this order. The chain is fixed; disputes about a number are disputes about a stage of it.

| Stage | Object | Produced by |
|---|---|---|
| 1 | Point cloud $P(t) \subset \Omega$ | Tracking, complete-coverage frames only |
| 2 | Reduced cloud $\tilde P_\delta(t)$ | Single-linkage clustering at interaction length $\delta$, then centroids |
| 3 | Diagram $D_\delta(t)$ | Vietoris–Rips persistent homology on $\tilde P_\delta(t)$, adaptive $\varepsilon_{\max}$ |
| 4 | Landscape $\lambda_\delta(t) \in L^2$ | Bubenik transform of $D_\delta(t)$ |
| 5 | Inference | Mean path, long-run covariance, functional CUSUM |

Formally, for cutoff $\delta > 0$ single-linkage clustering partitions $P(t)$ into $C_1,\dots,C_k$ such that any two points in a cluster are joined by a chain of pairwise distances at most $\delta$, and

$$\tilde P_\delta(t) = \Bigl\{ \bar c_j = \tfrac{1}{|C_j|}\textstyle\sum_{p \in C_j} p \;:\; j = 1,\dots,k \Bigr\}.$$

Homology is computed on $\tilde P_\delta(t)$, never on $P(t)$. That substitution *is* the scale decomposition, and it is the reason a Betti number at a single filtration value does not determine the diagram.

### 1.3 What is defined but out of scope

A **role variable** $b(t) \in \{0,1\}$ inverts which set is pressing and which is evading. In football it is ball possession. It is defined here so that the Standard Grant architecture (§7) has a referent, and so that nobody reintroduces it into Small Grant text by accident.

*Action.* Do not use $b(t)$ in any Small Grant deliverable. T1 and T2 are stated for the merged cloud without role conditioning. Bilateral decomposition by team identity is Paper B's object, not this grant's.

---

## 2. Parameter register

Status codes: **M** measured from data; **C** chosen by convention with a stated reason; **G** gated, i.e. re-derived and tested during the grant; **S** synthetic only; **X** defined but out of scope.

### 2.1 System and sampling

| Parameter | Value | Status | Why | Action it obliges |
|---|---|---|---|---|
| Domain $\Omega$ | **Unresolved.** Paper A says only "a standard pitch model"; the toy uses $120 \times 80$ | M / S | Bounded domain is a hypothesis of T1 and T2, and $D_\Omega$ enters T2's constant $C$ explicitly | Fix the pitch model from SkillCorner metadata and record $D_\Omega$ here. Until then no numerical value of $C$ can be quoted. See ruling R11 |
| $N_A = N_B$ | 11 per side, $N = 22$ | M | Complete-coverage frames only | Discard frames with fewer than 22 tracked players before any computation |
| Pilot rate $f$ | 10 Hz (SkillCorner) | M | Source resolution of the validated pilot | Cutoffs in §2.2 are 10 Hz-derived; they are not automatically valid at other rates |
| Production rate $f$ | 1 Hz | C | Frame-level homology runs in under 2 s and is embarrassingly parallel, so 1 Hz is affordable at season scale | The Month-2 gate must confirm 1 Hz preserves features validated at 10 Hz. This check is not optional; it is the answer to the downsampling objection |
| Pilot subsampling | Every 290th complete frame, 150 per match | C | Gives 1,500 frames across 10 matches with even temporal coverage | Reproduce with this exact stride or the pilot numbers will not match |

### 2.2 Interaction lengths

The single most error-prone table in the project. Read the last row before using any value.

| Scale | Adopted $\delta$ | Status | Why this value | Action |
|---|---|---|---|---|
| Individual | **2.98 m** | M | Carried over from an earlier normalised-coverage calibration; retained because the sweep validates the individual $H_0$ band ($15$–$22$ clusters) at this value. Cross-epoch stability **0.875** at 2.98 m. The Calinski–Harabasz optimum is **1.39 m** (stability 0.956); not adopted | Use 2.98 m; quote stability 0.875, not 0.956 |
| Tactical | **12.0 m** | M / C | The automated metrics *disagree* here: silhouette optimum 16.31 m, information-content optimum 6.87 m. 12.0 m is a domain-informed choice within that range, being half the width of a standard pitch zone | Present as a judgement call with both metric optima named. Presenting it as a metric output is the single easiest way to lose a methods referee |
| Team | **30.0 m** | M | Selected directly by the automated metrics | Use 30.0 m |
| Sweep design | 100 points over $[0.5, 30.0]$ m, against 58 temporal windows balanced across epoch lengths of 1, 2, 5 and 10 minutes | M | Defines what "cross-epoch" means in the stability score | Any re-derivation must reuse this design or state its departure |
| Operative range, tactical $H_1$ | $[6, 14]$ m | M | $H_1$ frame presence falls from 87.3% at 6 m to 3.3% at 14 m and 0% at 16 m | The robustness claim is that detection survives across this band, not that 12.0 m is optimal |
| Filtration percentile | $P_{75}$ | C | $P_{50}$ through $P_{95}$ return *identical* $H_1$ totals and presence rates | State as a reporting convention, never as an optimisation |
| **Do not use: 1.39 m** | — | — | `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` and `numbers.json` record `optimal_cutoff_m = 1.39` for the individual scale with `selection_method = "CH optimum"`. This is the raw Calinski–Harabasz optimum, not the adopted value | **Cluster at 2.98 m.** An RA reading the pipeline outputs unaided will otherwise use 1.39 m and reproduce nothing. See ruling R4 in §9 |

### 2.3 Gates and thresholds

Every gate here is a point at which the project can be told it is wrong. That is their purpose.

| Gate | Threshold | When | Why this threshold | Action on failure |
|---|---|---|---|---|
| Cutoff stability | $\geq 0.80$ | Month 2 | At the **adopted** cutoffs, cross-epoch stability is 0.875 / 0.836 / 1.000 (individual / tactical / team). The 0.80 floor sits below the weakest adopted scale with margin | Re-derive interaction lengths on Championship data before O2 begins |
| Dependence diagnostic | Autocovariance decay consistent with summable mixing | Month 9 | T1 and T2 assume $\alpha$-mixing with summable coefficients. This checks the assumption rather than asserting it | Consistency is not proof. The label is "diagnostic"; do not upgrade it to "verified" |
| Eigengap | Recorded, not thresholded | Month 9 | The projected (FPCA-score) form of T2 needs Davis–Kahan; the landscape-series form does not | State T2 on the landscape series. Report the eigengap alongside for the projected form |
| Discriminability | $\geq 3$ organisational states separated, $p < 0.05$ BH-corrected | Month 9 | Benchmarked against team length, width and convex-hull area | Below this, the comparison geometry does not support fingerprinting |
| Change-point recovery | $\geq 70\%$ of held-out annotated transitions within $\pm 10$ s, at a calibrated 5% false-alarm rate, permutation $p < 0.05$ | Month 9 | A tolerance window is required or the criterion is not checkable | Fall back to diagram-valued Wasserstein comparison (risk R3) |

### 2.4 Season design

| Quantity | Value | Why | Action |
|---|---|---|---|
| Fixtures | 552 in a Championship season, $\approx 540$ after pre-registered exclusions | $24 \times 46 / 2 = 552$; a reviewer will do this arithmetic | Tie the reduction to the OSF exclusion criteria, never leave $\approx 540$ unexplained |
| Unit of analysis | **The fixture**, represented by one focal team, opponent as covariate | The two teams in a fixture are maximally dependent. Counting them separately is precisely the error §1 accuses the field of making | State the unit explicitly in any power claim |
| Stratification | Venue $\times$ opponent strength $=$ 6 cells, $\approx 90$ matches each | Phase of play is a *within*-match factor and cannot partition matches | Never include phase of play in the crossing; it enters as repeated measures |
| Precision target | 32 matches per cell gives 95% CI half-width 0.025 at pilot s.d. 0.072 | $1.96 \times 0.072/\sqrt{32} = 0.0249$ | Smallest cell (~90) clears this comfortably |
| Formation power | 180 per class detects Cohen's $d \geq 0.30$ at 80% power, $\alpha = 0.05$, BH-FDR | $540/180 = 3$ balanced classes exactly | Scope to the three most common formations as a pre-registered comparison set |
| Replication target | Stratified permutation $p = 0.051$ | A borderline within-match pilot effect is the thing season scale is meant to resolve | Cite as motivation for replication, never as a positive finding |

### 2.5 Compute and software

| Item | Value | Action |
|---|---|---|
| Frame-level homology | Under 2 s, embarrassingly parallel | This is what licenses 1 Hz; do not delete the timing when compressing text |
| Allocation | $\approx 1{,}600$ of 5{,}000 CPU-hours, Supercomputing Wales | Report both numbers; the headroom is the feasibility argument |
| Stack | Python 3.11, Ripser.py 0.6.12, GUDHI 3.11.0, giotto-tda 0.6.0, NumPy 2.0.2, SciPy 1.13.1, pandas 2.3.2, scikit-learn 1.6.1 | Pin exactly. Diagrams were cross-checked across all three TDA libraries to $10^{-6}$ m |
| Adaptive filtration | $\varepsilon_{\max} = \max\bigl(P_{75}\{d(\bar c_i, \bar c_j)\},\ \max(5.0,\, 2\delta)\bigr)$ | Inter-centroid distances exceed $\delta$, so a fixed $\varepsilon_{\max}$ fails across scales. The floor prevents degenerate filtration at small $\delta$ |

---

## 3. Prior art ledger

The novelty argument is not "nobody has done TDA on football". It is that each ingredient exists under an assumption this class of system violates. The *assumes* column is where the grant lives.

| Work | V&A [n] | Establishes | Assumes | Does not cover | Action |
|---|---|---|---|---|---|
| Carlsson (2009); Zomorodian & Carlsson (2005) | 1, 2 | Persistent homology and its computation | — | Nothing about which agents enter the filtration | Cite as foundation only |
| Edelsbrunner & Harer (2010) | 3 | Computational topology text | — | Scale attribution across organisational levels | Cite for the single-filtration limitation, phrased as "a single filtration over the full agent set" |
| Cohen-Steiner et al. (2007); (2010) | 11, 14 | Bottleneck stability; $L^p$-stable persistence under bounded total persistence | Bounded total persistence for the $L^p$ case | The propagation of that stability into a sequential statistic | Supplies T2's input-perturbation link and the total-persistence hypothesis |
| Bubenik (2015) | 8 | Persistence landscapes; values in $L^2$ | — | Dependent sampling | The reason we work in a Hilbert space at all |
| Chazal et al. (2014) | 7 | Stochastic convergence of landscapes and silhouettes | **Independent sampling** | Weakly dependent trajectories | **The single most important row.** T1 exists to remove this assumption |
| Turner et al. (2014) | 27 | Fréchet means for diagram distributions | — | Uniqueness | Non-uniqueness for diagram-valued means is *why* the grant is landscape-valued. Cite whenever the choice is questioned |
| Adams et al. (2017) | 19 | Persistence images | — | Sequential inference | Alternative vectorisation; not the grant's statistic |
| Botnan & Lesnick (2022); Lesnick (2015) | 4, 5 | Multiparameter persistence | — | Tractability at these data rates | Say "impractical at the data rates required here", not "intractable". An author of these papers would contest the stronger word |
| Schenck (2022) | 6 | Algebraic foundations of applied TDA; Chapter 8 on multiparameter persistent homology | — | Tractability at these data rates | Textbook companion to [4,5]. Cite the book generally; name Chapter 8 when the claim is the algebraic setting of multiparameter persistence |
| Bosq (2000); Hörmann & Kokoszka (2010) | 9, 10 | Linear processes and weak dependence in function spaces | Stationarity, mixing | Topological inputs | Supplies the long-run covariance machinery T1 imports |
| Berkes et al. (2009); Page (1954) | 13, 12 | Functional CUSUM; sequential change detection | Known or estimable covariance | Topologically derived inputs measured with error | T2 chains stability into this |
| Gu et al. (2022) | 18 | Change-point detection in multi-agent systems from higher-order features | **Single scale** | Multi-scale competitive systems | The nearest prior art for O2. Name the single-scale restriction explicitly |
| Schindler & Barahona (2023) | 20 | Multiscale clusterings analysed with persistent homology | Cooperative or slowly evolving systems | Adversarial coupling; sequential inference | **The sharpest incremental-novelty risk.** Differentiate on the *statistical* contribution (dependence, sequential guarantees), not on cluster-then-PH, which has precedent here |
| Topaz et al. (2015); Bhaskar et al. (2019); Ballerini et al. (2008) | 15, 16, 17 | Topology of biological aggregation, collective motion, flocking | Single cooperative collective | Two mutually responsive populations | Motivates interaction-length framing; does not pre-empt it |
| Folgado et al. (2014); Fernández & Bornn (2018) | 21, 22 | Geometric team descriptors; pitch control | — | Loop structure, scale separation | The benchmark O1 must beat. Without these the claim "unavailable from conventional geometry" has no support |
| Ramsay & Silverman (2005) | 28 | Functional data analysis, FPCA | Fixed basis for score-space Lipschitz claims | — | Expand "FPCA" on first use; panels include non-FDA mathematicians |
| Bauer (2021); Maria et al. (2014); Tauzin et al. (2021) | 24, 25, 26 | Ripser, GUDHI, giotto-tda | — | — | Software citation |
| Carlsson & Mémoli (2010) | — | MST $\leftrightarrow$ Vietoris–Rips $H_0$; dendrogram correspondence | Finite metric space | That every bounded competitive system *is* a hierarchy | Used exactly in the toy model. Does **not** license the claim that four domains share a barcode |
| MacPherson & Schweinhart (2012) | — | $H_1$ from embedding geometry | — | — | The theoretical home for encirclement loops, distinct from hierarchy-generated $H_1$ |
| Vipond et al. (2021) | — | Multiparameter persistence for tumour–immune spatial patterns | Static imaging | Serial paired clouds | Oncology is *crowded* for static TDA. The open gap is longitudinal, which is Standard Grant |
| Gidea & Katz (2017) | — | TDA change detection in financial time series | Contrived spatial domain | — | Finance is deprioritised: densest prior art, no Co-I, weakest bounded domain |
| Bhattacharya et al. (2016) | — | TDA of a single robot swarm | One swarm | Adversarial two-swarm | Robotics transfer is open |
| Nguyen, Du & Yin (2014) | — | Stationary distributions for competitive Kolmogorov systems under telegraph noise | **Stochastic** switching | Deterministic role inversion | Standard Grant only. The stochastic-to-deterministic gap is real; do not import the guarantee |

---

## 4. Our own work

### 4.1 Outputs and their status

| Output | Status | Claims | Does **not** license |
|---|---|---|---|
| **Paper A** — multi-scale PH for competitive spatial systems | Submitted, *J. Applied and Computational Topology* | Cluster-then-adaptive-filtration; three $H_0$ regimes and two $H_1$ regimes across 10 matches; scales carry distinct information; every $H_1$ generator recoverable as a geometric cycle | Any statistical guarantee under dependence. Event correlation is construct validity only |
| **Paper B** — topological signatures of tactical organisation | In preparation, *J. Sports Sciences* | Persistence tracks events; non-redundancy with geometric descriptors; home/away near-independence; predictive null | Anything in the grant. Paper B is deliberately absent from the V&A |
| **Paper C** — methods note | After A and B submit | Diagram $W_1/W_2$ analogues on synthetic ecology and robotics generators; three-tier claim split | Landscape T1 or T2. Never quote ecology $\hat T$ as T2 in JeS |
| **Toy model** | Internal, 10 figures | Mechanism illustration under known ground truth | Any results section. See the prohibition in §4.3 |

### 4.2 The pilot, exactly

Ten A-League matches, SkillCorner open broadcast tracking. Primary match 1996435 (Sydney FC v Adelaide United), 43,531 complete-coverage frames at 10 Hz, subsampled to 150.

**$H_0$ regimes, ten matches (grand means).** Individual $19.05$, tactical $4.92$, team $1.38$.

**$H_0$, primary match.** Individual $19.02 \pm 2.47$, tactical $4.77 \pm 1.60$.

**$H_1$, primary match** (403 loops total):

| Scale | Loops | Frames with loops | Mean persistence (m) | Max (m) |
|---|---|---|---|---|
| Individual (2.98 m) | 382 | 143/150 = **95.3%** | $1.977 \pm 1.128$ | 12.991 |
| Tactical (12.0 m) | 21 | 19/150 = **12.7%** | $3.797 \pm 3.008$ | 10.771 |
| Team (30.0 m) | 0 | 0/150 = 0% | — | — |

**$H_1$, ten matches** (4,515 loops total): individual presence $97.0\% \pm 1.5\%$ (bootstrap CI $[96.1, 97.9]$, 4,200 loops); tactical presence $19.3\% \pm 7.2\%$ (CI $[15.3, 23.7]$, 315 loops); team presence 0% across all 1,500 frames.

**Team-scale $H_1$ is zero a priori, not empirically.** Clustering at 30.0 m leaves at most two centroids, and $H_1$ of one or two points is trivially empty. This is a structural remark, and it is a small genuine piece of mathematics worth leaning on as evidence of rigour. Do not report it as a finding about football.

**Scale complementarity.** Spearman $\rho = 0.264$ on **total $H_1$ persistence** over 1,500 frames, $p = 2.4 \times 10^{-25}$; the same test on loop counts gives $0.211$ (ruling R13, and never quote either without naming which). Match-resampled bootstrap (1,000 draws, seed 42) gives median 0.262, CI $[0.200, 0.314]$, for the total-persistence statistic. Fisher exact odds ratio 10.91, $p = 9.4 \times 10^{-4}$, contingency $[[289, 1166], [1, 44]]$, computed on binary $H_1$ presence. Bottleneck distance between scales has median 1.511 m with a 95th-percentile tail of 7.994 m; landscape $L^2$ distance has median 5.671.

**Cross-epoch stability (at adopted cutoffs).** Individual **0.875** at 2.98 m, tactical 0.836 at 12.0 m, team 1.000 at 30.0 m; validation rate 1.000 at all three scales. The Calinski–Harabasz optimum for individual is 1.39 m (stability 0.956); not adopted. See ruling R12.

**Event–topology pairs.** 104,722 across ten matches.

**Within-match effect.** Stratified permutation $p = 0.051$; pilot half-level random-effects $\hat\beta_1 = -0.081$, $p = 0.079$. Borderline. Motivates replication; is not a result.

### 4.3 The toy model, and its boundary

The toy computes honest objects: $H_0$ via the MST (exact for finite metric spaces), exact $W_p$ by optimal transport with diagonal matching, the $W_2$ Fréchet mean, and a Monte-Carlo-calibrated Page CUSUM. Domain $[0,120] \times [0,80]$, diameter 144.22, $N = 12$ per side.

Reference values: $W_1(\text{A\_WIDE}, \text{A\_NARROW}) = 76.13$ by exact optimal transport, against 87.15 for naive sorted matching. CUSUM at 5% calibrated false-alarm rate gives $\hat T = 54$ against $T^* = 50$. Encirclement $H_1$ bar $[27.24, 40.00]$, persistence 12.76, destroyed when an opposing cluster penetrates the ring.

**Prohibitions.**

1. No toy number enters a results section of any paper, or the grant. Not 12.66, not 76.13, not $\hat T = 54$.
2. The toy's display scales $\delta \in \{4.5, 40, 66\}$ are **not** interaction lengths and bear no relation to 2.98 / 12.0 / 30.0 m.
3. Figure 5 shows four domains sharing a barcode *because the same cluster template was copied into each*. It is a schematic of a transfer hypothesis. It is not a transfer test, and calling it theorem-level would not survive a methods referee.
4. The historical order is football first, toy afterwards. Never write the project as though the synthetic work preceded the ten-match study.
5. The toy computes **diagram** $W_1/W_2$; the grant theorems are **landscape**-valued. The toy is evidence for the R3 fallback, which is what it actually is.

---

## 5. What we investigate, and why it matters

**The question.** Given two mutually responsive agent sets in a bounded domain, observed as a single dependent trajectory rather than as independent samples: can we average their topological summaries in a well-posed way, and can we locate the moments at which their organisation changes, with proven error control?

**Why it is currently unanswerable.** Two obstacles, and each maps to one theorem.

*Scale.* Organisation exists at several interaction lengths simultaneously. Persistent homology is multi-scale in its filtration parameter, but a single filtration over the full agent set does not separate organisational levels: features from different levels interleave in one diagram and cannot be attributed to a level. Multiparameter persistence is the principled alternative and is impractical at these data rates. Our answer is to decompose by validated interaction length *before* computing homology, which is what makes the summaries scale-attributable.

*Dependence.* Each agent adapts continuously to its opponents, so observations are neither independent nor exchangeable. Existing statistical topology assumes otherwise, and inference built on that assumption understates uncertainty.

**T1 — averaging under competitive dependence is well posed.** On a bounded domain with fixed $N$, diagrams have bounded cardinality and bounded persistence, so landscapes are uniformly bounded in the separable Hilbert space $L^2$. The mean is then the Bochner expectation, unique by strict convexity. *That much is routine, and we say so.* The theorem is the limit law: for a strictly stationary $\alpha$-mixing landscape series with summable coefficients, the empirical mean path is $\sqrt{n}$-consistent with a Gaussian limit whose covariance is the **long-run** covariance $\Sigma_{\mathrm{LR}} = \sum_k \operatorname{Cov}(\lambda_0, \lambda_k)$, not the marginal one.

Why it matters operationally: competitive dependence does not move the mean, it changes every variance built on it. That is what makes a block bootstrap the correct calibration rather than a heuristic, and it is what invalidates the naive inference currently standard in this literature.

**T2 — transitions are localised with a proven error bound.** The landscape map is 1-Lipschitz from diagrams under the bottleneck distance into the sup-norm. Boundedness converts this to an $L^2$ bound with constant $C$ explicit in $N$ and $D_\Omega$. For a functional CUSUM on the landscape series,

$$|\hat\tau - \tau| = O_P\Bigl( \sigma^2 / (\Delta - 2C\varepsilon)^2 \Bigr), \qquad \Delta > 2C\varepsilon,$$

with $\Delta$ the jump in the mean landscape, $\sigma^2$ the long-run variance from T1, and $\varepsilon$ the worst-case input perturbation.

The **identifiability threshold $\Delta > 2C\varepsilon$ is the substantive content**: a transition is locatable only once it exceeds twice the measurement-induced perturbation. The rate itself is standard once the constant is explicit. Two distinct operational quantities follow, and conflating them is a known past error: block-bootstrap calibration sets the *detection threshold* controlling false alarms, while the bound sets the *localisation window* reported with each detection.

**Why football.** It is the only setting supplying a full population of adversarially coupled trajectories, continuously tracked within strict boundaries, with expert labels for verification. It is the falsification platform, not the contribution. The framework transfers to any bounded competitive system *once interaction lengths are re-derived* — that qualifier travels with the claim, always.

---

## 6. The rigour contract

Every claim the project makes sits in exactly one tier. The tier determines the language permitted.

| Tier | Meaning | Permitted verbs | Examples |
|---|---|---|---|
| **1. Cited** | Established in the literature, used as-is | "follows from", "by" | Bottleneck stability; MST–$H_0$ correspondence; Page CUSUM; landscapes in $L^2$ |
| **2. Proved here** | Proved under stated hypotheses within the grant | "we prove", "under (H)" | T1 limit law; T2 localisation bound; the team-null remark |
| **3. Gated** | An empirical condition tested at a declared checkpoint | "we test whether", "gated at" | Cutoff stability $\geq 0.80$; mixing diagnostic; discriminability |
| **4. Demonstrated** | Computed under known ground truth, synthetic | "illustrates", "under known ground truth" | Everything the toy model produces; Paper C's Monte Carlo |
| **5. Conjectured** | Believed, not established | "we conjecture", "remains open" | Transfer to non-football systems; topology-conditional switching; the Collatz thread |

**Hypotheses on which the Tier 2 claims rest.** Bounded domain, fixed $N$. Strict stationarity within a regime. $\alpha$-mixing with summable coefficients. Bounded total persistence, supplied by boundedness. For the projected (FPCA-score) form of T2 only: an eigengap condition via Davis–Kahan. State T2 on the landscape series; retain scores for interpretation.

**Named failure conditions.** T1 fails if the dependence diagnostic shows non-summable decay. T2 is vacuous if $\Delta \leq 2C\varepsilon$, and saying so is a feature. R3 is the declared fallback: diagram-valued Wasserstein comparison, already demonstrated in the pilot, under which the T1 limit law is not claimed and the season analysis, library and diagram-valued change-point results still ship.

**Language discipline.** These substitutions are mandatory and were each adopted after a specific error.

| Do not write | Write | Why |
|---|---|---|
| "A unique mean path exists" | "The empirical mean path converges" | Existence is trivial in a Hilbert space; the claim invites "so what?" |
| "Single-threshold persistent homology" | "A single filtration over the full agent set" | PH is multi-scale by definition; the original reads as a misunderstanding |
| "The landscape representation is a Hilbert space" | "Landscapes take values in a Hilbert space" | A landscape is an element of $L^2$, not a space |
| "Both theorems are instantiated in software" | "Both results are implemented" | Theorems are proved; methods are implemented |
| "CUSUM on the FPCA scores" | "Functional CUSUM on the landscape series" | The score-space form needs an eigengap hypothesis |
| "Mixing verified" | "Dependence diagnostic" | Autocovariance decay is *consistent with* mixing, not proof of it |
| "Multiparameter persistence is intractable" | "impractical at the data rates required here" | An overclaim its authors would contest |
| "The framework generalises" | "...once interaction lengths are re-derived" | The scope boundary travels with the claim |
| "Validates the theorems" | "proves the theorems / tests their operational consequences" | Data does not validate a theorem |

A bold label, headline or bullet lead is read as a claim. Carry any hedge into the label or drop it from both.

---

## 7. Speculative threads, tiered

All Tier 5 unless stated. Recorded here so they are available without leaking into Small Grant text.

**GTPPF — Generalised Topological Predator-Prey Framework.** The Standard Grant paradigm name. The claim is that competitive collective systems across sport, oncology, defence and ecology share the structure of §1: spatially bounded, adversarially coupled, non-exchangeable point processes. *Keep "adversarial geometry" as the Small Grant term and GTPPF as the Standard Grant term.* Requires new theorems beyond T1/T2: cross-domain transfer rates, mean-field limits, topological phase transitions. Must position against mean-field games, pursuit–evasion and Lotka–Volterra rather than replicate them.

**Switching dynamics with topological feedback.** With $b(t)$ from §1.3, the switching rate $\lambda(X, b) = \lambda_0 + \lambda_1 f(\varphi(X))$ makes possession transitions depend on topological state. The mathematically novel claim is the feedback: topology as predictive of transitions rather than merely correlated with them. Not tested. Not in the Small Grant.

**Mean-field limit.** As $N \to \infty$, the empirical measure converges to $\mu_t$ satisfying a Fokker–Planck equation on $\Omega \times \{0,1\}$ with switching terms and reflecting boundary conditions. The key open question is whether the topological functional $\varphi[\mu]$ is continuous in the Wasserstein metric on measures, which is what would connect the limit to T2. Standard Grant theory.

**Collatz thread.** Assessed and largely closed. Honest verdict: primarily analogical. Three findings worth keeping. Persistent homology of Collatz orbits is genuinely unstudied, so the niche is real. The $n \equiv 7 \pmod 8$ enrichment is explained by Terras's parity-vector structure and needs no new theory. Critically, **the ratio$(\ell) = a + b/\ell$ law is governed by the universal coefficient theorem and torsion via multi-field persistence (Boissonnat–Maria), not by the Hasse principle** — the local-global framing is a metaphor and should not be used load-bearing. Two citation corrections: "Bradley (2009), *Ultrametrics and p-adic analysis in persistent homology*" **does not exist**; the correct references are Bradley (2017), *Finding Ultrametricity in Data using Topology*, J. Classification 34(1):76–84, and Bradley (2010). Tao's "almost all" is logarithmic density, weaker than natural density; the exceptional set is not known to be finite.

**Excluded, permanently for this grant.** Armed conflict as an application domain: ethics approval is pending and naming it could delay the application. This constraint carries to the Standard Grant. Quantitative finance: densest prior art, most contrived bounded domain, no Co-I.

---

## 8. Month 1, week by week

The acceptance test for this document. If §§1–7 are right, an RA can execute this without asking a question that is not a genuine research question.

**Standing rule.** Every task below has a pass condition. Report the pass condition's value, not "done".

### Week 1 — Reproduce the pilot

*Rationale.* Nothing downstream is trustworthy until the RA's environment reproduces the published numbers bit for bit. This also transfers the pipeline's tacit knowledge in the only way that works.

1. Build the container against the pinned stack in §2.5. Pass condition: `pip freeze` matches the pinned versions exactly.
2. Pull SkillCorner match 1996435. Retain only complete 22-player frames. Pass condition: **43,531** frames.
3. Subsample every 290th complete frame. Pass condition: **150** frames.
4. Cluster with single linkage at $\delta = 2.98$, $12.0$ and $30.0$ m and reduce to centroids. **Ignore the 1.39 m value in `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv`** (§2.2, ruling R4). Pass condition: $H_0$ means $19.02$, $4.77$.
5. Compute Vietoris–Rips $H_1$ with the adaptive $\varepsilon_{\max}$ of §2.5. Pass condition: **382** individual loops in 143/150 frames; **21** tactical loops in 19/150 frames; **0** team loops.
6. Cross-check one match's diagrams against GUDHI and giotto-tda. Pass condition: agreement to $10^{-6}$ m.

*If step 5 fails,* the fault is almost always the filtration floor or the linkage method. Single linkage, and the floor is $\max(5.0, 2\delta)$.

### Week 2 — Extend to the ten-match pilot and the derived statistics

*Rationale.* Establishes that the reproduction is not specific to one match, and exercises the bootstrap machinery O1 will depend on.

1. Repeat weeks 1.2–1.5 for the nine additional matches. Pass condition: grand means $19.05$ / $4.92$ / $1.38$; presence $97.0\%$ and $19.3\%$; 4,515 loops total.
2. Recompute scale complementarity. Pass condition: $\rho = 0.264$, and match-resampled bootstrap (1,000 draws, seed 42) median $0.262$ with CI $[0.200, 0.314]$.
3. Recompute cross-epoch stability using the sweep design in §2.2 and the definition now in Paper A's methods: pool sweep evaluations within 0.5 m of the cutoff, take the median cluster count, score the fraction within $\pm 2$ of it. Pass condition: **0.875** at the individual scale (2.98 m), **0.836** at the tactical scale, and **1.000** at the team scale.

### Week 3 — Championship ingestion

*Rationale.* The Month-2 gate needs a 20-match batch, and the data differ from the pilot in provenance, competition and frame rate. Discovering that in Month 2 is too late.

1. Ingest the first 20 Championship matches via the Swansea City AFC–StatsBomb agreement.
2. Audit against the pilot: frame rate, coverage completeness, pitch model, coordinate convention.
3. Produce a data-quality report. Pass condition: per-match complete-coverage frame counts and any coordinate transformations, written down.
4. Build the 10 Hz to 1 Hz downsampling path and retain both streams for the same matches.

### Week 4 — Prepare the two Month-2 gates

*Rationale.* The gates are the project's falsification points. They are prepared, pre-registered and only then run — running them first and pre-registering afterwards would be worthless.

1. Recompute cutoff stability on the 20-match batch using the definition written in week 2.3. Pass condition: $\geq 0.80$ at all three scales. **Below that, interaction lengths are re-derived before O2 starts.** This is a real decision point, not a formality.
2. Run the 1 Hz preservation check: compare $H_0$ regimes and $H_1$ presence between the 10 Hz and 1 Hz streams on the same matches. Rationale: pilot cutoffs are 10 Hz-derived and production is 1 Hz, so this closes the downsampling objection.
3. Draft the OSF pre-registration: exclusion criteria (the 552 to ~540 reduction), the venue $\times$ opponent-strength stratification, the three pre-registered formation classes, and the BH-FDR procedure.
4. Draft the Supercomputing Wales job structure. Rationale: frame-level homology is embarrassingly parallel, so the season is a scheduling problem, not a compute problem.

### What the RA should not do in Month 1

Not touch landscapes; the landscape module is Month 8. Not attempt bilateral or team-conditional decomposition; that is Paper B's object (§1.3). Not use the toy model for anything (§4.3). Not compute change-points before the dependence diagnostic exists, because the calibration depends on it.

---

## 9. Rulings

Each ruling resolves a contradiction that existed across the repository on 24 August 2026, and each is settled against pipeline evidence rather than by preferring a document.

**Status.** R1, R2, R4, R7, R8, R12, R13 and R14 were actioned on 24–25 August 2026; all are marked closed in place, because the reasoning is what prevents the error recurring. R3, R9 and R10 are standing prohibitions with no work attached. **R6 and R11 remain open and need a decision or a recompute.**

**R1 — Spearman $\rho$ is 0.264.** Evidence: `PAPERS/paper_A_JACT/pipeline/outputs/numbers.json` gives $0.26403$ over 1,500 frames, $p = 2.4 \times 10^{-25}$; `PAPERS/paper_A_JACT/pipeline/outputs/complementarity/bootstrap_multi_match_ci.json` gives median $0.2617$, CI $[0.1999, 0.3137]$. `CANONICAL_NUMBERS.md` is correct. The value 0.254 in `working_foundations.md` §11 predates the 6 July recompute. *Action: delete 0.254 from `working_foundations.md`.* **Closed 24 Aug 2026.**

**R2 — Primary-match $H_1$ presence is 95.3% and 12.7%, and the standing instruction to change it is wrong.** Evidence: `PAPERS/paper_A_JACT/pipeline/outputs/uniform_150/uniform_summary.json` and Paper A's Table `tab:h1single` both give 143/150 and 19/150. `working_foundations.md` §11 items 2 and 3 instruct updating the grant to 96.0% and 12.0%, which would put the grant *out* of agreement with the paper. *Action: delete those two instructions.* **Closed 24 Aug 2026** — both are struck in place, with the sampling difference explained rather than deleted.

**R3 — Match 1996435 has two legitimate analyses, and the primary one is canonical.** The multi-match batch row for the same match gives 144/150 (96.0%) individual and 18/150 (12.0%) tactical, under different sampling. Both are real. *Action: quote the `uniform_150` primary-match analysis whenever "the primary match" is named. Cite the multi-match row only as one of ten.*

**R4 — The individual cutoff is 2.98 m; 1.39 m is not an adopted value.** Evidence: `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` and `numbers.json` record `optimal_cutoff_m = 1.39` with `selection_method = "CH optimum"`, while Paper A, the grant and `CANONICAL_NUMBERS.md` all use 2.98 m. 1.39 m is the raw Calinski–Harabasz optimum. *Action: annotate the pipeline outputs to distinguish metric optimum from adopted value. Until then, §2.2 is the authority.* **Closed 24 Aug 2026** — the trap is documented in `PAPERS/paper_A_JACT/pipeline/README.md`. See R12, which is the deeper form of this problem and remains open.

**R5 — The cutoff stability score is now defined, and the definition is not what the name suggests.** Evidence: `identify_regimes()` in `ANALYSIS/AvailableData/primary_match_skillcorner_analysis.py` pools every sweep evaluation within 0.5 m of the selected cutoff, takes the median cluster count over that pool, and scores the fraction of evaluations whose cluster count lies within $\pm 2$ of that median. So it measures **reproducibility of the partition**, not reproducibility of the cutoff. Added to Paper A's cutoff-selection subsection on 24 August 2026. *Action: when quoting the 0.80 gate, describe it as partition reproducibility across temporal windows. Do not describe it as cutoff agreement.*

**R6 — Team-scale $H_0$ has three recorded values under unstated conventions.** `numbers.json` gives 0.88 for the primary match; Paper A's results text gives $1.44 \pm 0.50$; the multi-match grand mean is 1.38. These differ in how the single all-players cluster is counted. *Action: fix one convention, state it in §1.2 terms, and recompute. Until resolved, quote 1.38 for the ten-match grand mean and do not quote 0.88 anywhere.*

**R7 — Reference numbering is out of sync.** REV3 renumbered to 28 entries in first-appearance order; `04_References.md` still holds 23; `CANONICAL_NUMBERS.md` still records the methodology paper as [19] and the football paper as [22]. *Action: sync both to REV3, using §3 of this file as the mapping source.* **Closed 24 Aug 2026** — then 28 entries at [22] and [28]. The same-day Schenck insertion (§10) makes this 29 entries: methodology paper [23], football-analytics paper [29].

**R8 — T1 is a convergence claim, and three dependents still carry the retired framing.** REV3 states T1 as convergence with uniqueness demoted to a precondition. Still outstanding: `AdversarialTDA_Specification.md` line 13 asserts uniqueness, and `fig4_frechet_T1.png` and `fig8_montecarlo_T2.png` are named for the retired statement. *Action: rewrite the line and rename the figures to their diagram-valued content.* **Closed 24 Aug 2026** — the specification is restated at lines 13, 100 and 298; the figures are now `fig4_frechet_diagram_mean.png` and `fig8_montecarlo_cusum_delay.png`, with `adversarial_tda.m` updated.

**R9 — Co-Investigator effort is 0.1 FTE combined.** `TIMELINE.md` and REV3 agree at 0.1; `VA_V8p9_EPSRC_R6.md` says 0.25. V8.9 is superseded. *Action: none beyond not reintroducing 0.25.*

**R10 — The objective structure is O1–O2, not O1–O4.** REV3 and `TIMELINE.md` agree on two objectives: O1 population-scale geometry (Months 1–9) and O2 inference for dependent topological processes (Months 4–10). The O1–O4 structure in V8.9 is superseded; evidence-pack compilation is an output at Month 12, not an objective. *Action: none beyond not reintroducing O3/O4 numbering.*

**R11 — The domain diameter is undocumented, and T2's constant depends on it.** Paper A's methods give positions "in metres on a standard pitch model" without stating the model. The toy uses $120 \times 80$ with $D_\Omega = 144.22$, which is not the real pitch. Since T2's Lipschitz constant $C$ is explicit in $N$ and $D_\Omega$, an unstated domain means the bound cannot be evaluated numerically. *Action: read the pitch dimensions from SkillCorner match metadata, record them in §2.1, state them in Paper A's Data subsection, and compute $D_\Omega$. Low effort, and it removes a question a referee will certainly ask of T2.*

**R12 — The individual-scale cutoff and its stability score do not come from the sweep Paper A describes, and this affects a submitted manuscript.** Two linked findings, both from reading `identify_regimes()` against `methods.tex`.

First, the sweep's Calinski–Harabasz optimum for the individual scale is **1.39 m**, recorded in `PAPERS/paper_A_JACT/pipeline/outputs/regime_summary.csv` with `selection_method = "CH optimum"`. Paper A's methods state that "the individual-scale cutoff, 2.98 m, and the team-scale cutoff, 30.0 m, are the values selected by these automated metrics directly." That is true of the team scale and **not** of the individual scale. 2.98 m is carried over from an earlier normalised-coverage derivation, hard-coded as `VALIDATED_CUTOFFS` in `primary_match_skillcorner_analysis.py`, where it is recorded as $2.98 \pm 0.37$ m with a temporal stability of 0.88 under a different definition.

Second, and consequently, the individual-scale stability score of **0.956 was computed at 1.39 m, not at 2.98 m**, because `identify_regimes()` scores each scale at its own recomputed cutoff. The tactical score (0.836 at 12.0 m) and the team score (1.000 at 30.0 m) do correspond to the adopted values; the individual one does not.

*Action, in order.* (i) Recompute individual-scale stability at 2.98 m. (ii) Decide whether Paper A's sentence is corrected to state that 2.98 m is carried over and independently validated, or whether the individual cutoff is re-derived on this sweep. This is a decision for the PI, not a silent edit, because the manuscript is submitted. (iii) Until (i) is done, quote 0.84–1.00 as the stability range only for the tactical and team scales. A LaTeX comment marking this sits in `methods.tex` immediately above the affected sentence.

*Action.* **Closed 25 Aug 2026 (Option A).** Individual stability at the adopted 2.98 m cutoff is **0.875** (recomputed from `cutoff_sweep_results.csv`). Paper A `methods.tex` now states that 2.98 m is carried over from an earlier normalised-coverage calibration, names 1.39 m as the CH optimum not adopted (stability 0.956), and quotes 0.875 / 0.836 / 1.000 at the three adopted cutoffs. `regime_summary.csv` and `numbers.json` distinguish adopted cutoffs from the CH optimum. *Standing rule: never quote 0.956 as individual stability without stating it is at 1.39 m, not 2.98 m.*

**R13 — $\rho = 0.264$ is a correlation on total persistence, and Paper A described it as a correlation on counts.** `steps/04_complementarity.py` computes the Spearman statistic from `h1_total_persistence_ind` against `h1_total_persistence_tac`, giving $0.26403$. Paper A's `results.tex` read "individual-scale and tactical-scale $H_1$ **counts** correlate weakly (Spearman $\rho=0.264$)". The counts version of the same test is $0.211$, so the text named one statistic and quoted another. `methods.tex` compounded this by describing both the Spearman and the Fisher test as operating on "frame-level co-occurrence", which is true only of the Fisher test.

The number was never wrong and the bootstrap CI $[0.200, 0.314]$ is valid, because `bootstrap_multi_match_ci.py` line 57 uses the same total-persistence column as the point estimate. Only the prose was wrong.

*Action.* **Closed 25 Aug 2026.** `results.tex` now says "total $H_1$ persistence" and quotes $\rho=0.211$ on counts as a robustness check; `methods.tex` now defines both statistics separately; `04_complementarity.py` emits `spearman_statistic`, `spearman_rho_counts` and `fisher_statistic` so the definition travels with the number; `numbers.json` was rebuilt with every other headline value unchanged. *Standing rule: never quote $\rho=0.264$ without naming the statistic it is computed on.*

**R14 — the bottleneck "95th-percentile tail" was the maximum, and the TDA-native numbers had no backing file in the pipeline.** Found while closing R13, in the same Results subsection. Two faults.

First, provenance. `results.tex` §3.4 quoted a bottleneck median of 1.511 m and a landscape $L^2$ median of 5.671, but `steps/04_complementarity.py` only runs `tda_native_distances.py` when `RUN_TDA_NATIVE=1`, which had never been set. `numbers.json` carried `tda_native: {}`, and `sync_to_paper.py` listed 1.511 as a **forbidden** pattern precisely because it was unbacked. The real outputs existed at `results/paper_v5_revisions/`, outside the pipeline tree, from an April run.

Second, and more serious, the number. The paper described **7.994 m** as "a 95th-percentile tail". `tda_native_distances_summary.json` records 7.9938 as `max`. The true 95th percentile is **3.416 m**. The sentence compares that tail to the tactical scale's own mean persistence of 3.797 m and calls it "comparable", which is true of 3.416 and not of 7.994, so the intent was clearly the percentile and the maximum was picked up by mistake.

*Action.* **Closed 25 Aug 2026, but the number change needs PI confirmation before the arXiv push**, because it alters a value in a manuscript recorded as submitted. The CSV and an enriched summary carrying `p95` alongside `median`, `iqr` and `max` now live in `pipeline/outputs/complementarity/`; `numbers.json` carries `tda_native` populated; `results.tex` reads 3.416 m; the `sync_to_paper.py` check was inverted from forbidding 1.511 to forbidding 7.994. *Standing rule: gudhi is not in the working environment, so any recompute of these four values must be done where GUDHI 3.11.0 is installed, per `methods.tex`.*

---

## 10. Sync obligations

**A change to the statement of T1 or T2 is a change to a system.** Sweep in this order: this file §5 and §6; `02_Vision_and_Approach_REV3.md` §1 and §5; the R3 wording in §6; `T1_T2_Six_Registers.md`; `AdversarialTDA_Specification.md`; the toy-model figure filenames; `01_Summary.md`.

**A change to a number** goes into §2 or §4 of this file first, then `CANONICAL_NUMBERS.md`, then the V&A markdown and its LaTeX twin, then the paper pipelines' sync scripts.

**Adding a reference** triggers three actions: renumber to first-appearance order, sync `04_References.md`, and update the ledger column in §3.

**24 Aug 2026 — Schenck (2022) inserted as [6].** Former [6]–[28] are now [7]–[29]. The methodology paper is [23]; the football-analytics paper is [29]. Chapter 8 of Schenck is the algebraic-foundations cite for multiparameter persistence, alongside Botnan & Lesnick [4] and Lesnick [5].

**Before accepting any V&A revision:** body word count measured, not inherited; mean sentence length at or below 18 words with none over 35; no bold label claiming more than its own body text; every number traceable to this file; every stratification divided out and checked; every "beyond X" has X named somewhere in the document.
