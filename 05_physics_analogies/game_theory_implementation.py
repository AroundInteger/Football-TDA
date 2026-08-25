#!/usr/bin/env python3
"""
Game Theory Implementation: Zero-Sum Configuration and p-adic Extensions
=====================================================================

This script implements game theory analysis of our zero-sum geometric configuration,
including classical game theory, p-adic extensions, and competitive measurement.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
from scipy.optimize import minimize
from scipy.stats import entropy
import json
warnings.filterwarnings('ignore')

class GameTheoryAnalyzer:
    """
    Analyzes football team dynamics through game theory frameworks
    """
    
    def __init__(self, first_half_dir='first_half_efficient_results', 
                 second_half_dir='second_half_efficient_results'):
        """
        Initialize the game theory analyzer
        
        Args:
            first_half_dir (str): Directory containing first half TDA results
            second_half_dir (str): Directory containing second half TDA results
        """
        self.first_half_dir = Path(first_half_dir)
        self.second_half_dir = Path(second_half_dir)
        
        self.combined_data = None
        self.game_theory_results = {}
        
        print(f"GameTheoryAnalyzer initialized")
        print(f"  First half TDA: {self.first_half_dir}")
        print(f"  Second half TDA: {self.second_half_dir}")
    
    def load_data(self):
        """
        Load TDA analysis data
        """
        print("\n=== Loading TDA Data for Game Theory Analysis ===")
        
        # Load first half data
        first_half_file = self.first_half_dir / 'efficient_comprehensive_analysis.csv'
        if first_half_file.exists():
            first_half_data = pd.read_csv(first_half_file)
            first_half_data['half'] = 'First Half'
            print(f"✓ Loaded first half data: {len(first_half_data)} windows")
        else:
            print(f"✗ First half data not found: {first_half_file}")
            return False
        
        # Load second half data
        second_half_file = self.second_half_dir / 'efficient_comprehensive_analysis.csv'
        if second_half_file.exists():
            second_half_data = pd.read_csv(second_half_file)
            second_half_data['half'] = 'Second Half'
            print(f"✓ Loaded second half data: {len(second_half_data)} windows")
        else:
            print(f"✗ Second half data not found: {second_half_file}")
            return False
        
        # Combine data
        self.combined_data = pd.concat([first_half_data, second_half_data], 
                                     ignore_index=True)
        self.combined_data = self.combined_data.sort_values('start_time')
        
        print(f"✓ Combined data: {len(self.combined_data)} total windows")
        print(f"  Time range: {self.combined_data['start_time'].min():.1f} - {self.combined_data['end_time'].max():.1f} minutes")
        
        return True
    
    def analyze_zero_sum_game(self):
        """
        Analyze the zero-sum game structure
        """
        print("\n=== Analyzing Zero-Sum Game Structure ===")
        
        # Extract team metrics
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        
        # Calculate game theory metrics
        total_spread = home_spread + away_spread
        spread_ratio = home_spread / away_spread
        
        # Nash Equilibrium analysis
        nash_home = np.mean(home_spread)
        nash_away = np.mean(away_spread)
        nash_total = nash_home + nash_away
        
        # Competitive balance
        balance = 1 - np.abs(home_spread - away_spread) / (home_spread + away_spread)
        mean_balance = np.mean(balance)
        
        # Payoff analysis (assuming tactical advantage)
        home_advantage = (home_spread - nash_home) / nash_home
        away_advantage = (away_spread - nash_away) / nash_away
        
        # Zero-sum verification
        total_advantage = home_advantage + away_advantage
        zero_sum_strength = -np.corrcoef(home_spread, away_spread)[0, 1]
        
        print(f"Zero-Sum Game Analysis:")
        print(f"  Nash Equilibrium:")
        print(f"    Home Strategy: {nash_home:.3f} meters")
        print(f"    Away Strategy: {nash_away:.3f} meters")
        print(f"    Total Strategy: {nash_total:.3f} meters")
        print(f"  Competitive Balance: {mean_balance:.3f} ({mean_balance*100:.1f}%)")
        print(f"  Zero-Sum Strength: {zero_sum_strength:.3f}")
        print(f"  Total Advantage Correlation: {np.corrcoef(home_advantage, away_advantage)[0, 1]:.3f}")
        
        return {
            'nash_home': nash_home,
            'nash_away': nash_away,
            'nash_total': nash_total,
            'mean_balance': mean_balance,
            'zero_sum_strength': zero_sum_strength,
            'home_advantage': home_advantage,
            'away_advantage': away_advantage,
            'total_advantage': total_advantage
        }
    
    def p_adic_valuation(self, x, p):
        """
        Calculate p-adic valuation of x
        
        Args:
            x (float): Number to evaluate
            p (int): Prime number
            
        Returns:
            int: p-adic valuation
        """
        if x == 0:
            return float('inf')
        
        # Convert to integer representation for p-adic analysis
        x_int = int(abs(x) * 1000)  # Scale to avoid floating point issues
        
        valuation = 0
        while x_int % p == 0 and x_int != 0:
            x_int //= p
            valuation += 1
        
        return valuation
    
    def p_adic_norm(self, x, p):
        """
        Calculate p-adic norm of x
        
        Args:
            x (float): Number to evaluate
            p (int): Prime number
            
        Returns:
            float: p-adic norm
        """
        valuation = self.p_adic_valuation(x, p)
        if valuation == float('inf'):
            return 0
        return p ** (-valuation)
    
    def analyze_p_adic_competition(self):
        """
        Analyze competition using p-adic frameworks
        """
        print("\n=== Analyzing p-adic Competition ===")
        
        # Extract team metrics
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        inter_team_distance = self.combined_data['avg_inter_team_distance'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread) | np.isnan(inter_team_distance))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        inter_team_distance = inter_team_distance[valid_mask]
        
        # Calculate competitive differences
        spread_difference = home_spread - away_spread
        distance_variation = inter_team_distance - np.mean(inter_team_distance)
        
        # p-adic analysis for different primes
        primes = [2, 3, 5, 7, 11]
        p_adic_results = {}
        
        for p in primes:
            # p-adic norms of competitive differences
            spread_diff_norm = [self.p_adic_norm(diff, p) for diff in spread_difference]
            distance_var_norm = [self.p_adic_norm(var, p) for var in distance_variation]
            
            # p-adic competitive distance
            p_adic_distance = [self.p_adic_norm(abs(home_spread[i] - away_spread[i]), p) 
                             for i in range(len(home_spread))]
            
            # p-adic balance
            p_adic_balance = [1 - self.p_adic_norm(abs(home_spread[i] - away_spread[i]), p) 
                            for i in range(len(home_spread))]
            
            p_adic_results[p] = {
                'spread_diff_norm': np.mean(spread_diff_norm),
                'distance_var_norm': np.mean(distance_var_norm),
                'p_adic_distance': np.mean(p_adic_distance),
                'p_adic_balance': np.mean(p_adic_balance)
            }
            
            print(f"  p = {p}:")
            print(f"    Spread Difference Norm: {np.mean(spread_diff_norm):.6f}")
            print(f"    Distance Variation Norm: {np.mean(distance_var_norm):.6f}")
            print(f"    p-adic Distance: {np.mean(p_adic_distance):.6f}")
            print(f"    p-adic Balance: {np.mean(p_adic_balance):.6f}")
        
        return p_adic_results
    
    def analyze_quantum_game_theory(self):
        """
        Analyze quantum game theory aspects
        """
        print("\n=== Analyzing Quantum Game Theory ===")
        
        # Load quantum analysis results if available
        quantum_file = Path('quantum_dot_full_match_results.json')
        if quantum_file.exists():
            with open(quantum_file, 'r') as f:
                quantum_data = json.load(f)
            
            # Extract quantum states and their properties
            quantum_states = quantum_data.get('quantum_analysis', {})
            energy_levels = quantum_states.get('energy_levels', [])
            quantum_yields = quantum_states.get('quantum_yields', [])
            coherence_values = quantum_states.get('coherence_values', [])
            
            # Calculate quantum game theory metrics
            n_states = len(energy_levels)
            state_frequencies = quantum_states.get('state_frequencies', [])
            
            # Quantum entropy (information content)
            if state_frequencies:
                # Normalize frequencies to probabilities
                total_freq = sum(state_frequencies)
                probabilities = [freq / total_freq for freq in state_frequencies]
                quantum_entropy = entropy(probabilities, base=2)
            else:
                quantum_entropy = 0
            
            # Quantum competitive advantage
            quantum_advantage = []
            for i in range(n_states):
                if i < len(quantum_yields) and i < len(coherence_values):
                    advantage = quantum_yields[i] * coherence_values[i]
                    quantum_advantage.append(advantage)
            
            # Quantum Nash equilibrium (state with highest advantage)
            if quantum_advantage:
                optimal_state = np.argmax(quantum_advantage)
                optimal_advantage = max(quantum_advantage)
            else:
                optimal_state = 0
                optimal_advantage = 0
            
            print(f"Quantum Game Theory Analysis:")
            print(f"  Number of Quantum States: {n_states}")
            print(f"  Quantum Entropy: {quantum_entropy:.3f} bits")
            print(f"  Optimal Quantum State: {optimal_state}")
            print(f"  Optimal Quantum Advantage: {optimal_advantage:.3f}")
            print(f"  Energy Level Range: {min(energy_levels):.3f} - {max(energy_levels):.3f}")
            print(f"  Quantum Yield Range: {min(quantum_yields):.3f} - {max(quantum_yields):.3f}")
            print(f"  Coherence Range: {min(coherence_values):.3f} - {max(coherence_values):.3f}")
            
            return {
                'n_states': n_states,
                'quantum_entropy': quantum_entropy,
                'optimal_state': optimal_state,
                'optimal_advantage': optimal_advantage,
                'energy_levels': energy_levels,
                'quantum_yields': quantum_yields,
                'coherence_values': coherence_values,
                'quantum_advantage': quantum_advantage
            }
        else:
            print("  Quantum analysis results not found. Skipping quantum game theory analysis.")
            return None
    
    def analyze_competitive_measurement(self):
        """
        Analyze competitive measurement frameworks
        """
        print("\n=== Analyzing Competitive Measurement ===")
        
        # Extract competitive metrics
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        inter_team_distance = self.combined_data['avg_inter_team_distance'].values
        team_area_ratio = self.combined_data['avg_team_area_ratio'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread) | 
                      np.isnan(inter_team_distance) | np.isnan(team_area_ratio))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        inter_team_distance = inter_team_distance[valid_mask]
        team_area_ratio = team_area_ratio[valid_mask]
        
        # Multi-dimensional competitive space
        competitive_space = np.column_stack([
            home_spread, away_spread, inter_team_distance, team_area_ratio
        ])
        
        # Competitive advantage metrics
        spread_advantage = (home_spread - away_spread) / (home_spread + away_spread)
        distance_advantage = (inter_team_distance - np.mean(inter_team_distance)) / np.std(inter_team_distance)
        area_advantage = (team_area_ratio - 1.0) / np.std(team_area_ratio)
        
        # Combined competitive advantage
        combined_advantage = (spread_advantage + distance_advantage + area_advantage) / 3
        
        # Competitive balance metrics
        classical_balance = 1 - np.abs(home_spread - away_spread) / (home_spread + away_spread)
        distance_balance = 1 - np.abs(distance_advantage)
        area_balance = 1 - np.abs(area_advantage)
        
        # Overall competitive balance
        overall_balance = (classical_balance + distance_balance + area_balance) / 3
        
        # Competitive stability (variance of competitive metrics)
        competitive_stability = 1 / (1 + np.var(combined_advantage))
        
        print(f"Competitive Measurement Analysis:")
        print(f"  Multi-dimensional Competitive Space: {competitive_space.shape}")
        print(f"  Mean Spread Advantage: {np.mean(spread_advantage):.3f}")
        print(f"  Mean Distance Advantage: {np.mean(distance_advantage):.3f}")
        print(f"  Mean Area Advantage: {np.mean(area_advantage):.3f}")
        print(f"  Mean Combined Advantage: {np.mean(combined_advantage):.3f}")
        print(f"  Mean Overall Balance: {np.mean(overall_balance):.3f}")
        print(f"  Competitive Stability: {competitive_stability:.3f}")
        
        return {
            'competitive_space': competitive_space,
            'spread_advantage': spread_advantage,
            'distance_advantage': distance_advantage,
            'area_advantage': area_advantage,
            'combined_advantage': combined_advantage,
            'overall_balance': overall_balance,
            'competitive_stability': competitive_stability
        }
    
    def create_game_theory_visualization(self):
        """
        Create comprehensive game theory visualization
        """
        print("\n=== Creating Game Theory Visualization ===")
        
        # Extract data for visualization
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Game Theory Analysis: Zero-Sum Configuration and p-adic Extensions', 
                     fontsize=16, fontweight='bold')
        
        # Plot 1: Zero-Sum Game Structure
        ax1 = axes[0, 0]
        ax1.scatter(home_spread, away_spread, alpha=0.6, s=20, color='blue')
        
        # Add Nash equilibrium point
        nash_home = np.mean(home_spread)
        nash_away = np.mean(away_spread)
        ax1.scatter(nash_home, nash_away, s=100, color='red', marker='*', 
                   label=f'Nash Equilibrium ({nash_home:.2f}, {nash_away:.2f})')
        
        # Add conservation constraint line
        total_spread = nash_home + nash_away
        x_line = np.linspace(min(home_spread), max(home_spread), 100)
        y_line = total_spread - x_line
        ax1.plot(x_line, y_line, 'r--', alpha=0.7, label=f'Conservation: x + y = {total_spread:.2f}')
        
        ax1.set_xlabel('Home Team Spread (m)')
        ax1.set_ylabel('Away Team Spread (m)')
        ax1.set_title('Zero-Sum Game Structure')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Competitive Balance
        ax2 = axes[0, 1]
        balance = 1 - np.abs(home_spread - away_spread) / (home_spread + away_spread)
        ax2.hist(balance, bins=30, alpha=0.7, color='green', edgecolor='black')
        ax2.axvline(np.mean(balance), color='red', linestyle='--', 
                   label=f'Mean Balance: {np.mean(balance):.3f}')
        ax2.set_xlabel('Competitive Balance')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Competitive Balance Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: p-adic Analysis
        ax3 = axes[0, 2]
        primes = [2, 3, 5, 7, 11]
        p_adic_balances = []
        
        for p in primes:
            p_adic_balance = [1 - self.p_adic_norm(abs(home_spread[i] - away_spread[i]), p) 
                            for i in range(len(home_spread))]
            p_adic_balances.append(np.mean(p_adic_balance))
        
        ax3.bar(primes, p_adic_balances, alpha=0.7, color='purple')
        ax3.set_xlabel('Prime p')
        ax3.set_ylabel('p-adic Balance')
        ax3.set_title('p-adic Competitive Balance')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Competitive Advantage Evolution
        ax4 = axes[1, 0]
        time_points = np.arange(len(home_spread))
        spread_advantage = (home_spread - away_spread) / (home_spread + away_spread)
        ax4.plot(time_points, spread_advantage, alpha=0.7, color='orange')
        ax4.axhline(0, color='black', linestyle='--', alpha=0.5)
        ax4.set_xlabel('Time (windows)')
        ax4.set_ylabel('Spread Advantage')
        ax4.set_title('Competitive Advantage Evolution')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Multi-dimensional Competitive Space
        ax5 = axes[1, 1]
        inter_team_distance = self.combined_data['avg_inter_team_distance'].values[valid_mask]
        team_area_ratio = self.combined_data['avg_team_area_ratio'].values[valid_mask]
        
        scatter = ax5.scatter(home_spread, away_spread, c=inter_team_distance, 
                            cmap='viridis', alpha=0.6, s=20)
        ax5.set_xlabel('Home Team Spread (m)')
        ax5.set_ylabel('Away Team Spread (m)')
        ax5.set_title('Multi-dimensional Competitive Space')
        plt.colorbar(scatter, ax=ax5, label='Inter-team Distance (m)')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Game Theory Summary
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        # Calculate summary statistics
        zero_sum_strength = -np.corrcoef(home_spread, away_spread)[0, 1]
        mean_balance = np.mean(balance)
        competitive_stability = 1 / (1 + np.var(spread_advantage))
        
        summary_text = f"""
