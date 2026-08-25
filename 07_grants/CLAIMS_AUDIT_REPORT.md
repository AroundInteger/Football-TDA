# Claims Validity Audit Report

**Date**: February 2026
**Scope**: Paper 1 (`06_papers/Paper1_MultiscaleTDA/TDALatentDynamics_Paper.md`), Grant V&A (`07_grants/small_grants/02_Vision_and_Approach - revised.md`), Grant Summary (`07_grants/small_grants/01_Application_Summary.md`)

---

## Summary of Findings

| Severity | Count | Description |
|----------|-------|-------------|
| **RED** | 7 | Factual errors requiring immediate correction |
| **AMBER** | 5 | Misleading or unsupported claims requiring revision |
| **GREEN** | 18 | Claims verified against codebase evidence |

---

## RED: Factual Errors (Must Fix)

### R1. "GPS tracking data" — Wrong data source type

**Claim**: Paper title, abstract, methods, and throughout: "GPS tracking data", "GPS-aware clustering"
**Reality**: SecondSpectrum provides **optical tracking** from stadium cameras, not GPS. SecondSpectrum captures data at 25 fps using cameras and ML — confirmed by SecondSpectrum's own documentation and FIFA EPTS certification. GPS tracking comes from wearable devices (Catapult, STATSports).
**Impact**: Runs through entire paper title, abstract, all methods sections, and grant V&A.
**Action**: Replace "GPS" with "optical" or use the neutral term "spatial tracking". Rename "GPS-aware clustering" to "measurement-aware clustering" or "proximity-aware clustering". The method itself is sound — only the label is wrong.

### R2. Frame count: 150,214 vs 150,213

**Claim**: Paper and grant: "150,214 GPS frames"
**Evidence**: `01_data/SECONDSPECTRUM_FULL_ANALYSIS_PLAN.md` line 6: "Total frames: 150,213"; `analyze_full_match_sliding_window.py` line 315: `total_frames=150213`
**Action**: Correct to 150,213.

### R3. Window count: "149 per half" vs 149 total

**Claim**: Paper Section 2.1: "yielding 149 analysis windows per half"
**Evidence**: `04_h1_loops/H1_LOOPS_FINDINGS.md` line 75: "Frames analyzed: 149 (full match)"; Paper Section 2.6 itself says "first half: windows 1-74; second half: windows 75-149" — confirming 149 total.
**Action**: Change "per half" to "across the full match" or remove the phrase entirely.

### R4. Three fabricated/incorrect references

**R4a. Jardine et al. (2023)**: Paper cites "Jardine, N., Mukherjee, S. and Turner, K. (2023). Analysing multiscale clusterings with persistent homology. arXiv:2305.04281." The actual paper at arXiv:2305.04281 is by **Schindler, D.J. and Barahona, M.** — completely different authors.
**R4b. Ulmer et al. (2022)**: Paper cites "Ulmer, M., Ziegelmeier, L. and Topaz, C.M. (2022). Change point detection in multi-agent systems based on higher-order features. Chaos, 32(1), 013117." The Chaos paper with that title is by **Gu, K., Yan, L., Li, X., Duan, X. and Liang, J.** — different authors. No paper by Ulmer, Ziegelmeier, and Topaz on this topic could be found.
**R4c. Botnan and Lesnick (2022)**: Paper cites this as "In Proceedings of the International Congress of Mathematicians, pp. 4290-4310." The actual venue is **"Representations of Algebras and Related Structures" (EMS Press)**, not ICM proceedings. The paper exists (arXiv:2203.14289) but the venue is wrong.
**Action**: Correct all three. Use actual authors for Schindler and Barahona; replace Ulmer et al. with Gu et al. or find correct Ziegelmeier reference; fix Botnan/Lesnick venue.

### R5. Two missing references cited in text

**Claim**: Introduction cites "Xia and Wei, 2014" and "Hiraoka et al., 2016" but neither appears in the References section.
**Evidence**: Both papers are real and correctly described:
- Xia, K. and Wei, G.-W. (2014). Persistent homology analysis of protein structure, flexibility and folding. *Int. J. Numer. Methods Biomed. Eng.*, 30, 814-844.
- Hiraoka, Y. et al. (2016). Hierarchical structures of amorphous solids characterized by persistent homology. *PNAS*, 113, 7035-7040.
**Action**: Add both to references section.

