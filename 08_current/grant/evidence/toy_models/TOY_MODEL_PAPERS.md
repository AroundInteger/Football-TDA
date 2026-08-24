# Toy model, Papers A/B, and Standard Grant transfer

Associated with `adversarial_tda.m`, `atda_core.py`, and `AdversarialTDA_Specification.md`.  
August 2026. UK English. Markdown is the source of truth.

This note does two jobs: (i) maps the toy figures onto the locked claims of Paper A (JACT) and Paper B (JSS); (ii) assesses the claim that the toy is mathematically honest, and records how it should be **tested and extended on other competitive systems** to underpin the follow-on Standard Grant. Paper C is the synthetic methods manuscript (ecology lead, robotics second); it is **not** a third football paper and is developed **after A and B are submitted**. Home: `08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/`.

**Rule.** The toy explains *mechanisms under known ground truth*. It does not reproduce SkillCorner numbers. Do not copy 12.66, 76.13, or $\hat T=54$ into `results.tex` of either paper.

---

## 1. What Papers A, B, and C actually claim

From `working_foundations.md` (locked claims).

**Paper A (JACT).** Multi-scale persistent homology for competitive point clouds: domain-informed hierarchical clustering, then an adaptive Vietoris–Rips filtration. Ten professional matches: three stable $H_0$ regimes and two $H_1$ regimes (individual, tactical) that are complementary, not redundant; every $H_1$ generator is a geometric cycle; a minimal event correlation is construct validity only. Football is the testbed; the framework is intended to transfer.

**Paper B (JSS).** What those measures add for football analysis. Persistence tracks events (pressing/engagements/breaks down; build-up up). Tactical persistence is not redundant with width or convex-hull area. Home and away tactical structures are nearly independent at frame resolution. That extra variance does not yet improve held-out phase-of-play prediction.

**Paper C (methods).** Diagram analogue of Fréchet mean and CUSUM on synthetic adversarial clouds. Ecology lead, robotics second. After A and B submit.

Paper B is intentionally absent from the EPSRC V&A. Paper C is not a JeS deliverable that quotes ecology $\hat T$ as landscape T2.

---

## 2. Mapping: toy figures → Paper A

Paper A’s method is **cluster-then-adaptive-PH** on 22-player clouds. The toy computes PH on the raw 12-agent cloud. Display scales $\delta\in\{5,40,66\}$ are not the clustering cutoffs 2.98 / 12.0 / 30.0 m.

| Paper A finding | Toy figure | What it explains | What it does not explain |
|-----------------|------------|------------------|--------------------------|
| Scale conflation: one filtration on the undecomposed cloud mixes organisational levels | **Fig 6** | At $\delta=35$, A_WIDE and A_LINE both have $(\beta_0,\beta_1)=(2,0)$, yet $W_1=42$. Same Betti numbers, different hierarchy | Empirical cutoffs; silhouette vs information-content disagreement |
| Three $H_0$ regimes (individual $\sim 19$, tactical $\sim 5$, team $\sim 1$–$2$) | **Fig 1** | Same 12 agents at three $\delta$ give $\beta_0=4\to 2\to 1$ (8 local / 2 tactical / 1 global deaths) | The means 19.05 / 4.92 / 1.38 |
| Two $H_1$ regimes; team-scale $H_1=0$ a priori | **Figs 9–10** | Encirclement $H_1$ born $\approx 27$, dies at 40. A_WIDE’s rectangular hole born $\approx 60$ is a different object | Remark (team-null): $H_1$ vanishes because clustering leaves $k\le 2$ centroids. The toy never reduces to 1–2 points |
| Complementarity $\rho=0.264$: scales are not the same structure at two resolutions | **Fig 2** | Adversarial coupling is scale-specific | Spearman / Fisher / 1,500-frame co-occurrence |
| Every $H_1$ generator is a geometric cycle | **Fig 9** | The green loop is the B-ring; a trapped A cluster kills the bar | Cycle lengths 3–6 vs 4–5 on real centroids |
| Adaptive filtration; cutoff robustness 6–14 m | — | — | The toy does not cluster, so $\varepsilon_{\max}$ never has to adapt |

