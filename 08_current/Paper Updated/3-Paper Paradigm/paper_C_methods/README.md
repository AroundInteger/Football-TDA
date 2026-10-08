# Paper C — hierarchical adversarial point processes (methods)

**Sequence (locked, 7 October 2026).** Papers B and C can be worked on in parallel, because their questions and datasets are independent. Work on Paper C must not delay the *Journal of Applied and Computational Topology* or the *Journal of Sports Sciences* submissions. Football is the originating case (cite A); this manuscript is not a third football paper. Paper A does not cite Paper C.

**Status.** Staging draft and generators exist. The full write-up can proceed in parallel with Paper B. Venue submission and the co-author decision remain open.

**Venue (working order).** *Journal of the Royal Society Interface*; *SIAM Journal on Mathematics of Data Science* or *Foundations of Data Science* if the Tier-2 lemmas carry the paper. Not JACT (Paper A). Not JSS (Paper B).

**What this paper is.** Diagram $W_1/W_2$ analogue of mean-path and change-point inference on synthetic adversarial clouds. Ecology-led generator, robotics second, oncology Outlook only. Three-tier claims: cite (Cohen–Steiner, Carlsson–Mémoli, Page); prove T1-lite / T2-lite; conjecture full competitive dependence.

**What this paper is not.** SkillCorner re-analysis. Movebank or MIBI in the results. Relabelled `A_WIDE`. Grant T1/T2 (those are landscape-valued).

## What complete means

The staging draft is complete as a staging object. The manuscript may be written in parallel with Paper B. The locked primary question, and the subsidiary questions C1–C4, are in `../working_foundations.md` §1b.

The following stay outside this paper.

- Landscape theorems T1 and T2 stay with the Small Grant. A delay computed in this note is not evidence for T2.
- Linkage, cutoff, and centroid-projection stability stay with Standard Grant Aims 1 and 2, recorded in `08_current/grant/standard/AIMS_MAP.md`. There is no linkage experiment on SkillCorner. A merge sketch is allowed later only if it serves the existing ecology or robotics generators, and only as motivation for the Standard Grant.
- \(H_0\) is the homology group. Counts stay \((\beta_0, \beta_1)\). Do not import \(H_0 = 19\).
- No Joint electronic submission (JeS) numbers enter this folder. Paper A does not cite Paper C.

## Layout

| Path | Role |
|------|------|
| `AGENT_BRIEF.md` | Single-run staging agent: locks, allowed files, Definition of Done |
| `CONSISTENCY.md` | Output of that run (created when the agent finishes) |
| `draft.md` | Working manuscript (UK English) |
| `lemmas.md` | T1-lite, $W_1$–$W_2$ gap, T2-lite |
| `literature_grounding.md` | Domain decisions (simulation only; Gunner et al. 2026 cited not used as data) |
| `generators.py`, `experiments.py` | Ecology and robotics generators; import `atda_core` from `08_current/grant/evidence/toy_models/` |
| `numbers.json`, `figures/` | Quoted values and 300 dpi panels |
| `../working_foundations.md` | Three-paper strategy and non-overlap rules |

## Reproduce

```bash
cd "08_current/Paper Updated/3-Paper Paradigm/paper_C_methods"
python experiments.py --verify
python experiments.py --quick    # figures only; does not rewrite numbers.json
python experiments.py            # full MC, T1-lite sweep, Figure 5 overlay
```

Shared H0 / $W_p$ / CUSUM numerics: `08_current/grant/evidence/toy_models/atda_core.py`. Do not paste football $W_1=76.13$ or $\hat T=54$ into JeS or into `results.tex` of A/B.
