# Vision and Approach — EPSRC criteria structure (V6.2)



---

**VISION**

**1. Excellent Quality and Importance**

This research develops a mathematical framework extending multi-scale topological analysis to *competitive collective systems*, an important but under-modelled class of dynamical systems. These systems comprise agents that coordinate internally while competing against an adversary within a bounded domain, arising in applications ranging from autonomous-vehicle fleets to team sports. Unlike cooperative swarms, competitive systems exhibit *adversarial geometry*: the additional degrees of freedom introduced by adversarial interactions render each subgroup's configuration susceptible to deformation by its opponent across multiple interaction scales.  
  
**Importance.** No existing method attributes topological structure, connected clusters (H₀) and enclosing loops (H₁), to the distinct interaction scales exhibited by competitive systems in hierarchical, high-frequency data. Standard persistent homology [1,2], applied using a single distance threshold across all agents [3], collapses these scales into a single summary, preventing features from being linked to individual-, group-, or system-level organisation. Although multi-parameter topology [4,5] provides a theoretical route to resolving such scale-specific structure, existing methods remain computationally prohibitive for **real-world, high-frequency observations of competitive systems**. This project closes that gap in professional football: pilot analysis has already identified distinct, stability-validated interaction scales (§2), albeit in only a small number of matches. Scaling to a full Championship season will test whether this phenomenon persists as a population-level property and establish an analysis framework transferable to other bounded competitive multi-agent systems once their characteristic scales have been re-derived (§5).

**Quality.** The project’s quality lies in combining mathematical rigour with empirical validation. Rigour comes from *stability-validated* cutoffs: groups are defined by empirically tested interaction lengths rather than arbitrary thresholds, making the procedure falsifiable rather than ad hoc. Reproducibility follows because the two core components of the pipeline, scale decomposition and adaptive distance thresholds, have already been validated at pilot scale (§2). The new contribution is to move from identifying scale-specific topological structure to analysing its evolution over time, producing dynamic summaries from which structural change-points can be detected [6,7] and tested at season scale (§7, O3). This advances prior work through: (i) domain-validated scale identification in place of heuristic choices; (ii) adaptive distance thresholds for consistent multi-scale loop (H₁) detection; and (iii) time-evolving topological summaries for detecting structural transitions in competitive systems.



**2. Background — Building on Previous Work**

Three foundations underpin this project: algebraic topology; the topology of collective systems; and football spatiotemporal analysis. The first foundation is persistent homology [1,2] and its stability theorem [8]: small tracking error produces only a small change in the topological summary, so the method can be used on real measurement data. Standard tools then turn those summaries into quantities that can be compared across matches and used for classification [6,7,9] — the basis for O2–O3. Existing multi-scale approaches that cluster first and then compute homology [10] are limited to cooperative, slowly changing systems; our decomposition by validated interaction length is the practical route for competitive, high-frequency data.

The second foundation is topology's demonstrated capacity to capture collective organisation: biological aggregation [11], collective motion [12], and flocking interactions governed by nearest-neighbour count rather than metric radius [13] — motivating our interaction-length framing. Gu et al. [14] detect topological change points in multi-agent systems, but at a single scale; O3 extends this to competitive, bounded, multi-scale systems (§7). The third foundation is football spatiotemporal analysis [15,16], whose established shape descriptors — team length, width, centroid distance [17] and pitch-control space creation [18] — furnish both the testbed and the baselines any new topological feature must exceed.

