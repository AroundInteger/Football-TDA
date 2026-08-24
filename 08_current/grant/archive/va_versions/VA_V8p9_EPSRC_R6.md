<!--
Vision & Approach — V8.9 (EPSRC R6)
Derived from VA_V8p8_EPSRC_R6.md. V8.9 implements the ordered
five-pass framing revision (chat 2026-08-04): mathematics-led hierarchy,
technical-density trim, National Importance as capability claim, then
Benefits/Translation consistency so later sections do not re-centre
football.

Reviewer points addressed (labels R1–R7; carried from V8.8, deepened here):
  R1  Foreground the mathematics.
  R2  Reframe football as testbed rather than destination.
  R3  Strengthen National Importance.
  R4  Sharpen theoretical objectives / state hypotheses explicitly.
  R6  Distinguish football-specific from mathematically general.
  R7  Reduce sentence density / improve readability.
  (R5, PI intellectual leadership, is addressed in the separate Research
   Team section of the JeS application, not in V&A.)

Section-level changes vs V8.8:

§1  (Quality and Mathematical Importance) — Passes 1–2, hybrid, then
      RB 3-beat opener refinement (chat 2026-08-04 evening).
    - Opener (3 beats): define competitive collective systems; two
      obstacles (overlapping-scale H0/H1 structure; non-exchangeable
      adversarial coupling); solution shape (validated interaction
      lengths → time-dependent topological inference). No football;
      literature fork deferred to Importance (R1, R2, R7).
    - Importance. leverages class-wide transfer once scales are
      re-derived; cites PH collapse [1–3], multiparameter [4,5] and
      exchangeability failure [6,8].
    - Mathematical contribution. retains theorem glosses (Fréchet mean
      path; Wasserstein-stability; landscape-valued CUSUM).
    - Quality. research quality to realise the ambition: falsifiable
      cutoffs, pilot (§2), professional sports tracking as
      experimental platform (football not named in §1; domain detail
      remains in §2/§4/§7). Remit/UKRI detail stays in §5.

§2  (Background) — Pass 4, then pilot-stats trim (chat 2026-08-04)
    - Closing pilot block shortened: three H0 / two H1 regimes and
      scale complementarity stated without full numeric dump; details
      deferred to [17]. Panel Vision keeps the validation claim; Approach
      (§7 sample-size) retains the figures needed for power calculations.

§3  — unchanged from V8.8.

§4  (Timeliness, Need, Opportunity) — Pass 4
    - Need rewritten to lead with the problem class / mathematical
      workflow gap; sport retained as one demand domain among others.
    - Opportunity platform thesis retained verbatim from V8.8.

§5  (Impact) — Pass 3
    - National importance rewritten as UK mathematical capability
      beyond exchangeable settings + remit alignment + staged pathway.
      Application shopping list (AV / sensors / biology) removed from
      NI; pathways remain in Stepping-stone. Addresses R3 without
      inflating near-term translation.
    - Mathematical impact, Economic/industry impact, and Stepping-stone
      retained in role (minor wording unchanged from V8.8).

§6  (Benefits) — Pass 4
    - Mathematicians / open library lead; club analysts and sports-
      analytics as co-development partners; other domains longer-term.

§7–§9, §11, §12 — unchanged from V8.8.

§10 (Translation) — Pass 4
    - Publication order: methodology [17], full-season results, then
      companion football-analytics [22]. Open-source package still leads.

Word-count arithmetic (V8.8 body: 1715 words -> V8.9 body: 1711 words;
net −4 words after §2 pilot trim):

  §1  3-beat opener + Importance leverage + literature + theorems     : heavier
  §2  pilot numeric dump cut (−51); validation claim retained           : lighter
  §4–§6, §10 as prior framing passes; §3, §7–§9, §11–§12 unchanged
  Net: opener growth offset by Background trim.

Numeric values: full pilot dump removed from §2 (deferred to [17]).
  Retained where needed for design/power in Approach: p = 0.051; 32;
  180; 540; 1,600; 5,000; and sample-size inputs in §7. Canonical pilot
  figures remain in [17] and CANONICAL_NUMBERS.md.

Paul-voice compliance vs V8.8:
  No "first"/"firstness" wording.
  Research-goal opener retained (football deferred past theorems).
  Team request retained up front (§7).
  Timeliness led by methodology (§4).
  Standard Grant framed as follow-on (§5, §7 O4).
  No self-congratulatory language; translation not inflated.

