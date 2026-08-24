# Response to the First Review: Why the Current V&A Is Mathematics-Led

This note is for Paul. It does not reopen the six problems he identified. Those problems were real, and the current Vision & Approach (`VA_140826.md`) still honours the *principles* of that review. What has changed is the *form* in which they are met.

The bid is submitted to **EPSRC Mathematical Sciences**. A mathematics panel scores Quality first. The leading constraint on the three-page V&A is therefore: **the Vision must be readable as a mathematics proposal on a first pass**. Everything else — including how, and where, the football pilot is evidenced — is subordinate to that.

---

## The governing choice

Paul’s V3 rewrite put the football validation numbers in the Vision (stability 0.96 / 0.84 / 1.00; H₁ presence 95.3% and 12.7%; Spearman ρ = 0.264; 104,722 event–topology pairs). That was the right correction *for that draft*: the first version had asserted novelty without evidence.

Those numbers are football measurements. Once they occupy the Vision, three things follow whether we intend them or not:

1. **The skim hinge becomes a sports result.** A panellist who reads only §1–§2 learns cutoffs in metres, loop-presence percentages and a correlation from ten Championship matches before they learn the theorem targets. That is a football-led document with a mathematical appendix, not a mathematical proposal with a validated testbed.
2. **The object of study collapses to the dataset.** 2.98 m / 12.0 m / 30.0 m, 143/150 frames, and event-pair counts are properties of this tracking feed. The mathematical object is a class: bounded competitive systems with non-exchangeable, multi-scale observations. Putting the dataset statistics in the Vision invites the panel to score a sports-analytics project.
3. **Page budget then defends the wrong claim.** Three pages cannot carry both a theorem-level contribution and a results table. Every metre, percentage and ρ we restore to §1–§2 is a sentence we cannot spend on well-posedness, Wasserstein stability, or why exchangeability fails. The numbers do not *support* the mathematics case; they *displace* it.

The current structure therefore does the following, by design:

- **Vision (§1–§6)** states the mathematical problem, the two theorem-level contributions, and the gap in existing statistical topology. Football appears as the experimental platform, not as the result.
- **Background (§2)** records that a 10-match pilot recovered three stable connected-component regimes and two complementary loop regimes, with scales carrying largely independent information, and **points to the methodology paper [17]** for the statistics. The validation claim is present; the sports-science table is not.
- **Approach (§7)** keeps the numbers that a workplan actually needs: season size (≈540), stratum sizes (32; 180), power, the borderline pilot effect (p = 0.051), the Month-2 stability gate (0.80), and the computational budget. Those figures justify *design*, not *domain identity*.

This is not a retreat from evidence. It is a decision about **which page of a mathematics proposal is allowed to look like a results section**.

---

## What we kept from the first review

| Paul’s problem | Principle we kept | How it now appears |
|---|---|---|
| 1. Novelty vague; “firstness” undefended | Name the contribution; do not claim priority | §1 **Mathematical contribution**: (i) unique Fréchet mean trajectories under dependent competitive dynamics, extending [6]; (ii) Wasserstein-stability bounds for landscape-valued CUSUM. “First / first tools / pioneering” remain out. |
| 1. No evidence | Evidence must exist and be findable | §2 cites the 10-match pilot and [17]. §7 and §9 use the pilot to fix parameter ranges and power. The numbers live in the paper the panel can read, not in the Vision skim. |
| 2. Pathway / scope creep | Four objectives; Standard Grant is not this grant | O1–O4 with month ranges. O4 (Months 9–12) is evidence synthesis for a **follow-on** Standard Grant. O1–O3 remain standalone publishable contributions. Broader domains (autonomous coordination, biological competition, tumour–immune with Powathil) are pathways, not deliverables. |
| 3. Drone/crowd vignette; no research goal | Open with the science, not a scenario | §1 opens by defining the system class and stating that the project will establish the missing statistical-topological framework. No drones, crowds, or disaster-zone vignette. |
| 4. Timeliness as library availability | Timeliness must be mathematical | §4 leads with maturity of multi-scale topology and statistical comparison [4,6,8,9], and with the specific gap: no validated workflow for continuous competitive interaction. Ripser, GUDHI and giotto-tda appear only in §8 (Methodology), as enabling computation. |
| 5. Team buried | FTE and roles up front in Approach | §7 opens with PI 0.2 FTE, Co-Is 0.25 FTE combined, RA Months 2–10, and the data partners. |
| 6. Self-congratulatory tone | Factual delivery, not adjectives | “Optimal”, “pioneering”, “strong track record”, and fabricated impact percentages remain out. The team’s delivery is the 10-match methodology paper [17]. |

