<!--
Vision & Approach — V8.1 (EPSRC R6, compressed)
Derived from VA_V8_EPSRC_R6.md; Tier-1 + Tier-2 word cuts applied.

Cuts applied vs V8:
  Tier 1 (highest-value / lowest-risk):
    C1  §5  Deleted last sentence of "Stepping-stone" para (duplicated first sentence).
    C2  §9  Factored "medium likelihood, medium impact" out of three risk lines.
    C3  §7  Team block: prose → labelled list.
    C4  §7  Sample-size: three sentences → one semicoloned sentence.
  Tier 2:
    C5  §1  Standard-PH sentence simplified; Quality-paragraph openers merged.
    C6  §2  Geometric-baseline citation compressed; flocking list trimmed; "However" removed.
    C7  §8  Opening two sentences merged.
    C8  §10 Publication line semicolons tightened.
    C9  §11 Dropped opening sentence (duplicated §12); role sentences tightened.

No content dropped. No claims changed. All numbers preserved:
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 2.98 / 12.0 / 30.0 m; p = 0.051.

UK English. Vancouver [n] citations preserved.
-->

# VISION

## 1. Quality and Mathematical Importance

This research develops a mathematical framework extending multi-scale topological analysis to competitive collective systems: agents that coordinate internally while competing against an adversary within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports, yet remain under-modelled as a distinct class of dynamical systems. Their defining feature is adversarial geometry: unlike cooperative swarms, adversarial interactions allow each subgroup's configuration to be deformed across multiple scales.

**Importance.** No existing method attributes topological structure, connected clusters (H₀) and enclosing loops (H₁), to the distinct interaction scales of hierarchical, high-frequency competitive systems. Standard persistent homology [1–3] uses a single distance threshold across all agents, collapsing these scales into one summary and blocking attribution to distinct organisational levels. Although multi-parameter topology [4,5] offers a theoretical route to scale-specific structure, current methods remain computationally prohibitive for real-world, high-frequency competitive data. This project closes that gap in professional football: pilot analysis has identified distinct, stability-validated interaction scales (§2). Scaling to a full Championship season will test whether these scales persist as population-level structure and establish a transferable framework once characteristic scales are re-derived in other bounded competitive systems (§5).

**Quality.** The project combines mathematical rigour and empirical validation: stability-validated cutoffs define groups by empirically tested interaction lengths rather than arbitrary thresholds, and pilot-validated scale decomposition with adaptive distance thresholds (§2) make the procedure falsifiable and reproducible. The new contribution is theoretical as well as empirical. Moving from static scale detection to time-evolving summaries requires two results not currently available: well-posedness of a mean path in summary space under competitive, non-exchangeable sequential data, extending [7]; and a stability bound for the CUSUM statistic under Wasserstein perturbation. This project establishes both results and tests their empirical utility at season scale (§7, O3).

## 2. Background Building on Previous Work

