# Audit Report: r=0.68 "Performance Correlation" Claim

**Date**: February 2026
**Status**: CONCLUDED — claim must be removed or replaced
**Scope**: All grant documents citing "r=0.68, p<0.001" between H1 persistence and "attacking effectiveness"

---

## Finding

The r=0.68 correlation between H1 persistence and "attacking effectiveness" cited throughout the EPSRC Small Grant application **does not originate from a validated analysis against real performance data**. It must be removed from all grant and publication materials.

---

## Evidence Trail

### 1. PerformanceMetrics.m Uses Synthetic Data

The `PerformanceMetrics.m` class (in `02_tda_core/`) — the only file containing a framework for correlating topological features with performance — generates **synthetic performance metrics** rather than computing against real match outcomes:

```matlab
% Line 73-74:
obj.generateSyntheticPerformanceMetrics(team_positions);

% Lines 95-98: "attacking_threat" is a synthetic formula:
forward_players = sum(home_pos(:, 1) > 70);
compactness = 1 / (1 + team_spread);
obj.performanceData.attacking_threat = (forward_players / 10) * compactness;
```

This formula is a heuristic derived solely from player positions, not from actual match events (goals, xG, shots, possession outcomes). The other metrics (shots, goals, passes) are generated using `rand()` calls (lines 106-131).

### 2. Presentation Scatter Plot Uses Fabricated Data

`02_tda_core/Presentation_Visuals_MATLAB.m` (lines 107-110) generates a scatter plot labelled "H1 Persistence vs. Attacking Success" using **random data designed to target r=0.68**:

```matlab
x = randn(n_points, 1) * 8 + 15;
y = r_target * x + sqrt(1 - r_target^2) * randn(n_points, 1) * 5 + 40;
```

This is not derived from any analysis of actual match data.

### 3. Closest Traceable Computation is a Model-to-Model Correlation

`PersistentHomologyAnalysis.m` (line 512) computes:

```matlab
quantumPersistence.h1QuantumCorrelation = corrcoef(h1Persistence, quantumLifetimes(...));
```

This correlates H1 persistence with **quantum model lifetimes** — a model-to-model correlation, not a correlation with any external performance metric. The resulting value is **0.65** (reported in `quantum_topological_features.csv`), not 0.68.

### 4. The Existing Audit Reached the Same Conclusion

`07_grants/PERFORMANCE_CORRELATION_METHODOLOGY.md` — an earlier attempt to trace this claim — explicitly states:

- "The exact operationalization of 'attacking success' needs to be documented"
- "The specific script that computed r=0.68 is not clearly identified"
- "analyze_h1_event_correlation.py ... Does NOT directly compute r=0.68 with 'attacking success'"
- The document remains marked **INCOMPLETE**

Its best inference is that r=0.68 is approximately the average of r=0.65 (individual scale) and r=0.71 (tactical scale) from `COMPREHENSIVE_PRESENTATION_DECK.md`, but neither of those values is traced to a computation against real performance data.

### 5. No Definition of "Attacking Effectiveness" Exists

No file in the codebase contains a validated, operationalised definition of "attacking effectiveness" as a dependent variable. The term appears only in grant documents and presentation materials, never in analysis code or results files.

---

## Affected Documents

The r=0.68 claim appears in:

1. `README.md` (line 12)
2. `07_grants/small_grants/02_Vision_and_Approach.md` (lines 9, 27)
3. `07_grants/small_grants/02_Vision_and_Approach - revised.md` (lines 7, 45)
4. `07_grants/small_grants/V&A R2.md` (lines 7, 19, 25)
5. `07_grants/small_grants/V&A R3.md` (line 11)
6. `07_grants/small_grants/05_Project_Partners_Swansea_City_AFC_Letter_of_Support.md` (line 32)
7. `07_grants/small_grants/05_Project_Partners_Swansea_City_AFC_Letter_of_Support_Email.md` (line 31)
8. `07_grants/small_grants/09_Key_Changes.md` (line 12)
9. `07_grants/EPSRC_Small_Grants_Application_REVISED.md` (line 44)
10. `07_grants/UKRI_AI_Strategy_Alignment/01_Conflict_Topology_Framework.md` (line 61)
11. `07_grants/UKRI_AI_Strategy_Alignment/03_Vision_and_Approach_DualUse.md` (line 180)

---

## Recommendation

### What to Remove

- All instances of "r=0.68, p<0.001"
- All references to "attacking effectiveness" as a validated outcome variable
- The claim that "topological features correlate strongly with attacking effectiveness"

### What to Replace With

The application's headline findings should be the results that ARE robustly validated:

1. **Three validated topological scales** (Individual 2.98m/99%, Tactical 12.0m/96%, Team 30.0m/100%) — from `04_h1_loops/H1_LOOPS_FINDINGS.md`
2. **523 H1 loops** across 149 frames with closed cycle identification — from `04_h1_loops/H1_LOOPS_FINDINGS.md`
3. **Scale complementarity**: individual scale captures dynamic micro-networks; tactical scale captures stable macro-networks — from `04_h1_loops/MULTISCALE_UPSTREAM_EFFECTS.md`
4. **Temporal evolution**: persistence increases +8.5% (individual) and +18.8% (tactical) from first to second half — from `04_h1_loops/H1_TEMPORAL_AND_EVENT_ANALYSIS.md`
5. **Adaptive filtration innovation** enabling H1 detection at all scales — from `04_h1_loops/H1_LOOPS_FINDINGS.md`
6. **GPS-aware clustering** resolving H0 artefact — from `02_tda_core/CORRECTED_TDA_REPORT.md`

### Future Work

A genuine performance correlation analysis is achievable by correlating H1 persistence with StatsBomb event data (xG, shot creation, territorial gain) already integrated in `03_football_analysis/`. This should be done properly and reported only when validated, potentially as part of Objective 1 of the grant.

---

## Summary

The r=0.68 figure propagated through grant documents without a validated computational origin. The most likely explanation is that it derives from model-to-model correlations (H1 vs quantum lifetimes) that were reframed as performance correlations in presentation/grant writing. The underlying methodology (`PerformanceMetrics.m`) generates synthetic data, not real performance analysis. The claim is not fraudulent in intent — it appears to reflect an aspiration that was written as a finding — but it cannot appear in an EPSRC submission.
