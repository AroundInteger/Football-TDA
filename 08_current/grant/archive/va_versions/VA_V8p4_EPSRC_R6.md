<!--
Vision & Approach — V8.4 (EPSRC R6)
Derived from VA_V8p3_EPSRC_R6.md, applying Priority-1 restorations and
Priority-2 fixes flagged in critical review of V8.3. Layout preserved (flat
paragraphs, no `##` headers) to protect V8.3's 3-page fit.

Priority-1 restorations (content that had been over-compressed in V8.3):
  §5  Research impact: named theorems restored — well-posedness of a mean path
       in summary space, extending [7]; Wasserstein-stability bound for CUSUM.
       (Kept in §1 Quality and §7 O3 as before.) Split into three short
       sentences per user request (em-dash aside removed for readability).
  §5  Stepping-stone: "post-grant pathways" hedge restored on translation
       targets, so tumour–immune competition does not read as an in-project
       deliverable.
  §10 Publications: target journal names restored — Journal of Applied and
       Computational Topology (or comparable) for [19]; Journal of Sports
       Sciences for [22].

Priority-2 fixes:
  §3  (iii): "establish O3 results" → "prove and test the O3 results" (§7 O3
       promises mathematical proofs, so "establish" was too soft).
  §7  Sample-size: subject–verb agreement ("gives" → "give"; "detects" →
       "detect"); "FDR correction" → "Benjamini–Hochberg FDR correction";
       "(permutation p = 0.051; pilot half-level random-effects fit)"
       restored so p = 0.051 is not confused with a published [19] figure.
  §7  O2: "at least three configurations" → "at least three tactical
       configurations"; "beyond baselines" → "beyond geometric baselines"
       for consistency.
  §7  O3: "single-scale change-point detection [14]" → "single-scale
       topological change-point detection [14]" (matches §2 phrasing).
  §9  Risk labels: factored "Three residual risks are all medium likelihood/
       impact." out to a shared lead-in; inline per-risk labels removed for
       consistency.
  §11 CoI expertise labels restored — "Prof Gibin Powathil brings
       mathematical-oncology and competitive-biology expertise"; "Prof Liam
       Kilduff brings sport and exercise science for tactical interpretation".

Priority-3 (zero-word) tweaks also applied:
  §4  "prospectively" hedge restored so Need for health/logistics/autonomous
       coordination is not stated as live now.
  §6  "numerical library" → "open-source library" (persistence/topology
       library, not a numerical-analysis library).
  §7  O1: "O1 tests how features vary" → "O1 measures how features vary"
       (O1 is descriptive, not hypothesis-testing).

Word count envelope: V8.3 = 1761 words (fitted "just about" to 3 pp).
V8.4 gross additions from P1+P2+small-P3 ≈ +60. To protect V8.3's 3-page fit,
four offsets applied in-file:

  Applied A: §11 opener "Swansea University provides the required environment
      through computational mathematics, applied topology, sport science and
      external partnership." folded into the Zienkiewicz-Institute sentence:
      "The Zienkiewicz Institute supports method development, high-performance
      analysis and reusable software across computational mathematics, applied
      topology and sport science."                       saves ≈ 8 words
  Applied B: §12 duplicated data-provision line "Championship tracking data
      and formation labels are secured through the Swansea City AFC–StatsBomb
      agreement." dropped (verbatim in §7 Team block).   saves ≈ 14 words
  Applied C: §8 opener restored to V8.2's tighter form (V8.3 had expanded it
      +12 words with no content change): "A containerised Python pipeline
      (Ripser [23], GUDHI, giotto-tda [24]) processes each frame as a point
      cloud: clustering at ..., homology with adaptive thresholds, and
      storage of barcodes and vectorised summaries."     saves ≈ 12 words
  Applied D: §10 "posted to arXiv in Month 1 and submitted in Months 1–2" →
      "arXiv Month 1, submitted Months 1–2".             saves ≈ 4 words
  Applied E: §5 "for competitive, time-evolving point clouds" →
      "for competitive point-cloud dynamics".            saves ≈ 2 words

