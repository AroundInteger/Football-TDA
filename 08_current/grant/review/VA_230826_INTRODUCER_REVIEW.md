# Vision & Approach — three-introducer review

**Date:** 23 August 2026  
**Text reviewed:** `02_Vision_and_Approach.md` (cut-and-pass + Gantt + readability pass + this residual pass)  
**Scheme:** EPSRC Mathematical Sciences Small Grant (≤ £100k fEC; ≤ 12 months)  
**Figure:** timeline-only `grant_figure_gantt.png` (16 cm × 5.2 cm), pasted at full JeS text width

This note is the panel-read of the working V&A. It is not submitted to JeS. Edit the V&A in `02_Vision_and_Approach.md`; keep this file in step when an introducer probe changes the text.

---

## How the three introducers use the text

On an EPSRC Mathematical Sciences Small Grant panel:

| Role | Typical seat | Job |
|---|---|---|
| **Introducer 1 (lead)** | Nearest field: statistical topology / TDA | Presents the case; must be able to defend T1 and T2 |
| **Introducer 2** | Adjacent: statistics, stochastic geometry, sequential inference | Tests whether the design and the guarantees are honest |
| **Introducer 3** | General mathematical sciences | Decides scheme fit and remit: maths that uses football, not sport science with topology attached |

General members then rank from that discussion. Scheme tests: **original research in the mathematical sciences remit**; **proof-of-principle**; **new collaboration**; **postdoctoral career development**; **£100k / 12 months**; not purely networking or travel; no equipment over £25k.

**PI pitch order at the meeting:** system class → T1/T2 → proof-of-principle → football as the bounded testbed → new collaboration and RA post. Do not open with formations or club outputs.

---

## Scheme scorecard

| Test | Verdict | Where found |
|---|---|---|
| Original research in mathematical sciences | Pass. T1/T2 are theorem-level, not a software port of [6,8] | §1 |
| Proof-of-principle | Pass. Named in the opening; season-scale validation of the theorems | §1, §4–§5 |
| New collaboration | Pass. Topology + oncology + sport science + SCAFC, not previously combined | §7; Powathil’s in-grant role is O2 well-posedness |
| RA career development | Pass. Training is a standalone sentence | §4 |
| Not networking / travel | Pass | Approach |
| Scale (£100k, 12 months, no kit >£25k) | Pass, consistent with `06_Resources_and_Costs.md` | §4, §7, Figure 1 |
| Football as testbed, not destination | Pass. Transfer is the Standard Grant; interaction lengths re-derived | §1, §2, §3 |

---

## Introducer 1 — statistical topology (lead)

**Supports.** T1 is uniqueness of a landscape-valued mean path, with the Hilbert-space reason named and [8] attached. That blocks the diagram-mean objection (Wasserstein means on diagrams need not be unique). T2 is a localisation bound for landscape-valued CUSUM under mixing, not a claim that CUSUM “detects events”. Quality no longer says “proved or they are not” while R3 withdraws uniqueness. O1 is hypotheses; O2 is proofs. §5 separates the analytical argument from the bootstrap check.

**Probes, now answered in §5.**

- **Which Wasserstein?** T2 is the diagram Wasserstein metric to which landscapes are Lipschitz [7,8]. The classical theorem [7] is bottleneck (W_∞). The O2 write-up records the exponent used for the CUSUM bound. Do not put the exponent in Vision; the ready answer is: the bound is stated for the metric in which landscapes are Lipschitz; [7] is W_∞; finite *p* is recorded if used.
- **Dependence.** T2 assumes temporal weak dependence (mixing). The admissible mixing rate is part of the proof, not a rate claimed in the proposal.
- **R3.** If landscapes fail, T1 uniqueness is dropped and O2 uses the diagram-W comparison already shown in the pilot. The landscape bound remains the target; the diagram analogue is the fallback.

**Likely lead line to the panel.** “This is a genuine statistical-topology proposal: two theorems under non-exchangeable competitive dynamics, with a falsifiable empirical platform.”

---

## Introducer 2 — statistics / sequential inference (adjacent)

**Supports.** Sample size is the right grain: 540 matches; 32 per subgroup; CI half-width 0.025 from a stated s.d.; 180 per formation for *d* ≥ 0.30; FDR; p=0.051 replication target. Success criteria are numerical. OSF and the Month-2 gate sit on Figure 1.

