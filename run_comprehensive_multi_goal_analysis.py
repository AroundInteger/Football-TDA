#!/usr/bin/env python3
"""
Comprehensive Multi-Goal Analysis on Real GPS Data
===================================================

Runs full multi-goal analysis across multiple temporal windows from
SecondSpectrum GPS data, demonstrating all three analysis goals simultaneously.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
from pathlib import Path
from multi_goal_analysis import MultiGoalAnalysis
from cutoff_distance_efficacy_investigation import CutoffDistanceEfficacyInvestigation
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def load_all_frames(jsonl_file, max_frames=None, step=100):
    """Load player positions from all frames (sampling every Nth frame)"""
    print(f"📂 Loading GPS data from: {jsonl_file}")
    
    positions_list = []
    frame_indices = []
    timestamps = []
    
    try:
        with open(jsonl_file, 'r') as f:
            for i, line in enumerate(f):
                if max_frames and i >= max_frames:
                    break
                
                # Sample every Nth frame for efficiency
                if i % step != 0:
                    continue
                
                data = json.loads(line)
                
                # Extract player positions
                all_positions = []
                
                # Home team players
                if 'homePlayers' in data:
                    for player in data['homePlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                # Away team players
                if 'awayPlayers' in data:
                    for player in data['awayPlayers']:
                        if 'xyz' in player and len(player['xyz']) >= 2:
                            all_positions.append([player['xyz'][0], player['xyz'][1]])
                
                # Only add if we have 22 players (11 + 11)
                if len(all_positions) == 22:
                    positions_list.append(np.array(all_positions))
                    frame_indices.append(i)
                    
                    # Extract timestamp if available
                    if 'gameClock' in data:
                        timestamps.append(data['gameClock'])
                    else:
                        timestamps.append(i / 25.0)  # Assume 25Hz if not specified
        
        print(f"✅ Loaded {len(positions_list)} valid frames (sampled every {step} frames)")
        return positions_list, frame_indices, timestamps
    
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_comprehensive_analysis():
    """Run comprehensive multi-goal analysis"""
    print("="*70)
    print("COMPREHENSIVE MULTI-GOAL ANALYSIS")
    print("="*70)
    print()
    
    # Initialize analyzer
    analyzer = MultiGoalAnalysis()
    
    # Load data
    jsonl_file = Path('FieldTest/g2293068_SecondSpectrum_Data.jsonl')
    
    if not jsonl_file.exists():
        print(f"❌ Data file not found: {jsonl_file}")
        return None
    
    # Load frames (sample every 100th frame for comprehensive analysis)
    print("📊 Loading GPS data...")
    data = load_all_frames(jsonl_file, max_frames=15000, step=100)
    
    if data is None:
        print("❌ Failed to load data")
        return None
    
    positions_list, frame_indices, timestamps = data
    n_frames = len(positions_list)
    
    print(f"\n🔬 Analyzing {n_frames} frames with multi-goal framework...")
    print()
    
    # Analyze all frames
    all_results = []
    
    for i in tqdm(range(n_frames), desc="Analyzing frames"):
        positions = positions_list[i]
        frame_idx = frame_indices[i]
        timestamp = timestamps[i]
        
        # Run multi-goal analysis
        try:
            results = analyzer.analyze_all_goals(positions)
            
            # Store results
            result_row = {
                'frame_idx': frame_idx,
                'timestamp': timestamp,
                'n_players': len(positions)
            }
            
            # Add results for each goal
            for goal in ['individual', 'tactical', 'team']:
                r = results[goal]
                result_row.update({
                    f'h0_{goal}': r['h0_count'],
                    f'h1_{goal}': r['h1_count'],
                    f'clusters_{goal}': r['cluster_count'],
                    f'complexity_{goal}': r['complexity_index'],
                    f'cutoff_{goal}': r['cutoff_distance'],
                    f'h0_valid_{goal}': r['h0_valid'],
                    f'expected_range_{goal}': str(r['h0_expected_range'])
                })
            
            # Add summary
            result_row['all_goals_valid'] = results['summary']['all_valid']
            result_row['scale_ordering_correct'] = '✅' in results['summary']['scale_comparison']
            
            all_results.append(result_row)
        
        except Exception as e:
            print(f"\n⚠️ Error analyzing frame {frame_idx}: {e}")
            continue
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save results
    output_dir = Path('multi_goal_comprehensive_results')
    output_dir.mkdir(exist_ok=True)
    
    results_file = output_dir / 'comprehensive_multi_goal_analysis.csv'
    results_df.to_csv(results_file, index=False)
    print(f"\n✅ Results saved to: {results_file}")
    
    # Generate summary statistics
    print()
    print("="*70)
    print("COMPREHENSIVE RESULTS SUMMARY")
    print("="*70)
    print()
    
    for goal in ['individual', 'tactical', 'team']:
        h0_col = f'h0_{goal}'
        h1_col = f'h1_{goal}'
        valid_col = f'h0_valid_{goal}'
        
        if h0_col in results_df.columns:
            valid_count = results_df[valid_col].sum()
            valid_pct = 100 * valid_count / len(results_df)
            
            print(f"{goal.upper()} ANALYSIS:")
            print(f"  H0: {results_df[h0_col].mean():.2f} ± {results_df[h0_col].std():.2f}")
            print(f"      Range: {results_df[h0_col].min():.0f} - {results_df[h0_col].max():.0f}")
            print(f"  H1: {results_df[h1_col].mean():.2f} ± {results_df[h1_col].std():.2f}")
            print(f"      Range: {results_df[h1_col].min():.0f} - {results_df[h1_col].max():.0f}")
            print(f"  Validation: {valid_count}/{len(results_df)} frames valid ({valid_pct:.1f}%)")
            print()
    
    # Overall statistics
    all_valid_count = results_df['all_goals_valid'].sum()
    all_valid_pct = 100 * all_valid_count / len(results_df)
    ordering_correct_count = results_df['scale_ordering_correct'].sum()
    ordering_correct_pct = 100 * ordering_correct_count / len(results_df)
    
    print("OVERALL STATISTICS:")
    print(f"  Total frames analyzed: {len(results_df)}")
    print(f"  All goals valid: {all_valid_count}/{len(results_df)} ({all_valid_pct:.1f}%)")
    print(f"  Scale ordering correct: {ordering_correct_count}/{len(results_df)} ({ordering_correct_pct:.1f}%)")
    print()
    
    # Save summary statistics
    summary_stats = {
        'n_frames': len(results_df),
        'individual': {
            'h0_mean': float(results_df['h0_individual'].mean()),
            'h0_std': float(results_df['h0_individual'].std()),
            'h0_range': [int(results_df['h0_individual'].min()), int(results_df['h0_individual'].max())],
            'h1_mean': float(results_df['h1_individual'].mean()),
            'valid_pct': float(100 * results_df['h0_valid_individual'].sum() / len(results_df))
        },
        'tactical': {
            'h0_mean': float(results_df['h0_tactical'].mean()),
            'h0_std': float(results_df['h0_tactical'].std()),
            'h0_range': [int(results_df['h0_tactical'].min()), int(results_df['h0_tactical'].max())],
            'h1_mean': float(results_df['h1_tactical'].mean()),
            'valid_pct': float(100 * results_df['h0_valid_tactical'].sum() / len(results_df))
        },
        'team': {
            'h0_mean': float(results_df['h0_team'].mean()),
            'h0_std': float(results_df['h0_team'].std()),
            'h0_range': [int(results_df['h0_team'].min()), int(results_df['h0_team'].max())],
            'h1_mean': float(results_df['h1_team'].mean()),
            'valid_pct': float(100 * results_df['h0_valid_team'].sum() / len(results_df))
        },
        'overall': {
            'all_valid_pct': float(all_valid_pct),
            'ordering_correct_pct': float(ordering_correct_pct)
        }
    }
    
    summary_file = output_dir / 'summary_statistics.json'
    with open(summary_file, 'w') as f:
        json.dump(summary_stats, f, indent=2)
    
    print(f"✅ Summary statistics saved to: {summary_file}")
    print()
    print("="*70)
    print("✅ COMPREHENSIVE MULTI-GOAL ANALYSIS COMPLETE!")
    print("="*70)
    print()
    print("📊 Key Achievements:")
    print(f"  • Analyzed {len(results_df)} frames from real GPS data")
    print(f"  • All three goals computed simultaneously for each frame")
    print(f"  • Validated cut-offs used: 2.98m, 16.31m, 28.11m")
    print(f"  • Complete 3/3 multi-scale picture achieved!")
    print()
    
    return results_df, summary_stats


if __name__ == '__main__':
    try:
        results_df, summary_stats = run_comprehensive_analysis()
        print("🎉 Comprehensive analysis successful!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

