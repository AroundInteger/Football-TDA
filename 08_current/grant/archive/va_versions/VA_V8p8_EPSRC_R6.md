<!--
Vision & Approach — V8.8 (EPSRC R6)
Derived from VA_V8p7_EPSRC_R6.md. V8.8 implements the six-point revision
plan synthesised in chat on 2026-08-03 in response to the reviewer note
"applied-topology project with football testbed" (headline recommendation).
The user's proposal (RB) and the assistant's proposal (AI) were merged;
each edit below is attributed accordingly.

Reviewer points addressed (labels R1–R7 correspond to the reviewer's
numbered "priority order for revisions"):
  R1  Foreground the mathematics.
  R2  Reframe football as testbed rather than destination.
  R3  Strengthen National Importance.
  R4  Sharpen theoretical objectives / state hypotheses explicitly.
  R6  Distinguish football-specific from mathematically general.
  R7  Reduce sentence density / improve readability.
  (R5, PI intellectual leadership, is addressed in the separate Research
   Team section of the JeS application, not in V&A.)

Section-level changes vs V8.7 (attribution: RB = user proposal; AI =
assistant proposal; RB+AI = merged):

§1  (Quality and Mathematical Importance)
    - Opener rewritten (RB). Football removed from the first three
      sentences; the third sentence positions football as the validation
      environment, not the research problem. Addresses R1, R2.
    - Mathematical-obstacle sentence inserted at end of Importance (RB):
        "Existing persistence-landscape theory [6,8] is largely developed
         for independent or exchangeable observations, whereas competitive
         systems generate temporally dependent and adversarially coupled
         data."
      Addresses R1, R4 (names why existing theory does not apply).
    - "Mathematical contribution" label added as the closer of §1 (AI),
      promoted from the V8.7 closer of §1 and duplicated V8.5/V8.7
      wording in §5 and §7. Two theorem-level results now visible on
      page 1. Addresses R1, R4.
    - "hierarchical, high-frequency" -> "hierarchical" and
      "real-world, high-frequency competitive data" -> "high-frequency
      competitive data" (AI, R7 sentence-density trim).
    - The V8.7 sentence "This project closes that gap in professional
      football: ..." (32 words) is removed (RB); its content is now
      carried by the rewritten opener and by §4's thesis sentence.
    - The V8.7 sentence "The new contribution is both theoretical and
      empirical: time-evolving summaries require ..." is removed (AI);
      its content is now carried by the new "Mathematical contribution"
      block, avoiding triple-statement of the same two theorems in §1,
      §5 and §7.

§2  (Background)
    - Minor: "SkillCorner, 10 Hz, 104,722 event–topology pairs [17]" ->
      "104,722 event–topology pairs [17] at 10 Hz" (AI, wording only;
      104,722 and 10 Hz retained verbatim per V8.7 header directive).
    - Otherwise unchanged. All V8.7 numeric values preserved verbatim.

§3  (Advancing Understanding)
    - Reframed as "the project culminates in O3" hierarchy (RB): O1 and
      O2 explicitly labelled as empirical basis; O3 named as the site of
      new statistical-topology theory. Addresses R1, R4, R7 (three
      parallel "(i)/(ii)/(iii)" clauses split into three sentences).
    - Closing clause "extending statistical topology [6,8,9] to
      competitive multi-scale systems" retained verbatim (V8.7 wording).

§4  (Timeliness, Need, Opportunity)
    - Opportunity clause rewritten (RB, point 7) to embed the single
      highest-value framing sentence:
        "Football serves as a population-scale experimental platform
         through which new statistical-topology theory for competitive
         multi-agent systems is developed, tested and generalised to
         other bounded competitive systems once scales are re-derived."
      Addresses R2, R6 (subsumes the AI-proposed general-vs-specific
      sentence; football is unambiguously the platform, the theory is
      the deliverable).

