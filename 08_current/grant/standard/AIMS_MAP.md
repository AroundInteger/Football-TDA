# Standard Grant aims map

October 2026. UK English. Working note for the follow-on Engineering and Physical Sciences Research Council (EPSRC) Standard Grant.

This file is not a Joint Electronic Submission (JeS) draft. It does not amend the live Small Grant pack: `08_current/grant/live/02_Vision_and_Approach_REV4.md`, `08_current/grant/live/01_Summary.md`, `08_current/grant/live/T1_T2_Six_Registers.md`, or `08_current/grant/FOUNDATION.md`.

The Small Grant paragraph can only name a pathway. This note names the aims, the work packages that deliver them, what already exists, and what the Small Grant must hand over before each package can start.

## The grant in one sentence

The Small Grant proves two theorems for a persistence diagram treated as given. Theorem T1 is averaging under competitive dependence. Theorem T2 localises a transition once the change exceeds a perturbation of that diagram. The Standard Grant asks when that diagram is a stable function of the point cloud, and whether the answer survives one change of system.

Two mathematical questions stay distinct and can proceed in parallel. They meet at the merge: single-linkage clustering jumps when a pairwise distance crosses the cutoff.

- **Conservation.** After clustering at a fixed linkage and cutoff, how much of the raw diagram survives replacement by centroids. Home: `08_current/Paper Updated/3-Paper Paradigm/working_foundations.md` §12 Question 1, and `08_current/grant/evidence/toy_models/DECOMPOSITION_ERROR_PROGRAMME.md`.
- **Linkage.** How the centroid diagram moves when the linkage rule, the cutoff, or the cloud is perturbed. Home: collaborator comment C5 in `08_current/Paper Updated/3-Paper Paradigm/COLLABORATOR_COMMENTS_OCT2026.md`. C5 sharpens Question 1 and does not replace it. The comparison is with Cohen–Steiner stability of diagrams of point clouds, and with Schindler and Barahona, who apply persistent homology to a sweep of clusterings. The map here is persistent homology of the centroid cloud after clustering. Algebraic ownership sits with the mathematics co-lead.

Paper C remains the synthetic diagram mean-path and change-point note. C5 keeps both questions out of Paper C's T1-lite and T2-lite.

## What already exists

### Enough to start Aim 1 before the Small Grant is awarded

The toy in `08_current/grant/evidence/toy_models/AdversarialTDA_Specification.md` computes persistent homology on the raw hierarchical cloud. It has exact Wasserstein distances, a diagram Fréchet mean, a Page cumulative sum (CUSUM), and a known ultrametric hierarchy. It does not cluster. The decomposition programme is a four-step module and has not been run.

The unconditional bound is already known, and it is too loose where it is needed. Let \(\rho_\delta(X)\) be the largest distance from a point to the centroid of its cluster at cutoff \(\delta\). The Hausdorff distance from the raw cloud to the centroid cloud is at most \(\rho_\delta\). Vietoris–Rips stability then gives a bottleneck distance of at most \(2\rho_\delta\) between the two diagrams (Cohen–Steiner; Chazal, de Silva and Oudot). At a tactical cutoff that constant is on the scale of the loops being studied, so the bound does not separate preserved features from destroyed ones.

The statement worth proving is the scale-restricted form: features born above roughly \(\delta + 2\rho_\delta\) should be preserved with a sharper constant than features born near the cutoff. There is an obstruction to state first. The clustering map is discontinuous. Two agents at \(\delta - \eta\) and at \(\delta + \eta\) can produce different cluster counts and a jump in the centroids, so the usual stability theorem does not apply to the pipeline as written. The fix is a gap condition: if no minimum-spanning-tree edge lies in \([\delta - g, \delta + g]\), the partition is locally constant, and the composite map is 1-Lipschitz for perturbations smaller than \(g/2\).

Connected-component information is essentially the dendrogram. Single-linkage merge heights are the Vietoris–Rips \(H_0\) deaths, and the number of clusters at \(\delta\) is the dimension of \(H_0\) at that scale. The family of centroid clouds over all \(\delta\) re-encodes that barcode. Choosing three fixed cutoffs is then a sampling loss. The loss is zero when each cutoff sits in a gap of the death vector. The loss that matters for the open question is in the loops: replacing a cluster by its centroid destroys within-cluster geometry, and a loop in the centroid diagram is not a loop in the raw cloud.

