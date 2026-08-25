# Paper 1 figures (`06_papers/Paper1_MultiscaleTDA/figures`)

Publication figures for the multi-scale TDA manuscript. **Output filenames match manuscript order:** `fig1` … `fig4` (LaTeX still auto-numbers them as Figure 1–4).

A parallel copy of the Python scripts and this layout exists under `08_current/paper/figures/`.

## Data export (required first)

Run from the Football-TDA project root:

```bash
python 06_papers/Paper1_MultiscaleTDA/figures/export_data_for_matlab.py
```

This exports CSV data from `h1_loops_full_data.json`, `per_window_persistence.csv`, and `event_correlation_summary.json`, writes them into this directory, and mirrors all CSVs to `08_current/paper/figures/`.

## Figure scripts

| Manuscript figure | Output files | MATLAB | Python |
|-------------------|--------------|--------|--------|
| 1. Pipeline schematic | `fig1_pipeline_schematic.pdf`, `.png` | `fig1_pipeline_schematic.m` | `fig1_pipeline_schematic.py` |
| Persistence diagrams | `fig_persistence_diagrams.pdf`, `.png` | `fig_persistence_diagrams.m` | `fig_persistence_diagrams.py` |
| 2. Cycle geometry | `fig2_cycle_geometry.pdf`, `.png` | `fig2_cycle_geometry.m` | `fig2_cycle_geometry.py` |
| 3. Temporal evolution | `fig3_temporal_evolution.pdf`, `.png` | `fig3_temporal_evolution.m` | `fig3_temporal_evolution.py` |
| 4. Event correlation | `fig4_event_correlation.pdf`, `.png` | `fig4_event_correlation.m` | `fig4_event_correlation.py` |

## MATLAB (R2025b)

From the `figures/` directory:

```matlab
fig1_pipeline_schematic
fig_persistence_diagrams
fig2_cycle_geometry
fig3_temporal_evolution
fig4_event_correlation
```

Or from command line:

```bash
/Applications/MATLAB_R2025b.app/bin/matlab -batch "cd('path/to/figures'); fig1_pipeline_schematic; fig_persistence_diagrams; fig2_cycle_geometry; fig3_temporal_evolution; fig4_event_correlation"
```

## Python

From the Football-TDA project root:

```bash
python 06_papers/Paper1_MultiscaleTDA/figures/fig1_pipeline_schematic.py
python 06_papers/Paper1_MultiscaleTDA/figures/fig_persistence_diagrams.py
python 06_papers/Paper1_MultiscaleTDA/figures/fig2_cycle_geometry.py
python 06_papers/Paper1_MultiscaleTDA/figures/fig3_temporal_evolution.py
python 06_papers/Paper1_MultiscaleTDA/figures/fig4_event_correlation.py
```

## Data dependencies

- **fig1**: None (schematic only). The Python version is the publication pipeline figure (contributions + schematic PD inset).
- **fig_persistence**: `fig_persistence_individual.csv`, `fig_persistence_tactical.csv` (from export)
- **fig2**: `fig1_*_points.csv`, `fig1_*_cycle.csv`, `fig1_*_meta.csv` (from export)
- **fig3**: `fig2_temporal.csv` (copy of `results/statistical_tests/per_window_persistence.csv`)
- **fig4**: `fig3_event_correlation.csv` (from export)