§5  (Impact)
    - "Research impact" heading renamed to "Mathematical impact" (RB);
      paragraph rewritten in RB's stronger form. The V8.7 explicit
      restatement of the two theorems is removed (they now live in §1
      and O3); §5 keeps only the framing that they are the "primary
      contribution ... extending [6] beyond exchangeable settings".
    - "National importance" inserted as a labelled sub-paragraph (RB,
      condensed form; ~45 words). Explicitly connects to UK mathematical
      sciences, AI-enabled modelling, complex systems, autonomous-vehicle
      coordination, distributed-sensor networks and adversarial
      biological dynamics. Addresses R3.
    - "Economic and industry impact" tightened (AI, R7): the football
      domain-example list ("pressing, formation gaps and defensive-line
      organisation") shortened to "practitioner outputs unavailable
      from conventional geometry", preserving co-development claim.
    - "Stepping-stone to translation" preserved with minor trim (AI).

§6  (Benefits)
    - Compressed to one sentence per beneficiary group (AI, R7).

§7  (Approach — O3 rewrite)
    - O1 and O2 unchanged.
    - O3 "Mathematical targets" clause replaced by two labelled
      theorem statements T1 (well-posedness) and T2 (stability) (AI,
      point 4). Assumptions are now explicit (bounded-domain, bounded-
      velocity, moment conditions on the landscape functional;
      stationary segment plus bounded perturbation; sup-norm landscape
      bound). Addresses R4 directly and R1 by making the mathematics
      the visible centrepiece of Approach.
    - "Proof routes" retained but tightened (AI); the citation load is
      unchanged ([6], [19]).

§8  (Methodology) — unchanged.
§9  (Feasibility and Risk) — unchanged.
§10 (Translation)
    - Publication targets tightened (AI, R7): the parenthetical journal
      names "(Journal of Applied and Computational Topology or
      comparable)" and "(Journal of Sports Sciences)" removed from §10
      because they are already carried by the references [17] and [22];
      arXiv/submission timing retained.
    - "pressing/formation decision-support tools" retained.

§11 (Research Environment) — unchanged.
§12 (Facilities) — unchanged.

Word-count arithmetic (V8.7 body: 1705 words -> V8.8 body: 1717 words;
net +12 words, i.e. +0.7%; this is within layout tolerance for the JeS
3-page V&A. All Δ measured against V8.7 per-section counts after the
tightening pass; the RB draft ran +90 words at first draft and was
trimmed in place to +12 without losing any reviewer-directed content.):

  §1  opener rewrite + math obstacle + math contribution label :  -12
      (RB opener removes "This project closes that gap in
      professional football..." sentence; AI "Mathematical
      contribution" label reuses V8.7 text duplicated in §5/§7;
      Importance paragraph tightened for readability.)
  §2  minor phrasing only ("SkillCorner, 10 Hz" -> "10 Hz")    :   0
  §3  culmination reframing (tightened after first draft)      :   -5
  §4  thesis-sentence embedding (RB point 7)                   :  +10
  §5  mathematical-impact rewrite + National Importance insert
      + industry/stepping-stone trim                           :  -10
      (National Importance costs ~40 words, funded by removing
      the V8.7 explicit theorem re-statement (~35 words), the
      "unavailable from conventional geometry" domain-example
      list, one duplicate mention of tumour–immune competition,
      and the "This builds UK capability ..." sentence.)
  §6  compression rolled back -- restored to V8.7 wording      :   0
  §7  O1/O2/project structure unchanged;
      O3 T1/T2 labelled theorems (net after tightening)        :  +29
      (T1/T2 add ~51 words in explicit assumptions and
      conclusions; the V8.7 "Mathematical targets ... Proof
      routes are ..." block supplied ~22 words that are re-
      purposed into the theorem statements.)
  §10 publication-target trim (journal names -> refs [17][22]) :  -14
  §8, §9, §11, §12 unchanged                                   :   0
  §4 thesis + §7 O3 T1/T2 together account for the entire
  net +12; both are directly reviewer-directed (R2/R6 and R4).

Numeric values preserved verbatim per V8.7 header directive:
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 10 Hz; 2.98 / 12.0 / 30.0 m; p = 0.051; 32;
  180; 540; 1,600; 5,000. p < 0.001 also preserved.

