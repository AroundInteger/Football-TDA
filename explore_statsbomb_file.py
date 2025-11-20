#!/usr/bin/env python3
"""
StatsBomb File Exploration Script
================================

This script explores a specific StatsBomb match file to understand
the detailed data structure and prepare for TDA analysis.

Based on: https://github.com/statsbomb/open-data
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class StatsBombFileExplorer:
    def __init__(self, data_path="open-data/data", match_id="3788741"):
        """
        Initialize the StatsBomb file explorer
        
        Args:
            data_path (str): Path to the StatsBomb data directory
            match_id (str): ID of the match to explore
        """
        self.data_path = Path(data_path)
        self.match_id = match_id
        
        # Data storage
        self.tracking_data = []
        self.events_data = []
        self.lineups_data = []
        
    def load_match_data(self):
        """Load all data for the specified match"""
        print(f"=== Loading Match {self.match_id} ===")
        
        # Load tracking data
        tracking_file = self.data_path / "three-sixty" / f"{self.match_id}.json"
        if tracking_file.exists():
            with open(tracking_file, 'r') as f:
                self.tracking_data = json.load(f)
            print(f"Loaded tracking data: {len(self.tracking_data)} events")
        else:
            print(f"Tracking file not found: {tracking_file}")
        
        # Load events data
        events_file = self.data_path / "events" / f"{self.match_id}.json"
        if events_file.exists():
            with open(events_file, 'r') as f:
                self.events_data = json.load(f)
            print(f"Loaded events data: {len(self.events_data)} events")
        else:
            print(f"Events file not found: {events_file}")
        
        # Load lineups data
        lineups_file = self.data_path / "lineups" / f"{self.match_id}.json"
        if lineups_file.exists():
            with open(lineups_file, 'r') as f:
                self.lineups_data = json.load(f)
            print(f"Loaded lineups data: {len(self.lineups_data)} teams")
        else:
            print(f"Lineups file not found: {lineups_file}")
        
        print()
    
    def analyze_tracking_structure(self):
        """Analyze the structure of tracking data"""
        print("=== Tracking Data Structure Analysis ===")
        
        if not self.tracking_data:
            print("No tracking data available")
            return
        
        # Analyze first few events
        print("Sample tracking events:")
        for i, event in enumerate(self.tracking_data[:3]):
            print(f"Event {i+1}:")
            print(f"  Event UUID: {event.get('event_uuid', 'N/A')}")
            print(f"  Visible area: {len(event.get('visible_area', []))} coordinates")
            
            freeze_frame = event.get('freeze_frame', [])
            print(f"  Freeze frame: {len(freeze_frame)} players")
            
            if freeze_frame:
                # Count player types
                teammates = sum(1 for p in freeze_frame if p.get('teammate', False))
                opponents = len(freeze_frame) - teammates
                actors = sum(1 for p in freeze_frame if p.get('actor', False))
                keepers = sum(1 for p in freeze_frame if p.get('keeper', False))
                
                print(f"    Teammates: {teammates}, Opponents: {opponents}")
                print(f"    Actors: {actors}, Keepers: {keepers}")
                
                # Sample positions
                if freeze_frame:
                    sample_player = freeze_frame[0]
                    print(f"    Sample position: {sample_player.get('location', 'N/A')}")
            print()
        
        # Analyze coordinate ranges
        self.analyze_coordinate_ranges()
    
    def analyze_coordinate_ranges(self):
        """Analyze coordinate ranges across all tracking data"""
        print("=== Coordinate Analysis ===")
        
        all_positions = []
        teammate_positions = []
        opponent_positions = []
        
        for event in self.tracking_data:
            freeze_frame = event.get('freeze_frame', [])
            for player in freeze_frame:
                location = player.get('location', [])
                if len(location) == 2:
                    all_positions.append(location)
                    if player.get('teammate', False):
                        teammate_positions.append(location)
                    else:
                        opponent_positions.append(location)
        
        if all_positions:
            positions_array = np.array(all_positions)
            teammate_array = np.array(teammate_positions) if teammate_positions else np.array([])
            opponent_array = np.array(opponent_positions) if opponent_positions else np.array([])
            
            print(f"Total positions analyzed: {len(all_positions)}")
            print(f"Teammate positions: {len(teammate_positions)}")
            print(f"Opponent positions: {len(opponent_positions)}")
            print()
            
            print("Overall coordinate ranges:")
            print(f"  X range: {positions_array[:, 0].min():.1f} to {positions_array[:, 0].max():.1f}")
            print(f"  Y range: {positions_array[:, 1].min():.1f} to {positions_array[:, 1].max():.1f}")
            print(f"  Field dimensions: {positions_array[:, 0].max() - positions_array[:, 0].min():.1f}m x {positions_array[:, 1].max() - positions_array[:, 1].min():.1f}m")
            print()
            
            if len(teammate_array) > 0:
                print("Teammate coordinate ranges:")
                print(f"  X range: {teammate_array[:, 0].min():.1f} to {teammate_array[:, 0].max():.1f}")
                print(f"  Y range: {teammate_array[:, 1].min():.1f} to {teammate_array[:, 1].max():.1f}")
                print()
            
            if len(opponent_array) > 0:
                print("Opponent coordinate ranges:")
                print(f"  X range: {opponent_array[:, 0].min():.1f} to {opponent_array[:, 0].max():.1f}")
                print(f"  Y range: {opponent_array[:, 1].min():.1f} to {opponent_array[:, 1].max():.1f}")
                print()
    
    def analyze_events_structure(self):
        """Analyze the structure of events data"""
        print("=== Events Data Structure Analysis ===")
        
        if not self.events_data:
            print("No events data available")
            return
        
        # Analyze event types
        event_types = {}
        for event in self.events_data:
            event_type = event.get('type', {}).get('name', 'Unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        print("Event types (top 15):")
        sorted_types = sorted(event_types.items(), key=lambda x: x[1], reverse=True)
        for event_type, count in sorted_types[:15]:
            print(f"  {event_type}: {count}")
        print()
        
        # Analyze sample events
        print("Sample events:")
        for i, event in enumerate(self.events_data[:5]):
            print(f"Event {i+1}:")
            print(f"  ID: {event.get('id', 'N/A')}")
            print(f"  Type: {event.get('type', {}).get('name', 'N/A')}")
            print(f"  Period: {event.get('period', 'N/A')}")
            print(f"  Timestamp: {event.get('timestamp', 'N/A')}")
            print(f"  Team: {event.get('team', {}).get('name', 'N/A')}")
            
            # Check for location data
            location = event.get('location', [])
            if location:
                print(f"  Location: {location}")
            
            # Check for tactics
            tactics = event.get('tactics', {})
            if tactics:
                print(f"  Formation: {tactics.get('formation', 'N/A')}")
            
            # Check for possession
            possession_team = event.get('possession_team', {})
            if possession_team:
                print(f"  Possession: {possession_team.get('name', 'N/A')}")
            print()
    
    def analyze_lineups_structure(self):
        """Analyze the structure of lineups data"""
        print("=== Lineups Data Structure Analysis ===")
        
        if not self.lineups_data:
            print("No lineups data available")
            return
        
        print("Team lineups:")
        for i, team in enumerate(self.lineups_data):
            print(f"Team {i+1}:")
            print(f"  Name: {team.get('team_name', 'N/A')}")
            print(f"  Country: {team.get('country', {}).get('name', 'N/A')}")
            
            lineup = team.get('lineup', [])
            print(f"  Players: {len(lineup)}")
            
            if lineup:
                # Show first few players
                print("  Sample players:")
                for j, player in enumerate(lineup[:5]):
                    print(f"    {j+1}. {player.get('player_name', 'N/A')} (#{player.get('jersey_number', 'N/A')}) - {player.get('position', {}).get('name', 'N/A')}")
                if len(lineup) > 5:
                    print(f"    ... and {len(lineup) - 5} more players")
            print()
    
    def extract_team_positions(self, event_index=0):
        """Extract team positions from a specific tracking event"""
        print(f"=== Team Positions Analysis (Event {event_index}) ===")
        
        if not self.tracking_data or event_index >= len(self.tracking_data):
            print("Invalid event index or no tracking data")
            return None, None
        
        event = self.tracking_data[event_index]
        freeze_frame = event.get('freeze_frame', [])
        
        if not freeze_frame:
            print("No freeze frame data available")
            return None, None
        
        # Separate teammates and opponents
        teammates = []
        opponents = []
        
        for player in freeze_frame:
            location = player.get('location', [])
            if len(location) == 2:
                if player.get('teammate', False):
                    teammates.append(location)
                else:
                    opponents.append(location)
        
        teammates_array = np.array(teammates) if teammates else np.array([])
        opponents_array = np.array(opponents) if opponents else np.array([])
        
        print(f"Teammates: {len(teammates)} players")
        print(f"Opponents: {len(opponents)} players")
        
        if len(teammates_array) > 0:
            print(f"Teammate positions: {teammates_array.tolist()}")
            print(f"Teammate centroid: {np.mean(teammates_array, axis=0).tolist()}")
        
        if len(opponents_array) > 0:
            print(f"Opponent positions: {opponents_array.tolist()}")
            print(f"Opponent centroid: {np.mean(opponents_array, axis=0).tolist()}")
        
        return teammates_array, opponents_array
    
    def calculate_team_metrics(self, teammates, opponents):
        """Calculate team metrics from player positions"""
        print("=== Team Metrics Calculation ===")
        
        if len(teammates) == 0 or len(opponents) == 0:
            print("Insufficient data for metrics calculation")
            return None
        
        # Team centroids
        teammate_centroid = np.mean(teammates, axis=0)
        opponent_centroid = np.mean(opponents, axis=0)
        
        # Inter-team distance
        inter_team_distance = np.linalg.norm(teammate_centroid - opponent_centroid)
        
        # Team spreads
        teammate_spread = np.std(teammates, axis=0)
        opponent_spread = np.std(opponents, axis=0)
        
        # Team areas (approximate)
        teammate_area = (teammates[:, 0].max() - teammates[:, 0].min()) * (teammates[:, 1].max() - teammates[:, 1].min())
        opponent_area = (opponents[:, 0].max() - opponents[:, 0].min()) * (opponents[:, 1].max() - opponents[:, 1].min())
        
        metrics = {
            'teammate_centroid': teammate_centroid.tolist(),
            'opponent_centroid': opponent_centroid.tolist(),
            'inter_team_distance': inter_team_distance,
            'teammate_spread': teammate_spread.tolist(),
            'opponent_spread': opponent_spread.tolist(),
            'teammate_area': teammate_area,
            'opponent_area': opponent_area,
            'area_ratio': teammate_area / opponent_area if opponent_area > 0 else 0
        }
        
        print("Calculated metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        return metrics
    
    def visualize_positions(self, teammates, opponents, event_index=0):
        """Create a simple visualization of player positions"""
        print(f"=== Position Visualization (Event {event_index}) ===")
        
        if len(teammates) == 0 and len(opponents) == 0:
            print("No position data to visualize")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Plot teammates
        if len(teammates) > 0:
            plt.scatter(teammates[:, 0], teammates[:, 1], c='blue', s=100, label='Teammates', alpha=0.7)
            plt.scatter(np.mean(teammates[:, 0]), np.mean(teammates[:, 1]), c='darkblue', s=200, marker='x', label='Teammate Centroid')
        
        # Plot opponents
        if len(opponents) > 0:
            plt.scatter(opponents[:, 0], opponents[:, 1], c='red', s=100, label='Opponents', alpha=0.7)
            plt.scatter(np.mean(opponents[:, 0]), np.mean(opponents[:, 1]), c='darkred', s=200, marker='x', label='Opponent Centroid')
        
        plt.xlabel('X Position (meters)')
        plt.ylabel('Y Position (meters)')
        plt.title(f'Player Positions - Event {event_index}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        # Save the plot
        plt.savefig(f'statsbomb_positions_event_{event_index}.png', dpi=150, bbox_inches='tight')
        print(f"Position visualization saved as: statsbomb_positions_event_{event_index}.png")
        plt.show()
    
    def run_complete_analysis(self):
        """Run the complete file analysis"""
        print("StatsBomb File Exploration")
        print("=" * 50)
        
        # Load all data
        self.load_match_data()
        
        # Analyze each data type
        self.analyze_tracking_structure()
        self.analyze_events_structure()
        self.analyze_lineups_structure()
        
        # Extract positions and calculate metrics
        teammates, opponents = self.extract_team_positions(0)
        if teammates is not None and opponents is not None:
            metrics = self.calculate_team_metrics(teammates, opponents)
            
            # Create visualization
            self.visualize_positions(teammates, opponents, 0)
        
        print("\n=== Analysis Complete ===")
        print("Ready for TDA pipeline development!")

def main():
    """Main function to run the analysis"""
    # Explore match 3788741 (Turkey vs Italy from Euro 2020)
    explorer = StatsBombFileExplorer(match_id="3788741")
    explorer.run_complete_analysis()

if __name__ == "__main__":
    main()
