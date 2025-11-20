#!/usr/bin/env python3
"""
SkillCorner Data Exploration Script
==================================

This script explores the SkillCorner Open Data repository to understand
the data structure and prepare for TDA analysis integration.

Based on: https://github.com/SkillCorner/opendata
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns  # Optional, not required for basic exploration
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

class SkillCornerDataExplorer:
    def __init__(self, data_path="opendata/data"):
        """
        Initialize the SkillCorner data explorer
        
        Args:
            data_path (str): Path to the SkillCorner data directory
        """
        self.data_path = Path(data_path)
        self.matches_info = None
        self.available_matches = []
        
    def setup_data_directory(self):
        """Setup the data directory and download instructions"""
        print("=== SkillCorner Data Setup ===")
        print("To get started with SkillCorner data:")
        print("1. Clone the repository: git clone https://github.com/SkillCorner/opendata.git")
        print("2. Set data_path to the 'data' directory in the cloned repo")
        print("3. Run this script to explore the data structure")
        print()
        
        if not self.data_path.exists():
            print(f"Data directory not found: {self.data_path}")
            print("Please clone the SkillCorner repository and set the correct path")
            return False
        
        return True
    
    def load_match_metadata(self):
        """Load the matches.json file with basic match information"""
        matches_file = self.data_path / "matches.json"
        
        if not matches_file.exists():
            print(f"Matches file not found: {matches_file}")
            return None
        
        try:
            with open(matches_file, 'r') as f:
                self.matches_info = json.load(f)
            
            print("=== Match Metadata ===")
            print(f"Total matches available: {len(self.matches_info)}")
            print()
            
            for i, match in enumerate(self.matches_info):
                print(f"Match {i+1}:")
                print(f"  ID: {match.get('id', 'N/A')}")
                print(f"  Home Team: {match.get('home_team', 'N/A')}")
                print(f"  Away Team: {match.get('away_team', 'N/A')}")
                print(f"  Date: {match.get('date', 'N/A')}")
                print(f"  Competition: {match.get('competition', 'N/A')}")
                print()
                
                self.available_matches.append(match['id'])
            
            return self.matches_info
            
        except Exception as e:
            print(f"Error loading matches metadata: {e}")
            return None
    
    def explore_match_structure(self, match_id=None):
        """Explore the structure of a specific match"""
        if match_id is None:
            match_id = self.available_matches[0] if self.available_matches else None
        
        if match_id is None:
            print("No matches available to explore")
            return
        
        match_dir = self.data_path / "matches" / str(match_id)
        
        if not match_dir.exists():
            print(f"Match directory not found: {match_dir}")
            return
        
        print(f"=== Exploring Match {match_id} ===")
        
        # List available files
        files = list(match_dir.glob("*"))
        print("Available files:")
        for file in files:
            print(f"  {file.name} ({file.stat().st_size / 1024 / 1024:.1f} MB)")
        print()
        
        # Explore match.json
        match_file = match_dir / f"{match_id}_match.json"
        if match_file.exists():
            self.explore_match_info(match_file)
        
        # Explore tracking data
        tracking_file = match_dir / f"{match_id}_tracking_extrapolated.jsonl"
        if tracking_file.exists():
            self.explore_tracking_data(tracking_file)
        
        # Explore dynamic events
        events_file = match_dir / f"{match_id}_dynamic_events.csv"
        if events_file.exists():
            self.explore_dynamic_events(events_file)
        
        # Explore phases of play
        phases_file = match_dir / f"{match_id}_phases_of_play.csv"
        if phases_file.exists():
            self.explore_phases_of_play(phases_file)
    
    def explore_match_info(self, match_file):
        """Explore the match information file"""
        print("=== Match Information ===")
        
        try:
            with open(match_file, 'r') as f:
                match_info = json.load(f)
            
            print(f"Match ID: {match_info.get('id', 'N/A')}")
            print(f"Home Team: {match_info.get('home_team', 'N/A')}")
            print(f"Away Team: {match_info.get('away_team', 'N/A')}")
            print(f"Date: {match_info.get('date', 'N/A')}")
            print(f"Competition: {match_info.get('competition', 'N/A')}")
            print(f"Pitch Size: {match_info.get('pitch_size', 'N/A')}")
            print(f"Referee: {match_info.get('referee', 'N/A')}")
            print()
            
            # Explore lineup information
            if 'lineup' in match_info:
                print("Lineup Information:")
                for team in ['home', 'away']:
                    if team in match_info['lineup']:
                        print(f"  {team.title()} Team:")
                        for player in match_info['lineup'][team]:
                            print(f"    Player {player.get('player_id', 'N/A')}: {player.get('name', 'N/A')}")
                print()
            
        except Exception as e:
            print(f"Error exploring match info: {e}")
    
    def explore_tracking_data(self, tracking_file, max_frames=100):
        """Explore the tracking data structure"""
        print("=== Tracking Data Structure ===")
        
        try:
            frames = []
            with open(tracking_file, 'r') as f:
                for i, line in enumerate(f):
                    if i >= max_frames:
                        break
                    frames.append(json.loads(line.strip()))
            
            if not frames:
                print("No tracking data found")
                return
            
            print(f"Sample frames loaded: {len(frames)}")
            print(f"Total file size: {tracking_file.stat().st_size / 1024 / 1024:.1f} MB")
            print()
            
            # Analyze first frame
            first_frame = frames[0]
            print("First frame structure:")
            for key, value in first_frame.items():
                if isinstance(value, list):
                    print(f"  {key}: list with {len(value)} elements")
                elif isinstance(value, dict):
                    print(f"  {key}: dict with keys {list(value.keys())}")
                else:
                    print(f"  {key}: {type(value).__name__} = {value}")
            print()
            
            # Analyze player data
            if 'player_data' in first_frame:
                player_data = first_frame['player_data']
                print(f"Players in first frame: {len(player_data)}")
                
                if player_data:
                    print("Player data structure:")
                    for key, value in player_data[0].items():
                        print(f"  {key}: {type(value).__name__}")
                    print()
                    
                    # Analyze player positions
                    x_coords = [p.get('x', 0) for p in player_data if 'x' in p]
                    y_coords = [p.get('y', 0) for p in player_data if 'y' in p]
                    
                    if x_coords and y_coords:
                        print(f"X coordinates range: {min(x_coords):.1f} to {max(x_coords):.1f}")
                        print(f"Y coordinates range: {min(y_coords):.1f} to {max(y_coords):.1f}")
                        print(f"Field dimensions: {max(x_coords) - min(x_coords):.1f}m x {max(y_coords) - min(y_coords):.1f}m")
                        print()
            
            # Analyze ball data
            if 'ball_data' in first_frame:
                ball_data = first_frame['ball_data']
                print("Ball data structure:")
                for key, value in ball_data.items():
                    print(f"  {key}: {type(value).__name__} = {value}")
                print()
            
            # Analyze possession data
            if 'possession' in first_frame:
                possession = first_frame['possession']
                print("Possession data structure:")
                for key, value in possession.items():
                    print(f"  {key}: {type(value).__name__} = {value}")
                print()
            
        except Exception as e:
            print(f"Error exploring tracking data: {e}")
    
    def explore_dynamic_events(self, events_file):
        """Explore the dynamic events data"""
        print("=== Dynamic Events Structure ===")
        
        try:
            # Load first few rows to understand structure
            df = pd.read_csv(events_file, nrows=10)
            
            print(f"Events file size: {events_file.stat().st_size / 1024:.1f} KB")
            print(f"Columns: {list(df.columns)}")
            print()
            
            print("Sample events:")
            print(df.head())
            print()
            
            # Load full dataset for statistics
            df_full = pd.read_csv(events_file)
            print(f"Total events: {len(df_full)}")
            
            if 'event_type' in df_full.columns:
                print("Event types:")
                print(df_full['event_type'].value_counts())
                print()
            
        except Exception as e:
            print(f"Error exploring dynamic events: {e}")
    
    def explore_phases_of_play(self, phases_file):
        """Explore the phases of play data"""
        print("=== Phases of Play Structure ===")
        
        try:
            df = pd.read_csv(phases_file)
            
            print(f"Phases file size: {phases_file.stat().st_size / 1024:.1f} KB")
            print(f"Columns: {list(df.columns)}")
            print(f"Total phases: {len(df)}")
            print()
            
            print("Sample phases:")
            print(df.head())
            print()
            
            if 'phase_type' in df.columns:
                print("Phase types:")
                print(df['phase_type'].value_counts())
                print()
            
        except Exception as e:
            print(f"Error exploring phases of play: {e}")
    
    def create_data_summary(self):
        """Create a comprehensive data summary"""
        print("=== SkillCorner Data Summary ===")
        
        if not self.matches_info:
            print("No match metadata loaded")
            return
        
        summary = {
            'total_matches': len(self.matches_info),
            'available_match_ids': self.available_matches,
            'data_structure': {
                'tracking_data': 'JSONL format, 10 FPS, player and ball positions',
                'dynamic_events': 'CSV format, game intelligence events',
                'phases_of_play': 'CSV format, attacking/defending phases',
                'match_info': 'JSON format, lineups, referee, pitch size'
            },
            'coordinate_system': {
                'origin': 'Center of pitch (0,0)',
                'x_axis': 'Long side of pitch',
                'y_axis': 'Short side of pitch',
                'units': 'Meters',
                'standard_pitch': '105m x 68m'
            },
            'data_quality': {
                'player_identity_accuracy': '97%',
                'tracking_method': 'Computer vision + ML from broadcast video',
                'sampling_rate': '10 FPS',
                'extrapolation': 'Some positions extrapolated when not detected'
            }
        }
        
        print(json.dumps(summary, indent=2))
        
        return summary
    
    def generate_integration_recommendations(self):
        """Generate recommendations for integrating SkillCorner data with our TDA analysis"""
        print("=== Integration Recommendations ===")
        
        recommendations = [
            "1. Data Format Conversion:",
            "   - Convert JSONL tracking data to our standard format",
            "   - Handle 10 FPS vs 25 Hz sampling rate differences",
            "   - Standardize coordinate systems (both use meters)",
            "",
            "2. TDA Pipeline Adaptation:",
            "   - Modify existing TDA code for SkillCorner format",
            "   - Implement team metric calculations for new data structure",
            "   - Test persistent homology computation with new data",
            "",
            "3. Cross-Validation Strategy:",
            "   - Compare findings across multiple matches",
            "   - Test formation 'DNA' consistency across teams",
            "   - Validate quantum dot analogies across different contexts",
            "",
            "4. Enhanced Analysis Opportunities:",
            "   - Full match dynamics (90+ minutes vs 5-minute segments)",
            "   - Event correlation analysis (goals, cards, etc.)",
            "   - Multi-team comparison and league-wide patterns",
            "   - Phase of play integration with formation analysis",
            "",
            "5. Implementation Priority:",
            "   - Start with 2-3 matches for validation",
            "   - Focus on matches with different team combinations",
            "   - Gradually expand to full 10-match analysis",
            "   - Develop automated pipeline for batch processing"
        ]
        
        for rec in recommendations:
            print(rec)
    
    def run_full_exploration(self):
        """Run the complete data exploration"""
        print("SkillCorner Data Exploration")
        print("=" * 50)
        
        if not self.setup_data_directory():
            return
        
        # Load match metadata
        self.load_match_metadata()
        
        if not self.matches_info:
            return
        
        # Explore first match structure
        if self.available_matches:
            self.explore_match_structure(self.available_matches[0])
        
        # Create summary
        self.create_data_summary()
        
        # Generate recommendations
        self.generate_integration_recommendations()

def main():
    """Main function to run the exploration"""
    explorer = SkillCornerDataExplorer()
    explorer.run_full_exploration()

if __name__ == "__main__":
    main()
