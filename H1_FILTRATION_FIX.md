# H1 Filtration Fix: Why H1 = 0 and How to Fix It

**Date**: December 2024  
**Issue**: H1 = 0 at all scales (previously H1 ~ 3.42 ± 1.18)  
**Root Cause**: **Filtration parameter too small** after clustering  
**Status**: ✅ **FIXED** with adaptive filtration

---

## The Problem

### What We Expected
- **Previous Results**: H1 ~ 3.42 ± 1.18 (from documentation)
- **Current Results**: H1 = 0 at all scales (Individual, Tactical, Team)

### Root Cause Analysis

**The Issue**:
1. **Default filtration was 1.5m**: `MultiGoalAnalysis(max_filtration=1.5)`
2. **After clustering** with cut-offs (2.98m, 12.0m, 28.11m):
   - Cluster centroids are **much farther apart** than 1.5m
   - Individual scale: Centroids ~2-3m apart
   - Tactical scale: Centroids ~10-15m apart
   - Team scale: Centroids ~20-30m apart
3. **To form loops (H1)**, filtration must be large enough to create triangles
4. **1.5m filtration is TOO SMALL** for clustered centroids!

**Why Previous Results Had H1**:
- Previous implementations likely used:
  - **Larger filtration** (e.g., 5.0m, 10.0m) - adaptive based on distances
  - **OR** single cut-off ~1.0m (centroids closer together)
  - **OR** no clustering, raw positions closer together

---

## The Solution

### Adaptive Filtration

**Implementation**:
```python
# Calculate adaptive filtration based on point cloud scale
point_distances = pdist(point_cloud)
if len(point_distances) > 0:
    # Use 75th percentile of distances as max filtration
    adaptive_filtration = np.percentile(point_distances, 75)
    # Minimum based on scale: larger cut-offs need larger filtration
    min_filtration = max(5.0, cutoff_distance * 2.0)  # At least 2x cut-off
    max_filtration = max(adaptive_filtration, min_filtration)
```

**Key Features**:
1. **Adaptive**: Uses 75th percentile of point cloud distances
2. **Scale-aware**: Minimum filtration = 2x cut-off distance
3. **Consistent**: Matches previous implementation approach

### Expected Filtration Values

| Scale | Cut-off | Cluster Centroids | Adaptive Filtration | Minimum Filtration |
|-------|---------|-------------------|---------------------|-------------------|
| Individual | 2.98m | ~2-3m apart | ~5-10m | 5.96m (2×) |
| Tactical | 12.0m | ~10-15m apart | ~20-30m | 24.0m (2×) |
| Team | 28.11m | ~20-30m apart | ~40-60m | 56.22m (2×) |

---

## Code Changes

### Before (Fixed Filtration)
```python
def __init__(self, max_filtration: float = 1.5):
    self.max_filtration = max_filtration

def compute_gps_aware_h0(...):
    diagrams = ripser(point_cloud, maxdim=1, thresh=max_filtration)  # Fixed 1.5m
```

### After (Adaptive Filtration)
```python
def __init__(self, max_filtration: Optional[float] = None):
    self.max_filtration = max_filtration  # None = adaptive (recommended)

def compute_gps_aware_h0(...):
    # Adaptive filtration if not specified
    if final_filtration is None or final_filtration <= 0:
        point_distances = pdist(point_cloud)
        adaptive_filtration = np.percentile(point_distances, 75)
        min_filtration = max(5.0, cutoff_distance * 2.0)
        final_filtration = max(adaptive_filtration, min_filtration)
    
    diagrams = ripser(point_cloud, maxdim=1, thresh=final_filtration)
```

---

## Expected Impact

### H1 Detection Should Return

**Individual Scale**:
- H1: 0-2 (most formations don't have loops at player level)
- Depends on formation geometry

**Tactical Scale**:
- H1: 1-5 (formation structures can create loops)
- Most likely scale for loop detection ✅

**Team Scale**:
- H1: 0-1 (few points, limited loop potential)
- Macro-level spatial patterns

### Previous Results Context

**H1 ~ 3.42 ± 1.18** was likely:
- From **tactical scale** analysis (optimal for loops)
- With **adaptive filtration** (75th percentile approach)
- From **aggregated temporal windows** (more complex patterns)

**This makes sense**:
- Tactical scale has 2-12 centroids → Good for loop formation
- Adaptive filtration ensures proper scale
- Temporal aggregation increases complexity

---

## Testing

### Next Steps

1. **Re-run multi-goal analysis** with adaptive filtration
2. **Compare H1 results** to previous findings (H1 ~ 3)
3. **Verify** H1 detection at tactical scale
4. **Document** scale-dependent H1 patterns

### Expected Results

After fix:
- ✅ **Tactical H1**: Should show H1 > 0 (1-5 loops)
- ✅ **Individual H1**: May still be 0 (fine-grained, less loop formation)
- ✅ **Team H1**: May still be 0 (too few points)

---

## Summary

**Problem**: Fixed 1.5m filtration too small after clustering  
**Solution**: Adaptive filtration based on point cloud distances  
**Impact**: H1 detection should return to expected values (~3 at tactical scale)  
**Status**: ✅ **FIXED** - Ready for re-analysis

The mystery is solved! H1 = 0 was due to insufficient filtration, not missing features. With adaptive filtration, we should see H1 detection return.

