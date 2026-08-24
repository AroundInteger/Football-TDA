# Multi-Scale TDA / Football — Working Foundations

*Living reference. Update this file as decisions firm up; treat anything here as the
default unless we explicitly agree to change it.*

---

## 1. Three-paper strategy

The original single manuscript tried to satisfy three audiences at once (topologists,
sports scientists, and EPSRC mathematical-sciences reviewers), which is the root cause
of its scope creep — no single audience existed to force a cut. Splitting by audience
restores that forcing function.

- **Paper A — JACT** (*Journal of Applied and Computational Topology*). Mathematics-first.
  This is the paper that underpins the EPSRC Mathematical Sciences grant narrative
  ("mathematics using football as a testbed," not sports analytics). Hybrid journal,
  no mandatory APC. Small/young (SJR ≈ 0.97, no WoS Impact Factor yet), single-blind
  review, explicitly scoped for applied topology in scientific/engineering settings.
- **Paper B — JSS** (*Journal of Sports Sciences*). Application-first. Built around
  interpreting the TDA outputs on the 10-match dataset for a sports-science readership:
  event correlation as the centrepiece, topology-vs-geometric-baseline comparison,
  bilateral (home/away) coupling, predictive utility, and a forward-looking discussion
  of adaptation to other sports. No mandatory fee.
- **Paper C — methods note (Interface / SIAM MDS / FoDS).** Diagram $W_1/W_2$ analogue
  of mean-path and change-point inference on *synthetic* adversarial clouds (ecology
  lead, robotics second). Not a third football paper. Not JACT (Paper A). **Developed
  only after Papers A and B are submitted.** Staging files: `paper_C_methods/`.
- **Ruled out:** Scientific Reports. Fully gold OA, mandatory APC currently
  £2,290/$2,850/€2,490 — reopens the same fee problem that already motivated moving off
  PLOS ONE, unless institutional funding changes that.
- **Non-overlap rule:** Paper B cites Paper A for the shared methodological machinery
  (clustering decomposition, adaptive filtration, the validated H0/H1 regimes) rather
  than re-deriving or re-tabulating it. Each paper's *novel* empirical claim is
  partitioned, not duplicated — see content map below. Paper C cites Paper A for
  observational football and does not re-analyse SkillCorner.

### 1a. Locked claims paragraphs (working-order item 1 — completed)

**Paper A (JACT).** This paper presents a multi-scale persistent homology framework
that resolves the scale-conflation problem in competitive multi-agent point clouds,
through two methodological contributions: domain-informed hierarchical clustering that
separates organisational levels before persistent homology is computed, and an adaptive
Vietoris–Rips filtration that keeps H1 detection consistent across scales despite the
clustering changing the point cloud's geometry at each level. Validated on ten
professional football matches, the framework identifies three stable H0 regimes and two
H1 regimes — individual and tactical — that hold across independent matches, across a
wide range of clustering cutoffs, and across the adaptive filtration's percentile
parameter; we further show the two H1 scales carry distinct rather than redundant
topological information, and that every H1 generator can be recovered as an
interpretable geometric cycle. A minimal correlation with real match events confirms the
detected features track genuine structure rather than noise. Football is a validated
testbed; the framework itself is domain-agnostic and intended for any bounded
competitive multi-agent system with spatial tracking data.

**Paper B (JSS).** This paper asks what persistent-homology-based measures of team shape
add for football analysis, building on a validated multi-scale topological method
described in a companion paper. Across the same ten professional matches, we show that
topological persistence tracks real match events coherently: pressing, engagements, and
quick breaks coincide with persistence decreases, while sustained build-up play
coincides with increases. Tactical-scale persistence also carries information not
captured by standard geometric descriptors — team width, convex-hull area — at the
per-frame level, and home and away teams' tactical structures evolve largely
independently of one another within a match. That non-redundancy does not, however, yet
translate into a detectable advantage for predicting phase of play on held-out matches
at the present sample size; we discuss what scale of data, and what adaptations to
other invasion sports, would be needed to test these patterns more fully.