On these foundations, our methodology paper (*Journal of Applied and Computational Topology* [19]) develops the multi-scale pipeline — decompose by validated interaction length, then compute homology at each scale with an adaptive distance threshold — and validates it across 10 professional matches (SkillCorner, 10 Hz; 104,722 event–topology pairs [19]; positional standards [20,21]). Three cluster-scale (H₀) regimes — individual 2.98 m, tactical 12.0 m, team 30.0 m — reproduce across all ten matches (cross-epoch stability 0.96, 0.84, 1.00). Two loop-scale (H₁) regimes emerge: individual-scale loops are near-universal but short-lived (97.0% ± 1.5% of frames); tactical-scale loops are rarer but last longer (19.3% ± 7.2%; mean persistence 3.80 m vs 1.98 m); the two scales carry largely independent information (correlation ρ = 0.264). Features respond coherently to match events (*p* < 0.001), though dynamics are match-specific. A companion football-analytics paper [22] (*Journal of Sports Sciences*) develops practitioner interpretation and motivates the fingerprinting question of §3. Pilot data are public; the pipeline will be open-source on submission.

**3. Advancing Current Understanding and Generating New Knowledge**

Section 2 shows that scale-specific topological summaries exist, are reproducible, and respond coherently to match events at 10-match scale. The open question — and the new knowledge this project generates — is what holds at *population* scale (~540 Championship matches). **(i) Distributional laws:** do pilot stability scores, loop-presence rates and scale complementarity behave as population-level regularities, or vary systematically with tactical context? **(ii) Comparison geometry:** can standard distances between topological summaries [6,9] distinguish formation systems, giving a topologically grounded definition of formation identity? **(iii) Functional dynamics:** treating each match as a time series of topological summaries, what within-match stability regimes and transitions can be characterised? Each direction extends already-cited statistical topology tools [6,7,9] into a setting they have not yet reached: competitive, multi-scale, hierarchical systems. Establishing them here maps directly onto Objectives O1–O3 (§7).

**4. Timeliness, Need and Opportunity**

**Timeliness.** Three developments have recently converged: multi-scale topology theory has matured [4], and statistical tools now support inference across large samples [6,7,9]; software makes frame-by-frame topological computation feasible at season scale (§8), enabling but not constituting the contribution; and season-scale competitive tracking data have, to our knowledge, only recently become accessible.

**Need.** No validated workflow yet exists for multi-scale topological analysis of competitive, hierarchical, high-frequency systems. Analysts in sports — and, prospectively, health and economic sectors — need interpretable structural metrics that conventional geometric descriptors do not provide.

**Opportunity.** Their simultaneous arrival opens a window to settle these questions now, making the project timely rather than merely feasible.

**5. Impact**

**Impact on research.** The primary impact is to the mathematical sciences: a validated open-source library for multi-scale persistent homology on competitive, time-evolving point clouds, contributing to EPSRC's *physical and mathematical sciences powerhouse* priority and, as a systems approach to competitive dynamics, to *AI, digitisation and data* — building UK capability in applied topology.

**Economic and industry impact.** Co-developed with Swansea City AFC and data partners (StatsBomb, Genius Sports), the project translates topological measures into practitioner-interpretable tools for pressing structures, formation gaps and defensive-line organisation that geometric descriptors miss (§6).

**Stepping-stone to translation.** This project prepares a follow-on Standard Grant (§7, O4). The domain-validation procedure transfers to other bounded competitive systems once scales are re-derived. Pathways (not deliverables) include tumour–immune competition (*transforming health and healthcare*; Co-I Powathil) and competitive logistics / autonomous-fleet coordination (*AI, digitisation and data*). The full-season evidence base makes that larger programme fundable.

**6. Benefits and Beneficiaries**

**Direct beneficiaries:** the mathematical sciences community (open-source library); sports analytics practitioners — notably Swansea City AFC performance analysts as co-development partner — who gain practitioner-interpretable visualisations of pressing structures, formation gaps and defensive-line organisation that standard geometric descriptors (length, width, convex-hull area) do not directly quantify; and the wider sports-analytics research community. **Longer-term:** operators of other competitive multi-agent domains (§5); the proposed Standard Grant programme (§7, O4); and industry users adopting the open-source pipeline.

---

**APPROACH**

**7. Research Design and Objectives**