Reserve trims (f) and (g) applied. Additional 80-word trim pass then applied
to bring V8.4 back to V8.3's word budget (user reported +80 over limit at
1786; V8.4 target 1706):

  §1  Opener "This research develops a mathematical framework extending
       multi-scale topological analysis" → "This research extends multi-scale
       topological analysis".                             ≈ −5 words
  §1  "adversarial interactions allow each subgroup's configuration to be
       deformed" → "competing subgroups deform each other's configurations".
                                                         ≈ −5 words
  §1  Quality closer: "This project establishes both and tests their empirical
       utility at season scale (§7, O3)." → "Both are established and tested
       at season scale (§7, O3)."                        ≈ −3 words
  §2  H1-regimes sentence re-cast with parenthesised numbers (persistence
       pair reordered short-lived / longer-lived); rho / p in parentheses.
                                                         ≈ −5 words
  §3  "mapping onto O1–O3 (§7)" → "(O1–O3, §7)".         ≈ −3 words
  §7  Team block: drop "The project has three research objectives and one
       strategic output." (immediate O1–O4 headings do the scoping).
                                                         ≈ −9 words
  §7  Sample-size: "approximately 32" → "≈32"; "approximately 180" → "≈180";
       "using pilot s.d. 0.072" → "(pilot s.d. 0.072)".
                                                         ≈ −3 words
  §7  Team block: "a 9-month Research Associate, Months 2–10" →
       "a Research Associate, Months 2–10" (9-month redundant with dates).
                                                         ≈ −1 word
  §7  O1: "RA processing runs Months 2–7, with PI-led analysis in Months
       5–7." → "RA processing Months 2–7; PI-led analysis Months 5–7."
                                                         ≈ −3 words
  §7  O1: "with stability below 0.80 triggering re-derivation" →
       "stability < 0.80 triggers re-derivation".        ≈ −1 word
  §7  O2: "signatures for at least three tactical configurations" →
       "signatures for ≥3 tactical configurations".      ≈ −2 words
  §7  O3: drop "by representing each match as a time series of topological
       summaries" (already in §3, iii); replaced with cross-ref "(§3, iii)".
                                                         ≈ −12 words
  §7  O4: "for a separate follow-on Standard Grant translating the framework
       to higher-impact adversarial systems (§5)" → "for the follow-on
       Standard Grant (§5)" (§5 already carries the translation description).
                                                         ≈ −10 words
  §9  Feasibility opener: colon-restructure — "The project is feasible in
       12 months: pilot-validated method (§2), modest computation (§8), and
       an early validation gate."                        ≈ −8 words
  §9  Two-sentence merge: "…(§12). The team combines…" → "…(§12); the team
       combines…"                                        ≈ 0 words
  §9  Data-access: "archived and held" → "held".         ≈ −1 word
  §9  Drop closing "These mitigations preserve publishable outputs." (each
       risk row already carries its fallback).           ≈ −5 words
  §10 Drop "not automated tactical prescriptions" tail on practitioner
       outputs (already framed as pathways, not products, in §5).
                                                         ≈ −4 words
  §10 "supports the follow-on Standard Grant" → "feeds the follow-on Standard
       Grant" (marginally shorter; also less passive).   ≈ −1 word
  §11 Reserve (g) applied: "Professor" → "Prof" (×2).    ≈ −2 words
  §12 Processing list: "validation batches, production runs, O3 analysis and
       contingency re-processing" → "validation, production, O3 and
       contingency runs".                                ≈ −4 words
  §5  "instantiated in a validated, open-source library" →
       "instantiated in an open-source library" (drop "validated,").
                                                         ≈ −2 words
  §5  "not directly captured by" → "unavailable from".   ≈ −3 words

Numbers preserved verbatim (identical to V8.3):
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 2.98 / 12.0 / 30.0 m; p = 0.051; 32; 180; 540;
  1,600; 5,000.

UK English. Vancouver [n] citations preserved.
-->

VISION

