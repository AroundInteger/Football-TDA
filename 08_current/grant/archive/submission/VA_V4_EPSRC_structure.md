# Vision and Approach — EPSRC criteria structure (V4)

<!-- Version: V4.1 — builds on V4's EPSRC criteria structure (per internal
     reviewer mapping `Map VA to EPSRC format.docx`, against
     `review/V_and_A_instructions.docx`). Two changes in this pass:
     (1) STRUCTURE — the former Approach section "Building on Previous Work"
     (Preliminary Validation) is moved UP into Vision as a new §2 "Background",
     per the internal grant review board convention (§7 always sits in Vision,
     to supply context and evidence of building on prior work before the
     forward-looking claims). This renumbers Vision as 1–6 and shifts the
     first Approach heading to §7; §8–§12 are unchanged. The one-sentence
     "what O1–O3 build upon" bridge stays in Approach beside the objectives.
     (2) NARRATIVE — §2 Background is expanded into an explicit intellectual
     lineage ("standing on the shoulders of giants"): the prior work that
     enabled our methodology and football-analytics papers and that underpins
     the proposed objectives.
     §§2–4 (Background → Advancing Understanding → Timeliness) are rewritten
     to build on one another. §1 is slimmed to address ONLY the first UKRI
     Vision bullet — "excellent quality and importance within or beyond the
     field(s)" — with an explicit Importance/Quality split; its former method
     mechanics (adaptive-filtration percentile, ablation) and validation
     numbers are folded into §2, and its prior-work review into §2's lineage,
     so the four Vision bullets now map cleanly to §1 (quality/importance),
     §3 (advance understanding), §4 (timely) and §5 (impact). Word count is
     NOT prioritised in this pass, per instruction (narrative first); trim
     toward the 3-page Vision+Approach limit once the narrative is agreed.

     CITATION NUMBERS — the [n] labels below have been re-synced to the
     compiled LaTeX order (natbib + unsrtnat, order of first appearance) of
     the twin `tex/sections/02_vision_and_approach.tex`. The full ordered list
     is at the foot of this file. Spot-check the numbers against the compiled
     bibliography before pasting into JeS; a few inferred keys ([3] Vietoris–
     Rips filtration, [20,21] positional standards) should be confirmed there.

     PAGE LIMIT — this candidate is NOT yet page-verified. Compile the twin
     `submission/tex` in Overleaf and confirm the Vision+Approach body is
     within the 3-page limit before submission; trim if it overflows.

     The football-analytics paper (Journal of Sports Sciences) now has its own
     BibTeX key `Brown2026b` and is cited as [22]. Papers are named by content
     + outlet throughout (no A/B or 1/2/3 labels), per the naming decision
     recorded in CANONICAL_NUMBERS.md. Do NOT cite the armed-conflict
     application (Brown2026inprep) — ethics approval pending (see
     CANONICAL_NUMBERS.md).

     Canonical numbers: ../CANONICAL_NUMBERS.md
     Long-form detail: ../full/02_Vision_and_Approach.md
     Prior version (EPSRC free-text order): VA_compressed_V3_no_figures.md -->

---

**VISION**

**1. Excellent Quality and Importance**

This research develops new mathematical frameworks for the multi-scale topological analysis of *competitive collective systems* — agents that coordinate internally while opposing an adversary within a bounded domain. This is an important but under-modelled class in applied mathematics, spanning autonomous-vehicle fleets sharing airspace, opposing crowd flows, predator–prey populations and team sports. Unlike cooperative swarms, competitive systems exhibit *adversarial geometry*, in which each subgroup's configuration is continuously deformed by its opponent across several distinct interaction length scales.

**Importance.** Within computational topology the field faces a specific, unresolved problem: how to attribute topological structure — connected clusters (H₀) and enclosing loops (H₁) — to the distinct organisational scales at which such systems operate. Standard single-parameter persistent homology [1,2], applied through one Vietoris–Rips filtration [3], analyses all agents in a single persistence diagram, merging features across scales so that level-specific attribution is lost. Multiparameter persistence [4,5] would address this in principle but remains computationally impractical at the point-cloud sizes and frame rates required. No existing method attributes competitive topological structure to validated interaction scales on hierarchical, high-frequency data. This project addresses that gap in professional football — a richly measured competitive system with well-separated individual, tactical and team scales — and scales the solution across a full Championship season to test whether topological structure holds as a population-level property rather than a single-match observation. The importance also reaches beyond the field: the resulting procedure transfers to any bounded competitive multi-agent system for which characteristic interaction scales can be identified.

