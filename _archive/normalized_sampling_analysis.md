# Normalized Sampling Strategy Analysis

**Date**: December 2024  
**Question**: Should we normalize coverage percentage across all temporal epochs?

---

## Current Sampling Strategy

| Epoch | Windows | Window Size | Coverage % | Total Time |
|-------|---------|-------------|------------|------------|
| 1min  | 5       | 1.0 min     | 5.0%       | 5.0 min    |
| 2min  | 5       | 2.0 min     | 9.3%       | 9.3 min    |
| 5min  | 4       | 5.0 min     | 20.0%      | 20.0 min   |
| 10min | 4       | 10.0 min    | 40.0%      | 40.0 min   |

**Issue**: Unequal coverage creates unfair comparisons across scales.

---

## Normalized Sampling (20% Coverage Target)

| Epoch | Current Windows | Normalized Windows | Coverage % | Increase Factor |
|-------|----------------|-------------------|------------|----------------|
| 1min  | 5              | 21                | 21.0%      | 4.2x           |
| 2min  | 5              | 11                | 22.0%      | 2.2x           |
| 5min  | 4              | 5                 | 25.0%      | 1.25x          |
| 10min | 4              | 3                 | 30.0%      | 0.75x          |

**Target**: 20% coverage for all epochs (20 minutes out of 100 minutes)

---

## Arguments FOR Normalization

### 1. **Methodological Fairness**
- ✅ Equal statistical power across all temporal scales
- ✅ Fair comparison of optimal cut-offs across epochs
- ✅ Reduces bias from sampling intensity differences
- ✅ More robust cross-scale validation

### 2. **Scientific Rigor**
- ✅ Ensures findings are not confounded by coverage differences
- ✅ Allows direct comparison of temporal stability metrics
- ✅ Better validates that cut-off optima are scale-independent

### 3. **Publication Readiness**
- ✅ Demonstrates thorough validation approach
- ✅ Addresses potential reviewer concerns about sampling bias
- ✅ Shows methodological rigor

---

## Arguments AGAINST Normalization

### 1. **Computational Cost**
- ⚠️ 1min epoch: 4.2x more windows (5 → 21)
- ⚠️ 2min epoch: 2.2x more windows (5 → 11)
- ⚠️ Each window requires 200 cut-off sweeps
- ⚠️ Total computation: ~3-4x increase

### 2. **Diminishing Returns**
- ⚠️ Current coverage may already be sufficient for validation
- ⚠️ Temporal stability already demonstrated (stability > 0.85)
- ⚠️ Optimal cut-offs are consistent across current sample sizes

### 3. **Practical Considerations**
- ⚠️ 41.3% unique coverage already provides robust validation
- ⚠️ Computational resources may be limited
- ⚠️ Time constraints for analysis

---

## Recommended Approach: **Balanced Normalization**

### Option 1: Moderate Normalization (Recommended)

**Target**: 15% coverage for all epochs (compromise between fairness and efficiency)

| Epoch | Windows | Coverage % | Increase Factor |
|-------|---------|------------|----------------|
| 1min  | 15      | 15.0%      | 3.0x           |
| 2min  | 8       | 16.0%      | 1.6x           |
| 5min  | 3       | 15.0%      | 0.75x          |
| 10min | 2       | 20.0%      | 0.5x           |

**Benefits**:
- ✅ More balanced comparison (15-20% range)
- ✅ Reasonable computational cost (moderate increase)
- ✅ Still demonstrates methodological rigor

### Option 2: Two-Tier Normalization

**Tier 1: Core Validation** (10% coverage)
- All epochs: 10% coverage
- Faster, initial validation

**Tier 2: Comprehensive Validation** (20% coverage)
- All epochs: 20% coverage
- Thorough validation for publication

### Option 3: Statistical Power-Based Sampling

**Calculate required sample size** based on:
- Effect size of interest
- Desired statistical power (e.g., 0.8)
- Significance level (e.g., 0.05)

This would determine minimum samples needed rather than arbitrary percentage.

---

## Implementation Recommendation

### **Phase 1: Re-run with Moderate Normalization (15%)**

1. Update investigation script to use normalized sampling
2. Re-run analysis with balanced coverage
3. Compare results with current findings
4. Validate that optimal cut-offs remain consistent

### **Phase 2: Decision Point**

**If results consistent with current findings:**
- Current validation is sufficient
- Normalization confirms robustness

**If results differ:**
- Normalized sampling reveals scale-dependent effects
- Provides more robust validation
- Worth the computational cost

---

## Implementation Code

```python
def calculate_normalized_windows(epoch_config, target_coverage_pct, match_duration_min):
    """
    Calculate number of windows needed for target coverage
    
    Args:
        epoch_config: Epoch configuration dict
        target_coverage_pct: Target coverage percentage
        match_duration_min: Match duration in minutes
    
    Returns:
        Number of windows needed
    """
    window_min = epoch_config['seconds'] / 60
    target_time_min = match_duration_min * target_coverage_pct / 100
    windows_needed = int(np.ceil(target_time_min / window_min))
    return windows_needed

# Apply to all epochs
target_coverage = 15.0  # 15% compromise
for epoch_name, config in epochs.items():
    n_windows = calculate_normalized_windows(
        config, target_coverage, match_duration_min
    )
    print(f"{epoch_name}: {n_windows} windows for {target_coverage}% coverage")
```

---

## Conclusion

**Recommendation**: **YES, normalize coverage** but use **moderate normalization (15%)** as a compromise:

1. ✅ **Methodologically sound**: Fair comparison across scales
2. ✅ **Computationally feasible**: Reasonable increase (not 4x)
3. ✅ **Scientifically robust**: Better validation without excessive cost
4. ✅ **Publication-ready**: Demonstrates rigor

**Alternative**: If computational resources are limited, document current approach but acknowledge coverage difference as a limitation in methodology section.

---

**Decision**: Implement moderate normalization (15% coverage) and re-run investigation.

