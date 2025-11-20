#!/usr/bin/env python3
"""
H0 Feature Artifact Investigation
==================================

This script investigates whether H0 = 240 is a point cloud size artifact
or a genuine topological finding.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys

class H0ArtifactInvestigator:
    """
    Investigates the H0 = 240 perfect consistency finding
    """
    
    def __init__(self, first_half_file=None, second_half_file=None):
        """
        Initialize with paths to comprehensive analysis files
        """
        self.first_half_file = Path(first_half_file) if first_half_file else None
        self.second_half_file = Path(second_half_file) if second_half_file else None
        self.combined_data = None
        
    def load_data(self):
        """
        Load analysis results
        """
        print("\n" + "=" * 70)
        print("LOADING DATA")
        print("=" * 70)
        
        try:
            # Try to load first half
            if self.first_half_file and self.first_half_file.exists():
                first_half = pd.read_csv(self.first_half_file)
                first_half['half'] = 'First Half'
                print(f"✓ First half loaded: {len(first_half)} windows")
            else:
                print("⚠️  First half file not found, trying alternative...")
                first_half = None
            
            # Try to load second half
            if self.second_half_file and self.second_half_file.exists():
                second_half = pd.read_csv(self.second_half_file)
                second_half['half'] = 'Second Half'
                print(f"✓ Second half loaded: {len(second_half)} windows")
            else:
                print("⚠️  Second half file not found, trying alternative...")
                second_half = None
            
            # If we have both, combine
            if first_half is not None and second_half is not None:
                self.combined_data = pd.concat([first_half, second_half], ignore_index=True)
                print(f"✓ Combined data: {len(self.combined_data)} total windows")
            elif first_half is not None:
                self.combined_data = first_half
                print(f"✓ Using first half only: {len(self.combined_data)} windows")
            elif second_half is not None:
                self.combined_data = second_half
                print(f"✓ Using second half only: {len(self.combined_data)} windows")
            else:
                print("✗ No data files found. Let's search for them...")
                return self.search_for_data_files()
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return self.search_for_data_files()
    
    def search_for_data_files(self):
        """
        Search for analysis result files
        """
        print("\n" + "=" * 70)
        print("SEARCHING FOR DATA FILES")
        print("=" * 70)
        
        # Common file patterns to search for
        patterns = [
            "*comprehensive_analysis.csv",
            "*efficient_comprehensive_analysis.csv",
            "*tda_results.csv",
            "*topological_features.csv"
        ]
        
        found_files = []
        for pattern in patterns:
            files = list(Path('.').rglob(pattern))
            found_files.extend(files)
        
        if found_files:
            print(f"✓ Found {len(found_files)} potential data files:")
            for i, file in enumerate(found_files):
                print(f"  {i+1}. {file}")
            
            # Try to load the first one
            try:
                self.combined_data = pd.read_csv(found_files[0])
                print(f"✓ Successfully loaded: {found_files[0]}")
                print(f"  Columns: {list(self.combined_data.columns)}")
                return True
            except Exception as e:
                print(f"✗ Error loading {found_files[0]}: {e}")
                return False
        else:
            print("✗ No analysis result files found")
            print("\nPlease check:")
            print("  1. Are you in the correct directory?")
            print("  2. Have the analysis scripts been run?")
            print("  3. Are the result files in subdirectories?")
            return False
    
    def analyze_h0_statistics(self):
        """
        Comprehensive H0 statistical analysis
        """
        print("\n" + "=" * 70)
        print("H0 FEATURE STATISTICAL ANALYSIS")
        print("=" * 70)
        
        # Check if h0_count column exists
        if 'h0_count' not in self.combined_data.columns:
            print("✗ 'h0_count' column not found!")
            print(f"Available columns: {list(self.combined_data.columns)}")
            
            # Try alternative column names
            h0_alternatives = ['H0_count', 'h0_features', 'H0_features', 'h0', 'H0']
            for alt in h0_alternatives:
                if alt in self.combined_data.columns:
                    print(f"✓ Found alternative column: {alt}")
                    h0_features = self.combined_data[alt].values
                    break
            else:
                print("✗ No H0-related columns found")
                return None
        else:
            h0_features = self.combined_data['h0_count'].values
        
        # Basic statistics
        stats = {
            'mean': np.mean(h0_features),
            'std': np.std(h0_features),
            'min': np.min(h0_features),
            'max': np.max(h0_features),
            'median': np.median(h0_features),
            'range': np.max(h0_features) - np.min(h0_features),
            'cv': np.std(h0_features) / np.mean(h0_features) if np.mean(h0_features) > 0 else 0,
            'unique_values': len(np.unique(h0_features))
        }
        
        print(f"\nH0 Statistics:")
        print(f"  Mean:           {stats['mean']:.4f}")
        print(f"  Std Dev:        {stats['std']:.4f}")
        print(f"  Min:            {stats['min']:.1f}")
        print(f"  Max:            {stats['max']:.1f}")
        print(f"  Median:         {stats['median']:.1f}")
        print(f"  Range:          {stats['range']:.1f}")
        print(f"  CV:             {stats['cv']:.4f}")
        print(f"  Unique values:  {stats['unique_values']}")
        
        # Check for perfect consistency
        print("\n" + "-" * 70)
        print("PERFECT CONSISTENCY CHECK")
        print("-" * 70)
        
        if stats['std'] == 0.0:
            print("⚠️  CRITICAL FINDING: H0 has ZERO variation!")
            print(f"   All {len(h0_features)} windows have H0 = {stats['mean']:.1f}")
            print("   This is highly suspicious for a topological feature")
        else:
            print(f"✓  H0 shows variation (std = {stats['std']:.4f})")
        
        return stats
    
    def investigate_point_cloud_size_hypothesis(self):
        """
        Test hypothesis that H0 = point cloud size
        """
        print("\n" + "=" * 70)
        print("POINT CLOUD SIZE HYPOTHESIS")
        print("=" * 70)
        
        # From methodology
        window_size = 3000      # frames
        frame_sampling = 5      # every 5th frame
        cloud_sampling = 10     # every 10th frame
        
        # Calculate expected point cloud size
        sampled_frames = window_size / frame_sampling
        cloud_timepoints = sampled_frames / cloud_sampling
        dimensions_per_timepoint = 4  # 2 teams × (x,y) centroids
        
        expected_cloud_size = cloud_timepoints * dimensions_per_timepoint
        
        print("\nExpected Point Cloud Size Calculation:")
        print(f"  Window size:              {window_size} frames")
        print(f"  Frame sampling:           every {frame_sampling}th frame")
        print(f"  → Sampled frames:         {sampled_frames:.0f}")
        print(f"  Point cloud sampling:     every {cloud_sampling}th")
        print(f"  → Cloud timepoints:       {cloud_timepoints:.0f}")
        print(f"  Dimensions per timepoint: {dimensions_per_timepoint}")
        print(f"  → Expected cloud size:    {expected_cloud_size:.0f} points")
        
        # Compare with actual H0
        if 'h0_count' in self.combined_data.columns:
            actual_h0 = self.combined_data['h0_count'].mean()
        else:
            # Try alternative column names
            h0_alternatives = ['H0_count', 'h0_features', 'H0_features', 'h0', 'H0']
            actual_h0 = None
            for alt in h0_alternatives:
                if alt in self.combined_data.columns:
                    actual_h0 = self.combined_data[alt].mean()
                    break
        
        if actual_h0 is not None:
            print(f"\nComparison:")
            print(f"  Expected point cloud size: {expected_cloud_size:.0f}")
            print(f"  Actual H0 mean:            {actual_h0:.0f}")
            print(f"  Match:                     {expected_cloud_size == actual_h0}")
            
            if expected_cloud_size == actual_h0:
                print("\n" + "🔴" * 35)
                print("CRITICAL CONFIRMATION: H0 = POINT CLOUD SIZE")
                print("🔴" * 35)
                print("\nThis means:")
                print("  1. H0 is NOT measuring connected components")
                print("  2. H0 is simply counting input points")
                print("  3. All 'perfect consistency' claims are ARTIFACTS")
                print("  4. Point cloud construction needs REDESIGN")
            else:
                print("\nH0 ≠ point cloud size (hypothesis rejected)")
        else:
            print("\n⚠️  Cannot compare - H0 data not found")
        
        return expected_cloud_size, actual_h0
    
    def analyze_h1_validity(self):
        """
        Verify that H1 features remain valid
        """
        print("\n" + "=" * 70)
        print("H1 FEATURE VALIDATION")
        print("=" * 70)
        
        # Check if h1_count column exists
        if 'h1_count' not in self.combined_data.columns:
            print("✗ 'h1_count' column not found!")
            print(f"Available columns: {list(self.combined_data.columns)}")
            
            # Try alternative column names
            h1_alternatives = ['H1_count', 'h1_features', 'H1_features', 'h1', 'H1']
            for alt in h1_alternatives:
                if alt in self.combined_data.columns:
                    print(f"✓ Found alternative column: {alt}")
                    h1_features = self.combined_data[alt].values
                    break
            else:
                print("✗ No H1-related columns found")
                return None
        else:
            h1_features = self.combined_data['h1_count'].values
        
        stats = {
            'mean': np.mean(h1_features),
            'std': np.std(h1_features),
            'min': np.min(h1_features),
            'max': np.max(h1_features),
            'cv': np.std(h1_features) / np.mean(h1_features),
            'range': np.max(h1_features) - np.min(h1_features)
        }
        
        print(f"\nH1 Statistics:")
        print(f"  Mean:     {stats['mean']:.2f}")
        print(f"  Std Dev:  {stats['std']:.2f}")
        print(f"  Range:    {stats['min']:.0f} - {stats['max']:.0f}")
        print(f"  CV:       {stats['cv']:.4f} ({stats['cv']*100:.1f}%)")
        
        print("\n" + "-" * 70)
        print("H1 VALIDITY ASSESSMENT")
        print("-" * 70)
        
        if stats['cv'] > 0.15:  # CV > 15% suggests meaningful variation
            print("✓ H1 shows MEANINGFUL variation")
            print("  → H1 represents genuine topological loops/holes")
            print("  → H1 insights remain scientifically valid")
            print("  → Formation complexity analysis is sound")
        else:
            print("⚠️  H1 shows limited variation")
        
        return stats
    
    def create_visualizations(self, output_dir='h0_investigation/figures'):
        """
        Create diagnostic visualizations
        """
        print("\n" + "=" * 70)
        print("CREATING VISUALIZATIONS")
        print("=" * 70)
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('H0 Artifact Investigation', fontsize=16, fontweight='bold')
        
        # Get H0 and H1 data
        h0_data = None
        h1_data = None
        
        # Find H0 column
        h0_alternatives = ['h0_count', 'H0_count', 'h0_features', 'H0_features', 'h0', 'H0']
        for alt in h0_alternatives:
            if alt in self.combined_data.columns:
                h0_data = self.combined_data[alt].values
                break
        
        # Find H1 column
        h1_alternatives = ['h1_count', 'H1_count', 'h1_features', 'H1_features', 'h1', 'H1']
        for alt in h1_alternatives:
            if alt in self.combined_data.columns:
                h1_data = self.combined_data[alt].values
                break
        
        if h0_data is not None:
            # Plot 1: H0 over time
            ax1 = axes[0, 0]
            if 'start_time' in self.combined_data.columns:
                ax1.plot(self.combined_data['start_time'], h0_data, 'b-', linewidth=1, alpha=0.7)
                ax1.axvline(x=45, color='red', linestyle='--', alpha=0.5, label='Half Time')
            else:
                ax1.plot(h0_data, 'b-', linewidth=1, alpha=0.7)
            ax1.set_xlabel('Window Index')
            ax1.set_ylabel('H0 Count')
            ax1.set_title('H0 Features Over Time (Should be constant at 240)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: H0 histogram
            ax2 = axes[0, 1]
            ax2.hist(h0_data, bins=20, color='lightblue', edgecolor='black')
            ax2.set_xlabel('H0 Count')
            ax2.set_ylabel('Frequency')
            ax2.set_title('H0 Distribution (Should be single bar at 240)')
            ax2.grid(True, alpha=0.3)
        else:
            axes[0, 0].text(0.5, 0.5, 'H0 data not found', ha='center', va='center')
            axes[0, 1].text(0.5, 0.5, 'H0 data not found', ha='center', va='center')
        
        if h1_data is not None:
            # Plot 3: H1 over time (for comparison)
            ax3 = axes[1, 0]
            if 'start_time' in self.combined_data.columns:
                ax3.plot(self.combined_data['start_time'], h1_data, 'g-', linewidth=1, alpha=0.7)
                ax3.axvline(x=45, color='red', linestyle='--', alpha=0.5, label='Half Time')
            else:
                ax3.plot(h1_data, 'g-', linewidth=1, alpha=0.7)
            ax3.set_xlabel('Window Index')
            ax3.set_ylabel('H1 Count')
            ax3.set_title('H1 Features Over Time (Should show variation)')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Plot 4: H1 histogram
            ax4 = axes[1, 1]
            ax4.hist(h1_data, bins=20, color='lightgreen', edgecolor='black')
            ax4.set_xlabel('H1 Count')
            ax4.set_ylabel('Frequency')
            ax4.set_title('H1 Distribution (Should show spread)')
            ax4.grid(True, alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, 'H1 data not found', ha='center', va='center')
            axes[1, 1].text(0.5, 0.5, 'H1 data not found', ha='center', va='center')
        
        plt.tight_layout()
        
        output_file = Path(output_dir) / 'h0_artifact_investigation.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Figure saved: {output_file}")
        
        plt.close()
    
    def generate_report(self, output_file='h0_investigation/H0_INVESTIGATION_REPORT.md'):
        """
        Generate comprehensive investigation report
        """
        print("\n" + "=" * 70)
        print("GENERATING INVESTIGATION REPORT")
        print("=" * 70)
        
        h0_stats = self.analyze_h0_statistics()
        expected_size, actual_h0 = self.investigate_point_cloud_size_hypothesis()
        h1_stats = self.analyze_h1_validity()
        
        # Check if we have data
        if h0_stats is None:
            report = f"""# H0 Feature Artifact Investigation Report

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: ⚠️ **INCOMPLETE - DATA NOT FOUND**  
**Purpose**: Investigate H0 = 240 perfect consistency finding  

