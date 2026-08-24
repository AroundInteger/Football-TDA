# SKILL: TDA Football Split-Publication Review
**File:** `review-tda-football-papers.md`  
**Role:** Project-specific calibration, scope boundaries, pipeline provenance, and joint-paper consistency for **Paper A** (`paper_A_JACT`) and **Paper B** (`paper_B_JSS`)  
**Read after:** `review-calibration.md` and **before** `review-science.md` when reviewing either TDA Football manuscript

---

## 1. Purpose

The Football-TDA project uses a **split publication strategy**: two manuscripts, one shared Python pipeline, one ten-match SkillCorner dataset. Generic review skills apply, but without this annex a reviewer will miscalibrate venue norms (JACT vs JSS), miss scope creep between papers, or flag “missing” football interpretation / “missing” theory that deliberately lives in the sibling manuscript.

**Always read this file when:**
- The document path or content references `paper_A_JACT`, `paper_B_JSS`, `3-Paper Paradigm`, or multi-scale persistent homology on SkillCorner data
- The user asks for a review of either manuscript or a joint pre-submission check
- The user asks for grant–Paper A alignment (EPSRC narrative vs JACT manuscript)

**Reference documents (read-only context; do not duplicate in review output):**
- `08_current/Paper Updated/3-Paper Paradigm/working_foundations.md` — scope boundaries, house style, locked claims, content map
- `08_current/grant/CANONICAL_NUMBERS.md` — grant ↔ Paper A numeric alignment
- `08_current/grant/archive/submission/VA_compressed_V3_no_figures.md` — compressed grant Vision & Approach

---

## 2. Document routing

At calibration, classify:

| Field | Paper A (`paper_A_JACT`) | Paper B (`paper_B_JSS`) |
|---|---|---|
| **Paper role** | Multi-scale PH framework, validation, robustness, complementarity | Football interpretation: events, baselines, bilateral, prediction |
| **Submit order** | **First** (arXiv → JACT; underpins EPSRC grant) | After Paper A posted; after grant submission |
| **Primary venue** | JACT (Springer; author–year via natbib) | JSS (Taylor & Francis; `interact` + Reference Style P) |
| **Primary field** | Applied / computational topology | Sports science / football analytics |
| **Application domain** | Football as validated testbed only | Football as subject matter |
| **LaTeX root** | `paper_A_JACT/main.tex` + `sections/` | `paper_B_JSS/main.tex` + `sections/` |
| **Bibliography** | `paper_A_JACT/references.bib` | `paper_B_JSS/references.bib` |

**Grant (parallel track):** EPSRC Vision & Approach — Format B in `review-outputs.md`. Align numbers to Paper A only; Paper B is intentionally absent from grant narrative.

Default venue inference: JACT for A, JSS for B unless user overrides.

---

## 3. Scope boundary checklist

Apply in every TDA Football review. Violations are typically **🔴 CRITICAL** for the manuscript where the violation occurs.

### 3.1 Paper A must not (as primary Results or Discussion outside Outlook)

- Headline event correlation, geometric baseline comparison, bilateral home/away coupling, or predictive utility as central findings (one short construct-validity paragraph in Results only)
- Cite Paper B (`paperB`) outside **Discussion → Outlook** (Paper A must be standalone)
- Re-tabulate or re-interpret Paper B–owned analyses
- Use numbered `[1]`-style citations (JACT requires author–year)
- Promise football-specific practitioner guidance as a contribution of this paper

### 3.2 Paper B must not

- Re-derive domain-informed clustering, adaptive filtration, cutoff selection, or full H₀/H₁ regime tables (cross-cite Paper A)
- Give H₀/H₁ scale regimes a standalone Results subsection (Methods recap only)
- Oversell the predictive null result as proof the measure is useless
- Present event correlation as discovery of new tactical knowledge (claim is **operationalisation**: continuous automated signal)
- Use equations in the topological pipeline subsection (plain language for sports-science readers)

### 3.3 Cross-citation discipline

- Paper B → Paper A: minimal forward cite for method and validated scales; no reproduced proofs or full sensitivity tables
- Paper A → Paper B: **Outlook only** (companion paper for football interpretation)
- Numeric claims appearing in both papers must match Paper A tables and pipeline CSVs
- Grant preprint `[12]` / Brown2026 must match Paper A when arXiv ID is assigned

