# Hierarchical adversarial point processes: a diagram analogue of mean-path and change-point inference

**Working draft (Paper C)** — methods note, UK English. Developed **after Papers A and B are submitted.** Not for JACT or JSS. Cite Paper A for observational football; do not re-analyse SkillCorner. Numbers from `numbers.json`. Proofs of the tractable cases: `lemmas.md`.

**Intended venues (in order):** *Journal of the Royal Society Interface*; *SIAM Journal on Mathematics of Data Science* or *Foundations of Data Science* if the Tier-2 lemmas carry the paper; *Methods in Ecology and Evolution* only if the editor accepts a simulation-first note. Not JACT (Paper A).

---

## Abstract

Competitive collectives organise at several spatial scales at once, and consecutive observations are dependent because each agent responds to an adversary. Statistical topology supplies stable summaries of that organisation, but convergence of an empirical mean path and localisation of a structural transition have been stated for persistence *landscapes* on football tracking data. This note is the corresponding computation on *persistence diagrams*, with an explicit split of what is proved and what is only checked. We cite Wasserstein stability, the Carlsson–Mémoli correspondence, and Page's CUSUM (Tier 1). We prove that the coordinatewise mean of sorted deaths is the exact $W_2$ Fréchet mean for equal-cardinality birth-zero diagrams, give a first-order $W_1$–$W_2$ gap, and a Wald delay formula for CUSUM on the persistent statistic $\xi_t=W_1(D_t,D_{\mathrm{ref}})$ under coin-flip increments (Tier 2). Full well-posedness under tug-of-war dependence, and the landscape theorems T1/T2, remain conjectures supported by Monte Carlo (Tier 3). The running example is a simulated territorial predator–prey system, not a relabelled pitch; a second generator is corridor pursuit–evasion. Observational Movebank GPS and serial multiplex imaging are the Standard Grant, not this paper.

---

## 1. Introduction

When two populations compete inside a bounded region, local clusters, larger groupings, and the envelope of the whole collection coexist. Single-threshold homology folds those levels into one picture. Consecutive snapshots are also not exchangeable: each agent's movement constrains what happens next. Those two obstacles are the reason a football-validated Small Grant targets landscape-valued convergence of an empirical mean path (T1) and a Wasserstein-stability bound for landscape-valued CUSUM (T2).

This paper does not prove T1 or T2. It is the **diagram $W_1/W_2$ analogue** on controlled adversarial clouds — the fallback named in the grant if the landscape argument is intractable — with known ground truth. Claims carry three weights, so a reviewer need not guess:

- **Tier 1.** Cohen–Steiner et al. (2007) stability; Carlsson and Mémoli (2010) $H_0$/MST; Page (1954) CUSUM. Cited, not re-derived.
- **Tier 2.** Lemma T1-lite and Proposition T2-lite (`lemmas.md`): the $W_2$ barycentre of equal-cardinality birth-zero diagrams; a first-order gap to the $W_1$ Fréchet mean; a Wald delay $h/\delta$ for CUSUM on $\xi_t=W_1(D_t,D_{\mathrm{ref}})$ under uncorrelated increments. Overlay on Monte Carlo (Figure 5).
- **Tier 3.** The same qualitative behaviour under genuine tug-of-war dependence, and the landscape theorems, are conjectures. Computational evidence is reported; the Standard Grant is where those theorems belong.

Football remains the calibrated empirical testbed (Paper A). We do not re-analyse those matches, and we do not copy football metre values. One paragraph of origin is enough: the pipeline was first used on twelve-agent pitch clouds; the present generators change $N$, diameter, and hierarchy depth.

The lead generator is territorial predator–prey ecology. The PI already publishes with a bio-logging group on high-resolution animal movement (Gunner et al. 2026): paths composed of fundamental steps and turns, with prey pursuit and predator evasion among the causes of heading change. That work is a different mathematical object — one trajectory, not two competing point clouds — and is not the dataset here. Movebank pack GPS is the observational next step, not Domain 1 of this note.