Game Theory Summary:

Zero-Sum Game:
• Nash Equilibrium: ({nash_home:.2f}, {nash_away:.2f})
• Zero-Sum Strength: {zero_sum_strength:.3f}
• Conservation Total: {total_spread:.2f}m

Competitive Balance:
• Mean Balance: {mean_balance:.3f}
• Balance Range: {np.min(balance):.3f} - {np.max(balance):.3f}
• Stability Index: {competitive_stability:.3f}

p-adic Analysis:
• Best p-adic Balance: p={primes[np.argmax(p_adic_balances)]}
• p-adic Balance: {max(p_adic_balances):.3f}
• Competitive Entropy: {entropy([f/sum(p_adic_balances) for f in p_adic_balances]):.3f}
        """
        
        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('game_theory_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Game theory visualization saved: game_theory_analysis.png")
        plt.show()
    
    def run_complete_analysis(self):
        """
        Run complete game theory analysis
        """
        print("Game Theory Analysis: Zero-Sum Configuration and p-adic Extensions")
        print("=" * 70)
        
        # Load data
        if not self.load_data():
            print("Failed to load data. Exiting.")
            return
        
        # Run all analyses
        zero_sum_results = self.analyze_zero_sum_game()
        p_adic_results = self.analyze_p_adic_competition()
        quantum_results = self.analyze_quantum_game_theory()
        competitive_results = self.analyze_competitive_measurement()
        
        # Create visualizations
        self.create_game_theory_visualization()
        
        # Store results
        self.game_theory_results = {
            'zero_sum_game': zero_sum_results,
            'p_adic_competition': p_adic_results,
            'quantum_game_theory': quantum_results,
            'competitive_measurement': competitive_results
        }
        
        print("\n=== Game Theory Analysis Complete ===")
        print("Complete game theory analysis finished successfully!")
        print("Zero-sum configuration analyzed through classical and p-adic frameworks.")


def main():
    """
    Main function to run the game theory analysis
    """
    analyzer = GameTheoryAnalyzer()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