### 3.4 House style (both papers)

From `working_foundations.md` §2:
- **Em dashes banned** in prose (`---` → comma, colon, semicolon, or new sentence)
- No rhetorical questions, vignettes, or idioms
- Paper A: one claim per sentence; lead with verb; max three heading levels
- Paper B: aim → method → result → implication; numbers in tables; one statistical fact per sentence in prose

---

## 4. TDA Football science checklist

Add to `review-science.md` Part A/B when reviewing either paper.

### 4.1 Paper A (JACT)

| Check | Review focus |
|---|---|
| Scale conflation problem | Clearly motivated before methods |
| Two contributions | Decomposition + adaptive filtration separable and non-redundant |
| Team-scale H₁ null | Structural Remark (k≤3 centroids), not empirical failure |
| Robustness | Operative cutoff range [6, 14] m; P50–P95 filtration insensitivity — lead in Discussion, not buried |
| Complementarity | Spearman + bottleneck/landscape distances support distinct scales |
| Incremental novelty | Schindler & Barahona and related work differentiated in Related Work |
| Reproducibility | Software versions, Dockerfile, GitHub URL in Declarations |
| Event correlation | Brief validity check only; no football interpretation |

**Flag [CRITICAL]** if Paper A headlines Paper B content or cites Paper B outside Outlook.

**Flag [SIGNIFICANT]** if Related Work does not sharpen differentiation from cluster-then-PH precedents.

### 4.2 Paper B (JSS)

| Tier | Content | Review focus |
|---|---|---|
| 1 | Event correlation | Directionally coherent; FDR; window sensitivity |
| 2 | Geometric baselines | Partial R² shows non-redundancy without implying prediction |
| 3 | Bilateral coupling | Near-zero cross-team ρ as explicit null baseline |
| 4 | Predictive utility | Match-grouped CV; null result framed as sample-size limit |

**Flag [CRITICAL]** if predictive evaluation uses random frame-level CV instead of match-grouped CV.

**Flag [SIGNIFICANT]** if tactical concepts (horseshoe, rest-defence arc, pressing encirclement) are absent from Introduction/Discussion.

**Do not** demand clinical-trial power calculations for n=10 matches — calibrate to observational sports analytics norms.

### 4.3 Statistical treatment (Paper B)

- Multiple event types: FDR correction expected where stated
- Bootstrap CIs over **matches** for cross-match summaries
- Effect sizes alongside significance for key contrasts
- Predictive comparison: permutation test + match-level bootstrap on ΔAUC

---

## 5. Pipeline and reproducibility checklist

Add to `review-science.md` Part B.

| Check | Paper A | Paper B |
|---|---|---|
| Dedicated pipeline | `paper_A_JACT/pipeline/` (`run_all.sh`, `sync_to_paper.py`) | `paper_B_JSS/pipeline/` (depends on Paper A outputs) |
| Committed outputs | `paper_A_JACT/pipeline/outputs/numbers.json`, `manifest.json` | `paper_B_JSS/pipeline/outputs/` |
| Core TDA pipeline | `02_tda_core/`, `03_football_analysis/` (wrappers only) | Same + `paper_v5_revisions/` |
| Key CSV outputs | `regime_summary.csv`, `uniform_summary.json`, complementarity JSON | `event_topology_correlation.csv`, `bilateral_topology.csv`, `predictive_utility_summary.json` |
| Numbers in `.tex` | Run `paper_A_JACT/pipeline/sync_to_paper.py` | Run `paper_B_JSS/pipeline/sync_to_paper.py` |
| Software stack | Methods § Software (GUDHI 3.11.0, Ripser.py 0.6.4, etc.) | Refer to Paper A |
| Figures | `figures/fig2_cycle_geometry.pdf` | `fig_event_correlation.pdf`, `fig_bilateral_timeseries.pdf`, `fig_roc_overlay.pdf` |
| Data | SkillCorner open data URL | Same |
| Code archive | GitHub URL in Declarations (placeholder until set) | Same |

**Flag [CRITICAL]** if manuscript numbers contradict canonical tables or `CANONICAL_NUMBERS.md`.

**Flag [SIGNIFICANT]** if methods omit seeds, software versions, or script paths needed for replication.

---

## 6. Known narrative traps (auto-flag)

When any of these appear mischaracterised, escalate severity:

| Trap | Correct framing |
|---|---|
| “Entirely novel pipeline” without Schindler differentiation | Combination + robustness on real 10 Hz competitive data |
| Paper B events “confirm the obvious” | Continuous automated monitor replacing manual coding |
| Predictive null = no practical value | Non-redundant descriptively; n=10 insufficient for held-out gain |
| Bilateral ρ≈0 dismissed as non-finding | Explicit null baseline for phase-conditioned coupling tests |
| Paper A event section too long | One paragraph construct-validity only |
| Em dashes in prose | House style violation — [SIGNIFICANT] for submission drafts |
| Grant cites Paper B | Paper B intentionally absent; maths-first narrative |
| “Stability scores 0.84–1.00” in grant without Paper A definition | Align metric names or qualify in grant |

---

## 7. Venue-specific emphasis

### 7.1 JACT (Paper A)

- Domain-agnostic framing; football as testbed only
- Methodological contributions + multi-match validation
- Team-null Remark and sensitivity ablation as rigour signals
- Author–year citations (`natbib` + `plainnat`)
- Abstract 150–250 words, no equations
- Mandatory Declarations: competing interests, data availability, LLM disclosure
- Template: Springer Nature universal template at transfer (not generic `article`)

### 7.2 JSS (Paper B)

- Practitioner-facing Introduction and Discussion
- Study Aims (not “Contributions” list)
- Numbers in tables; plain declaratives in prose
- ~4000 words excluding tables, references, figure captions
- Unstructured abstract ~200–250 words
- Back matter sequence: Acknowledgements → Disclosure → Funding → Notes on contributor(s)
- Figure alt text for argument-bearing figures (T&F policy)

### 7.3 EPSRC grant (alignment with Paper A)

- Cross-check `CANONICAL_NUMBERS.md` and `working_foundations.md` §11
- Preprint citation must update when Paper A arXiv ID exists
- Paper B and JSS narrative not required in grant

---

## 8. Mode D — Joint consistency review

**Trigger:** User requests cross-paper pre-submission check, or both `paper_A_JACT` and `paper_B_JSS` are in scope.

**Sequence:**
1. Brief dual calibration (roles and venues)
2. Run §3 scope boundary checklist across both manuscripts
3. Run §5 pipeline checklist and compare to `CANONICAL_NUMBERS.md`
4. Run §6 narrative trap scan on both
5. **Do not** repeat full Mode A science/communication audits unless user asks

**Output format:**

```
JOINT CONSISTENCY REVIEW — TDA Football Paper A + Paper B — [date/version]

CALIBRATION
  Paper A venue: JACT
  Paper B venue: JSS
  Paper A status: [draft / arXiv / submitted]
  Grant alignment checked: [yes / no]

SCOPE BOUNDARY
  [CRITICAL / SIGNIFICANT] [issue] — [which paper] — [resolution]

NUMERIC / PROVENANCE
  [severity] [issue] — [resolution]

CROSS-CITATION
  [severity] [issue] — [resolution]

NARRATIVE TRAPS
  [severity] [issue] — [resolution]

GRANT ↔ PAPER A (if requested)
  [severity] [issue] — [resolution]

RECOMMENDED ORDER OF WORK
  1. Complete Paper A Mode A review and submission blockers
  2. Post Paper A arXiv; update paperA stub in Paper B
  3. Generate Paper B placeholder figures; Paper B Mode A
  4. Grant final numeric sync

PRIORITY ACTION LIST (cross-paper items only)
  [C/S/P items affecting submission readiness]
```

End with recommendation: proceed Paper A Mode A / refresh numbers / Paper B blocked until arXiv ID, etc.

---

## 9. Abstract conventions

See `abstract-structure-guide-tda.md` for Paper A and Paper B skeletons and sentence-level rules.

---

## 10. Integration with other skill files

| Skill file | TDA Football addition |
|---|---|
| `project-instructions.md` | Load this file for `paper_A_JACT` / `paper_B_JSS` paths |
| `review-calibration.md` | §5.6 profiles; extended venue table |
| `review-science.md` | §4 split-paper tensions; Paper B observational ML note |
| `review-communication.md` | §2.1 TDA abstract notes; house style |
| `review-orchestrator.md` | Mode D for TDA Football pair |
| `review-outputs.md` | TDA CRITICAL examples; joint format §8 above |

When **not** reviewing TDA Football papers, skip this file entirely.