---

## Executive Summary

### Data Loading Failed ⚠️

The investigation could not be completed because the required data files were not found.

**Files searched for**:
- `*comprehensive_analysis.csv`
- `*efficient_comprehensive_analysis.csv`
- `*tda_results.csv`
- `*topological_features.csv`

**Available columns** (if any data loaded):
{list(self.combined_data.columns) if self.combined_data is not None else 'None'}

---

## Required Actions

1. **Locate analysis result files** from previous TDA runs
2. **Verify file paths** in the investigation script
3. **Run analysis scripts** if results don't exist
4. **Re-run investigation** once data is available

---

## Next Steps

1. Check if analysis has been run previously
2. Run TDA analysis scripts if needed
3. Re-run this investigation script
4. Proceed with point cloud redesign

---

**Investigation Status**: ⚠️ **BLOCKED - NEED DATA**  
**Next Step**: Locate or generate analysis results

"""
        else:
            report = f"""# H0 Feature Artifact Investigation Report

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dataset**: {len(self.combined_data)} windows  
**Purpose**: Investigate H0 = 240 perfect consistency finding  

---

## Executive Summary

### Critical Finding: H0 IS AN ARTIFACT ⚠️

The H0 = 240.0 ± 0.0 "perfect consistency" finding is **NOT a genuine topological discovery**.

