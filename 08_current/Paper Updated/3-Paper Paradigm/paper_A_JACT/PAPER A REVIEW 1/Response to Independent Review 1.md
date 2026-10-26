# Response to Independent Review 1

**Manuscript:** Multi-Scale Persistent Homology for Competitive Collective Systems
**Review:** Paper A Independent Review 1, 25 October 2026
**Revised text:** `paper_A_JACT` (journal source) and the same scientific claims in `arXiv_Paper_A`

The arithmetic checks in the review were left as they stood. Table 1, the null tables, the Fisher odds ratio 6.12, the merge rates, and the team-level mean of 1.96 were not recomputed. The barcodes, presence rates, filtration lifetimes, nulls, bottleneck distances, and cutoff sensitivity do not depend on the cycle proxy, so those tables are unchanged.

One suggested sentence was not adopted. The review says team-level \(H_1\) is zero by construction in every frame, because the printed split \(k\le 2\) in 93.6% and \(k=3\) in 6.4% appears to cover the sweep. Those two percentages are one-decimal rounding. At \(\delta=23.0\) m the 436,648 complete frames include 141 frames with \(k=4\) (0.032%). No frame has \(k>4\). A loop is impossible for \(k\le 3\). It is not impossible by construction on those 141 frames. Ripser was run on that tail: the \(H_1\) count is zero. The Remark states both facts.

The geometric representative was also replaced, rather than annotated. The review asked for a sentence saying that a midpoint proxy can close after birth. The revised paper no longer uses that proxy. Each bar is assigned the 1-cycle returned by column reduction of the Vietoris–Rips boundary matrix. On all 403 primary-match bars that cycle is present at birth.

---

## Points that go beyond readability

### 1. Remark: three points cannot carry a Vietoris–Rips loop

**Addressed in** the abstract, Remark (Results, team-level \(H_1\)), Section 2.3, Section 4.2, and the Conclusion.

The Remark is retitled “Team-level \(H_1\) needs four centroids.” It states that three pairwise-connected vertices span a 2-simplex as soon as the last edge enters, so \(k\le 3\) cannot carry a loop. The recomputed split at \(\delta=23.0\) m is \(k\le 2\) in 93.6%, \(k=3\) in 6.4%, and \(k=4\) in 141 frames (0.032%), with no frame above four. The computed \(H_1\) count on those 141 frames is zero. The 1,500-frame sample contains one of them, and that frame has no loop either.

The abstract no longer says that loops appear at the first two levels and not the third. It says a loop needs at least four vertices, that this count occurs in 141 of 436,648 frames at the team cutoff, and that no team-level loop is present. The same statement is in Section 4.2. The Conclusion no longer treats absence at the team level as a truncation result.

The review’s suggested abstract line, “Loops are possible at the first two levels only, and appear at both,” was not used. It would still describe the 141 four-centroid frames as impossible.

### 2. Three-vertex cycles in Sections 2.5 and 3.3

**Addressed in** Section 2.5 and Section 3.3.

Section 2.5 no longer enumerates cycles of at least three vertices, and it no longer describes a breadth-first search or a fallback to \([\tfrac12\mathrm{birth},\mathrm{death}]\). That fallback was not in the code. The representative is the reduced boundary of the triangle that destroys the class. A triangle cannot represent a bar: three vertices span a 2-simplex at the filtration value of their longest edge.

On the primary match the representative is a simple cycle for all 403 finite bars. The cycles have four to thirteen vertices, and 352 of the 403 have four, five, or six. Birth–death values from the reduction match the stored Ripser diagrams to within \(10^{-5}\) m. Section 3.3 reports those lengths and drops “typically three to six vertices.”

### 3. Drawn cycles that do not exist at the plotted birth

**Addressed in** Section 2.5, Section 3.3, the Figure 3 caption, and the abstract.

The old Figure 3 edges were the midpoint proxy. On sample frame 95 the individual edges were 17.8–19.2 m, all after the birth at 15.6 m, and the tactical edges included lengths past the birth at 22.1 m. The caption’s 28.8 m did not match the drawn 28.7 m.

Figure 3 was rebuilt from the reduction cycles of the same two bars (the longest finite bar on that frame at each cutoff). The individual cycle has eight vertices and edges from 6.9 to 15.6 m. The tactical cycle has six groups, one a 14-player cluster, and edges from 14.6 to 22.1 m. In both panels the longest edge is the birth value. The two cycles use different vertices and are born at 15.6 m and 22.1 m.

“Every examined loop is realised in space” has been removed from the abstract, Section 3.3, Section 4.2, and the Conclusion. The replacement is that every examined bar has a simple-cycle representative present at birth. The review’s softer phrase, “closed-cycle proxy,” was not used, because the object is no longer a proxy.