A second generator, multi-robot pursuit–evasion in a corridor, uses pair geometry rather than the football triangle. Oncology is named in the Outlook. Vipond et al. (2021) already classify static multiplex images with multiparameter landscapes; a 2025 vineyard/zigzag study already treats synthetic tumour–immune dynamics. Our remaining gap is serial paired clouds with competitive dependence.

## 2. Framework

Let $X_t\subset\Omega$ be a finite point cloud. Vietoris–Rips $H_0$ deaths are the edge weights of a Euclidean minimum spanning tree (Carlsson and Mémoli 2010). For birth-zero diagrams the $p$-Wasserstein distance is optimal transport on the line, including matching to the diagonal at cost $(\mathrm{death}/2)^p$; we solve the assignment problem rather than sort-and-match.

**T1-lite.** Following Turner et al. (2014) in the one-dimensional special case: for equal-cardinality birth-zero diagrams, if the $W_2$ matching does not use the diagonal, the coordinatewise mean of sorted deaths is the exact $W_2$ Fréchet mean (Lemma T1-lite). It is **not** the minimiser of $\mathbb{E}[W_1(D_i,\mu)^2]$. A first-order expansion in death-space noise $\varepsilon$ shows that the coordinate gap is $\Theta(\varepsilon)$ while the relative $W_1$-objective gap stays $\Theta(1)$ (Proposition, `lemmas.md`). Around the ecology dispersed diagram, that relative gap is about $6\%$ at $\sigma=1.2$, with a global-feature shift of $0.06$ units. Dispersion is reported as $\sigma_F^2=\frac1n\sum_i W_2(D_i,\mu_2)^2$.

