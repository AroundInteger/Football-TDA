<!--
Vision & Approach — V8.7 (EPSRC R6)
Derived from VA_V8p6_EPSRC_R6.md. Two synchronisation passes applied:

(1) Paul-concerns re-audit. V8.6 was mapped against the six issues in
    08_current/grant/review/WHAT_CHANGED_FOR_PAUL.md; five are already
    addressed unchanged (research-goal opener, team block up front,
    timeliness led by methodology not libraries, Standard Grant framed
    as follow-on, no self-congratulatory language). One item slipped
    back in when the V8.6 §5 theorem-novelty sentence was drafted:

      V8.6 §5: "... the second gives the first change-point stability
                bound for landscape-valued time series."

    reintroduces a "firstness" claim that Paul explicitly flagged and
    that his fix replaced with an "advances" framing (see review file,
    row 1). V8.7 restores Paul's fix using the exact "advances" verb:

      V8.7 §5: "... the second advances change-point stability theory
                to landscape-valued time series."      ≈ -2 words

    No other Paul-relevant phrasing was found in V8.6.

(2) Reference re-sync. V8.6 inherited the 26-item numbering from the
    fuller 6-page version. Compression to 3 pages dropped four
    contextual citations whose sentences no longer appear:
      15 Gudmundsson & Horton 2017 (spatio-temporal team sports)
      16 Memmert et al. 2017       (tactical performance analyses)
      20 Di Salvo et al. 2007      (playing-position performance)
      21 Bradley et al. 2009       (high-intensity running EPL)
    (Paul-excluded Brown-in-prep conflict paper was already out.)

    The remaining 22 references are re-ordered by first appearance so
    the manual [n] numbers match what natbib+unsrtnat will compile.
    Mapping (V8.6 [old] -> V8.7 [new], key preserved):

       1 -> 1   Carlsson2009            15 (dropped)
       2 -> 2   Zomorodian2005          16 (dropped)
       3 -> 3   Edelsbrunner2010        17 -> 15   Folgado2014
       4 -> 4   BotnanLesnick2022       18 -> 16   FernandezBornn2018
       5 -> 5   Lesnick2015             19 -> 17   Brown2026 (JACT)
       6 -> 8   Bubenik2015             20 (dropped)
       7 -> 6   Chazal2014              21 (dropped)
       8 -> 7   CohenSteiner2007        22 -> 22   Brown2026b (JSS)
       9 -> 9   Adams2017               23 -> 20   Bauer2021 (Ripser)
      10 -> 10  SchindlerBarahona2023   24 -> 21   Tauzin2021 (giotto-tda)
      11 -> 11  Topaz2015               25 -> 18   RamsaySilverman2005
      12 -> 12  Bhaskar2019             26 -> 19   Page1954
      13 -> 13  Ballerini2008
      14 -> 14  Gu2022

    All bracket lists re-sorted ascending (natbib numbers,sort&compress
    convention): [6,7,9] -> [6,8,9]; [6,9] -> [8,9]; [4,6,7,9] ->
    [4,6,8,9]; [6,7] -> [6,8]. Bibliography appended at foot of file.

Word count deltas:
  Paul-fix (§5)     : -2 words
  Renumbering       :  0 words
  In-place tweak    : +1 word (see below)
  Net vs V8.6       : -1 word (V8.6 body 1705 -> V8.7 body 1704)