**Strongest Paper A use.** Fig 6 is the scale-conflation paragraph made visual. Optional schematic in Methods or Discussion, labelled synthetic.

---

## 3. Mapping: toy figures → Paper B

Paper B’s three locked loop types: (1) peripheral possession ring, (2) rest-defence arc, (3) pressing encirclement (trigger then close).

| Paper B finding | Toy figure | What it explains | What it does not explain |
|-----------------|------------|------------------|--------------------------|
| Pressing / engagements → persistence down; build-up → up | **Figs 9–10** | Predator ring present ($H_1=12.76$) while hunting; trapped cluster fills the hole ($H_1=0$); prey spread has no encirclement $H_1$ | SkillCorner labels, $\pm$window tests, 104,722 pairs. Direction only |
| Pressing encirclement (concept 3) | **Fig 9 A–B** | Ring closed, interior empty → $H_1$ lives; opponent trapped → $H_1$ dies | 3–4 player Gegenpress distances in metres |
| Peripheral possession ring / rest-defence (concepts 1–2) | **Fig 10** | Empty midfield ring while the other team spreads: a dead zone inside a loop | 3-2-5 / 2-3-5 rest-defence geometry |
| Home/away independence (lag-0 $\rho\approx 0.04$) | **Fig 7**, as a *contrast* | Coin-flip column is what Paper B measured at match-average. Tug-of-war column is the coupling Paper B says might appear only in a press or a possession spell | Why ten real matches average to independence. The toy imposes coupling |
| Not redundant with width / hull (partial $R^2$ hull $=0.09$) | **Fig 6** | Two shapes of similar spatial extent, $W_1=42$. Persistence can move when length/width barely do | The partial-$R^2$ table |
| Predictive null ($\Delta$AUC $\approx 0$) | — | — | A 12-agent cartoon cannot speak to held-out classification |

**Strongest Paper B use.** Fig 9 as the schematic for encirclement then collapse. Fig 7 as the picture of the independence baseline and of context-dependent coupling left open in the Discussion.

---

## 4. Assessment of the “honest mathematics / third paper” claim

The quoted assessment is largely right about the *objects*, and too strong about *what has been proved* and about Figure 5.

### 4.1 Where it is right

| Claim | Verdict |
|-------|---------|
| Ultrametric hierarchy is a genuine Carlsson–Mémoli object; dendrogram correspondence is exact | **Yes**, for $H_0$ of a finite metric space: MST edge weights are the Vietoris–Rips $H_0$ deaths. The 8–2–1 gap pattern is exact for *this* point cloud |
| $H_0$ via MST is the real statistic, not a cartoon | **Yes** |
| Wasserstein distances satisfy the stability theorem | **Yes** in the sense that we compute exact $W_p$ (optimal transport, diagonal matching). Cohen–Steiner applies. The toy uses the theorem; it does not prove it |
| CUSUM is Page (1954) | **Yes**. Thresholds are Monte Carlo calibrated (5% false-alarm), not an ad hoc indicator. $N=1000$ per jump size: $\mathbb{E}|\hat T-T^*|$ falls as the $W_1$ jump grows |
| “Toy” refers to the synthetic setting, not to fake mathematics | **Yes**, for the objects listed above, with the qualifications in §4.2 |

A controlled hierarchical adversarial point process with known ground truth is a standard computational-topology workflow. Fig 6 is already close to a worked example for a lemma: Betti numbers at a single scale do not determine the persistence diagram. Fig 7 reports real lag-1 autocorrelation of a designed AR(1) mixing process, not shuffled noise.

### 4.2 Where it needs to be qualified

**Fréchet mean.** The assessment says the coordinatewise mean of sorted deaths is “exact for $H_0$ diagrams on the birth $=0$ line.” That is exact for the **$W_2$** Fréchet functional (Turner et al.), under equal cardinality and when the optimal matching does not use the diagonal. It is **not** the minimiser of $\mathbb{E}[W_1(D_i,\mu)^2]$. Independent Python checks put a large gap on an adversarial four-diagram example and a few per cent in the low-noise sliding window. Spec §2.5 already records this. Do not repeat the older “exact under $W_1$” wording.

