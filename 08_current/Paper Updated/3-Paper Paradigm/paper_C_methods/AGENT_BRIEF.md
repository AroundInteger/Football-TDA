# Agent brief — Paper C staging pass (single run)

UK English. One background job. Stop when the Definition of Done is met. Do not loop.

## Goal of this run

Make the staging tree internally consistent so a human can pick it up after Papers A and B are submitted. This is **not** authorship, venue submission, or a third football paper.

## Sequence lock

Paper C is developed **after A and B submit**. Do not delay JACT or JSS. Do not cite C from A. Do not put ecology or robotics numbers into JeS or into `results.tex` of A/B.

## Allowed to read

- This folder: `draft.md`, `lemmas.md`, `literature_grounding.md`, `numbers.json`, `generators.py`, `experiments.py`, `README.md`, `figures/`
- `08_current/grant/evidence/toy_models/atda_core.py` (shared numerics)
- `../working_foundations.md` (Paper C paragraphs only)
- `06_papers/OVERLEAF_BEST_PRACTICES.md` if you add LaTeX

## Allowed to write (this folder only)

| File | What you may do |
|------|-----------------|
| `CONSISTENCY.md` | **Required.** Run log: commands, mismatches, fixes, leftovers |
| `draft.md` | Quote-sync only: numbers and statistic names that disagree with `numbers.json` or `lemmas.md` |
| `lemmas.md` | Notation vs code only. Do not add theorems |
| `tex/` | Optional skeleton (`main.tex` + section stubs). UK English; `natbib` numbers later. No new claims |
| `numbers.json` | Only if `--verify` disagrees **and** you record the old/new pair in `CONSISTENCY.md` |

## Forbidden

- Any file under `paper_A_JACT/`, `paper_B_JSS/`, `grant/live/`, `grant/archive/`
- `grant/CANONICAL_NUMBERS.md`, JeS V&A twins, A/B `results.tex`
- Changing generator geometry, $N$, $T^*$, $\sigma$, or football toy scales
- Editing `atda_core.py` unless `--verify` cannot import; if so, stop and report
- Movebank, MIBI, LOBSTER, SkillCorner re-analysis, new domains, new co-authors
- Relabelling `A_WIDE`. Copying $W_1=76.13$ or $\hat T=54$ (football toy) into this paper
- Claiming grant T1/T2 (landscapes). T2-lite is on $\xi_t=W_1(D_t,D_{\mathrm{ref}})$, **not** consecutive-frame $W_1$
- Full Monte Carlo (`python experiments.py` with no flags). Use `--verify`; `--quick` only to write figures (it must not rewrite `numbers.json`)
- Commits, PRs, emails, venue cover letters

## Commands (from this folder)

```bash
python experiments.py --verify
```

Compare stdout to `numbers.json` and to every numeric claim in `draft.md` §§3–5 and the abstract. Fix quotes or flag them. Do not invent a replacement Monte Carlo table.

## Definition of Done

1. `--verify` exits 0, or `CONSISTENCY.md` states the exact traceback and stops.
2. `CONSISTENCY.md` lists each checked number (pass / fixed / leftover).
3. Draft and lemmas name T2-lite as $\xi_t$; consecutive-frame $W_1$ is labelled operational, not the theorem.
4. No new scientific claim, domain, or football metre in C results.
5. Stop. Do not start a second pass, a literature review, or co-author text.

## Report

Write `CONSISTENCY.md` so a human can read it without the chat. Three headings: **Ran**, **Fixed**, **Leftover**.