**Quality.** The quality of the contribution rests on rigour, reproducibility and the concreteness of the advance it makes over current practice. Our framework decomposes the competitive point cloud by empirically validated interaction length, computes single-parameter homology at each scale with adaptive filtration for consistent H₁ detection, and extends this to persistence landscape dynamics [6,7] for competitive sequential diagrams. Decisively for rigour, the decomposition rests on *stability-validated* cutoffs, making it falsifiable, reproducible and transferable rather than heuristic. Three contributions advance prior work: (i) domain-validated scale identification, replacing heuristic filtration choices with a reproducible, stability-scored procedure; (ii) adaptive filtration for consistent multi-scale H₁ detection; and (iii) persistence landscape dynamics enabling change-point detection of topological phase transitions. This is already more than conceptual: the framework is validated across ten professional matches, with reproducible scale regimes and topology that responds coherently to match events (§2), so the proposed season-scale programme rests on a proven, open and reproducible foundation. Together these constitute a practical advance in computational topology: validated multi-scale persistent homology on hierarchical, competitive, time-evolving point clouds.

**2. Background — Building on Previous Work**

This project stands on four decades of algebraic topology and two established empirical literatures; our contribution is to combine and extend them, not to build from nothing. The mathematical foundation is persistent homology [1,2] and its stability theorem [8], which guarantees that bounded measurement error perturbs a persistence diagram only boundedly. That guarantee is the licence for applying topology to noisy, real-world tracking data and is the theoretical bedrock of our measurement-aware pipeline. To move from qualitative diagrams to statistical inference we build directly on persistence landscapes [6] and their proven stochastic convergence [7] — which underwrite the bootstrap confidence intervals we report — and on stable diagram vectorisations [9] for classification. On multi-scale structure specifically, multiparameter persistence [4,5] is the theoretical ideal but remains computationally out of reach at our point-cloud sizes and frame rates, while cluster-then-homology methods [10] operate only in cooperative, quasi-static settings. Our domain-validated decomposition by interaction length is the complementary, tractable route that this body of work motivates but does not yet provide.

The second foundation is the demonstrated capacity of topology to capture the organisation of collective systems: biological aggregation [11], collective motion analysed with topology [12], and the finding that flocking interactions are governed by topological rather than metric distance [13] — which directly motivates our interaction-length framing. Gu et al. [14] detect topological change points in multi-agent systems, but at a single interaction scale; extending change-point detection to competitive, multi-scale, sequential diagrams is a defining aim of O3. The third foundation is the maturity of football spatiotemporal analysis [15,16], whose established shape descriptors — team length, width and centroid distance [17] and pitch-control space creation [18] — furnish both a rigorous, richly measured testbed and the conventional baselines that any new topological feature must be shown to exceed.

On these foundations we have produced two companion outputs. Our methodology paper (*Journal of Applied and Computational Topology* [19]) develops the measurement-aware, multi-scale pipeline — hierarchical decomposition at empirically validated cutoffs followed by adaptive Vietoris–Rips filtration (75th percentile of inter-centroid distances, floored at the validated cutoff δ; H₁ outputs are insensitive to this choice) — and validates it across 10 professional matches (SkillCorner open broadcast tracking, 10 Hz; 104,722 event–topology pairs [19]), a testbed with high-frequency measurement and established positional standards [20,21]. Three H₀ regimes are identified — individual 2.98 m, tactical 12.0 m, team 30.0 m — reproducing across all ten matches with cross-epoch stability 0.96, 0.84 and 1.00. Two H₁ regimes emerge: individual-scale loops are near-universal and transient (97.0% ± 1.5% frame presence), tactical-scale loops rarer but geometrically more persistent (19.3% ± 7.2%; mean persistence 3.80 m vs 1.98 m); scale non-redundancy is confirmed (Spearman ρ = 0.264, 95% bootstrap CI [0.200, 0.314]). Crucially, topological features respond coherently to match dynamics — on-ball engagements and quick breaks decrease persistence, build-up phases increase it (*p* < 0.001 for both) — though these dynamics are match-specific rather than universal. A companion football-analytics paper [22] (targeting the *Journal of Sports Sciences*) applies the same validated pipeline to practitioner-facing tactical interpretation, and directly motivates the topological-fingerprinting question of §3. All pilot data are public and the Python pipeline will be open-source released on submission. This validated foundation — a 10-match proof of concept — is precisely what the proposed work advances to population scale.