**Project Structure and Team.** This 12-month project comprises: (i) the PI (0.2 FTE), responsible for framework development, analysis oversight and publication; (ii) two Co-Investigators (0.25 FTE combined), providing statistical and domain expertise; (iii) a Research Associate (1.0 FTE, 9 months, Months 2–10), implementing the pipeline, running the full-season analysis and developing the landscape library; (iv) partnership with Swansea City AFC and StatsBomb for Championship tracking data and formation labels. Four objectives follow: three research objectives (O1–O3) and one strategic output (O4).

**Sample-size rationale.** A full Championship season (~540 matches) is sized for both precision and power. For subgroup inference, n ≈ 32 matches per stratum yields a 95% CI half-width of 0.025 on tactical-scale loop (H₁) presence (pilot across-match s.d. 0.072). For O2 formation comparisons, n ≈ 180 matches per tactical class detects an effect of Cohen's *d* ≥ 0.30 at power 0.80 and α = 0.05, with Benjamini–Hochberg FDR correction. A pilot estimate of the within-match half-effect on tactical-scale H₁ persistence is borderline (*p* = 0.051 [19]), consistent with match-specific dynamics; season-scale replication is designed to resolve it.

These objectives advance the §2 pilot to season scale, mapping directly onto §3 (i)–(iii):

**O1 — Population-level topological statistics** (PI and RA, Months 1–7). How do topological features vary across a full Championship season, and how do they relate to standard tactical descriptors from partner data? The PI establishes the Supercomputing Wales concurrent pipeline in Month 1. A 20-match Championship batch (Months 1–2) re-validates interaction-length cutoffs against [19]; stability below 0.80 triggers re-derivation and gates downstream work. The RA processes the full season (Months 2–7); the PI leads exploratory joint analysis (Months 5–7). *Milestone: cutoff gate (Month 2); barcode database (Month 7).*

