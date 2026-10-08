# Friday submission harness — 7–10 October 2026

UK English. **APP98322** (EPSRC Small Grant) + **Paper A** (JACT / arXiv post).

**Definition of done (Friday):**

| Deliverable | Done when |
|---|---|
| **Grant** | JeS submitted; confirmation saved; team = PL 0.10 + PcL Villamizar 0.05 + RA Months 5–10; SCAFC partner PDF attached; V&A from `grant/live/02_Vision_and_Approach_REV4.md` ≤3 pages |
| **Paper A** | Nelly decisions C1–C5 implemented in **both** trees; `sync_to_paper.py` PASS; clean PDF from `main.tex`; posted or ready to post (arXiv / collaborator channel per your plan) |

**Decision map (do not renegotiate in prose):**  
`Paper Updated/3-Paper Paradigm/COLLABORATOR_COMMENTS_OCT2026.md`

**Normative numbers / notation:** `grant/FOUNDATION.md` (update **with** Track B, not before).

---

## Execution order

```mermaid
flowchart LR
  A[Track A: C2 then C4] --> B[Track B: C1 C3 C5 + arXiv mirror]
  B --> G[Track C: Grant JeS]
  G --> F[Friday: submit + post]
```

Tracks **A** and **C** can overlap only after Paper A methods are frozen (C2 outcome). **Grant V&A does not wait** on Paper A except where you cite the pilot; default C5 = **no** Month-2 clause insertion.

---

## Track A — Science gate + abstract (C2, C4)

**Owner:** agent or PI with pipeline venv.

### A1 — C2 diameter check (blocks methods edits)

- [x] On **150-frame** and **1,500-frame** samples, compute Vietoris–Rips on each reduced centroid cloud **to diameter** (≤22 points per cloud).
- [x] Compare finite \(H_1\) bars to pipeline output with adaptive \(\varepsilon_{\max}\).
- [x] **If no new finite bars:** remove adaptive equation, percentile ablation table, and “fitted to one cutoff” paragraph; state all \(H_1\) classes are finite on this corpus. Update `FOUNDATION.md` §2.5 in Track B.
- [ ] **If long bars appear:** keep a cut with explicit **modelling** reason (not tuning prose). *(N/A — see log.)*
- [x] Record outcome in a one-line note at the bottom of this file (dated).

**Code locus:** `paper_A_JACT/pipeline/` — add a small script or one-off step if none exists; reuse `tda_utils` / ripser patterns from step 03/04.

### A2 — C4 abstract lifetimes

- [x] Replace placeholder “short / longer bar length” in:
  - `paper_A_JACT/main.tex`
  - `paper_A_JACT/Paper_A_collaborator.md` + `.tex`
  - `arXiv_Paper_A/main.tex`
- [x] Use: individual \(96.5\% \pm 1.5\%\) (mean filtration lifetime **1.886 m**); tactical \(18.8\% \pm 6.5\%\) (**3.411 m**). Primary-match lifetimes stay in Results only.

**Gate:** `grep -R "short bar length" paper_A_JACT arXiv_Paper_A` → empty (regenerate `Paper_A_collaborator.html` optional).

---

## Track B — Manuscript + FOUNDATION (C1, C3, C5)

**Apply every edit in both trees:** `paper_A_JACT/` and `arXiv_Paper_A/`.

### B1 — C1 notation

- [x] Replace \(\overline{H_0}(\delta)\) with cluster-count curve language; replace “\(H_0 = 19\)” with **\(k\)** / connected-component count.
- [x] Touch: `sections/methods.tex`, `sections/results.tex`, figure captions, `pipeline/CUTOFF_PROTOCOL.md`.
- [x] Keep \(H_0\) only where the **group** is meant (intro homology feature).
- [x] **Same pass:** `grant/FOUNDATION.md` sweep notation (comment file: do not leave FOUNDATION on \(\overline{H_0}\) after A changes).

### B2 — C3 supplement numbering

- [x] `sections/supplement.tex`: reset table/figure counters; S1, S2, …; remove hardcoded “Supplementary Table S1” heading; body uses `Supplementary Table~\ref{tab:matches}`.

### B3 — C5 limitations (in place, no lengthening)

- [x] `sections/discussion.tex`: 106 / 802 / 822 tactical \(H_1\) loops; composed map (cluster → VR); one-sentence open problem; single-linkage remains pre-specified.

### B4 — Compile + numbers gate

- [x] `cd paper_A_JACT/pipeline && python3 sync_to_paper.py` → **PASS**
- [x] `tectonic main.tex` (or your usual build) — zero undefined refs on supplement counters *(7 Oct: `main.pdf` built; hyperref duplicate-object warnings on supplement counters — spot-check PDF numbering.)*
- [ ] Optional: rebuild `Paper_A_collaborator.pdf`

**Gate:** no `\overline{H_0}` in Paper A tex except FOUNDATION cross-refs if any remain by design.

---

## Track C — Grant JeS (parallel after REV4 strip-check)

**Masters:** `grant/live/TIMELINE.md`, `02_Vision_and_Approach_REV4.md`, `01`–`08`, `Costs/IPA_799_v2_final_lock.md`.