The first review asked us to stop sounding like an ungrounded sports pitch. We agree. The current draft stops sounding like a sports pitch *and* stops *looking* like one.

---

## What we deliberately did not restore — and why

### Football in paragraph 1

Paul asked the V3 draft to name football as testbed in the first paragraph, to kill the drone/crowd opening. That diagnosis was correct. The prescription that replaced it (“this research develops… professional football provides an ideal testbed”) was right for V3.

A later constraint is stricter. **If football is named before the theorems, the panel classifies the bid before it has seen the mathematics.** The current §1 therefore does three beats in order: (i) define competitive collective systems; (ii) name the two mathematical obstacles (multi-scale structure; non-exchangeable observations); (iii) state the two theorem-level results. Football enters in the Quality paragraph as the “fully observed, spatially bounded, population-scale experimental platform”, and again in §4 Opportunity. That is testbed language. It is not identity language.

Putting football in sentence 1 would undo the classification we now need: Mathematical Sciences, football as instrument.

### The validation dump in Vision

Restoring 0.96 / 0.84 / 1.00, 95.3% (143/150), 12.7% (19/150), ρ = 0.264 and 104,722 pairs to §1 or §2 would:

- force the reader through a sports-science results block before O3 is even named;
- make the Vision numerically denser than the theorems;
- re-open a known internal reconciliation (frame counts and cutoff values in the paper versus `numbers.json`) *inside the grant text*, which the current draft correctly avoids;
- spend the only three pages on quantities that [17] already reports.

The panel does not need those figures to believe the pilot exists. It needs to believe that the pilot **fixes the conditions under which the theorems are stated**. §9 now says that directly: the pilot has already fixed the parameter ranges, so the twelve months are spent proving, not deciding what to prove. That is the feasibility sentence a mathematics panel is scoring. A table of H₁ presence rates is not.

### Timeliness as three named football methods

Paul’s V3 Timeliness listed landscape dynamics, tactical fingerprinting, and empirical distributions. Those are real, and they now sit where they belong: as **O1–O3**, with O3 as the principal theoretical advance. Leading Timeliness with them again would present the grant as a methods-for-football programme. Current §4 instead answers the panel question *why now mathematically*: the tools have matured; the exchangeability gap has not; high-frequency competitive data now exist; football is the platform on which the theory can be tested at population scale.

### “Separate Standard Grant” as a slogan

The boundary is kept (O4 is synthesis; O1–O3 standalone; follow-on, not in-grant translation). We do not spend Vision words on the administrative claim “this is a separate project”. The panel will read that as nervousness about scope. The workplan already shows it.

---

## Where the numbers actually are

Nothing has been discarded. The lock-file remains `CANONICAL_NUMBERS.md`. The methodology paper [17] is the public record. The V&A uses numbers only where they change a design decision:

| Number | Role in current V&A | Section |
|---|---|---|
| 10 matches; three / two regimes; independent scales | Existence of a validated pilot | §2, cited to [17] |
| ≈540; 32; 180; p = 0.051 | Sample-size and power | §7 |
| Stability gate 0.80 | Falsifiable cutoff risk | §7 O1, §9 |
| ≥70%; permutation p < 0.05 | O3 success criterion | §7 |
| 1,600 / 5,000 CPU-hours | Computational feasibility | §12 |

That split is intentional: **Vision cites the paper; Approach cites the design.**

---

## Publication line (unchanged in substance)

- [17] methodology → *Journal of Applied and Computational Topology* (Months 1–2)
- Full-season results + landscapes → Month 11 (primary 12-month output)
- [22] football-analytics companion → *Journal of Sports Sciences* (practitioner interpretation; not the mathematical centre of mass)

The ethics-pending conflict paper remains out of JeS. Transfer language is generic and post-grant (autonomous coordination, biological competition, tumour–immune with Co-I Powathil). Related Swansea awards in adjacent computational fields (for example robotic-swimmer optimisation) are not cited: they are not this mathematics, and listing them would invite an overlap question the V&A should not open.

---

## What we are asking Paul to accept

The first review stopped us from writing an ungrounded, self-congratulatory, vignette-led sports bid. That correction stands.

The current draft answers a further question that V3 had not yet faced: **will a Mathematical Sciences panel, on a first pass, think this is a mathematics grant?**

If the Vision leads with football statistics, the honest answer is no. If it leads with the system class, the exchangeability failure, and two named theorems, with the pilot cited rather than tabulated, the answer is yes.

We therefore ask Paul to treat the V3 number-dump and the “football in paragraph 1” instruction as **corrective for that draft**, not as standing constraints on a mathematics-led three-pager. The evidence is in [17] and in the Approach. The Vision is for the theorems.
