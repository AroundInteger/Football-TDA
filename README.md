# Football-TDA

Multi-scale Topological Data Analysis of competitive collective systems, using professional football as a rigorous mathematical testbed.

> **Active source of truth:** `08_current/` contains the live paper (`08_current/paper/`) and grant (`08_current/grant/`). Directories `06_papers/` and `07_grants/` are archived legacy snapshots and are **not** being updated; they are retained for provenance only. When preparing edits, PRs, or CI checks that target the current manuscript or proposal, scope them to `08_current/`.

## Research Summary

This project develops mathematical frameworks for analysing hierarchical, time-evolving systems where groups actively compete — from player formations to drone swarms. The core contribution is the first application of multi-scale persistent homology to competitive, coupled, high-frequency dynamical systems.

**Key preliminary results (single match, SecondSpectrum GPS data):**
- 523 distinct structural patterns detected across 149 analysis windows (>95% statistical reliability)
- Three validated analysis scales: individual (3 m), tactical (12 m), team (30 m)
- Topological features correlate with attacking effectiveness (r = 0.68, p < 0.001)
- GPS-aware clustering resolves H0 artefacts from measurement noise
- Adaptive filtration enables consistent H1 detection across all three scales

---

## Repository Structure

```
Football-TDA/
│
├── 01_data/                    Raw and reference data
│   ├── open-data/              StatsBomb open data
│   ├── FieldTest/              GPS capture scripts and sample match videos
│   ├── secondspectrum_results/ Loaded SecondSpectrum tracking data
│   └── *.m / *.py              Data loading and exploration scripts
│
├── 02_tda_core/                Core TDA methodology (underpins Paper 1 and grant)
│   ├── corrected_analysis/     GPS-aware pipeline results
│   ├── cutoff_distance_analysis/  Cutoff distance investigation
│   ├── cutoff_efficacy_results/   Multi-scale cutoff efficacy
│   ├── h0_investigation/       H0 artefact diagnosis
│   ├── final_h0_solution/      GPS-aware H0 resolution
│   ├── tactical_cutoff_test_results/
│   └── *.py / *.m              Pipeline, filtration, and validation scripts
│
├── 03_football_analysis/       Football-specific empirical analyses
│   ├── first_half_efficient_results/   108-window first half analysis
│   ├── second_half_efficient_results/  108-window second half analysis
│   ├── statsbomb_complete_results/     StatsBomb multi-match analysis
│   ├── parallel_segment_results/       Segment-level analysis
│   ├── temporal_spatial_analysis/      Temporal and spatial H0 analysis
│   └── *.py                            Match analysis and sliding window scripts
│
├── 04_h1_loops/                H1 closed-cycle detection (key grant result)
│   ├── h1_loop_analysis/       Complete H1 loop results and visualisations
│   │   ├── in_play_visualizations/
│   │   ├── event_correlation/
│   │   ├── temporal_analysis/
│   │   └── multiscale_upstream_effects/
│   └── *.py                    Loop detection, visualisation, and event correlation
│
├── 05_physics_analogies/       Speculative exploratory threads (feeds Paper 2)
│   ├── step1–step4 results/    MATLAB pipeline steps
│   ├── quantum_dot_*results/   Quantum dot attractor state analysis
│   ├── complete_quantum_game_theory_results/
│   └── *.py / *.m              Quantum, game theory, zero-sum scripts
│
├── 06_papers/                  LEGACY manuscript snapshots (see 06_papers/LEGACY.md)
│   ├── Paper1_MultiscaleTDA/   Archived draft; superseded by 08_current/paper/
│   └── Paper2_PhysicsAnalogies/ Archived exploratory draft (not under active revision)
│
├── 07_grants/                  LEGACY grant drafts (see 07_grants/LEGACY.md)
│   ├── small_grants/           Archived EPSRC materials; superseded by 08_current/grant/
│   └── UKRI_AI_Strategy_Alignment/  Archived exploratory strand
│
├── 08_current/                 ACTIVE sources of truth (see 08_current/README.md)
│   ├── paper/                  Multi-scale TDA paper (Draftv5.md, main.tex, sections/, references.bib)
│   ├── grant/                  EPSRC Small Grant (NN_*.md + tex/)
│   └── data/                   Provenance notes for tracking data used in 08_current
│
├── Presentation_Figures/       Figures, slides, and audience summaries
├── tda_visualisations/         Visualisation suite scripts and guides
├── figures/                    Core summary figures
├── _archive/                   Superseded intermediate explorations
│
├── GPS-TDA.md                  Original research proposal
├── PROJECT_STATUS.md           Current project status
└── COMPREHENSIVE_PRESENTATION_DECK.tex  LaTeX presentation
```

---

## Paper Roadmap

### Paper 1 — Multi-scale TDA (active)
**"Multi-Scale Persistent Homology for Competitive Spatial Systems: Measurement-Aware Methods and Validation in Professional Football"**

- Active sources: `08_current/paper/` (Markdown: `Draftv5.md`; LaTeX: `main.tex` + `sections/`; bibliography: `references.bib`)
- Legacy snapshot: `06_papers/Paper1_MultiscaleTDA/` — **do not edit**
- Status: 10-match validation complete; post-execution numbers incorporated into `08_current/paper/` (April 2026)
- Target journals: Journal of Applied and Computational Topology; SIAM Journal on Applied Mathematics

### Paper 2 — Exploratory (future)
**"Quantum Dot Attractor States in Football Team Dynamics: An Exploratory Framework"**

- Legacy snapshot: `06_papers/Paper2_PhysicsAnalogies/` (not under active revision)
- Status: Speculative — requires independent experimental validation before submission
- Target journal: Chaos, Solitons & Fractals

---

## Grant Applications

| Grant | Active sources | Legacy snapshot | Status |
|---|---|---|---|
| EPSRC Small Grant (12-month, multi-match validation) | `08_current/grant/` (`submission/` = 3-page JeS V&A; `full/` = long form) | `07_grants/small_grants/` | Active submission |
| UKRI AI Strategy — Conflict Topology | — | `07_grants/UKRI_AI_Strategy_Alignment/` | Archived / exploratory |

---

## Running the Analysis

All scripts use paths relative to the project root. Always run from here:

```bash
cd /path/to/Football-TDA
python 02_tda_core/corrected_tda_pipeline.py
python 04_h1_loops/analyze_h1_loops.py
```

**Dependencies:** `ripser`, `gudhi`, `giotto-tda`, `numpy`, `scipy`, `matplotlib`, `pandas`

```bash
pip install ripser gudhi giotto-tda numpy scipy matplotlib pandas
```