**T1 / T2 vs the V&A.** The Small Grant theorems are **landscape-valued**. The toy is the **diagram $W_1/W_2$ analogue**, which is also the stated R3 fallback. Honest objects, different statistic from the grant statements. That is a framing distinction, not a fake CUSUM.

**Paper A’s contribution is absent.** Clustering-then-adaptive-filtration is the JACT method. The toy never clusters. Honesty about $H_0$/$W_p$/CUSUM does not make the toy a miniature Paper A.

**Historical order.** The suggested sentence “we demonstrate first on a controlled process, then on observational football” is the right *methodological* order for a future paper. It is not the actual research sequence: Papers A/B on SkillCorner came first; the toy was built later for the grant. Do not write the grant or a methods paper as if the toy preceded the 10-match study.

### 4.3 Figure 5 is the overclaim

> “The mathematical structure is identical across all four domains not because you designed them to look similar, but because hierarchical competitive organisation in a bounded domain genuinely produces the same topological signature.”

The second clause does not hold of the present figure. Football, tumour–immune, predator–prey, and fleet panels all use the same `tri_cluster` template (four triples). The barcodes match **because the geometry was copied**, then painted onto different backgrounds. Carlsson–Mémoli says: a finite metric space determines an ultrametric dendrogram via $H_0$. It does **not** say that every bounded competitive system is a three-level ultrametric hierarchy.

The true statements are:

1. **Lemma-shaped (already true).** If a point cloud is a $k$-level ultrametric hierarchy with given gap scales, its $H_0$ barcode has the corresponding gap pattern. Fig 1 is the football instance; Fig 5 repeats the instance in three other embeddings.
2. **Empirical prediction (not yet tested).** Once interaction lengths are re-derived (O1 stability gate), tumour–immune / ecology / fleets will show an analogous multi-gap $H_0$ barcode. That is a Standard Grant hypothesis. Fig 5 illustrates the hypothesis; it does not confirm it.

Calling Fig 5 “theorem-level, not an analogy” would not survive a methods referee.

### 4.4 What *is* theorem-level adjacent

| Object | Status |
|--------|--------|
| MST $\leftrightarrow$ VR $H_0$ | Theorem (Carlsson–Mémoli), used exactly |
| $W_p$ stability | Theorem (Cohen–Steiner; Skraba–Turner), used exactly |
| Single-scale Betti numbers do not determine the diagram | Lemma-shaped; Fig 6 is a concrete witness ($W_1=42$ at equal $(\beta_0,\beta_1)$) |
| $H_1$ from embedding geometry, not from hierarchy | MacPherson–Schweinhart / Schindler–Barahona; Fig 9 is a witness (ring vs trapped fill) |
| Same 8–2–1 barcode in four painted domains | Schematic of a transfer *hypothesis*, not a theorem |
| Landscape T1/T2 | Grant theorems; not what the toy computes |

---

## 5. Extending the toy to other competitive systems (Standard Grant)

The Small Grant V&A is explicit: this award delivers football-validated theory and software; **transfer to another system is a later step**, once interaction lengths are re-derived. The follow-on Standard Grant tests whether T1/T2 transfer to spatial predator–prey dynamics, including tumour–immune competition (Co-I Powathil).

The toy’s job in that story is not a third JACT/JSS paper. It is a **controlled transfer testbed**: change the generative system, keep the same honest statistics ($H_0$ MST, exact $W_p$, $W_2$ Fréchet, Page CUSUM, encirclement $H_1$), and ask what survives.

### 5.1 What Fig 5 is not

Fig 5 copies the football four-triple template onto a pink disc, a tan rectangle, and a blue corridor. Identical 8–2–1 barcodes are guaranteed by construction. That is a schematic of a transfer *hypothesis*, useful in a slide, not a transfer *test*.

A test changes at least one of: number of agents, number of hierarchy levels, domain shape, interaction kernel (press vs consume vs intercept), or the switching rule $b(t)$. If the barcode still has a multi-gap $H_0$ structure *after* scales are re-derived from the new geometry, that is evidence. If it does not, that is also evidence: it tells the Standard Grant where O1’s stability gate must do real work.