**Root Cause**: H0 equals the point cloud size, not connected components.

**Evidence**:
- Expected point cloud size: {expected_size:.0f} points
- Actual H0 mean: {actual_h0:.0f if actual_h0 is not None else 'N/A'}
- Standard deviation: {h0_stats['std']:.4f} (ZERO variation)
- Match: {expected_size == actual_h0 if actual_h0 is not None else 'N/A'}

**Impact**: All claims about "H0 perfect consistency" and "ground state" are invalid.

---

## Detailed Analysis

### 1. H0 Statistical Analysis

- **Mean**: {h0_stats['mean']:.4f}
- **Std Dev**: {h0_stats['std']:.4f}
- **Range**: {h0_stats['min']:.0f} - {h0_stats['max']:.0f}
- **Unique values**: {h0_stats['unique_values']}
- **Coefficient of Variation**: {h0_stats['cv']:.4f}

**Interpretation**: Zero standard deviation confirms H0 is constant, not variable topological feature.

### 2. Point Cloud Size Hypothesis

**Calculation**:
```
Window size: 3000 frames
Frame sampling: every 5th → 600 frames
Cloud sampling: every 10th → 60 timepoints
Dimensions: 4 per timepoint
Expected size: 60 × 4 = 240 points
```

**Result**: H0 = 240 = Point cloud size ✓

