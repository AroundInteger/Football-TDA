# Collaborator comments, 5 October 2026

Record of five comments on Paper A, and the decision for each across Papers A–C, the live Engineering and Physical Sciences Research Council (EPSRC) Mathematical Sciences Small Grant (APP98322), and the follow-on Standard Grant.

This note is the response map. It does not itself change manuscript prose, `08_current/grant/FOUNDATION.md`, or `08_current/grant/live/02_Vision_and_Approach_REV4.md`. Those files stay as written until a later pass actions the rows below. `FOUNDATION.md` remains normative for numbers and for the adaptive-filtration formula until that later pass.

Paper A has two trees. Edits, when made, move together:

- Canonical: `paper_A_JACT/`
- arXiv twin: `arXiv_Paper_A/`

---

## C1. \(H_0\) versus the group count

**Comment.** Reserve \(H_0\) for the homology group, and use \(\beta_0 = \dim H_0\), or simply "number of connected components", for the group count. Statements such as \(H_0 = 19\) read slightly oddly.

**Decision.** \(H_0\) is the homology group. The integer is the cluster count \(k\), and the cutoff curve is \(\overline{k}(\delta)\). At filtration zero on the centroid cloud, \(k = \beta_0 = \dim H_0\); say that once. Do not make \(\beta_0(\delta)\) the name of the sweep: that curve is clustering in the cutoff \(\delta\), not a Betti curve in the Vietoris–Rips parameter. Counts of finite \(H_1\) bars stay counts of bars, not \(\dim H_1\).

| Artefact | Action |
|---|---|
| Paper A, later edit | Replace \(\overline{H_0}(\delta)\) and sentences such as \(H_0 = 19.32\) in `paper_A_JACT/sections/methods.tex`, `paper_A_JACT/sections/results.tex`, figure captions (including \(H_0 = 20, 7, 2\)), and `paper_A_JACT/pipeline/CUTOFF_PROTOCOL.md`. Keep \(H_0\) where the group itself is meant (the introduction, where connected components are a homology feature). Mirror the same edits in `arXiv_Paper_A/`. |
| Paper B | Methods already glosses connected components as \(H_0\), counting distinct spatial groups. When A changes, retarget that gloss to "number of connected components" and cite A. No equations. |
| Paper C | Already writes \((\beta_0, \beta_1)\) for dimensions at one scale and \(H_0\) for the diagram. Do not import \(H_0 = 19\). No draft edit until C is written up; this row is the standing rule. |
| Small Grant | Prose already says "connected-component regimes", not \(H_0 = 19\). No Vision and Approach change. |
| Standard Grant | Same notation rule when that case is drafted. |

`FOUNDATION.md` still writes the sweep as \(\overline{H_0}(\delta)\). Do not amend it in this pass. Update it in the same pass that edits Paper A, so the normative file and the manuscript do not diverge.

---

## C2. Whether \(\varepsilon_{\max}\) is needed

**Comment.** Is \(\varepsilon_{\max}\) necessary? The reduced point clouds contain at most 22 points, so computing the full \(H_1\) persistence up to the diameter should be inexpensive. The Vietoris–Rips complex on a finite planar cloud is a full simplex once \(\varepsilon\) reaches the diameter, so all \(H_1\) bars are finite anyway. If there is a computational or modelling reason, say more explicitly why it is needed.

**Decision.** Do not drop the truncation on the comment alone. Computation is not a reason to keep it: at most 22 points, and the Vietoris–Rips complex is a full simplex at the diameter, so every \(H_1\) bar is finite. The percentile ablation in the Results does not settle it either. \(P_{50}\) through \(P_{95}\) agree, but a bar dying above about 65 m would be excluded at every percentile, because only finite bars are reported. `FOUNDATION.md` §2.5 still records the formula and the cross-scale motive: inter-centroid distances exceed \(\delta\), so a fixed \(\varepsilon_{\max}\) fails across scales, and the floor \(\max(5.0, 2\delta)\) prevents a degenerate filtration at small \(\delta\).

| Artefact | Action |
|---|---|
| Paper A, after one check | On the existing 150-frame and 1,500-frame samples, compute Vietoris–Rips to the diameter of each reduced cloud. If no further finite \(H_1\) bar appears, delete the adaptive equation, the percentile table, and the "fitted to one cutoff" paragraph, and state that every \(H_1\) class on these clouds is finite. If long bars appear, keep a cut only with an explicit modelling reason, not the current tuning sentence. Apply the same change in both Paper A trees. |
| Paper B | Cites A's filtration and does not re-derive \(\varepsilon_{\max}\). No change unless A drops it, in which case B's pipeline recap drops the phrase. |
| Paper C | Does not use this truncation. No change. |
| Small Grant | The live Vision and Approach does not quote \(\varepsilon_{\max}\). Leave it. |
| Standard Grant | Inherits whichever decision the diameter check produces. |

---

## C3. Supplementary Table S1 numbered as Table 8

**Comment.** "Supplementary Table S1" is then labelled "Table 8", and elsewhere the text refers to "Supplementary Table 8".

**Decision.** One object, three names. Seven main `table` environments precede the supplement, so `\ref{tab:matches}` prints 8, while the starred heading says Supplementary Table S1. The same counter makes the two supplementary figures Figures 5 and 6.

| Artefact | Action |
|---|---|
| Paper A, later edit | At the start of `paper_A_JACT/sections/supplement.tex`, reset the table and figure counters and number them S1, S2, and so on. Delete the hardcoded "Supplementary Table S1" heading so the float caption is the only title. Body text keeps `Supplementary Table~\ref{tab:matches}`. Mirror in `arXiv_Paper_A/sections/supplement.tex`. |
| Papers B and C | Not present. No action. |
| Small Grant and Standard Grant | Not present. No action. |