**Non-overlap check (passed).** Paper A treats event correlation as a one-sentence
construct-validity check only ("not noise"); Paper B owns the full interpretive claim.
Neither paragraph required new analysis — both are fully supported by results already
in `results.tex`. This is a writing/selection task from here, not a research task.

**Paper C (methods; after A and B submit).** Hierarchical adversarial point processes:
the diagram analogue of a mean path ($W_2$ Fréchet mean of birth-zero $H_0$ diagrams)
and of change-point detection (Page CUSUM on diagram $W_1$), with interaction lengths
re-derived on a simulated territorial predator–prey generator and a corridor
pursuit–evasion generator. Claims are split into three tiers: cited stability and MST
theory; proved T1-lite / T2-lite under stated hypotheses; conjectured behaviour under
genuine tug-of-war dependence. Football is the originating testbed (cite Paper A), not
the dataset. Observational ecology (Movebank / dual-species GPS) and serial multiplex
imaging are Outlook / Standard Grant, not results. Gunner et al. (2026) is the
movement-grammar citation, not this paper's point clouds.

**Non-overlap with A/B (locked).** Paper C does not re-analyse SkillCorner, does not
copy football metre values into its results, and is not submitted to JACT or JSS.
Papers A and B do not depend on Paper C; A is submitted first and must not cite C.

---

## 2. House style

### JACT (Paper A)
- One claim per sentence.
- Lead with the verb. Don't nominalize the action into the subject — "X makes Y an
  explicit object of inference" should be "X analyses Y" or "X treats Y explicitly."
- Equations and notation carry the precision; prose stays plain and short.
- Citations and section cross-references sit at clause boundaries, never embedded
  mid-clause.
- If a parenthetical is carrying real content (a list, a justification), give it its
  own sentence instead of hiding it in brackets.
- No sentence does more than two jobs. If a sentence states a result *and* its
  implication *and* its relation to deferred future work, split it.

