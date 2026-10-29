# RESOURCES AND COSTS

<!-- Paste from ## Overview through ## Impact and value (inclusive headings).
     Do not paste this header, the lock table, or the "must not say" list.
     Staff: Costs/IPA_799_16Oct_lock.md and Budget 16 10 26 IPA 799.xlsx (16 Oct 2026).
     Travel: Costs/Travel budget planner 21 10 26 IPA 799.xlsx (£2,150; 21 Oct 2026).
     Project dates 1 Mar 2027–29 Feb 2028. Month map: TIMELINE.md.
     UKRI titles: Project Lead (PL), Project co-lead (PcL).
     Tone: EPSRC cost justification (staff; facilities; travel; consumables; Exceptions). -->

Pound figures follow **Finance lock** `Costs/IPA_799_16Oct_lock.md` and workbook **`Costs/Budget 16 10 26 IPA 799.xlsx`** (staff), with travel from **`Costs/Travel budget planner 21 10 26 IPA 799.xlsx`**. **Staff total fEC:** **£96,918** (EPSRC 80% **£77,534**). **Travel:** **£2,150** (PL only, ATMCS 13). **Project total with travel:** **£99,068**. Unused headroom under the £100k fEC cap: **£932**.

| Role | Effort | Project window | JeS dates | 100% fEC |
|---|---|---|---|---|
| PL, Dr Rowan Brown | **0.10 FTE** (~4 h/week) | Months 1–12 | 1 Mar 2027–29 Feb 2028 | £17,664 |
| Research Associate (Grade 7, SP30) | 1.0 FTE | Months **5–10** (6 months) | 1 Jul 2027–31 Dec 2027 | £71,392 |
| PcL, Dr Nelly Villamizar (Mathematics) | **0.05 FTE** (~2 h/week) | Months 1–12; peak O2 Months 5–10 | 1 Mar 2027–29 Feb 2028 | £7,862 |
| Travel (Directly Incurred) | ATMCS 13, KTH Stockholm (**PL only**) | Months 4–5 | 26 Jun–3 Jul 2027 | **£2,150** |

Kilduff and Powathil are **not** costed. No equipment line. Open-access publication costs: UKRI block grant.

---

## Overview and resourcing strategy

This application asks for the minimum staff needed to analyse a full Championship football season over 12 months (1 March 2027–29 February 2028), plus one Directly Incurred conference trip for the Project Lead. Staff total £96,918 Full Economic Cost (fEC; EPSRC 80% £77,534). Travel is £2,150, bringing the project total to £99,068, with £932 unused under the £100k fEC cap. There is no equipment line, no exceptional consumables, and no costs under Exceptions. Supercomputing Wales, secure storage and meeting space are already available and are not charged to the award. Open-source software removes licence fees. Partnership data from Swansea City Association Football Club (SCAFC) are supplied in kind.

## Project staff

Staff are the main cost, and each role is sized to a clear job.

**Research Associate (RA; 1.0 FTE, Months 5–10; 1 July–31 December 2027; £71,392 at 100% fEC).** This is the main cost. A full Championship season is about 540 matches. Running and documenting that analysis is a specialist programming job: Python, parallel processing, and topological data analysis (TDA) libraries. A six-month, full-time post is the least that can deliver the season once the method is ready, and fits the £100k fEC envelope with the PL, PcL and travel lines. Months 1–4 are led by the Project Lead (PL), so the RA joins a ready, checked pipeline rather than designing it. The RA runs the season-scale computation, builds the analysis library, and hands over documented code and figures at Month 10. After that, Months 11–12 are PL-owned. Hiring this skill in-house avoids external contractors.

**Project Lead, Dr Rowan Brown (0.10 FTE, Months 1–12; about four hours per week; £17,664 at 100% fEC).** The PL designs the study, checks quality gates, proves the mathematical results, writes the papers, and manages the club partnership. This is leadership and integration, not day-to-day season processing. Four hours per week is enough because a ten-match pilot already supplies the methods, code and decision rules. The heavier periods are Months 1–4 (prepare and check the pipeline before the RA starts) and Months 9–12 (results, papers, and the evidence pack for a follow-on Standard Grant). The PL also recruits, supervises and trains the RA.

**Project co-lead, Dr Nelly Villamizar, Mathematics (0.05 FTE, Months 1–12; about two hours per week; £7,862 at 100% fEC).** The PcL gives algebraic and mathematical advice on the harder theoretical claims, mainly while the RA is in post (Months 5–10). This is review and guidance, not coding. Two hours per week is enough for that advice and for structured input to the RA's training. No other co-leads are costed.

