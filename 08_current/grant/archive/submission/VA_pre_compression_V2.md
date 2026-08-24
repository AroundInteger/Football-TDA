**VISION**

**Mathematical Importance and Quality.** Competitive spatial systems,
collections of agents that coordinate internally while opposing an
adversary within a bounded domain, are a ubiquitous class in applied
mathematics. What distinguishes them from cooperative swarms or static
aggregations is adversarial geometry: the spatial configuration of each
group is continuously deformed by the presence and actions of the
opposing group. This produces topological structure simultaneously at
multiple organisational scales: loops in the individual-scale point
cloud (small player groups encircling space), loops in the
tactical-scale reduced cloud (formation gaps, pressing shapes), and
whole-system organisation.

Topological Data Analysis, and persistent homology in particular,
provides the natural framework for studying such structure \[1,2\]: by
constructing a filtration of simplicial complexes and tracking the birth
and death of topological features, it captures multi-scale spatial
organisation in a mathematically rigorous way. Standard single-parameter
Vietoris--Rips persistent homology \[3\] applied to the full competitive
point cloud, however, conflates all of these organisational levels into
a single persistence diagram, making scale-specific attribution and
temporal tracking of scale dynamics analytically intractable. This is
not a modelling choice but a structural limitation: adversarial
interactions force geometrically distinct organisational scales to
coexist within overlapping filtration ranges.

This challenge is recognised across the TDA literature. Topaz et
al. \[4\] visualise Betti numbers across both simulation time and
filtration value to identify scale-dependent structure in biological
aggregations, but in cooperative, non-adversarial settings. Schindler
and Barahona \[5\] develop rigorous tools for analysing multiscale
clusterings with persistent homology, directly addressing hierarchical
decomposition, but again in cooperative, quasi-static contexts where
adversarial geometry is absent. Gu et al. \[6\] apply Vietoris--Rips
persistent homology to multi-agent snapshots for change-point detection,
demonstrating topological features as temporal indicators, but at a
single analysis scale. Multiparameter persistence \[7,8\] provides
algebraic machinery for simultaneous multi-scale analysis, but current
computational barriers prevent practical application to point clouds of
the size and temporal density encountered here.

Our framework takes a complementary, domain-informed route: hierarchical
clustering at empirically validated cutoff distances decomposes the
competitive point cloud by organisational level before standard
single-parameter persistent homology is applied at each level. The
contribution is not the use of clustering per se, but the demonstration
that hierarchical decomposition provides a principled, scalable
alternative where single-parameter Vietoris--Rips on the full
competitive cloud fails through structural attribution intractability,
and multiparameter persistence --- while algebraically motivated --- is
computationally impractical at this data scale and temporal density;
stability-validated cutoffs make the decomposition falsifiable
(domain-determined scales, not free parameters) and transferable across
competitive systems. This makes three specific mathematical
contributions beyond prior work.

***First***, *domain-validated scale identification for competitive
systems*: a systematic parameter sweep over the clustering cutoff
distance, evaluated by multiple quality metrics, identifies stable
regimes with cross-epoch stability scores of 0.88, 0.97, and 1.00
(individual, tactical, team; computed from the validation sweep
described in \[12\]). This replaces heuristic filtration parameter
choices, the dominant practice in applied TDA, with a reproducible,
domain-grounded procedure that makes the scale decomposition falsifiable
and transferable.

***Second***, *adaptive filtration for multi-scale H₁ detection*: a
data-driven maximum filtration formula adjusting to post-clustering
geometry at each scale. Ablation across percentiles P50--P95 confirms
that H₁ barcode outputs are insensitive to the maximum-filtration
parameter value across all tested values --- robustness of the
filtration cap itself, independently of the adaptive computation that
set it --- consistent with the stability guarantees of Cohen-Steiner et
al. \[9\].

***Third***, *persistence landscape theory for competitive sequential
diagrams* \[10,11\]: extending the statistical framework of Bubenik
\[10\] and Chazal et al. \[11\] to treat each match as a path t → λδ(t)
in landscape function space, enabling CUSUM change-point detection of
topological phase transitions, to our knowledge the first rigorous
framework for classifying stability regimes in competitive encounters.