**Probe that was wrong in the text, now fixed.** CUSUM is a *within-match* detector (held-out match annotations). An earlier draft calibrated it with *inter-match* blocks. The text now uses across-match blocks for the T1 mean-landscape check, and within-match blocks (length from the pilot’s temporal dependence) for T2 thresholds.

**≥70% annotation agreement.** The permutation test is now stated as against chance alignment of event times (O2 success sentence).

**Still a discussion question, not a text change.** Co-I time is 0.1 FTE combined. Powathil’s 33 hours are enough if he is a critic of an already-stated proof strategy (Hilbert + bounded domain), not the person writing the paper.

**Likely lead line.** “The design is powered, pre-registered, and the sequential procedure is not confused with the proof.”

---

## Introducer 3 — general mathematical sciences (scheme and remit)

**Supports.** Page 1 is a system class, two obstacles, two theorems, proof-of-principle, then football as the testbed. New collaboration and RA training are explicit. Health is not an in-grant deliverable.

**Probes that were wrong in the text, now fixed.**

- **[6,8] on “UK groups lead”.** Those papers are INRIA / Canada. They now sit on “current methods remain confined to static or exchangeable settings.”
- **Powathil as ornament.** He advises on O2 well-posedness; oncology is the Standard Grant.
- **AI-washing.** “AI-enabled modelling” was dropped from the priorities clause. The work is statistical topology and sequential inference.
- **StatsBomb.** Named in §4 as the SCAFC data route, matching the public summary and partners form.

**Still a presentation risk.** If Introducer 1 opens with formations and loop-presence rates, Introducer 3 will hear sports science. The pitch order above is the mitigation.

**Likely lead line.** “Scheme-compliant Small Grant: proof-of-principle mathematics, a new collaboration, and a structured RA post, with football as the bounded testbed.”

---

## Ranking risk

Fundable if Introducer 1 accepts T1/T2 as theorem-level and Introducer 3 accepts remit. The two drop paths are: (i) Introducer 1 treats R3 as the real project and the landscape theorems as decorative; (ii) Introducer 3 hears “Championship / SCAFC” before “non-exchangeable statistical topology.” Both are presentation risks more than remaining text risks.

---

## Fixes applied in this review cycle

**First pass (score-moving, before this note).** Hilbert uniqueness [8]; Quality aligned with R3; UK-leadership citation moved; across-match vs within-match bootstrap; Powathil in-grant role; AI priority dropped.

**Residual pass (this note).**

| Residual | Action | Where |
|---|---|---|
| W_∞ vs finite *p* unnamed | Named: [7] is bottleneck (W_∞); landscapes Lipschitz [7,8]; exponent recorded in the O2 proof | §5 |
| Mixing rate unnamed | T2 assumes weak dependence (mixing); admissible rate is part of the proof | §1 T2, §5 |
| [17] claimed as “ArXiv preprint” | Now “manuscript submitted to JACT” until an arXiv id exists | `02` and `04_References.md` |
| 70% vs chance alignment | Permutation test stated as against chance alignment of event times | §4 O2 |
| StatsBomb only in the summary | SCAFC data route named in the V&A | §4 |
| Word overflow | Standing cut rule below; not cut in advance | This note |

---

## Standing process notes (not V&A text)

1. **Page-cut.** The §3 EPSRC-priorities sentence was dropped in this residual pass to fund the W_∞ / mixing clauses. If Word still overflows after the 16 cm Gantt paste, next cut is the StatsBomb clause in §4 (“through its StatsBomb agreement”). Do not cut T1/T2, the dual O2 success test, or the scheme-fit sentences (proof-of-principle, RA training, new collaboration).
2. **Paste Figure 1** at ~16 cm width. Caption is already in the V&A (“Twelve-month workplan…”).
3. **[17] arXiv.** When a preprint id exists, restore it in `02` and `04_References.md`. Until then, “manuscript submitted” is the defensible form.
4. **[23]** remains “in preparation”; do not cite it as published.
5. **Panel date check.** Confirm [17] is still “submitted” and that the SCAFC–StatsBomb agreement language matches the partners form.

---

## Verdict

The V&A is ready for postal reviewers and then the three introducers. Keep this note with the JeS pack; update the tables if a later edit moves a theorem statement or a scheme-fit sentence.
