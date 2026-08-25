# T1 and T2 in six registers

Reference sheet for the EPSRC Mathematical Sciences Small Grant. Same two theorems, six audiences. Lift text directly; the wording is consistent with `02_Vision_and_Approach_REV2.md`.

## The two canonical lines

Use these verbatim wherever a single sentence is all there is room for.

> **T1 — Competitive dependence does not move the mean; it changes every variance built on it.**
>
> **T2 — A transition can only be located once it exceeds twice the measurement error, and beyond that point the error in locating it is bounded.**

---

## 1. Lay person

**T1 — Averaging is safe. The error bars are not.**
If you average the shape of play over hundreds of matches, do you get one stable answer, or an artefact of which matches you happened to include? T1 proves you get one stable answer — even though everything a team does depends on what just happened. But that same dependence means the usual confidence intervals come out too narrow. T1 supplies the correct ones.

**T2 — You get a timestamp, with a margin.**
When the shape of play changes, we want to say *when* it changed, not merely that it did, and to attach a margin of error to that moment. T2 proves the margin exists and shows what governs it: the size of the change, set against how noisy the tracking is. A small change buried in measurement error cannot be pinned down at all — and T2 says exactly where that line falls.

---

## 2. Sports practitioner

**T1 — You can build a season baseline you can trust.**
Average the topological signature across a season and you get a stable reference for how a team organises, rather than an artefact of the fixtures in your sample. The operational consequence matters more than the theorem: because play is continuous and reactive, off-the-shelf significance tests will overstate your confidence. T1 tells you how much to widen the error bars, so that a "significant" difference between two formations is real rather than an artefact of a long, self-correlated sequence.

**T2 — Alerts arrive with a defensible window, and a floor on what is detectable.**
When the framework flags a change in organisation — a press triggering, a defensive line dropping — T2 attaches a window around that moment rather than a bare flag, so it can be checked against video. It also states the floor: the change has to be around twice your tracking error before it can be located at all. That floor is the guarantee that stops the tool reporting shifts that are really just noise.

---

## 3. Mathematician in topology / statistical TDA

**T1.** On a bounded domain with fixed agent count *N*, diagrams have bounded cardinality and bounded persistence, so landscapes are uniformly bounded in L² — a separable Hilbert space. The Fréchet mean is therefore the Bochner expectation, unique by strict convexity of the squared norm. That is precisely the property that fails for diagram-valued Fréchet means under Wasserstein metrics (Turner et al. 2014), and it is why we work with landscapes rather than diagrams. This much is routine, and we say so rather than dressing it up.

The theorem is the limit law. For a strictly stationary landscape series that is α-mixing with summable coefficients, λ̄ₙ → μ almost surely and √n(λ̄ₙ − μ) ⇒ N(0, Σ_LR) in L², where **Σ_LR = Σ_k Cov(λ₀, λ_k)** rather than Cov(λ₀). This takes Chazal et al. (2014) off i.i.d. sampling, and it is the precondition for FPCA on landscape trajectories.

**T2.** λ is 1-Lipschitz from (Dgm, W_∞) into (L^∞, ‖·‖_∞). On a bounded domain with fixed *N*, the landscape difference is supported on a set of finite measure, giving

> ‖λ(D) − λ(D′)‖_L² ≤ √(N · diam D) · W_∞(D, D′)

— Lipschitz with exponent 1 and explicit constant *C*, the bounded-total-persistence hypothesis for the L^p case supplied by boundedness (Cohen-Steiner et al. 2010). Feeding this into a functional CUSUM in L², calibrated with T1's Σ_LR, gives

> |τ̂ − τ| = O_P( σ² / (Δ − 2Cε)² ),  for Δ > 2Cε,

with Δ = ‖μ₂ − μ₁‖ the jump in the mean landscape and ε = sup_t W_∞(D_t, D̂_t) the worst-case input perturbation. **The identifiability threshold Δ > 2Cε is the substantive content**; the rate itself is standard once the stability constant is explicit.

*Note we state T2 on the landscape series, not on FPCA scores.* The projection onto an estimated eigenbasis is Lipschitz only for a fixed basis, so the score-space version carries an additional eigengap (Davis–Kahan) hypothesis. We make that explicit and check it in O1.

---

## 4. Panel introducer — specialist (statistical TDA, stochastic topology)

**To the room.** "This takes statistical topology off the i.i.d. assumption. Chazal et al. give convergence of landscapes for independent samples; the question here is what survives when the sample is a single adversarially coupled trajectory. The well-posedness half is routine — landscapes sit in L², boundedness gives integrability, uniqueness is strict convexity — and the applicants say so rather than inflating it. The work is in the mixing limit law, and more usefully in identifying the long-run covariance as the object that replaces the marginal one, because that is what makes their bootstrap calibration principled rather than heuristic. T2 chains bottleneck stability into a functional CUSUM to get a localisation rate with an explicit identifiability threshold. Both are twelve-month theorems, and both are stated so that failure is visible."

