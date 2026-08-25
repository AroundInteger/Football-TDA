# Paper B (JSS) pipeline

Football analytics manuscript: event correlation, baseline comparison, bilateral
topology, predictive utility.

## Dependency

Self-contained: event-correlation inputs are snapshotted under
`inputs/from_paper_a/`. Analysis modules are vendored under the paper folder
(`../01_data`, `../02_tda_core`, `../03_football_analysis`).

Full re-runs of steps 03–05 require SkillCorner opendata under
`../01_data/opendata/` (see `../01_data/README.md`).

## Run

```bash
cd pipeline
chmod +x run_all.sh
./run_all.sh
```

By default, step 02 writes the locked headline window-sensitivity table
(`mode: headline_table_locked` in the output JSON) matching
Table `tab:windows` in the manuscript (±0.5, ±1, ±5 s). Set
`RUN_FULL_WINDOW_SENS=1` before `./run_all.sh` for a full recomputation
(~hours; requires opendata and event inputs).

## Outputs

- `outputs/numbers.json`, `manifest.json`
- `outputs/*_summary.json` per analysis step
- `../figures/fig_event_correlation.pdf`, `fig_bilateral_timeseries.pdf`, `fig_roc_overlay.pdf`

## Sync

After `build_numbers.py`, `run_all.sh` runs:

```bash
python3 sync_to_paper.py
```

Sync failures abort the pipeline (no longer silenced).