### JSS (Paper B)
- Paragraph order: aim → method → result → practical implication.
- Numbers live in tables. Prose states findings as plain declaratives ("persistence
  decreased during on-ball engagements; it increased during build-up") rather than
  carrying inline statistics.
- One statistical fact per sentence, maximum.
- The practitioner-relevant implication is the main clause, never a trailing
  subordinate clause.
- Light citation density inside sentences; cite at the paragraph or section level
  where possible rather than stacking citations mid-sentence.

### Shared (both papers)
- No rhetorical questions, no imagined scenarios or vignettes, no idioms. State an
  anticipated objection and its answer as two plain declaratives, not as a spoken
  question and reply. (Caught when both papers' Discussion 4.1 drafts leaned
  conversational — "A natural objection... dress it up as derived" for A, "A coach
  watching a match already knows... wearing a more complicated name" for B — both
  corrected to flatter declaratives.)
- **Em dashes banned.** Replace `---` with standard punctuation: commas for
  parenthetical asides, colons for lists, semicolons or a new sentence for strong
  breaks. En dashes (`--`) for ranges and compound names (Vietoris--Rips) are
  unaffected.
- **Sentence length.** No sentence should carry more than two jobs. Compound sentences
  joined by "so that", "such that", or "which means that" chains are the primary
  offenders; split at the conjunction. Checked at each revision pass before compiling.

### Paper A standalone rule (locked)
Paper A is submitted first and must be fully self-contained. References to Paper B are
permitted **only** in the Outlook subsection of Discussion. Every other mention of a
"companion paper", "forthcoming analysis", or similar in Paper A must be rephrased to
"forthcoming work" or "deferred to future analysis" without a citation. The Methods and
Results sections of Paper A must not depend on or forward-reference Paper B in any way.
Paper C is written after A and B are submitted; Paper A must not cite Paper C.

### Paper B tactical concepts link (locked)
Ring-like H1 features detected by the framework must be explicitly linked to three
recognisable tactical structures in Paper B's Introduction and Discussion:
1. Peripheral possession ring (horseshoe): large loop persisting over many frames
   indicates the attacking team is orbiting rather than penetrating the defensive block.
2. Rest-defence arc: deliberate ring formed by deeper players in positional play
   (3-2-5 / 2-3-5 shapes) to contain counter-attacking transitions.
3. Pressing encirclement (Gegenpressing): tight loop formed by 3-4 players closing
   simultaneously around a ball-carrier; loop formation then collapse marks the
   trigger-and-close sequence.
These concepts exist in coaching and analytics literature but have no standard
quantitative definition; that is the contribution the paper is making explicit.

### Paper B TDA pipeline section (locked addition to Methods)
Paper B's Methods section must include a substantive "Topological Analysis Pipeline"
subsection (replacing the lighter "Topological Feature Summary" section) that:
- Gives a plain-language account of what persistent homology measures (proximity
  networks, birth/death of features, persistence as stability measure)
- Describes the three-step pipeline: clustering, Vietoris-Rips filtration, persistence
  diagram, H1 persistence scalar
- Names the two spatial scales (individual, tactical) and states they are pre-validated
- Cites Paper A for full mathematical details
- Uses no equations; the target reader is a sports scientist, not a topologist

---

## 3. Known prose failure patterns (with worked fixes)

**Nominalization-as-subject.** Original: "The bilateral decomposition... makes the team
identity that the 22-player analysis discards an explicit object of inference." Fixed:
"The 22-player analysis discards team identity. The bilateral decomposition analyses it
directly."

**Parenthetical-list-smuggling.** Original: "Operationalising this criterion (i.e.
choosing the dynamical state, defending sparsity-of-library against AIC/BIC/
cross-validation baselines, and confirming that the chosen linkage's persistence
sequence is genuinely lower-dimensional) is beyond the scope of the present validation
paper..." Fixed: "Operationalising this criterion would require three things: choosing
the dynamical state, defending sparsity-of-library selection against AIC/BIC/
cross-validation baselines, and confirming the chosen linkage's persistence sequence is
genuinely lower-dimensional. We defer this to the forthcoming full-season work."

**Four-jobs-one-sentence.** Outlook section currently carries what's being scaled, what
it will characterise, why it matters for the linkage criterion, and what that requires,
all in one ~70-word sentence. Split each job into its own sentence.

---

## 4. Content map: Draft v4/v5 → Paper A (JACT) vs Paper B (JSS)