The five experiments that test this are written under WP1 below. They were first set out in the August 2026 scale-decomposition discussion and are recorded here so the programme note can stand without that transcript.

Paper A already prints the empirical linkage gap and the cutoff sweep: 106 tactical \(H_1\) loops under single-linkage, 802 under complete-linkage, and 822 under Ward's method, on a 600-frame, four-match sample; 275 loops at 6 m and none at 16 m on the primary-match cutoff sweep. The cardinality-null check shows that tactical loops are carried by the arrangement of centroids, not only by how many centroids there are. Single-linkage stays the pre-specified proximity rule.

### Reserved for the transfer aim

`08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/` is a staging draft: ecology and robotics generators with re-derived gaps, diagram analogues of a mean path and a change-point, and figures. It may be written in parallel with Paper B, because the questions and datasets are independent. It is the synthetic rehearsal for Aim 3. It is not the theorem of Aim 1 or Aim 2.

`08_current/grant/evidence/toy_models/TOY_MODEL_PAPERS.md` §5.5 lists the transfer failures to adopt as written: after the interaction lengths are re-derived, the new system has no stable gaps; an encirclement loop does not appear for a natural ring; the CUSUM does not localise a programmed switch once noise is on the scale of the gap.

The Small Grant names two later settings: spatial predator–prey dynamics, including tumour–immune competition, and competitive logistics with autonomous-fleet coordination. Static topological analysis of tumour–immune images is a crowded literature. Serial imaging is the open observational path, and it needs a data agreement. Biologging global positioning system (GPS) tracks from the existing collaborator group are the nearer observational path. Armed-conflict data stay out of this grant, as they stay out of the Small Grant.

## What the Small Grant hands over

- **Month 2, cutoff gate.** Interaction lengths either transfer to the Championship batch or are re-derived. That is the rehearsal for Aim 3. Collaborator comment C5 allows one optional clause, only if a revision window opens and an equal cut is made elsewhere: the validation batch also records whether linkage and a small spatial perturbation preserve the diagrams that will be averaged. That record would feed Aim 2. The Small Grant theorems do not require it, and the live Vision does not currently contain it.
- **Month 7, barcode store and landscape library.** Research Associate deliverables. Aim 2's season package cannot start before this store exists.
- **Month 9 gates.** Empirical autocovariance decay consistent with the summable-mixing condition that T1 and T2 assume; the eigengap for the projected form of T2 recorded alongside; separation of at least three organisational states. Aims 1 and 2 inherit these as fixed hypotheses.
- **Months 9–12, T1 and T2, or the stated fallback.** If the landscape argument stalls, the Small Grant falls back to diagram-valued Wasserstein comparison and does not claim the T1 limit law. In that case this map is rewritten before Standard Grant drafting: the object of stability is the diagram, and a landscape form of the bound is dropped.
- **Month 12, evidence pack.** Drafting of the Standard Grant is scheduled from Month 9. This note is the brief for that draft.

The Small Grant does not prove the stability lemma, does not run the five toy experiments, and does not acquire a second dataset.

## Three aims

**Aim 1. What the centroid projection preserves.** For a fixed linkage, bound the bottleneck distance between the diagram of the raw cloud and the diagram of the centroid cloud by cluster radius, the gap around the cutoff, and cardinality. The bound has to be informative above the cutoff, where the unconditional factor of two is vacuous. Failure is visible: if every informative feature on the toy hierarchy sits inside the loose bound, and the gap condition never holds, the aim stops.

**Aim 2. How the centroid diagram depends on the clustering construction.** Characterise sensitivity to the linkage rule, the cutoff, and a small perturbation of the cloud. The season store from the Small Grant is the empirical object. The theorem is about the jump at a merge. It is a separate question from T1 and from T2. Failure is visible: if single-linkage, complete-linkage, and Ward's method agree on the season store once the cutoff lies inside a death gap, the order-of-magnitude pilot gap was a small-sample fact, and the aim narrows to cutoff and perturbation.