Together these constitute a practical advance in computational topology:
validated methods for multi-scale persistent homology on hierarchical,
competitive, time-evolving point clouds, where existing literature
provides either algebraic theory without practical scalability, or
scalable methods without competitive or validated multi-scale structure.

**Preliminary Validation.** The framework is validated across 10
professional football matches (SkillCorner open broadcast tracking,
10 Hz; 104,722 event--topology pairs) \[12\]. Professional football is
an ideal mathematical testbed: high-frequency spatial measurements,
well-defined hierarchical structure, and established standards for
positional data collection \[13,14\]. Three H₀ regimes, individual
(2.98 m), tactical (12.0 m), team (30.0 m), are confirmed with
cross-epoch stability scores of 0.88, 0.97, and 1.00 respectively
(computed from the validation sweep described in \[12\]). Two H₁ regimes
emerge. Individual-scale loops (97.0% ± 1.5% frame presence, 95% CI
\[96.1%, 97.9%\]) are near-universal and transient; tactical-scale loops
(19.3% ± 7.2%, 95% CI \[15.3%, 23.7%\]) are rarer but geometrically more
persistent (mean 3.80 m vs 1.98 m). The hierarchical decomposition
partitions filtration parameter space by construction, ensuring the two
H₁ scales address geometrically distinct regimes; non-redundancy --- the
empirically relevant property --- is confirmed separately: Spearman ρ =
0.254 (95% bootstrap CI \[0.200, 0.314\]) indicates low redundancy
between the two scale-specific features, with no evidence of the
near-unity correlation that would render one scale superfluous.
Topological features respond coherently to match dynamics: on-ball
engagements and quick breaks are associated with decreased persistence
(p \< 0.001), build-up phases with increased persistence (p \< 0.001),
with effect signs consistent across event-window half-widths of
±0.5--5 s. All data are from the public SkillCorner repository; the
Python pipeline will be open-source released with journal submission.

*\[FIGURE PLACEHOLDER --- S7b: Three-scale pilot validation figure: (a)
cutoff stability sweep (parameter sweep vs stability score, three H₀
regimes marked); (b) H₁ regime comparison (individual vs tactical: frame
presence, persistence, diameter); (c) topological event-response by
event type (±SE bands). Lifts number-wall from Preliminary Validation
prose. Insert and typeset before compression step.\]*

**Timeliness and Beneficiaries.** The Botnan and Lesnick survey \[7\]
marks theoretical maturity in multiparameter persistence; practical
validated workflows for domain-informed competitive systems are the gap
the field is ready to fill. Simultaneously, professional tracking
datasets have reached the scale --- a Championship season exceeds 500
matches --- at which population-level topological statistics are
computationally tractable for the first time. Direct beneficiaries: the
mathematical sciences community gains a validated open-source Python
library for multi-scale persistent homology on competitive point clouds
--- to our knowledge the first reproducible workflow for this class of
system, since existing TDA implementations handle cooperative or
quasi-static data but not adversarial, hierarchical, time-evolving
structure. Sports analytics practitioners gain a continuously computable
tactical shape measure validated at Championship scale; Swansea City
AFC's performance analysts, as co-development partner, receive
practitioner-interpretable visualisations of pressing structures,
formation gaps, and defensive line organisation that standard geometric
descriptors (team length, width, convex-hull area) do not directly
quantify. Indirect beneficiaries include autonomous vehicle coordination
researchers and ecological monitoring practitioners, for whom the
domain-validation procedure --- cutoff sweep, stability scoring,
adaptive filtration --- transfers to any competitive multi-agent system
once characteristic interaction scales are re-derived on system-specific
spatial data.

**National Importance.** This project directly strengthens the UK
mathematical sciences base by delivering rigorously validated
computational topology methods for competitive, hierarchical,
time-evolving point clouds --- a system class currently absent from TDA
toolkits worldwide. The open-source library and Championship-scale
dataset establish durable UK research infrastructure in applied
algebraic topology, aligned with EPSRC mathematical sciences priorities.
The Swansea City AFC--StatsBomb partnership demonstrates mathematically
driven engagement with the UK sports analytics industry; the
domain-validation methodology --- cutoff sweep, stability scoring,
adaptive filtration --- transfers to autonomous systems coordination,
ecological monitoring, and biological multi-scale modelling, multiplying
cross-disciplinary research return on EPSRC investment.

