> **SUPERSEDED** — The r=0.68 claim documented here was found to be unsubstantiated by the audit in `R068_AUDIT_REPORT.md`. This file is retained for reference only. The claim has been removed from all current submission documents.

# Performance Correlation Methodology: r=0.68 Analysis

## Overview

This document details the methodology for calculating the **r=0.68 correlation** between H1 persistence and attacking success, as referenced in the EPSRC Small Grants Application.

## Correlation Reference

**From EPSRC_Small_Grants_Application.md:**
- **Correlation**: r=0.68 for H1 persistence → attacking success
- **Context**: Preliminary work validation
- **Mentioned in**: Lines 33, 79, 263, 390

## Available Information

### Sample Size Context
From the grant application and related documents:
- **H1 Loops Detected**: 523 loops across 149 match frames
- **Data Source**: SecondSpectrum GPS tracking data
- **Temporal Coverage**: Full 90-minute match
- **Sampling Rate**: 25Hz GPS tracking

**Note**: The exact sample size (N) for the correlation calculation is not explicitly stated in the current documentation. This needs to be clarified.

### Dependent Variable: "Attacking Success"

**Current Status**: The operationalization of "attacking success" is not fully detailed in existing documentation.

**Possible Definitions** (based on codebase analysis):
1. **From PerformanceMetrics.m** (lines 79-134):
   - `attacking_threat`: Based on forward position and compactness
   - Formula: `(forward_players / 10) * compactness`
   - Where `forward_players = sum(home_pos(:, 1) > 70)`
   - And `compactness = 1 / (1 + team_spread)`

2. **From Paper2_TDALatentDynamics_Paper.md** (line 230):
   - Mentions "H1 correlation: 0.800 (formation loops and performance)"
   - But this is a different correlation value

3. **Potential Metrics**:
   - Expected Goals (xG) generated
   - Shots on target
   - Successful passes in attacking third
   - Field control in attacking zones
   - Goals scored

**Action Required**: The exact operationalization of "attacking success" needs to be documented.

### Independent Variable: H1 Persistence

**Definition**: 
- H1 persistence = (death - birth) for H1 topological features (loops)
- Represents the stability/lifespan of formation loops
- Higher persistence = more stable formation structures

**From H1_LOOPS_FINDINGS.md**:
- **Individual scale**: Mean persistence ~2.5 (range 0.000 - 7.971)
- **Tactical scale**: Mean persistence ~5.0 (range 0.194 - 9.392)
- **523 loops total** across 149 frames

**Note**: The grant application mentions "H1 persistence → attacking success" but doesn't specify which scale (individual vs. tactical) was used for the r=0.68 correlation.

### Statistical Method

**From PerformanceMetrics.m** (lines 136-193):
- Uses MATLAB's `corrcoef()` function
- Computes Pearson correlation coefficient
- Includes p-value calculation
- Significance threshold: p < 0.05 (default)

**Code Reference**:
```matlab
[correlation, p_value] = corrcoef(feature_subset, performance_subset);
```

**Statistical Test**: Pearson product-moment correlation

**P-Value**: From COMPREHENSIVE_PRESENTATION_DECK.md (line 300):
- **r = 0.68, p < 0.001** (highly significant)
- This indicates the correlation is statistically significant at α = 0.001 level

## Missing Information

To fully document the r=0.68 correlation, the following details need to be provided:

### 1. Sample Size (N)
- **Question**: What is the exact N for the correlation calculation?
- **Possible answers**:
  - N = 149 (one value per frame)
  - N = 523 (one value per H1 loop)
  - N = some aggregated value
- **Action**: Check analysis scripts or results files

### 2. Dependent Variable Operationalization
- **Question**: How exactly is "attacking success" measured?
- **Options to document**:
  - Binary (successful attack = 1, 0 otherwise)?
  - Continuous (xG, threat score, etc.)?
  - Time-windowed (attacking success in next 10 seconds)?
