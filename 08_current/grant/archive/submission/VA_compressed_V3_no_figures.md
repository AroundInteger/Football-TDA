# Vision and Approach — compressed submission (no figures)

<!-- Target: ≤3 pages, Calibri 11 pt, 2 cm margins, 3 pt paragraph spacing (JeS paste).
     Version: V3.5 — H₀/H₁ introduced at first PH mention.
     PAGE-VERIFIED: exactly 3 pages at V3.0 — re-verify in Word after V3.1 edits.
     Submission master: use this file for JeS Vision & Approach paste.
     Pair document: VA_compressed_V3.md (with figures — shorter body text).
     Canonical numbers: ../CANONICAL_NUMBERS.md
     Long-form detail: ../full/02_Vision_and_Approach.md
     Approx. word count (body): ~1,650 words + Gantt table (3 pt paragraph spacing) -->

---

**VISION**

**Mathematical Importance and Quality.** This research develops new mathematical frameworks for the multi-scale topological analysis of competitive collective systems. These systems, comprising agents that coordinate internally while actively opposing an adversary within a bounded domain, represent an important yet under-modelled class in applied mathematics. Coordination in such systems is organised across multiple scales simultaneously — individual agents, coordinated sub-groups, and system-wide organisation — rather than at a single level. What further distinguishes them from cooperative swarms is their *adversarial geometry*: each group's spatial configuration is continuously deformed by the opposition, potentially generating distinct topological structure at more than one scale. Professional football serves as the primary validation testbed for these frameworks (detailed below), where multi-scale topological structure can correspond to individual, tactical, and team organisational levels.

Persistent homology [1,2] quantifies loops and enclosure in multi-agent configurations rigorously: the parameters H₀ and H₁ record the numbers of connected clusters and loops, respectively. A single Vietoris–Rips filtration [3] on the full competitive point cloud (all 22 players jointly), however, merges individual, tactical, and team features into one persistence diagram, so features cannot be attributed to each organisational level. Prior work addresses parts of this gap: cooperative biological aggregation [4]; multiscale cluster-then-homology methods in quasi-static settings [5]; Gu et al. [6] track topological change points in multi-agent snapshots at a single analysis scale. Multiparameter persistence [7,8] permits simultaneous scale analysis in principle but remains computationally impractical at the point-cloud sizes and frame rates required here.

Our framework takes a complementary, domain-informed route. Hierarchical clustering at empirically validated cutoffs decomposes the competitive point cloud by organisational level; single-parameter homology is then computed at each level separately. Adaptive filtration ensures consistent H₁ detection on the post-clustering geometry at each scale.

The project builds on two methodological pillars: (i) domain-informed decomposition and (ii) adaptive filtration — and extends both with persistence landscape dynamics for competitive sequential diagrams. Stability-validated cutoffs make the decomposition falsifiable and transferable across competitive systems. Three mathematical contributions extend prior work:

- **Domain-validated scale identification:** a systematic cutoff sweep identifies three H₀ regimes (individual 2.98 m, tactical 12.0 m, team 30.0 m) with cross-epoch stability scores 0.96, 0.84, and 1.00 [12], replacing heuristic filtration choices with a reproducible, domain-grounded procedure.
- **Adaptive filtration for multi-scale H₁ detection:** a data-informed maximum filtration adjusts to post-clustering geometry at each scale (75th percentile of inter-centroid distances, with a floor tied to validated cutoff δ); ablation confirms H₁ outputs are insensitive to the percentile choice within this formula [9].
- **Persistence landscape dynamics [10,11]:** at each validated scale δ, each frame's persistence barcode is summarised as a landscape λ_δ; tracked through the match, these form the time-indexed path *t* ↦ λ_δ(*t*), enabling CUSUM change-point detection of topological phase transitions [18].

Together these constitute a practical advance in computational topology: validated multi-scale persistent homology on hierarchical, competitive, time-evolving point clouds.

**What This Proposal Adds.** The preprint [12] establishes that scale-specific barcodes exist and are reproducible across 10 independent matches. This proposal asks what they tell us at population scale: (i) distributional laws of H₀/H₁ barcodes and landscape norms over a full Championship season (~540 matches); (ii) comparison geometry in persistence space — landscape distances that treat tactical systems as distinguishable subsets, enabling topological fingerprinting; (iii) functional dynamics of the landscape paths *t* ↦ λ_δ(*t*), characterising stability regimes and transitions within matches. None of (i)–(iii) is demonstrated at championship scale in the preprint.