**APPROACH**

**Sample-size rationale.** The ∼540-match target is powered across all
three objectives. For O1, the 10-match pilot yields an across-match
standard deviation of 0.072 for tactical-scale H₁ presence rate;
achieving a 95% CI half-width of 0.025 --- appropriate for subgroup
inference by phase-of-play, opponent strength, and venue --- requires
n ≈ 32 matches per subgroup, so a full Championship season comfortably
supports the planned 5--10 covariate strata. A pilot linear mixed model
of the within-match half-effect on tactical-scale H₁ persistence gives
β̂₁ = −0.081 (LMM p = 0.079, stratified permutation p = 0.051; Brown et
al., in preparation), borderline at α = 0.05 and consistent with the
match-specific dynamics interpretation; cross-match replication at
season scale is what resolves it. For O2, a two-sample landscape L²-norm
comparison with n ≈ 180 matches per tactical class detects Cohen's
d ≥ 0.30 at power 0.80 (α = 0.05, Benjamini--Hochberg FDR correction).

*\[FIGURE PLACEHOLDER --- S7a: Compact Gantt chart (12-month, 7-row).
Rows: O1--PI (pipeline setup M1, analysis M5--7), O1--RA (processing
M2--7, D1 ◆M7), O2--PI (fingerprinting M6--9, D2 ◆M9), O3--PI+RA
(landscape M4--10, module ◆M8, D2 ◆M9), O4--PI (synthesis M10--12, D3
◆M12); Milestones: M2 cutoff gate ◆, M7 D1 ◆, M8 landscape module ◆, M9
D2 ◆, M12 D3 ◆. RA 1.0 FTE M2--10; PI 0.2 FTE throughout. Insert and
typeset before compression step.\]*

**Objectives.** Three mathematical research objectives and one strategic
output are pursued over 12 months, extending our submitted preliminary
work \[12\], building directly on the landscape theory foundations of
Bubenik \[10\] and Chazal et al. \[11\], and informed by the multiscale
clustering framework of Schindler and Barahona \[5\]:

**O1, Population-level topological statistics** (PI and RA, Months
1--10): PI establishes a Supercomputing Wales concurrent processing
pipeline in Month 1 (Ripser H₀+H₁, embarrassingly parallel by match;
∼1,600 CPU-hours at 1 Hz (see Methodology and Feasibility)). A 20-match
Championship batch in Months 1--2 re-validates the three cutoff
distances (δ = 2.98, 12.0, 30.0 m) on English professional football data
before full-season execution is committed; stability scores below 0.80
trigger cutoff re-derivation, gating all downstream objectives. RA
(Months 2--7) processes the full ∼540-match dataset, delivering D1. PI
conducts exploratory joint analysis of H₀/H₁ distributions against
StatsBomb match-level tactical descriptors (Months 5--7), testing
whether topological statistics vary systematically with formation,
competition phase, or opponent quality, positioning barcode statistics
relative to established KPIs.

*Milestone: cutoff gate (Month 2); D1 (Month 7).*

**O2, Topological fingerprinting of tactical systems** (PI, Months
6--9): Formation labels drawn from the StatsBomb commercial feed
(Swansea City AFC partnership) and SkillCorner broadcast annotation as
an independent parallel source; Cohen's κ inter-rater reliability
computed on the full label overlap before any confirmatory test, with
κ-flagged disagreements resolved by manual review against broadcast
clips or documented exclusion (exclusion list frozen in the Month 2
pre-registration). Persistence diagrams compared using two complementary
metrics: a persistence-image kernel for vectorised classification and
landscape L²-distance for continuous contrasts. Non-redundancy of
topological fingerprints tested by ANCOVA against geometric baselines
(team length, width, convex-hull area, Voronoi dispersion entropy) after
adjusting for all four covariates jointly. Hypotheses pre-registered on
OSF (Month 2) before full-season results are examined.

*Milestone: OSF pre-registration (Month 2 --- pre-registers O2 and O3
hypotheses before full-season data are examined); D2 (Month 9).*

