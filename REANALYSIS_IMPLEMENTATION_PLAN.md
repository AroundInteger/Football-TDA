# GPS-Aware TDA Re-Analysis Implementation Plan

**Date**: October 19, 2025  
**Purpose**: Efficient re-computation of H0 with GPS-aware clustering  
**Timeline**: 2-3 hours implementation + 5 minutes computation  
**Status**: Ready to implement  

---

## 🎯 Executive Summary

**What needs updating**: Only H0 (from 240 → 2-22 with GPS-aware clustering)  
**What stays the same**: H1, team metrics, temporal windows  
**Recommended approach**: Keep 2-minute windows, efficient re-computation  
**Estimated time**: 2-3 hours to code, 5 minutes to run  

---

## 📋 Quick Decision Matrix

| Question | Answer | Rationale |
|----------|--------|-----------|
| Re-run analysis? | ✅ YES | H0 needs GPS-aware clustering |
| Change window size? | ❌ NO | 2-minute windows work well |
| Recompute H1? | ❌ NO | H1 already correct |
| Keep existing data? | ✅ YES | Leverage existing computation |
| Timeline? | ⏱️ 2-3 hrs | Simple preprocessing update |

---

## 🔧 Implementation Strategy

### **Strategy: Efficient Update (RECOMMENDED)**

**Philosophy**: Don't throw away good work—update only what needs fixing

**What to Keep**:
- ✅ Window definitions (216 windows, 2-minute size, 24s steps)
- ✅ H1 values (already correct, unaffected by preprocessing)
- ✅ Team metrics (spread, distance, area)
- ✅ Temporal structure (80% overlap)

**What to Update**:
- 🔄 H0 computation (add GPS-aware clustering)
- 🔄 Complexity index (recalculate with new H0)
- 🔄 Point cloud size (varies 2-22, not constant 240)

**Result**: New analysis file with corrected H0, same everything else

---

## 💻 Implementation Code

### **Step 1: GPS-Aware TDA Function**

```python
import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster
from ripser import ripser

def compute_gps_aware_h0(player_positions, cutoff_distance=1.0, 
                         max_filtration=1.5):
    """
    Compute H0 with GPS-aware clustering preprocessing
    
    Args:
        player_positions: (22, 2) array of player (x,y) positions
        cutoff_distance: clustering threshold in meters (default: 1.0m)
        max_filtration: maximum filtration for persistent homology
        
    Returns:
        dict with h0_count, h1_count, cluster_count, complexity
    """
    # Step 1: Hierarchical clustering (GPS-aware preprocessing)
    if len(player_positions) > 1:
        distances = pdist(player_positions)
        linkage_matrix = linkage(distances, method='single')
        cluster_labels = fcluster(linkage_matrix, cutoff_distance, 
                                  criterion='distance')
        
        # Step 2: Compute cluster centroids
        unique_labels = np.unique(cluster_labels)
        cluster_centers = []
        for label in unique_labels:
            cluster_points = player_positions[cluster_labels == label]
            center = np.mean(cluster_points, axis=0)
            cluster_centers.append(center)
        
        point_cloud = np.array(cluster_centers)
    else:
        point_cloud = player_positions
    
    # Step 3: Persistent homology on clusters
    if len(point_cloud) > 1:
        diagrams = ripser(point_cloud, maxdim=1, thresh=max_filtration)
        h0_count = len(diagrams['dgms'][0])
        h1_count = len(diagrams['dgms'][1])
    else:
        h0_count = 1
        h1_count = 0
    
    # Step 4: Calculate complexity
    cluster_count = len(point_cloud)
    complexity = (h0_count + h1_count) / cluster_count if cluster_count > 0 else 0
    
    return {
        'h0_count': h0_count,
        'h1_count': h1_count,
        'cluster_count': cluster_count,
        'complexity': complexity,
        'point_cloud': point_cloud
    }
```

### **Step 2: Re-Analysis Script**

