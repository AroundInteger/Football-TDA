# VISION AND APPROACH

<!-- JeS Vision & Approach. REVISION 4, 10 Sep 2026 (page-fit); gate rewrite 11 Sep 2026. Working draft.
     Base: 02_Vision_and_Approach_REV3.md (24 Aug 2026). STRIP this comment before submission.

     PURPOSE OF REV4 (10 Sep 2026): page-fit. REV3 measured 2,090 body words
     against a three-page allowance (Calibri 11 pt, A4, 2 cm margins,
     Figure 1 included, references excluded). Ceiling: 1,600 words hard
     (REVISION_DISCIPLINE.md), ~1,660 working. Cuts are deduplication and
     the §5 print-the-claim / cite-the-machinery rule.

     PIVOT 11 Sep 2026 (FOUNDATION.md ruling R15): Paper A cutoffs are
     cardinality inversions on SkillCorner (2.75 / 11.75 / 23.0 m). Only
     the §4 Month-2 gate is rewritten in this body so it matches [23];
     metres are not re-inserted (page budget ~35 words). Pilot s.d.
     0.072 -> 0.065; n=32 kept. Re-measure page 3 in the JeS/Word template
     before paste. CANONICAL_NUMBERS.md locked the same day. Papers B and
     C deferred. REV3 remains the archive of the 0.80 / collage-metre V&A.

     WORD-COUNT METHOD (fixed here so the target is not inherited):
       body = text between "## Vision" and "## References", this comment and
       the image line removed, headings and bold run-in labels counted.

     MEASURED 10 Sep 2026 (pandoc -> Word, A4, 2 cm, Calibri 11 pt, 3 pt after,
     Figure 1 at 13 cm wide): body 1,604 words, 102 sentences, mean 15.0 w,
     max 34 w; 3 pages, page 3 ends at line 44 of ~49. REV3 baseline was
     2,090 words / 4 pages (last paragraph on page 4 line 14).
     LAYOUT DEPENDENCY: the fit relies on Figure 1 sitting at the foot of
     page 2. Sensitivity test: +2 lines of text in §1-§4 still fits;
     +4 lines pushes the figure to page 3 and the document to 4 pages.
     Treat ~35 words as the margin before the figure. Re-measure in the
     JeS/Word template before submission.
     NEXT CUTS if the template is tighter (in order): §7 Team institute
     sentence (~14 w); §2 "generalises to any bounded competitive system"
     (~15 w); §3 National importance first sentence (~11 w); Figure 1 to
     12 cm wide (~1 line).

     COSTED LOCK (TIMELINE.md): PI 0.10 FTE; Co-I Villamizar 0.05 FTE;
     RA 1.0 FTE Months 5-10; Months 1-4 PI-led so the Month-2 gate and a
     runnable pipeline exist before the RA arrives.

     CUT ORDER APPLIED (see plan): A compress §5 T1/T2/Pipeline;
     C dedupe team/roles (§4 O2, §7 Team); D dedupe §1 opener against
     §2/§3/§7; E sweeps (§4 sample size, §6, §2, §3, §4 O1) only as far as
     the page requires.
     Fixed in passing: §3 "sequential adversarial dynamics" -> "competitive
     dependence" (locked terminology); §4 covariate/stratification ->
     opposition as covariate, venue x opposition strength (CANONICAL_NUMBERS.md);
     colon after bold leads in O1 and
     R1-R3 bullets (no em dashes); acronyms defined at first use (PI, FTE,
     Co-I, RA, BH-FDR, CUSUM, OSF; CI and TDA written out); Figure 1
     caption moved into the image alt text (pandoc was emitting two
     captions) and width fixed at 13 cm; §1 Importance/Scale, §1
     Mathematical contribution/T1 and §7 Team/Resources merged into single
     paragraphs to recover part-lines.
     Beyond the plan's A/C/D/E list, the page required further trims in
     §1 (agent-domain examples sentence), §2 (Timeliness closing sentence),
     §3 (Standard Grant drafting-date sentence), §4 (O2 method clause,
     Month-4 protocol clause, StatsBomb clause) and §5 (T2 finite-measure
     mechanics). No number, gate, citation or restoration was removed.
     Not cut: 1 Hz timing and the 10 Hz -> 1 Hz Month-2 check; geometric
     baselines [21,22]; OSF at Month 2; six-cell arithmetic and
     32 / 0.025 / 0.065; detection threshold vs localisation bound;
     R3 limit-law disclaimer; Months 1-4 PI-led sentence; all 29 citations.

     HISTORY: REV2 -> REV3 changelog, the OLD -> NEW reference renumbering
     map, and the toy-model ruling (FOUNDATION.md R8) are in the REV3 header.
     References: unsrtnat order of first appearance, 29 entries, all cited.
     Open actions carried from REV3: 04_References.md numbering (unchanged
     29 entries); Figure 1 relabel ("methods paper [23]", Month-2 cutoff
     gate and Month-9 O1 gate as separate diamonds, OSF M2).
     CANONICAL_NUMBERS.md synced 11 Sep 2026 to R15. -->

