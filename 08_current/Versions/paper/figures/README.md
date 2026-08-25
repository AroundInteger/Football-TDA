# Paper 1 figures (`08_current/paper/figures`)

Publication figures for the multi-scale TDA manuscript. **Output filenames match manuscript order:** `fig1` … `fig4` (LaTeX still auto-numbers them as Figure 1–4).

Implementations are **Python** (primary here). The same script names and MATLAB entry points are mirrored under `06_papers/Paper1_MultiscaleTDA/figures/`.

## Data export (required first)

Run from the Football-TDA project root:

```bash
python 06_papers/Paper1_MultiscaleTDA/figures/export_data_for_matlab.py
```

Copy the generated CSVs into this directory so the Python figure scripts can read them (same layout as `06_papers/.../figures/`):

- `fig1_*` point/cycle/meta files, `fig2_temporal.csv`, `fig3_event_correlation.csv`, persistence CSVs if using `fig_persistence_diagrams.py`.

## Figure scripts (Python)

From the Football-TDA project root:

```bash
python 08_current/paper/figures/fig1_pipeline_schematic.py
python 08_current/paper/figures/fig2_cycle_geometry.py
python 08_current/paper/figures/fig3_temporal_evolution.py
python 08_current/paper/figures/fig4_event_correlation.py
```

| Manuscript figure | Output files | Script |
|-------------------|--------------|--------|
| 1. Pipeline schematic | `fig1_pipeline_schematic.pdf`, `.png` | `fig1_pipeline_schematic.py` |
| 2. Cycle geometry | `fig2_cycle_geometry.pdf`, `.png` | `fig2_cycle_geometry.py` |
| 3. Temporal evolution | `fig3_temporal_evolution.pdf`, `.png` | `fig3_temporal_evolution.py` |
| 4. Event correlation | `fig4_event_correlation.pdf`, `.png` | `fig4_event_correlation.py` |

## Data dependencies

- **fig1**: none (schematic only).
- **fig2**: `fig1_individual_points.csv`, `fig1_individual_cycle.csv`, `fig1_individual_meta.csv`, `fig1_tactical_points.csv`, `fig1_tactical_cycle.csv`, `fig1_tactical_meta.csv` (from export).
- **fig3**: `fig2_temporal.csv` (from export; copy of `results/statistical_tests/per_window_persistence.csv`).
- **fig4**: `fig3_event_correlation.csv` (from export).
