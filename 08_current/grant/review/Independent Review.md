I've read the current draft against the 20 Aug review notes (most of those items are now closed), plus the Summary for consistency, and run a density analysis over the prose. Here's what I found.

---

## 1. First, a reframe: sentence *length* isn't your problem

| Section | Sents | Words | Mean len | Max | Semicolons | Colons |
|---|---|---|---|---|---|---|
| §1 Research Problem | 21 | 334 | 15.9 | 32 | 2 | 2 |
| §2 Background | 14 | 228 | 16.3 | **41** | 2 | 2 |
| §3 Impact | 13 | 165 | 12.7 | 21 | 0 | 0 |
| §4 Design & Objectives | 20 | 286 | 14.3 | 31 | 3 | 5 |
| §5 Methodology | 14 | 244 | 17.4 | 29 | 2 | 0 |
| §6 Feasibility & Risk | 7 | 118 | 16.9 | 30 | 2 | 3 |
| §7 Outcomes & Team | 11 | 177 | 16.1 | 33 | 1 | 2 |
| **Whole doc** | **101** | **1,556** | **15.4** | 41 | 12 | 14 |

Only **one** sentence exceeds 35 words. Mean 15.4, median 14 — that's genuinely good prose by the numbers. So your instinct that readability is low is right, but the cause is misdiagnosed.

The real cost is **parsing load per sentence**: citation brackets, `§n` cross-references, parentheticals, semicolons, colons, and numerals. Across 1,556 words you have **26 citation brackets, 13 cross-references, 12 semicolons, 14 colons** — 1.85 "load units" per sentence. A skimmer's eye stops at every one of them. The worst sentences aren't long; they're **stacked**.

The top offenders by load:

1. **§4 success criteria** (load 13) — colon + two semicolons + two parentheticals + five numerals in 30 words
2. **§2 Timeliness** (load 11) — colon + two semicolons + a seven-reference citation carpet `[4,6,8,9,11–14]`
3. **§4 sample size** (load 8) — three parentheticals, five numerals
4. **§6 R1/R2** (load 7 each) — parenthetical rating + colon + semicolon, three times in a row

Notice the pattern: **the four densest sentences are exactly the four things a reviewer skims *for*** — success criteria, timeliness, sample size, risks. You've compressed hardest precisely where compression hurts most.

---

## 2. Mathematical content — six things worth a second look

I think the mathematics is broadly sound, and the sample-size arithmetic now reconciles (1.96 × 0.072/√32 = 0.0249 ✓; d=0.30 at 80% power gives n≈175, so 180 with BH is right ✓). But six items would draw fire from a TDA-literate or stats-literate referee.

**A. "single-threshold persistent homology" (§1, Importance) — highest risk phrase in the document.**
PH is *definitionally* multi-scale; the filtration parameter *is* the scale. A referee who reads "single-threshold persistent homology folds their signatures into one picture" may conclude the author doesn't know what persistence does. Your actual point is different and defensible: *a single filtration over the full agent set* superimposes structure from all organisational levels into one barcode, so features can't be attributed to a level. Suggest:

> "…persistent homology is multi-scale in its filtration parameter, but a single filtration over the full agent set does not separate organisational levels: local-cluster and formation-scale features interleave in one diagram and cannot be attributed to a level [1–3]."

**B. T1 may now read as trivially true.**
The 20 Aug fix (adding the Hilbert clause) closed the uniqueness gap — but it may have overcorrected. In a Hilbert space the Fréchet mean *is* the Bochner expectation, unique by strict convexity of ‖·‖², and existence needs only integrability. Dependence is irrelevant to that. So "a unique mean path exists when observations are dependent, not only when exchangeable" invites the response: *of course it does — you didn't need mixing for that.*

The theorem that is actually non-trivial and actually extends [6] is about the **empirical** mean: consistency (and ideally a rate or functional CLT) for the sample mean landscape path under α-mixing. I'd restate T1 as convergence, not existence. This is the single biggest "so what" risk in the case for support.

**C. Unit of analysis is never stated — and it changes the arithmetic by 2×.**
"180 matches per tactical formation" — but formation is a *team* property. 540 matches = 1,080 team-matches. If the unit is team-match, 180 supports six formation classes; if match, exactly three. Reviewers will ask. Worse: the two teams in a match are *maximally dependent* — they're competing — so counting them as independent units is precisely the error your own §1 says the field makes. Whichever way you go, say so in one clause.

