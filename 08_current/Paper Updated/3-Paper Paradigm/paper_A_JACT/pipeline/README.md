# Paper A (JACT) pipeline

Reproducible analysis chain for the multiscale TDA manuscript. Analysis modules
are vendored under the paper folder (`../01_data`, `../02_tda_core`,
`../03_football_analysis`); summaries are written to `outputs/` for LaTeX sync.

## Prerequisites

- Python 3.10+ (`pip install -r ../requirements.txt`)
- SkillCorner Open Data at the **monorepo** `01_data/opendata/data/` (see
  `../01_data/README.md` and `08_current/REPO_AND_PIPELINE.md`)
- Run via `run_all.sh` (resolves monorepo root when the paper-local tree lacks
  `matches.json`)

**Full re-run guide:** `08_current/REPO_AND_PIPELINE.md` §2 (environment, data,
`RUN_TDA_NATIVE=1`, step 08 monorepo path, success checks).

## Sampling profiles (`config.yaml`)

| Profile | Frames | Used for |
|---------|--------|----------|
| `uniform_150` | 150 uniformly spaced **complete** frames (`stride = N // 150`) | Paper A tables (primary and ten-match), sensitivity, complementarity, cardinality null |
| `acf_supplement` | 1 Hz on the primary match | Supplementary ACF panel only; does **not** choose the stride |
| `cutoff_sweep_windows` | 58 windows × 4 epoch lengths | `tab:regimes`, stability scores |
| `temporal_2min` | 2-min non-overlapping windows | Grant-only temporal analysis (not headline Paper A tables) |
| native 10 Hz | complete frames | Event construct-validity (step 05) |

Ten-match validation previously used every 100th tracking line. That is no longer used. Re-run steps 03, 04, and 07 after this change before treating committed `outputs/` as matching the Methods.

## Reading `regime_summary.csv`

Ruling R12 (closed 25 Aug 2026). The file records **adopted** cutoffs and
**stability at the adopted cutoff**, not the raw Calinski–Harabasz optimum.

| Scale | Adopted $\delta$ | Stability at adopted | Notes |
|-------|------------------|----------------------|-------|
| Individual | 2.98 m | 0.875 | CH optimum is 1.39 m (stability 0.956); not adopted |
| Tactical | 12.0 m | 0.836 | domain-informed within metric disagreement |
| Team | 30.0 m | 1.000 | IC / team $H_0$ validation |

Cluster at the **adopted** values in `VALIDATED_CUTOFFS`. Never cluster at 1.39 m
expecting to reproduce the paper.

## Run order

```bash
cd pipeline
chmod +x run_all.sh
./run_all.sh
```

Individual steps:

```bash
python3 steps/00_pipeline_figure.py
python3 steps/01_primary_uniform.py
python3 steps/02_cutoff_sweep.py
python3 steps/03_multi_match.py
python3 steps/05_event_validity.py
python3 steps/04_complementarity.py
python3 steps/07_cardinality_null.py
python3 steps/08_linkage_comparison.py
python3 steps/06_figures.py
python3 steps/09_acf_supplement.py
python3 lib/build_numbers.py
python3 sync_to_paper.py
```

## Outputs (committed)

- `outputs/manifest.json` — SHA-256 hashes, git commit, timestamp
- `outputs/numbers.json` — headline scalars for sync
- `outputs/regime_summary.csv`
- `outputs/uniform_150/uniform_summary.json`
- `outputs/aggregate_stats.json`
- `outputs/complementarity/complementarity_tests.json`
- `outputs/linkage/linkage_headline.json` — Discussion linkage comparison (600 frames, 4 matches)
- `../figures/fig1_pipeline_schematic.pdf`
- `../figures/fig2_cycle_geometry.pdf`
- `../figures/figS1_acf.pdf` (after step 09)