Paul-fix compliance vs V8.7:
  V8.7's "advances" verb in §5 is preserved as "extends ... beyond
  exchangeable settings ... through mean-path theory and Wasserstein-
  stability results" (no "first"/"firstness" claim reintroduced).
  V8.7's §5 "pushes statistical topology beyond the exchangeable
  regime" phrase is subsumed into the tighter RB rewrite of §5
  mathematical impact.
  No "first"/"firstness" wording appears in V8.8.
  Research-goal opener retained (§1 opener now: "Competitive
  collective systems form an important but largely unstudied class ..."
  which is a research-goal opener in RB's proposed form).
  Team block retained up front (§7 "Project structure and team").
  Timeliness led by methodology (§4 "mature multi-scale topology and
  statistical comparison tools [4,6,8,9]") not by libraries.
  Standard Grant framed as follow-on (§5, §7 O4).
  No self-congratulatory language.

Reference list unchanged from V8.7 (22 items). Citation audit:
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
  numbering therefore unchanged from V8.7.

UK English throughout. Vancouver [n] citations preserved (natbib
+ unsrtnat conventions).
-->

VISION

1. Quality and Mathematical Importance Competitive collective systems form a largely unstudied class of multi-agent systems in which agents coordinate internally while competing against adversarial groups within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports. Existing topological methods do not separate structure at different interaction scales, limiting their ability to characterise organisation, adaptation and structural transition. This project develops the statistical topology required to analyse such systems, validated at population scale using professional football data. Importance. No existing method attributes connected-cluster and loop structure to the distinct interaction scales of hierarchical competitive systems. Standard persistent homology [1,2] with a single threshold across all agents [3] collapses these scales, obscuring individual-, group- and system-level organisation. Multi-parameter topology [4,5] offers a theoretical route to scale-specific structure but remains computationally prohibitive at high frequency. Existing persistence-landscape theory [6,8] is largely developed for independent or exchangeable observations, whereas competitive systems generate temporally dependent and adversarially coupled data. Quality. The project combines mathematical rigour with empirical validation. Stability-validated cutoffs define groups by empirically tested interaction lengths rather than arbitrary thresholds, making the procedure falsifiable. Scale decomposition and adaptive distance thresholds are already validated at pilot scale (§2). Mathematical contribution. Two theorem-level results: existence and uniqueness of a Fréchet mean path in persistence-summary space under non-exchangeable competitive dynamics, extending [6]; and a Wasserstein-stability bound for landscape-valued CUSUM statistics with explicit dependence assumptions. Both are proved and tested at season scale (§7, O3).

2. Background Building on Previous Work Persistent homology [1,2] and its stability theorem [7] provide the mathematical basis: small tracking errors induce only small changes in topological summaries. Statistical tools compare persistence summaries for classification, distance-based analysis and change-point detection [6,8,9], forming the basis for O2–O3. Standard applications either use a single global scale [3] or multi-scale clustering developed for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in biological aggregation, motion and nearest-neighbour-governed flocking [11–13], motivating this interaction-length framing. Existing topological change-point methods [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the high-frequency, bounded testbed; geometric baselines include team length, width, centroid distance [15] and pitch-control space creation [16]. Our methodology paper [17] develops and validates the pipeline: decompose by interaction length, then compute scale-wise homology using adaptive thresholds. Across 10 professional matches, 104,722 event–topology pairs [17] at 10 Hz, three connected-cluster regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale regimes emerge: individual-scale loops are near-universal (97.0% ± 1.5%) but short-lived (mean persistence 1.98 m); tactical-scale loops are rarer (19.3% ± 7.2%) but longer-lived (3.80 m). The scales carry largely independent information (ρ = 0.264) and respond coherently to match events (p < 0.001).

3. Advancing Current Understanding and Generating New Knowledge The project culminates in O3, which develops new statistical-topology theory for time-evolving competitive systems. O1 establishes the distributional laws that underpin the theory: whether stability scores, loop-presence rates and scale complementarity are population-level regularities, and whether the moments required for a Wasserstein-mean path over topological summaries converge across matches. O2 establishes the comparison geometry: distances between topological summaries [8,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for change-point statistics. O3 treats each match as a time series of summaries to prove and test the mean-path and CUSUM-stability results at season scale, extending statistical topology [6,8,9] to competitive multi-scale systems (§7).

4. Timeliness, Need and Opportunity Timeliness. Three developments have converged: mature multi-scale topology and statistical comparison tools [4,6,8,9]; scalable season-scale computation (§8); and competitive tracking data at population scale. Need. No validated workflow exists for this problem class (§1); sport, and prospectively health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry. Opportunity. Football serves as a population-scale experimental platform through which new statistical-topology theory for competitive multi-agent systems is developed, tested and generalised to other bounded competitive systems once scales are re-derived.

5. Impact Mathematical impact. The primary contribution is new statistical-topology theory for dependent competitive systems (§1, O3). Existing results address static or exchangeable settings; this project extends them to sequential adversarial dynamics through mean-path theory and Wasserstein-stability results for landscape-valued change-point statistics. Both theorems are instantiated in an open-source library for competitive point-cloud dynamics. National importance. The project develops mathematical capability for analysing data-rich competitive systems, contributing to UK strengths in mathematical sciences, AI-enabled modelling and complex-systems research. The resulting methods are relevant wherever competing agents generate large-scale spatial–temporal data, including autonomous-vehicle coordination, distributed-sensor networks and adversarial biological dynamics. Economic and industry impact. Co-developed with Swansea City AFC and StatsBomb, the project translates summaries into practitioner outputs unavailable from conventional geometry. Stepping-stone to translation. It prepares a follow-on Standard Grant (§7, O4); post-grant pathways include tumour–immune competition with Co-I Powathil and other bounded adversarial systems.

6. Benefits and Beneficiaries Mathematicians, sports-analytics researchers and Swansea City AFC analysts benefit immediately from the open-source library and benchmarked features (§5); other bounded competitive multi-agent domains benefit longer-term via the follow-on Standard Grant pathway (§7, O4).

APPROACH

7. Research Design and Objectives Project structure and team. This 12-month project comprises the PI, 0.2 FTE, leading framework development, analysis and publication; two Co-Investigators, 0.25 FTE combined, providing statistical and domain expertise; a Research Associate, Months 2–10, implementing the pipeline and full-season analysis; and Swansea City AFC–StatsBomb partnerships for tracking data and formation labels. Sample-size rationale. A full Championship season (≈540 matches) provides precision and power: ≈32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale loop presence (pilot s.d. 0.072); ≈180 matches per tactical class detect Cohen's d ≥ 0.30 at 80% power, α = 0.05, Benjamini–Hochberg FDR. A borderline pilot within-match effect (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

O1: Population-level topological statistics (PI and RA, Months 1–7). O1 measures how features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match Month 1–2 batch re-validates cutoffs against [17]; stability < 0.80 triggers re-derivation. RA processing Months 2–7; PI-led analysis Months 5–7. Milestones: cutoff gate, Month 2; barcode database, Month 7. O2: Topological fingerprinting (PI, Months 6–9). O2 tests whether formation systems have signatures beyond geometric metrics. StatsBomb and SkillCorner labels are checked using Cohen's κ. Tactical systems are compared using topological-summary distances [6,8] and diagram-image features (§8), benchmarked against length, width and convex-hull area. Success criteria: signatures for ≥3 tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. Milestones: OSF pre-registration, Month 2; fingerprint results, Month 9. O3: Temporal dynamics and structural transitions (PI and RA, Months 4–10). O3 extends single-scale topological change-point detection [14] to competitive, bounded, multi-scale systems (§3). The PI applies FPCA [18], CUSUM [19] and bootstrap calibration [6]. Two theorems are targeted. T1 (well-posedness): the Fréchet mean path in landscape space exists uniquely on any compact interval under bounded-domain, bounded-velocity and landscape-moment assumptions, extending [6] beyond exchangeable data. T2 (stability): for the landscape-valued CUSUM on a stationary segment under bounded perturbation, the expected localisation error is bounded by the Wasserstein distance between pre- and post-change diagram distributions up to a sup-norm landscape constant. Proofs use Wasserstein continuity of landscapes under bootstrap resampling [6] and moment bounds on CUSUM increments [19]. Success criterion: change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05; fallback is direct Wasserstein diagram comparison. Milestones: landscape module, Month 8; O2/O3 outputs, Month 9.

O4: Standard Grant evidence synthesis (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for the follow-on Standard Grant (§5). O1–O3 remain standalone publishable contributions. Milestone: evidence pack, Month 12.

8. Methodology A containerised Python pipeline (Ripser [20], GUDHI, giotto-tda [21]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests cutoff transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

9. Feasibility and Risk Management Feasibility. The project is feasible in 12 months: pilot-validated method (§2), modest computation (§8), and an early validation gate. Season-scale processing requires ≈1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12); the team combines applied topology, statistical modelling and football-domain expertise (§11), with RA implementation capacity. Risk management. Data access is resolved: the 2024/25 Championship season is held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium likelihood/impact. Scale transferability: the Month-2 gate re-derives cutoffs if stability falls below 0.80. Formation-label noise: mitigated through dual-source verification, Cohen's κ, unsupervised clustering and pre-registered exclusions. Landscape theory: if sequential landscape development exceeds the timescale, O3 uses direct Wasserstein diagram comparison.

10. Translation to Outcomes and Impact The pipeline will be released as a documented, containerised open-source package via Swansea University's Zenodo community with DOI, including scripts, diagnostics, workflows and feature tables. Publications: the methodology paper [17], arXiv Month 1, submitted Months 1–2; the companion football-analytics paper [22]; and a full-season results paper for Month 11. Practitioner outputs with Swansea City AFC translate summaries into pressing/formation decision-support tools (§5). The Month-12 evidence pack feeds the follow-on Standard Grant (§7, O4).

11. Research Environment The Zienkiewicz Institute supports method development, high-performance analysis and reusable software across computational mathematics, applied topology and sport science. The PI leads the applied-topology framework; Prof Gibin Powathil brings mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff brings sport and exercise science for tactical interpretation; and Swansea City AFC provides a live co-development setting.

12. Facilities, Infrastructure and Host Support Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production, O3 and contingency runs. The containerised pipeline (§8) supports reproducible local and high-performance execution. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and ethics review.

---

**References** *(natbib/unsrtnat order of first appearance; 22 items; unchanged from V8.7. Verify against the compiled LaTeX bibliography before pasting into JeS.):*

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