Related: "32 matches per covariate subgroup (phase of play, opponent strength or venue)". 540/32 ≈ 17 implies a fully crossed cell (2 venue × 3 strength × 3 phase = 18 ✓). But phase of play is a *within*-match factor — every match contributes to every phase cell, so "32 matches per cell" doesn't describe it. One clause fixes it.

**D. T2's stability chain has a missing link.**
T2 is stated on landscape-valued series, but §5 applies CUSUM to **FPCA scores**. The chain diagram → landscape is Lipschitz; landscape → FPCA score is only Lipschitz for a *fixed* basis. Perturb the data and you perturb the covariance operator, hence the eigenfunctions (Davis–Kahan), which needs an **eigengap** condition. A functional-data referee will spot this immediately. Either state T2 directly on landscapes, or add the eigengap assumption.

**E. The O1 "moment conditions" gate is circular with T1's own argument.**
T1 says boundedness of the domain secures integrability. If so, why is "moment conditions documented at season scale" an empirical O1 gate — what could fail? I suspect the thing you actually need to check empirically is the **mixing decay**, not the moments. Replacing that criterion with "empirical mixing decay estimated and consistent with the rate assumed by T2" makes the gate non-trivial and ties O1 to O2 much more tightly.

**F. Two success metrics are undefined.**
- "cutoff stability ≥ 0.80" — 0.80 of *what*? Correlation, ICC, proportion of matches within a band?
- "change-points agreeing with held-out annotations at ≥70%" — recall, precision, F1? And within what temporal tolerance (±5 s? ±30 s)? Without a tolerance window the criterion isn't checkable.

**Smaller items:** "The landscape representation *is* a Hilbert space" — landscapes *lie in* one (L²); "the summaries are stable under small measurement error [7]" — [7] is diagram stability, landscape stability is [8], so cite [7,8]; "block bootstrap **across matches**" is checking a *within*-match dependence assumption, which needs a clause; "multiparameter persistence… remains computationally **intractable**" is an overclaim a [4,5] author would contest — "impractical at the frame rates required here" is equally forceful and safer; the Championship is 552 league fixtures (24 × 46 ÷ 2), so tie "≈540" to your pre-registered exclusions (R2) or a reviewer will wonder; §3's "sequential inference on **abstract metric spaces**" sits oddly against T1's whole point that landscapes live in a *Hilbert* space.

---

## 3. Readability — the six rewrites with the highest skim-payoff

**(i) Success criteria (§4) — the worst sentence in the document.**

> Success criteria: cutoff stability ≥ 0.80 (below this, interaction lengths are re-derived); moment conditions documented at season scale; discriminable signatures for ≥3 tactical formations (FDR-corrected differences, p<0.05).

→

> **O1 succeeds if all three hold:**
> - cutoff stability ≥ 0.80 across the validation batch (below this, interaction lengths are re-derived);
> - empirical mixing decay consistent with the rate T2 assumes;
> - signatures distinguishing ≥3 tactical formations (p<0.05, BH-corrected).

**(ii) Timeliness (§2) — your only 41-word sentence, and a seven-reference carpet.**

> **Timeliness.** Three developments have converged. Multi-scale topology and statistical comparison tools have matured [4,6,8,9]. Scalable computation now supports rigorous analysis at population scale. Fully labelled competitive tracking data have become available at that same scale. No statistical-topology treatment of competitive collective systems yet combines all three.

Three sentences, one citation cluster, no punctuation stack. Move [11–14] to where those applications are actually discussed.

**(iii) T1/T2 — give each a plain-English headline.**
This is the highest-value change in the document. A skimmer currently has to parse two dense technical sentences to learn what you're proving. Give them the claim in ten words first:

> **(T1) Averaging is well posed under competitive dependence.** The empirical mean path of landscape-valued summaries converges to a unique population mean under temporal mixing, not only under exchangeability [6]. Landscapes take values in a Hilbert space [8], where the mean is the Bochner expectation; a bounded domain supplies the integrability.
>
> **(T2) Transitions can be located with a proven error bound.** We prove a Wasserstein-stability result for a sequential (CUSUM) change-point statistic on landscape-valued series. The bound holds under temporal weak dependence and a bounded domain, and yields the calibrated detection thresholds of §5.

