# Review of "Multi-Scale Persistent Homology for Competitive Collective Systems"

**Reviewer focus:** readability, with content changes only where an error can be evidenced
**Date:** 25 October 2026

---

## Overall assessment

The paper is well scoped. The four questions in Section 1.3 are each answered, the numbers agree across sections, and the restrained tone suits the claims. I checked the arithmetic throughout, and it holds:

- Table 1: 378/150 = 2.52.
- Table 4: rows sum to 1,500. Weighted observed presence gives 282 frames, which is 18.8% and matches Table 6. Weighted null presence is 9.06%.
- Fisher odds ratio: (280 × 51)/(1,167 × 2) = 6.12.
- Merge rates in Section 2.3: 14 groups over 9 m ≈ 1.56 per metre, and 3 groups over 11.25 m ≈ 0.27 per metre.
- Team-level k distribution: mean 1.96.

The main readability problem is linking. The prose is mostly short declarative sentences, and each one points back to the previous sentence with "That", "This" or "Those". This keeps the tone neutral, but it makes the reader rebuild the logic connecting the sentences. Most fixes below merge sentence pairs and state the logical relation directly ("because", "so", "whereas", "but").

Before the readability notes, the next section lists points where there is a real error or an inconsistency a referee would catch, with the evidence for each.

---

## Points that go beyond readability

### 1. Remark 1: three points cannot carry a Vietoris–Rips loop

The Remark says frames with k = 3 "are the only team-level configurations in which a loop is possible." This is not correct. The Vietoris–Rips complex is a flag complex: once all three edges among three points are present, the 2-simplex they span enters at the same filtration value. So three points can never carry a non-trivial H1 class, and a Rips loop needs at least four vertices.

The paper already relies on this fact elsewhere. The tactical rule in Section 2.3 requires k ≥ 4 "so that a loop remains possible," and Table 4 shows zero observed loops for k ≤ 4. The paper's own figures say team-level k ≤ 2 in 93.6% of frames and k = 3 in 6.4%, which together make 100%. Team-level H1 is therefore zero **by construction in every frame**, not just in most of them.

This strengthens the Remark, but it changes how the result should be stated. "Loops appear at the first two levels, not the third" (abstract, Section 3.2, Conclusion) reads like an empirical finding, when it is a structural consequence of the team cutoff. A possible correction:

> At δ = 23.0 m the 22 players reduce to at most three centroids in every complete frame of the ten-match sweep (k ≤ 2 in 93.6%, k = 3 in 6.4%; Section 2.3). A Vietoris–Rips complex needs at least four vertices to carry a non-trivial 1-cycle, since three pairwise-connected vertices span a 2-simplex as soon as the last edge enters. Team-level H1 is therefore zero by construction.

In the abstract, something like "Loops are possible at the first two levels only, and appear at both" would be accurate.

### 2. Three-vertex cycles in Sections 2.5 and 3.3

The same flag-complex fact affects the cycle proxy. Section 2.5 enumerates cycles of "at least three vertices." Section 3.3 says individual-level cycles are "typically three to six vertices." A three-vertex cycle in a Rips complex is always the boundary of a triangle, so it cannot represent a non-trivial H1 class. Because breadth-first search favours short cycles, the enumeration will find triangles first.

Either the "three" in Section 3.3 is a slip, or the proxy sometimes returns a cycle that cannot represent the class. The code is worth checking. The fix may be a minimum of four vertices in Section 2.5, or a filter that rejects any cycle filled by triangles below death.

### 3. Drawn cycles that do not exist at the plotted birth

In Figure 4(a), the marked individual-level pair appears to be born at about 15.5 m and to die at about 22 m (reading from the plot). The representative drawn in Figure 3(b) has edges of 17.8–19.2 m, so that cycle closes only at 19.2 m, after the plotted birth. The tactical case behaves the same way: birth is about 22.2 m, but the drawn cycle contains a 28.7 m edge.

This follows from the stated rule. The representative is the cycle whose edges lie nearest the midpoint of the interval, and it is explicitly a proxy, not a generator. A reader who compares the two figures will still stop at this, so one sentence in Section 2.5 or the Figure 3 caption would prevent it, for example:

> Because the proxy is chosen near the midpoint of the interval, its longest edge can exceed the birth value of the bar it represents.

For the same reason, "Every examined loop is realised in space" (abstract) and "receive a geometric realisation" (Section 3.3) claim slightly more than the method gives. "Every examined loop has a closed-cycle proxy in space" fits the paper's reserved register better.