**O2 — Topological fingerprinting** (PI, Months 6–9). Can different formation systems be distinguished by topological signatures, beyond what geometric shape metrics already capture? Formation labels come from StatsBomb and SkillCorner; inter-rater agreement (Cohen's κ) is checked before confirmatory tests, and hypotheses are pre-registered on the Open Science Framework in Month 2. Systems are compared using standard distances between averaged topological summaries [6,7] and vectorised diagram-image features (§8), benchmarked against team length, width and convex-hull area. Success criteria: distinct signatures for ≥3 tactical configurations; statistically significant between-system differences after FDR correction (*p* < 0.05); topological measures add information beyond the geometric baselines. *Milestone: OSF pre-registration (Month 2); fingerprint results (Month 9).*

**O3 — Temporal dynamics and phase transitions** (PI and RA, Months 4–10). Extending single-scale multi-agent change-point detection [14] to competitive, bounded, multi-scale systems (§2): does the within-match evolution of topological structure align with annotated tactical events (substitutions, formation changes)? The RA implements tracking of each match as a time series of topological summaries (Months 6–10). The PI applies functional principal component analysis [25] and CUSUM change-point detection [26], with bootstrap calibration [7]. Mathematical targets: well-posedness of the mean path in summary space under competitive sequential data, extending [7]; and a stability bound for the CUSUM statistic when summaries are perturbed in Wasserstein distance. Success criterion: detected change-points agree with held-out tactical annotations at ≥70% (permutation *p* < 0.05). If the landscape-based extension requires development beyond [6,7], direct Wasserstein comparison of diagrams is the defined fallback. *Milestone: landscape module (Month 8); combined O2/O3 outputs (Month 9).*

**O4 — Standard Grant evidence synthesis** (PI, Months 9–12). From Month 9, compile full-season results into a reproducible evidence pack for a **separate** follow-on application translating the framework to higher-impact adversarial systems (§5). Submission is targeted within 12 months of project completion. O1–O3 remain standalone publishable contributions independently of this strategic output. *Milestone: evidence pack (Month 12).*

**8. Methodology**

The analysis uses a containerised Python pipeline (Ripser [23], GUDHI, giotto-tda [24]) that computes homology in under 2 s per frame. Tracking data are processed through clustering at the validated interaction lengths, adaptive distance thresholds and barcode computation, then compared via diagram-image features, distances between averaged landscape summaries, and ANCOVA baselines against conventional shape metrics. The Month 1–2 gate confirms that cutoffs transfer to Championship data and that 1 Hz production sampling preserves fidelity before full-season commitment. Computational infrastructure and data access are detailed in §12.

**9. Feasibility and Risk Management**

**Feasibility.** The project is feasible within 12 months. Computation is modest and embarrassingly parallel — about 1,600 CPU-hours within a 5,000 core-hour allocation (§12). The schedule is de-risked by the Month-2 cutoff gate before full-season commitment (§7, §8), and the team holds the required topological, statistical and domain expertise (§11).

**Risk management.**


| Risk                  | Likelihood | Impact | Mitigation                                                                                                                           |
| --------------------- | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Data access           | Low        | High   | StatsBomb agreement confirmed for 2024/25; ~270-match contingency remains publishable for O1 (O2 exploratory only under contingency) |
| Scale transferability | Medium     | Medium | Month 2 validation gate re-derives cutoffs on Championship data                                                                      |
| Formation-label noise | Medium     | Medium | Dual-source verification, unsupervised clustering of topological summaries, pre-registered exclusion protocol                        |
| Landscape theory      | Medium     | Medium | Wasserstein fallback preserves O3 if sequential landscape extension requires further development                                     |




**10. Translation to Outcomes and Impact**

Open-source code will be archived via Swansea University's Zenodo community (DOI). The methodology paper [19] is submitted to arXiv and to the *Journal of Applied and Computational Topology* from Month 1; the football-analytics paper [22] targets the *Journal of Sports Sciences*; a full-season results and landscapes paper targets Month 11. Practitioner-facing outputs with Swansea City AFC, and the follow-on Standard Grant pathway, are detailed in §5.

**11. Research Environment**

Swansea University's Zienkiewicz Institute provides the computational mathematics research environment. Co-Investigator Professor Gibin Powathil brings mathematical-oncology expertise underpinning the planned health-sector pathway (§5); Professor Liam Kilduff (sport and exercise sciences) provides domain expertise for tactical interpretation. The established Swansea City AFC partnership supports co-development of practitioner outputs.

**12. Facilities, Infrastructure and Host Support**

Full-season processing requires ~1,600 CPU-hours; the Supercomputing Wales allocation (5,000 core-hours; PI's existing access) covers processing, gate batches and O3 computation with margin. Championship tracking data and formation labels are secured through the Swansea City AFC–StatsBomb agreement. Swansea University's Research Office supports partnership negotiation and provides fast-tracked ethics review.

---

**Project Timeline**


| Activity                           | M1  | M2  | M3  | M4  | M5  | M6  | M7  | M8  | M9  | M10 | M11 | M12 |
| ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pipeline setup & RA onboarding     | ■   |     |     |     |     |     |     |     |     |     |     |     |
| Cutoff gate & OSF pre-registration |     | ■   |     |     |     |     |     |     |     |     |     |     |
| Full-season computation (O1)       |     |     | ■   | ■   | ■   | ■   | ■   |     |     |     |     |     |
| Barcode database (O1)              |     |     |     |     |     |     | ■   |     |     |     |     |     |
| Fingerprinting (O2)                |     |     |     |     |     | ■   | ■   | ■   | ■   |     |     |     |
| Landscape methods (O3)             |     |     |     | ■   | ■   | ■   | ■   | ■   | ■   | ■   |     |     |
| O2/O3 outputs                      |     |     |     |     |     |     |     |     | ■   |     |     |     |
| Standard Grant synthesis (O4)      |     |     |     |     |     |     |     |     | ■   | ■   | ■   | ■   |


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