---

## C4. Abstract lifetimes

**Comment.** In the abstract, "short bar length in metres" and "longer bar length" read a little like placeholders. Give the actual mean persistence values instead.

**Decision.** Those phrases are unfilled. The abstract's presence rates are the ten-match figures, so the lifetimes must be the matching conditional means from Table `tab:h1multi`: 1.886 m at the individual level and 3.411 m at the tactical level. Use the defined term filtration lifetime (death minus birth, in metres on the Vietoris–Rips parameter). The primary-match values \(1.931 \pm 1.735\) m and \(3.778 \pm 2.723\) m stay in the Results.

| Artefact | Action |
|---|---|
| Paper A, later edit | One sentence in `paper_A_JACT/main.tex`, and in `paper_A_JACT/Paper_A_collaborator.md` (and its `.tex` twin) if that abstract still mirrors the manuscript. The same sentence in `arXiv_Paper_A/main.tex`. Suggested form: individual-level loops appear in \(96.5\% \pm 1.5\%\) of frames (mean filtration lifetime 1.886 m); tactical-level loops appear in \(18.8\% \pm 6.5\%\) (mean filtration lifetime 3.411 m). |
| Paper B | Does not own these summary statistics. If the introduction quotes A's abstract, update the quotation after A changes. Do not add a second abstract claim. |
| Paper C | No action. |
| Small Grant and Standard Grant | Do not put metre-valued lifetimes into grant prose. The Small Grant already points at the pilot paper for the statistics. |

---

## C5. Dependence on the clustering construction

**Comment.** For the EPSRC application, one of the strongest mathematical angles may be the dependence of the persistent homology on the clustering construction: how sensitive are the resulting persistence diagrams to the choice of cutoff, linkage rule, or small perturbations of the underlying point cloud? The very large dependence on the linkage rule already observed seems potentially interesting mathematically, and could motivate part of the proposed work rather than appearing only as a limitation.

**Decision.** The order-of-magnitude linkage gap (106 / 802 / 822 tactical \(H_1\) loops under single-linkage, complete-linkage, and Ward's method) and the cutoff sweep (275 loops at 6 m, and none at 16 m) are findings about the composed map: point cloud, then linkage at \(\delta\), then Vietoris–Rips on the centroids. Cohen–Steiner stability bounds diagrams of point clouds. It does not bound this map, because single-linkage jumps when a pairwise distance crosses \(\delta\). That question is not a third Small Grant theorem, and it is not Paper B's question.

This sharpens, and does not replace, §12 Question 1 in `working_foundations.md`. Question 1 asks how much the centroid projection discards. C5 asks how the centroid diagram depends on cutoff, linkage, and small perturbations. Paper A may state the empirical gap and name the open problem. It does not prove the stability lemma. The proof-shaped work is the follow-on Standard Grant. Paper C remains the synthetic mean-path and change-point note. Do not fold C5 into Paper C's T1-lite or T2-lite.

| Artefact | Action |
|---|---|
| Paper A, later edit, in place | In `paper_A_JACT/sections/discussion.tex` (Limitations), and the arXiv twin, report 106 / 802 / 822 as a result about that composed map. Keep single-linkage as the pre-specified proximity rule. State the open problem in one sentence. Leave the sparse-identification criterion as one possible selector, not the whole future question. Do not lengthen the section. |
| Paper B | Inherit single-linkage by citation. Do not discuss linkage sensitivity. |
| Paper C | When drafted, keep \((\beta_0, \beta_1)\) and do not add a linkage experiment on SkillCorner (non-overlap with A and B). A synthetic illustration of a merge discontinuity is allowed only if it serves C's existing generators, and is marked as motivation for the Standard Grant, not as a C theorem. |
| Small Grant (current) | `02_Vision_and_Approach_REV4.md` stays as written. It is at the page ceiling, and the two theorem targets (T1, averaging under competitive dependence; T2, localising transitions) already assume a fixed diagram. Do not add a linkage theorem or the 106 / 802 / 822 counts to the Vision. If a revision window opens before submission, the only permitted insertion is one clause on the Month-2 cutoff gate: the validation batch also records whether linkage and a small spatial perturbation preserve the diagrams that will be averaged. That clause requires an equal cut elsewhere. The default is no insertion. |
| Standard Grant (future) | The aims sketch is `08_current/grant/standard/AIMS_MAP.md` (October 2026). Aim 2 is the stability of the centroid persistence diagram under linkage, cutoff, and perturbation of the cloud. It is distinct from T1 and from T2. It is positioned against Cohen–Steiner, and against Schindler and Barahona (persistent homology of clusterings; Small Grant reference [20]), who study a different map: persistent homology applied to the clustering, not persistent homology of the centroid cloud after clustering. Algebraic ownership sits with the mathematics co-lead. `AIMS_MAP.md` does not amend the live Small Grant Vision and Approach. |

---

## Sync, 8 October 2026

- Restored local drafts of `03_Applicant_and_Team_Capability.md`, `06_Resources_and_Costs.md`, and `TIMELINE.md` to the IPA 799 v2 final lock on `main` (they had reintroduced placeholder cost wording).
- Aligned this note's Standard Grant row with `grant/standard/AIMS_MAP.md`.
- Aligned `grant/FOUNDATION.md` Paper C status with `working_foundations.md`: Papers B and C may proceed in parallel; Paper A is first and does not cite C.

## What the October comment pass did not change

- Live Small Grant Vision and Approach (`02_Vision_and_Approach_REV4.md`), apart from later JeS paste readiness work on `main`.
- Paper B and Paper C manuscript bodies beyond the parallel-sequencing rule.