### R6. Tactical cutoff "12.0m" misrepresented as silhouette-optimal

**Claim**: Paper table (line 88): "Tactical | 12.0 m (silhouette-optimal range 8-15 m)"
**Evidence**: `METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md` identifies silhouette-optimal at **16.31m** (not 12.0m). The value 12.0m comes from `TACTICAL_CUTOFF_OPTIMIZATION_REPORT.md` where it was validated on 50 single frames (96% validation), not from the parameter sweep.
**Action**: Either (a) report honestly that 12.0m was selected from the tactical range and validated on single frames, or (b) use the actual sweep-optimal value. Do not claim 12.0m is "silhouette-optimal".

### R7. Team scale inconsistency: 30.0m vs 28.11m

**Claim**: Grant and some paper text use "30m" for team scale; paper table uses "28.11m".
**Evidence**: Computed optimal is 28.11m ± 0.47m. The H1 analysis used 30.0m.
**Action**: Standardise to whichever value was actually used in the H1 analysis. If H1 loops were computed at 30.0m, state 30.0m and note the computed optimal is 28.11m.

---

## AMBER: Misleading Claims (Should Revise)

### A1. "Statistical reliability exceeding 95%"

**Claim**: Grant summary and V&A: "statistical reliability exceeding 95%"
**Reality**: This phrase is never defined or computed. It appears to restate the validation rates (99%, 96%, 100%), which measure "fraction of windows where H0 falls in expected range" — not "statistical reliability" in the usual sense (confidence intervals, p-values, statistical significance).
**Action**: Replace with precise language: "scale-validation rates exceeding 95% (fraction of analysis windows producing H0 in the expected range for each regime)".

### A2. "Coherence" metric presented without explanation

**Claim**: Paper Table 3.5: "Coherence | 0.655 ± 0.076 | 0.452 ± 0.259"
**Reality**: Computed as `1 / (1 + std/mean)` — an ad-hoc inverse coefficient of variation using a 10-frame rolling window. Not a standard topological or statistical quantity. Presented alongside genuine topological features (H1 count, persistence) without distinguishing its nature.
**Action**: Either (a) remove from the paper's results table, or (b) define explicitly and label as a derived stability metric, not a topological feature.

### A3. "Network strength" is an ad-hoc compound metric

**Claim**: Paper Table 3.5: "Network strength | 4.31 ± 3.31 | 5.16 ± 2.10"
**Reality**: Computed as `n_loops × mean_persistence`. This multiplies a count by a distance measure, producing a dimensionally mixed quantity with no established theoretical basis.
**Action**: Either (a) remove, or (b) define explicitly and justify why this product is meaningful.

### A4. Circular validation risk

**Claim**: Paper Section 2.3: "Validation denotes the fraction of analysis windows in which H0 falls within the expected range for that regime."
**Reality**: The "expected ranges" (15-22 for individual, 3-12 for tactical, 1-3 for team) are defined by the analysis goal, then "validation" checks that H0 falls in those same ranges. This is partially tautological — you define the target then measure how often you hit it. The validation is more about parameter consistency across epochs than about external validity.
**Action**: Reframe as "cross-epoch consistency" rather than "validation". Acknowledge that the expected ranges are domain-informed targets, not independently derived ground truth.

### A5. Fisher's combined test: chi-squared vs permutation p-values

**Claim**: Grant V&A: "Fisher's combined test p = 0.03"
**Reality**: The computation script (`run_permutation_test.py`) computes both p = 0.10 (permutation-based) and p = 0.03 (chi-squared combination). The grant cites only the more favourable chi-squared value. For three events, reporting the permutation-based value (p = 0.10) would be more conservative.
**Action**: Report both values, or at minimum note "p = 0.03 (chi-squared); p = 0.10 (permutation)".

---

## GREEN: Verified Claims