1. Quality and Mathematical Importance This research extends multi-scale topological analysis to competitive collective systems: agents that coordinate internally while competing against an adversary within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports, yet remain under-modelled as a distinct class of dynamical systems. Their defining feature is adversarial geometry: unlike cooperative swarms, competing subgroups deform each other's configurations across multiple scales. Importance. No existing method attributes connected-cluster and loop structure to the distinct interaction scales of hierarchical, high-frequency competitive systems. Standard persistent homology [1,2], applied with a single threshold across all agents [3], collapses these scales into one summary, preventing features from being linked to individual-, group- or system-level organisation. Multi-parameter topology [4,5] offers a theoretical route to scale-specific structure, but remains computationally prohibitive for real-world, high-frequency competitive data. This project closes that gap in professional football: pilot analysis has identified stability-validated interaction scales (§2), and a full Championship season will test whether they persist as population-level structure and establish a transferable framework once characteristic scales are re-derived elsewhere (§5). Quality. The project combines mathematical rigour with empirical validation. Stability-validated cutoffs define groups by empirically tested interaction lengths rather than arbitrary thresholds, making the procedure falsifiable. Scale decomposition and adaptive distance thresholds are already validated at pilot scale (§2). The new contribution is theoretical as well as empirical: moving from static scale detection to time-evolving summaries requires well-posedness of a mean path in summary space under competitive, non-exchangeable sequential data, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation. Both are established and tested at season scale (§7, O3).