**3. Advancing Current Understanding and Generating New Knowledge**

Section 2 establishes, at 10-match scale, that scale-specific barcodes exist, are reproducible, and respond coherently to match events. The open question — and the new knowledge this project generates — is what holds at *population* scale, in three linked directions. **(i) Distributional laws:** across a full Championship season (~540 matches), do the pilot stability scores, H₁ presence rates and complementarity behave as population-level regularities, or do they vary systematically with tactical context? **(ii) Comparison geometry:** landscape [6] and image [9] distances in persistence space that render tactical systems distinguishable, providing a topologically grounded definition of formation identity that is consistent across matches. **(iii) Functional dynamics:** treating each match as a path *t* ↦ λ_δ(*t*) in landscape space to characterise within-match stability regimes and transitions. None of (i)–(iii) is demonstrated at championship scale in the pilot; establishing them is this project's contribution to knowledge, and maps directly onto Objectives O1–O3 (§7).

**4. Timeliness, Need and Opportunity**

**Timeliness.** The knowledge set out in §3 is attainable now because three developments have recently converged. First, the mathematics has matured: multiparameter persistence has reached survey-level consolidation [4], and statistical TDA — landscapes with convergence guarantees [6,7] and stable vectorisations [9] — now supports population-level inference. Second, computational tooling (Ripser [23], GUDHI, giotto-tda [24]) makes per-frame homology tractable at season scale; it enables the work but is not the contribution. Third, season-scale competitive tracking data have, to our knowledge, only recently become accessible.

**Need.** No validated workflow yet exists for multi-scale persistent homology on competitive, hierarchical, high-frequency systems. Analysts in sports — and, prospectively, the health and economic sectors — need interpretable structural metrics that conventional geometric descriptors do not provide. This project answers that methodological and applied need.

**Opportunity.** The simultaneous arrival of mature theory, mature tooling and season-scale data opens a window to settle these questions now rather than later. This makes the project timely rather than merely feasible.

**5. Impact**

**Impact on research and the discipline.** The primary impact is to the mathematical sciences. The project delivers a validated, reproducible workflow and an open-source library for multi-scale persistent homology on competitive, time-evolving point clouds. This contributes to EPSRC's discovery priority of a *physical and mathematical sciences powerhouse* and to the Mathematical Sciences theme's aim of transformative, cross-disciplinary methods. As a systems approach to hierarchical, competitive dynamics, it also connects the mathematical sciences to EPSRC's *AI, digitisation and data* priority. In doing so it builds UK capability in an emerging area of applied topology.

**Economic and industry impact.** The project is developed with Swansea City AFC and data partners (StatsBomb, Genius Sports). It translates topological measures into practitioner-interpretable tools for the UK sports analytics sector, an area of clear industrial demand. These tools quantify aspects of team structure that conventional geometric descriptors miss (detailed in §6). They also build durable routes to academia–industry collaboration.

**Longer-term reach — a stepping-stone to higher-impact translation.** This project is deliberately scoped as a stepping-stone to a follow-on Standard Grant (§7, O4). The domain-validation procedure — cutoff sweep, stability scoring, adaptive filtration — transfers to any bounded competitive multi-agent system once its characteristic scales are re-derived. The natural next targets are adversarial spatial systems in the health and economic sectors, where the potential benefit is greater. In health, tumour–immune competition is a direct fit: it aligns with EPSRC's *transforming health and healthcare* priority and draws on Co-I Powathil's mathematical-oncology expertise. In the economic and security domain, competitive logistics and autonomous-fleet coordination align with the *AI, digitisation and data* priority. We frame these as pathways, not deliverables. The football-validated, open-source workflow and full-season evidence base are what make that larger programme fundable. This grant provides the proof of concept; the Standard Grant delivers the translation.

**6. Benefits and Beneficiaries**

**Direct beneficiaries:** the mathematical sciences community, through a validated open-source library for multi-scale homology on competitive point clouds; sports analytics practitioners, notably Swansea City AFC performance analysts as co-development partner, who receive practitioner-interpretable visualisations of pressing structures, formation gaps, and defensive-line organisation that standard geometric descriptors (team length, width, convex-hull area) do not directly quantify; and the wider sports analytics research community.

