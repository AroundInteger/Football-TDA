# Paper C — hierarchical adversarial point processes (methods)

**Sequence (locked).** Develop and submit **after Papers A and B are submitted.** Do not let Paper C delay JACT or JSS. Football is the originating case (cite A); this manuscript is not a third football paper.

**Status.** Staging draft and generators exist. Full write-up, venue submission, and co-author decision come after A/B.

**Venue (working order).** *Journal of the Royal Society Interface*; *SIAM Journal on Mathematics of Data Science* or *Foundations of Data Science* if the Tier-2 lemmas carry the paper. Not JACT (Paper A). Not JSS (Paper B).

**What this paper is.** Diagram $W_1/W_2$ analogue of mean-path and change-point inference on synthetic adversarial clouds. Ecology-led generator, robotics second, oncology Outlook only. Three-tier claims: cite (Cohen–Steiner, Carlsson–Mémoli, Page); prove T1-lite / T2-lite; conjecture full competitive dependence.

**What this paper is not.** SkillCorner re-analysis. Movebank or MIBI in the results. Relabelled `A_WIDE`. Grant T1/T2 (those are landscape-valued).

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