**Aim 3. One transfer test.** Re-derive interaction lengths on one non-football bounded competitive system and repeat the Aim 1 and Aim 2 checks. The workflow transfers. The metre values do not. The domain is not locked here. Synthetic ecology and pursuit–evasion already exist as Paper C. An observational system is added only when a data path is real, with biologging GPS tracks before serial tumour–immune imaging. Competitive logistics remains an outlook sentence, not a work package.

## Work packages

**Work package 1 (WP1). Synthetic conservation (Aim 1).** Extend the existing toy with centroid projection. Run the five experiments below. No SkillCorner data. This package can start while the Small Grant application is being finished. The output is a note of when the bound is tight and when it is vacuous.

The module, as already specified in the decomposition stub:

1. Fix the ground-truth ultrametric hierarchy (existing generators).
2. Cluster at \(\delta\) with the known merge tree and replace each cluster by its centroid.
3. Compare the diagram of the raw cloud with the diagram of the centroid cloud using the exact Wasserstein distances in `atda_core.py`.
4. Sweep \(\delta\), gap scales, and agent count, and report when the bounds are tight and when they are vacuous.

Do not mix this module with Figure 6 of the toy (scale conflation on a fixed point set) or with Paper C.

The five experiments, in order:

1. **Scale-restricted bottleneck.** Restrict both diagrams to bars with birth at least \(b\), and plot bottleneck distance against \(b\). A sharp drop once \(b\) exceeds roughly \(\delta + 2\rho_\delta\), followed by a near-zero plateau, is the shape of the lemma and an empirical value for its hypothesis. This is the check that distinguishes a lossy blur from a map that is exact above its own scale. Run it first.
2. **Merge crossing.** Slide two clusters together so their separation crosses \(\delta\), and track the bottleneck distance across the crossing. The expected picture is a spike at the merge, of a size set by the centroid displacement, and near-flat behaviour elsewhere. How that spike scales with cluster size is the amplification that would later enter T2's perturbation term.
3. **Competitive coupling at the merge.** Repeat the crossing under the toy's coupled generator and under the independent generator (`coupled` true and false). If competitive coupling crosses the merge more often, because the two groups physically close clusters, then the instability of the decomposition lines up with the events T2 is meant to locate. That result is worth knowing before a season-scale run.
4. **Tightness of the factor of two.** Plot the observed bottleneck distance against the certified \(2\rho_\delta\) across configurations. If the observed distance tracks \(\rho_\delta\) rather than \(2\rho_\delta\), with a stable ratio, there is a sharper constant to prove.
5. **Sampling three cutoffs.** Compare the full family of centroid clouds on a fine \(\delta\) grid with three sampled cutoffs. Then add noise until the gap in the death vector closes. The result says how much heterogeneity the cloud can carry before three cutoffs are the wrong summary of the dendrogram.

**WP2. Scale-restricted lemma (Aim 1).** Prove the bound under the gap condition. WP1 fixes the hypothesis, including the birth threshold and the constant. The mathematics co-lead owns the proof. The package starts when WP1 shows a plateau above the cutoff.

**WP3. Season sensitivity (Aim 2).** Pre-register linkage, cutoff, and perturbation checks on the Small Grant barcode store. The package starts after that store exists (Small Grant Month 7). It does not reopen Paper A's choice of single-linkage.

**WP4. Discontinuity lemma (Aim 2).** State what changes across a merge, and what is invariant while the cutoff stays inside a gap. The gap condition is shared with WP2. A draft against the toy can start before the season store exists.

**WP5. One re-derived system (Aim 3).** Paper C's generators are the synthetic rehearsal and may be refined in parallel with Paper B. They are not relabelled as this aim's theorem. The observational half waits on a data agreement. Success is stable gaps and a localisable jump after the interaction lengths are re-derived. The failure list in `TOY_MODEL_PAPERS.md` §5.5 is adopted as written.

## What is comfortable to lock

Aim 1's question, and WP1, are comfortable to write down now. Aim 2's question is comfortable. Its season package waits on the Small Grant store. Aim 3's domain stays unlocked on purpose.

No Standard Grant case for support, budget, or JeS text is written from this note.
