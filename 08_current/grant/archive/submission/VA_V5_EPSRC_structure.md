# Vision and Approach — EPSRC criteria structure (V5)

<!-- Version: V5 — compression pass on V4.1 (`VA_V4_EPSRC_structure.md`).
     Keeps the EPSRC 12-heading Vision/Approach map; cuts repeated claims so
     each idea is said primarily once (see say-it-once map in the V4 review
     notes). Target: ≤3 pages Calibri 11 pt, 2 cm margins (JeS paste).
     NOT yet page-verified — paste into Word/Overleaf and trim if over.

     Compression principles applied:
     (1) §1 Quality: keep (i)–(iii) list only; drop second method prose and
         closing “proven foundation” (evidence lives in §2).
     (2) §2: drop rhetorical opener; ¶1 keeps only what §1 lacks ([8], [10]);
         pilot paragraph keeps headline numbers, cites [19] for mechanics.
     (3) §3: no §2 recap; short (i)–(iii) only.
     (4) §4: Timeliness/Need/Opportunity merged to one paragraph.
     (5) §5 slimmed; §6 reduced to a short beneficiary line (was a §5 echo).
     (6) §7: drop bridge and “Building on…” lead-in; O1–O4 keep gates,
         success criteria, milestones; O4 does not re-narrate §5 pathways.
     (7) §8–§12: one telling each of pipeline, CPU-hours, Swansea/StatsBomb.
     (8) Gantt retained (milestones also in O1–O4); drop first if still over.

     CITATION NUMBERS — retained from V4.1 / compiled LaTeX order. Spot-check
     against `submission/tex` before JeS paste. Do NOT cite Brown2026inprep.

     Canonical numbers: ../CANONICAL_NUMBERS.md
     Narrative (uncompressed): VA_V4_EPSRC_structure.md
     Prior page-verified free-text master: VA_compressed_V3_no_figures.md -->

---

**VISION**

**1. Excellent Quality and Importance**

This research develops new mathematical frameworks for the multi-scale topological analysis of *competitive collective systems* — agents that coordinate internally while opposing an adversary within a bounded domain. This under-modelled class spans autonomous-vehicle fleets, opposing crowd flows, predator–prey populations and team sports. Unlike cooperative swarms, competitive systems exhibit *adversarial geometry*: each subgroup's configuration is continuously deformed by its opponent across distinct interaction length scales.

**Importance.** Computational topology lacks a method to attribute topological structure — connected clusters (H₀) and enclosing loops (H₁) — to the organisational scales at which such systems operate. Standard single-parameter persistent homology [1,2] via one Vietoris–Rips filtration [3] merges all agents into a single persistence diagram, so level-specific attribution is lost. Multiparameter persistence [4,5] would address this in principle but remains computationally impractical at the required point-cloud sizes and frame rates. No existing method attributes competitive topological structure to validated interaction scales on hierarchical, high-frequency data. This project closes that gap in professional football — a richly measured system with well-separated individual, tactical and team scales — and scales to a full Championship season to test whether topological structure holds as a population-level property. The procedure transfers to any bounded competitive multi-agent system once characteristic interaction scales are identified.

**Quality.** Rigour rests on *stability-validated* cutoffs, making the decomposition falsifiable, reproducible and transferable rather than heuristic. Three contributions advance prior work: (i) domain-validated scale identification via a reproducible, stability-scored procedure; (ii) adaptive filtration for consistent multi-scale H₁ detection; (iii) persistence landscape dynamics [6,7] enabling change-point detection of topological phase transitions. Pilot validation (§2) shows the season-scale programme rests on a proven foundation.

**2. Background — Building on Previous Work**

The mathematical foundation is persistent homology [1,2] and its stability theorem [8], which licences application to noisy tracking data. Persistence landscapes [6], their stochastic convergence [7] and stable diagram vectorisations [9] underwrite the bootstrap intervals and classification methods used in O2–O3. Multiparameter persistence [4,5] remains out of computational reach here; cluster-then-homology methods [10] operate only in cooperative, quasi-static settings. Our domain-validated decomposition by interaction length is the complementary, tractable route.

