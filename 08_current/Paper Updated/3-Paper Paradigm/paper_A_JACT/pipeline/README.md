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
| `cutoff_sweep` | Every complete frame, ten Table S1 matches (436{,}648 frames); grid 0.25–40.0 m | Cardinality inversion; Figure 2; `regime_summary.csv` |
| `temporal_2min` | 2-min non-overlapping windows | Grant-only temporal analysis (not headline Paper A tables) |
| native 10 Hz | complete frames | Event construct-validity (step 05) |

Headline tables use the uniform 150-frame sample on the ten Table S1 matches. That is the operational rule in `config.yaml`.

## Reading `regime_summary.csv`

Step 02 writes this file from `CUTOFF_PROTOCOL.md`. There is no hand overlay.
Adopted metres are the cardinality inversion on the pooled $H_0(\delta)$ curve.

| Scale | Adopted $\delta$ | Selection rule |
|-------|------------------|----------------|
| Individual | 2.75 m | largest $\delta$ with mean $H_0 \ge 19$ |
| Tactical | 11.75 m | nearest mean $H_0 = 5$ among $P(k \ge 4) \ge 0.5$ |
| Team | 23.0 m | smallest $\delta$ with mean $H_0 \le 2$ |

`config.yaml` `validated_cutoffs` is written by the same step. Later steps
read those values. Quality metrics are diagnostics only.

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
python3 steps/10_cutoff_sweep_figure.py
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

### Figure 1 layout editor (interactive)

To adjust panel (a) cluster positions and annotations with a live panel (b) preview:

```bash
python3 steps/00_pipeline_figure_layout_editor.py
```

Drag the coloured handles, then **Save YAML** (or press `s`). Positions are stored in
`config/fig1_layout.yaml`. **Export PDF** (or `e`) writes the full four-panel figure via
`steps/00_pipeline_figure.py`. Subsequent non-interactive runs load the saved layout
automatically.

## Outputs (committed)

- `outputs/manifest.json` — SHA-256 hashes, git commit, timestamp
- `outputs/numbers.json` — headline scalars for sync
- `outputs/regime_summary.csv`
- `outputs/uniform_150/uniform_summary.json`
- `outputs/aggregate_stats.json`
- `outputs/complementarity/complementarity_tests.json`
- `outputs/linkage/linkage_headline.json` — Discussion linkage comparison (600 frames, 4 matches)
- `../figures/fig1_pipeline_schematic.pdf`
- `../figures/fig2_cutoff_sweep.pdf`
- `../figures/fig3_cycle_geometry.pdf`
- `../figures/figS1_acf.pdf` (after step 09)