| Section (current draft) | Paper A (JACT) | Paper B (JSS) |
|---|---|---|
| 1.1–1.2 Background, Scale Conflation Problem | Keep, rebalance away from football-only examples | Short summary only, cites Paper A |
| 1.3 Contributions | Keep, reword item 4 to match trimmed Results | N/A — JSS framed around questions, not "contributions" |
| 1.4 Related Work | Keep in full | Trim to football-analytics literature only |
| 2.1 Data | Keep | Keep (brief) |
| 2.2 Clustering (core) | Keep | Cite Paper A |
| 2.2 Bilateral decomposition (methods) | One sentence, defer detail | Keep in full |
| 2.3 Cutoff selection | Keep | Cite Paper A |
| 2.4 Adaptive filtration | Keep | Cite Paper A |
| 2.5 Closed cycle identification | Keep | Cite Paper A briefly |
| 3.1 H0 regimes | Keep | Cite Paper A |
| 3.2 H1 detection (incl. team-null Remark) | Keep | Cite Paper A |
| 3.3 Closed cycle structures | Keep | Cite Paper A |
| 3.4 Temporal evolution / half-time LMM | Cut | Move in full, football-context interpretation |
| 3.5 Scale complementarity (Spearman/Fisher/TDA-native distances) | Keep — defends the decomposition itself | Cite Paper A |
| 3.6 Sensitivity analysis | Keep, compressed | Cite Paper A |
| 3.7 Linkage method comparison | Move into Discussion/Limitations, not a Results subsection | Not needed |
| 3.8 Event correlation | One paragraph + one merged table, construct-validity check only | Move in full — this is the centrepiece |
| 3.9 Baseline vs geometric descriptors | Cut | Move in full |
| 3.10 Bilateral topological coupling | Cut (one forward-pointing sentence only) | Move in full |
| 3.11 Predictive incremental utility | Cut | Move in full |
| 4.1 Methodological contributions | Keep | N/A |
| 4.2 Multi-scale structure | Keep complementarity discussion; cut baseline-vs-topology reconciliation | Reframe around 3.9/3.11 |
| 4.3 Temporal dynamics & event correlation | Shrink to match compressed 3.8 | Move in full |
| 4.4 Bilateral coupling | Cut to one sentence | Move in full |
| 4.5 Limitations | Keep, absorbs linkage-comparison numbers from 3.7 | Lighter version |
| 4.6 Outlook | Keep, name *both* companion papers explicitly | Brief, forward to other sports |
| Code/data availability | Keep only scripts backing what's actually in Paper A | Keep scripts for 3.9/3.10/3.11/3.4 |

---

## 5. Working order — inside-out drafting sequence

1. **Lock the claims paragraph** for each paper — a skeleton-abstract statement of what
   the paper actually claims, tighter than a "research question." This is the filter
   for everything downstream.
2. **Select and lock the Results** that support those claims, from material that
   already exists (per the content map above) — no new analysis at this stage.
3. **Draft Methods** — only what's needed to justify the locked Results.
4. **Draft Discussion** — interpretation, limitations, outlook — written immediately
   after Results is fixed, so numbers aren't re-derived from memory and accidentally
   restated.
5. **Draft Introduction** — motivate backward from the locked claims paragraph. Protect
   real drafting time here even though it's last; it's the first thing a reviewer reads.
6. **Draft Abstract** last of all, as a compressed synthesis of the finished paper.

---

## 6. Decided / settled facts (don't re-litigate without new information)