## Vision

### 1. Research Problem and Mathematical Contribution

When two groups of agents compete inside a bounded space, each shapes the other's organisation at every scale at once, and no statistical theory yet describes that record. Such competitive collective systems comprise two or more groups of agents that share a bounded domain, each coordinating internally while responding to the opposing group. Statistical topology cannot yet describe how such organisation forms, changes and breaks down; this project seeks that theory, averaging configurations at population scale and locating change with a proven error bound. The grant is a proof of principle on a fully tracked platform (professional football, §2) and the evidence base for a follow-on Standard Grant.

**Importance.** Two obstacles limit existing approaches. *Scale.* Organisation exists at several spatial scales at once, from small interaction groups to enclosed coverage regions. A single persistent-homology filtration over the full agent set does not separate these levels: their features interleave in one diagram [1–3]. Multiparameter persistence [4–6] is principled but computationally impractical at these data rates.

*Dependence.* Continuous mutual adaptation violates the exchangeability assumptions underpinning current statistical topology [7,8], so inference that treats observations as independent understates the uncertainty.

**Mathematical contribution.** The framework rests on two theorems this project seeks to prove (§5). **(T1) Averaging under competitive dependence is well posed.** The empirical mean path of landscape summaries converges under temporal mixing rather than exchangeability, with the long-run rather than the marginal covariance in the limit [7,9,10]. Competitive dependence does not move the mean; it changes every variance built on it.

**(T2) Transitions are localised with a proven error bound.** The bound depends on the size of the change, T1's long-run variance and the worst-case perturbation of the input diagrams [11–14]. Below a threshold set by that perturbation, a transition cannot be located. Both are explicit, checkable claims with named failure conditions; O1 establishes their geometry and O2 carries the proofs (§4, fallback §6).

### 2. Background, Timeliness, Need and Opportunity

Established topological results assume cooperative or slowly evolving organisation: biological aggregation, collective motion and flocking [15–17], and topological change-point detection [18]. These rely on persistent homology [1,2] and its statistical summaries [7,8,19], which are stable under small measurement error [8,11]. Multi-scale methods exist for slowly evolving systems [20]; competitive systems are still described by single-scale geometric descriptors [21,22]. Our ten-match pilot [23] recovers three stable connected-component regimes and two complementary loop regimes, with the scales carrying largely independent information.

**Timeliness.** Multi-scale topology and statistical comparison tools have matured [4,6–8,19], scalable computation supports rigorous analysis at population scale, and fully labelled competitive tracking data exist at that scale.

**Need and opportunity.** No validated statistical-topology workflow exists for continuously competing systems. Professional football is the platform: all agents are tracked within strict boundaries and domain experts can verify results. The framework generalises to any bounded competitive system once interaction lengths are re-derived.

### 3. Impact, National Importance and Beneficiaries

**Mathematical impact.** The primary contribution is new statistical-topology theory extending current foundations [7,8] to competitive dependence. Beneficiaries are researchers in topology, statistics and complex systems, who gain the foundations and an open-source library.

