#!/usr/bin/env python3
"""
Test Tactical Cut-off Distances
================================

Tests different tactical cut-off distances to find optimal for single-frame analysis.
Compares 16.31m (validated for temporal windows) vs. lower values.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from multi_goal_analysis import MultiGoalAnalysis
import json
from tqdm import tqdm

def load_sample_frames(n_frames=50):
    """Load sample frames from GPS data"""
    jsonl_file = Path('FieldTest/g2293068_SecondSpectrum_Data.jsonl')
    
    if not jsonl_file.exists():
        return None
    
    positions_list = []
    frame_indices = []
    
    try:
        with open(jsonl_file, 'r') as f:
            for i, line in enumerate(f):
                if i >= n_frames * 100:  # Sample every 100th frame
                    break
                
                if i % 100 != 0:
                    continue
                
                data = json.loads(line)
                all_positions = []
                
                if 'homePlayers' in data:
                    for player in data['homePlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                if 'awayPlayers' in data:
                    for player in data['awayPlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                if len(all_positions) == 22:
                    positions_list.append(np.array(all_positions))
                    frame_indices.append(i)
        
        return positions_list, frame_indices
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_tactical_cutoffs():
    """Test different tactical cut-off distances"""
    print("="*70)
    print("TACTICAL CUT-OFF DISTANCE TESTING")
    print("="*70)
    print()
    
    # Load sample frames
    print("📊 Loading sample frames...")
    data = load_sample_frames(n_frames=50)
    
    if data is None:
        print("❌ Failed to load data")
        return
    
    positions_list, frame_indices = data
    print(f"✅ Loaded {len(positions_list)} frames")
    print()
    
    # Test different cut-off distances
    tactical_cutoffs = [12.0, 13.0, 14.0, 15.0, 16.0, 16.31, 17.0, 18.0]
    
    print("🔬 Testing tactical cut-off distances...")
    print()
    
    results = []
    
    analyzer = MultiGoalAnalysis()
    
    for cutoff in tactical_cutoffs:
        h0_values = []
        valid_count = 0
        
        for positions in positions_list:
            # Compute H0 with this cut-off
            result = analyzer.analyze_single_goal(positions, goal='tactical', cutoff_distance=cutoff)
            h0_values.append(result['h0_count'])
            
            # Check if valid (H0 in range 3-12, but also check if 2 is acceptable)
            if 2 <= result['h0_count'] <= 12:
                valid_count += 1
        
        h0_array = np.array(h0_values)
        
        # Calculate statistics
        stats = {
            'cutoff': cutoff,
            'h0_mean': float(np.mean(h0_array)),
            'h0_std': float(np.std(h0_array)),
            'h0_min': int(np.min(h0_array)),
            'h0_max': int(np.max(h0_array)),
            'valid_strict': int((h0_array >= 3).sum()),  # Strict: 3-12
            'valid_lenient': int((h0_array >= 2).sum()),  # Lenient: 2-12
            'valid_pct_strict': float(100 * (h0_array >= 3).sum() / len(h0_array)),
            'valid_pct_lenient': float(100 * (h0_array >= 2).sum() / len(h0_array)),
            'h0_distribution': {int(h0): int((h0_array == h0).sum()) for h0 in np.unique(h0_array)}
        }
        
        results.append(stats)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    print("="*70)
    print("RESULTS: TACTICAL CUT-OFF TESTING")
    print("="*70)
    print()
    print(f"{'Cut-off':<10} {'H0 Mean':<10} {'H0 Range':<15} {'Valid (3-12)':<15} {'Valid (2-12)':<15}")
    print("-" * 70)
    
    for _, row in results_df.iterrows():
        print(f"{row['cutoff']:<10.2f} {row['h0_mean']:<10.2f} {row['h0_min']}-{row['h0_max']:<12} "
              f"{row['valid_pct_strict']:.1f}% ({row['valid_strict']}/{len(positions_list)})    "
              f"{row['valid_pct_lenient']:.1f}% ({row['valid_lenient']}/{len(positions_list)})")
    
    print()
    print("="*70)
    print("ANALYSIS")
    print("="*70)
    print()
    
    # Find best cut-off
    best_strict = results_df.loc[results_df['valid_pct_strict'].idxmax()]
    best_lenient = results_df.loc[results_df['valid_pct_lenient'].idxmax()]
    
    print(f"📊 BEST CUT-OFF (Strict 3-12 range):")
    print(f"   Cut-off: {best_strict['cutoff']:.2f}m")
    print(f"   Validation: {best_strict['valid_pct_strict']:.1f}%")
    print(f"   H0: {best_strict['h0_mean']:.2f} ± {best_strict['h0_std']:.2f} (range: {best_strict['h0_min']}-{best_strict['h0_max']})")
    print()
    
    print(f"📊 BEST CUT-OFF (Lenient 2-12 range):")
    print(f"   Cut-off: {best_lenient['cutoff']:.2f}m")
    print(f"   Validation: {best_lenient['valid_pct_lenient']:.1f}%")
    print(f"   H0: {best_lenient['h0_mean']:.2f} ± {best_lenient['h0_std']:.2f} (range: {best_lenient['h0_min']}-{best_lenient['h0_max']})")
    print()
    
    # Compare to current (16.31m)
    current = results_df[results_df['cutoff'] == 16.31].iloc[0]
    print(f"📊 CURRENT CUT-OFF (16.31m):")
    print(f"   Validation (strict): {current['valid_pct_strict']:.1f}%")
    print(f"   Validation (lenient): {current['valid_pct_lenient']:.1f}%")
    print(f"   H0: {current['h0_mean']:.2f} ± {current['h0_std']:.2f} (range: {current['h0_min']}-{current['h0_max']})")
    print()
    
    # Save results
    output_dir = Path('tactical_cutoff_test_results')
    output_dir.mkdir(exist_ok=True)
    
    results_df.to_csv(output_dir / 'tactical_cutoff_comparison.csv', index=False)
    
    with open(output_dir / 'tactical_cutoff_analysis.json', 'w') as f:
        json.dump({
            'best_strict': best_strict.to_dict(),
            'best_lenient': best_lenient.to_dict(),
            'current': current.to_dict(),
            'all_results': results_df.to_dict('records')
        }, f, indent=2)
    
    print(f"✅ Results saved to: {output_dir}/")
    print()
    
    # Recommendations
    print("="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print()
    
    if best_strict['valid_pct_strict'] > current['valid_pct_strict']:
        improvement = best_strict['valid_pct_strict'] - current['valid_pct_strict']
        print(f"✅ RECOMMEND: Use {best_strict['cutoff']:.2f}m for single-frame analysis")
        print(f"   Improvement: +{improvement:.1f}% validation rate")
    else:
        print("⚠️ Current 16.31m may be appropriate, but:")
        print("   • Consider if H0=2 is valid for compact formations")
        print("   • May need to adjust expected range to 2-12 for very compact matches")
    
    print()
    print("💡 KEY INSIGHT:")
    print("   • Temporal windows (aggregated): 16.31m optimal")
    print("   • Single frames (instantaneous): May need different cut-off")
    print("   • Consider match-specific formation compactness")
    print()
    
    return results_df


if __name__ == '__main__':
    test_tactical_cutoffs()