### 4. “Truncation” in the framing but not in the method

**Addressed in** Question 2 (Section 1.3), Section 2.4, the Conclusion, and the abstract.

Question 2 no longer asks whether detection is robust to truncation. It asks whether every finite bar has a 1-cycle present at birth. The Conclusion says clustering at recovered interaction lengths, followed by Vietoris–Rips persistence on the centroids. Section 2.4 still ends at the diameter. The sentence “no additional finite bar appears beyond that diameter” has been removed, because at that extent the complex is already a full simplex and every \(H_1\) class on this corpus is finite.

The stored diameter check on the 1,500-frame sample found no extra finite bar relative to the earlier upper-quartile stop. The headline barcodes were not recomputed.

### 5. Mann–Whitney “of \(\Delta\) against zero”

**Addressed in** Section 2.6 and Section 3.6.

The test is a two-sided Wilcoxon signed-rank test of the stored \(\Delta\) values against zero. Exact zeros are discarded before ranking (SciPy `zero_method='wilcox'`). For these sample sizes the \(p\)-value is SciPy’s asymptotic approximation (`method='auto'`, SciPy 1.13.1). The two classes reported in the results have no exact zeros.

The means are unchanged: \(\Delta=-0.253\) m for on-ball engagement (\(n=8{,}927\)) and \(\Delta=+0.700\) m for build-up (\(n=618\)). The engagement bound remains \(p<10^{-13}\). The build-up bound is now \(p<10^{-7}\).

### 6. Smaller factual mismatches

| Comment | Where it is addressed |
|---|---|
| Figure 3(d) longest edge 28.7 m against a caption range to 28.8 m | Figure 3 and Section 3.3. The tactical edges are 14.6–22.1 m. The longest edge equals the birth. |
| Gudmundsson and Horton pages printed as 22–12234 | `references.bib`, and a colon exception in `sn-mathphys-ay.bst`. The compiled PDF reads 22:1–22:34. |
| Only Gudmundsson and Horton (2017) is a survey | Section 1.3. Grund (2012) and Buldú et al. (2019) are named as network studies. |
| Bottleneck 95th percentile compared with the primary-match tactical mean | Section 3.5. The ten-match 95th percentile, 3.556 m, is compared with the ten-match tactical mean, 3.411 m. |
| Section 4.4 says “(Paper B)” | Section 4.4 now says “a companion manuscript,” as Section 3.6 does. |
| Reference order | Buldú now follows Botnan and Bubenik. A sort key `\noopsort{Buldu}` was added so the accent does not place Buldú first. The `.bib` file was not reordered. The journal style still prints Gudmundsson before Ghrist, Hiraoka before Herbert-Read, and Tralie before Topaz. |

---

## Readability patterns

### Demonstrative chaining

**Addressed** in the passages the review marked, not by a sweep of every pronoun.

The Section 2.3 merge-curve paragraph now uses “whereas” and “Because the curve flattens.” Section 4.2 no longer opens the team-level sentence with “almost never.” Section 4.4 no longer uses “That movement.” Section 4.5 no longer uses “That is a difference.” The Outlook no longer runs “That sample will / It is also the setting / That is the setting.” “That match was chosen” in Section 3.2 is now “The match was chosen.”

A few sentences still open with “This” or “Those” where the noun is the subject just named (the subsample in Section 2.1, the levels in Section 3.1, the diagnostics in Section 2.3). They were left because merging them would have joined two jobs into one sentence.

### “Filtration lifetime is not time”

**Addressed.** The definition is in Section 2.4: filtration lifetime is death minus birth, in metres, and none of the summaries is a duration in seconds. The Table 1 caption keeps the reminder: “not a duration in time.” The repetitions in Section 4.2 and the Figure 4 caption have been removed. The abstract says “mean bar length” so the term is not used before it is defined.

### Terminology

**Addressed in part.**

- “Roster statements” is now “targets are group counts” in Section 2.3 and the Figure 2 caption.
- Figure 2(a) is labelled “Mean group count \(\overline{k}\).”
- Section 3.1 states that at filtration zero \(H_0\) equals the group count \(k\) by construction. The suggested sentence was not placed in Section 2.2. The equivalence is stated where the subsample is compared with the sweep.
- “Level” remains the name of the three organisational levels. “Regime” is still used for the observed \(H_0\) and \(H_1\) patterns in the abstract and the discussion. A global replacement was not made.

### Competitive dependence

**Addressed.** The sentence has been removed from Section 1.1. Section 2.1 states it once: opposition couples successive positions (competitive dependence), and that inference problem is not treated here.

### Signposting of the four questions

**Addressed.** Sections 3.1, 3.2, 3.5, and 3.6 each open with “Addressing question.” Section 3.5 had been the missing label.

### The Discussion repeats the Results