| # | Claim | Source | Status |
|---|-------|--------|--------|
| G1 | 523 total H1 loops | `h1_loops_full_data.json`, temporal report | VERIFIED |
| G2 | 470 individual, 53 tactical | Same | VERIFIED |
| G3 | 148/149 frames with individual loops | Same | VERIFIED |
| G4 | 42/149 frames with tactical loops | Same | VERIFIED |
| G5 | Mean persistence 1.781 ± 1.455 (individual) | `temporal_evolution_report.txt` line 11 | VERIFIED |
| G6 | Mean persistence 3.285 ± 2.241 (tactical) | Same line 25 | VERIFIED |
| G7 | Max persistence 7.971 (individual) | Same | VERIFIED |
| G8 | Max persistence 9.392 (tactical) | Same | VERIFIED |
| G9 | Frame 72: persistence 7.97 | `H1_LOOPS_FINDINGS.md` line 88 | VERIFIED |
| G10 | Frame 73: persistence 9.39 | Same line 93 | VERIFIED |
| G11 | +8.5% individual persistence (1.708 → 1.853) | Temporal report; arithmetic correct | VERIFIED |
| G12 | +18.8% tactical persistence (2.998 → 3.562) | Same; arithmetic correct | VERIFIED |
| G13 | H0 = 17.85 ± 3.54 at individual scale | `MULTISCALE_UPSTREAM_EFFECTS.md` line 155 | VERIFIED |
| G14 | H0 = 7.67 ± 1.63 at tactical scale | Same | VERIFIED |
| G15 | Individual cutoff 2.98m ± 0.37m | `METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md` | VERIFIED |
| G16 | Team cutoff 28.11m ± 0.47m | Same | VERIFIED |
| G17 | Stability scores 0.88, 0.97, 0.98 | Same and `NORMALIZED_SAMPLING_RESULTS_COMPARISON.md` | VERIFIED |
| G18 | Parameter sweep: 100 test points, 58 windows, 30% | `METHODOLOGY_CUTOFF_DISTANCE_SELECTION.md` lines 40-48 | VERIFIED |
| G19 | Event transitions: -7.92 (f138), +6.98 (f12) etc. | `significant_transitions.json` | VERIFIED |
| G20 | Conflict precursors 4-6 weeks (grant) | `RESULTS_SUMMARY.md`; computed from real ACLED data | VERIFIED |
| G21 | Fisher p = 0.03 chi-squared (grant) | `run_permutation_test.py` line 280 | VERIFIED (but see A5) |
| G22 | Structural suitability conditions (grant) | `01_Conflict_Topology_Framework.md` with quantitative diagnostics | VERIFIED |

---

## Methodological Observations (2E)

These are not errors but should be acknowledged in limitations or addressed in methodology:

### M1. Single-linkage clustering
Single-linkage is known to produce elongated, chain-like clusters ("chaining effect"). For player positions this is less concerning than for high-dimensional data, but alternative linkage methods (complete, Ward's) should be noted as unexplored.

### M2. 75th percentile for adaptive filtration
The choice of 75th percentile is not theoretically motivated. No sensitivity analysis (e.g., comparing 50th, 75th, 90th percentile) is reported. This should be acknowledged.

### M3. Event correlation uses synthetic markers
The paper correctly states this, but the grant does not mention that the event correlation framework uses synthetic events. The grant's Objective 4 ("event-topology relationships") should acknowledge this is a future validation step, not a completed result.

---

## Novelty Claims Assessment (2B)

### "First application of multi-scale persistent homology to competitive, coupled, high-frequency dynamical systems"
No prior work combining scale decomposition with persistent homology for competitive spatial tracking data was found. The claim appears defensible but is very specific in its qualifications. One 2025 paper uses persistent homology for player scouting (different application), and Topaz et al. (2015) show multi-scale structure in simulated collective motion (non-competitive, non-tracking).
**Recommendation**: Keep but soften slightly: "To our knowledge, no prior work..."

### "Multi-scale complementarity...has not been reported in prior TDA applications"
This is a strong negative claim. Topaz et al. (2015) show different structures at different filtration values, which is related. The specific finding of complementarity (where neither scale subsumes the other) may be novel.
**Recommendation**: Soften to "has not been explicitly characterised" rather than "has not been reported".

---

## Priority Corrections List

### Critical (must fix before any submission):
1. **R1**: Replace "GPS" with "optical tracking" throughout paper and grant
2. **R4**: Fix three incorrect/fabricated references
3. **R5**: Add two missing references to reference list
4. **R3**: Fix "149 per half" to "149 total"
5. **R2**: Fix frame count to 150,213

### Important (should fix):
6. **R6**: Correct tactical cutoff description (not silhouette-optimal)
7. **R7**: Standardise team scale (28.11m vs 30.0m)
8. **A1**: Replace "statistical reliability exceeding 95%"
9. **A5**: Report both Fisher p-values

### Recommended:
10. **A2/A3**: Remove or properly define ad-hoc metrics (coherence, network strength)
11. **A4**: Reframe "validation" as "cross-epoch consistency"
12. **M1-M3**: Add sensitivity analysis acknowledgements to limitations

---

## Code Corrections Applied

In addition to manuscript corrections, the following Python scripts were updated:

### `04_h1_loops/analyze_multiscale_upstream_effects.py`
1. **20-frame limitation removed** (line 392): Network analysis was only computed on the first 20 of 149 frames (`[:20]` slice). This meant network strength values (4.31 ± 3.31, 5.16 ± 2.10) were based on a small subset. Removed the slice to use all frames. The ad-hoc metrics have also been removed from the paper table.
2. **Team cutoff standardised** (line 36): Changed from `'team': 30.0` to `'team': 28.11` to match the information-content optimal and `analyze_h1_loops.py`.
3. **Author line**: `GPS-TDA Research Team` → `TDA Research Team`

### `04_h1_loops/analyze_h1_loops.py`
1. **Data loading comment**: `"Load GPS data"` → `"Loading SecondSpectrum optical tracking data"`
2. **Author line**: `GPS-TDA Research Team` → `TDA Research Team`

### `04_h1_loops/analyze_h1_temporal_evolution.py`
1. **Author line**: `GPS-TDA Research Team` → `TDA Research Team`

### `04_h1_loops/analyze_h1_event_correlation.py`
1. **Sampling rate comment**: `"Typical GPS sampling rate"` → `"SecondSpectrum optical tracking frame rate"`
2. **Author line**: `GPS-TDA Research Team` → `TDA Research Team`

---

## Corrections Applied to Paper 1

| Issue | Action Taken |
|-------|-------------|
| R1 (GPS → optical) | Title, abstract, keywords, Sections 2.1, 2.2, 4.4, 5, Acknowledgements updated |
| R2 (frame count) | 150,214 → 150,213 throughout |
| R3 (window count) | "per half" → "across the full match" |
| R4a (Jardine et al.) | → Schindler, D.J. and Barahona, M. (all in-text and references) |
| R4b (Ulmer et al.) | → Gu, K., Yan, L., Li, X., Duan, X. and Liang, J. (all in-text and references) |
| R4c (Botnan/Lesnick venue) | ICM proceedings → Representations of Algebras and Related Structures, EMS Press |
| R5 (missing refs) | Xia and Wei (2014) and Hiraoka et al. (2016) added to reference list |
| R6 (tactical cutoff) | "silhouette-optimal range 8-15m" → "selected from tactical range; single-frame validated"; provenance note added |
| A1 ("statistical reliability") | Replaced with "cross-epoch consistency rates" (grant V&A and Summary) |
| A2/A3 (ad-hoc metrics) | Coherence, network complexity, network strength removed from paper Table 3.5; replaced with standard topological quantities |
| A4 (validation framing) | Validation footnote expanded to describe cross-epoch consistency methodology |
| A5 (Fisher p-values) | Both p = 0.03 and p = 0.10 now reported in grant Summary |

## Corrections Applied to Grant V&A

| Issue | Action Taken |
|-------|-------------|
| R2 | 150,214 → 150,213 |
| R1 | "GPS frames" → "optical tracking frames" |
| A1 | "statistical reliability exceeding 95%" → "cross-epoch consistency rates exceeding 95%" |
| A2/A3 | "high coherence", "high strength" → quantified loop frequency and persistence values |
| R6/R7 | Team scale standardised to 28.11m |

---

*Audit conducted February 2026. All evidence traced to specific file paths and line numbers as documented above.*
