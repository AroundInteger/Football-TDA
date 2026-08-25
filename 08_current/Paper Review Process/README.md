# Academic Paper and Grant Review — Football-TDA

Generic review skills plus project-specific annexes for split-publication workflows.

## Skill files (read in order for Mode A)

1. `project-instructions.md` — session defaults
2. `review-orchestrator.md` — workflow modes A–D
3. `review-calibration.md` — field and venue norms
4. **Project annex** (one of):
   - `review-pef-papers.md` — PEF empirical + companion
   - `review-tda-football-papers.md` — **Paper A (JACT) + Paper B (JSS)**
5. `review-science.md`
6. `review-communication.md`
7. `review-outputs.md`

## TDA Football project

| Manuscript | Path | Venue |
|---|---|---|
| Paper A | `08_current/Paper Updated/3-Paper Paradigm/paper_A_JACT/` | JACT |
| Paper B | `08_current/Paper Updated/3-Paper Paradigm/paper_B_JSS/` | JSS |
| Paper C | `08_current/Paper Updated/3-Paper Paradigm/paper_C_methods/` | Interface / SIAM MDS (after A and B submit) |

**Reference docs:** `3-Paper Paradigm/working_foundations.md`, `grant/CANONICAL_NUMBERS.md`

**Abstract guides:** `abstract-structure-guide-tda.md` (Paper A & B)

**Recommended sequence:** Paper A Mode A → pipeline run + `sync_to_paper.py` → Paper A Mode B (section passes) → grant Format B alignment → Mode D joint check → Paper B Mode A → Paper B pipeline + sync → **Paper C only after A and B are submitted**

## Review log

| Date | Document | Mode | Output |
|---|---|---|---|
| 2026-07-06 | Paper A (JACT) V1 | Mode A | First-pass report in conversation; priority list C1–P4 |
| 2026-07-06 | Paper A (JACT) | Mode B (resume) | C2/C3 closed via `paper_A_JACT/pipeline/`; `sync_to_paper.py` PASS; C1 declarations still manual |
| 2026-07-17 | Paper A Draft_for_discussion | Mode A | Major revision; C1–C4 numeric/sampling/repro blockers |
| 2026-07-17 | Paper A Draft + LaTeX | Mode B (C1–C3) | Resynced Table 1/3/4, sampling every 290th, complementarity ρ=0.264 / OR=10.91; headline sync checks OK |
| 2026-07-17 | Paper A Draft + LaTeX | Mode B (S1–S6, C4 partial) | Team cluster-count wording; Table1/2 persistence clause; em dashes; sole author; fig frames 141/97 regen; event validity framing; Dockerfile→requirements; repo URL deferred to arXiv |
| 2026-07-17 | Paper A current | Mode B rescore | Minor revision / arXiv-ready; all C1–C3 + S1–S6 closed; only deferred: public repo URL at posting |