**Addressed in part.** Section 4.3 is unchanged in role: it says why the Section 3.5 results support complementarity. Section 4.4 keeps the two means, because those are what the check shows, and then says that multiple-testing control and a football reading belong to a companion manuscript. It no longer adds a separate interpretation of the direction. Section 4.2 still reports the two \(H_1\) regimes, then gives the four-centroid fact, which is not a restatement of a table.

---

## Section-by-section suggestions

### Abstract

**Addressed in substance.** Football and “positions in metres” now appear in the results sentence, not between the question and the method. “Filtration lifetime” is not used. The team-level sentence and the representative sentence follow point 1 and point 3 above.

The review’s single rewritten abstract was not pasted in. The existing sentence breaks were kept, and the false claims inside them were replaced.

### Section 1.1 and Section 1.2

**Addressed.** Section 1.1 now ends on the prior applications. “This paper asks whether…” is the last sentence of Section 1.2. The competitive-dependence sentence is in Section 2.1.

Section 1.2 now opens the contrast with “More general responses exist, but neither returns a scale-attributable diagram.”

### Section 1.3

**Addressed.** The pipeline is three numbered steps: the cutoff and the centroids, Vietoris–Rips persistence out to the diameter, and the reduction cycle present at birth. The third step does not say “closed-cycle proxy.”

### Section 2.1

**Not rewritten in full.** The reason for subsampling is already stated before the stride: consecutive frames share nearly the same configuration, so summaries are estimated on a uniform subsample. The suggested “Because…” opening was not substituted. The 1 Hz event check is still summarised here, with the test specified in Section 2.6. The competitive-dependence sentence was added, as requested under Section 1.1.

### Section 2.2

**Not reordered.** The subsection still names the three levels and then points to the figure and the clustering rule. The levels are introduced in Section 1.2, and this subsection instantiates them on the football cloud. Moving the definition ahead of the names would separate the names from that instantiation.

### Section 2.3

**Addressed.** After the tie-break, the paragraph states that each target is a statement about the number of groups, not about distance. The tactical rule keeps \(k\ge 4\) because a loop needs four vertices. The reviewer’s merge-curve paragraph, with “whereas” and “Because the curve flattens,” replaces the “That flattening” chain. The three rules are still listed before this motivation, because the list is the definition of the estimator and the following sentences say what the targets mean.

### Section 2.4

**Addressed.** The filtration paragraph ends at “every \(H_1\) class on this corpus is finite.”

### Section 3.1

**Addressed.** The opening is “the uniform subsample reproduces the three group-count levels.” It states that at filtration zero \(H_0=k\) by construction, so the check is the match to the full-sweep counts.

### Section 3.2, null-comparison paragraphs

**Addressed.** The null is motivated before the tables: presence alone cannot separate arrangement from group count, because more centroids close more cycles. The floor (no loops in the 40.6% of frames with four or fewer tactical groups) is then read off Table 4, after the reason for the null.

### Section 3.3

**Addressed.** “Four nearby players” and the edges 17.8–19.2 m are gone. The individual cycle has eight vertices, seven of them singletons and one a pair. The sentence that the two cycles are not the same bar now gives the reason: different vertices, born at 15.6 m and 22.1 m.

### Section 3.5

**Addressed.** The subsection opens with “Addressing question.” The Fisher paragraph states why the odds ratio 6.12 does not undermine complementarity: individual loops are present in almost every frame, so joint presence is expected once a tactical loop forms. The weak rank correlation remains the main evidence. The bottleneck comparison uses the ten-match tactical mean, as in point 6.

### Section 4.5

**Addressed.** “Robust against over-partitioning artefacts” has been deleted. Single linkage is retained because its definition is the direct reading of spatial proximity. Chaining is named as one source of the gap with complete linkage (802) and Ward’s method (822) against single linkage (106). The gap stays open. The sparse-identification paragraph is one sentence: a choice of dynamical state, a defence of the library against AIC, BIC, or cross-validation, and a check that the persistence sequence is lower-dimensional under the selected linkage.

### Section 4.6 and the Conclusion

**Addressed.** “Truncation” is removed from the Conclusion. The Outlook no longer chains “That sample will,” “It is also the setting,” and “That is the setting.”

---

## What a reader should not expect to have changed

The adopted cutoffs remain 2.75 m, 11.75 m, and 23.0 m. Individual presence remains \(96.5\%\pm 1.5\%\) (mean bar length 1.886 m) and tactical presence \(18.8\%\pm 6.5\%\) (mean bar length 3.411 m). The primary-match counts remain 378 and 25 loops, with conditional means 1.931 m and 3.778 m. The null excesses remain +9.7 and +5.1 percentage points. The Fisher odds ratio remains 6.12. The event means remain −0.253 m and +0.700 m.