**Longer-term beneficiaries:** operators of other competitive multi-agent domains, once characteristic interaction scales are re-derived for their setting; the proposed Standard Grant programme (§7, O4), for which this project provides the full-season evidence base; and industry users adopting the open-source pipeline for their own competitive-system analyses.

---

**APPROACH**

**7. Research Design and Objectives**

**Project Structure and Team.** This 12-month project involves: (i) the PI (0.2 FTE), framework development, analysis oversight, and publication; (ii) two Co-Investigators (0.25 FTE combined), statistical and domain expertise; (iii) a Research Associate (1.0 FTE, 9 months, Months 2–10), pipeline implementation, full-season analysis, and landscape library development; (iv) partnership with Swansea City AFC and StatsBomb (Championship tracking data and formation labels). Four integrated objectives are pursued (three research objectives plus one strategic output).

**Sample-size rationale.** A full Championship season (~540 matches) supports subgroup inference: n ≈ 32 matches per stratum gives a 95% CI half-width of 0.025 on tactical-scale H₁ presence (pilot across-match s.d. 0.072). It also powers O2 landscape comparisons: n ≈ 180 matches per tactical class detects an effect size of Cohen's *d* ≥ 0.30 at power 0.80 and α = 0.05, with Benjamini–Hochberg FDR correction. A pilot linear mixed model of the within-match half-effect on tactical-scale H₁ persistence (β̂₁ = −0.081, stratified permutation *p* = 0.051 [19]) is borderline at α = 0.05 and consistent with match-specific dynamics. Season-scale replication resolves this.

The validated foundation of §2 is what these objectives advance and progress: from a 10-match proof of concept to full-season distributional statistics (O1), from detection to classification (O2), and from single-diagram summaries to functional dynamics (O3).

**Objectives.** Building on the validated multi-scale framework of Brown et al. [19] and persistence landscape methods of Bubenik [6] and Chazal et al. [7]:

**O1 — Population-level topological statistics** (PI and RA, Months 1–7): Scale the validated pipeline [19] to a full Championship season. Establish how topological features vary across hundreds of matches and how they relate to standard tactical descriptors from partner data. PI establishes the Supercomputing Wales concurrent pipeline in Month 1; a 20-match Championship batch (Months 1–2) re-validates cutoffs per [19] before full-season execution — stability scores below 0.80 trigger re-derivation, gating downstream work. RA (Months 2–7) processes the full season (barcode database complete by Month 7). PI conducts exploratory joint analysis (Months 5–7). *Milestone: cutoff gate (Month 2); barcode database (Month 7).*

**O2 — Topological fingerprinting** (PI, Months 6–9): Can different formation systems be distinguished by topological signatures? Formation labels from StatsBomb and SkillCorner; inter-rater agreement between the two label feeds (Cohen's κ) computed before confirmatory tests; hypotheses pre-registered on the Open Science Framework (OSF) in Month 2. Success criteria: distinct signatures for ≥3 tactical configurations; statistically significant between-system differences after Benjamini–Hochberg multiple-comparison correction (*p* < 0.05); topological measures add information beyond team length, width, and convex-hull area. Formation types are compared by standard L² distance between their averaged landscape summaries [6,7] and by vectorised diagram-image features, benchmarked against conventional team-shape metrics (§8). *Milestone: OSF pre-registration (Month 2); fingerprint results (Month 9).*

**O3 — Temporal dynamics and phase transitions** (PI and RA, Months 4–10): How does topological structure evolve within matches, and do detected transitions align with tactical events (substitutions, formation changes)? RA implements landscape tracking for within-match paths *t* ↦ λ_δ(*t*) (Months 6–10); PI applies functional PCA [25] and CUSUM change-point detection [26], with bootstrap calibration [7]. Mathematical targets: well-posedness of the Fréchet mean under competitive sequential paths extending [7], and a stability bound for the CUSUM statistic under Wasserstein diagram perturbations. Success criteria: CUSUM change-points align with tactical annotations at ≥70% agreement in randomly held-out match sub-samples (permutation *p* < 0.05). Wasserstein comparison is the defined fallback if landscape extension requires development beyond [6,7]. *Milestone: landscape module (Month 8); combined O2/O3 outputs (Month 9).*

**O4 — Standard Grant evidence synthesis** (PI, Months 9–12): Standard Grant preparation begins in Month 9, compiling full-season results into a reproducible evidence base for a **separate follow-on application** that translates the framework to higher-impact adversarial spatial systems in the health and economic sectors (for example tumour–immune competition and competitive logistics), where domain-validated scales can be re-derived (§5). Submission is targeted within 12 months of project completion. O1–O3 are standalone publishable contributions independently of this strategic output. *Milestone: evidence pack (Month 12).*

**8. Methodology**

The containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) computes homology in under 2 s per frame. It processes tracking data through clustering, adaptive filtration and barcode computation, then persistence comparisons (diagram-image features, L² distance between averaged landscapes, and ANCOVA baselines). The Month 1–2 gate confirms cutoff transferability and 1 Hz production fidelity before full-season commitment. Computational infrastructure and data-access arrangements are detailed in §12.

