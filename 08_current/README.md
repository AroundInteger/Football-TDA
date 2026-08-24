# 08_current — active sources of truth

This directory holds the **live** paper and grant sources. All edits, revisions, CI checks, and citation work target files under `08_current/`; the older `06_papers/` and `07_grants/` trees are archived snapshots and are not synchronised with the current drafts.

## Layout

```
08_current/
├── Paper Updated/             Paper drafts (General, 3-Paper Paradigm, Versions)
├── grant/                     EPSRC Small Grant — see grant/README.md
│   ├── CANONICAL_NUMBERS.md
│   ├── shared/references.bib
│   ├── full/                  Long-form application (all sections)
│   ├── submission/            3-page JeS V&A
│   └── review/                Paul review artefacts
│
├── Versions/                  Legacy paper snapshots (grant moved to grant/)
└── data/                      Data-provenance notes
    ├── README.md
    ├── primary_match/
    ├── multi_match/
    └── event_correlation/
```

## Companion analysis scripts

Python scripts supporting the post-execution numerical results in the paper live in:

```
03_football_analysis/paper_v5_revisions/
├── baseline_vs_topology.py          §3.9 baseline comparison
├── bootstrap_multi_match_ci.py      §3.2 / §3.5 bootstrap CIs (1,000 match resamples)
├── event_window_sensitivity.py      §3.8 event-window sign stability table
├── half_level_random_effects.py     §3.4 LMM + stratified permutation test
└── tda_native_distances.py          §3.5 bottleneck / landscape-L² cross-scale distances
```

These are invoked from the project root (see the root `README.md`) and write summary JSON/CSV artefacts beside the driver scripts. Reproducing the full paper numbers requires the SkillCorner open data snapshot documented in `08_current/data/README.md`.

## Conventions

- **Bibliography.** LaTeX is the citation-numbering source of truth (`natbib`, `unsrtnat`, Vancouver numbering with compressed ranges). Markdown drafts use author–year for readability; cross-reference the compiled PDF for final numbering. See `.cursor/rules/vancouver-referencing.mdc`.
- **Language.** UK English throughout both the Markdown and LaTeX twins.
- **Paper ↔ grant alignment.** The paper's preliminary-results numbers are cited by the grant via `\citep{Brown2026}`. `grant/FOUNDATION.md` is the normative source for definitions, parameters and contested numbers; any change to a headline number must go there first, then to `grant/CANONICAL_NUMBERS.md` and `grant/live/`. See `grant/README.md`.
- **Legacy trees.** Do not edit files under `06_papers/` or `07_grants/` unless explicitly salvaging a retired section — these are pinned for provenance. Each carries a `LEGACY.md` stub pointing here.

## Current alignment audit

The last grant ↔ paper sense-check (April 2026, see repository agent transcripts) reconciled:

- Power calculation in `grant/archive/full/tex/sections/02_vision_and_approach.tex` against the empirical match-level bootstrap half-width (0.042) and the pilot LMM half-effect (`β̂₁ = −0.081`, LMM `p = 0.079`, permutation `p = 0.051`).
- Paper §3.9 observed partial `R²` values (hull area 0.091; width 0.036; length 0.025; Voronoi 0.004) against Objective 2 non-redundancy criterion (partial `η² ≥ 0.05` in ANCOVA).
- Paper §3.5 Spearman ρ and Fisher OR bootstrap CIs (1,000 resamples over the 6 matches contributing to that block).
- Paper Table `tab:tda_distances` clarified as within-frame cross-scale distances, distinct from the between-tactical-class distances that drive the grant's Objective 2 Cohen's `d` power calculation.