**Preliminary Validation.** The framework is validated across 10 professional football matches (SkillCorner open broadcast tracking, 10 Hz; 104,722 event–topology pairs) [12] — an ideal testbed with high-frequency spatial measurements and established positional standards [13,14]. Two H₁ regimes emerge: individual-scale loops are near-universal and transient (97.0% ± 1.5% frame presence; 95.3%, 143/150 frames in the primary match); tactical-scale loops are rarer but geometrically more persistent (19.3% ± 7.2%; 12.7%, 19/150 in the primary match; mean persistence 3.80 m (tactical) vs 1.98 m (individual)). Scale non-redundancy is confirmed (Spearman ρ = 0.264, 95% bootstrap CI [0.200, 0.314]). Topological features respond coherently to match dynamics — on-ball engagements and quick breaks are associated with decreased persistence, build-up phases with increased persistence (*p* < 0.001 for both). Temporal persistence dynamics are match-specific rather than universal; the framework provides systematic tools to quantify this variation [12]. All pilot data are public; the Python pipeline will be open-source released with journal submission.

**Timeliness, Beneficiaries and National Importance.** The Botnan and Lesnick survey [7] marks theoretical maturity in multiparameter persistence; validated workflows for competitive hierarchical systems are the gap this project addresses. Computational libraries (Ripser, GUDHI) enable execution but are not the research contribution. To our knowledge, a full Championship season now makes population-level topological statistics tractable at this scale for the first time. Direct beneficiaries: the mathematical sciences community (validated open-source library for multi-scale homology on competitive point clouds) and sports analytics practitioners — Swansea City AFC performance analysts, as co-development partner, receive practitioner-interpretable visualisations of pressing structures, formation gaps, and defensive-line organisation that standard geometric descriptors (team length, width, convex-hull area) do not directly quantify. The project strengthens UK research infrastructure in applied algebraic topology, aligned with EPSRC mathematical sciences priorities, and demonstrates mathematically driven engagement with the UK sports analytics industry. The domain-validation procedure — cutoff sweep, stability scoring, adaptive filtration — transfers to any competitive multi-agent system once characteristic interaction scales are re-derived.

---

**APPROACH**

**Project Structure and Team.** This 12-month project involves: (i) the PI (0.2 FTE), framework development, analysis oversight, and publication; (ii) two Co-Investigators (0.25 FTE combined), statistical and domain expertise; (iii) a Research Associate (1.0 FTE, 9 months, Months 2–10), pipeline implementation, full-season analysis, and landscape library development; (iv) partnership with Swansea City AFC and StatsBomb (Championship tracking data and formation labels). Four integrated objectives are pursued (three research objectives plus one strategic output).