In-place tweak (applied to this file, not spawned as a new version because
it is a single-sentence edit that does not change any structural claim):

  §5 second sentence, to drop the duplicate [6] citation flagged as a
  read-through niggle (natbib will re-cite the same key twice within a
  paragraph, which is legal but reads repetitively next to the earlier
  "extending [6]"):

    Before: "The first extends [6] beyond the exchangeable regime to
             competitive sequential data; ..."
    After : "The first pushes statistical topology beyond the exchangeable
             regime to competitive sequential data; ..."

  Rationale: "statistical topology" is the exact phrase used in §3's
  closer ("extend statistical topology [6,8,9] to competitive multi-scale
  systems") -- so this §5 sentence now reads as a specific instantiation
  of §3's summary claim rather than a repetition. Cost +1 body word;
  bibliography unchanged (Chazal2014 is still cited via "extending [6]"
  in the preceding sentence and elsewhere in §7 O3).

Bibliography (22 items) is appended in the same file for audit and
LaTeX-sync purposes; the JeS 3-page V&A count refers to the body only
(VISION -> §12), consistent with V8.4-V8.6.

All V8.4-V8.6 Priority-1 restorations retained. All numeric values
preserved verbatim:
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 2.98 / 12.0 / 30.0 m; p = 0.051; 32; 180; 540;
  1,600; 5,000.

UK English. Vancouver [n] citations preserved.
-->

VISION

1. Quality and Mathematical Importance This research extends multi-scale topological analysis to competitive collective systems: agents that coordinate internally while competing against an adversary within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports, yet remain under-modelled as a distinct class. Their defining feature is adversarial geometry: unlike cooperative swarms, competing subgroups deform each other's configurations across multiple scales. Importance. No existing method attributes connected-cluster and loop structure to the distinct interaction scales of hierarchical, high-frequency competitive systems. Standard persistent homology [1,2], applied with a single threshold across all agents [3], collapses these scales into one summary, obscuring individual-, group- and system-level organisation. Multi-parameter topology [4,5] offers a theoretical route to scale-specific structure, but remains computationally prohibitive for real-world, high-frequency competitive data. This project closes that gap in professional football: pilot analysis has identified stability-validated interaction scales (§2), and a full Championship season will test whether they persist as population-level structure and establish a transferable framework once characteristic scales are re-derived elsewhere (§5). Quality. The project combines mathematical rigour with empirical validation. Stability-validated cutoffs define groups by empirically tested interaction lengths rather than arbitrary thresholds, making the procedure falsifiable. Scale decomposition and adaptive distance thresholds are already validated at pilot scale (§2). The new contribution is both theoretical and empirical: time-evolving summaries require well-posedness of a mean path in summary space under competitive, non-exchangeable sequential data, extending [6], and a stability bound for the CUSUM statistic under Wasserstein perturbation. Both are established and tested at season scale (§7, O3).

2. Background Building on Previous Work Persistent homology [1,2] and its stability theorem [7] provide the mathematical basis: small tracking errors induce only small changes in topological summaries. Statistical tools compare persistence summaries for classification, distance-based analysis and change-point detection [6,8,9], forming the basis for O2–O3. Standard applications either use a single global scale [3] or multi-scale clustering developed for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in biological aggregation, motion and nearest-neighbour-governed flocking [11–13], motivating this interaction-length framing. Existing topological change-point methods [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the high-frequency, bounded testbed; geometric baselines include team length, width, centroid distance [15] and pitch-control space creation [16]. Our methodology paper [17] develops and validates the pipeline: decompose by interaction length, then compute scale-wise homology using adaptive thresholds. Across 10 professional matches, SkillCorner, 10 Hz, 104,722 event–topology pairs [17], three connected-cluster regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale regimes emerge: individual-scale loops are near-universal (97.0% ± 1.5%) but short-lived (mean persistence 1.98 m); tactical-scale loops are rarer (19.3% ± 7.2%) but longer-lived (3.80 m). The scales carry largely independent information (ρ = 0.264) and respond coherently to match events (p < 0.001).

3. Advancing Current Understanding and Generating New Knowledge The project builds summary-space results for time-evolving competitive systems (O3) through three advances. (i) Distributional laws: establishing whether stability scores, loop-presence rates and scale complementarity are population-level regularities rather than pilot artefacts, enabling a mean path over such summaries (specifically, convergent moments across matches, permitting Wasserstein-mean estimation). (ii) Comparison geometry: establishing that distances between topological summaries [8,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for change-point statistics. (iii) Functional dynamics: treating each match as a time series of summaries to characterise structural transitions and prove and test the O3 results at season scale. Together they extend statistical topology [6,8,9] to competitive multi-scale systems (O1–O3, §7).

4. Timeliness, Need and Opportunity Timeliness. Three developments have converged: mature multi-scale topology and statistical comparison tools [4,6,8,9]; scalable season-scale computation (§8); and competitive tracking data at population scale. Need. No validated workflow exists for this problem class (§1); sport, and prospectively health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry. Opportunity. Professional football provides a population-scale testbed for a validated workflow transferable to other bounded competitive systems once scales are re-derived.

5. Impact Research impact. The primary mathematical contribution is publishable theory for statistical topology on competitive sequential data (§1, §7, O3). Two results are targeted: well-posedness of a mean path in summary space, extending [6], and a Wasserstein-stability bound for CUSUM. The first pushes statistical topology beyond the exchangeable regime to competitive sequential data; the second advances change-point stability theory to landscape-valued time series. Both are instantiated in an open-source library for competitive point-cloud dynamics. This builds UK capability in applied topology, aligned with EPSRC's mathematical sciences and AI/data priorities. Economic and industry impact. Co-developed with Swansea City AFC and StatsBomb, the project translates summaries into practitioner outputs for pressing, formation gaps and defensive-line organisation, unavailable from conventional geometry. Stepping-stone to translation. It prepares a follow-on Standard Grant (§7, O4), building the evidence base for translation beyond football; post-grant pathways include tumour–immune competition with Co-I Powathil and other bounded adversarial systems once scales are re-derived.

6. Benefits and Beneficiaries Mathematicians, sports-analytics researchers and Swansea City AFC analysts benefit immediately from the open-source library and benchmarked features (§5); other bounded competitive multi-agent domains benefit longer-term via the follow-on Standard Grant pathway (§7, O4).

APPROACH

7. Research Design and Objectives Project structure and team. This 12-month project comprises the PI, 0.2 FTE, leading framework development, analysis and publication; two Co-Investigators, 0.25 FTE combined, providing statistical and domain expertise; a Research Associate, Months 2–10, implementing the pipeline and full-season analysis; and Swansea City AFC–StatsBomb partnerships for tracking data and formation labels. Sample-size rationale. A full Championship season (≈540 matches) provides precision and power: ≈32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale loop presence (pilot s.d. 0.072); ≈180 matches per tactical class detect Cohen's d ≥ 0.30 at 80% power, α = 0.05, Benjamini–Hochberg FDR. A borderline pilot within-match effect (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

O1: Population-level topological statistics (PI and RA, Months 1–7). O1 measures how features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match Month 1–2 batch re-validates cutoffs against [17]; stability < 0.80 triggers re-derivation. RA processing Months 2–7; PI-led analysis Months 5–7. Milestones: cutoff gate, Month 2; barcode database, Month 7. O2: Topological fingerprinting (PI, Months 6–9). O2 tests whether formation systems have signatures beyond geometric metrics. StatsBomb and SkillCorner labels are checked using Cohen's κ. Tactical systems are compared using topological-summary distances [6,8] and diagram-image features (§8), benchmarked against length, width and convex-hull area. Success criteria: signatures for ≥3 tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. Milestones: OSF pre-registration, Month 2; fingerprint results, Month 9. O3: Temporal dynamics and structural transitions (PI and RA, Months 4–10). O3 extends single-scale topological change-point detection [14] to competitive, bounded, multi-scale systems (§3, iii). The PI applies FPCA [18], CUSUM [19] and bootstrap calibration [6]. Mathematical targets are well-posedness of a mean path in summary space, extending [6], and a Wasserstein-stability bound for CUSUM. Proof routes are Wasserstein continuity of landscape maps under bootstrap resampling [6] and moment-condition bounds on CUSUM increments [19]. Success criterion: change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05; fallback is direct Wasserstein diagram comparison. Milestones: landscape module, Month 8; O2/O3 outputs, Month 9.

O4: Standard Grant evidence synthesis (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for the follow-on Standard Grant (§5). O1–O3 remain standalone publishable contributions. Milestone: evidence pack, Month 12.

8. Methodology A containerised Python pipeline (Ripser [20], GUDHI, giotto-tda [21]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests cutoff transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

9. Feasibility and Risk Management Feasibility. The project is feasible in 12 months: pilot-validated method (§2), modest computation (§8), and an early validation gate. Season-scale processing requires ≈1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12); the team combines applied topology, statistical modelling and football-domain expertise (§11), with RA implementation capacity. Risk management. Data access is resolved: the 2024/25 Championship season is held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium likelihood/impact. Scale transferability: the Month-2 gate re-derives cutoffs if stability falls below 0.80. Formation-label noise: mitigated through dual-source verification, Cohen's κ, unsupervised clustering and pre-registered exclusions. Landscape theory: if sequential landscape development exceeds the timescale, O3 uses direct Wasserstein diagram comparison.

10. Translation to Outcomes and Impact The pipeline will be released as a documented, containerised open-source package via Swansea University's Zenodo community with DOI, including scripts, diagnostics, workflows and feature tables. Publications comprise the methodology paper [17] (target: Journal of Applied and Computational Topology or comparable), arXiv Month 1, submitted Months 1–2; the companion football-analytics paper [22] (Journal of Sports Sciences); and a full-season results paper for Month 11. Practitioner outputs with Swansea City AFC translate summaries into pressing/formation decision-support tools (§5). The Month-12 evidence pack feeds the follow-on Standard Grant (§7, O4).

11. Research Environment The Zienkiewicz Institute supports method development, high-performance analysis and reusable software across computational mathematics, applied topology and sport science. The PI leads the applied-topology framework; Prof Gibin Powathil brings mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff brings sport and exercise science for tactical interpretation; and Swansea City AFC provides a live co-development setting.

12. Facilities, Infrastructure and Host Support Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production, O3 and contingency runs. The containerised pipeline (§8) supports reproducible local and high-performance execution. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and ethics review.

---

**References** *(natbib/unsrtnat order of first appearance; 22 items; four references from the fuller 6-page version — Gudmundsson2017, Memmert2017, DiSalvo2007, Bradley2009 — are omitted because the sentences citing them are no longer in this 3-page V&A. Verify against the compiled LaTeX bibliography before pasting into JeS.):*

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