**9. Feasibility and Risk Management**

**Feasibility.** The project is feasible within 12 months. Computation is modest and embarrassingly parallel — about 1,600 CPU-hours within a 5,000 core-hour allocation (§12). The schedule is de-risked by the Month-2 cutoff gate before full-season commitment, and the team holds the required topological, statistical and domain expertise (§11).

**Risk management.** Key risks and mitigations are as follows.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data access | Low | High | StatsBomb agreement confirmed for 2024/25; ~270-match contingency remains publishable for O1 (O2 reported as exploratory only under contingency) |
| Scale transferability | Medium | Medium | Month 2 validation gate re-derives cutoffs on Championship data |
| Formation-label noise | Medium | Medium | Dual-source verification (StatsBomb and SkillCorner), parallel unsupervised landscape clustering, pre-registered exclusion protocol |
| Landscape theory | Medium | Medium | Wasserstein fallback preserves O3 if sequential landscape extension requires additional development |

**10. Translation to Outcomes and Impact**

Open-source code is archived via Swansea University's Zenodo community (DOI). The methodology paper [19] is submitted to ArXiv and to the *Journal of Applied and Computational Topology* (JACT) from Month 1. The football-analytics paper [22] targets the *Journal of Sports Sciences*. A full-season results and persistence-landscapes paper targets Month 11. The two further translation routes — practitioner-facing tactical outputs co-developed with Swansea City AFC, and the follow-on Standard Grant (§7, O4) — are detailed in §5.

**11. Research Environment**

Swansea University's Zienkiewicz Institute provides the computational mathematics research environment for this project. Co-Investigator Professor Gibin Powathil brings mathematical-biology and mathematical-oncology expertise in the modelling of competitive biological systems — the foundation for the planned health-sector translation (§5; §7, O4) — and Professor Liam Kilduff (sport and exercise sciences) provides domain expertise for tactical interpretation. The established Swansea City AFC partnership provides sustained access to a professional football environment for co-development of practitioner outputs.

**12. Facilities, Infrastructure and Host Support**