2. Background Building on Previous Work Persistent homology [1,2] and its stability theorem [8] provide the mathematical basis: small tracking errors induce only small changes in topological summaries. Statistical tools compare persistence summaries for classification, distance-based analysis and change-point detection [6,7,9], forming the basis for O2–O3. Standard applications either use a single global scale [3] or multi-scale clustering developed for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in biological aggregation, collective motion and nearest-neighbour-governed flocking [11–13], motivating this interaction-length framing. Existing topological change-point methods [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the high-frequency, spatially bounded testbed with geometric baselines including team length, width, centroid distance [17] and pitch-control space creation [18]. Our methodology paper [19] develops and validates the pipeline: decompose by validated interaction length, then compute scale-wise homology using adaptive thresholds. Across 10 professional matches, SkillCorner, 10 Hz, 104,722 event–topology pairs [19], three connected-cluster regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale regimes emerge: individual-scale loops are near-universal (97.0% ± 1.5%) but short-lived (mean persistence 1.98 m); tactical-scale loops are rarer (19.3% ± 7.2%) but longer-lived (3.80 m). The scales carry largely independent information (ρ = 0.264) and respond coherently to match events (p < 0.001).

3. Advancing Current Understanding and Generating New Knowledge Pilot data (§2) show these summaries are reproducible and event-responsive. The project builds summary-space results for time-evolving competitive systems (O3) through three advances. (i) Distributional laws: establishing whether stability scores, loop-presence rates and scale complementarity are population-level regularities rather than pilot artefacts, enabling a mean path over such summaries. (ii) Comparison geometry: establishing that distances between topological summaries [6,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for change-point statistics. (iii) Functional dynamics: treating each match as a time series of summaries to characterise structural transitions and prove and test the O3 results at season scale. Together these extend statistical topology [6,7,9] into competitive, multi-scale, hierarchical systems (O1–O3, §7).

4. Timeliness, Need and Opportunity Timeliness. Three developments have converged: mature multi-scale topology and statistical comparison tools [4,6,7,9]; scalable season-scale frame-wise computation (§8); and competitive tracking data at population-level resolution. Need. No validated workflow exists for this problem class (§1); sport, and prospectively health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry. Opportunity. Professional football provides an ideal population-scale testbed for a validated workflow transferable to other bounded competitive systems once interaction scales are re-derived.

5. Impact Research impact. The primary contribution to the mathematical sciences is publishable theory for statistical topology on competitive sequential data (§1, §7, O3). Two results are targeted: well-posedness of a mean path in summary space, extending [7], and a Wasserstein-stability bound for CUSUM. Both are instantiated in an open-source library for competitive point-cloud dynamics. This builds UK capability in applied topology, contributing to EPSRC's physical and mathematical sciences powerhouse and AI, digitisation and data priorities. Economic and industry impact. Co-developed with Swansea City AFC and StatsBomb, the project translates summaries into practitioner-interpretable tools for pressing structures, formation gaps and defensive-line organisation, unavailable from length, width or convex-hull area. Stepping-stone to translation. It prepares a follow-on Standard Grant (§7, O4) by providing the evidence base to transfer the framework beyond football; post-grant pathways include tumour–immune competition with Co-I Powathil and other bounded adversarial systems once scales are re-derived.

6. Benefits and Beneficiaries Mathematicians, data scientists, Swansea City AFC analysts and the wider sports-analytics community benefit immediately from the open-source library, visualisations and benchmarked features (§5). Longer term, other bounded competitive multi-agent domains benefit from the transferable validation procedure and follow-on Standard Grant pathway (§7, O4).

APPROACH

7. Research Design and Objectives Project structure and team. This 12-month project comprises the PI, 0.2 FTE, leading framework development, analysis and publication; two Co-Investigators, 0.25 FTE combined, providing statistical and domain expertise; a Research Associate, Months 2–10, implementing the pipeline and full-season analysis; and Swansea City AFC–StatsBomb partnerships for tracking data and formation labels. Sample-size rationale. A full Championship season, approximately 540 matches, provides precision and power: ≈32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale loop presence (pilot s.d. 0.072); ≈180 matches per tactical class detect Cohen's d ≥ 0.30 at power 0.80 and α = 0.05 with Benjamini–Hochberg FDR correction. A borderline pilot within-match effect (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

O1: Population-level topological statistics (PI and RA, Months 1–7). O1 measures how features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match Month 1–2 batch re-validates cutoffs against [19]; stability < 0.80 triggers re-derivation. RA processing Months 2–7; PI-led analysis Months 5–7. Milestones: cutoff gate, Month 2; barcode database, Month 7. O2: Topological fingerprinting (PI, Months 6–9). O2 tests whether formation systems have signatures beyond geometric metrics. StatsBomb and SkillCorner labels are checked using Cohen's κ. Tactical systems are compared using topological-summary distances [6,7] and diagram-image features (§8), benchmarked against length, width and convex-hull area. Success criteria: signatures for ≥3 tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. Milestones: OSF pre-registration, Month 2; fingerprint results, Month 9. O3: Temporal dynamics and structural transitions (PI and RA, Months 4–10). O3 extends single-scale topological change-point detection [14] to competitive, bounded, multi-scale systems (§3, iii). The PI applies FPCA [25], CUSUM [26] and bootstrap calibration [7]. Mathematical targets are well-posedness of a mean path in summary space, extending [7], and a Wasserstein-stability bound for CUSUM. Success criterion: change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05; fallback is direct Wasserstein diagram comparison. Milestones: landscape module, Month 8; O2/O3 outputs, Month 9.

O4: Standard Grant evidence synthesis (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for the follow-on Standard Grant (§5). O1–O3 remain standalone publishable contributions. Milestone: evidence pack, Month 12.

8. Methodology A containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests cutoff transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

9. Feasibility and Risk Management Feasibility. The project is feasible in 12 months: pilot-validated method (§2), modest computation (§8), and an early validation gate. Season-scale processing requires approximately 1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12); the team combines applied topology, statistical modelling and football-domain expertise (§11), with RA implementation capacity. Risk management. Data access is resolved: the 2024/25 Championship season is held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium likelihood/impact. Scale transferability: the Month-2 gate re-derives cutoffs if stability falls below 0.80. Formation-label noise: mitigated through dual-source verification, Cohen's κ, unsupervised clustering and pre-registered exclusions. Landscape theory: if sequential landscape development exceeds the timescale, O3 uses direct Wasserstein diagram comparison.

10. Translation to Outcomes and Impact The pipeline will be released as a documented, containerised open-source package via Swansea University's Zenodo community with DOI, including scripts, diagnostics, workflows and feature tables. Publications comprise the methodology paper [19] (target: Journal of Applied and Computational Topology or comparable), arXiv Month 1, submitted Months 1–2; the companion football-analytics paper [22] (Journal of Sports Sciences); and a full-season results paper targeted for Month 11. Practitioner outputs with Swansea City AFC translate summaries into pressing/formation decision-support tools (§5). The Month-12 evidence pack feeds the follow-on Standard Grant (§7, O4).

11. Research Environment The Zienkiewicz Institute supports method development, high-performance analysis and reusable software across computational mathematics, applied topology and sport science. The PI leads the applied-topology framework; Prof Gibin Powathil brings mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff brings sport and exercise science for tactical interpretation; and Swansea City AFC provides a live co-development setting.

12. Facilities, Infrastructure and Host Support Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production, O3 and contingency runs. The containerised pipeline (§8) supports reproducible local and high-performance execution. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and ethics review.