Persistent homology [1,2], supported by its stability theorem [8], provides the mathematical basis: small tracking errors induce only small changes in topological summaries, suiting real measurement data. Statistical tools for classification, distance-based analysis and change-point detection [6,7,9] form the basis for O2–O3. Standard applications use a single global scale [3] or rely on multi-scale clustering developed for cooperative, slowly evolving systems [10]. This project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation in aggregation, motion and flocking [11–13], motivating the interaction-length framing. Existing topological change-point methods for multi-agent systems [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the testbed: competitive, high-frequency, spatially bounded, and supported by established geometric baselines [17,18].

Our methodology paper [19] develops and validates the pipeline: decompose by validated interaction length, then compute homology at each scale using an adaptive distance threshold. Across 10 professional matches, SkillCorner, 10 Hz, 104,722 event–topology pairs [19], three cluster-scale (H₀) regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale (H₁) regimes emerge: individual-scale loops are near-universal but short-lived, 97.0% ± 1.5% of frames, while tactical-scale loops are rarer but more persistent, 19.3% ± 7.2%, mean persistence 3.80 m versus 1.98 m. The scales carry largely independent information, ρ = 0.264, and respond coherently to match events, p < 0.001.

## 3. Advancing Current Understanding and Generating New Knowledge

Pilot data (§2) show these summaries are reproducible and respond coherently to match events. The project builds toward summary-space results for time-evolving competitive systems (O3), via three advances that make those results well-posed and testable. (i) Distributional laws: establishing whether stability scores, loop-presence rates and scale complementarity are population-level regularities rather than pilot artefacts, the precondition for defining a mean path over such summaries. (ii) Comparison geometry: establishing that distances between topological summaries [6,9] distinguish formation systems, yielding both a topological definition of formation identity and the metric structure on which the change-point statistic operates. (iii) Functional dynamics: with these in place, each match becomes a time series of topological summaries, allowing structural transitions to be characterised and the O3 results proved and tested at season scale. Together these extend statistical topology [6,7,9] into competitive, multi-scale, hierarchical systems, mapping onto O1–O3 (§7).

## 4. Timeliness, Need and Opportunity

**Timeliness.** Three developments have converged: multi-scale topology and statistical comparison tools have matured [4,6,7,9]; scalable computation now makes season-scale frame-wise topology feasible (§8); and competitive tracking data have become available at the resolution needed to test population-level structure.

**Need.** No validated workflow exists for this problem class (§1); analysts in sport, and prospectively in health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry.

**Opportunity.** Professional football provides an ideal population-scale testbed for a validated workflow transferable to other bounded competitive systems once interaction scales are re-derived.

## 5. Impact

**Research impact.** The primary contribution to the mathematical sciences is theoretical: two new results for statistical topology on competitive sequential data (§1, §7, O3) — well-posedness of a mean path in summary space, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation. These are delivered as publishable proofs and instantiated in a validated, open-source library for multi-scale persistent homology on competitive, time-evolving point clouds. Together these build UK capability in applied topology, contributing to EPSRC's physical and mathematical sciences powerhouse and AI, digitisation and data priorities.

**Economic and industry impact.** Co-developed with Swansea City AFC and StatsBomb, the project translates topological summaries into practitioner-interpretable tools for pressing structures, formation gaps and defensive-line organisation, quantities not directly captured by length, width or convex-hull area.

**Stepping-stone to translation.** The project prepares a follow-on Standard Grant (§7, O4) by establishing the season-scale evidence base needed to transfer the framework beyond football. Pathways, not deliverables, include tumour–immune competition with Co-I Powathil and other bounded adversarial systems once interaction scales are re-derived.

## 6. Benefits and Beneficiaries

Mathematicians, data scientists, Swansea City AFC analysts and the wider sports-analytics community are the immediate beneficiaries of the library, visualisations and benchmarked features described in §5. Longer term, other bounded competitive multi-agent domains benefit from the transferable validation procedure and follow-on Standard Grant pathway (§7, O4).

# APPROACH

## 7. Research Design and Objectives

**Team.** PI (0.2 FTE — framework, oversight, publication); two Co-Investigators (0.25 FTE combined — statistical and domain expertise); Research Associate (1.0 FTE, Months 2–10 — pipeline and full-season analysis). Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb agreement. The project has three research objectives and one strategic output.

**Sample-size rationale.** A full Championship season (≈540 matches) delivers precision and power: 32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale H₁ presence (pilot s.d. 0.072); 180 matches per tactical class detect Cohen's *d* ≥ 0.30 at power 0.80 and α = 0.05, with Benjamini–Hochberg FDR correction. A borderline pilot within-match effect on tactical H₁ persistence (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

**O1: Population-level topological statistics** (PI and RA, Months 1–7). O1 asks how topological features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline. A 20-match batch in Months 1–2 re-validates interaction-length cutoffs against [19]; stability below 0.80 triggers re-derivation and gates downstream analysis. RA processing runs Months 2–7, with PI-led joint analysis in Months 5–7. *Milestones:* cutoff gate, Month 2; barcode database, Month 7.

**O2: Topological fingerprinting** (PI, Months 6–9). O2 tests whether formation systems have topological signatures beyond geometric metrics. Formation labels come from StatsBomb and SkillCorner; Cohen's κ checks agreement. Tactical systems are compared using distances between averaged topological summaries [6,7] and vectorised diagram-image features (§8), benchmarked against length, width and convex-hull area. *Success criteria:* distinguishable signatures for at least three tactical configurations; FDR-corrected differences, p < 0.05; and added information beyond geometric baselines. *Milestones:* OSF pre-registration, Month 2; fingerprint results, Month 9.

**O3: Temporal dynamics and structural transitions** (PI and RA, Months 4–10). O3 extends single-scale multi-agent change-point detection [14] to competitive, bounded, multi-scale systems. Each match is represented as a time series of topological summaries. The PI applies FPCA [25] and CUSUM change-point detection [26], with bootstrap calibration [7]. Mathematical targets are well-posedness of a mean path in summary space under competitive sequential data, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation. *Success criterion:* change-points agree with held-out tactical annotations at ≥70%, permutation p < 0.05. If landscape development exceeds the timescale, Wasserstein diagram comparison is the fallback. *Milestones:* landscape module, Month 8; O2/O3 outputs, Month 9.

**O4: Standard Grant evidence synthesis** (PI, Months 9–12). From Month 9, the PI compiles full-season results into a reproducible evidence pack for a separate follow-on Standard Grant translating the framework to higher-impact adversarial systems (§5). O1–O3 remain standalone publishable contributions. *Milestone:* evidence pack, Month 12.

## 8. Methodology

A containerised Python pipeline built around Ripser [23], GUDHI and giotto-tda [24] processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology computation using adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests whether pilot-derived cutoffs transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises H₀/H₁ cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility is ensured through containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

## 9. Feasibility and Risk Management

**Feasibility.** The project is feasible within 12 months because the core method is pilot-validated (§2), computation is modest (§8), and the workplan contains an early validation gate. Season-scale processing requires approximately 1,600 CPU-hours within the 5,000 core-hour Supercomputing Wales allocation (§12). The team combines applied topology, statistical modelling and football-domain expertise (§11), with the RA providing dedicated implementation capacity.

**Risk management.** Data access is resolved: the 2024/25 Championship season is archived and already held through the Swansea City AFC–StatsBomb agreement, removing data access as a live risk. Three residual risks are all medium-likelihood/medium-impact. *Scale transferability:* the Month-2 gate re-derives cutoffs if stability falls below 0.80. *Formation-label noise:* mitigated through dual-source verification, Cohen's κ, unsupervised clustering and a pre-registered exclusion protocol. *Landscape theory:* if sequential landscape development exceeds the project timescale, O3 uses direct Wasserstein diagram comparison. These mitigations preserve publishable outputs under realistic contingencies.

## 10. Translation to Outcomes and Impact

The pipeline will be released as a containerised open-source package via Swansea University's Zenodo community with a DOI (scripts, diagnostics, example workflows and derived feature tables). Three publications: the methodology paper [19] — arXiv in Month 1, journal submission (target: *Journal of Applied and Computational Topology*, or comparable venue) in Months 1–2; the football-analytics companion [22], targeting the *Journal of Sports Sciences*; and a full-season results paper targeted for Month 11. Practitioner outputs co-developed with Swansea City AFC will translate these into pressing/formation decision-support tools (§5), not automated tactical prescriptions. The Month-12 evidence pack supports the follow-on Standard Grant (§7, O4).

## 11. Research Environment

The Zienkiewicz Institute supports method development, high-performance analysis and reusable software. The PI leads the applied-topology framework and season-scale analysis; Professor Gibin Powathil brings mathematical oncology and competitive biological-systems expertise (future health pathway, §5); Professor Liam Kilduff brings sport and exercise science for tactical interpretation and practitioner outputs; Swansea City AFC provides a live co-development setting.

## 12. Facilities, Infrastructure and Host Support

Full-season processing (§9) draws on the PI's Supercomputing Wales allocation, covering validation batches, production runs, O3 analysis and contingency re-processing. Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb agreement. The containerised pipeline (§8) ensures reproducible execution across local and high-performance environments. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and fast-tracked ethics review for the future in-domain extensions in §5.