Topology has been shown to capture collective organisation in biological aggregation [11], collective motion [12], and flocking governed by topological rather than metric distance [13] — motivating our interaction-length framing. Gu et al. [14] detect topological change points in multi-agent systems, but at a single scale; extending this to competitive, multi-scale, sequential diagrams is a defining aim of O3. Football spatiotemporal analysis [15,16] supplies both the testbed and the conventional baselines — team length, width, centroid distance [17] and pitch-control space creation [18] — that topological features must be shown to exceed.

Our methodology paper (*Journal of Applied and Computational Topology* [19]) develops the measurement-aware multi-scale pipeline and validates it across 10 professional matches (SkillCorner; 104,722 event–topology pairs [19,20,21]). Three H₀ regimes — individual 2.98 m, tactical 12.0 m, team 30.0 m — reproduce across all ten matches (cross-epoch stability 0.96, 0.84, 1.00). Two H₁ regimes emerge: individual-scale loops near-universal but transient (97.0% ± 1.5% frame presence); tactical-scale loops rarer but more persistent (19.3% ± 7.2%; mean persistence 3.80 m vs 1.98 m); scales are non-redundant (Spearman ρ = 0.264). Features respond coherently to match events (*p* < 0.001), though dynamics are match-specific. A companion football-analytics paper [22] (*Journal of Sports Sciences*) develops practitioner interpretation and motivates the fingerprinting question of §3. Pilot data are public; the pipeline will be open-source on submission.

**3. Advancing Current Understanding and Generating New Knowledge**

The open question is what holds at *population* scale (~540 Championship matches). **(i) Distributional laws:** do pilot stability scores, H₁ presence rates and complementarity behave as population regularities, or vary with tactical context? **(ii) Comparison geometry:** landscape [6] and image [9] distances that distinguish formation systems in persistence space. **(iii) Functional dynamics:** within-match paths *t* ↦ λ_δ(*t*) characterising stability regimes and transitions. Establishing (i)–(iii) is this project's contribution to knowledge (Objectives O1–O3, §7).

**4. Timeliness, Need and Opportunity**

Three developments now converge: survey-level consolidation of multiparameter persistence [4] and statistical TDA with convergence guarantees [6,7,9]; computational tooling (Ripser [23], GUDHI, giotto-tda [24]) that makes per-frame homology tractable at season scale; and, to our knowledge, newly accessible season-scale competitive tracking data. No validated workflow yet exists for multi-scale persistent homology on competitive, hierarchical, high-frequency systems — the methodological and applied need this project answers.

**5. Impact**

**Research.** A validated open-source library for multi-scale persistent homology on competitive, time-evolving point clouds, contributing to EPSRC's *physical and mathematical sciences powerhouse* priority and building UK capability in applied topology, with links to *AI, digitisation and data*.

**Industry.** Co-developed with Swansea City AFC and data partners (StatsBomb, Genius Sports), translating topological measures into practitioner-interpretable tools for pressing structures, formation gaps and defensive-line organisation that geometric descriptors miss.

**Stepping-stone.** This project prepares a follow-on Standard Grant (§7, O4). The domain-validation procedure transfers to other bounded competitive systems once scales are re-derived. Pathways (not deliverables) include tumour–immune competition (*transforming health and healthcare*; Co-I Powathil) and competitive logistics / autonomous-fleet coordination (*AI, digitisation and data*). The full-season evidence base makes that larger programme fundable.

**6. Benefits and Beneficiaries**

Direct: mathematical sciences community (open-source library); Swansea City AFC analysts and the wider sports-analytics research community. Longer-term: operators of other competitive multi-agent domains; the proposed Standard Grant programme (§7, O4).

---

**APPROACH**

**7. Research Design and Objectives**

**Project Structure and Team.** 12 months: (i) PI (0.2 FTE) — framework, analysis oversight, publication; (ii) two Co-Investigators (0.25 FTE combined) — statistical and domain expertise; (iii) Research Associate (1.0 FTE, 9 months, Months 2–10) — pipeline, full-season analysis, landscape library; (iv) Swansea City AFC and StatsBomb (Championship tracking and formation labels).