```python
#!/usr/bin/env python3
"""
GPS-Aware TDA Re-Analysis
=========================

Updates H0 values with GPS-aware clustering while preserving H1 and other metrics
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from tqdm import tqdm

def load_original_results(first_half_file, second_half_file):
    """Load existing analysis results"""
    first_half = pd.read_csv(first_half_file)
    second_half = pd.read_csv(second_half_file)
    combined = pd.concat([first_half, second_half], ignore_index=True)
    return combined.sort_values('start_time').reset_index(drop=True)

def load_player_positions(data_file, start_frame, end_frame, 
                          frame_sampling=5):
    """
    Load player positions for a specific window
    
    Args:
        data_file: Path to SecondSpectrum data
        start_frame: Window start frame
        end_frame: Window end frame
        frame_sampling: Sample every Nth frame
        
    Returns:
        (22, 2) array of middle-frame player positions
    """
    frames = []
    with open(data_file, 'r') as f:
        for i, line in enumerate(f):
            if i < start_frame:
                continue
            if i >= end_frame:
                break
            if (i - start_frame) % frame_sampling == 0:
                try:
                    frame = json.loads(line.strip())
                    frames.append(frame)
                except:
                    continue
    
    if len(frames) == 0:
        return None
    
    # Get middle frame (representative snapshot)
    mid_idx = len(frames) // 2
    mid_frame = frames[mid_idx]
    
    # Extract player positions
    positions = []
    
    # Home team (11 players)
    for player in mid_frame.get('homePlayers', [])[:11]:
        xyz = player.get('xyz', [0, 0, 0])
        positions.append([xyz[0], xyz[1]])
    
    # Away team (11 players)
    for player in mid_frame.get('awayPlayers', [])[:11]:
        xyz = player.get('xyz', [0, 0, 0])
        positions.append([xyz[0], xyz[1]])
    
    return np.array(positions) if len(positions) == 22 else None

def reanalyze_with_gps_aware_tda(original_results, data_file, 
                                 cutoff_distance=1.0,
                                 output_file='gps_aware_results.csv'):
    """
    Re-analyze with GPS-aware H0, keeping H1 and other metrics
    
    Args:
        original_results: DataFrame with original analysis
        data_file: Path to SecondSpectrum data
        cutoff_distance: GPS-aware clustering threshold
        output_file: Output CSV file path
    """
    print("=" * 70)
    print("GPS-AWARE TDA RE-ANALYSIS")
    print("=" * 70)
    
    print(f"\nOriginal results: {len(original_results)} windows")
    print(f"GPS-aware cutoff: {cutoff_distance}m")
    
    # Create new results DataFrame
    new_results = original_results.copy()
    
    # Add new columns
    new_results['h0_gps_aware'] = 0
    new_results['cluster_count'] = 0
    new_results['complexity_gps_aware'] = 0.0
    
    print("\nProcessing windows...")
    
    successful = 0
    failed = 0
    
    for idx, row in tqdm(new_results.iterrows(), 
                         total=len(new_results),
                         desc="Re-computing H0"):
        try:
            # Load player positions for this window
            positions = load_player_positions(
                data_file,
                int(row['start_frame']),
                int(row['end_frame'])
            )
            
            if positions is None:
                print(f"Warning: No positions for window {row['window_id']}")
                failed += 1
                continue
            
            # Compute GPS-aware H0
            result = compute_gps_aware_h0(positions, cutoff_distance)
            
            # Update DataFrame
            new_results.at[idx, 'h0_gps_aware'] = result['h0_count']
            new_results.at[idx, 'cluster_count'] = result['cluster_count']
            
            # Keep original H1 (already correct)
            h1_original = row['h1_count']
            
            # Recalculate complexity with new H0
            new_h0 = result['h0_count']
            cluster_count = result['cluster_count']
            if cluster_count > 0:
                new_complexity = (new_h0 + h1_original) / cluster_count
            else:
                new_complexity = 0.0
            
            new_results.at[idx, 'complexity_gps_aware'] = new_complexity
            
            successful += 1
            
        except Exception as e:
            print(f"Error processing window {row['window_id']}: {e}")
            failed += 1
            continue
    
    print(f"\n✓ Successfully processed: {successful} windows")
    print(f"✗ Failed: {failed} windows")
    
    # Save results
    new_results.to_csv(output_file, index=False)
    print(f"\n✓ Results saved: {output_file}")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)
    
    print("\nOriginal H0 (artifact):")
    print(f"  Mean: {new_results['h0_count'].mean():.1f}")
    print(f"  Std:  {new_results['h0_count'].std():.1f}")
    print(f"  Range: {new_results['h0_count'].min():.0f} - {new_results['h0_count'].max():.0f}")
    
    print("\nGPS-Aware H0 (corrected):")
    valid_mask = new_results['h0_gps_aware'] > 0
    print(f"  Mean: {new_results.loc[valid_mask, 'h0_gps_aware'].mean():.1f}")
    print(f"  Std:  {new_results.loc[valid_mask, 'h0_gps_aware'].std():.1f}")
    print(f"  Range: {new_results.loc[valid_mask, 'h0_gps_aware'].min():.0f} - {new_results.loc[valid_mask, 'h0_gps_aware'].max():.0f}")
    
    print("\nH1 (unchanged):")
    print(f"  Mean: {new_results['h1_count'].mean():.1f}")
    print(f"  Std:  {new_results['h1_count'].std():.1f}")
    print(f"  Range: {new_results['h1_count'].min():.0f} - {new_results['h1_count'].max():.0f}")
    
    return new_results

def main():
    """Main execution"""
    # File paths
    first_half = 'first_half_efficient_results/efficient_comprehensive_analysis.csv'
    second_half = 'second_half_efficient_results/efficient_comprehensive_analysis.csv'
    data_file = 'FieldTest/g2293068_SecondSpectrum_Data copy.txt'
    
    # Load original results
    print("Loading original results...")
    original = load_original_results(first_half, second_half)
    
    # Re-analyze with GPS-aware TDA
    new_results = reanalyze_with_gps_aware_tda(
        original,
        data_file,
        cutoff_distance=1.0,
        output_file='gps_aware_comprehensive_analysis.csv'
    )
    
    print("\n" + "=" * 70)
    print("RE-ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\n✓ New H0 values computed with GPS-aware clustering")
    print("✓ H1 values preserved (already correct)")
    print("✓ Complexity recalculated")
    print("\nNext steps:")
    print("  1. Validate new H0 range (2-22)")
    print("  2. Compare with formation types")
    print("  3. Update documentation")
    print("  4. Proceed with validation studies")

if __name__ == "__main__":
    main()
```

