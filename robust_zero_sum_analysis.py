#!/usr/bin/env python3
"""
Robust Zero-Sum Configuration Analysis with L1-Norm
=================================================

This script performs robust zero-sum analysis using L1-norm fitting to be less
sensitive to outliers and provide a cleaner view of the fundamental zero-sum
configuration in football team dynamics.

Author: GPS-TDA Research Team
Date: December 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
from sklearn.linear_model import Lasso, HuberRegressor
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.optimize import minimize
warnings.filterwarnings('ignore')

class RobustZeroSumAnalyzer:
    """
    Performs robust zero-sum analysis using L1-norm fitting
    """
    
    def __init__(self, first_half_dir='first_half_efficient_results', 
                 second_half_dir='second_half_efficient_results'):
        """
        Initialize the robust zero-sum analyzer
        
        Args:
            first_half_dir (str): Directory containing first half TDA results
            second_half_dir (str): Directory containing second half TDA results
        """
        self.first_half_dir = Path(first_half_dir)
        self.second_half_dir = Path(second_half_dir)
        
        self.combined_data = None
        self.robust_analysis = {}
        
        print(f"RobustZeroSumAnalyzer initialized")
        print(f"  First half TDA: {self.first_half_dir}")
        print(f"  Second half TDA: {self.second_half_dir}")
    
    def load_data(self):
        """
        Load TDA analysis data
        """
        print("\n=== Loading TDA Data for Robust Zero-Sum Analysis ===")
        
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
    
    def l1_norm_fit(self, x, y, alpha=0.01):
        """
        Perform L1-norm (Lasso) regression fit
        
        Args:
            x (array): Independent variable
            y (array): Dependent variable
            alpha (float): Regularization parameter
        
        Returns:
            dict: Fitting results
        """
        # Reshape data for sklearn
        X = x.reshape(-1, 1)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Fit L1-norm (Lasso) regression
        lasso = Lasso(alpha=alpha, max_iter=10000)
        lasso.fit(X_scaled, y)
        
        # Get coefficients and intercept
        coef = lasso.coef_[0]
        intercept = lasso.intercept_
        
        # Calculate predictions
        y_pred = lasso.predict(X_scaled)
        
        # Calculate L1-norm residuals
        residuals = np.abs(y - y_pred)
        l1_loss = np.mean(residuals)
        
        # Calculate R-squared
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return {
            'coefficient': coef,
            'intercept': intercept,
            'predictions': y_pred,
            'residuals': residuals,
            'l1_loss': l1_loss,
            'r_squared': r_squared,
            'scaler': scaler,
            'model': lasso
        }
    
    def huber_robust_fit(self, x, y, epsilon=1.35):
        """
        Perform Huber robust regression fit
        
        Args:
            x (array): Independent variable
            y (array): Dependent variable
            epsilon (float): Huber parameter
        
        Returns:
            dict: Fitting results
        """
        # Reshape data for sklearn
        X = x.reshape(-1, 1)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Fit Huber robust regression
        huber = HuberRegressor(epsilon=epsilon, max_iter=1000)
        huber.fit(X_scaled, y)
        
        # Get coefficients and intercept
        coef = huber.coef_[0]
        intercept = huber.intercept_
        
        # Calculate predictions
        y_pred = huber.predict(X_scaled)
        
        # Calculate Huber loss
        residuals = y - y_pred
        huber_loss = np.mean(self._huber_loss(residuals, epsilon))
        
        # Calculate R-squared
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        return {
            'coefficient': coef,
            'intercept': intercept,
            'predictions': y_pred,
            'residuals': residuals,
            'huber_loss': huber_loss,
            'r_squared': r_squared,
            'scaler': scaler,
            'model': huber
        }
    
    def _huber_loss(self, residuals, epsilon):
        """
        Calculate Huber loss function
        
        Args:
            residuals (array): Residuals
            epsilon (float): Huber parameter
        
        Returns:
            array: Huber loss values
        """
        abs_residuals = np.abs(residuals)
        return np.where(abs_residuals <= epsilon, 
                       0.5 * residuals**2, 
                       epsilon * (abs_residuals - 0.5 * epsilon))
    
    def analyze_robust_zero_sum_correlations(self):
        """
        Analyze zero-sum correlations using robust fitting methods
        """
        print("\n=== Analyzing Robust Zero-Sum Correlations ===")
        
        # Extract team metrics
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        inter_team_distance = self.combined_data['avg_inter_team_distance'].values
        team_area_ratio = self.combined_data['avg_team_area_ratio'].values
        
        # Remove any NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread) | 
                      np.isnan(inter_team_distance) | np.isnan(team_area_ratio))
        
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        inter_team_distance = inter_team_distance[valid_mask]
        team_area_ratio = team_area_ratio[valid_mask]
        
        print(f"Valid data points: {len(home_spread)}")
        
        # Perform robust fits
        robust_fits = {}
        
        # 1. Home vs Away Spread (main zero-sum relationship)
        print("\n1. Home vs Away Spread (L1-norm fit):")
        l1_fit = self.l1_norm_fit(home_spread, away_spread, alpha=0.01)
        robust_fits['home_away_l1'] = l1_fit
        
        print(f"   L1 Coefficient: {l1_fit['coefficient']:.4f}")
        print(f"   L1 Intercept: {l1_fit['intercept']:.4f}")
        print(f"   L1 Loss: {l1_fit['l1_loss']:.4f}")
        print(f"   R-squared: {l1_fit['r_squared']:.4f}")
        
        # Huber robust fit for comparison
        huber_fit = self.huber_robust_fit(home_spread, away_spread, epsilon=1.35)
        robust_fits['home_away_huber'] = huber_fit
        
        print(f"   Huber Coefficient: {huber_fit['coefficient']:.4f}")
        print(f"   Huber Intercept: {huber_fit['intercept']:.4f}")
        print(f"   Huber Loss: {huber_fit['huber_loss']:.4f}")
        print(f"   R-squared: {huber_fit['r_squared']:.4f}")
        
        # 2. Home Spread vs Inter-team Distance
        print("\n2. Home Spread vs Inter-team Distance (L1-norm fit):")
        l1_fit_distance = self.l1_norm_fit(home_spread, inter_team_distance, alpha=0.01)
        robust_fits['home_distance_l1'] = l1_fit_distance
        
        print(f"   L1 Coefficient: {l1_fit_distance['coefficient']:.4f}")
        print(f"   L1 Intercept: {l1_fit_distance['intercept']:.4f}")
        print(f"   L1 Loss: {l1_fit_distance['l1_loss']:.4f}")
        print(f"   R-squared: {l1_fit_distance['r_squared']:.4f}")
        
        # 3. Away Spread vs Inter-team Distance
        print("\n3. Away Spread vs Inter-team Distance (L1-norm fit):")
        l1_fit_away_distance = self.l1_norm_fit(away_spread, inter_team_distance, alpha=0.01)
        robust_fits['away_distance_l1'] = l1_fit_away_distance
        
        print(f"   L1 Coefficient: {l1_fit_away_distance['coefficient']:.4f}")
        print(f"   L1 Intercept: {l1_fit_away_distance['intercept']:.4f}")
        print(f"   L1 Loss: {l1_fit_away_distance['l1_loss']:.4f}")
        print(f"   R-squared: {l1_fit_away_distance['r_squared']:.4f}")
        
        # 4. Home Spread vs Team Area Ratio
        print("\n4. Home Spread vs Team Area Ratio (L1-norm fit):")
        l1_fit_area = self.l1_norm_fit(home_spread, team_area_ratio, alpha=0.01)
        robust_fits['home_area_l1'] = l1_fit_area
        
        print(f"   L1 Coefficient: {l1_fit_area['coefficient']:.4f}")
        print(f"   L1 Intercept: {l1_fit_area['intercept']:.4f}")
        print(f"   L1 Loss: {l1_fit_area['l1_loss']:.4f}")
        print(f"   R-squared: {l1_fit_area['r_squared']:.4f}")
        
        # Calculate robust zero-sum strength
        main_coefficient = l1_fit['coefficient']
        zero_sum_strength = abs(main_coefficient)
        
        print(f"\nRobust Zero-Sum Analysis:")
        print(f"  Main Zero-Sum Coefficient: {main_coefficient:.4f}")
        print(f"  Zero-Sum Strength: {zero_sum_strength:.4f}")
        
        if zero_sum_strength > 0.5:
            print("  ✓ Strong robust zero-sum configuration detected!")
        elif zero_sum_strength > 0.3:
            print("  ✓ Moderate robust zero-sum configuration detected")
        else:
            print("  ✗ Weak robust zero-sum configuration")
        
        return robust_fits
    
    def analyze_outlier_robustness(self):
        """
        Analyze the robustness to outliers
        """
        print("\n=== Analyzing Outlier Robustness ===")
        
        # Extract team metrics
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        
        # Calculate outlier statistics
        home_q1, home_q3 = np.percentile(home_spread, [25, 75])
        home_iqr = home_q3 - home_q1
        home_outliers = np.sum((home_spread < home_q1 - 1.5 * home_iqr) | 
                              (home_spread > home_q3 + 1.5 * home_iqr))
        
        away_q1, away_q3 = np.percentile(away_spread, [25, 75])
        away_iqr = away_q3 - away_q1
        away_outliers = np.sum((away_spread < away_q1 - 1.5 * away_iqr) | 
                              (away_spread > away_q3 + 1.5 * away_iqr))
        
        print(f"Outlier Analysis:")
        print(f"  Home Spread Outliers: {home_outliers} ({home_outliers/len(home_spread)*100:.1f}%)")
        print(f"  Away Spread Outliers: {away_outliers} ({away_outliers/len(away_spread)*100:.1f}%)")
        print(f"  Total Data Points: {len(home_spread)}")
        
        # Compare L1-norm vs L2-norm (ordinary least squares)
        from sklearn.linear_model import LinearRegression
        
        # L2-norm (OLS) fit
        X = home_spread.reshape(-1, 1)
        ols = LinearRegression()
        ols.fit(X, away_spread)
        ols_coef = ols.coef_[0]
        ols_intercept = ols.intercept_
        ols_pred = ols.predict(X)
        ols_residuals = np.abs(away_spread - ols_pred)
        ols_loss = np.mean(ols_residuals)
        
        # L1-norm fit
        l1_fit = self.l1_norm_fit(home_spread, away_spread, alpha=0.01)
        
        print(f"\nRobustness Comparison:")
        print(f"  L2-norm (OLS) Coefficient: {ols_coef:.4f}")
        print(f"  L1-norm Coefficient: {l1_fit['coefficient']:.4f}")
        print(f"  L2-norm Loss: {ols_loss:.4f}")
        print(f"  L1-norm Loss: {l1_fit['l1_loss']:.4f}")
        print(f"  Robustness Improvement: {((ols_loss - l1_fit['l1_loss']) / ols_loss * 100):.1f}%")
        
        return {
            'home_outliers': home_outliers,
            'away_outliers': away_outliers,
            'ols_coefficient': ols_coef,
            'l1_coefficient': l1_fit['coefficient'],
            'ols_loss': ols_loss,
            'l1_loss': l1_fit['l1_loss']
        }
    
    def create_robust_visualization(self):
        """
        Create visualization comparing robust and non-robust fits
        """
        print("\n=== Creating Robust Zero-Sum Visualization ===")
        
        # Extract data
        home_spread = self.combined_data['avg_home_spread'].values
        away_spread = self.combined_data['avg_away_spread'].values
        
        # Remove NaN values
        valid_mask = ~(np.isnan(home_spread) | np.isnan(away_spread))
        home_spread = home_spread[valid_mask]
        away_spread = away_spread[valid_mask]
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Robust Zero-Sum Configuration Analysis (L1-norm vs L2-norm)', fontsize=16, fontweight='bold')
        
        # Plot 1: L1-norm fit
        ax1 = axes[0, 0]
        l1_fit = self.l1_norm_fit(home_spread, away_spread, alpha=0.01)
        
        scatter = ax1.scatter(home_spread, away_spread, alpha=0.6, s=20, color='blue')
        ax1.plot(home_spread, l1_fit['predictions'], 'r-', linewidth=2, 
                label=f'L1-norm fit (coef={l1_fit["coefficient"]:.3f})')
        ax1.set_xlabel('Home Team Spread (m)')
        ax1.set_ylabel('Away Team Spread (m)')
        ax1.set_title('L1-norm Robust Fit')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: L2-norm (OLS) fit for comparison
        ax2 = axes[0, 1]
        from sklearn.linear_model import LinearRegression
        
        X = home_spread.reshape(-1, 1)
        ols = LinearRegression()
        ols.fit(X, away_spread)
        ols_pred = ols.predict(X)
        
        scatter = ax2.scatter(home_spread, away_spread, alpha=0.6, s=20, color='blue')
        ax2.plot(home_spread, ols_pred, 'g-', linewidth=2, 
                label=f'L2-norm fit (coef={ols.coef_[0]:.3f})')
        ax2.set_xlabel('Home Team Spread (m)')
        ax2.set_ylabel('Away Team Spread (m)')
        ax2.set_title('L2-norm (OLS) Fit')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Residuals comparison
        ax3 = axes[1, 0]
        l1_residuals = l1_fit['residuals']
        ols_residuals = np.abs(away_spread - ols_pred)
        
        ax3.scatter(home_spread, l1_residuals, alpha=0.6, s=20, color='red', label='L1-norm residuals')
        ax3.scatter(home_spread, ols_residuals, alpha=0.6, s=20, color='green', label='L2-norm residuals')
        ax3.set_xlabel('Home Team Spread (m)')
        ax3.set_ylabel('Absolute Residuals')
        ax3.set_title('Residuals Comparison')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Outlier analysis
        ax4 = axes[1, 1]
        
        # Identify outliers
        home_q1, home_q3 = np.percentile(home_spread, [25, 75])
        home_iqr = home_q3 - home_q1
        home_outlier_mask = (home_spread < home_q1 - 1.5 * home_iqr) | (home_spread > home_q3 + 1.5 * home_iqr)
        
        away_q1, away_q3 = np.percentile(away_spread, [25, 75])
        away_iqr = away_q3 - away_q1
        away_outlier_mask = (away_spread < away_q1 - 1.5 * away_iqr) | (away_spread > away_q3 + 1.5 * away_iqr)
        
        outlier_mask = home_outlier_mask | away_outlier_mask
        
        # Plot normal points
        ax4.scatter(home_spread[~outlier_mask], away_spread[~outlier_mask], 
                   alpha=0.6, s=20, color='blue', label='Normal points')
        
        # Plot outliers
        ax4.scatter(home_spread[outlier_mask], away_spread[outlier_mask], 
                   alpha=0.8, s=30, color='red', label='Outliers')
        
        # Plot both fits
        ax4.plot(home_spread, l1_fit['predictions'], 'r-', linewidth=2, 
                label=f'L1-norm (robust)')
        ax4.plot(home_spread, ols_pred, 'g--', linewidth=2, 
                label=f'L2-norm (sensitive)')
        
        ax4.set_xlabel('Home Team Spread (m)')
        ax4.set_ylabel('Away Team Spread (m)')
        ax4.set_title('Outlier Impact on Fits')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('robust_zero_sum_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Robust zero-sum visualization saved: robust_zero_sum_analysis.png")
        plt.show()
    
    def run_complete_analysis(self):
        """
        Run complete robust zero-sum analysis
        """
        print("Robust Zero-Sum Configuration Analysis with L1-norm")
        print("=" * 60)
        
        # Load data
        if not self.load_data():
            print("Failed to load data. Exiting.")
            return
        
        # Run all analyses
        robust_fits = self.analyze_robust_zero_sum_correlations()
        outlier_analysis = self.analyze_outlier_robustness()
        
        # Create visualizations
        self.create_robust_visualization()
        
        # Store results
        self.robust_analysis = {
            'robust_fits': robust_fits,
            'outlier_analysis': outlier_analysis
        }
        
        print("\n=== Robust Zero-Sum Analysis Complete ===")
        print("Complete robust zero-sum analysis finished successfully!")
        print("L1-norm fitting provides a more robust view of the zero-sum configuration")
        print("by being less sensitive to outliers.")


def main():
    """
    Main function to run the robust zero-sum analysis
    """
    analyzer = RobustZeroSumAnalyzer()
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
