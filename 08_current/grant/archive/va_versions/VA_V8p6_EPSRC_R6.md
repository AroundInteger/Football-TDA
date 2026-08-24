<!--
Vision & Approach — V8.6 (EPSRC R6)
Derived from VA_V8p5_EPSRC_R6.md. V8.5 recovered ~65 words (1719 → 1654
body words) via phrase-level trims. V8.6 reinvests ~52 of those words in
three targeted additions chosen to strengthen the mathematical reviewer's
reading of the proposal, keeping V8.5's shorter sentence style throughout.

All V8.4/V8.5 Priority-1 restorations retained; all numeric values and
objective structure (O1, O2, O3, O4) preserved verbatim.

Additions applied (all single-sentence inserts; no restructuring):

  §3 (i)  Append parenthetical to the "Distributional laws" item to
          state the concrete form of the population-level regularity
          the objective targets, tying (i) to §5/§7 O3's mean-path
          theorem:
            "(specifically, convergent moments across matches,
             permitting Wasserstein-mean estimation)."       ≈ +9 words

  §5      Insert one sentence after "Two results are targeted: ..."
          to state the novelty of each theorem (what makes it new
          relative to [7] and to existing CUSUM stability theory):
            "The first extends [7] beyond the exchangeable regime to
             competitive sequential data; the second gives the first
             change-point stability bound for landscape-valued time
             series."                                        ≈ +24 words

  §7 O3   Insert one sentence after "Mathematical targets are ..." to
          give the reviewer a proof-route hint for both named
          theorems, reassuring them that O3 is deliverable in 12
          months:
            "Proof routes are Wasserstein continuity of landscape
             maps under bootstrap resampling [7] and moment-condition
             bounds on CUSUM increments [26]."               ≈ +19 words

Net expected addition ≈ 52 words. V8.5 = 1654 → V8.6 ≈ 1706 words
(back at V8.4's budget, but with the extra words placed where a
mathematical reviewer will look for reassurance: named theorems
paired with proof-route hints and novelty claims).

Not applied (kept in reserve for post-compile calibration):
  • §9 residual-risk quantification (~30 words, option 4). Would
    strengthen the risk-audit reading; can be added later if space
    remains after compile.
  • §4 Need example on defensive transitions (~22 words, option 5).
    Would strengthen felt-need; kept out because §7 O2 already
    provides the empirical hook.
  • §1 "why competitive systems have been under-modelled" (~25 words,
    option 6). Redundant with §1's existing claim in the Importance
    subsection.

Numbers preserved verbatim (identical to V8.3–V8.5):
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 2.98 / 12.0 / 30.0 m; p = 0.051; 32; 180; 540;
  1,600; 5,000.

UK English. Vancouver [n] citations preserved.
-->

VISION

1. Quality and Mathematical Importance This research extends multi-scale topological analysis to competitive collective systems: agents that coordinate internally while competing against an adversary within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports, yet remain under-modelled as a distinct class. Their defining feature is adversarial geometry: unlike cooperative swarms, competing subgroups deform each other's configurations across multiple scales. Importance. No existing method attributes connected-cluster and loop structure to the distinct interaction scales of hierarchical, high-frequency competitive systems. Standard persistent homology [1,2], applied with a single threshold across all agents [3], collapses these scales into one summary, obscuring individual-, group- and system-level organisation. Multi-parameter topology [4,5] offers a theoretical route to scale-specific structure, but remains computationally prohibitive for real-world, high-frequency competitive data. This project closes that gap in professional football: pilot analysis has identified stability-validated interaction scales (§2), and a full Championship season will test whether they persist as population-level structure and establish a transferable framework once characteristic scales are re-derived elsewhere (§5). Quality. The project combines mathematical rigour with empirical validation. Stability-validated cutoffs define groups by empirically tested interaction lengths rather than arbitrary thresholds, making the procedure falsifiable. Scale decomposition and adaptive distance thresholds are already validated at pilot scale (§2). The new contribution is both theoretical and empirical: time-evolving summaries require well-posedness of a mean path in summary space under competitive, non-exchangeable sequential data, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation. Both are established and tested at season scale (§7, O3).