Note the T2 rewrite also dissolves the cryptic "The calibrated thresholds are that bound in operational form" later in §5 — elegant, but on a skim it lands as a riddle.

**(iv) §2's opening sentence is a tautology.**

> Topological methods have shown that spatial organisation in multi-agent systems carries structure.

"Organisation carries structure" says nothing. The Background section's first sentence is prime real estate. Try: *"Topological methods can already detect and quantify spatial organisation in multi-agent systems — but only where that organisation is cooperative or slowly evolving."* That opener sets up your gap in the same breath.

**(v) §1's opening buries the ask until sentence five.**
Sentences 1–4 are definition and negative space; the reader doesn't learn what you'll *do* until "This grant delivers a proof-of-principle." Consider leading with the claim and following with the definition. Reviewers assign a verdict in the first 30 seconds.

**(vi) Risks (§6) — a run-in list where a display list belongs.**
Three risks, each with a parenthetical rating, a colon, and a semicolon, all in flowing prose. Risk registers are the single most-skimmed element of a feasibility section. Break R1/R2/R3 onto their own lines. Costs you three line-breaks; buys you the one thing panels actually look up.

---

## 4. Structural and skim-layer issues

- **Zero bullets in 1,556 words.** Unbroken prose with 26 bracketed citations is punishing to skim. Three display lists (success criteria, timeliness, risks) would change the document's feel more than any sentence-level edit.
- **Heading hierarchy is flat and broken.** `## Vision` and `## Approach` are H2, but so are `## 1. Research Problem`, `## 4. Research Design`… — so the two top-level parts are siblings of their own children. Push the numbered sections to H3, or the visual hierarchy collapses on render.
- **FPCA is never expanded.** "applying FPCA [18]" — first use, no gloss, on a panel that will include non-FDA mathematicians. Same for **OSF** in the Figure 1 legend, which appears nowhere in the text.
- **Figure 1's legend is opaque to a cold reader.** "[17] (M2)" as an output label means nothing without hunting the reference list — write "methods paper [17]". Also: [17] is already *submitted*, so listing it as an M2 output invites "why is a submitted paper a project deliverable?" — say "acceptance of [17]".
- **13 cross-references is a lot** for 1,556 words. Some are load-bearing (§4 cutoff gate ← §5 failure trigger). Some are decorative: "Production processing runs at 1 Hz (§7)" points at the resources section, which doesn't justify the rate. Pruning four or five would lighten the whole document.
- **Terminology drift in the grouping vocabulary.** You now use "covariate subgroup", "tactical formation", "competitive organisational states", "organisational-state distinctions". The 20 Aug review flagged this and it's *better*, but "organisational state" vs "tactical formation" still reads as possibly-the-same, possibly-not. One sentence defining the relation, or collapse to one term.
- **"Competitive" appears ~20 times in eight different noun phrases** — competitive collective systems / domains / data rates / organisational states / bounded competitive system / competitive-systems methodology / continuous competitive interaction. Keyword discipline is good; mutating the phrase each time is not. Fix on two or three canonical forms.
- **Football appears nowhere in §1.** You say "benchmark system" with no referent. Holding the abstraction for a maths panel is a defensible strategic choice — but "benchmark system" as an unresolved noun is worse than naming it once: *"validates them at scale on a benchmark competitive system (professional football, §2)."* Worth a decision either way rather than drift.

---

## My ranking, if you only do five things

1. Fix **"single-threshold persistent homology"** (§1) — reputational risk with a TDA referee.
2. Restate **T1 as convergence, not existence** — otherwise your headline theorem may read as trivial.
3. **Headline sentences for T1/T2**, plain English first.
4. **Three display lists**: success criteria, timeliness, risks.
5. **State the unit of analysis** (match vs team-match) in the sample-size paragraph.

Want me to produce a marked-up revision of `02_Vision_and_Approach.md` with these applied — tracked as a diff against the current text so you can accept or reject each one? I'd also suggest we sanity-check the T1 restatement against the T2 Monte Carlo validation doc in the project before committing to the convergence framing, since that's the claim the evidence has to support.

**Sources:** [claude/Review_Notes_2026-08-20.md](project://claude/Review_Notes_2026-08-20.md), [claude/01_Summary.md](project://claude/01_Summary.md)