- **Action**: Review analysis scripts that compute this correlation

### 3. H1 Persistence Calculation
- **Question**: Which H1 persistence metric was used?
- **Options**:
  - Mean persistence per frame?
  - Maximum persistence per frame?
  - Sum of persistence values?
  - Tactical scale vs. individual scale?
- **Action**: Check which scale/aggregation method was used

### 4. Statistical Test Details
- **Test Type**: Pearson correlation (confirmed from code)
- **P-value**: Not stated in grant application
- **Confidence Interval**: Not provided
- **Effect Size**: r=0.68 (moderate-strong positive correlation)
- **Action**: Calculate/report p-value and confidence intervals

### 5. Temporal Alignment
- **Question**: How are H1 persistence and attacking success temporally aligned?
- **Options**:
  - Same time point (synchronous)?
  - H1 leads attacking success (predictive)?
  - Attacking success leads H1 (reactive)?
- **Action**: Document temporal relationship

## Recommended Documentation

### To Complete the Methodology Documentation:

1. **Create Analysis Script Review**:
   - Review `analyze_h1_loops.py`
   - Review `analyze_h1_event_correlation.py`
   - Review `PerformanceMetrics.m`
   - Identify which script computed r=0.68

2. **Document Operationalization**:
   - Define "attacking success" precisely
   - Specify measurement units and scale
   - Provide formula or algorithm

3. **Report Statistical Details**:
   - Sample size (N)
   - P-value
   - 95% confidence interval
   - Effect size interpretation
   - Assumptions checked (normality, linearity)

4. **Clarify Scale and Aggregation**:
   - Which H1 scale (individual vs. tactical)?
   - How persistence was aggregated (mean, max, sum)?
   - Time window for correlation calculation

## Files Reviewed

### Primary Analysis Files Reviewed:
1. **`analyze_h1_event_correlation.py`** ✅ REVIEWED
   - **Purpose**: Correlates H1 loops with match events (goals, possession changes, etc.)
   - **Findings**: 
     - Analyzes 523 loops across 149 frames
     - Creates frame-level aggregations (mean_persistence, max_persistence, total_persistence)
     - Does NOT directly compute r=0.68 with "attacking success"
     - Focuses on event correlation, not performance correlation
   - **Sample Size**: 149 frames (or 296 frame-scale combinations)
   - **H1 Metrics Used**: mean_persistence, max_persistence, total_persistence per frame

2. **`analyze_h1_temporal_evolution.py`** - Temporal H1 analysis (not yet reviewed in detail)

3. **`PerformanceMetrics.m`** ✅ REFERENCED
   - **Purpose**: Links topological features to performance metrics
   - **Method**: Uses `corrcoef()` for Pearson correlation
   - **Performance Metrics**: attacking_threat, field_control, defensive_stability, etc.
   - **Note**: Contains synthetic performance metric generation

4. **`Paper2_TDALatentDynamics/analyze_tda_results.m`** ✅ REVIEWED
   - **Purpose**: Analyzes TDA results for Paper 2
   - **Findings**: 
     - Reports H1 Quantum Correlation: 0.65 (different from r=0.68)
     - Does NOT show r=0.68 attacking success correlation
     - Focuses on quantum correlations, not performance correlations

### Results Files Reviewed:
1. **`h1_loop_analysis/event_correlation/significant_transitions.json`** ✅ REVIEWED
   - Contains loop transition data (persistence changes)
   - Does NOT contain performance correlation data

2. **`Paper2_TDALatentDynamics/tactical_effectiveness.csv`** ✅ REVIEWED
   - Very simple file: 3 metrics (Complexity_Effectiveness, Persistence_Balance, Quantum_Effectiveness)
   - Does NOT contain correlation coefficients

3. **`Paper2_TDALatentDynamics/quantum_topological_features.csv`** ✅ REVIEWED
   - Shows H1 Quantum Correlation: 0.65 (not 0.68)
   - Does NOT show attacking success correlation