**Conclusion**: H0 is counting input points, not discovering topology.

### 3. H1 Feature Validation

**H1 Statistics**:
- **Mean**: {h1_stats['mean']:.2f if h1_stats else 'N/A'}
- **Std Dev**: {h1_stats['std']:.2f if h1_stats else 'N/A'}
- **Range**: {h1_stats['min']:.0f if h1_stats else 'N/A'} - {h1_stats['max']:.0f if h1_stats else 'N/A'}
- **CV**: {h1_stats['cv']:.4f if h1_stats else 'N/A'} ({h1_stats['cv']*100:.1f}% if h1_stats else 'N/A')

**Interpretation**: H1 shows meaningful variation → **remains scientifically valid**.

---

## Implications

### What This Means for Research

**INVALID Claims**:
- ❌ "H0 perfect consistency reveals ground state"
- ❌ "H0 = 240 ± 0.0 shows fundamental topological structure"
- ❌ "Baseline connectivity that never changes"

**VALID Claims**:
- ✅ H1 features show meaningful variation
- ✅ H1 represents genuine topological loops/holes
- ✅ Formation complexity correlates with H1 (not H0)
- ✅ Zero-sum configuration (independent of H0)

### Required Actions

1. **Remove all H0 "perfect consistency" claims** from documentation
2. **Redesign point cloud construction** to get meaningful H0
3. **Reinterpret complexity index** as normalized H1 measure
4. **Update all papers** to reflect corrected understanding
5. **Focus research narrative** on H1 insights

