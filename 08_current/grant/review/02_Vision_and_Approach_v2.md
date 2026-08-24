# VISION AND APPROACH

<!-- 3-page limit: 11pt Arial (or equivalent sans serif), 2 cm margins, single spaced.
     Word count: ~1,870 words (body) + Gantt table — fits within limit.
     References use author–year here for readability; final numbered citations
     follow the compiled LaTeX (unsrtnat / Vancouver order of appearance).
     Canonical numbers (locked 2026-06-26):
       stability scores: 0.88 (individual), 0.97 (tactical), 1.00 (team)
       primary-match H1 presence: 96.0% individual (144/150), 12.0% tactical (18/150)
       multi-match H1 presence: 97.0% ± 1.5% individual, 19.3% ± 7.2% tactical
       Spearman ρ = 0.254, 95% bootstrap CI [0.200, 0.314]
       event–topology pairs: 104,722 across 10 matches -->

---

## VISION

**Quality and Mathematical Importance**

This research develops new mathematical frameworks for multi-scale topological analysis of competitive collective systems. The mathematical question of how multi-scale spatial organisation emerges from local interactions recurs across active matter physics, collective animal behaviour, and network science, where ring-like and higher-order structures appear at scale-dependent interaction radii (Marchetti et al., 2013; Ballerini et al., 2008; Giusti et al., 2016). These systems are usually summarised by geometric and kinematic descriptors that capture motion but not the loop and enclosure structure that coordination produces; persistent homology measures that structure rigorously and is now mature in biology and materials science (Topaz et al., 2015; Bhaskar et al., 2019; Hiraoka et al., 2016). Applied to multi-agent systems, however, persistent homology has operated at single scales, in cooperative or static settings, or on small samples, and none combines domain-validated scale decomposition and adaptive filtration on competitive, hierarchical, high-frequency tracking validated at population scale.

Standard single-parameter persistent homology applied to a competitive multi-agent point cloud conflates topological features from all organisational levels into a single persistence diagram, making scale-specific attribution impractical. The TDA community has begun addressing hierarchical decomposition: Schindler and Barahona (2023) develop multiscale clustering tools for persistent homology, but in cooperative, quasi-static settings; multiparameter persistence theory (Botnan and Lesnick, 2022) provides algebraic machinery for simultaneous multi-scale analysis but faces computational barriers at the point-cloud scales relevant here. Our framework takes a complementary, domain-informed route: hierarchical clustering at validated cutoff distances decomposes the competitive point cloud by organisational level before single-parameter persistent homology is computed at each level. A second step — adaptive filtration — ensures the Vietoris–Rips threshold is appropriate for the post-clustering geometry at each scale. The mathematical contribution lies in (i) systematic, empirically validated scale identification, replacing heuristic filtration choices; (ii) adaptive filtration ensuring consistent H₁ loop detection across all scales; and (iii) persistence landscape theory for competitive sequential diagrams, enabling rigorous detection of topological regime transitions.

The framework is not domain-specific. Any bounded competitive multi-agent system with a domain-interpretable hierarchy of interaction scales admits the same clustering–adaptive filtration–homology construction once cutoffs are validated. Professional football is an ideal testbed: high-frequency tracking data (10–25 Hz), a well-structured competitive system, a domain-interpretable hierarchy (individual players ↔ tactical units ↔ team), and detailed event annotations. Football provides the data density to calibrate and validate the pipeline rigorously; the framework, by design, transfers to other domains.

**Validated Foundation**

Validation across 10 professional football matches (SkillCorner open broadcast tracking; 10 Hz; 1,500 uniformly sampled frames; 104,722 event–topology pairs) establishes three H₀ analysis regimes — individual (2.98 m), tactical (12.0 m), team (30.0 m) — with cross-epoch stability scores of 0.88, 0.97, and 1.00 respectively. Two complementary H₁ regimes are confirmed: individual-scale loops are near-universal (97.0% ± 1.5% frame presence across 10 matches) and transient; tactical-scale loops are rarer (19.3% ± 7.2%) but geometrically persistent. In the primary validation match, individual-scale presence is 96.0% (144/150 frames) and tactical-scale presence is 12.0% (18/150 frames), both within one standard deviation of the multi-match mean. Scale complementarity is quantified: Spearman ρ = 0.254 (95% bootstrap CI [0.200, 0.314]), confirming that neither scale subsumes the other. Real event correlation across all 10 matches confirms that topological features respond coherently to match dynamics — disruption events decrease persistence, organisational events increase it (p < 0.001 for both) — providing construct validity for the framework. The preliminary work is fully reproducible: all tracking data are from the SkillCorner public repository; the Python implementation is released open-source alongside journal submission.