### Documentation Files Reviewed:
1. **`H1_LOOPS_FINDINGS.md`** - H1 loop methodology ✅ REFERENCED
2. **`H1_TEMPORAL_AND_EVENT_ANALYSIS.md`** ✅ REVIEWED
   - Comprehensive temporal and event analysis
   - Does NOT detail r=0.68 attacking success correlation
   - Focuses on temporal evolution and event correlation patterns
3. **`COMPREHENSIVE_RESULTS_DOCUMENT.md`** - Comprehensive results ✅ REFERENCED

## Review Findings Summary

### What Was Found:

1. **H1 Loop Data Structure**:
   - 523 loops across 149 frames
   - Two scales: individual (470 loops) and tactical (53 loops)
   - Frame-level aggregations: mean_persistence, max_persistence, total_persistence

2. **Related Correlations Found**:
   - **H1 Quantum Correlation**: 0.65 (from quantum_topological_features.csv)
   - **Individual H1 → Attacking Success**: r = 0.65 (from COMPREHENSIVE_PRESENTATION_DECK.md)
   - **Tactical H1 → Attacking Success**: r = 0.71 (from COMPREHENSIVE_PRESENTATION_DECK.md)
   - **Overall H1 → Attacking Success**: r = 0.68 (likely aggregate of individual + tactical)

3. **Statistical Details Found**:
   - **P-value**: p < 0.001 (highly significant)
   - **Test Type**: Pearson correlation (from PerformanceMetrics.m)
   - **Multi-scale breakdown**: Individual (0.65) and Tactical (0.71)

### What Is Still Missing:

1. **Exact Calculation Script**: The specific script that computed r=0.68 is not clearly identified
2. **Sample Size (N)**: Not explicitly stated - could be:
   - N = 149 (one value per frame)
   - N = 296 (frame-scale combinations)
   - N = 523 (one value per loop)
   - N = some other aggregation
3. **"Attacking Success" Operationalization**: Not clearly defined in reviewed files
   - Possible definitions from PerformanceMetrics.m:
     - `attacking_threat = (forward_players / 10) * compactness`
     - But exact definition for r=0.68 correlation is unclear
4. **H1 Persistence Aggregation**: Not specified
   - Mean, max, or sum persistence?
   - Which scale(s) used for r=0.68?

### Likely Methodology (Inferred):

Based on the files reviewed, the r=0.68 correlation was likely computed as:

1. **Independent Variable**: H1 persistence (mean or max) per frame
   - Possibly aggregated across both scales
   - Or weighted combination: 0.68 ≈ (0.65 + 0.71) / 2

2. **Dependent Variable**: "Attacking Success"
   - Likely based on `attacking_threat` metric from PerformanceMetrics.m
   - Or derived from match events (goals, shots, successful attacks)

3. **Sample Size**: Likely N = 149 (one correlation per frame)
   - Or N = 296 (frame-scale combinations)

4. **Statistical Test**: Pearson correlation with p < 0.001

## Next Steps

1. **Search for Additional Scripts**: Look for scripts that specifically compute performance correlations
2. **Check Results Directories**: Review all CSV/JSON files in results directories
3. **Review Presentation Materials**: Check if COMPREHENSIVE_PRESENTATION_DECK.md has more details
4. **Contact Original Analysts**: If available, verify methodology with research team
5. **Replicate Analysis**: If needed, recompute correlation using available data to verify methodology

## References

- **Grant Application**: `EPSRC_Small_Grants_Application.md` (lines 33, 79, 263, 390)
- **H1 Analysis**: `H1_LOOPS_FINDINGS.md`
- **Performance Metrics**: `PerformanceMetrics.m`
- **Results Summary**: `RESULTS_SUMMARY.md`

---

**Status**: ⚠️ **INCOMPLETE** - Requires review of analysis scripts to extract full methodology

**Last Updated**: Based on codebase review  
**Action Required**: Review analysis scripts to complete methodology documentation