### 4. "Truncation" appears in the framing but not in the method

Question 2 in Section 1.3 asks whether detection is robust to "the cutoff and truncation choices." The Conclusion credits "a truncation of the Vietoris–Rips parameter." Section 2.4, however, runs the filtration to the full diameter of the reduced cloud, at which point the complex is a full simplex. Nothing is truncated, and Section 3.4 tests only the cutoff.

This looks like leftover wording from an earlier draft. Suggested fix: drop "and truncation" from Question 2 and rephrase the Conclusion as "computing Vietoris–Rips persistence on the cluster centroids."

### 5. Mann–Whitney "of Δ against zero"

The Mann–Whitney U test compares two independent samples. Testing a single sample of Δ values against zero is the Wilcoxon signed-rank test. If the five pre-event frames were compared with the five post-event frames as two samples, the description should say so. If Δ was tested against zero, the test name should change. Either way, Sections 2.6 and 3.6 currently describe a combination that does not exist.

### 6. Smaller factual mismatches

- **Figure 3(d) edge length.** The figure labels the longest edge 28.7 m, but the caption and Section 3.3 give the range as 21.1–28.8 m.
- **Gudmundsson and Horton page numbers.** The reference reads "22–12234." ACM Computing Surveys uses article numbering, so this should be 22:1–22:34.
- **Survey attribution.** "Spatial analysis of team sport is surveyed by Gudmundsson and Horton (2017) and by Buldú et al. (2019) and Grund (2012)." Only the first is a survey; the other two are network-analysis studies. Suggested wording: "…is surveyed by Gudmundsson and Horton (2017); network approaches include Grund (2012) and Buldú et al. (2019)."
- **Bottleneck comparison baseline.** Section 3.5 compares a ten-match bottleneck median (1.456 m) with the primary-match tactical mean (3.778 m). The like-for-like comparison is the ten-match mean of 3.411 m. That comparison also reads well: the 95th-percentile bottleneck (3.556 m) almost equals the ten-match tactical mean.
- **Unnamed companion paper.** Section 4.4 refers to "(Paper B)." A referee will not know what this is, and the other sections say "companion manuscript."
- **Reference order.** A few entries are out of alphabetical order (Buldú/Botnan/Bubenik, Gudmundsson/Ghrist/Grund, Hiraoka/Herbert-Read, and the T entries). The reference style may handle this automatically.

---

## Readability: patterns across the whole paper

### Demonstrative chaining

Many sentences open by pointing back: "That display remains…", "That series can detect…", "That flattening is why…", "That match was chosen…", "That is a difference of…", "That gap is large enough…", "That movement is…", "That sample will…", "That is the setting in which…". Each one is clear in isolation. Together they produce a stop-start rhythm and hide whether the next sentence is a consequence, a contrast or an aside.

A practical rule: where "That/This X" restates the subject of the previous sentence, merge the two sentences with the logical connective. For example:

**Before:**

> The curve is asymmetric. Nearby agents merge quickly, at about 1.6 groups per metre from k = 19 to 5. Larger gaps then resist merging, at about 0.27 groups per metre from 5 to 2. The remaining gaps are the large between-group distances. That flattening is why the team cutoff sits far out at 23.0 m and still returns two envelopes, not two teams.

**After:**

> The curve is asymmetric. Nearby agents merge quickly, at about 1.6 groups per metre between k = 19 and 5, whereas the remaining large between-group gaps resist merging, at about 0.27 groups per metre between 5 and 2. Because the curve flattens, the team cutoff sits far out at 23.0 m and still returns two spatial envelopes rather than the two teams.

### The "filtration lifetime is not time" caveat is repeated

It appears in Section 2.4, the Table 1 caption, Section 4.2 and the Figure 4 caption, and Section 2.1 makes a related point. Define it firmly once in Section 2.4 and keep one reminder in the Table 1 caption, where readers first meet the numbers. Removing the other repetitions makes Section 4.2 and the Figure 4 caption noticeably smoother.

### Terminology drifts between near-synonyms

The paper uses "group count", "cluster count" (Figure 2 axis), H0, k and β0 for the same quantity, and "level", "scale", "regime" and "organisational level" for related ideas. Most are defined, but a reader still has to check each time whether two words mean the same thing.

Suggestions:

- Add a short statement in Section 2.2: "k, the group count, equals H0 (β0 at filtration zero) and is used interchangeably with it."
- Keep "level" for the three named levels and "regime" only for the observed H0/H1 patterns.
- Rename the Figure 2(a) axis to "Mean group count k̄."

### Unexplained in-house terms

"Roster statements" (Section 2.3 and the Figure 2 caption) is not a standard phrase, and readers will not know whether "roster" refers to football squads. "Targets stated as group counts" says the same thing plainly. Similarly, "competitive dependence" appears once in Section 1.1, in a sentence that has little connection to what surrounds it.

### Inconsistent signposting

Sections 3.1, 3.2 and 3.6 open with "Addressing question N," but Section 3.5 (question 3) does not. Either label all four or none. Labelling all four suits a paper built around a fixed set of questions.

### The Discussion repeats the Results

Sections 4.2 and 4.4 largely restate numbers already given (−0.253 m, +0.700 m, "[6, 14] m"). Section 4.4 could be two sentences: what the check shows and what it does not. Section 4.3 is the strongest discussion paragraph, because it explains why the Section 3.5 results imply complementarity instead of repeating them.

---

## Section-by-section suggestions

### Abstract

The sentence "Positions are recorded in metres on a standard football pitch" comes between the research question and the method, before the reader knows football is the test case. "Filtration lifetime" is used before it is explained. A revised version that keeps the content:

> Competitive collective systems, including sports teams contesting a pitch, organise at several named levels at once: individuals, small groups, and a system-wide envelope. Persistent homology records connected components (H0) and loops (H1) as a distance parameter grows, but on the full point cloud those levels mix in one diagram, so a change cannot be assigned to a level. This paper asks whether the homology can be made scale-attributable, with each diagram belonging to one organisational level. Levels are named by how many groups they contain rather than by an assumed length, and a cutoff sweep recovers the corresponding distances from the group-count curve. Hierarchical clustering at those distances reduces the cloud to group centroids, on which persistent homology is computed. On ten professional football matches (broadcast tracking at 10 Hz, positions in metres), three H0 regimes appear: individual (2.75 m), tactical (11.75 m), and team (23.0 m). Loops are possible only at the first two levels, and appear at both: individual-level loops in 96.5% ± 1.5% of frames (mean bar length 1.886 m) and tactical-level loops in 18.8% ± 6.5% (mean bar length 3.411 m). Every examined loop has a closed-cycle proxy in space, and the two levels carry distinct information. The same pipeline applies to other bounded competitive systems once interaction lengths are re-derived.

### Section 1.1, final paragraph

This paragraph covers three topics: prior applications, the research question, and a scope exclusion. The research question is the most important sentence in the Introduction and is buried here. Suggested changes:

- End 1.1 after the Topaz et al. example.
- Make "This paper asks whether…" the last sentence of 1.2, where it follows directly from the problem.
- Move the competitive-dependence sentence to Section 2.1, which already refers back to it.

### Section 1.2

This section reads well; it has the best linking in the paper. One small change: "Responses for the general case exist, but they do not return a scale-attributable diagram" could open with a contrast, such as "More general responses exist, but neither returns a scale-attributable diagram," which links more clearly to the two methods discussed next.

### Section 1.3, second paragraph

This paragraph is six short sentences that the reader has to assemble into a pipeline. Numbering the steps in prose fixes this:

> The pipeline has three steps. First, a cutoff distance δ groups nearby agents and each group is replaced by its centroid; the reduced cloud represents one organisational level, named by how many groups it contains. The value of δ is not assumed but read from the group-count curve (Section 2.3). Second, Vietoris–Rips persistence is computed on the centroids, with the filtration running to the diameter of the reduced cloud (Section 2.4). Third, each H1 bar is given a closed-cycle proxy in space (Section 2.5).

### Section 2.1

The subsampling paragraph puts notation before purpose. A version that states the reason first:

> Because consecutive frames share nearly the same configuration, component and loop summaries are estimated on a uniform subsample rather than the full stream. Every match uses the same rule: list the complete 22-player frames, set the stride to ⌊N/150⌋, and retain 150 frames. …

The last paragraph of 2.1 (event check, 1 Hz, Figure S1) repeats Section 2.6 closely. Keep one sentence here and leave the details to 2.6.

### Section 2.2

The order is: name the levels, then the figure pointer, then the method. Defining the clustering first and naming the levels afterwards reads more naturally, because the names only make sense once the reader knows a level is a group count.

### Section 2.3