This work is available as an ArXiv preprint (Brown et al., 2026) with journal submission to the *Journal of Applied and Computational Topology* (JACT) in Month 1 of this project.

**What This Proposal Adds**

The preprint establishes *that* scale-specific barcodes exist and are reproducible across 10 independent matches. This proposal asks *what they tell us at scale*, extending from a proof of concept to three mathematically distinct directions: (i) *distributional questions* — population-level laws of variation for H₀/H₁ barcodes and landscape norms over a full Championship season (~540 matches); (ii) *comparison geometry* in persistence space — distances between persistence landscapes to treat tactical systems as distinguishable subsets of landscape space, enabling topological fingerprinting; (iii) *functional dynamics* — time-indexed landscapes characterising stability regimes and transitions within matches. None of (i)–(iii) is demonstrated at championship scale in the preprint.

**Excellence and Importance**

Topological Data Analysis has proven effective for characterising the shape of complex data, but existing applications examine systems at single scales, in non-competitive scenarios, or with static data. A standard Vietoris–Rips filtration on a multi-agent point cloud conflates topological features from different organisational levels. This project advances computational topology through two methodological contributions: domain-informed hierarchical clustering to decompose point clouds by organisational level, and adaptive filtration ensuring consistent H₁ detection across all scales — a practical necessity, since a fixed Vietoris–Rips threshold appropriate at one level produces null results at another.

**Timeliness**

This research addresses foundational open questions in computational topology for hierarchical, time-evolving systems. Three new theoretical and methodological contributions are developed: (1) persistence landscape methods for temporal dynamics, characterising stability regimes and regime shifts within and across matches; (2) comparison geometry in persistence space, enabling topological fingerprinting — discriminating between tactical systems via landscape distances; (3) empirical distributional theory on topological invariants at championship scale, supporting hypothesis tests against match-level covariates. The Botnan and Lesnick (2022) survey signals theoretical maturity in multiparameter persistence; practical validated workflows for domain-informed decomposition remain underdeveloped. A full Championship season now provides, for the first time, a dataset large enough to establish population-level topological statistics — a scale more typical of physics or materials science than applied topology. Computational advances in TDA libraries (Ripser, GUDHI) now make full-season multi-scale analysis feasible.

**Beneficiaries**

Direct beneficiaries are the computational topology community (validated multi-scale workflows, open-source Python library) and sports analytics practitioners (interpretable formation metrics grounded in rigorous mathematics). Indirect beneficiaries include operators of any bounded competitive multi-agent system with tracking data: the domain-validated scale-identification approach transfers wherever empirically identifiable characteristic length scales exist, including autonomous vehicle platoon coordination, competitive crowd management at transport hubs, and ecological predator–prey monitoring. Preliminary cross-domain application to armed conflict event data (Brown et al., in preparation) provides a Standard Grant pathway to these broader domains.

---

## APPROACH

**Project Structure and Team**

This 12-month project involves: (i) the Principal Investigator (PI, 0.2 FTE), responsible for framework development, analysis oversight, and publication; (ii) two Co-Investigators (combined 0.25 FTE) contributing statistical expertise and domain knowledge; (iii) a Research Associate (1.0 FTE, 9 months, Months 2–10), responsible for data pipeline implementation, full-season analysis, and landscape methods development; (iv) partnership with Swansea City AFC and StatsBomb, providing secured access to Championship tracking data and formation labels. The project is structured around four integrated Objectives (three research objectives plus one strategic output).

**Delivering the Objectives**

*Objective 1 — Full-Season Analysis (Months 1–7).* Scale the validated pipeline to the full Championship season (~540 matches), establishing population-level H₀ and H₁ distributions and cross-match variance. PI establishes the concurrent processing pipeline on Supercomputing Wales (Months 1–2); RA executes full-season analysis (Months 3–7). Success criteria: >500 matches processed; population-level H₀ and H₁ distributions established; exploratory joint analysis with match-level tactical descriptors positioning barcode statistics relative to established metrics.

*Objective 2 — Topological Fingerprinting (Months 4–8).* Develop Fréchet mean barcodes and inter-diagram distances in persistence space distinguishing formation classes. A pre-registered analysis plan (OSF, Month 2) fixes formation labelling, metric choices, and statistical thresholds before the full-season run. Persistence diagrams are compared using a persistence-image kernel for vectorised classification and a landscape L² distance for continuous contrasts. Success criteria: topological signatures for ≥3 tactical configurations; inter-system differences with Benjamini–Hochberg FDR correction (p < 0.05); non-redundancy confirmed by ANCOVA after adjusting for standard geometric descriptors (team length, width, convex-hull area).