Full-season processing requires ~1,600 CPU-hours; the Supercomputing Wales allocation (5,000 core-hours; PI's existing access) covers processing, gate batches, and O3 landscape computation with margin. Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb data agreement. Swansea University's Research Office supports partnership negotiation and provides fast-tracked ethics review — specific host-organisation support secured for this application.

---

**Project Timeline**

| Activity | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Pipeline setup & RA onboarding | ■ | | | | | | | | | | | |
| Cutoff gate & OSF pre-registration | | ■ | | | | | | | | | | |
| Full-season computation (O1) | | | ■ | ■ | ■ | ■ | ■ | | | | | |
| Barcode database (O1) | | | | | | | ■ | | | | | |
| Fingerprinting (O2) | | | | | | ■ | ■ | ■ | ■ | | | |
| Landscape methods (O3) | | | | ■ | ■ | ■ | ■ | ■ | ■ | ■ | | |
| O2/O3 outputs | | | | | | | | | ■ | | | |
| Standard Grant synthesis (O4) | | | | | | | | | ■ | ■ | ■ | ■ |

---

**References** *(compiled order — natbib/unsrtnat, order of first appearance; verify against the compiled LaTeX bibliography before pasting into JeS):*

1. Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255–308. `Carlsson2009`
2. Zomorodian, A. & Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249–274. `Zomorodian2005`
3. Edelsbrunner, H. & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society. `Edelsbrunner2010`
4. Botnan, M. B. & Lesnick, M. (2022). An introduction to multiparameter persistence. In *Representations of Algebras and Related Structures* (pp. 77–150). EMS Press. `BotnanLesnick2022`
5. Lesnick, M. (2015). The theory of the interleaving distance on multidimensional persistence modules. *Foundations of Computational Mathematics*, 15(3), 613–650. `Lesnick2015`
6. Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16(1), 77–102. `Bubenik2015`
7. Chazal, F., Fasy, B. T., Lecci, F., Rinaldo, A. & Wasserman, L. (2014). Stochastic convergence of persistence landscapes and silhouettes. *Proceedings of the 30th Annual Symposium on Computational Geometry*, 474–483. `Chazal2014`
8. Cohen-Steiner, D., Edelsbrunner, H. & Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120. `CohenSteiner2007`
9. Adams, H. et al. (2017). Persistence images: a stable vector representation of persistent homology. *Journal of Machine Learning Research*, 18(8), 1–35. `Adams2017`
10. Schindler, D. J. & Barahona, M. (2023). Analysing multiscale clusterings with persistent homology. arXiv:2305.04281. `SchindlerBarahona2023`
11. Topaz, C. M., Ziegelmeier, L. & Halverson, T. (2015). Topological data analysis of biological aggregation models. *PLoS ONE*, 10(5), e0126383. `Topaz2015`
12. Bhaskar, D. et al. (2019). Analysing collective motion with machine learning and topology. *Chaos*, 29(12), 123125. `Bhaskar2019`
13. Ballerini, M. et al. (2008). Interaction ruling animal collective behaviour depends on topological rather than metric distance. *PNAS*, 105(4), 1232–1237. `Ballerini2008`
14. Gu, K. et al. (2022). Change point detection in multi-agent systems based on higher-order features. *Chaos*, 32(11), 113117. `Gu2022`
15. Gudmundsson, J. & Horton, M. (2017). Spatio-temporal analysis of team sports. *ACM Computing Surveys*, 50(2), 22:1–22:34. `Gudmundsson2017`
16. Memmert, D., Lemmink, K. A. P. M. & Sampaio, J. (2017). Current approaches to tactical performance analyses in soccer using position data. *Sports Medicine*, 47(1), 1–10. `Memmert2017`
17. Folgado, H. et al. (2014). Length, width and centroid distance as measures of teams' tactical performance in youth football. *European Journal of Sport Science*, 14(S1), S487–S492. `Folgado2014`
18. Fernández, J. & Bornn, L. (2018). Wide open spaces: a statistical technique for measuring space creation in professional soccer. *Sloan Sports Analytics Conference*. `FernandezBornn2018`
19. Brown, R. et al. (2026). Multi-scale persistent homology for competitive spatial systems: measurement-aware methods and validation in professional football. *ArXiv preprint*; submitted to the *Journal of Applied and Computational Topology*. `Brown2026`
20. Di Salvo, V. et al. (2007). Performance characteristics according to playing position in elite soccer. *International Journal of Sports Medicine*, 28(3), 222–227. `DiSalvo2007`
21. Bradley, P. S. et al. (2009). High-intensity running in English FA Premier League soccer matches. *Journal of Sports Sciences*, 27(2), 159–168. `Bradley2009`
22. Brown, R. et al. (2026). Multi-scale topological signatures of tactical organisation in professional football. *In preparation*; to be submitted to the *Journal of Sports Sciences*. `Brown2026b`
23. Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423. `Bauer2021`
24. Tauzin, G. et al. (2021). giotto-tda: a topological data analysis toolkit for machine learning and data exploration. *Journal of Machine Learning Research*, 22(39), 1–6. `Tauzin2021`
25. Ramsay, J. O. & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.). Springer. `RamsaySilverman2005`
26. Page, E. S. (1954). Continuous inspection schemes. *Biometrika*, 41(1/2), 100–115. `Page1954`

*Note: numbers follow the compiled LaTeX order (order of first appearance). [1,2] are the foundational persistent-homology references and [3] the Vietoris–Rips filtration; the original provisional [9] ("H₁ insensitive to percentile") was the methodology paper's own ablation and is now covered by the [19] citation. The inferred keys [3] (Vietoris–Rips) and [20,21] (positional standards) should be confirmed against the compiled bibliography.*