---

## ⏱️ Timeline & Effort

### **Implementation (2-3 hours)**

**Hour 1: Setup**
- Create `compute_gps_aware_h0()` function
- Test on single window
- Verify clustering works correctly
- Check H0 variation

**Hour 2: Integration**
- Create re-analysis script
- Test on 5-10 windows
- Debug any issues
- Validate output format

**Hour 3: Deployment**
- Run on all 216 windows
- Generate comparison statistics
- Create validation plots
- Document results

### **Computation (5 minutes)**

```
216 windows × 0.2s per window = ~43 seconds
+ File I/O overhead = ~2-3 minutes
+ Safety margin = ~5 minutes total
```

---

## 📊 Expected Results

### **New H0 Distribution**

Based on your Phase 5 results:

```
Formation Type    | H0 Range | Interpretation
------------------|----------|------------------
Tight formations  | 2-4      | Two team clusters
Medium spread     | 8-16     | Sub-group formations
Wide spread       | 18-22    | Individual players
```

### **H1 (Unchanged)**

```
H1 Statistics (Should match original):
  Mean: 16.09
  Std:  3.56
  Range: 9-30
  CV:   22.1%
```

### **Complexity Index (Updated)**

```
Old: complexity = (240 + H1) / 240 = 1 + H1/240
New: complexity = (H0 + H1) / cluster_count
     where H0 varies 2-22, cluster_count varies 2-22
```

---

## ✅ Validation Checklist

After re-analysis, verify:

- [ ] **H0 range**: 2-22 (not 240)
- [ ] **H0 variation**: CV > 0% (not zero)
- [ ] **H1 unchanged**: Exact match with original
- [ ] **Tight formations**: H0 = 2-4
- [ ] **Spread formations**: H0 = 18-22
- [ ] **Complexity updated**: Uses new H0
- [ ] **216 windows**: All processed successfully
- [ ] **Team metrics**: Unchanged (spread, distance, area)

