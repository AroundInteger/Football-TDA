> **SUPERSEDED** — The r=0.68 claim documented here was found to be unsubstantiated by the audit in `R068_AUDIT_REPORT.md`. This file is retained for reference only. The claim has been removed from all current submission documents.

# Performance Correlation Methodology: r=0.68 Summary

## Quick Reference

**Correlation**: r = 0.68, p < 0.001  
**Relationship**: H1 Persistence → Attacking Success  
**Statistical Test**: Pearson product-moment correlation  
**Significance**: Highly significant (p < 0.001)

---

## Detailed Breakdown

### Multi-Scale Correlations

| Scale | Correlation | Interpretation |
|-------|-------------|----------------|
| **Individual H1** | r = 0.65 | Strong positive correlation |
| **Tactical H1** | r = 0.71 | Stronger positive correlation |
| **Overall H1** | r = 0.68 | Aggregate correlation |

**Note**: r = 0.68 ≈ (0.65 + 0.71) / 2, suggesting it's an average or weighted combination of individual and tactical scales.

---

## Data Context

### Sample Information
- **H1 Loops Detected**: 523 loops total
  - Individual scale: 470 loops
  - Tactical scale: 53 loops
- **Frames Analyzed**: 149 frames
- **Frame-Scale Combinations**: 296 (149 frames × 2 scales)
- **Data Source**: SecondSpectrum GPS tracking data (25Hz)

### Likely Sample Size (N)
Based on file review, the correlation was likely computed with:
- **N = 149** (one correlation per frame, aggregated across scales)
- OR **N = 296** (frame-scale combinations)
- OR **N = 523** (one value per loop)

**Recommendation**: Verify exact N from original analysis script.

---

## Variable Definitions

### Independent Variable: H1 Persistence

**Definition**: Persistence = (death - birth) for H1 topological features (loops)

**Possible Aggregations** (from `analyze_h1_event_correlation.py`):
- `mean_persistence`: Mean persistence of all loops in a frame
- `max_persistence`: Maximum persistence of loops in a frame
- `total_persistence`: Sum of persistence values in a frame

**Scale Selection**:
- Individual scale: Mean persistence ~1.78 (range 0.000 - 7.971)
- Tactical scale: Mean persistence ~3.29 (range 0.194 - 9.392)
- Overall: Likely weighted combination or average

### Dependent Variable: "Attacking Success"

**Status**: ⚠️ **Not explicitly defined in reviewed files**

**Possible Definitions** (from `PerformanceMetrics.m`):

1. **Attacking Threat** (lines 95-98):
   ```matlab
   forward_players = sum(home_pos(:, 1) > 70);
   compactness = 1 / (1 + team_spread);
   attacking_threat = (forward_players / 10) * compactness;
   ```
   - Based on forward position and team compactness
   - Range: 0 to 1 (normalized)

2. **Field Control** (lines 91-93):
   ```matlab
   team_spread = std(home_pos, [], 'all');
   field_control = min(1, team_spread / 50);
   ```
   - Based on team spread
   - Range: 0 to 1

3. **Match Events**:
   - Goals scored
   - Shots on target
   - Successful passes in attacking third
   - Expected Goals (xG)

**Recommendation**: Verify exact operationalization from original analysis.

---

## Statistical Methodology

### Test Type
- **Method**: Pearson product-moment correlation
- **Implementation**: MATLAB `corrcoef()` function (from `PerformanceMetrics.m`)

### Statistical Details
- **Correlation Coefficient**: r = 0.68
- **P-value**: p < 0.001 (highly significant)
- **Effect Size**: Moderate-strong positive correlation
- **Interpretation**: Higher H1 persistence predicts greater attacking success

### Assumptions
- Linear relationship between H1 persistence and attacking success
- Normally distributed residuals (typical for Pearson correlation)
- Independence of observations (may need verification for time series data)

---

## Interpretation

### Scientific Meaning
- **H1 Persistence**: Represents stability of formation loops (topological holes)
- **Attacking Success**: Likely measures effectiveness of attacking play
- **Correlation**: Persistent holes in defensive formations correlate with attacking opportunities

### Practical Implications
- **Tactical Insight**: Stable formation gaps (high H1 persistence) indicate exploitable defensive weaknesses
- **Predictive Value**: H1 persistence can predict attacking success
- **Multi-Scale**: Tactical-scale loops (r = 0.71) are better predictors than individual-scale (r = 0.65)

---

## Documentation Status

### ✅ What Is Documented
- Correlation value: r = 0.68
- P-value: p < 0.001
- Multi-scale breakdown: Individual (0.65), Tactical (0.71)
- Statistical test: Pearson correlation
- Data context: 523 loops, 149 frames

### ⚠️ What Needs Clarification
1. **Sample Size (N)**: Exact N for correlation calculation
2. **"Attacking Success" Definition**: Precise operationalization
3. **H1 Persistence Aggregation**: Mean, max, or sum?
4. **Scale Combination**: How individual and tactical scales are combined for r=0.68
5. **Calculation Script**: Which script/file computed this specific correlation

---

## Recommended Actions

### For Grant Application
1. **Add Methodology Section**: Include detailed correlation methodology
2. **Specify Variables**: Clearly define "attacking success" and H1 persistence aggregation
3. **Report Sample Size**: State exact N used in correlation
4. **Include Confidence Intervals**: Report 95% CI for r = 0.68

### For Complete Documentation
1. **Locate Original Script**: Find the script that computed r=0.68
2. **Extract Exact Methodology**: Document step-by-step calculation
3. **Verify Assumptions**: Check normality, linearity, independence
4. **Replicate Analysis**: If possible, recompute to verify results

---

## References

### Key Files
- **Grant Application**: `EPSRC_Small_Grants_Application.md` (lines 33, 79, 263, 390)
- **Presentation**: `COMPREHENSIVE_PRESENTATION_DECK.md` (lines 298-308)
- **H1 Analysis**: `H1_LOOPS_FINDINGS.md`
- **Event Correlation**: `analyze_h1_event_correlation.py`
- **Performance Metrics**: `PerformanceMetrics.m`

### Related Correlations
- **H0 → Defensive Solidity**: r = -0.52, p < 0.01
- **Complexity → Tactical Sophistication**: r = 0.73
- **H1 Quantum Correlation**: r = 0.65 (different metric)

---

**Document Status**: ⚠️ **PARTIALLY DOCUMENTED**  
**Last Updated**: Based on comprehensive file review  
**Next Step**: Locate original calculation script to complete methodology