2. Background Building on Previous Work Persistent homology [1,2] and its stability theorem [8] provide the mathematical basis: small tracking errors induce only small changes in topological summaries. Statistical tools compare persistence summaries for classification, distance-based analysis and change-point detection [6,7,9], forming the basis for O2–O3. Standard applications either use a single global scale [3] or multi-scale clustering developed for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in biological aggregation, motion and nearest-neighbour-governed flocking [11–13], motivating this interaction-length framing. Existing topological change-point methods [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the high-frequency, bounded testbed; geometric baselines include team length, width, centroid distance [17] and pitch-control space creation [18]. Our methodology paper [19] develops and validates the pipeline: decompose by interaction length, then compute scale-wise homology using adaptive thresholds. Across 10 professional matches, SkillCorner, 10 Hz, 104,722 event–topology pairs [19], three connected-cluster regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale regimes emerge: individual-scale loops are near-universal (97.0% ± 1.5%) but short-lived (mean persistence 1.98 m); tactical-scale loops are rarer (19.3% ± 7.2%) but longer-lived (3.80 m). The scales carry largely independent information (ρ = 0.264) and respond coherently to match events (p < 0.001).

3. Advancing Current Understanding and Generating New Knowledge The project builds summary-space results for time-evolving competitive systems (O3) through three advances. (i) Distributional laws: establishing whether stability scores, loop-presence rates and scale complementarity are population-level regularities rather than pilot artefacts, enabling a mean path over such summaries (specifically, convergent moments across matches, permitting Wasserstein-mean estimation). (ii) Comparison geometry: establishing that distances between topological summaries [6,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for change-point statistics. (iii) Functional dynamics: treating each match as a time series of summaries to characterise structural transitions and prove and test the O3 results at season scale. Together they extend statistical topology [6,7,9] to competitive multi-scale systems (O1–O3, §7).

4. Timeliness, Need and Opportunity Timeliness. Three developments have converged: mature multi-scale topology and statistical comparison tools [4,6,7,9]; scalable season-scale computation (§8); and competitive tracking data at population scale. Need. No validated workflow exists for this problem class (§1); sport, and prospectively health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry. Opportunity. Professional football provides a population-scale testbed for a validated workflow transferable to other bounded competitive systems once scales are re-derived.

5. Impact Research impact. The primary mathematical contribution is publishable theory for statistical topology on competitive sequential data (§1, §7, O3). Two results are targeted: well-posedness of a mean path in summary space, extending [7], and a Wasserstein-stability bound for CUSUM. The first extends [7] beyond the exchangeable regime to competitive sequential data; the second gives the first change-point stability bound for landscape-valued time series. Both are instantiated in an open-source library for competitive point-cloud dynamics. This builds UK capability in applied topology, aligned with EPSRC's mathematical sciences and AI/data priorities. Economic and industry impact. Co-developed with Swansea City AFC and StatsBomb, the project translates summaries into practitioner outputs for pressing, formation gaps and defensive-line organisation, unavailable from conventional geometry. Stepping-stone to translation. It prepares a follow-on Standard Grant (§7, O4), building the evidence base for translation beyond football; post-grant pathways include tumour–immune competition with Co-I Powathil and other bounded adversarial systems once scales are re-derived.

6. Benefits and Beneficiaries Mathematicians, sports-analytics researchers and Swansea City AFC analysts benefit immediately from the open-source library and benchmarked features (§5); other bounded competitive multi-agent domains benefit longer-term via the follow-on Standard Grant pathway (§7, O4).

APPROACH

7. Research Design and Objectives Project structure and team. This 12-month project comprises the PI, 0.2 FTE, leading framework development, analysis and publication; two Co-Investigators, 0.25 FTE combined, providing statistical and domain expertise; a Research Associate, Months 2–10, implementing the pipeline and full-season analysis; and Swansea City AFC–StatsBomb partnerships for tracking data and formation labels. Sample-size rationale. A full Championship season (≈540 matches) provides precision and power: ≈32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale loop presence (pilot s.d. 0.072); ≈180 matches per tactical class detect Cohen's d ≥ 0.30 at 80% power, α = 0.05, Benjamini–Hochberg FDR. A borderline pilot within-match effect (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

O1: Population-level topological statistics (PI and RA, Months 1–7). O1 measures how features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match Month 1–2 batch re-validates cutoffs against [19]; stability < 0.80 triggers re-derivation. RA processing Months 2–7; PI-led analysis Months 5–7. Milestones: cutoff gate, Month 2; barcode database, Month 7. O2: Topological fingerprinting (PI, Months 6–9). O2 tests whether formation systems have signatures beyond geometric metrics. StatsBomb and SkillCorner labels are checked using Cohen's κ. Tactical systems are compared using topological-summary distances [6,7] and diagram-image features (§8), benchmarked against length, width and convex-hull area. Success criteria: signatures for ≥3 tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. Milestones: OSF pre-registration, Month 2; fingerprint results, Month 9. O3: Temporal dynamics and structural transitions (PI and RA, Months 4–10). O3 extends single-scale topological change-point detection [14] to competitive, bounded, multi-scale systems (§3, iii). The PI applies FPCA [25], CUSUM [26] and bootstrap calibration [7]. Mathematical targets are well-posedness of a mean path in summary space, extending [7], and a Wasserstein-stability bound for CUSUM. Proof routes are Wasserstein continuity of landscape maps under bootstrap resampling [7] and moment-condition bounds on CUSUM increments [26]. Success criterion: change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05; fallback is direct Wasserstein diagram comparison. Milestones: landscape module, Month 8; O2/O3 outputs, Month 9.

O4: Standard Grant evidence synthesis (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for the follow-on Standard Grant (§5). O1–O3 remain standalone publishable contributions. Milestone: evidence pack, Month 12.

8. Methodology A containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests cutoff transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

9. Feasibility and Risk Management Feasibility. The project is feasible in 12 months: pilot-validated method (§2), modest computation (§8), and an early validation gate. Season-scale processing requires ≈1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12); the team combines applied topology, statistical modelling and football-domain expertise (§11), with RA implementation capacity. Risk management. Data access is resolved: the 2024/25 Championship season is held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium likelihood/impact. Scale transferability: the Month-2 gate re-derives cutoffs if stability falls below 0.80. Formation-label noise: mitigated through dual-source verification, Cohen's κ, unsupervised clustering and pre-registered exclusions. Landscape theory: if sequential landscape development exceeds the timescale, O3 uses direct Wasserstein diagram comparison.

10. Translation to Outcomes and Impact The pipeline will be released as a documented, containerised open-source package via Swansea University's Zenodo community with DOI, including scripts, diagnostics, workflows and feature tables. Publications comprise the methodology paper [19] (target: Journal of Applied and Computational Topology or comparable), arXiv Month 1, submitted Months 1–2; the companion football-analytics paper [22] (Journal of Sports Sciences); and a full-season results paper for Month 11. Practitioner outputs with Swansea City AFC translate summaries into pressing/formation decision-support tools (§5). The Month-12 evidence pack feeds the follow-on Standard Grant (§7, O4).

11. Research Environment The Zienkiewicz Institute supports method development, high-performance analysis and reusable software across computational mathematics, applied topology and sport science. The PI leads the applied-topology framework; Prof Gibin Powathil brings mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff brings sport and exercise science for tactical interpretation; and Swansea City AFC provides a live co-development setting.

12. Facilities, Infrastructure and Host Support Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production, O3 and contingency runs. The containerised pipeline (§8) supports reproducible local and high-performance execution. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and ethics review.