**Challenge to expect:** *"Isn't T1 trivial?"*
**Answer:** "The existence claim is, and they don't make it — they state it as a precondition and put the weight on the limit law under mixing. The non-trivial content is the long-run covariance appearing in the limit, which is what invalidates the naive inference currently standard in this literature."

**Challenge to expect:** *"Why not multiparameter persistence?"*
**Answer:** "Computationally impractical at these data rates, and they say so. The algebraic setting is Schenck (2022, Chapter 8) and the Botnan–Lesnick survey; the empirically derived interaction lengths are the pragmatic substitute, and O1 gates on whether they transfer."

---

## 5. Panel introducer — adjacent mathematician (probability, statistics, analysis; not TDA)

**To the room.** "Read it as functional data analysis in which the observations are topological summaries rather than curves. Persistence landscapes live in L², so the machinery is familiar: a Hilbert-space law of large numbers and CLT, but for a weakly dependent sequence rather than an i.i.d. one, which puts the long-run covariance in the limit instead of the marginal covariance. That is T1, and it matters because it is exactly what makes a block bootstrap the correct calibration rather than an ad hoc one. T2 is a change-point localisation rate for a functional CUSUM, with the wrinkle that the input is measured with error in the bottleneck metric — so a change must exceed twice the input perturbation before it can be located at all. Both sit in established literatures, which is why twelve months is realistic rather than optimistic."

**Challenge to expect:** *"Is this mathematics or sports analytics?"*
**Answer:** "The deliverables are two theorems and a library. The football data is the falsification platform — it is the only setting where you can obtain a full population of adversarially coupled trajectories with expert labels — and the theorems are stated for bounded competitive systems generally."

**Challenge to expect:** *"Can they really prove two theorems in twelve months?"*
**Answer:** "They are extensions within known frameworks rather than new frameworks, the enabling conditions are gated empirically at Month 9, and R3 declares the fallback if the landscape argument stalls."

---

## 6. Panel introducer — generalist mathematical sciences member

**To the room.** "Two clean, checkable theorems in twelve months, with a data platform large enough to falsify them. The first says that averaging topological summaries over a competitively coupled system is well posed, and identifies the right measure of variability — the point being that standard practice gets the uncertainty wrong. The second bounds the error in locating a structural change, and states an explicit condition below which detection is impossible. Both come with named failure conditions, pre-declared success criteria and a stated fallback. This is squarely within the mathematical sciences remit — the football data is the test platform, not the contribution — and it meets the scheme on all three counts: proof of principle, a genuinely new collaboration across three departments, and structured postdoctoral training."

**Challenge to expect:** *"Is this £100k of mathematics, or £100k of football analytics?"*
**Answer:** "The costed effort is a PI at 0.2 FTE and one Research Associate building the pipeline and running the season. The outputs are theorems, an open-source library and an evidence pack for a Standard Grant. The club supplies data in kind."

**Challenge to expect:** *"What if the theorems don't come out?"*
**Answer:** "O1 gates them at Month 9 on three pre-declared criteria, and R3 names the fallback — Wasserstein diagram comparison, already demonstrated in the pilot — under which the project still delivers the season analysis and the library."

---

## Phrases to retire

| Don't say | Say instead | Why |
|---|---|---|
| "A unique mean path exists" | "The empirical mean path converges" | Existence is trivially true in a Hilbert space; the claim invites "so what?" |
| "Single-threshold persistent homology" | "A single filtration over the full agent set" | PH is multi-scale by construction; the original phrasing reads as a misunderstanding. |
| "The landscape representation is a Hilbert space" | "Landscapes take values in a Hilbert space" | A landscape is an element of L², not a space. |
| "Both theorems are instantiated in software" | "Both results are implemented" | Theorems are proved; methods are implemented. |
| "CUSUM on the FPCA scores" (when stating T2) | "Functional CUSUM on the landscape series" | The score-space version needs an eigengap hypothesis. |
| "In the metric to which landscapes are Lipschitz" | "Lipschitz from bottleneck into L²" | Name the metric pair or a referee will ask. |
| "The framework generalises to other systems" | "…once interaction lengths are re-derived" | Keep the scope boundary attached; it appears in both documents already. |

---

## Where each register belongs

| Register | Use in |
|---|---|
| Lay person | JeS public summary (`01_Summary.md`), club-facing material, press |
| Sports practitioner | SCAFC letter of support, Pathways to Impact, practitioner outputs |
| Topologist / statistical TDA | §5 Methodology, the methods paper [17], reviewer responses |
| Introducer, specialist | Anticipated postal reviewer; §1 Mathematical contribution |
| Introducer, adjacent | §1 and §3 framing; the "why this is mathematics" defence |
| Introducer, generalist | §1 opening, §7 team, and the remit argument throughout |

The three panel registers matter most because introducers present proposals they did not write, often outside their own field, and the room scores what the introducer says rather than what the document contains. Every claim in registers 4–6 should be traceable to a sentence in the case for support — if an introducer has to invent a defence, the wording in §1 is not doing its job.