- JACT: hybrid Springer journal, no mandatory APC, single-blind review.
- JSS: no mandatory APC (established prior to this document).
- Scientific Reports: mandatory APC (~£2,290/$2,850/€2,490), ruled out on cost grounds.
- arXiv deposit can be the *comprehensive* version (everything, including what's cut
  from JACT's main text) since arXiv has no editorial scope constraint — EPSRC
  reviewers likely read that version, where more rigour only helps.

---

## 7. Subsection skeletons (locked)

Macro-sections (Introduction, Methods, Results, Discussion, Conclusion) are shared in
name only. Subsection structure within each is decided independently per paper — what
earns a standalone subsection in one paper may only earn a recap paragraph, or nothing,
in the other. Confirmed case in point: H0/H1 regime structure is a full Results
subsection in Paper A (it's A's contribution) but only a recap paragraph in Paper B's
Methods (it's inherited, not B's contribution) — caught when a first draft wrongly gave
it a parallel standalone subsection in B.

### Paper A (JACT)
- **Introduction:** Background; The Scale Conflation Problem; Contributions; Related Work.
- **Methods:** Data; Proximity-Aware Clustering (bilateral decomposition reduced to one
  sentence); Domain-Informed Cutoff Selection; Adaptive Filtration for H1 Detection;
  Closed Cycle Identification; minimal statistical-test description.
- **Results:** Scale-Specific H0; H1 Loop Detection (+ team-null Remark); Closed Cycle
  Structures; Scale Complementarity; Sensitivity Analysis; construct-validity coda on
  event correlation (deliberately small).
- **Discussion:** Methodological Contributions; Multi-Scale Topological Structure;
  Limitations (absorbs linkage-method numbers); Outlook (names both companion papers).
- **Conclusion:** single paragraph, no subsections.

### Paper B (JSS)
- **Introduction:** Background (practitioner-facing, cites Paper A for the maths); Study
  Aims (sports-science convention, not a "Contributions" list); Related Work
  (football-analytics literature — heavier here than in A).
- **Methods:** Data (brief); Topological Feature Summary (plain-language recap of
  H0/H1/persistence, cites Paper A, no equations); Event Annotation and Correlation
  Methodology; Geometric Baseline Descriptors; Bilateral (Home/Away) Decomposition;
  Predictive Utility / Cross-Validated Classification.
- **Results:** Topological Persistence Tracks Match Events; Topology versus Standard
  Geometric Descriptors; Home and Away Tactical Independence; Predictive Value for
  Phase-of-Play Classification. No standalone H0/H1-regime subsection.
- **Discussion:** What Topological Persistence Adds for Practitioners; Tactical
  Independence and What It Suggests for Analysis; Why No Predictive Gain Yet, and What
  Would Change That; Limitations and Future Directions in Other Sports.
- **Conclusion:** single paragraph, practitioner-facing takeaway.

---

## 8. So-what checklist (locked principle for Discussion drafting)

For every Discussion subsection, state explicitly what a skeptical reviewer would say
and why the framing answers it — don't assume the numbers speak for themselves. Specific
risk points identified so far, to revisit when drafting the corresponding subsection:

**Paper A**
- Incremental-novelty risk: every individual piece of the pipeline (cluster-then-PH,
  scale-aware filtration) has precedent (Schindler & Barahona in particular). This needs
  a sharper differentiation in Related Work when we draft the Introduction, not just
  restated results — framing alone in Discussion won't fully resolve it.
- The strongest exportable so-what is the robustness result (wide safe zone on cutoff
  [6,14] m and percentile P50–P95) — lead with this in Methodological Contributions
  rather than letting it sit inside a sensitivity table.
- The team-null Remark is a genuine small piece of mathematics (structural, not
  empirical) — lean on this as evidence of rigour.

**Paper B**
- "Confirms the obvious" risk for event correlation: the so-what is operationalisation
  (a continuous, automatically computable signal replacing manual coding), not discovery
  of new tactical knowledge — must be named as such, not left implicit.
- Predictive null result risk: frame as a genuine boundary-condition finding (tells
  future work where not to expect easy wins, and what scale of data would resolve it),
  not apologised for.
- Bilateral independence already has a clean answer: an explicit null baseline for
  future tactical-context-dependent coupling tests.
- Single-competition, ten-match sample is a real generalisability limit — name it
  plainly in Limitations rather than softening it; a defensive tone would hurt more
  than the limitation itself.

---

## 9. LaTeX/Overleaf conventions (for eventual transfer)

Reviewed against the uploaded `OVERLEAF_BEST_PRACTICES.md` (generic guide, originally
written for a different paper). Most of it already matches what we've independently
locked above and needs no action now, just confirmation at transfer time:

- Modest, substantiated claims; minimal bullet points in narrative prose; reduce
  repetition; define notation — all consistent with Sections 2–3 above.
- Abstract: no equations, 150–250 words, no overselling — applies when we draft
  Abstracts last, per the working order in Section 5.
- File structure (`main.tex` + one `.tex` per section via `\input{}`) already matches
  our actual repository layout.

**One conflict to flag — and a correction to an earlier call.** I previously told you to
keep numbered citations for Paper A and override the generic Overleaf doc's `\citep{}`
recommendation, reasoning that this matched Springer/JACT convention. Having now fetched
JACT's live submission guidelines directly, that was wrong: JACT explicitly requires
name-year parenthetical citations — "(Thompson 1990)", "(Abbott 1991; Barakat et al.
1995)" — via natbib, exactly what the generic doc said. The reference list itself is
alphabetised by first author's surname, with full DOI links. Paper A's existing
numbered `[1]`-style citations will need converting to author-year at transfer time.
Paper B is unaffected and was correct as established: Taylor & Francis' "Reference
Style P", used by the `interact` class file, is numbered and italic in parentheses —
"(1)", "(2, 4, 10)", "(11–15)" — confirmed directly from the template source.