**Sample-size rationale.** A full Championship season (~540 matches) supports subgroup inference (n ≈ 32 per stratum → 95% CI half-width 0.025 on tactical-scale H₁ presence; pilot s.d. 0.072) and powers O2 comparisons (n ≈ 180 per tactical class detects Cohen's *d* ≥ 0.30 at power 0.80, α = 0.05, Benjamini–Hochberg FDR). A pilot half-effect on tactical-scale H₁ persistence is borderline (*p* = 0.051 [19]); season-scale replication resolves this.

**O1 — Population-level topological statistics** (PI and RA, Months 1–7): Scale the validated pipeline [19] to a full Championship season and relate topological features to partner tactical descriptors. Month 1: Supercomputing Wales concurrent pipeline. Months 1–2: 20-match Championship cutoff gate (stability < 0.80 triggers re-derivation). RA Months 2–7: full-season barcodes. *Milestone: cutoff gate (Month 2); barcode database (Month 7).*

**O2 — Topological fingerprinting** (PI, Months 6–9): Can formation systems be distinguished by topological signatures? Dual-source labels (StatsBomb, SkillCorner) with Cohen's κ before confirmatory tests; OSF pre-registration in Month 2. Success: distinct signatures for ≥3 configurations; significant between-system differences after FDR correction (*p* < 0.05); information gain beyond team length, width and convex-hull area. Comparisons use L² landscape distances [6,7] and diagram-image features. *Milestone: OSF pre-registration (Month 2); fingerprint results (Month 9).*

**O3 — Temporal dynamics and phase transitions** (PI and RA, Months 4–10): Do within-match landscape paths *t* ↦ λ_δ(*t*) yield transitions aligned with tactical events? RA implements landscape tracking (Months 6–10); PI applies functional PCA [25] and CUSUM [26] with bootstrap calibration [7]. Mathematical targets: well-posedness of the Fréchet mean under competitive sequential paths extending [7], and a CUSUM stability bound under Wasserstein perturbations. Success: ≥70% agreement with held-out tactical annotations (permutation *p* < 0.05). Wasserstein comparison is the defined fallback. *Milestone: landscape module (Month 8); combined O2/O3 outputs (Month 9).*

**O4 — Standard Grant evidence synthesis** (PI, Months 9–12): Compile full-season results into a reproducible evidence pack for a **separate** follow-on application translating the framework to higher-impact adversarial systems (§5). Target submission within 12 months of project completion. O1–O3 remain standalone publishable contributions. *Milestone: evidence pack (Month 12).*

**8. Methodology**

Containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]; <2 s/frame): clustering, adaptive filtration, barcodes, then landscape and diagram-image comparisons with ANCOVA baselines. The Month 1–2 gate confirms cutoff transferability and 1 Hz production fidelity before full-season commitment (§12).

**9. Feasibility and Risk Management**

Feasible within 12 months: ~1,600 CPU-hours within a 5,000 core-hour allocation (§12); de-risked by the Month-2 cutoff gate; required expertise in place (§11).

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data access | Low | High | StatsBomb agreement confirmed for 2024/25; ~270-match contingency remains publishable for O1 (O2 exploratory only under contingency) |
| Scale transferability | Medium | Medium | Month 2 validation gate re-derives cutoffs on Championship data |
| Formation-label noise | Medium | Medium | Dual-source verification, unsupervised landscape clustering, pre-registered exclusion protocol |
| Landscape theory | Medium | Medium | Wasserstein fallback preserves O3 if sequential landscape extension requires further development |

**10. Translation to Outcomes and Impact**

Open-source code archived via Swansea University Zenodo (DOI). Methodology paper [19] to arXiv and JACT from Month 1; football-analytics paper [22] to *Journal of Sports Sciences*; full-season landscapes paper targets Month 11. Practitioner outputs and Standard Grant pathway: §5.

**11. Research Environment**

Zienkiewicz Institute, Swansea University. Co-I Professor Gibin Powathil (mathematical oncology; health-sector pathway, §5) and Professor Liam Kilduff (sport and exercise sciences; tactical interpretation). Swansea City AFC partnership supports co-development of practitioner outputs.

**12. Facilities, Infrastructure and Host Support**

Supercomputing Wales allocation (5,000 core-hours; PI's existing access) covers the ~1,600 CPU-hour full-season load with margin. Championship tracking and formation labels secured via the Swansea City AFC–StatsBomb agreement. Swansea University Research Office supports partnership negotiation and fast-tracked ethics review.

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

*Note: numbers follow the V4.1 / compiled LaTeX order. Spot-check against the compiled bibliography before JeS paste.*