### 5.2 What “re-derive interaction lengths” means in the toy

In football, Paper A’s cutoffs are 2.98 / 12.0 / 30.0 m from a sweep plus domain judgement. In the toy they are display $\delta$ chosen to sit between known deaths (4.03, 32.56, 60).

For a non-football cloud the analogue of O1 is:

1. Build the new generative geometry (do not paste `A_WIDE`).
2. Compute the $H_0$ death vector (noise-free).
3. Identify gap scales from the sorted deaths (or from a cutoff sweep on noisy realisations, matching Paper A’s method more closely).
4. Only then choose display $\delta$ and run W1 / Fréchet / CUSUM / $H_1$.

The prediction worth writing into a Standard Grant is: **the workflow transfers, not the metre values.** A tumour–immune toy whose local/tactical/global deaths sit at 8 / 25 / 50 still supports T1/T2 analogues if the gaps are stable and the jump is localisable.

### 5.3 Domain order (aligned with the V&A)

The methods note (`paper_C_methods/` in the three-paper paradigm) inverts the *publication* order relative to the V&A's named follow-on: **ecology first (synthetic)**, robotics second, oncology Outlook only. That is for panel confidence (complementary fields on one object) and because Vipond (2021) plus the 2025 synthetic vineyard paper make a general “TDA of tumour–immune” paper crowded. The Standard Grant observational order can still put tumour–immune (Powathil) first once serial imaging is in hand. **Paper C is developed after Papers A and B are submitted.**

| Priority | System | Status (August 2026) |
|----------|--------|----------------------|
| 1 | Ecological predator–prey (synthetic) | **Paper C lead.** Territory $240\times 180$, $N=15$ vs $12$, re-derived deaths (local $\approx 7$, herded $\approx 17$–$20$, dispersed merge $\approx 87$). Not `A_WIDE`. See `08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/numbers.json`. |
| 2 | Autonomous pursuit–evasion (synthetic) | **Methods note second.** Corridor $180\times 50$, pair geometry $N=8$ vs $6$. |
| 3 | Tumour–immune (observational) | Outlook only in the methods note; Standard Grant with Powathil. Position against Vipond (2021) and the 2025 zigzag/vineyard paper. |
| — | Movebank / dual-species GPS | Standard Grant with the existing biologging group (Gunner, Wilson, Lurgi, Börger, Shepard, Redcliffe). Gunner et al. (2026) is steps/turns, not this paper’s clouds. |

Do not add armed conflict (Small Grant ethics constraint carries). Finance, outbreak line-lists, and platform moderation are out of Paper C (see `paper_C_methods/literature_grounding.md`).

### 5.4 Concrete extensions that would actually test transfer

These are the next toy-model developments that earn a place in a Standard Grant evidence pack. None of them requires SkillCorner.

1. **Re-derived gaps (minimum).** **Done for ecology and robotics** in Paper C (`paper_C_methods/`). Ecology prey $W_1(\mathrm{dispersed},\mathrm{herded})=212$; CUSUM $N=200$, mean $\lvert\hat T-T^*\rvert=4.1$ at the full jump, power $100\%$. A tumour–immune generator with a third geometry remains Standard Grant.
2. **Role reversal, not just possession paint.** Fig 10 already inverts predator/prey with $b(t)$. The Standard Grant version is topology-conditional $\lambda(X,b)=\lambda_0+\lambda_1 f(\varphi(X))$ (Chat 2): encirclement $H_1$ raises the chance of a switch (kill / loss of possession). That is the feedback loop GTPPF would prove.
3. **Hierarchy depth as a stress test.** Football’s three levels are an empirical finding. A two-level immune infiltrate, or a four-level ecological guild, asks whether T1/T2 need a fixed number of scales or only *some* multi-gap structure. Fig 6 is the witness that a missing level is invisible at one $\delta$.
4. **Unequal cardinality.** Red card / cell death: $N$ changes. Exact $W_p$ already allows this; the football toy never uses it. A tumour-shrink generator is the natural first use.
5. **Domain shape.** Pitch vs disc vs corridor. Diameter still discharges T1 integrability; the constant changes. Worth one figure so a referee cannot say the bound is an artefact of 120×80.
6. **Mean-field sketch (later).** Replace $N=12$ with a density $\mu(x,t)$ and a Fokker–Planck structure. That is Standard Grant theory, not a Small Grant deliverable. The $N$-agent toy is the finite-$N$ check.