*Objective 3 — Persistence Landscape Dynamics (Months 6–10).* Implement persistence landscape representations (Bubenik, 2015) for temporal evolution at both analysis scales. Within-match paths t ↦ λ_δ(t) are summarised by functional PCA; regime transitions are detected by CUSUM change-point procedures on landscape L²-norm increments, with bootstrap calibration (Chazal et al., 2014). Success criteria: reproducible stability-regime segmentation (≥70% frame-level agreement across random sub-samples); change-point alignment with tactical annotation above chance (permutation p < 0.05).

*Objective 4 — Standard Grant Preparation (Months 9–12).* Synthesise full-season results, landscape theory, and fingerprinting evidence into a Standard Grant application. The Standard Grant will extend the validated framework to broader competitive systems — cross-domain application begins separately with the conflict-data paper (Brown et al., in preparation). Standard Grant preparation begins in Month 9, incorporating full-season results for submission within 12 months of project completion.

**Methodology**

The established pipeline (Brown et al., 2026) operates through six stages: (1) point cloud construction from 22-player positions; (2) hierarchical clustering at validated cutoffs (individual 2.98 m, tactical 12.0 m, team 30.0 m); (3) adaptive filtration using ε_max = max(P₇₅(d_ij), max(5.0, 2δ)); (4) persistent homology via Ripser (H₀ and H₁); (5) closed cycle identification through geometric realisation of H₁ generators; (6) statistical analysis (Wilcoxon rank-sum, permutation tests, Spearman correlation, FDR correction). New methods developed in this grant: persistence landscape computation from diagrams at each scale; landscape distance metrics for temporal window comparison; hierarchical clustering in persistence space for tactical system classification; concurrent processing pipeline for full-season execution.

**Feasibility and Risk**

At <2 s per frame, the full H₁ sweep over ~540 matches requires approximately 1,100 CPU-days; the Supercomputing Wales allocation at this scale is within the PI's current standing access and is embarrassingly parallel by match. The full pipeline is implemented, tested, and documented in Python; all computational groundwork is complete. Primary risks and mitigations: (i) *Formation-label noise* — mitigated by parallel unsupervised clustering and inter-rater reliability (Cohen's κ) computed before any downstream tests; (ii) *Scale-drift across leagues* — mitigated by a Month 2 validation gate re-running the Brown et al. (2026) cutoff-sweep analysis on the first 20 Championship matches before the full-season run; (iii) *RA recruitment* — mitigated by early advertising (Month −2), competitive salary, and cross-disciplinary project scope. A pre-registered power analysis is deposited on OSF at Month 2.

**Maximising Translation**

Paper 1 (Brown et al., 2026) is on ArXiv, with journal submission to JACT in Month 1. Paper 3 (full-season results and persistence landscapes) targets submission in Month 11, with JACT as the primary target. Open-source code release (containerised with Apptainer/Docker, pinned dependency versions) at Month 12. Industry impact through quarterly meetings with championship club partners. Standard Grant preparation (Months 9–12) incorporates full-season results and cross-domain evidence.

**Research Environment**

Swansea University provides Supercomputing Wales (2 Petaflops), secure GDPR-compliant data storage (100 TB), fast-tracked ethics approval (4-week turnaround), and a dedicated Impact Officer. Championship broadcast data is secured through the Swansea City AFC–StatsBomb agreement; GPS data pathways remain open via Genius Sports UK and Borussia Dortmund. The project is delivered by a Research Associate (1.0 FTE, Months 2–10) supervised by PI Dr Rowan Brown, with Co-Investigators Professor Liam Kilduff (Sport and Exercise Sciences) and Professor Gibin Powathil (Mathematics) providing domain expertise and mathematical rigour.

**Project Timeline**

| Activity | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Pipeline validation & RA onboarding | ■ | | | | | | | | | | | |
| OSF pre-registration (O2) | | ■ | | | | | | | | | | |
| Full-season computation (O1) | | | ■ | ■ | ■ | ■ | ■ | | | | | |
| **D1:** Full-season barcode database | | | | | | | ■ | | | | | |
| Topological fingerprinting (O2) | | | | ■ | ■ | ■ | ■ | ■ | | | | |
| Landscape dynamics methods (O3) | | | | | | ■ | ■ | ■ | ■ | ■ | | |
| **D2:** Landscape library + fingerprint results | | | | | | | | | ■ | | | |
| Publications and dissemination | | | | | | | | | | | ■ | ■ |
| Standard Grant preparation (O4) | | | | | | | | | ■ | ■ | ■ | |
| **D3:** Standard Grant evidence pack | | | | | | | | | | | | ■ |