**National importance.** UK groups lead internationally in statistical topology and stochastic geometry. This project develops UK capability at that frontier: sequential inference for function-space-valued topological summaries under competitive dependence.

**Economic and industry impact.** Co-developed with Swansea City AFC (SCAFC), the project delivers practitioner outputs unavailable from the geometric measures benchmarked in O1, for sports analytics researchers and practitioners.

**Standard Grant pathway.** The T1 and T2 foundations prepare a follow-on Standard Grant transferring the guarantees to two further bounded competitive systems: spatial predator–prey dynamics (including tumour–immune competition with mathematical-oncology collaborators) and competitive logistics with autonomous-fleet coordination.

## Approach

### 4. Research Design and Objectives

**Project structure.** The Principal Investigator (PI; 0.10 full-time equivalent, FTE) leads the framework, analysis and publication. Co-Investigator (Co-I) Dr Nelly Villamizar (Mathematics, 0.05 FTE) supplies algebraic and topological guidance for O2. A Research Associate (RA; 1.0 FTE, Months 5–10) implements season-scale compute and the landscape library on SCAFC tracking data and tactical labels. Months 1–4 are PI-led so the Month-2 gate and a runnable pipeline exist before the RA arrives. The post is structured postdoctoral training in statistical topology and sequential inference.

**Sample-size rationale.** A full Championship season supplies the replication the pilot cannot: 552 fixtures, about 540 after pre-registered exclusions (R2). The unit is the fixture (one focal team, opposition as covariate), so the two dependent teams are not double-counted. Venue × opposition strength gives six cells of about 90 matches, each above the 32 needed for a 95% confidence-interval half-width of 0.025 on the tactical-scale loop-presence rate (pilot across-match s.d. 0.065 [23]). Phase of play is a within-match stratum and does not partition matches. For formation comparison, 180 matches per class detect Cohen's d ≥ 0.30 at 80% power (α = 0.05, Benjamini–Hochberg false-discovery-rate control, BH-FDR); 540 matches cover the three most common formations, the pre-registered comparison set. The replication target is a borderline within-match pilot effect (stratified permutation p = 0.051).

**O1: Population-scale geometry (PI Months 1–9; RA Months 5–9).** O1 tests whether scale-specific summaries are stable enough to average at population scale and whether their distances distinguish organisational states (in football, tactical formations). A 20-match validation batch in Months 1–2 tests whether the pilot interaction lengths transfer to Championship data, and whether 1 Hz sampling preserves the features validated at 10 Hz.

- **Cutoff acceptance** (gate, Month 2): invert the cardinality rules of [23] on the validation batch; a match outside a named connected-component band triggers re-derivation.
- **Dependence diagnostic** (gate, Month 9): empirical autocovariance decay consistent with the summable-mixing condition T1 and T2 assume, with the eigengap for T2's projected form recorded alongside.
- **Discriminability** (gate, Month 9): separation of at least three organisational states (p < 0.05, BH-corrected), benchmarked against team length, width and convex-hull area [21,22].

**O2: Inference for dependent topological processes (PI Months 4–10; RA and Co-I Months 5–10).** The Month-2 gate licenses O2; the Month-9 criteria are the hypotheses under which T1 and T2 are to be proved (§5). O2 succeeds if both theorems hold under the O1 conditions and detected change-points recover at least 70% of held-out annotated transitions within ±10 s at a calibrated 5% false-alarm rate (permutation p < 0.05).

![**Figure 1.** Twelve-month workplan: decision gates (diamonds) and dated outputs (triangles).](grant_figure_gantt.png){width=13cm}

### 5. Methodology

**Pipeline.** A containerised Python pipeline processes each match frame as a point cloud. Agents are partitioned using the empirically derived interaction lengths (§2; Month-2 gate). Persistent homology at each accepted scale is computed with Ripser [24], GUDHI [25] and giotto-tda [26] and summarised as persistence landscapes. Frame-level homology takes under two seconds and is embarrassingly parallel, so production runs at 1 Hz. For O1, landscape distributions are compared across organisational states and covariate cells by the landscape L² distance (permutation tests, BH-FDR).