### 5.5 What would count as failure (useful for the Standard Grant)

- After re-deriving $\delta$, the new system has **no stable gaps** (deaths fill $[0,D]$ uniformly). Then multi-scale decomposition is football-specific and O1’s gate is the whole story.
- Encirclement $H_1$ **does not appear** for biologically natural rings (too sparse, or the prey sits on the ring). Then Fig 9 does not transfer; MacPherson–Schweinhart still holds, but not as a tumour biomarker cartoon.
- CUSUM **does not localise** a programmed switch once noise is on the scale of the gap. Then T2’s analogue needs a larger jump or a landscape statistic — exactly the R3 discussion.
- Home/away-style **independence** (Paper B) appears even when the generator is coupled. Then Fig 7’s tug-of-war is too strong a model of real competition.

Failure here is not a problem for the Small Grant. It is design information for the Standard Grant.

### 5.6 Honest sentences for the evidence pack

> The Small Grant validates T1/T2 on football. A methods note on controlled hierarchical point processes (ecology-led generator, robotics second) asks which diagram-level guarantees survive a change of domain, agent number, and interaction kernel, before observational tumour–immune or ecological data are attempted. The biologging group is already a collaborator; oncology remains the named health pathway.

Not: “Fig 5 shows the same topology in four domains.”

Not: “We demonstrated the method first on the toy, then on football.” (Historical order is the reverse.)

Not: Gunner et al. (2026) as this methods note’s dataset (individual steps/turns, not two competing clouds).

### 5.7 Methods note vs observational pack

Locked: simulation only in this manuscript; **Paper C is written after A and B submit.** Panel evidence of complementary fields. Contribution split: Tier 1 cite, Tier 2 T1-lite/T2-lite (`paper_C_methods/lemmas.md`), Tier 3 conjecture under tug-of-war. T2-lite is on $W_1(D_t,D_{\mathrm{ref}})$, not consecutive-frame $W_1$. Draft and figures: `08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/`. Still open: whether Wilson / Börger / Lurgi join the author line. Month-12 observational pack: simultaneous pack/herd GPS; serial MIBI is not claimed done. Movebank is **not** Domain 1 of this note.

---

## 6. Practical use now

- **Talks / Co-I briefing.** Pair Fig 6 with Paper A’s scale-conflation intro; pair Fig 9 with Paper B’s three loop types.
- **Optional schematic in A or B.** Fig 6 in A, Fig 9 in B, captions: “synthetic, known ground truth.”
- **Reviewer replies.** “Why not convex hull?” → Fig 6. “Is $H_1$ just a pretty ring?” → Fig 9 trapped vs escaped. “Do the two teams move together?” → Fig 7 vs Paper B’s near-zero $\rho$.
- **Small Grant text.** Do not import toy numbers. If a sentence is needed: synthetic diagram-$W_1$ CUSUM recovers a known jump; T1/T2 remain landscape-valued.
- **Standard Grant pack (Month 12).** The ecology/robotics generators with re-derived gaps (Paper C) show the *workflow* transfers. Fig 5 as currently drawn is not that evidence. Observational Movebank/MIBI remains the follow-on.

---

## 7. Files

| File | Role |
|------|------|
| `AdversarialTDA_Specification.md` | Mathematical spec (source of truth) |
| `adversarial_tda.m` | Figures 1–9 |
| `atda_core.py` / `verify_atda.py` | Independent numerics |
| `gtppf_switching.py` | Figure 10 (possession / role reversal preview) |
| `../../Paper Updated/3-Paper Paradigm/paper_C_methods/` | Paper C: ecology-led methods note (after A and B submit) |
| This file | Mapping to Papers A/B; Standard Grant transfer plan for the toy |