**Confirmed template specifics for eventual transfer.**

*Paper A (JACT/Springer):* use the Springer Nature universal LaTeX template (one
template for any Springer Nature journal, "content-first", minimal formatting,
available on Overleaf or as a zip) — not a JACT-specific template. Decimal heading
system, maximum three levels. Single-blind peer review. A mandatory "Statements and
Declarations" section before the references: Competing Interests is required, and a
Data Availability Statement is required for all original research articles (separate
from any existing Code and Data Availability text already in the draft — check the two
don't duplicate awkwardly). Figures: vector EPS preferred for line art (≥1200 dpi or
0.1 mm minimum line weight), halftone TIFF (≥300 dpi), combination art ≥600 dpi, RGB
for colour, Helvetica/Arial lettering at 8–12 pt, no titles inside the figure itself.
The AI-disclosure requirement flagged earlier is confirmed verbatim from this same page.

*Paper B (JSS/Taylor & Francis):* `\documentclass{interact}`, not generic `article` —
do not use the `10pt`/`11pt`/`12pt`, `twocolumn`, or `geometry` options, which the class
file doesn't support. Defaults to B5 single-column; use the `largeformat` option for
A4 two-column if the journal requires it. Five heading levels available (section
through subparagraph), all auto-numbered. Figure captions go below the figure; table
captions go above the table body (opposite conventions — easy to get backwards at
transfer time). A fixed sequence of unnumbered sections after the main text and before
references: Acknowledgement(s), Disclosure statement, Funding, Notes on
contributor(s), Notes. I still could not access JSS's own structural instructions page
directly (tandfonline.com blocks automated access — confirmed again on a second
attempt); if you want the exact abstract structure or word limit verified, pasting the
relevant section of that page directly would let me check it against the draft.

**Update from directly pasted T&F instructions content.** A ~4000-word guideline
(excluding tables, references, and figure captions) appears to be the general word
limit for a standard JSS research article — not a hard cap. A separate set of figures
(200-word unstructured abstract, 3500-word total) was listed under a "Registered
Reports" heading specifically, a distinct pre-registered submission type that doesn't
match what either paper actually is (we have results already); these likely don't
apply to Paper B unless the Registered Reports route is deliberately chosen, which
would also require restructuring Results and Discussion, not just the abstract.
**Confirmed:** Paper B targets Taylor & Francis's *Journal of Sports Sciences* (plural,
`interact`/Reference Style P) as a standard research article, not a Registered Report.
A separate, similarly-named journal — David Publishing's *Journal of Sports Science*
(singular) — surfaced briefly via a mismatched search result and was ruled out: it's a
different publisher with a pay-to-publish model, which would have undermined the whole
reason JSS was chosen over Scientific Reports in the first place. Disregard any
reference to that journal if it resurfaces in old notes. The ~4000-word guideline
(excluding tables, references, and figure captions) and the existing drafted abstract
(unstructured, ~220 words) both stand as confirmed.

JSS now adds AI-generated image descriptions (alt text) to all published figures by
default; authors can opt to write their own instead. Worth doing manually for any
figure carrying a specific argument (the cutoff-sweep disagreement, the home/away
non-synchrony) rather than leaving it to their automated tool — note for when the
actual figures are built.

Confirmed from the uploaded `interacttfpsample.bib`: `tfp.bst` works with standard
BibTeX entry types and fields (article, book, incollection, phdthesis, etc.) with no
unusual structure required. Converting the existing `references.bib` to this style
should be a style-file swap, not a manual per-entry rewrite.

