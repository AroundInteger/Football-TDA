# Paper 1 figures (`08_current/Paper Updated/figures`)

Publication figures for the multi-scale TDA manuscript. Output filenames stay `fig1` … `fig4` regardless of Markdown ordering quirks in some drafts.

The same filenames and MATLAB entry points remain under [`06_papers/Paper1_MultiscaleTDA/figures/`](../../../06_papers/Paper1_MultiscaleTDA/figures/); `export_data_for_matlab.py` writes canonical CSVs to `06_papers/…` **and mirrors** them here, `08_current/paper/figures/`, and `08_current/Versions/paper/figures/`.

---

## Canonical SkillCorner reproducibility chain

Execute from the **Football-TDA repository root**:

### 1. H₁ loop archive (Fig. 2 persistence panels + export inputs)

Produces `04_h1_loops/h1_loop_analysis/h1_loops_skillcorner_1996435.json`:

```bash
python 04_h1_loops/analyze_h1_loops.py --skillcorner --match-id 1996435
```

 Override the JSON destination with `-h` defaults (`--json-name`, `--output-dir`).
 To force a SecondSpectrum rerun into the legacy file name, omit `--skillcorner`.

### 2. Primary-match temporal windows (Fig. 3 + half-level tests)

Rebuilds **`results/statistical_tests/per_window_persistence.csv`** from SkillCorner ID **1996435** using **non-overlapping 1200-frame (2 min @ 10 Hz)** windows:

```bash
python 03_football_analysis/statistical_tests_temporal.py
```

For the old exploratory mix (SecondSpectrum + three SkillCorner matches, 100-frame windows):

```bash
python 03_football_analysis/statistical_tests_temporal.py --legacy-multi
```

### 3. Event correlation summary (Fig. 4 CSV input)

Uses SkillCorner events already:

```bash
python 03_football_analysis/real_event_correlation.py
```

### 4. CSV export bundle

Prefer the SkillCorner JSON when present (`h1_loops_skillcorner_1996435.json`). Override explicitly:

```bash
export TDA_H1_LOOPS_JSON="/absolute/path/to/h1_loops_*.json"   # optional
python "08_current/Paper Updated/figures/export_data_for_matlab.py"
```

### 5. Rasterise figures

Still from repo root:

```bash
python "08_current/Paper Updated/figures/fig1_pipeline_schematic.py"
python "08_current/Paper Updated/figures/fig2_cycle_geometry.py"
python "08_current/Paper Updated/figures/fig3_temporal_evolution.py"
python "08_current/Paper Updated/figures/fig4_event_correlation.py"
python "08_current/Paper Updated/figures/fig_persistence_diagrams.py"   # optional supporting figure
```

`fig3_temporal_evolution.py` filters **`match_id == 1996435`** explicitly (no reliance on CSV row ordering).

---

## Data dependencies quick reference

| Figure | Inputs |
|--------|--------|
| 1 (`fig1_*`) | Schematic — no tracking data |
| 2 | `fig1_*individual*.csv`, `fig1_*tactical*.csv` via export script |
| 3 | `fig2_temporal.csv` mirrored from `results/statistical_tests/per_window_persistence.csv` |
| 4 | `fig3_event_correlation.csv` from `results/event_correlation/event_correlation_summary.json` |
| Persistence diagram | Same loop JSON / `fig_persistence_*.csv` from export |

---

## Environment knobs

| Variable | Effect |
|---------|--------|
| `TDA_H1_LOOPS_JSON` | Absolute path to loop JSON consumed by export + persistence scripts |