**Sample-size rationale.** A full Championship season (~540 matches) supports subgroup inference (n ≈ 32 matches per stratum for 95% CI half-width 0.025 on tactical-scale H₁ presence; pilot across-match s.d. 0.072) and powers O2 landscape comparisons (effect size Cohen's *d* ≥ 0.30 at power 0.80, α = 0.05, Benjamini–Hochberg FDR correction; n ≈ 180 matches per tactical class). A pilot linear mixed model of the within-match half-effect on tactical-scale H₁ persistence (β̂₁ = −0.081, stratified permutation *p* = 0.051 [12]) is borderline at α = 0.05 and consistent with match-specific dynamics; season-scale replication resolves it.

**Objectives.** Building on the validated multi-scale framework of Brown et al. [12] and persistence landscape methods of Bubenik [10] and Chazal et al. [11]:

**O1 — Population-level topological statistics** (PI and RA, Months 1–10): Scale the validated pipeline [12] to a full Championship season. Establish how topological features vary across hundreds of matches and how they relate to standard tactical descriptors from partner data. PI establishes the Supercomputing Wales concurrent pipeline in Month 1; a 20-match Championship batch (Months 1–2) re-validates cutoffs per [12] before full-season execution — stability scores below 0.80 trigger re-derivation, gating downstream work. RA (Months 2–7) processes the full season (barcode database complete by Month 7). PI conducts exploratory joint analysis (Months 5–7). *Milestone: cutoff gate (Month 2); barcode database (Month 7).*

**O2 — Topological fingerprinting** (PI, Months 6–9): Can different formation systems be distinguished by topological signatures? Formation labels from StatsBomb and SkillCorner; inter-rater agreement between the two label feeds (Cohen's κ) computed before confirmatory tests; hypotheses pre-registered on the Open Science Framework (OSF) in Month 2. Success criteria: distinct signatures for ≥3 tactical configurations; statistically significant between-system differences after Benjamini–Hochberg multiple-comparison correction (*p* < 0.05); topological measures add information beyond team length, width, and convex-hull area. Formation types are compared by standard L² distance between their averaged landscape summaries [10,11] and by vectorised diagram-image features, benchmarked against conventional team-shape metrics (Methodology and Feasibility). *Milestone: OSF pre-registration (Month 2); fingerprint results (Month 9).*

**O3 — Temporal dynamics and phase transitions** (PI and RA, Months 4–10): How does topological structure evolve within matches, and do detected transitions align with tactical events (substitutions, formation changes)? RA implements landscape tracking for within-match paths *t* ↦ λ_δ(*t*) (Months 6–10); PI applies functional PCA [17] and CUSUM change-point detection [18], with bootstrap calibration [11]. Mathematical targets: well-posedness of the Fréchet mean under competitive sequential paths extending [11], and a stability bound for the CUSUM statistic under Wasserstein diagram perturbations. Success criteria: CUSUM change-points align with tactical annotations at ≥70% agreement in randomly held-out match sub-samples (permutation *p* < 0.05). Wasserstein comparison is the defined fallback if landscape extension requires development beyond [10,11]. *Milestone: landscape module (Month 8); combined O2/O3 outputs (Month 9).*

**O4 — Standard Grant evidence synthesis** (PI, Months 9–12): Standard Grant preparation begins in Month 9, compiling full-season results into a reproducible evidence base for a **separate follow-on application** extending the framework to broader competitive multi-agent systems where domain-validated scales can be re-derived. Submission is targeted within 12 months of project completion. O1–O3 are standalone publishable contributions independently of this strategic output. *Milestone: evidence pack (Month 12).*

**Methodology and Feasibility.** The containerised Python pipeline (Ripser [15], GUDHI, giotto-tda [16]; <2 s per frame) processes tracking data through clustering, adaptive filtration, barcode computation, and persistence comparisons (diagram-image features, L² distance between averaged landscapes, ANCOVA baselines) under the Swansea City AFC–StatsBomb agreement. Full-season processing requires ~1,600 CPU-hours; Supercomputing Wales allocation (5,000 core-hours) covers processing, gate batches, and O3 landscape computation with margin. The Month 1–2 gate confirms cutoff transferability and 1 Hz production fidelity before full-season commitment.

**Risk Management.** (i) *Data access:* StatsBomb agreement confirmed for 2024/25; ~270-match contingency remains publishable for O1; O2 would be reported as exploratory only. (ii) *Scale transferability:* Month 2 gate re-derives cutoffs on Championship data. (iii) *Formation-label noise:* dual-source verification and parallel unsupervised landscape clustering; pre-registered exclusion protocol. (iv) *Landscape theory:* Wasserstein fallback preserves O3 if sequential landscape extension requires additional development.

**Translation to Impact.** Open-source code archived via Swansea University's Zenodo community (DOI). Paper 1 (methodology [12]) submitted to ArXiv and to the *Journal of Applied and Computational Topology* (JACT) from Month 1; Paper 2 (football analytics) targets *Journal of Sports Sciences*; Paper 3 (full-season results and persistence landscapes) targets Month 11. Tactical outputs co-developed with Swansea City AFC as practitioner-interpretable visualisations.

**Research Environment.** Swansea University's Zienkiewicz Institute provides Supercomputing Wales (PI has existing allocation) and the Swansea City AFC–StatsBomb data agreement; the Research Office supports partnership negotiation and fast-tracked ethics review. Co-Is Professor Gibin Powathil (Mathematics) and Professor Liam Kilduff (Sport and Exercise Sciences) provide mathematical and domain supervision.

**Project Timeline**

| Activity | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Pipeline setup & RA onboarding | ■ | | | | | | | | | | | |
| Cutoff gate & OSF pre-registration | | ■ | | | | | | | | | | |
| Full-season computation (O1) | | | ■ | ■ | ■ | ■ | ■ | | | | | |
| Barcode database (O1) | | | | | | | ■ | | | | | |
| Fingerprinting (O2) | | | | | ■ | ■ | ■ | ■ | ■ | | | |
| Landscape methods (O3) | | | | ■ | ■ | ■ | ■ | ■ | ■ | | | |
| O2/O3 outputs | | | | | | | | | ■ | | | |
| Standard Grant synthesis (O4) | | | | | | | | | ■ | ■ | ■ | ■ |

---

**References added for O3 methods** *(append to JeS bibliography; numbers [17–18] assume existing list [1–16] unchanged):*

17. Ramsay, J. O. & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.). Springer. https://doi.org/10.1007/b98809

18. Page, E. S. (1954). Continuous inspection schemes. *Biometrika*, 41(1/2), 100–115. https://doi.org/10.2307/2333009

*Note: [11] Chazal et al. (2014) covers bootstrap convergence of persistence landscapes; [17] and [18] cite the functional PCA and CUSUM procedures applied to landscape paths.*