**T1.** On a bounded domain with a fixed agent count, landscapes are uniformly bounded in L² [8], so the mean path is well defined and unique, unlike diagram-valued means [27]. For a strictly stationary, α-mixing landscape series with summable coefficients, the empirical mean path is √n-consistent with a Gaussian limit whose covariance is the long-run, not the marginal, covariance [9,10]. That licenses functional principal component analysis (FPCA) [28] on landscape trajectories and block-bootstrap calibration.

**T2.** The landscape map is 1-Lipschitz from diagrams under the bottleneck distance into the sup-norm [8], and on a bounded domain into L² with a constant C explicit in agent count and domain diameter [14]. For a functional cumulative-sum (CUSUM) statistic [12,13] on the landscape series, T2 bounds the localisation error by

|τ̂ − τ| = O_P( σ² / (Δ − 2Cε)² ),  for Δ > 2Cε,

where Δ is the change in the mean landscape, σ² is T1's long-run variance and ε is the worst-case diagram perturbation. The threshold Δ > 2Cε is the substantive content: a transition is locatable only once it exceeds twice the measurement-induced perturbation. Block-bootstrap calibration sets the detection threshold at a fixed false-alarm rate; the bound sets the localisation window reported with each detection. T2 is stated on the landscape series; its projected form on FPCA scores also needs the eigengap condition recorded in O1.

### 6. Feasibility and Risk Management

The project is feasible in twelve months: the method is pilot-validated (§2), data access is secured through the SCAFC agreement, and the computational budget is modest (§7). Three risks remain.

- **(R1) Scale transferability**: medium likelihood, high impact. Without transferable interaction lengths averaging is not meaningful; the Month-2 cutoff gate mitigates this.
- **(R2) Label uncertainty**: medium likelihood, low impact. Dual-source verification, Cohen's κ and Open Science Framework (OSF) pre-registered exclusions mitigate this. Labels affect the interpretation of O1, not the theorems.
- **(R3) Landscape theory**: low likelihood, medium impact. If the landscape argument proves intractable, O2 falls back to the diagram-valued Wasserstein comparison already demonstrated in the pilot. The T1 limit law is then not claimed.

### 7. Outcomes, Team and Resources

**Publications and software.** The methodology paper [23] is submitted. The dated deliverables in Figure 1 are a season-results paper, a football-analytics paper [29], a Zenodo library DOI and SCAFC practitioner outputs. The analysis plan is pre-registered on OSF at Month 2. These form the Month-12 evidence pack for the Standard Grant (§3).

**Team.** The project is based at Swansea University's Zienkiewicz Institute for Modelling, Data and AI. It brings together statistical topology for competitive systems (PI, Biomedical Engineering), applied algebraic geometry and topological methods (Co-I Villamizar, Mathematics) and SCAFC as industry co-development partner. This new cross-school and industry collaboration fits the scheme's remit. **Resources.** Full-season processing uses the PI's Supercomputing Wales allocation: approximately 1,600 of 5,000 available CPU-hours.

## References

*Numbered in order of first appearance (unsrtnat convention). All 29 entries are cited.*

