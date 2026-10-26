I can't save files in this conversation, so the full second review is below as Markdown. Copy everything inside the code block into a file named something like `review_2.md`.

````markdown
# Re-review: "Multi-Scale Persistent Homology for Competitive Collective Systems" (revision 1)

**Reviewer focus:** readability, with content changes only where an error can be evidenced
**Date:** 26 October 2026
**Documents reviewed:** revised manuscript; *Response to Independent Review 1*

---

## Summary

The revision is a clear improvement. The two substantive changes, the reduction-based cycle representative and the corrected Remark 1, make the paper stronger rather than just patching it. Figures 3 and 4 now agree with each other: the drawn cycles close at 15.6 m and 22.1 m, which match the plotted births of about 15.5 m and 22.2 m. The text, captions and tables are consistent wherever I checked.

One correction to the previous review. It said team-level H1 was zero "by construction in every frame." That conclusion came from adding two rounded percentages, which was not a safe inference. The 141 frames with k = 4 show it was wrong. The revised Remark now handles this correctly: impossible on k ≤ 3, computed and found absent on k = 4. Declining the suggested abstract line was also right.

The remaining points are mostly small. Three are about logic or precision rather than wording, so they are listed first.

---

## Points of substance

### 1. "Present at birth" is a property of the method, not a finding

The reduced column of the destroying triangle always has the creating edge as its lowest entry. So every edge enters no later than birth, and the cycle exists at birth for every bar, in any dataset. Section 2.5 says this correctly.

The problem is that Question 2 ("is every finite bar represented by a 1-cycle present at birth"), the abstract and the Conclusion present it as something the data showed. The empirical result is that the representative is a *simple* cycle for all 403 bars, so it can be drawn as a single ring in space. A reduced column could, in principle, be a sum of several cycles or pass through a vertex more than once. Suggested rewording:

**Question 2:**

> …does scale-attributable persistent homology then detect H1 loop structure at those levels, does each finite bar have a simple-cycle representative that can be drawn in space, and is detection robust to the cutoff?

**Abstract and Conclusion:**

> On the primary match, every finite H1 bar has a simple-cycle representative, present at birth by construction.

### 2. Scope of "every examined"

The simple-cycle check covers the 403 primary-match bars, not the 4,345 bars in the ten-match sample. Section 3.3 makes this clear. The abstract ("Every examined loop") and the Conclusion ("Every examined H1 bar") leave it to the reader to infer. Naming the primary match in both places removes the ambiguity. This should take a line or two, and it is worth doing so a referee does not ask whether the other nine matches were checked.

### 3. Section 4.4: "the same direction"

"The same two classes move in the same direction at the tactical level" can be read as engagement and build-up moving in the same direction as each other. They move in opposite directions. Suggested wording:

> At the tactical level, both classes move in the same directions as at the individual level.

---

## New linking problems introduced by the edits

These come from sentences that were moved or merged, which changed what pronouns and connectives refer to.

### Section 1.3, related work

After the split, "Those methods include pitch-control models and network metrics" follows "Network approaches include Grund (2012) and Buldú et al. (2019)." "Those methods" now refers to the network studies, which do not include pitch-control models. Suggested wording:

> Spatial analysis of team sport is surveyed by Gudmundsson and Horton (2017); network approaches include Grund (2012) and Buldú et al. (2019). Together these cover pitch-control models and network metrics on passing and collective structure, which complement the present pipeline but do not quantify two-dimensional enclosure through persistent homology.

### Section 1.3, opening sentence

Section 1.2 now ends with the research question, and 1.3 immediately restates it ("Section 1.2 leaves a concrete question: whether…"). The repetition stands out now that the two sentences are adjacent. Opening 1.3 with this is enough:

> This paper answers that question by changing the input rather than slicing bars of one diagram.

### Section 2.1, competitive dependence

The moved sentence sits between two statements about the subsample and does not connect to either. Suggested wording:

> This subsample limits temporal pseudo-replication but does not remove a second dependence: opposition couples successive positions (competitive dependence), an inference problem not treated here. Nor can the subsample resolve formation or dispersion of loops between samples.

### Section 2.5, reversed causation

"The complex uses every edge and every triangle on the centroid cloud, so the filtration runs to the diameter." It works the other way round: because the filtration runs to the diameter, the complex contains every edge and triangle. Suggested wording:

> Because the filtration runs to the diameter, the complex contains every edge and every triangle on the centroid cloud.

### Section 2.4, the same issue in a milder form

"Each reduced cloud has at most 22 centroid points, so pairwise inter-centroid distances are bounded. The filtration therefore runs to the diameter." Bounded distances do not imply the choice; the small size makes the full filtration cheap. Suggested wording:

> Each reduced cloud has at most 22 centroids, so the full filtration is inexpensive and is run to the diameter: the maximum pairwise distance between centroids.

### Section 4.5, "which we leave open"

In "Its tendency to chain is one source of the gap with complete linkage and Ward's method, which we leave open," the relative clause attaches to "Ward's method." Also, "is one source" states as fact something the paper does not test. Suggested wording:

> Its tendency to chain is a likely source of the gap with complete linkage and Ward's method; resolving that gap is left open.

### Section 4.6, "The path is the sample"

A path is not a sample. Suggested wording:

> This representation is the setting in which the landscape-stability cutoff can be evaluated, with the match-level landscape, not the per-frame summary, as the resampling unit.

---

## Repetition created by the revision

### The four-vertex fact

It now appears five times: the abstract, Section 2.3, the Figure 2 caption, Section 2.5 and Remark 1. Section 2.3 gives the full reason. The Remark needs it because its argument depends on it. Section 2.5 and the abstract can state it briefly or refer back. The cost is the same as the old filtration-lifetime caveat: it suggests the reader may not have taken it in the first time.

### Cycle-length statistics

"Four to thirteen vertices, and 352 of the 403 have four, five, or six" appears in both Section 2.5 and Section 3.3. It is a result, so it belongs in 3.3. Section 2.5 should end once the method is defined. The Ripser agreement check (10⁻⁵ m) can stay in 2.5 as a validation of the implementation.

### H0 = k in Section 3.1

The new second sentence says H0 equals k by construction. Two sentences later, "Throughout, H0 is the group count… Equivalently, it is β0…" says it again. Delete the second statement.

---

## Smaller wording points

- **Abstract antecedent.** In "A Vietoris–Rips loop needs at least four vertices. At the team cutoff that happens in 141 of 436,648 frames," it is unclear what "that" refers to. Suggested wording: "At the team cutoff, four centroids occur in only 141 of 436,648 frames, and none carries a loop."
- **Section 3.5 grammar.** "In only two frames the reverse occurs" needs inversion after a restrictive opener: "In only two frames does the reverse occur." Also, "and the association is one-sided" would read better with "but," since the sentence is a contrast.
- **Figure 3 caption.** "Eight vertices in (b) and six in (d), not the bar of largest p on the match" reads as if the vertices are being contrasted with a bar. Suggested wording: "These are the longest bars on frame 95, not the longest on the match; the cycles have eight vertices in (b) and six in (d)."
- **Section 3.4.** In "not confined to the adopted cutoff alone," "alone" is redundant.
- **Hyphenation.** "single-linkage" and "single linkage" are both used as nouns in Section 4.5. Hyphenate only when the term modifies a noun ("single-linkage cluster").
- **Tolerances.** Section 2.4 reports agreement with GUDHI and giotto-tda to 10⁻⁶ m, while Section 2.5 reports agreement with Ripser to 10⁻⁵ m. If the looser tolerance is just the stored precision, a few words saying so would stop a careful reader wondering why they differ.
- **Figure 1(g).** The schematic still draws grey diagonals across the quadrilateral, and the caption does not say what they are. For a four-cycle to carry a class at birth, both diagonals must enter after its longest side. Unexplained diagonals invite the opposite reading. A short note such as "grey diagonals enter at death" would settle it.
- **Wilcoxon and means.** The signed-rank test concerns the location of the Δ distribution, roughly its median under symmetry, but Section 3.6 reports means. A referee may ask for medians alongside the means. This is optional, and the nominal-p framing already limits the claim.

---

## References

Buldú is now correctly placed. Gudmundsson still precedes Ghrist and Grund, Hiraoka precedes Herbert-Read, and Tralie precedes Topaz. An author-year .bst would not produce that order from the surnames alone (h < u, e < i, o < r). This suggests stale `key`, `sortkey` or `\noopsort` fields in those `.bib` entries rather than journal-style behaviour. It is worth a two-minute check, because copy editors flag it.

---

## Response document

The response is clear and well judged. Each declined suggestion has a stated reason, and the closing section on what has *not* changed is useful for an editor. The one place to tighten is Point 3, where "present at birth" is again framed as a finding. The same change as in point 1 above would apply there.

---

## Priorities

1. Reframe "present at birth" as true by construction, and name the primary match as the scope of the simple-cycle check.
2. Fix the Section 4.4 "same direction" ambiguity and the Section 1.3 "Those methods" antecedent.
3. Fix the remaining linking points (2.1, 2.4, 2.5, 4.5, 4.6) and the three repetitions.
4. Check the reference sort keys.

None of these affects a number in any table.