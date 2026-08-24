# Paper A (JACT) pipeline

Reproducible analysis chain for the multiscale TDA manuscript. Analysis modules
are vendored under the paper folder (`../01_data`, `../02_tda_core`,
`../03_football_analysis`); summaries are written to `outputs/` for LaTeX sync.

## Prerequisites

- Python 3.10+ (`pip install -r ../requirements.txt`)
- SkillCorner Open Data at `../01_data/opendata/data/` (see `../01_data/README.md`)
- Run via `run_all.sh` (sets working directory to the paper root)

## Sampling profiles (`config.yaml`)

| Profile | Frames | Used for |
|---------|--------|----------|
| `uniform_150` | 150 uniformly spaced complete frames | Paper A Tables (`tab:h1single`, `tab:h1multi`, sensitivity, complementarity) |
| `cutoff_sweep_windows` | 58 windows × 4 epoch lengths | `tab:regimes`, stability scores |
| `temporal_2min` | 2-min non-overlapping windows | Grant-only temporal analysis (not headline Paper A tables) |

## Reading `regime_summary.csv` — two traps

Both are recorded as rulings R4 and R12 in `08_current/grant/FOUNDATION.md`.

**`optimal_cutoff` is not the adopted cutoff.** The column holds what
`identify_regimes()` recomputes from the sweep. For the individual scale that is
the Calinski–Harabasz optimum, **1.39 m**. The adopted individual cutoff used
throughout the paper and the grant is **2.98 m**, hard-coded as
`VALIDATED_CUTOFFS` in `primary_match_skillcorner_analysis.py` and carried over
from the earlier normalised-coverage derivation. Clustering at 1.39 m will
reproduce none of the published numbers. The tactical (12.0 m) and team (30.0 m)
rows do match the adopted values.

**`stability` is scored at the recomputed cutoff, not the adopted one.** The
score is the fraction of sweep evaluations within 0.5 m of that cutoff whose
cluster count lies within ±2 of the pooled median — partition reproducibility,
not cutoff agreement. So 0.836 (tactical) and 1.000 (team) are scored at the
adopted values, but **0.956 (individual) is scored at 1.39 m, not at 2.98 m**,
and must be recomputed before it is quoted against the grant's 0.80 gate.

## Run order

```bash
cd pipeline
chmod +x run_all.sh
./run_all.sh
```

Individual steps:

```bash
python3 steps/01_primary_uniform.py
python3 steps/02_cutoff_sweep.py
python3 steps/03_multi_match.py
python3 steps/05_event_validity.py
python3 steps/04_complementarity.py
python3 steps/06_figures.py
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
- `../figures/fig2_cycle_geometry.pdf`