The three rules are listed before they are motivated, and the motivating paragraph begins with the tie-break rule, which is the least important point. A suggested replacement for that paragraph, which also builds in the four-vertex fact from point 1:

> Each target is a statement about the number of groups, not about distance. The individual target, n − 3 = 19, leaves most agents resolved individually. The tactical target, 5, is a handful of coordinating groups; requiring k ≥ 4 in at least half of frames keeps a loop possible, since a Vietoris–Rips loop needs at least four vertices. The team target, 2, is at most two spatial envelopes. Where a rule is satisfied equally at two values of δ, the smaller is taken.

### Section 2.4

"No additional finite bar appears beyond that diameter" adds nothing, because the filtration stops at the diameter and the complex is already a full simplex there. Ending at "every H1 class on this corpus is finite" is cleaner.

### Section 3.1

"The homology sample confirms the three organisational levels read from the group-count curve" overstates what is shown. At filtration zero, H0 equals k by construction, so this section checks that the 150-frame subsample reproduces the full-sweep group counts. "The uniform subsample reproduces the three group-count levels of Section 2.3" is accurate and fits the tone.

### Section 3.2, null-comparison paragraphs

The current order is: the floor observation, then "Presence alone cannot separate…", then the null, then the tables. Putting the reason for the null first gives a cleaner argument:

> Presence alone cannot separate arrangement from group count, because more centroids close more cycles. The matched null of Section 2.6 holds both the group count and the spatial envelope fixed and randomises only the arrangement. Against that null, tactical presence is 18.8% compared with 9.1%, an excess of +9.7 percentage points (Table 3). Table 4 shows where the excess arises. No loops appear in the 40.6% of frames with four or fewer tactical groups; presence then rises from 9.3% at k = 5 to 67.0% at k = 8 and stays above the null at every k. At the individual level the null rate is already 91.4%, since twenty points in a bounded region almost always close a cycle, so the observed excess is modest (+5.1 percentage points).

### Section 3.3

"At δ = 2.75 m the vertices are four nearby players" sits next to cycle edges of 17.8–19.2 m, so "nearby" reads as a contradiction. "Four players, each a singleton cluster" says what is meant.

"The two cycles are not the same bar at two resolutions" is an important point. It would be clearer to give the reason in the same sentence (different vertex sets and different birth values), rather than leaving the reader to work it out from Figure 4.

### Section 3.5

The Fisher paragraph currently reports co-occurrence above chance, then the asymmetry, then the statement that correlation remains the main evidence. It never explains why above-chance co-occurrence does not count against complementarity. A version that supplies the missing link:

> Presence at the two levels co-occurs more often than chance (Fisher odds ratio 6.12, p = 0.002; bootstrap CI [2.32, 16.33]), but the association is one-sided (Table 6). In 1,167 frames individual loops appear without a tactical partner; in only two does the reverse occur. Because individual loops are present in almost every frame, joint presence is expected whenever a tactical loop forms and does not imply that the two levels record the same structure. The weak rank correlation therefore remains the main evidence for complementarity.

### Section 4.5

The linkage paragraph is the most important limitation and currently reads as a list of facts. One connective helps.

"It is also robust against over-partitioning artefacts" is asserted without support, and single linkage is better known for the opposite failure (chaining), which a referee may raise. Suggested wording:

> We retain single-linkage because its definition is the most direct reading of spatial proximity, while noting that its tendency to chain is one source of the gap.

The SINDy paragraph lists "First… Second… Third…" in short sentences. It would read better as one sentence with a colon.

### Section 4.6 and Conclusion

Both read well once the "truncation" wording is fixed. In the Outlook, "That sample will…" followed by "It is also the setting…" and "That is the setting in which…" is the densest run of demonstratives in the paper and would benefit most from merging.

---

## Summary of priorities

1. **Content fixes first:**
   - the three-point Rips claim (Remark 1 and its echo in the abstract and Conclusion);
   - the three-vertex proxy cycles;
   - the leftover "truncation" wording;
   - the Mann–Whitney naming.
2. **Readability changes with the most effect:**
   - move the research question to the end of 1.2;
   - present the 1.3 pipeline as numbered steps in prose;
   - reorder the 2.3 justification and the 3.2 null paragraphs;
   - add the missing link in the 3.5 Fisher paragraph;
   - remove the repeated "lifetime is not time" caveats;
   - break up the "That/This/Those" chains with explicit connectives.

None of these changes the tone, and most make the text shorter.