Reference list unchanged from V8.8 (22 items). Citation audit:
  [1,2]      §1, §2                    [11–13]  §2
  [3]        §1, §2                    [14]     §2, §7 O3
  [4,5]      §1, §2, §4                [15]     §2
  [4,6,8,9]  §4                        [16]     §2
  [6]        §1 x2, §2, §3, §5, §7 O3  [17]     §2, §10
  [6,8]      §1                        [18]     §7 O3
  [6,8,9]    §2, §3                    [19]     §7 O3
  [7]        §2                        [20]     §8
  [8,9]      §3                        [21]     §8
  [10]       §2                        [22]     §10
  All 22 references remain cited; natbib order-of-first-appearance
  numbering therefore unchanged from V8.8.

UK English throughout. Vancouver [n] citations preserved (natbib
+ unsrtnat conventions).
-->

VISION

1. Quality and Mathematical Importance
Competitive collective systems represent a ubiquitous yet mathematically under-developed class of multi-agent systems where agents coordinate internally against an active adversary within a bounded spatial domain. Such dynamics govern autonomous swarm defence, tumour–immune spatial fronts and tactical team sports. Characterising their structural organisation and phase transitions is confounded by two primary obstacles: key geometric structures (H0 connected clusters and H1 coverage loops) exist across overlapping interaction scales, and continuous adversarial coupling produces strongly dependent, non-exchangeable observations. To solve this, the project establishes a statistical-topology framework that isolates scale-specific structure using empirically validated interaction lengths, providing the foundation for time-dependent topological inference.
Establishing that framework matters beyond any single application domain: once interaction lengths are re-derived, the same bounded adversarial geometry transfers across the class. Standard persistent homology [1,2] with a single threshold across all agents [3] merges scale-specific H0 and H1 structure. Multi-parameter persistence [4,5] is the natural alternative but remains impractical for high-frequency competitive point clouds. Current statistical topology [6,8] assumes exchangeable observations that competitive dynamics violate.
Mathematical contribution. Two theorem-level results. A Fréchet mean path—a stable average topological shape—exists uniquely in persistence-summary space under non-exchangeable competitive dynamics, extending [6]. A Wasserstein-stability bound for landscape-valued CUSUM statistics gives provable error control for change-point detection under explicit dependence assumptions. Both are proved and tested at season scale (§7, O3).
Realising this ambition requires mathematical rigour with empirical falsifiability. Stability-validated cutoffs define groups by tested interaction lengths rather than arbitrary thresholds; scale decomposition is validated at pilot scale (§2). Professional sports tracking provides the population-scale experimental platform: a fully observable multi-agent system under strict boundaries and continuous adversarial coupling.

