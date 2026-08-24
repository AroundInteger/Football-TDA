<!--
Vision & Approach — V8.2 (EPSRC R6, second-pass compression)
Derived from VA_V8p1_EPSRC_R6.md; reserve-tier cuts applied to reach 3 A4 pages.

Pass A cuts vs V8.1 (structure/phrasing):
  §1  Importance: "blocking attribution..." tail dropped; scaling-to-season
       sentence fused; Quality: "stability-validated cutoffs" and "pilot-validated
       scale decomposition" clauses merged; "The new contribution is..." welded
       into the next sentence with an em-dash.
  §2  Para 1: stability-theorem clause tightened. Para 2: H1-regimes sentence
       restructured (persistence pair reordered to remove "versus"); "adaptive
       distance threshold" → "adaptive threshold" once, on second mention.
  §3  Opener merged with next sentence to remove signposting; (i)–(iii) trimmed
       (em-dash for precondition; drop "with these in place"; "for the
       change-point statistic" replaces longer clause).
  §5  Research-impact: "These are delivered" → "Both are delivered"; drop
       "validated,". Stepping-stone: two sentences fused with semicolon.
  §7  O1 sentences fused (semicolons); O2 Cohen's κ folded into parenthesis;
       O3 removes duplicated "time series of topological summaries" (already in
       §3); success criterion + fallback fused; O4 sentences fused.
  §8  Package list moved into parenthesis; reproducibility list de-verbed.
  §9  Feasibility opener uses colon; data-access sentence trimmed; drop closing
       "These mitigations preserve publishable outputs..." (self-evident from
       fallbacks above).
  §10 Publication line semicolon-compressed; practitioner sentence tightened.
  §12 Drop duplicated data-provision sentence (already in §7 Team); HPC abbrev.

Pass B further trims (to sit inside 3 A4 pages):
  §1  Opener "yet remain under-modelled as a distinct class..." →
       "yet are not treated as a distinct class..."; Importance final sentence:
       "distinct, stability-validated" → "stability-validated"; "and yield" →
       ", yielding".
  §2  "Statistical tools for classification, distance-based analysis and
       change-point detection [6,7,9]" → "Classification, distance-based analysis
       and change-point tools [6,7,9]"; "developed for cooperative" →
       "built for cooperative".
  §5  "Together these build UK capability in applied topology" →
       "These build UK applied-topology capability"; Co-I Powathil folded into
       parenthesis in the stepping-stone sentence.
  §7  O1: "in Months 1–2" → "(Months 1–2)"; "gating downstream analysis" →
       "gating downstream work"; "with PI-led joint analysis in Months 5–7" →
       "PI-led joint analysis follows Months 5–7".
  §9  Drop ", with the RA providing dedicated implementation capacity"
       (RA already declared in §7 Team). Data-access rewording.
  §10 "not automated prescriptions" dropped (§5 already frames as pathways);
       "target: X or comparable venue" → "X or comparable".
  §12 "validation batches" → "validation".

Pass C micro-trims:
  §5  "on competitive, time-evolving point clouds" → "on competitive point-cloud dynamics".
  §7  O2 success criteria: three-item list → two clauses (FDR into parenthesis).
       O3 success criterion: "change-points agree ... at ≥ 70%" → "≥ 70% agreement";
       fallback prefixed "direct".
  §11 "Professor" → "Prof"; "mathematical oncology and competitive biological-
       systems expertise" → "mathematical-oncology and competitive-biology expertise".

Numbers preserved verbatim:
  0.96 / 0.84 / 1.00; ρ = 0.264; 97.0% ± 1.5%; 19.3% ± 7.2%;
  3.80 / 1.98 m; 104,722; 2.98 / 12.0 / 30.0 m; p = 0.051; 32; 180; 540; 1,600; 5,000.

UK English. Vancouver [n] citations preserved.
-->

# VISION

## 1. Quality and Mathematical Importance

This research develops a mathematical framework extending multi-scale topological analysis to competitive collective systems: agents that coordinate internally while competing against an adversary within a bounded domain. Such systems arise in autonomous-vehicle fleets, tumour–immune dynamics and team sports, yet are not treated as a distinct class of dynamical systems. Their defining feature is adversarial geometry: unlike cooperative swarms, competing subgroups deform each other's configurations across multiple scales.

**Importance.** No existing method attributes topological structure, connected clusters (H₀) and enclosing loops (H₁), to the distinct interaction scales of hierarchical, high-frequency competitive systems. Standard persistent homology [1–3] uses a single distance threshold across all agents, collapsing these scales into a single summary. Multi-parameter topology [4,5] offers a theoretical route to scale-specific structure but remains computationally prohibitive at real-world, high-frequency scale. This project closes that gap: pilot analysis in professional football has identified stability-validated interaction scales (§2), and Championship-season scaling will test whether these persist as population-level structure, yielding a framework transferable to other bounded competitive systems once scales are re-derived (§5).

**Quality.** The project combines mathematical rigour and empirical validation: stability-validated cutoffs and adaptive distance thresholds define groups by empirically tested interaction lengths rather than arbitrary values, making the procedure falsifiable and reproducible (§2). The contribution is theoretical as well as empirical — moving from static scale detection to time-evolving summaries requires two results not currently available: well-posedness of a mean path in summary space under competitive, non-exchangeable sequential data, extending [7]; and a stability bound for the CUSUM statistic under Wasserstein perturbation. This project establishes both and tests their empirical utility at season scale (§7, O3).

## 2. Background Building on Previous Work

Persistent homology [1,2], with its stability theorem [8] ensuring that small tracking errors induce only small summary changes, provides the mathematical basis suited to real measurement data. Classification, distance-based analysis and change-point tools [6,7,9] form the basis for O2–O3. Standard applications use a single global scale [3] or multi-scale clustering built for cooperative, slowly evolving systems [10]; this project instead decomposes competitive systems by validated interaction length before computing homology at each scale. Topology has captured collective organisation across aggregation, motion and flocking [11–13], motivating the interaction-length framing. Existing topological change-point methods for multi-agent systems [14] are single-scale; O3 extends them to competitive, bounded, multi-scale systems. Football provides the testbed: competitive, high-frequency, spatially bounded, and supported by established geometric baselines [17,18].

Our methodology paper [19] develops and validates the pipeline: decompose by validated interaction length, then compute homology at each scale with an adaptive threshold. Across 10 professional matches (SkillCorner, 10 Hz; 104,722 event–topology pairs) [19], three cluster-scale (H₀) regimes reproduce: individual 2.98 m, tactical 12.0 m and team 30.0 m, with cross-epoch stability 0.96, 0.84 and 1.00. Two loop-scale (H₁) regimes emerge: individual-scale loops appear in 97.0% ± 1.5% of frames but are short-lived (mean persistence 1.98 m), while tactical-scale loops are rarer (19.3% ± 7.2%) yet longer-lived (3.80 m). The scales carry largely independent information (ρ = 0.264) and respond coherently to match events (p < 0.001).

## 3. Advancing Current Understanding and Generating New Knowledge

Building on pilot reproducibility and event coherence (§2), the project develops summary-space results for time-evolving competitive systems (O3) via three advances that make those results well-posed and testable. (i) *Distributional laws:* establishing whether stability scores, loop-presence rates and scale complementarity are population-level regularities — the precondition for defining a mean path over such summaries. (ii) *Comparison geometry:* establishing that distances between topological summaries [6,9] distinguish formation systems, yielding a topological definition of formation identity and the metric structure for the change-point statistic. (iii) *Functional dynamics:* each match then becomes a time series of topological summaries, allowing structural transitions to be characterised and the O3 results proved and tested at season scale. Together these extend statistical topology [6,7,9] into competitive, multi-scale, hierarchical systems, mapping onto O1–O3 (§7).

## 4. Timeliness, Need and Opportunity

**Timeliness.** Three developments have converged: multi-scale topology and statistical comparison tools have matured [4,6,7,9]; scalable computation now makes season-scale frame-wise topology feasible (§8); and competitive tracking data have become available at the resolution needed to test population-level structure.

**Need.** No validated workflow exists for this problem class (§1); analysts in sport, and prospectively in health, logistics and autonomous coordination, need interpretable structural measures capturing organisation, gaps, loops and transitions beyond conventional geometry.

**Opportunity.** Professional football provides an ideal population-scale testbed for a validated workflow transferable to other bounded competitive systems once interaction scales are re-derived.

## 5. Impact

**Research impact.** The primary contribution to the mathematical sciences is theoretical: two new results for statistical topology on competitive sequential data — well-posedness of a mean path in summary space, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation (§1, §7, O3). Both are delivered as publishable proofs and instantiated in an open-source library for multi-scale persistent homology on competitive point-cloud dynamics. These build UK applied-topology capability, contributing to EPSRC's physical and mathematical sciences powerhouse and AI, digitisation and data priorities.

**Economic and industry impact.** Co-developed with Swansea City AFC and StatsBomb, the project translates topological summaries into practitioner-interpretable tools for pressing structures, formation gaps and defensive-line organisation — quantities not captured by length, width or convex-hull area.

**Stepping-stone to translation.** The project prepares a follow-on Standard Grant (§7, O4) by establishing the season-scale evidence base needed to transfer the framework beyond football; pathways (not deliverables) include tumour–immune competition (Co-I Powathil) and other bounded adversarial systems once scales are re-derived.

## 6. Benefits and Beneficiaries

Mathematicians, data scientists, Swansea City AFC analysts and the wider sports-analytics community are the immediate beneficiaries of the library, visualisations and benchmarked features described in §5. Longer term, other bounded competitive multi-agent domains benefit from the transferable validation procedure and follow-on Standard Grant pathway (§7, O4).

# APPROACH

## 7. Research Design and Objectives

**Team.** PI (0.2 FTE — framework, oversight, publication); two Co-Investigators (0.25 FTE combined — statistical and domain expertise); Research Associate (1.0 FTE, Months 2–10 — pipeline and full-season analysis). Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb agreement. The project has three research objectives and one strategic output.

**Sample-size rationale.** A full Championship season (≈540 matches) delivers precision and power: 32 matches per stratum give a 95% CI half-width of 0.025 for tactical-scale H₁ presence (pilot s.d. 0.072); 180 matches per tactical class detect Cohen's *d* ≥ 0.30 at power 0.80 and α = 0.05, with Benjamini–Hochberg FDR correction. A borderline pilot within-match effect on tactical H₁ persistence (permutation p = 0.051; pilot half-level random-effects fit) motivates season-scale replication.

**O1: Population-level topological statistics** (PI and RA, Months 1–7). O1 measures how topological features vary across the season and relate to tactical descriptors. Month 1 establishes the Supercomputing Wales pipeline; a 20-match batch (Months 1–2) re-validates cutoffs against [19], with stability < 0.80 triggering re-derivation and gating downstream work. RA processing runs Months 2–7; PI-led joint analysis follows Months 5–7. *Milestones:* cutoff gate, Month 2; barcode database, Month 7.

**O2: Topological fingerprinting** (PI, Months 6–9). O2 tests whether formation systems have topological signatures beyond geometric metrics. Formation labels come from StatsBomb and SkillCorner (Cohen's κ for agreement). Tactical systems are compared via distances between averaged topological summaries [6,7] and vectorised diagram-image features (§8), benchmarked against length, width and convex-hull area. *Success criteria:* distinguishable signatures for ≥ 3 tactical configurations (FDR-corrected p < 0.05), with added information beyond geometric baselines. *Milestones:* OSF pre-registration, Month 2; fingerprint results, Month 9.

**O3: Temporal dynamics and structural transitions** (PI and RA, Months 4–10). O3 extends single-scale multi-agent change-point detection [14] to competitive, bounded, multi-scale systems. The PI applies FPCA [25] and CUSUM change-point detection [26] to per-match summary time series, with bootstrap calibration [7]. Mathematical targets are well-posedness of a mean path in summary space, extending [7], and a stability bound for the CUSUM statistic under Wasserstein perturbation. *Success criterion:* ≥ 70% agreement with held-out tactical annotations (permutation p < 0.05); if landscape development exceeds the timescale, direct Wasserstein diagram comparison is the fallback. *Milestones:* landscape module, Month 8; O2/O3 outputs, Month 9.

**O4: Standard Grant evidence synthesis** (PI, Months 9–12). From Month 9 the PI compiles full-season results into a reproducible evidence pack for a follow-on Standard Grant translating the framework to higher-impact adversarial systems (§5); O1–O3 remain standalone publishable contributions. *Milestone:* evidence pack, Month 12.

## 8. Methodology

A containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) processes each frame as a point cloud: clustering at empirically derived interaction lengths, homology with adaptive thresholds, and storage of barcodes and vectorised summaries. Frame-level homology takes under 2 seconds and is embarrassingly parallel, enabling 1 Hz production processing on Supercomputing Wales (§12). The Month 1–2 gate (§7) tests whether pilot cutoffs transfer to Championship data and whether 1 Hz sampling preserves high-resolution features. O1 summarises H₀/H₁ cluster and loop statistics; O2 compares landscape distances, diagram-image features and geometric baselines; O3 applies FPCA, CUSUM and bootstrap calibration to topological time series. Reproducibility: containerisation, OSF pre-registration, DOI-archived code, diagnostics and documented scripts.

## 9. Feasibility and Risk Management

**Feasibility.** The project is feasible within 12 months: the core method is pilot-validated (§2), computation is modest (§8), and the workplan contains an early validation gate. Season-scale processing needs ~1,600 CPU-hours of the 5,000 core-hour Supercomputing Wales allocation (§12). The team combines applied topology, statistical modelling and football-domain expertise (§11).

**Risk management.** Data access is resolved: 2024/25 Championship data are already held through the Swansea City AFC–StatsBomb agreement. Three residual risks are all medium-likelihood/medium-impact. *Scale transferability:* the Month-2 gate re-derives cutoffs if stability falls below 0.80. *Formation-label noise:* mitigated through dual-source verification, Cohen's κ, unsupervised clustering and a pre-registered exclusion protocol. *Landscape theory:* if sequential landscape development exceeds the project timescale, O3 uses direct Wasserstein diagram comparison.

## 10. Translation to Outcomes and Impact

The pipeline releases as a containerised open-source package via Swansea University's Zenodo community with a DOI (scripts, diagnostics, workflows, feature tables). Three publications: methodology paper [19] — arXiv Month 1, journal submission (*Journal of Applied and Computational Topology* or comparable) Months 1–2; football-analytics companion [22] to *Journal of Sports Sciences*; full-season results paper Month 11. Practitioner outputs with Swansea City AFC translate these into pressing/formation decision-support tools (§5). The Month-12 evidence pack supports the follow-on Standard Grant (§7, O4).

## 11. Research Environment

The Zienkiewicz Institute supports method development, high-performance analysis and reusable software. The PI leads the applied-topology framework and season-scale analysis; Prof Gibin Powathil provides mathematical-oncology and competitive-biology expertise (future health pathway, §5); Prof Liam Kilduff provides sport and exercise science for tactical interpretation and practitioner outputs; Swansea City AFC provides a live co-development setting.

## 12. Facilities, Infrastructure and Host Support

Full-season processing (§9) uses the PI's Supercomputing Wales allocation for validation, production runs, O3 analysis and contingency re-processing. The containerised pipeline (§8) ensures reproducible execution across local and HPC environments. Swansea University provides host support through the Zienkiewicz Institute, Research Office and partnership infrastructure, including data governance and fast-tracked ethics review for the future in-domain extensions in §5.
