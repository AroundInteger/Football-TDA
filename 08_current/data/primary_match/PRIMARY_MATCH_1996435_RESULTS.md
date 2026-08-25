# Primary match results: SkillCorner 1996435 (Sydney FC vs Adelaide United)

This document summarises outputs from [`03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py`](../../03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py): cutoff sweep, regime identification, and temporal H₀/H₁ statistics. Raw tables and JSON are alongside this file.

**Source data:** SkillCorner open data, match ID **1996435**, 10 Hz broadcast tracking, **43,531** frames with complete 22-player coverage (~72 minutes at this sampling rate).

---

## 1. Two notions of “cutoff”

| Role | Meaning |
|------|--------|
| **Regime sweep** | Cutoffs δ ∈ [0.5, 30] m (100 steps), four epoch lengths (1/2/5/10 min), 30% window sampling. Used to locate **individual / tactical / team** regimes via clustering metrics and H₀ validation bands. |
| **Temporal analysis** | Fixed domain-informed δ from the paper pipeline: **2.98 m** (individual) and **12.0 m** (tactical). H₀/H₁ abundances below refer to these δ values, not necessarily to the sweep-optimal individual cutoff. |

Sweep-optimal **individual** δ (Calinski–Harabasz) for this match is **1.39 m**, whilst temporal H₁ uses **2.98 m** for comparability with the published methodology.

---

## 2. Cutoff sweep: three regimes (aggregated)

Identified from `cutoff_sweep_results.csv` via `identify_regimes()` (see script). “Validation rate” is the mean rate at which H₀ cluster counts fall in the expected band for that scale; “stability” is the fraction of windows with |H₀ − median H₀| ≤ 2 at that cutoff.

| Scale | Optimal δ (m) | Validation rate | Stability | Expected H₀ (clusters) | Selection |
|-------|----------------|-----------------|-----------|-------------------------|-----------|
| Individual | 1.39 | 1.00 | 0.956 | 15–22 | CH optimum |
| Tactical | 12.00 | 1.00 | 0.836 | 2–12 | Domain-informed (12.0 m) |
| Team | 30.00 | 1.00 | 1.00 | 1–3 | IC / H₀ team validation |

Full sweep: **3,800** rows (100 cutoffs × epochs × sampled windows). See `cutoff_sweep_results.csv` and `regime_summary.csv`.

Figures: `fig_cutoff_sweep.png`, `fig_temporal_evolution.png`.

---

## 3. Temporal analysis: H₀ and H₁ abundance (δ = 2.98 m and 12.0 m)

**Windows:** 36 non-overlapping **2-minute** windows (1,200 frames each at 10 Hz). Within each window, frames are subsampled (every *n*th frame, *n* chosen so ~60 samples per window); at each sampled frame, adaptive filtration PH is run on clustered centroids.

### 3.1 H₁ (loops): totals and rates

| Scale | δ (m) | Total H₁ loops (summed across windows) | Windows with ≥1 H₁ | Presence across windows | Mean H₁ features per window | Mean persistence (non-zero), m |
|-------|-------|------------------------------------------|----------------------|-------------------------|-----------------------------|----------------------------------|
| Individual | 2.98 | **5,717** | 36 / 36 | 100% | 2.65 | 1.98 |
| Tactical | 12.0 | **377** | 36 / 36 | 100% | 0.18 | 3.09 |

Interpretation: at the **individual** scale (2.98 m), H₁ features are abundant and appear in every window. At the **tactical** scale (12.0 m), H₁ is rarer but still present in every window on aggregate; mean counts per window are much smaller than at individual scale.

### 3.2 H₀ (diagram-level counts)

For each sampled frame, **H₀** is reported as the number of points in the **H₀ persistence diagram** after clustering at δ (not the raw player count). Window-level columns in `temporal_windows.csv` are means over sampled frames:

- **`h0_individual`:** mean H₀ diagram size at δ = 2.98 m (typically in the high teens, reflecting many components at fine scale).
- **`h0_tactical`:** mean H₀ diagram size at δ = 12.0 m (smaller, reflecting fewer centroids).

Exact values vary by window; see `temporal_windows.csv` for full trajectories. Example rows (minutes into the match are approximate from `t_centre`):

| Window (exemplar) | Mean H₀ ind. | Mean H₁ ind. | Mean H₀ tac. | Mean H₁ tac. |
|-------------------|--------------|--------------|--------------|--------------|
| Early 1st half | ~18–20 | ~2.5–3.2 | ~4–5 | ~0.1–0.25 |

### 3.3 Half-time comparison (Wilcoxon rank-sum on mean persistence)

Persistence is averaged over positive H₁ bars within each window (`mean_pers_ind`, `mean_pers_tac`).

| Scale | 1st half mean (m) | 2nd half mean (m) | % change | *p* |
|-------|-------------------|-------------------|----------|-----|
| Individual | 1.90 | 2.07 | +8.8% | 0.120 |
| Tactical | 2.84 | 3.37 | +18.8% | 0.358 |

(*n* = 19 and 17 windows by period for period-labelled windows.)

---

## 4. Sensitivity (tactical scale)

**4.1 Cutoff δ, 150 uniformly spaced frames**

| δ (m) | Total H₁ | H₁ presence | Mean H₀ |
|-------|----------|-------------|---------|
| 6 | 275 | 87.3% | 13.4 |
| 8 | 162 | 68.0% | 9.8 |
| 10 | 78 | 42.7% | 6.9 |
| **12** | **21** | **12.7%** | **4.8** |
| 14 | 5 | 3.3% | 3.5 |
| 16 | 0 | 0.0% | 2.8 |
| 17 | 0 | 0.0% | 2.6 |

**4.2 Filtration percentile at δ = 12.0 m** (P50–P95): H₁ totals and presence **unchanged** in this sample (21 total, 12.7% presence); mean filtration radius increases with percentile (see `sensitivity_percentile.csv`).

---

## 5. Machine-readable outputs

| File | Contents |
|------|----------|
| `analysis_summary.json` | Headline numbers, regimes, H₁ totals, sensitivity |
| `regime_summary.csv` | Three-regime table |
| `cutoff_sweep_results.csv` | Full sweep |
| `temporal_windows.csv` | Per-window H₀/H₁ and persistence |
| `temporal_halftime_test.json` | Wilcoxon statistics |
| `sensitivity_cutoff.csv` | Tactical δ sensitivity |
| `sensitivity_percentile.csv` | Percentile ablation |

---

## 6. Regenerating

From the repository root:

```bash
python3 03_football_analysis/AvailableData/primary_match_skillcorner_analysis.py
```

or:

```bash
bash 03_football_analysis/AvailableData/run_primary_match.sh
```

---

*Generated to accompany the SkillCorner primary match pipeline; numbers match `analysis_summary.json` produced by the run that created this folder.*