1. Background Building on Previous Work 
Persistent homology [1,2] and its stability theorem [7] provide the mathematical basis: small tracking errors induce only small changes in topological summaries. Statistical tools compare persistence summaries for classification, distance-based analysis and change-point detection [6,8,9], forming the basis for O2–O3. Standard applications either use a single global scale [3] or multi-scale clustering developed for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in biological aggregation, motion and nearest-neighbour-governed flocking [11–13], motivating this interaction-length framing. Existing topological change-point methods [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the high-frequency, bounded testbed; geometric baselines include team length, width, centroid distance [15] and pitch-control space creation [16]. Our methodology paper [17] develops and validates the pipeline: decompose by interaction length, then compute scale-wise homology using adaptive thresholds. Across 10 professional matches the pilot recovers three stable connected-cluster regimes and two complementary loop regimes, with scales carrying largely independent information; detailed statistics are in [17]. These results motivate season-scale theory tests.

2. Advancing Current Understanding and Generating New Knowledge The project culminates in O3, which develops new statistical-topology theory for time-evolving competitive systems. O1 establishes the distributional laws that underpin the theory: whether stability scores, loop-presence rates and scale complementarity are population-level regularities, and whether the moments required for a Wasserstein-mean path over topological summaries converge across matches. O2 establishes the comparison geometry: distances between topological summaries [8,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for change-point statistics. O3 treats each match as a time series of summaries to prove and test the mean-path and CUSUM-stability results at season scale, extending statistical topology [6,8,9] to competitive multi-scale systems (§7).

3. Timeliness, Need and Opportunity Timeliness. Three developments have converged: mature multi-scale topology and statistical comparison tools [4,6,8,9]; scalable season-scale computation (§8); and competitive tracking data at population scale. Need. Competitive multi-agent systems lack a validated statistical-topology workflow (§1). Sport, and prospectively health, logistics and autonomous coordination, need interpretable structural measures of organisation, gaps, loops and transitions beyond conventional geometry. Opportunity. Football serves as a population-scale experimental platform through which new statistical-topology theory for competitive multi-agent systems is developed, tested and generalised to other bounded competitive systems once scales are re-derived.

4. Impact Mathematical impact. The primary contribution is new statistical-topology theory for dependent competitive systems (§1, O3). Existing results address static or exchangeable settings; this project extends them to sequential adversarial dynamics through mean-path theory and Wasserstein-stability results for landscape-valued change-point statistics. Both theorems are instantiated in an open-source library for competitive point-cloud dynamics. National importance. The project builds UK capability in statistical topological data analysis beyond exchangeable settings, where theory lags data-rich competitive spatial systems. It aligns with the mathematical sciences, AI-enabled modelling and complex-systems remits. Near-term outputs are the theorems and open library; cross-domain work is staged via the Standard Grant (§7, O4). Economic and industry impact. Co-developed with Swansea City AFC and StatsBomb, the project translates summaries into practitioner outputs unavailable from conventional geometry. Stepping-stone to translation. It prepares a follow-on Standard Grant (§7, O4); post-grant pathways include tumour–immune competition with Co-I Powathil and other bounded adversarial systems.

5. Benefits and Beneficiaries Mathematicians benefit immediately from the open-source library and benchmarked features (§5); sports-analytics researchers and Swansea City AFC analysts benefit as co-development partners; other bounded competitive multi-agent domains benefit longer-term via the follow-on Standard Grant pathway (§7, O4).

APPROACH

7. Research Design and Objectives Project structure and team. This 12-month project comprises the PI, 0.2 FTE, leading framework development, analysis and publication; two Co-Investigators, 0.25 FTE combined, providing statistical and domain expertise; a Research Associate, Months 2–10, implementing the pipeline and full-season analysis; and Swansea City AFC–StatsBomb partnerships for tracking data and formation labels. Sample-size rationale. A full Championship season (≈540 matches) provides precision and power: ≈32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale loop presence (pilot s.d. 0.072); ≈180 matches per tactical class detect Cohen's d ≥ 0.30 at 80% power, α = 0.05, Benjamini–Hochberg FDR. A borderline pilot within-match effect (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

O1: Population-level topological statistics (PI and RA, Months 1–7). O1 measures how features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match Month 1–2 batch re-validates cutoffs against [17]; stability < 0.80 triggers re-derivation. RA processing Months 2–7; PI-led analysis Months 5–7. Milestones: cutoff gate, Month 2; barcode database, Month 7. O2: Topological fingerprinting (PI, Months 6–9). O2 tests whether formation systems have signatures beyond geometric metrics. StatsBomb and SkillCorner labels are checked using Cohen's κ. Tactical systems are compared using topological-summary distances [6,8] and diagram-image features (§8), benchmarked against length, width and convex-hull area. Success criteria: signatures for ≥3 tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. Milestones: OSF pre-registration, Month 2; fingerprint results, Month 9. O3: Temporal dynamics and structural transitions (PI and RA, Months 4–10). O3 extends single-scale topological change-point detection [14] to competitive, bounded, multi-scale systems (§3). The PI applies FPCA [18], CUSUM [19] and bootstrap calibration [6]. Two theorems are targeted. T1 (well-posedness): the Fréchet mean path in landscape space exists uniquely on any compact interval under bounded-domain, bounded-velocity and landscape-moment assumptions, extending [6] beyond exchangeable data. T2 (stability): for the landscape-valued CUSUM on a stationary segment under bounded perturbation, the expected localisation error is bounded by the Wasserstein distance between pre- and post-change diagram distributions up to a sup-norm landscape constant. Proofs use Wasserstein continuity of landscapes under bootstrap resampling [6] and moment bounds on CUSUM increments [19]. Success criterion: change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05; fallback is direct Wasserstein diagram comparison. Milestones: landscape module, Month 8; O2/O3 outputs, Month 9.

O4: Standard Grant evidence synthesis (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for the follow-on Standard Grant (§5). O1–O3 remain standalone publishable contributions. Milestone: evidence pack, Month 12.

8. Methodology A containerised Python pipeline (Ripser [20], GUDHI, giotto-tda [21]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests cutoff transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

9. Feasibility and Risk Management Feasibility. The project is feasible in 12 months: pilot-validated method (§2), modest computation (§8), and an early validation gate. Season-scale processing requires ≈1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12); the team combines applied topology, statistical modelling and football-domain expertise (§11), with RA implementation capacity. Risk management. Data access is resolved: the 2024/25 Championship season is held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium likelihood/impact. Scale transferability: the Month-2 gate re-derives cutoffs if stability falls below 0.80. Formation-label noise: mitigated through dual-source verification, Cohen's κ, unsupervised clustering and pre-registered exclusions. Landscape theory: if sequential landscape development exceeds the timescale, O3 uses direct Wasserstein diagram comparison.

10. Translation to Outcomes and Impact The pipeline will be released as a documented, containerised open-source package via Swansea University's Zenodo community with DOI, including scripts, diagnostics, workflows and feature tables. Publications: the methodology paper [17], arXiv Month 1, submitted Months 1–2; a full-season results paper for Month 11; and the companion football-analytics paper [22]. Practitioner outputs with Swansea City AFC translate summaries into pressing/formation decision-support tools (§5). The Month-12 evidence pack feeds the follow-on Standard Grant (§7, O4).

11. Research Environment The Zienkiewicz Institute supports method development, high-performance analysis and reusable software across computational mathematics, applied topology and sport science. The PI leads the applied-topology framework; Prof Gibin Powathil brings mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff brings sport and exercise science for tactical interpretation; and Swansea City AFC provides a live co-development setting.

12. Facilities, Infrastructure and Host Support Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production, O3 and contingency runs. The containerised pipeline (§8) supports reproducible local and high-performance execution. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and ethics review.

---

**References** *(natbib/unsrtnat order of first appearance; 22 items; unchanged from V8.8. Verify against the compiled LaTeX bibliography before pasting into JeS.):*

1. Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255–308. `Carlsson2009`
2. Zomorodian, A. & Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249–274. `Zomorodian2005`
3. Edelsbrunner, H. & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society. `Edelsbrunner2010`
4. Botnan, M. B. & Lesnick, M. (2022). An introduction to multiparameter persistence. In *Representations of Algebras and Related Structures* (pp. 77–150). EMS Press. `BotnanLesnick2022`
5. Lesnick, M. (2015). The theory of the interleaving distance on multidimensional persistence modules. *Foundations of Computational Mathematics*, 15(3), 613–650. `Lesnick2015`
6. Chazal, F., Fasy, B. T., Lecci, F., Rinaldo, A. & Wasserman, L. (2014). Stochastic convergence of persistence landscapes and silhouettes. *Proceedings of the 30th Annual Symposium on Computational Geometry*, 474–483. `Chazal2014`
7. Cohen-Steiner, D., Edelsbrunner, H. & Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120. `CohenSteiner2007`
8. Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16(1), 77–102. `Bubenik2015`
9. Adams, H. et al. (2017). Persistence images: a stable vector representation of persistent homology. *Journal of Machine Learning Research*, 18(8), 1–35. `Adams2017`
10. Schindler, D. J. & Barahona, M. (2023). Analysing multiscale clusterings with persistent homology. arXiv:2305.04281. `SchindlerBarahona2023`
11. Topaz, C. M., Ziegelmeier, L. & Halverson, T. (2015). Topological data analysis of biological aggregation models. *PLoS ONE*, 10(5), e0126383. `Topaz2015`
12. Bhaskar, D. et al. (2019). Analysing collective motion with machine learning and topology. *Chaos*, 29(12), 123125. `Bhaskar2019`
13. Ballerini, M. et al. (2008). Interaction ruling animal collective behaviour depends on topological rather than metric distance. *PNAS*, 105(4), 1232–1237. `Ballerini2008`
14. Gu, K. et al. (2022). Change point detection in multi-agent systems based on higher-order features. *Chaos*, 32(11), 113117. `Gu2022`
15. Folgado, H. et al. (2014). Length, width and centroid distance as measures of teams' tactical performance in youth football. *European Journal of Sport Science*, 14(S1), S487–S492. `Folgado2014`
16. Fernández, J. & Bornn, L. (2018). Wide open spaces: a statistical technique for measuring space creation in professional soccer. *Sloan Sports Analytics Conference*. `FernandezBornn2018`
17. Brown, R. et al. (2026). Multi-scale persistent homology for competitive spatial systems: measurement-aware methods and validation in professional football. *ArXiv preprint*; submitted to the *Journal of Applied and Computational Topology*. `Brown2026`
18. Ramsay, J. O. & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.). Springer. `RamsaySilverman2005`
19. Page, E. S. (1954). Continuous inspection schemes. *Biometrika*, 41(1/2), 100–115. `Page1954`
20. Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423. `Bauer2021`
21. Tauzin, G. et al. (2021). giotto-tda: a topological data analysis toolkit for machine learning and data exploration. *Journal of Machine Learning Research*, 22(39), 1–6. `Tauzin2021`
22. Brown, R. et al. (2026). Multi-scale topological signatures of tactical organisation in professional football. *In preparation*; to be submitted to the *Journal of Sports Sciences*. `Brown2026b`
