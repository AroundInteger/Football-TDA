Reading the V3 document carefully against the full V1/V2 priority list before writing the review.Now I have a complete picture. Writing the Mode B review.

---

```
REVISION REVIEW — Vision & Approach — V2 → V3 (compressed)
Sections reviewed: all
```

---

## WHAT HAS IMPROVED ✅

The compression is genuinely well-executed. The scientific substance has been preserved at material density, and several structural choices in V3 are improvements on V2, not just neutral cuts.

**"What This Proposal Adds"** is an excellent new section that was absent in V2. Delineating what [12] establishes (scale-specific barcodes exist and replicate) from what this proposal investigates at population scale — distributional laws (O1), comparison geometry (O2), temporal dynamics (O3) — is exactly the framing a panel needs to understand the progression. This section earns its space even under the 3-page constraint.

**"Project Structure and Team"** clearly delineates FTE up front (PI 0.2, Co-Is 0.25 combined, RA 1.0 / 9 months). Panels appreciate this orientation before the detail of the objectives.

**O2 success criteria** are new and concrete: "topological signatures for ≥3 tactical configurations; inter-system differences with Benjamini–Hochberg FDR correction (p < 0.05)." These give a panel a specific falsifiability test.

**"Scale non-redundancy"** replaces "scale complementarity" as the framing for ρ = 0.254. This is the right terminology — it names the empirically relevant property directly.

**O4** now brings Standard Grant preparation forward to Month 9, which is more realistic and signals planning maturity.

**Against the V1 priority list**, the following are confirmed resolved: C1 (compute budget consistent throughout at ∼1,600 CPU-hours / 1 Hz), C2 (placeholder removed), S1 (necessity reframed), S2 (by-construction / confirmed-empirically confusion gone), S3 (1 Hz stated with gate confirmation), S4 (270-match contingency honest about O2 power), S6 (National Importance named in section header and addressed in text), S8 (all uncaveated "first" claims removed or replaced), S9 (project structure section, D2 split, team mapping).

---

## WHAT REMAINS UNRESOLVED 🟠

**S5 — O3 mathematical question (partially addressed, 🔄).** V2 added the stated mathematical targets: well-posedness and stability of the Fréchet mean in landscape function space under the competitive sequential setting, and a stability bound for the CUSUM detection statistic under Wasserstein perturbations of the diagrams. V3 replaced these with the empirical success criterion "≥70% frame-level agreement on stability-regime segmentation across random sub-samples." That criterion is good for feasibility, but for a Quality-primary maths panel O3 is the most novel mathematical content, and what a panellist scoring science quality wants to see is the mathematical question being asked, not only the operational metric for answering it. The two statements serve different purposes and both are needed. Resolution: add approximately 25 words to O3 reinstating the mathematical question. Something in the vein of: "Mathematical targets: well-posedness of the Fréchet mean under competitive sequential paths extending [11], and a stability bound for the CUSUM statistic under Wasserstein diagram perturbations." This can slot in before the Wasserstein fallback sentence without meaningfully affecting page count.

---

## NEW ISSUES INTRODUCED ⚠️

**⚠️ P3 reverted — causal verbs back.** The V2 fix changed "engagements decrease persistence / build-up phases increase it" to "are associated with decreased / increased persistence." V3 has reverted: "on-ball engagements and quick breaks decrease persistence, build-up phases increase it (p < 0.001 for both)." The data are event-window associations, not interventions — the causal phrasing is technically inaccurate and a methodologically careful reviewer will notice. A two-word fix each time.

**⚠️ "For the first time" without caveat (Timeliness).** "A Championship season (~540 matches) now makes population-level topological statistics computationally tractable for the first time." This is lower-risk than the V1 "first rigorous framework" formulation, since it refers to scale rather than method, but it is still uncaveated. Add "to our knowledge" as a one-word insurance policy.

**⚠️ O3 success criterion needs clarification.** "≥70% frame-level agreement on stability-regime segmentation across random sub-samples" — agreement with what reference, and sub-samples of what? If this means CUSUM-identified change-points agree with tactical annotations (substitutions, formation changes) at ≥70% within randomly held-out matches, say so. Currently the sentence is precise enough to look rigorous but not precise enough to be independently understood.

**⚠️ JACT not expanded.** "submitted to ArXiv and JACT from Month 1" — JACT is not expanded for a non-specialist panel member. Add "(Journal of Applied and Computational Topology)" once.

---

## UPDATED PRIORITY LIST — V&A V3

🔴 **CRITICAL**

None outstanding. C1 and C2 are fully resolved.

🟠 **SIGNIFICANT**

S5 🔄 O3 mathematical question — add ~25-word statement of the mathematical targets (Fréchet mean well-posedness; CUSUM stability bound) before the Wasserstein fallback sentence. Operational success criteria do not substitute for a stated mathematical question for a Quality-scoring maths panel.

⚠️ PAGE COUNT — verify in Word that the Gantt fits on page 3 and total document is ≤ 3 pages. If it overflows, trim 3–4 lines or resize the Gantt.

🟡 **POLISH**

P3 🔄 "decrease persistence / increase it" → "are associated with decreased / increased persistence" (event-window data, not experimental).

P_JACT: add "(Journal of Applied and Computational Topology)" after JACT.

P_firsttime: add "to our knowledge" before "for the first time" in the Timeliness tractability sentence.

P_70pct: clarify the ≥70% criterion — specify what "agreement" is measured against and what "random sub-samples" refers to.

✅ **STRENGTHS — do not change**

\+ "What This Proposal Adds" section: structurally excellent, clearly delineates preprint from proposal contributions.

\+ O2 success criteria (≥3 configurations, BH FDR p < 0.05): concrete and testable.

\+ Project Structure and Team upfront FTE delineation.

\+ "Scale non-redundancy" framing for ρ = 0.254 is precise and correct.

\+ Power reasoning (n ≈ 32 for O1, n ≈ 180 for O2) retained verbatim — still exemplary.

\+ Month-2 stability gate and Wasserstein fallback both intact.

\+ Reproducibility posture (open-source, Zenodo DOI, OSF pre-registration, Apptainer) all present.

\+ Dual-source label verification (κ, StatsBomb / SkillCorner) retained in Risk Management.

---

## V3.1 RESOLUTIONS (applied to `VA_compressed_V3_no_figures.md`)

| Item | Fix |
|---|---|
| **S5** | O3: mathematical targets (Fréchet well-posedness; CUSUM stability bound under Wasserstein perturbations) restored before fallback sentence |
| **P3** | Event correlation: "associated with decreased / increased persistence" |
| **P_firsttime** | "to our knowledge for the first time" at this scale |
| **P_70pct** | ≥70% defined: CUSUM change-points vs tactical annotations in held-out match sub-samples |
| **P_JACT** | *Journal of Applied and Computational Topology* (JACT) expanded in Translation |

**Re-verify page count in Word** (V3.0 was exactly 3 pages; V3.1 is net ~+15 words).