**C5 default:** do **not** add linkage clause to Month-2 gate unless you cut equal text elsewhere.

### C1 — Text freeze

- [x] Strip HTML / revision comments from REV4 top matter (archived `grant/live/archive/REV4_revision_header_oct2026.md`)
- [ ] Page check REV4 ≤3 pages (Calibri 11 pt, ~2 cm) — see `grant/live/JES_READINESS_OCT2026.md` (~1,619 body words; re-measure in JeS/Word)
- [x] `01_Summary.md` ≤550 words; `03` R4RI ≤1000 — Summary 546 OK; R4RI ~913 OK (JeS re-count after paste)
- [x] `04_References.md` matches REV4 Vancouver order (29 entries)

### C2 — JeS paste + attachments

- [ ] Paste 01–08; word-count each box after paste
- [x] Staff table = TIMELINE / `06_Resources_and_Costs.md` (verified 7 Oct; see `JES_READINESS_OCT2026.md`)
- [x] Gantt: `live/grant_figure_gantt.png`
- [ ] SCAFC project-partner PDF (**awaited** — Dan Morris); NV Co-I confirmed

### C3 — Dry-run + submit

- [ ] Full JeS dry-run Wednesday (or Thursday AM)
- [ ] Research Office / HoS approval complete
- [ ] **Submit Thursday** (buffer before cut-off); save confirmation Friday AM if needed

Checklist detail: `grant/live/SUBMISSION_CHECKPOINT_WEEK.md` (dates shifted to this harness).

---

## Calendar (suggested)

| Day | Focus |
|---|---|
| **Wed 7 Oct** | Track **A** complete; start **B**; grant **C1** (strip, page check, finance/NV/SCAFC unblock) |
| **Thu 8 Oct** | Finish **B** + gates; JeS **submit**; Paper A PDF frozen |
| **Fri 9 Oct** | arXiv / JACT **post**; grant confirmation archived; triage any last collaborator typos |

*(Adjust if your JeS deadline is Fri 10 — move submit to Fri AM, Paper A post Fri PM.)*

---

## Agent loop — how to run

Use **one track per loop** or a **single orchestrator** prompt. Local IDE: `/loop` per `~/.cursor/skills-cursor/loop/SKILL.md`.

### Orchestrator (recommended)

```text
/loop 25m Read 08_current/SUBMISSION_HARNESS_OCT2026.md and COLLABORATOR_COMMENTS_OCT2026.md. Continue the first unchecked item in execution order (A→B→C). One substantive chunk per tick. Update harness checkboxes in-repo. Run sync_to_paper when Track B changes numbers. End with: track status, blockers, next tick item.
```

### Single-track loops

```text
/loop 2h Track A only: C2 diameter check then C4 abstract per SUBMISSION_HARNESS_OCT2026.md. Do not edit grant V&A.
```

```text
/loop 2h Track B only: C1+C3+C5 in paper_A_JACT and arXiv_Paper_A; sync FOUNDATION.md; sync_to_paper PASS.
```

```text
/loop 2h Track C only: grant live 01–08 JeS readiness per SUBMISSION_HARNESS_OCT2026.md; no Paper A rewrites unless sync fails.
```

### Session kickoff (paste once, no loop)

```text
Open SUBMISSION_HARNESS_OCT2026.md. Execute Track A from the first unchecked box. Authority: COLLABORATOR_COMMENTS_OCT2026.md. Both Paper A trees stay in sync. Do not change REV4 for C5 unless I explicitly opt into the Month-2 clause.
```

---

## Parking lot (not this week)

- Paper B / C manuscript work
- C5 Month-2 gate clause (default **off**)
- Reopening PI 0.15 / LK / GP on JeS
- Decomposition-error toy ( `DECOMPOSITION_ERROR_PROGRAMME.md` )

---

## C2 outcome log

*(Agent or PI: one line after diameter check.)*

- **7 Oct 2026:** `drop_adaptive_epsmax` — 150 primary + 1,500 ten-match frames; 0 frames with extra finite \(H_1\) at diameter vs adaptive. JSON: `paper_A_JACT/pipeline/outputs/epsmax_diameter_check.json`; script: `pipeline/steps/check_epsmax_diameter.py`. **Next:** apply removal in Paper A methods/results + `FOUNDATION.md` §2.5 (Track A1 third box / Track B).
- **7 Oct 2026 (later):** C2 prose removal, C1–C5 TeX, `sync_to_paper` PASS, both PDFs built; grant JeS paste pack prepared (`JES_PASTE_SEQUENCE.md`).

---

## Friday deliverables (checklist)

| Task | Action |
|---|---|
| **Paper A post** | Upload `arXiv_Paper_A/main.pdf` (or JACT channel); optional collaborator resend from `Paper_A_collaborator.pdf` |
| **Grant submit** | JeS per `grant/live/JES_PASTE_SEQUENCE.md`; attach SCAFC PDF when received |
| **Git** | Commit/push manuscript + grant live changes before/after submit |
| **Archive** | JeS confirmation; note submission timestamp in `grant/live/` |

**Repo automation (Tracks A–B):** complete 7 Oct. **Track C:** human JeS + partner gates only.