## Facilities and infrastructure

No facilities or infrastructure are purchased on this award. Season-scale runs use about 1,600 of the PL's existing 5,000 Supercomputing Wales CPU-hours. Secure storage (about 100 TB) and estates meeting space are institutional and in-kind. Technician support for cluster setup is covered through standard estates and infrastructure charging on the staff lines, not as a separate purchase. There are no new computers, no software licences, and no paid external cluster time.

## Other cost categories

**Travel.** One Directly Incurred conference trip is costed at **£2,150** for the **Project Lead only**: Algebraic Topology: Methods, Computation and Science (ATMCS 13), KTH Stockholm, conference 28 June–2 July 2027, travel window 26 June–3 July 2027 (project Months 4–5). The RA is not costed to attend: the post starts 1 July mid-meeting, and a delayed start would leave an orphan registration. The line-item audit budget is in `Costs/ATMCS_13_travel_budget.md` (codes REG-PL / FLT-PL / TRN / HOT-PL / SUB-PL), locked from `Costs/Travel budget planner 21 10 26 IPA 799.xlsx`. Summary at planning rates (HMRC Stockholm Overseas Scale Rates; xe.com FX on 21 Oct 2026):

| Code | Item | Basis | £ |
|---|---|---|---:|
| REG-PL | Conference registration | Planner lock | 375 |
| FLT-PL | Economy return UK–Arlanda | Planner lock | 170 |
| TRN | Train / ground | UK airport rail + Arlanda link | 100 |
| HOT-PL | Hotel, 7 nights | £146/night (HMRC room SEK 1,939.50) | 1,022 |
| SUB-PL | Subsistence / food, 7 days | £69/day (HMRC residual SEK 917.50) | 483 |
| | **Trip total** | | **2,150** |

Claims keep invoices, boarding passes and the HMRC table against those codes (Swansea Travel and Expenses Policy). Unused headroom under the £100k fEC cap is **£932**. There is no fieldwork and no other conference travel. Regular local travel between Swansea collaborators is not claimed.

**Consumables.** None beyond ordinary office and computing use. No exceptional quantities.

**Exceptions.** None.

## Delivery plan

**Months 1–4 (PL).** Prepare and check the analysis pipeline; register the analysis plan; specify the RA's work so that scale-up starts from a known baseline. Present the methodology at ATMCS 13 at the Month 4–5 boundary.

**Months 5–10 (RA full-time; PL oversight; PcL advice).** Process the season, build the analysis software, and deliver a documented handover at Month 10. Drafting for a follow-on Standard Grant begins in Months 9–10 with RA input.

**Months 11–12 (PL).** Complete papers, release open code with a digital object identifier (DOI), deliver club-facing outputs, and finish the Month-12 evidence pack.

This plan puts the expensive compute work inside the RA appointment, keeps leadership and writing with the PL, and reduces risk by checking the pipeline before the RA starts.

## Impact and value

The award buys specialist staff time, one dissemination trip, and uses facilities the university already has. Outputs are a checked analysis method, open code, full-season results, club-usable summaries, and conference presentation to the applied-topology community. In-kind high-performance computing, storage and SCAFC data avoid capital and data-purchase costs. RA involvement in writing, conference presentation and Standard Grant drafting supports career development. Together, these resources give the largest publishable return within the Small Grant envelope and prepare a follow-on Standard Grant.

## What this costing must not say

- RA Months 2–10 / 9 months / Months 4–9 (lock is **Months 5–10**, 6 months).
- PL / PI 0.2 FTE or 165 hours as a separate claim (lock is **0.10 FTE**).
- Co-Is Kilduff and/or Powathil on JeS staff lines.
- Two Co-Is at 33 hours each (lock is sole PcL **Villamizar 0.05 FTE**).
- Total staff fEC £95,188 or £95,233 (current lock is **£96,918**; RA salary **£24,829**).
- MATLAB licences, paid cluster time, or a 10–15 match compute budget.
- T1/T2 statements Month 9 and calibration Month 10 as separate gates (both at Month 9).
- RA ownership of the Month-12 Standard Grant pack.
- "No conference travel" (superseded: ATMCS headroom line).
- Travel **£1,800** / 5 nights / unused headroom **£1,282** (superseded 21 Oct 2026: **£2,150** / 7 nights / unused **£932**).