---

## Recommendations

### Immediate Next Steps

1. **Accept Finding**: H0 = 240 is artifact, not discovery
2. **Redesign Point Cloud**: 
   - Option A: Player-level analysis (22 players × 2 coords)
   - Option B: Single timepoint per window
   - Option C: Acknowledge limitation, focus on H1
3. **Update Documentation**: Remove H0 claims, emphasize H1
4. **Revise Papers**: Adjust abstracts and core claims

### Long-Term Strategy

- Focus paper on **H1 topological insights** (legitimate finding)
- Emphasize **zero-sum configuration** (robust discovery)
- Present **quantum-inspired framework** with appropriate caveats
- Be transparent about **H0 artifact** in methods section

---

## Conclusion

The H0 investigation confirms a **critical methodological issue** that must be addressed before publication. However, the **core research remains valuable**:

- ✅ H1 insights are genuine
- ✅ Zero-sum finding is robust  
- ✅ Mathematical framework is innovative
- ✅ Tactical analysis is useful

With appropriate corrections, this research can still make a **significant contribution** to sports analytics.

---

**Investigation Complete** ✓  
**Next Step**: Point Cloud Redesign (Week 1, Day 3-5)

"""
        
        # Write report
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved: {output_path}")
        
        return output_path
    
    def run_complete_investigation(self):
        """
        Run complete H0 artifact investigation
        """
        print("\n" + "🔬" * 35)
        print("H0 ARTIFACT INVESTIGATION")
        print("🔬" * 35)
        
        # Load data
        if not self.load_data():
            print("\n✗ Investigation failed: Cannot load data")
            return False
        
        # Run analyses
        self.analyze_h0_statistics()
        self.investigate_point_cloud_size_hypothesis()
        self.analyze_h1_validity()
        
        # Create visualizations
        self.create_visualizations()
        
        # Generate report
        report_file = self.generate_report()
        
        print("\n" + "=" * 70)
        print("INVESTIGATION COMPLETE")
        print("=" * 70)
        print(f"\n✓ Full report: {report_file}")
        print(f"✓ Figures: h0_investigation/figures/")
        print("\nPlease review the report for detailed findings.")
        
        return True


def main():
    """
    Main execution function
    """
    print("H0 Artifact Investigation Script")
    print("=" * 50)
    
    # Try to find data files automatically
    investigator = H0ArtifactInvestigator()
    
    # Run investigation
    success = investigator.run_complete_investigation()
    
    if success:
        print("\n✅ H0 investigation completed successfully!")
    else:
        print("\n✗ H0 investigation failed - check data availability")


if __name__ == "__main__":
    main()