**O3, Temporal dynamics and phase transition classification** (PI and
RA, Months 4--10): RA implements the persistence landscape computational
library in Months 6--10: λδ(t) computation at both validated scales,
Fréchet mean landscapes per tactical class, and inter-landscape
L²-distance routines (contributing to D2). PI applies functional
principal component analysis (FPCA) to within-match landscape paths to
extract low-dimensional tactical modes, and CUSUM change-point detection
on running L²-norm increments to identify topological phase transitions.
Change-point alignment against tactical annotations (substitutions,
formation changes) is assessed by permutation test (p \< 0.05). The
stated mathematical targets are: (i) well-posedness and stability of the
Fréchet mean in landscape function space under the competitive
sequential setting, extending the static-diagram framework of Chazal et
al. \[11\] to adversarial temporal paths; and (ii) a stability bound for
the CUSUM detection statistic under Wasserstein perturbations of the
underlying persistence diagrams. Should these extensions require
theoretical development beyond current landscape theory, Wasserstein
distance comparison provides a defined fallback preserving the O3
temporal dynamics objective.

*Milestone: landscape module complete (Month 8); D2 (Month 9).*

**O4, Standard Grant evidence synthesis** (PI, Months 10--12): Compile
full-season results and landscape methods into a reproducible evidence
base for a Standard Grant application extending the framework to broader
competitive multi-agent systems. O1--O3 are standalone publishable
contributions independently of this strategic output.

**Methodology and Feasibility.** The Python pipeline (Ripser \[15\],
GUDHI, giotto-tda \[16\]; \<2 s per frame; containerised with Apptainer)
processes tracking data through clustering, adaptive filtration, and
barcode computation. For O1, the pipeline runs across the 2024/25
Championship season under the Swansea City AFC--StatsBomb data
agreement. Computation: ∼540 matches × ∼5,400 frames (1 Hz; 90-minute
match, downsampled from the 10 Hz pilot) = ∼2.9M frames; at \<2 s per
frame, ∼1,600 CPU-hours. Supercomputing Wales initial allocation of
5,000 core-hours covers full-season processing (∼1,600 hours),
Month 1--2 gate batch runs, any failed-gate re-derivation, and O3
landscape computation, with ample margin. The Month 1--2 gate includes a
frame-rate sensitivity check at 0.5, 1, and 2 Hz to confirm that
topological features identified at 10 Hz in the pilot are preserved at
the 1 Hz production rate before full-season commitment. Batch testing on
20 matches in Months 1--2 validates scale stability and pipeline
integrity before full-season execution.