**One tension to flag and resolve deliberately.** The guide's "engaging tone... present
findings in an interesting and compelling manner" sits awkwardly against the rule just
locked in Section 2 (no rhetorical questions, vignettes, or idioms) — that rule exists
*because* reaching for engagement produced exactly the conversational drift we just
corrected. Resolution: engagement should come from precision and well-chosen concrete
results, not from rhetorical scaffolding. Don't let "engaging" be read as licence to
reintroduce vignettes or idioms.

**Practical reminders for transfer time (not yet — we're still drafting prose).**
Greek letters and symbols written as raw Unicode in our drafted prose (δ, ρ, ε) need
converting to proper LaTeX commands (`$\delta$`, `$\rho$`, `$\varepsilon$`) when this
moves into actual `.tex` files. Confirm British English spelling throughout at that
point. Confirm British English spelling throughout at that
point too — we've been drafting in British English already, but a systematic check at
transfer is worth doing rather than assuming.

---

## 10. Figures and tables (tracking)

**Principle.** Figure style should be internally consistent within each paper, but need
not match between Paper A and Paper B — they serve different disciplinary audiences with
different visual conventions. Before designing any figure, state its one-sentence
message explicitly; a figure earns its place only if it communicates something prose and
tables don't (a disagreement, a non-synchrony, a near-identical-curves null result), not
merely because the underlying data happens to be plottable.

**Paper A**
- Cutoff-sweep figure (candidate, pending real data). Three clustering-quality metrics
  (Calinski–Harabasz, silhouette, information-content) plotted against δ ∈ [0.5, 30.0] m,
  with the three chosen cutoffs (2.98, 12.0, 30.0 m) marked. Message: the tactical cutoff
  is a genuine judgement call between two disagreeing automated metrics, not an
  arbitrary pick. Needs the actual per-δ metric values from the original 100-point
  sweep — cannot be mocked up from the summary optima alone. Revisit numerically once
  Introductions are drafted.
- Percentile ablation (P50–P95): explicitly **not** a figure. Five identical results are
  clearer as a compact table than as a flat line plot.

**Paper B**
- Event-type persistence change (existing Figure 4 from the original draft). Bar chart
  of mean persistence change by event type, individual and tactical scales, with
  significance markers. Carries over directly — the headline visual for the paper's
  central finding.
- Home/away tactical-persistence time series (candidate, pending real data). Two lines,
  home and away tactical persistence across the primary match's timeline. Message: the
  two teams' tactical shapes visibly fail to synchronise, which is more persuasive than
  reporting a near-zero correlation coefficient. Structurally similar to the original
  draft's cut Figure 3 (which plotted individual- vs tactical-scale persistence over
  time on the merged cloud), so the underlying plotting approach may partly transfer.
  Needs the actual per-frame bilateral persistence values across one match's timeline.
- ROC-curve overlay, baseline vs baseline-plus-topology (candidate, pending real data).
  Two near-overlapping ROC curves. Message: the predictive-utility null result is
  visually, as well as statistically, a non-difference. Needs the actual out-of-fold
  predicted probabilities from the cross-validated classifier, not just summary AUC.
- Geometric-descriptor scatter plots (lower priority, optional). Persistence against
  each of the four baseline descriptors. The existing partial-R² table already carries
  most of this message; a figure here would add texture rather than a genuinely new
  argument, so lower priority than the two above.

---

## 11. Grant–Paper A alignment notes (checked 2026-06-23; corrected 2026-08-24)

> **Superseded in part.** This section was checked on 23 June 2026 and predates the
> 6 July pipeline recompute. `08_current/grant/FOUNDATION.md` is now the normative
> source for every number below; where the two differ, `FOUNDATION.md` wins. Three
> entries were wrong and have been corrected in place — see the struck rows and the
> revised action list.

Cross-referenced: `grant/archive/full/tex/sections/02_vision_and_approach.tex` against
Paper A locked claims (§1a above). All core claims are aligned. Four minor discrepancies
to resolve when incorporating grant feedback:

### Aligned (confirmed)
| Claim | Paper A value | Grant value |
|---|---|---|
| Individual cutoff | 2.98 m | 2.98 m (line 65); rounded to "3 m" in prose (line 19) — acceptable |
| Tactical cutoff | 12.0 m | 12.0 m ✓ |
| Team cutoff | 30.0 m | 30.0 m ✓ |
| Multi-match individual H1 presence | 97.0% ± 1.5% | 97.0% ± 1.5% ✓ |
| Multi-match tactical H1 presence | 19.3% ± 7.2% | 19.3% ± 7.2% ✓ |
| Spearman ρ (scale complementarity) | **0.264** | **0.264** ✓ (was recorded as 0.254 here; corrected 2026-08-24 against `numbers.json`, which gives 0.26403 over 1,500 frames, *p* = 2.4 × 10⁻²⁵) |
| Event–topology pairs | 104,722 | 104,722 ✓ |
| Sensitivity range | 6–14 m | 6–14 m ✓ |
| Total H1 loops (10 matches) | 4,200 + 315 = 4,515 | 4,515 ✓ |
| Convex-hull area partial R² | 0.091 | 0.091 ✓ (cited from Brown2026) |

### Discrepancies to fix in grant before submission

1. **"Stability scores 0.84–1.00"** (grant): the phrase is a fair rounding of the
   `stability` column in `paper_A_JACT/pipeline/outputs/regime_summary.csv`
   (0.956 / 0.836 / 1.000), so the range itself is correct. The real defect is that
   the score is **defined nowhere in Paper A's text** — `methods.tex` describes the
   sweep design but never says what is being scored. The grant's 0.80 gate therefore
   has provenance in our pipeline but not in the published record.
   → **Action (open)**: add the definition to Paper A's cutoff-selection subsection.
   Tracked as ruling R5 in `FOUNDATION.md`.

2. ~~**Primary-match individual H1 presence: 95.3% vs 96.0%** — update the grant to
   96.0%.~~ **WRONG; DO NOT ACTION.** `uniform_150/uniform_summary.json` and Paper A
   Table `tab:h1single` both give **143/150 = 95.3%**. Following this instruction
   would have put the grant *out* of agreement with the paper. Corrected 2026-08-24.

3. ~~**Primary-match tactical H1 presence: 12.7% vs 12.0%** — update the grant to
   12.0%.~~ **WRONG; DO NOT ACTION.** Both sources give **19/150 = 12.7%**.
   Corrected 2026-08-24.

**Where 96.0% and 12.0% actually come from.** Match 1996435 is analysed twice. The
`uniform_150` primary-match run gives 143/150 and 19/150; the ten-match batch row for
the same match gives 144/150 (96.0%) and 18/150 (12.0%) under different sampling. Both
are real. The `uniform_150` figures are canonical whenever "the primary match" is named,
and the batch row is quoted only as one of ten. See `FOUNDATION.md` ruling R3.

### Structural note: grant vs. three-paper paradigm

The grant's publication-adjacent pipeline is:
- Brown2026 = Paper A (methodology, ArXiv/JACT) — **same as this project's Paper A**
- Brown2026inprep = cross-domain application to armed conflict event data — **separate**
  from Paper B; Paper B (JSS, football analytics) is not mentioned in the grant
- Full-season results paper = planned under this grant (future)
- Paper C = synthetic methods note (ecology + robotics generators; diagram T1/T2 analogue).
  Supports the Standard Grant *panel* story (complementary fields). Not a JeS deliverable
  that quotes ecology $\hat T$ as landscape T2. Developed after A and B submit.

**Paper B is intentionally absent from the EPSRC grant**, which is correctly positioned
as mathematical sciences with football as a testbed. Paper B is the sports-science
publication track and does not need to appear in the grant narrative.
