# Vision and Approach — EPSRC criteria structure (V4.2, trimmed)

<!-- Version: V4.2 — trims V4.1 toward the 3-page Vision+Approach limit.
     Cuts applied (see chat discussion for full rationale):
     (1) Removed cross-section duplication: the multiparameter-persistence
     gap (was in both §1 and §2), the Ripser/GUDHI/giotto-tda tool list
     (was in both §4 and §8, now only in §8), the Standard Grant/O4
     narrative (was told in full in both §5 and §7, now full version only
     in §5), the Month-2 cutoff-gate mechanics (was described in §7, §8,
     §9 Feasibility and the §9 risk table; now described once in §7 and
     referenced elsewhere), and the transferability-to-other-domains claim
     (was in §1, §5 and §6; now full version only in §5).
     (2) Compressed §2's numeric results paragraph and §7's objective
     descriptions to headline figures/actions only — full statistics
     remain in ../full/02_Vision_and_Approach.md and the methodology
     paper [19].
     (3) Cut §7's transitional summary paragraph (duplicated §3's framing
     and the O1–O3 descriptions immediately following it).
     (4) Cut two further "framing" sentences carrying no citation/fact
     of their own — §2's "On these foundations we have produced two
     companion outputs" (transition already signalled by the pivot to
     "Our methodology paper..."), and §5's "The primary impact is to
     the mathematical sciences:" (already signalled by the subheading;
     remaining clause reworded into a standalone sentence). Left
     deliberately alone: §1's Quality-paragraph lead-in (primes the
     reviewer against the named EPSRC sub-qualities); §9's "The project
     is feasible within 12 months" (claim-before-evidence, lower stakes
     either way).
     (5) §2's opening "four decades..." sentence was reconsidered and
     cut after all — but as a set, not in isolation: the dependent
     "second foundation"/"third foundation" ordinal labels in the two
     paragraphs after it were also removed/reworded (now plain topic
     sentences: "Topology also demonstrably captures..." / "Football
     spatiotemporal analysis..."), so nothing is left dangling.
     (6) §3's closing sentence rewritten from a vague "none of this has
     been done" claim (checked against the literature — it isn't fully
     true: population-level topological statistics, landscape-distance
     classification and functional change-point detection all have
     precedent in other domains, per Bubenik [6]/Chazal [7]/Adams [9])
     to a precise, defensible claim: this machinery hasn't yet reached
     competitive, multi-scale, hierarchical systems. No new citations
     added — reuses [6,7,9] already established in §2.
     (7) O3 (§7) now explicitly distinguishes itself from Gu et al. [14]
     (single-scale, multi-agent) as "competitive, bounded, multi-scale,"
     cross-referencing §2 rather than re-explaining.
     (8) §1's opening paragraph rewritten: "new mathematical frameworks" (plural,
     overclaims invention) → "a mathematical framework extending..." (matches
     §2/§3's "combine and extend already-cited machinery" framing); split
     into two sentences (definition separated from examples); example list
     tightened from four to three — "opposing crowd flows" and "predator–prey
     populations" dropped (unsupported anywhere else in the document),
     replaced with tumour–immune competition (which now threads through to
     §5's named follow-on target and §11's Co-I justification). The
     "several interaction scales" claim was also hedged: "is continuously
     deformed... across several" → "can be deformed... across multiple,"
     with the mechanism (added degrees of freedom from adversarial coupling)
     stated with confidence and the multi-scale claim stated as a structural
     possibility rather than an observed universal — since only football
     (§2, 10-match pilot) has actually been shown to have several validated
     scales; other named domains are illustrative, not yet tested.
     (9) Full-document coherence check after (8): all cross-references
     (§1↔§2, §1↔§5, §2↔§7 O3, §3↔§7, §5↔§6/§7 O4/§10/§11, §7↔§8/§9,
     §9↔§7/§8/§11/§12) still resolve to sections that exist and carry the
     content being pointed to; no citation first-appearance order disrupted
     by these specific edits (all reused numbers were already introduced
     earlier in document order); "framework" used consistently as singular
     throughout (§1, §7 Project Structure); tumour–immune competition now
     appears consistently as an illustrative/future-target example (§1,
     §5, §11), never implied as current-grant research (that remains
     football only).
     (10) Importance and Quality paragraphs reworked together: merged a
     redundant pair of "no method exists" sentences into one, restored
     the "point-cloud sizes and frame rates" specificity that an earlier
     trim had blurred into an ambiguous second sense of "scale," hedged
     "the scales at which competitive systems organise" to "can exhibit"
     (consistency with §1's opening paragraph hedge), and gave Importance's
     closing sentence an actual evidentiary basis — pilot analysis already
     finds distinct scales (§2), on a small sample, ahead of the
     population-scale test — rather than asserting the population-scale
     test as a leap of faith. In Quality, reordered so "rigour,
     reproducibility, concreteness" are each paired with their evidence
     (concreteness was previously asserted but never cashed out), and
     corrected an overclaim spotted by cross-checking §7/§9: the
     landscape-dynamics/change-point piece is NOT pilot-validated (§9's
     risk table treats it as needing further development under a
     Wasserstein fallback) — only the interaction-length decomposition
     and adaptive filtration are. Quality now separates "already proven"
     from "this project's new contribution" accordingly.
     Word count sections 1–12 body: ~1,800 (was ~2,824) — a 36% cut.
     At the document's own original ratio (~2,824 words = 5.5 pages,
     i.e. ~510 words/page), this is ~3.5 pages: close to the 3-page
     target but likely not quite there. Closing the remaining gap needs
     a further, more judgement-heavy pass rather than more line-editing
     — remaining prose is fairly tight. NOT yet page-verified — compile
     the twin submission/tex in Overleaf and confirm Vision+Approach
     fits 3 pages before submission.

     CITATION NUMBERS — cuts do not reorder citations, but first-appearance
     order may have shifted slightly. Re-check [n] labels against the
     compiled LaTeX bibliography before pasting into JeS.

     Canonical numbers: ../CANONICAL_NUMBERS.md
     Long-form detail: ../full/02_Vision_and_Approach.md
     Prior version (pre-trim): VA_V4_EPSRC_structure.md -->

---

**VISION**

**1. Excellent Quality and Importance**

This research develops a mathematical framework extending multi-scale topological analysis to *competitive collective systems* — an important but under-modelled class in applied mathematics. Such systems comprise agents that coordinate internally while opposing an adversary within a bounded domain: autonomous-vehicle fleets, tumour–immune competition, team sports. Unlike cooperative swarms, competitive systems exhibit *adversarial geometry*: the added degrees of freedom from adversarial coupling mean each subgroup's configuration can be deformed by its opponent across multiple interaction scales.

**Importance.** No existing method attributes topological structure — connected clusters (H₀) and enclosing loops (H₁) — to the distinct interaction scales competitive systems can exhibit, on hierarchical, high-frequency data. Standard single-parameter persistent homology [1,2] merges all agents into one diagram, losing scale-specific attribution. Multiparameter persistence [4,5] would resolve this in principle, but remains computationally impractical at the point-cloud sizes and frame rates this project requires. This project closes that gap in professional football: pilot analysis already finds distinct, stability-validated interaction scales (§2), though so far only across a handful of matches, and scaling this to a full Championship season tests whether the finding holds as a population-level property (transferable beyond football, §5).

**Quality.** The contribution rests on rigour, reproducibility and concreteness. Rigour and reproducibility follow from *stability-validated* cutoffs: the point-cloud decomposition is set by empirically validated interaction length rather than heuristic choice, making it falsifiable rather than ad hoc. Concreteness follows from validation: the interaction-length decomposition and adaptive-filtration pipeline are already validated at pilot scale (§2), not merely proposed; the landscape-dynamics extension [6,7] for change-point detection is the new contribution this project builds and tests (§7, O3). Three contributions advance prior work: (i) domain-validated scale identification in place of heuristic filtration choices; (ii) adaptive filtration for consistent multi-scale H₁ detection; (iii) landscape dynamics enabling change-point detection of topological phase transitions.

**2. Background — Building on Previous Work**

Persistent homology [1,2] and its stability theorem [8] — bounded measurement error perturbs a persistence diagram only boundedly — licenses applying topology to noisy tracking data. We build on persistence landscapes [6] and their stochastic convergence [7], underwriting our bootstrap confidence intervals, and on stable diagram vectorisations [9] for classification. Cluster-then-homology methods [10] operate only in cooperative, quasi-static settings; our domain-validated decomposition by interaction length is the tractable route this work motivates but does not yet provide.

Topology also demonstrably captures collective organisation: biological aggregation [11], collective motion [12], and the finding that flocking interactions are governed by topological rather than metric distance [13] — which motivates our interaction-length framing. Gu et al. [14] detect topological change points in multi-agent systems, but at a single scale; O3 extends this to competitive, bounded, multi-scale systems (§7). Football spatiotemporal analysis [15,16] and its established shape descriptors [17,18] furnish both a testbed and the baselines any new topological feature must exceed.

Our methodology paper (*Journal of Applied and Computational Topology* [19]) develops the measurement-aware, multi-scale pipeline — decomposition at validated cutoffs followed by adaptive Vietoris–Rips filtration — validated across 10 professional matches (SkillCorner tracking, 10 Hz; 104,722 event–topology pairs [20,21]). Three H₀ regimes reproduce across all matches — individual, tactical, team — with cross-epoch stability 0.96, 0.84, 1.00; two H₁ regimes emerge, scale non-redundancy confirmed. Features respond coherently to match dynamics (*p* < 0.001), match-specifically rather than universally. A companion paper [22] applies the pipeline to practitioner interpretation and motivates §3's fingerprinting question. Pilot data are public and the pipeline will be open-source on submission — the proof of concept this project advances to population scale.

**3. Advancing Current Understanding and Generating New Knowledge**

Section 2 establishes, at pilot scale, that scale-specific barcodes exist, are reproducible, and respond coherently to match events. The open question is what holds at *population* scale, in three directions. **(i) Distributional laws:** across a full Championship season (~540 matches), do stability scores, H₁ presence rates and complementarity behave as population-level regularities, or vary systematically with tactical context? **(ii) Comparison geometry:** do landscape [6] and image [9] distances render tactical systems distinguishable, giving a topologically grounded definition of formation identity? **(iii) Functional dynamics:** treating each match as a path *t* ↦ λ_δ(*t*), what within-match stability regimes and transitions can be characterised? Each direction extends already-cited statistical TDA machinery [6,7,9] into a setting it has not yet reached: competitive, multi-scale, hierarchical systems. Establishing them here maps directly onto Objectives O1–O3 (§7).

**4. Timeliness, Need and Opportunity**

**Timeliness.** Three developments have recently converged: the mathematics has matured (multiparameter persistence has reached survey-level consolidation [4]; statistical TDA now supports population-level inference); computational tooling makes per-frame homology tractable at season scale (§8), enabling but not constituting the contribution; and season-scale competitive tracking data have only recently become accessible.

**Need.** No validated workflow yet exists for multi-scale persistent homology on competitive, hierarchical, high-frequency systems. Analysts in sports — and, prospectively, health and economic sectors — need interpretable structural metrics that conventional geometric descriptors do not provide.

**Opportunity.** Their simultaneous arrival opens a window to settle these questions now, making the project timely rather than merely feasible.

**5. Impact**

**Impact on research and the discipline.** A validated, reproducible workflow and open-source library for multi-scale persistent homology on competitive, time-evolving point clouds contributes to EPSRC's *physical and mathematical sciences powerhouse* priority and, as a systems approach to competitive dynamics, to *AI, digitisation and data* — building UK capability in an emerging area of applied topology.

**Economic and industry impact.** Developed with Swansea City AFC and data partners (StatsBomb, Genius Sports), the project translates topological measures into practitioner-interpretable tools for UK sports analytics, quantifying team-structure aspects conventional descriptors miss (§6), and builds durable academia–industry collaboration routes.

**Longer-term reach.** This project is a stepping-stone to a follow-on Standard Grant (§7, O4). The domain-validation procedure transfers to any bounded competitive multi-agent system once its scales are re-derived — natural next targets are tumour–immune competition (health; Co-I Powathil's expertise) and competitive logistics/autonomous-fleet coordination (economic/security). These are pathways, not deliverables: the football-validated workflow and evidence base make that larger programme fundable.

**6. Benefits and Beneficiaries**

**Direct beneficiaries:** the mathematical sciences community, via a validated open-source library for multi-scale homology on competitive point clouds; sports analytics practitioners — notably Swansea City AFC performance analysts as co-development partner — who gain practitioner-interpretable visualisations of pressing structures, formation gaps and defensive-line organisation that standard geometric descriptors (length, width, convex-hull area) do not directly quantify; and the wider sports analytics research community.

**Longer-term beneficiaries:** operators of other competitive multi-agent domains (§5); the proposed Standard Grant programme (§7, O4), for which this project provides the evidence base; and industry users adopting the open-source pipeline.

---

**APPROACH**

**7. Research Design and Objectives**

**Project Structure and Team.** This 12-month project involves: (i) the PI (0.2 FTE), framework development, analysis oversight, publication; (ii) two Co-Investigators (0.25 FTE combined), statistical and domain expertise; (iii) a Research Associate (1.0 FTE, 9 months, M2–10), pipeline implementation, full-season analysis, landscape library development; (iv) partnership with Swansea City AFC and StatsBomb (Championship tracking data, formation labels). Four integrated objectives are pursued (three research, one strategic output).

**Sample-size rationale.** A full Championship season (~540 matches) supports subgroup inference: n ≈ 32 per stratum gives a 95% CI half-width of 0.025 on tactical-scale H₁ presence, and n ≈ 180 per tactical class detects Cohen's *d* ≥ 0.30 at power 0.80 (BH-FDR correction). A pilot mixed-model estimate of the within-match half-effect on tactical-scale H₁ persistence (*p* = 0.051 [19]) is borderline, consistent with match-specific dynamics; season-scale replication resolves this.

**Objectives.**

**O1 — Population-level topological statistics** (PI and RA, M1–7): Scale the validated pipeline [19] to a full season, relating features to tactical descriptors. PI establishes the Supercomputing Wales pipeline (M1); a 20-match batch (M1–2) re-validates cutoffs — stability below 0.80 triggers re-derivation. RA processes the full season (M2–7); PI conducts exploratory analysis (M5–7). *Milestone: cutoff gate (M2); barcode database (M7).*

**O2 — Topological fingerprinting** (PI, M6–9): Can formation systems be distinguished by topological signature? Formation labels from StatsBomb and SkillCorner (inter-rater κ checked first); hypotheses pre-registered on OSF (M2). Success criteria: distinct signatures for ≥3 configurations, significant between-system differences (*p* < 0.05, BH-corrected), adding information beyond team length, width and convex-hull area, via L² landscape distance and diagram-image features (§8). *Milestone: OSF registration (M2); results (M9).*

**O3 — Temporal dynamics and phase transitions** (PI and RA, M4–10): Extending single-scale multi-agent change-point detection [14] to competitive, bounded, multi-scale systems (§2) — does within-match evolution of topological structure align with tactical events? RA implements landscape tracking for paths *t* ↦ λ_δ(*t*) (M6–10); PI applies functional PCA [25] and CUSUM change-point detection [26] with bootstrap calibration [7], targeting Fréchet-mean well-posedness and a Wasserstein stability bound for CUSUM. Success criterion: change-points align with tactical annotations at ≥70% agreement (*p* < 0.05); Wasserstein comparison is the fallback. *Milestone: landscape module (M8); O2/O3 outputs (M9).*

**O4 — Standard Grant evidence synthesis** (PI, M9–12): From M9, compile full-season results into an evidence base for a separate follow-on application translating the framework to health and economic-sector systems (§5). O1–O3 are standalone publishable contributions independent of this output. *Milestone: evidence pack (M12).*

**8. Methodology**

The containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) computes homology in under 2 s per frame, processing tracking data through clustering, adaptive filtration and barcode computation, then persistence comparisons (diagram-image features, L² landscape distance, ANCOVA baselines). The Month 1–2 gate confirms cutoff transferability and 1 Hz production fidelity before full-season commitment. Infrastructure and data-access arrangements are detailed in §12.

**9. Feasibility and Risk Management**

**Feasibility.** The project is feasible within 12 months. Computation is modest and embarrassingly parallel — about 1,600 CPU-hours within a 5,000 core-hour allocation (§12). The schedule is de-risked by the Month-2 gate (§7, §8), and the team holds the required topological, statistical and domain expertise (§11).

**Risk management.**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data access | Low | High | StatsBomb agreement confirmed for 2024/25; ~270-match contingency remains publishable for O1 (O2 exploratory only) |
| Scale transferability | Medium | Medium | Month 2 gate re-derives cutoffs on Championship data |
| Formation-label noise | Medium | Medium | Dual-source verification, unsupervised landscape clustering, pre-registered exclusion protocol |
| Landscape theory | Medium | Medium | Wasserstein fallback preserves O3 if extension requires development |

**10. Translation to Outcomes and Impact**

Open-source code is archived via Swansea University's Zenodo community (DOI). The methodology paper [19] is submitted to ArXiv and JACT from Month 1; the football-analytics paper [22] targets *Journal of Sports Sciences*; a full-season results and landscapes paper targets Month 11. Practitioner-facing outputs with Swansea City AFC and the follow-on Standard Grant (§7, O4) are detailed in §5.

**11. Research Environment**

Swansea University's Zienkiewicz Institute provides the research environment. Co-I Professor Gibin Powathil brings mathematical-oncology expertise, the foundation for the planned health-sector translation (§5), and Professor Liam Kilduff (sport and exercise sciences) provides tactical domain expertise. The Swansea City AFC partnership provides sustained access for co-development of practitioner outputs.

**12. Facilities, Infrastructure and Host Support**

Full-season processing requires ~1,600 CPU-hours; the Supercomputing Wales allocation (5,000 core-hours; PI's existing access) covers processing, gate batches and O3 computation with margin. Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb agreement. Swansea University's Research Office supports partnership negotiation and provides fast-tracked ethics review.

---