**Risk Management.** **Data access:** StatsBomb agreement confirmed for
the full 2024/25 EFL Championship season (broadcast tracking data and
formation label feed); ∼270 matches is sufficient for O1
population-level distributional claims and remains independently
publishable; under this contingency, O2 confirmatory fingerprinting is
underpowered for the full multi-class comparison (n ≈ 180 per class
required) and would be reported as exploratory landscape-space analysis
only. **Scale transferability:** the three validated cutoffs (δ = 2.98,
12.0, 30.0 m) were derived from A-League broadcast data; Championship
pitches and tracking pipelines differ. Mitigation: the 20-match gate in
Months 1--2 (O1) re-derives cutoffs on Championship data before
full-season execution is committed; stability scores below 0.80 trigger
cutoff re-derivation, preventing propagation of competition-specific
artefacts. Either outcome --- confirmed transferability or identified
divergence --- yields publishable mathematical insight into the limits
of topological structure transferability. **Formation-label noise:**
StatsBomb labels may lag real in-match formation changes, introducing
noise into O2's topological fingerprints. Mitigation: dual-source label
verification (StatsBomb and SkillCorner, Cohen's κ on full overlap; O2)
and a parallel unsupervised landscape-space clustering analysis
independent of formation labels; objectives are reported against
whichever labelling scheme shows higher internal consistency, with
disagreements documented in the pre-registered exclusion protocol.
**Landscape theory:** competitive sequential landscape extension may
require non-trivial mathematical development beyond Bubenik \[10\];
Wasserstein distance comparison provides a defined fallback preserving
the O3 temporal dynamics objective. **Personnel:** the RA (1.0 FTE, 9
months, Months 2--10) leads O1 full-season pipeline execution (D1, Month
7) and implements persistence landscape computational infrastructure for
O3 (Months 6--10); a 9-month appointment improves recruitment viability
for a specialist computational topology post and gives the RA a defined
contribution to the analytical phase rather than purely to data
processing. PI-led mathematical analysis (O2, O3, O4) begins in Month 4,
running in parallel once the first Championship barcodes are available.
The Month 6--7 overlap in RA tasks --- completing O1 full-season
processing (D1, Month 7) while initiating O3 landscape library
implementation (Month 6) --- is a planned feature of the 9-month
appointment; either task can be prioritised if the other runs behind
schedule, and the Month 7 milestone provides a checkpoint for workload
redistribution. Monthly computational milestones (Months 2, 4, 7, 9)
allow early identification of pipeline or data access delays.

**Deliverables**

**D1, Full-season barcode database** (Month 7, RA primary deliverable):
reproducible Parquet/HDF5 store of H₀ and H₁ diagrams at both validated
scales for all ∼540 Championship matches, with per-match metadata and
provenance hashes.

**D2, Landscape library \[O3\] and pre-registered tactical fingerprint
analysis \[O2\]** (Month 9, PI-led): Python module computing persistence
landscapes, Fréchet means, and CUSUM change points at both scales (O3
component, RA implements Months 6--10; PI integrates); and headline
tactical fingerprint results from the formation-label analysis delivered
against the Month 2 OSF pre-registration (O2 component, PI Months 6--9).

**D3, Standard Grant evidence pack** (Month 12, PI-led): synthesised
evidence base, figures, tables, and prose, ready for incorporation into
the follow-on Standard Grant proposal.

**Translation to Impact.** The open-source Python library is released
with journal submission and archived via Swansea University's
institutional Zenodo community with a minted DOI, consistent with the
reproducibility ethos of the preliminary work. Tactical outputs are
co-developed with Swansea City AFC as practitioner-interpretable
visualisations. Pilot data are from the publicly available SkillCorner
open broadcast repository \[12\]; full-season data are provided under
the Swansea City AFC--StatsBomb research partnership (commercial feed,
restricted access). Paper 1 (methodology, \[12\]) is submitted to ArXiv
and to JACT (Journal of Applied and Computational Topology) for peer
review from Month 1 \[update to 'under review' at submission if timing
aligns\]; Paper 2 (football analytics; Brown, Powathil and Kilduff, in
preparation) targets *Journal of Sports Sciences*; Paper 3 (full-season
results and persistence landscapes) targets submission in Month 11.
Dissemination targets two complementary conferences: SIAM Conference on
Applied and Computational Discrete Algorithms (ACDA27, Pittsburgh,
February 2027), where the algorithmic contributions --- pipeline design,
adaptive filtration, and scale identification --- are directly in scope;
and the International Congress on Industrial and Applied Mathematics
(ICIAM 2027, The Hague, July 2027), where the broader mathematical
framing and population-level results will reach the widest applied
mathematics audience and strengthen the case for the subsequent Standard
Grant.

**Research Environment.** Swansea University's Zienkiewicz Institute for
Modelling, Data and AI provides the computational and collaborative
infrastructure for this project. Supercomputing Wales (2 Petaflops; PI
has existing allocation) delivers the ∼1,600 CPU-hour processing
requirement within standard access limits. The Swansea City
AFC--StatsBomb data agreement provides secured Championship broadcast
tracking data and formation labels; the Research Office supports
partnership negotiation, provides fast-tracked ethics review (4-week
turnaround), and advises on IP arising from industry-facing outputs
developed through the partnership. Co-investigator Professor Gibin
Powathil (Mathematics) brings active research in mathematical modelling
of complex systems, including multi-scale biological dynamics;
Co-investigator Professor Liam Kilduff (Sport and Exercise Sciences)
brings established industry partnerships with professional sport
organisations and expertise in performance analytics at Championship
level. Both Co-Is have supervised industry-embedded doctoral students
(INEOS, Swansea City AFC, Ospreys, Scarlets). Open-science outputs are
archived via Swansea University's institutional Zenodo community (see
Translation to Impact).
