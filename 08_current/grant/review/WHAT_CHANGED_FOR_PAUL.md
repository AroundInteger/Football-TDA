# What Changed Since First Review

This document maps each issue Paul raised to the specific changes made in the revised V&A.
Send this alongside the revised 3-page PDF.

---

## Summary of Six Problems Addressed

| # | Paul's Problem | Key Change | Where to See It |
|---|---|---|---|
| 1 | Novelty claim vague; no evidence numbers; "firstness" undefended | Two contributions named explicitly; all validation numbers included; "firstness" replaced with "advances computational topology" | V&A §Quality and Mathematical Importance, §Excellence and Importance |
| 2 | Pathway section had typos; scope creep; Standard Grant not clearly separate | Four objectives with concrete timelines; Standard Grant explicitly framed as *separate* project starting Month 9 | V&A §Pathway to Larger Research Programme, §Objective 4 |
| 3 | Opened with drone/crowd vignette; no concrete research goal upfront | Opens with "This research develops new mathematical frameworks…"; football-as-testbed stated in paragraph 1 | V&A first paragraph |
| 4 | Timeliness led with Ripser/GUDHI library availability; no theoretical novelty | Leads with three named methodological contributions (landscape dynamics, fingerprinting, empirical distributions); libraries appear as enabling context only | V&A §Timeliness |
| 5 | Team buried mid-document; no FTE or timeline upfront | "Project Structure and Team" block appears at the top of the Approach section | V&A §Project Structure and Team |
| 6 | Self-congratulatory language throughout ("optimal", "pioneering", "strong track record", fabricated impact percentages) | These phrases removed; replaced with factual statements about what the team has delivered (10-match preprint) | Throughout |

---

## Numbers Corrected

All headline statistics in the JeS submission master (`VA_compressed_V3_no_figures.md`) match `CANONICAL_NUMBERS.md` (locked 2026-07-06, Paper A pipeline recompute).

| Value | First Review Version | Revised Version | Source |
|---|---|---|---|
| Stability scores | "0.84–1.00" (single range) | 0.96 (individual), 0.84 (tactical), 1.00 (team) | `CANONICAL_NUMBERS.md` / `numbers.json` |
| Primary-match individual H₁ | uncited / vague | 95.3% (143/150) | Paper A Table 1 / `numbers.json` |
| Primary-match tactical H₁ | uncited / vague | 12.7% (19/150) | Paper A Table 1 / `numbers.json` |
| Spearman ρ (scale non-redundancy) | 0.254 (early drafts) | 0.264 | Paper A pipeline / `numbers.json` |
| "First tools to quantify…" | "the first tools to quantify" | "systematic tools to quantify" | Throughout |

---

## 3-Paper Submission Track

The JeS V&A positions this as **EPSRC Mathematical Sciences** with football as the validated testbed.

- **Paper 1 (Brown et al., 2026 → JACT, Month 1):** methodology underpinning the grant
- **Paper 2 (football analytics → *Journal of Sports Sciences*):** O2 fingerprinting and practitioner outputs
- **Paper 3 (full-season results + landscapes → JACT, Month 11):** primary output of the 12-month grant

**Excluded from submission:** the cross-domain armed-conflict TDA paper (*Brown et al., in preparation*) — ethics approval for publication is pending; citing it in the grant could trigger additional review and delay submission by months. O4 and beneficiaries retain generic transfer language only (robotics, crowd management, ecology). The `full/` long-form grant may still mention the conflict paper for internal completeness; do not paste that wording into JeS.

Event correlation from the preprint appears as a single construct-validity sentence only:
> "Real event correlation across 10 matches (104,722 event–topology pairs) demonstrates that topological features respond coherently to match dynamics."
It is not the interpretive centrepiece (that belongs in Paper B / JSS).

---

## EPSRC V&A Criteria Coverage (3-page document)

| Criterion | Covered by |
|---|---|
| Excellent quality and importance | §Quality and Mathematical Importance |
| Advances current understanding | §What This Proposal Adds, §Excellence and Importance |
| Timely | §Timeliness |
| Impacts world-leading research / society | §Beneficiaries |
| Effective and appropriate objectives | §Delivering the Objectives (O1–O4 with success criteria) |
| Feasibility and risk management | §Feasibility and Risk |
| Clear and transparent methodology | §Methodology |
| Previous work and how built upon | §Validated Foundation, §What This Proposal Adds |
| Maximise translation | §Maximising Translation |
| Research environment | §Research Environment |
| Access to services/facilities | §Research Environment (SCW, StatsBomb) |
| Host organisation support | §Research Environment (Swansea Research Office, fast-tracked ethics) |

---

## Files Changed

| File | Change |
|---|---|
| `grant/submission/VA_compressed_V3_no_figures.md` | **Submission master** — page-verified 3-page V&A for JeS paste |
| `grant/submission/VA_compressed_V3.md` | Figure variant (synced to canonical numbers) |
| `grant/submission/02_Vision_and_Approach.md` | Earlier compressed draft (superseded by V3 no-figures master) |
| `grant/submission/tex/sections/02_vision_and_approach.tex` | LaTeX twin of the 3-page V&A |
| `grant/full/01_Application_Summary.md` | Opening rewritten; stability scores corrected; "first tools" → "systematic tools" |
| `grant/full/02_Vision_and_Approach.md` | Opening, timeliness, team upfront, numbers, pathway, publication line all updated |
| `grant/full/tex/sections/01_application_summary.tex` | Same as .md equivalent |
| `grant/full/tex/sections/02_vision_and_approach.tex` | Same as .md equivalent; LaTeX typesetting applied |

---

## What Is NOT Changed (Deliberately)

- Full statistical power analysis in `grant/full/02_Vision_and_Approach.md` (appropriate in the long form only; compressed to one sentence in the 3-pager)
- Detailed Obj 2 formation-label protocol (appropriate in long form; compressed in 3-pager)
- Full computational budget detail (appropriate in long form; one sentence in 3-pager)
- References bibliographies (Topaz 2015 in PLoS ONE, sports-science literature — these are citations of others' work, not target journals)
- Team capability, resources, DMP, ethics, and project partners sections (not within the scope of Paul's V&A review)