---

## 🎯 Alternative: Multi-Scale Analysis (Future)

If you want to demonstrate robustness across temporal scales (good for validation):

### **Phase 2 Extension (Week 3-4)**

```python
# Run analysis at multiple temporal scales
window_sizes = {
    '1-minute': 1500,   # 1 min
    '2-minute': 3000,   # Current
    '5-minute': 7500,   # Standard
    '10-minute': 15000  # Long-term
}

for scale_name, window_size in window_sizes.items():
    run_gps_aware_tda(
        window_size=window_size,
        output_file=f'results_{scale_name}.csv'
    )
```

**Benefits**:
- Shows method works across scales
- Demonstrates robustness
- Great for supplementary materials
- Addresses reviewer concerns

**When to do it**:
- After main re-analysis complete
- During validation phase (Week 3-4)
- For multi-match validation

---

## 📁 Output Files

### **Primary Output**
```
gps_aware_comprehensive_analysis.csv
Columns:
  - window_id
  - start_frame, end_frame
  - start_time, end_time
  - h0_count (original - artifact)
  - h0_gps_aware (NEW - corrected)
  - h1_count (unchanged)
  - cluster_count (NEW - 2-22)
  - complexity_index (original)
  - complexity_gps_aware (NEW - corrected)
  - [all other metrics unchanged]
```

### **Comparison Report**
```
gps_aware_comparison_report.txt
  - Original vs new H0 statistics
  - H1 validation (should match)
  - Complexity comparison
  - Formation type distribution
```

### **Validation Plots**
```
figures/
  - h0_comparison_before_after.png
  - h0_distribution_by_formation.png
  - h1_validation_unchanged.png
  - complexity_recalculation.png
```

---

## 🎓 Documentation Updates Needed

After re-analysis, update these files:

1. **COMPREHENSIVE_SCIENTIFIC_DOCUMENTATION.md**
   - Update H0 statistics (2-22, not 240)
   - Note GPS-aware preprocessing
   - Keep H1 section unchanged

2. **FINAL_SCIENTIFIC_BREAKTHROUGH_SUMMARY.md**
   - Update H0 findings
   - Emphasize H1 as primary
   - Add GPS-aware methodology note

3. **TDA_REVOLUTIONARY_INSIGHTS_SUMMARY.md**
   - Correct H0 interpretation
   - Update complexity formula
   - Validate with new results

4. **ZERO_SUM_GEOMETRIC_ANALYSIS.md**
   - Verify findings still hold
   - May need minor updates if complexity used

---

## 🚀 Ready to Execute?

### **Quick Start Commands**

```bash
# 1. Create the GPS-aware TDA function
# Copy compute_gps_aware_h0() from above

# 2. Create the re-analysis script  
# Copy reanalyze_with_gps_aware_tda() from above

# 3. Run re-analysis
python reanalyze_gps_aware_tda.py

# 4. Validate results
python validate_gps_aware_results.py

# Total time: ~5 minutes
```

---

## 💡 Recommendation Summary

### **DO THIS NOW** ✅
1. Keep 2-minute windows (already computed)
2. Re-compute only H0 with GPS-aware clustering
3. Keep H1 values (already correct)
4. Takes 2-3 hours to implement, 5 min to run
5. Generates corrected comprehensive analysis

### **DO THIS LATER** 📅
1. Multi-scale validation (1min, 2min, 5min, 10min)
2. StatsBomb multi-match validation
3. Cross-league comparison
4. Real-time implementation

### **DON'T DO THIS** ❌
1. Throw away existing work
2. Start from scratch with 5-minute windows
3. Recompute H1 (already correct!)
4. Over-complicate the approach

---

## ✅ Final Answer to Your Questions

**Q: Shall I re-run the sliding window analysis for the whole game(s)?**
**A: YES - but efficiently! Only H0 needs updating (5 minutes total)**

**Q: Shall we still go with the 5-minute rolling window?**
**A: NO - keep 2-minute windows (already computed, good resolution)**

**Bonus: Later run 5-minute as validation (Week 3-4)**

---

**This is a 2-3 hour task, not a multi-day re-computation!** 🎯

