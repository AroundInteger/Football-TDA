# Publication-domain decisions (adversarial TDA, non-football)

**Date:** 2026-08-21 (locked after the literature check below).  
**Purpose:** Record what the methods note is — and is not — relative to the domain brainstorm. UK English.

The brainstorm asked three questions. They are now closed. A later prospectus (Tier 1–3 lemmas, Movebank as Domain 1) was merged on 2026-08-21: **take the tiers and T1-lite / T2-lite; keep simulation-only ecology; do not submit to JACT; T2-lite is stated on $W_1(D_t,D_{\mathrm{ref}})$, not consecutive-frame $W_1$.**

| Question | Decision |
|----------|----------|
| Methods/toy paper vs single-domain field paper | **Methods / synthetic now.** Submittable in the Small Grant window. Two simulated domains (ecology lead, robotics second). No Movebank, MIBI, or LOBSTER in this manuscript. |
| New domain collaborator | **Not a cold call.** The PI is already a co-author with the Swansea bio-logging group (Gunner, Wilson, Lurgi, Börger, Shepard, Redcliffe, Holton). They frame $\hat T$ and the observational follow-on. Invitation onto this author line is still open. |
| Before or after the Standard Grant | **Before.** The paper is the panel-confidence object: complementary fields on one workflow, not a speculative transfer sentence. |
| Contribution weight | **Three tiers**, stated in the introduction. Tier 1 cite Cohen–Steiner / Carlsson–Mémoli / Page. Tier 2 prove T1-lite and T2-lite (`lemmas.md`). Tier 3 conjecture full competitive dependence; Monte Carlo only. |
| Football in this manuscript | One paragraph plus a pointer to Paper A. Not a full validation section; not JACT. |

Honest bound: complementary fields is a **team and Outlook** claim, not “the same barcode in four domains.” Fig 5 of the football toy remains a schematic, not a transfer test.

---

## What the model needs (unchanged)

Two or more populations as point clouds in a bounded domain; a real competitive coupling (not two independent processes that happen to coexist); temporally dependent observations; and, ideally, more than one characteristic length. Missing the coupling collapses the problem to “topology of two point clouds,” which is crowded and less novel.

Small-Grant T1/T2 are **landscape-valued**. This paper is the **diagram $W_1/W_2$ analogue** (Vision and Approach R3 fallback). Do not quote ecology $\hat T$ as T2 in JeS.

---

## Candidate domains (literature check)

### 1. Oncology — tumour–immune spatial competition

**Data.** Keren et al. (2018) MIBI-TOF TNBC; 54-sample melanoma-immunotherapy MIBI on Mendeley. Co-I Powathil.

**Prior art.** Vipond et al. (2021, *PNAS*): multiparameter-persistence classification of tumour–immune spatial patterns. 2025 “Topological classification of tumour–immune interactions and dynamics”: vineyards and zigzag on **synthetic** Bull–Byrne runs; the authors note that real imaging is coarser in time.

**This manuscript.** Outlook only. Not a third painted figure. Not “TDA of tumour–immune data” in general. The remaining gap is T1/T2-style inference on **serial** paired clouds (pre-/post-treatment biopsies), which needs a longitudinal multiplex cohort. That is Standard Grant, with Powathil.

### 2. Movement ecology — predator–prey / territorial (lead)

**Public data (not used here).** Movebank wolf and jaguar GPS. Those remain the observational next step (simultaneous multi-animal clouds).

**In-house track record (not this paper’s dataset).** Gunner, Wilson, Lurgi, Börger, Redcliffe, Shepard, Holton, Brown et al., *Ecological Monographs* 96(2):e70069 (2026), doi:10.1002/ecm.70069: high-resolution ($\ge 10$ Hz) paths from 43 vertebrates; fundamental steps and turns; Dryad headings doi:10.5061/dryad.gxd2547sd. Redcliffe, Wilson, Holton et al., *Canadian Journal of Zoology* 103:1–18 (2025): ungulate slope-use. Prey pursuit and predator evasion appear there as **causes of turns**, not as two simultaneous point clouds. Using those heading series here would change the mathematical object.

**Novelty.** No located paper does multi-scale competitive-point-cloud TDA (individual → group → pack) with a Fréchet-mean / CUSUM framework on predator–prey or inter-pack territorial dynamics. Closest hits are single-population aggregation TDA.

**This manuscript.** Simulated territorial packs. $\hat T$ = dispersed hunting → encirclement of a herded group. Ecological meaning is written so the biologging group can check it. Gunner et al. (2026) is cited as the fine-scale movement grammar a later agent-based generator should respect.

**Venue.** *Journal of the Royal Society Interface* first; *Methods in Ecology and Evolution* if the editor will take a simulation-first note; not *Ecological Monographs* (they already have the 43-species empiric).

### 3. Multi-robot pursuit–evasion (second)

Simulation-first; closest in spirit to the toy’s AU_A/AU_B. TDA of a **single** swarm exists (Bhattacharya et al., SIGSPATIAL 2016); adversarial two-swarm TDA with this CUSUM/Fréchet pipeline was not found. Pair geometry and a corridor, not the football triangle. Reviewers may later want robot-trial validation; that is not this note.

### 4. Quantitative finance — deprioritised

Gidea and Katz (2017) and subsequent CUSUM-on-market-topology papers through 2025. The two-population order-flow framing may still be open, but the prior art is the densest and the bounded domain is the most contrived. No finance Co-I. Out of scope.

### 5. Longer shots — out of scope

Epidemiology (intervention is not the same kind of point process). Information warfare / platform moderation (domain and point cloud are metaphorical; API access is poor). Armed conflict remains excluded (Small Grant ethics constraint).

---

## Team papers that are not this object

Tales, Thomas, Littlemore, Brown — dementia / attention. Bezodis, Jones, Powles, Kilduff, … — Data-CAPS high-performance sport. Jones and Brown — US patent on impact auto-classification. None of these is adversarial spatial TDA.

---

## Panel payload for the Standard Grant

A Case for Support can say: the team already has (in draft / in review) a methods object that joins statistical topology with an ecology-led generator, a second bounded competitive system (robotics), and names oncology as the next observational system; the biologging collaboration is not a new Co-I search. That sentence is the panel-confidence payload. It does not require Movebank analysis first.

Files: `generators.py`, `experiments.py`, `numbers.json`, `figures/`, `draft.md`.