1. Carlsson, G. (2009). Topology and data. *Bulletin of the American Mathematical Society*, 46(2), 255–308.
2. Zomorodian, A. & Carlsson, G. (2005). Computing persistent homology. *Discrete & Computational Geometry*, 33(2), 249–274.
3. Edelsbrunner, H. & Harer, J. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
4. Botnan, M. B. & Lesnick, M. (2022). An introduction to multiparameter persistence. In *Representations of Algebras and Related Structures* (pp. 77–150). EMS Press.
5. Lesnick, M. (2015). The theory of the interleaving distance on multidimensional persistence modules. *Foundations of Computational Mathematics*, 15(3), 613–650.
6. Schenck, H. (2022). *Algebraic Foundations for Applied Topology and Data Analysis*. Mathematics of Data, vol. 1. Springer, Cham. doi:10.1007/978-3-031-06664-1. Chapter 8 treats the algebraic foundations of multiparameter persistent homology.
7. Chazal, F., Fasy, B. T., Lecci, F., Rinaldo, A. & Wasserman, L. (2014). Stochastic convergence of persistence landscapes and silhouettes. *Proceedings of the 30th Annual Symposium on Computational Geometry*, 474–483.
8. Bubenik, P. (2015). Statistical topological data analysis using persistence landscapes. *Journal of Machine Learning Research*, 16(1), 77–102.
9. Bosq, D. (2000). *Linear Processes in Function Spaces: Theory and Applications*. Lecture Notes in Statistics 149. Springer.
10. Hörmann, S. & Kokoszka, P. (2010). Weakly dependent functional data. *Annals of Statistics*, 38(3), 1845–1884.
11. Cohen-Steiner, D., Edelsbrunner, H. & Harer, J. (2007). Stability of persistence diagrams. *Discrete & Computational Geometry*, 37(1), 103–120.
12. Page, E. S. (1954). Continuous inspection schemes. *Biometrika*, 41(1/2), 100–115.
13. Berkes, I., Gabrys, R., Horváth, L. & Kokoszka, P. (2009). Detecting changes in the mean of functional observations. *Journal of the Royal Statistical Society: Series B*, 71(5), 927–946.
14. Cohen-Steiner, D., Edelsbrunner, H., Harer, J. & Mileyko, Y. (2010). Lipschitz functions have L^p-stable persistence. *Foundations of Computational Mathematics*, 10(2), 127–148.
15. Topaz, C. M., Ziegelmeier, L. & Halverson, T. (2015). Topological data analysis of biological aggregation models. *PLoS ONE*, 10(5), e0126383.
16. Bhaskar, D. et al. (2019). Analysing collective motion with machine learning and topology. *Chaos*, 29(12), 123125.
17. Ballerini, M. et al. (2008). Interaction ruling animal collective behaviour depends on topological rather than metric distance. *PNAS*, 105(4), 1232–1237.
18. Gu, K. et al. (2022). Change point detection in multi-agent systems based on higher-order features. *Chaos*, 32(11), 113117.
19. Adams, H. et al. (2017). Persistence images: a stable vector representation of persistent homology. *Journal of Machine Learning Research*, 18(8), 1–35.
20. Schindler, D. J. & Barahona, M. (2023). Analysing multiscale clusterings with persistent homology. arXiv:2305.04281.
21. Folgado, H. et al. (2014). Length, width and centroid distance as measures of teams' tactical performance in youth football. *European Journal of Sport Science*, 14(S1), S487–S492.
22. Fernández, J. & Bornn, L. (2018). Wide open spaces: a statistical technique for measuring space creation in professional soccer. *Sloan Sports Analytics Conference*.
23. Brown, R. et al. (2026). Multi-scale persistent homology for competitive spatial systems: measurement-aware methods and validation in professional football. Manuscript submitted to the *Journal of Applied and Computational Topology*.
24. Bauer, U. (2021). Ripser: efficient computation of Vietoris–Rips persistence barcodes. *Journal of Applied and Computational Topology*, 5(3), 391–423.
25. Maria, C., Boissonnat, J.-D., Glisse, M. & Yvinec, M. (2014). The Gudhi library: simplicial complexes and persistent homology. In *Mathematical Software – ICMS 2014* (pp. 167–174). Springer.
26. Tauzin, G. et al. (2021). giotto-tda: a topological data analysis toolkit for machine learning and data exploration. *Journal of Machine Learning Research*, 22(39), 1–6.
27. Turner, K., Mileyko, Y., Mukherjee, S. & Harer, J. (2014). Fréchet means for distributions of persistence diagrams. *Discrete & Computational Geometry*, 52(1), 44–70.
28. Ramsay, J. O. & Silverman, B. W. (2005). *Functional Data Analysis* (2nd ed.). Springer.
29. Brown, R. et al. (2026). Multi-scale topological signatures of tactical organisation in professional football. In preparation; to be submitted to the *Journal of Sports Sciences*.