**T2-lite.** The theorem-shaped statistic is the *persistent* series $\xi_t=W_1(D_t,D_{\mathrm{ref}})$ against a pre-change diagram. Under coin-flip (independent) jitter, increments of $\xi_t$ may be treated as uncorrelated; Cohen–Steiner / MST Lipschitz gives $W_1(D(X),D(X'))\le 2(N-1)\varepsilon$. Wald/Siegmund then yields $\mathbb{E}[\hat T-T^*]\approx h/\delta$ with $\delta=J-\kappa$ (Proposition T2-lite). Consecutive-frame $W_1(D_t,D_{t-1})$ is a *pulse* detector: it is autocorrelated even under coin-flips, and the Wald formula is not claimed for it. It remains the operational CUSUM in Figure 3. Tug-of-war dependence is outside (A1) and is Tier 3.

Calibration: $\kappa$ and $h$ from a $5\%$ false-alarm in-control Monte Carlo. No $t\ge 30$ guard. Quote curves, not a single $\hat T$.

Display thresholds sit in gaps of the **new** death vector. They are not football's $\delta\in\{5,40,66\}$, not Paper A's clustering cutoffs, and not a copied `A_WIDE` barcode. Encirclement $H_1$ uses a birth maximum taken from that generator's ring (here $80$, not $45$).

## 3. Ecology generator (lead)

Territory $\Omega=[0,240]\times[0,180]$ (diameter $300$). Prey: five triples, $r=3.5$ ($N=15$). Predators: four triples, $r=2.8$ ($N=12$). Programmed $T^*=55$: dispersed hunting $\to$ encircling a herded group (smoothstep to $t=64$). Predators track prey centroids. Gaussian jitter $\sigma=1.8$.

Noise-free $H_0$ deaths (local / grouping / global):

| Cloud | Deaths (rounded) |
|-------|------------------|
| Prey dispersed | $7.00\times 5$, $7.05\times 5$, $87.49\times 4$ |
| Prey herded | $7.00\times 5$, $7.05\times 5$, $17.00\times 2$, $20.18\times 2$ |
| Prey column | $7.00\times 5$, $7.05\times 5$, $26.11\times 4$ |
| Predators hunting | $5.60\times 4$, $5.64\times 4$, $74.98$, $81.60$, $86.66$ |
| Predator ring | $5.60\times 4$, $5.64\times 4$, $62.46\times 3$ |

$W_1(\mathrm{dispersed},\mathrm{herded})=212.16$. The herded state is a two-level hierarchy (individuals within a tight meadow); the dispersed state merges groups only at $\approx 87$. Hierarchy *depth* is not a football constant.

**Scale conflation.** At $\delta=16$, dispersed groups and a north–south column both have $(\beta_0,\beta_1)=(5,0)$, yet $W_1=227.20$ (Figure 2A–C). Equal Betti numbers at one scale do not determine the diagram.

**Encirclement.** The predator ring has an $H_1$ bar $[62.46,90.40]$ (persistence $27.94$). Stacking the herd in the interior kills every finite $H_1$ bar (Figure 2D–F). $H_1$ here is an embedding feature (ring vs filled hole), not a dendrogram feature.

**CUSUM and Fréchet.** On consecutive prey-diagram $W_1$ (operational pulse detector, not T2-lite): headline seed $7$ gives $\hat T=59$ ($T^*=55$, error $4$). Quote the curve ($N=200$):

| Jump $W_1$ | $\mathbb{E}\lvert\hat T-T^*\rvert$ | Median | Power |
|-----------:|----------------------------------:|-------:|------:|
| 112.9 | 15.3 | 10 | 58.5% |
| 171.7 | 6.0 | 5 | 100% |
| 199.8 | 4.8 | 4 | 100% |
| 212.2 | 4.1 | 4 | 100% |

The $W_2$ Fréchet variance of a trailing window of length $12$ spikes while the window straddles $T^*$ and recovers. Predator $H_1$ persistence is zero until the ring closes after $T^*$. Figure 5 overlays the noise-free interpolant CUSUM (which tracks Monte Carlo of $\xi_t$) and the Wald $h/(J-\kappa)$ instant-shift formula (too optimistic on a smoothstep). Consecutive-frame delay is shown beside it as a different object.

**Ecological reading of $\hat T$.** The change-point is the onset of a coordinated hunt: prey groups collapse into a meadow and the pack closes a ring. That is a takeover / encirclement event a movement ecologist can accept or reject; it is not a pressing trigger imported from football. Gunner et al. (2026) supply the fine-scale grammar (straight steps, sharp turns, pursuit and evasion as heading decisions) that a later agent-based generator should respect. They do not supply this paper's point clouds.

## 4. Robotics generator (second)

Corridor $\Omega=[0,180]\times[0,50]$ (diameter $187$). Pursuers: four pairs ($N=8$). Evaders: three pairs ($N=6$). Internal pair length $4.8$, not the football triangle ($4.00$ / $4.03$). $T^*=40$ (open transit $\to$ funnel intercept). A rigid translation of the pursuer gate would leave $H_0$ invariant; the chase configuration pinches, so $W_1(\mathrm{gate},\mathrm{chase})=7.00$ is a different, smaller jump. CUSUM is run on **evader** diagrams.

Evader $W_1(\mathrm{open},\mathrm{funnel})=70.64$. At $\delta=12$, open layout and a single-file layout both have $(\beta_0,\beta_1)=(3,0)$ while $W_1=49.69$: the same conflation lesson, with this generator's gaps. Monte Carlo ($N=200$): at jump $W_1=48.4$, power $60\%$ and mean error $4.0$; at jumps $76.0$, $78.5$, and $70.6$, power $100\%$ and mean errors $2.8$, $2.2$, and $2.2$. Euclidean interpolation of point clouds is not monotone in $W_1$ (an intermediate blend can exceed the endpoint distance); detection still tracks jump size.

The statistics are the same; the metre values are not.

## 5. Dependence with identical marginals

Cluster centres are displaced by a zero-mean Gaussian field of fixed marginal variance. In the coupled model the predator (or pursuer) field is a lagged AR(1) of the prey (or evader) field — a tug-of-war. In the independent model each frame is a fresh draw. The one-frame marginal of every agent is the same, so a difference in the topological signal is dependence, not a change of noise level. The statistic is $W_1(D_t,D_{\mathrm{ref}})$ against the undisturbed cloud; consecutive-frame $W_1$ is autocorrelated even under independence and must not be used for this comparison.

On the ecology generator, $80$ replicates: coupled $\rho_1=+0.296$ (s.d. $0.139$); independent $\rho_1=-0.025$ (s.d. $0.106$). One realisation is shown in Figure 4D.

## 6. Limitations and Outlook

Diagrams are not landscapes. Tier 2 is not grant T1/T2. Simulation is not field data. Figure 5 of the football toy — four painted domains with identical $8$–$2$–$1$ barcodes — is a schematic of a transfer *hypothesis*; the present generators are the transfer *test*.

The Standard Grant closes the gap between (A1) coin-flip increments and tug-of-war, and between diagrams and landscapes. This paper's job is to state that gap precisely and to show the workflow on two non-football generators first.

**Observational ecology.** Needs simultaneous multi-animal positions in one territory. That is closer to Movebank-style pack GPS, or a dual-species deployment with the existing biologging group, than to the Dryad heading archive of Gunner et al. (2026). Redcliffe et al. (2025) ungulate slope-use is single-guild topography, not two-population TDA. Those datasets are **not** Domain 1 of this note.

**Oncology.** Serial multiplex imaging is the health pathway, with Co-I Powathil. Position against Vipond et al. (2021) and the 2025 synthetic vineyard paper.

Authorship may include a named subset of the biologging group to check the generator and $\hat T$. That decision is open.

## Figures

- `figures/fig1_ecology_territory.png` — three snapshots and prey $H_0$ barcodes.
- `figures/fig2_conflation_h1.png` — scale conflation; ring vs filled $H_1$.
- `figures/fig3_cusum_frechet.png` — operational consecutive-frame CUSUM, Fréchet variance, encirclement, Monte Carlo.
- `figures/fig4_robotics_dependence.png` — corridor intercept; coupled vs independent; evader barcode.
- `figures/fig5_t2_lite.png` — interpolant CUSUM vs Wald vs Monte Carlo of $\xi_t$; consecutive-frame delay as a separate object.

## References (author–year for this markdown draft)

Carlsson G, Mémoli F. Characterization, stability and convergence of hierarchical clustering methods. *J Mach Learn Res* 2010;11:1425–70.

Cohen-Steiner D, Edelsbrunner H, Harer J. Stability of persistence diagrams. *Discrete Comput Geom* 2007;37:103–20.

Gidea M, Katz Y. Topological data analysis of financial time series: Landscapes of crashes. *Physica A* 2018;491:820–34.

Gunner RM, Wilson RP, Lurgi M, Börger L, Redcliffe J, Shepard ELC, Holton MD, …, Brown R, …, Potts JR. High resolution data reveal fundamental steps and turns in animal movements. *Ecol Monogr* 2026;96(2):e70069. doi:10.1002/ecm.70069.

Page ES. Continuous inspection schemes. *Biometrika* 1954;41:100–15.

Redcliffe J, Wilson R, Holton M, et al. Steep slopes, shallow angles: mountain ungulates create their own topography through movements. *Can J Zool* 2025;103:1–18.

Siegmund D. *Sequential Analysis*. Springer; 1985. (Wald approximations for CUSUM delay.)

Turner K, Mileyko Y, Mukherjee S, Harer J. Fréchet means for distributions of persistence diagrams. *Discrete Comput Geom* 2014;52:44–70.

Vipond O, Bull JA, Macklin PS, et al. Multiparameter persistent homology landscapes identify immune cell spatial patterns in tumors. *Proc Natl Acad Sci USA* 2021;118:e2102166118.

Paper A (in review / JACT target): multi-scale persistent homology of competitive football point clouds.

*Add on submission:* the 2025 tumour–immune vineyard/zigzag paper (PMC12325540); Bhattacharya et al. (SIGSPATIAL 2016); Bubenik landscapes.
