#!/usr/bin/env python3
"""
StatsBomb Data Exploration Script
================================

This script explores the StatsBomb Open Data repository to understand
the data structure and prepare for TDA analysis integration.

Based on: https://github.com/statsbomb/open-data
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

class StatsBombDataExplorer:
    def __init__(self, data_path="open-data/data"):
        """
        Initialize the StatsBomb data explorer
        
        Args:
            data_path (str): Path to the StatsBomb data directory
        """
        self.data_path = Path(data_path)
        self.competitions = []
        self.available_matches = []
        self.tracking_matches = []
        
    def load_competitions(self):
        """Load competitions and seasons information"""
        competitions_file = self.data_path / "competitions.json"
        
        if not competitions_file.exists():
            print(f"Competitions file not found: {competitions_file}")
            return None
        
        try:
            with open(competitions_file, 'r') as f:
                self.competitions = json.load(f)
            
            print("=== StatsBomb Competitions ===")
            print(f"Total competitions: {len(self.competitions)}")
            print()
            
            # Group by competition
            competition_groups = {}
            for comp in self.competitions:
                comp_name = comp['competition_name']
                if comp_name not in competition_groups:
                    competition_groups[comp_name] = []
                competition_groups[comp_name].append(comp)
            
            print("Available competitions:")
            for comp_name, comps in competition_groups.items():
                seasons = [c['season_name'] for c in comps]
                countries = [c['country_name'] for c in comps]
                print(f"  {comp_name} ({countries[0]}): {len(comps)} seasons")
                print(f"    Seasons: {', '.join(seasons)}")
                print(f"    Has 360 data: {any(c.get('match_available_360') for c in comps)}")
                print()
            
            return self.competitions
            
        except Exception as e:
            print(f"Error loading competitions: {e}")
            return None
    
    def explore_tracking_data(self):
        """Explore the StatsBomb 360 tracking data"""
        three_sixty_dir = self.data_path / "three-sixty"
        
        if not three_sixty_dir.exists():
            print("Three-sixty directory not found")
            return
        
        print("=== StatsBomb 360 Tracking Data ===")
        
        # List available tracking files
        tracking_files = list(three_sixty_dir.glob("*.json"))
        print(f"Available tracking files: {len(tracking_files)}")
        
        if not tracking_files:
            print("No tracking files found")
            return
        
        # Analyze first tracking file
        sample_file = tracking_files[0]
        print(f"Analyzing sample file: {sample_file.name}")
        
        try:
            with open(sample_file, 'r') as f:
                tracking_data = json.load(f)
            
            print(f"Sample file size: {sample_file.stat().st_size / 1024 / 1024:.1f} MB")
            print(f"Number of events: {len(tracking_data)}")
            print()
            
            # Analyze first few events
            print("Sample event structure:")
            for i, event in enumerate(tracking_data[:3]):
                print(f"Event {i+1}:")
                print(f"  Event UUID: {event.get('event_uuid', 'N/A')}")
                print(f"  Visible area: {len(event.get('visible_area', []))} coordinates")
                print(f"  Freeze frame: {len(event.get('freeze_frame', []))} players")
                
                # Analyze freeze frame
                freeze_frame = event.get('freeze_frame', [])
                if freeze_frame:
                    teammates = sum(1 for p in freeze_frame if p.get('teammate', False))
                    opponents = len(freeze_frame) - teammates
                    actors = sum(1 for p in freeze_frame if p.get('actor', False))
                    keepers = sum(1 for p in freeze_frame if p.get('keeper', False))
                    
                    print(f"    Teammates: {teammates}, Opponents: {opponents}")
                    print(f"    Actors: {actors}, Keepers: {keepers}")
                    
                    # Sample player positions
                    if freeze_frame:
                        sample_player = freeze_frame[0]
                        print(f"    Sample position: {sample_player.get('location', 'N/A')}")
                print()
            
            # Analyze coordinate ranges
            all_positions = []
            for event in tracking_data[:100]:  # Sample first 100 events
                freeze_frame = event.get('freeze_frame', [])
                for player in freeze_frame:
                    location = player.get('location', [])
                    if len(location) == 2:
                        all_positions.append(location)
            
            if all_positions:
                positions_array = np.array(all_positions)
                print("Coordinate analysis (sample of 100 events):")
                print(f"  X range: {positions_array[:, 0].min():.1f} to {positions_array[:, 0].max():.1f}")
                print(f"  Y range: {positions_array[:, 1].min():.1f} to {positions_array[:, 1].max():.1f}")
                print(f"  Field dimensions: {positions_array[:, 0].max() - positions_array[:, 0].min():.1f} x {positions_array[:, 1].max() - positions_array[:, 1].min():.1f}")
                print()
            
            self.tracking_matches = [f.stem for f in tracking_files]
            
        except Exception as e:
            print(f"Error analyzing tracking data: {e}")
    
    def explore_events_data(self, sample_match_id=None):
        """Explore the events data structure"""
        events_dir = self.data_path / "events"
        
        if not events_dir.exists():
            print("Events directory not found")
            return
        
        print("=== StatsBomb Events Data ===")
        
        # List available event files
        event_files = list(events_dir.glob("*.json"))
        print(f"Available event files: {len(event_files)}")
        
        if not event_files:
            print("No event files found")
            return
        
        # Use provided match ID or first available
        if sample_match_id:
            sample_file = events_dir / f"{sample_match_id}.json"
        else:
            sample_file = event_files[0]
        
        if not sample_file.exists():
            print(f"Sample file not found: {sample_file}")
            return
        
        print(f"Analyzing sample file: {sample_file.name}")
        
        try:
            with open(sample_file, 'r') as f:
                events_data = json.load(f)
            
            print(f"Sample file size: {sample_file.stat().st_size / 1024:.1f} KB")
            print(f"Number of events: {len(events_data)}")
            print()
            
            # Analyze event types
            event_types = {}
            for event in events_data:
                event_type = event.get('type', {}).get('name', 'Unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            print("Event types (top 10):")
            sorted_types = sorted(event_types.items(), key=lambda x: x[1], reverse=True)
            for event_type, count in sorted_types[:10]:
                print(f"  {event_type}: {count}")
            print()
            
            # Analyze first few events
            print("Sample event structure:")
            for i, event in enumerate(events_data[:3]):
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
                print()
            
            self.available_matches = [f.stem for f in event_files]
            
        except Exception as e:
            print(f"Error analyzing events data: {e}")
    
    def explore_lineups_data(self, sample_match_id=None):
        """Explore the lineups data structure"""
        lineups_dir = self.data_path / "lineups"
        
        if not lineups_dir.exists():
            print("Lineups directory not found")
            return
        
        print("=== StatsBomb Lineups Data ===")
        
        # List available lineup files
        lineup_files = list(lineups_dir.glob("*.json"))
        print(f"Available lineup files: {len(lineup_files)}")
        
        if not lineup_files:
            print("No lineup files found")
            return
        
        # Use provided match ID or first available
        if sample_match_id:
            sample_file = lineups_dir / f"{sample_match_id}.json"
        else:
            sample_file = lineup_files[0]
        
        if not sample_file.exists():
            print(f"Sample file not found: {sample_file}")
            return
        
        print(f"Analyzing sample file: {sample_file.name}")
        
        try:
            with open(sample_file, 'r') as f:
                lineups_data = json.load(f)
            
            print(f"Sample file size: {sample_file.stat().st_size / 1024:.1f} KB")
            print(f"Number of teams: {len(lineups_data)}")
            print()
            
            # Analyze team lineups
            for i, team in enumerate(lineups_data):
                print(f"Team {i+1}:")
                print(f"  Name: {team.get('team_name', 'N/A')}")
                print(f"  Country: {team.get('country', {}).get('name', 'N/A')}")
                
                # Analyze lineup
                lineup = team.get('lineup', [])
                print(f"  Players: {len(lineup)}")
                
                if lineup:
                    # Sample player
                    sample_player = lineup[0]
                    print(f"  Sample player: {sample_player.get('player_name', 'N/A')}")
                    print(f"  Position: {sample_player.get('position', {}).get('name', 'N/A')}")
                    print(f"  Jersey number: {sample_player.get('jersey_number', 'N/A')}")
                print()
            
        except Exception as e:
            print(f"Error analyzing lineups data: {e}")
    
    def find_matches_with_tracking(self):
        """Find matches that have both events and tracking data"""
        print("=== Matches with Tracking Data ===")
        
        if not self.tracking_matches:
            print("No tracking matches loaded")
            return
        
        if not self.available_matches:
            print("No event matches loaded")
            return
        
        # Find intersection
        matches_with_tracking = set(self.tracking_matches) & set(self.available_matches)
        
        print(f"Total event matches: {len(self.available_matches)}")
        print(f"Total tracking matches: {len(self.tracking_matches)}")
        print(f"Matches with both: {len(matches_with_tracking)}")
        print(f"Coverage: {len(matches_with_tracking)/len(self.available_matches)*100:.1f}%")
        print()
        
        if matches_with_tracking:
            print("Sample matches with tracking data:")
            for match_id in list(matches_with_tracking)[:10]:
                print(f"  {match_id}")
        
        return list(matches_with_tracking)
    
    def create_data_summary(self):
        """Create a comprehensive data summary"""
        print("=== StatsBomb Data Summary ===")
        
        summary = {
            'total_competitions': len(self.competitions),
            'total_event_matches': len(self.available_matches),
            'total_tracking_matches': len(self.tracking_matches),
            'data_structure': {
                'competitions': 'JSON format, competition and season information',
                'events': 'JSON format, detailed event data with locations',
                'lineups': 'JSON format, team lineups and formations',
                'tracking': 'JSON format, StatsBomb 360 tracking data'
            },
            'tracking_data_features': {
                'player_locations': 'x, y coordinates for all players',
                'team_identification': 'teammate true/false flags',
                'actor_identification': 'actor true/false for event performers',
                'field_boundaries': 'visible_area coordinates',
                'high_resolution': 'Detailed positional data'
            },
            'data_quality': {
                'professional_standard': 'StatsBomb is industry-leading',
                'comprehensive_coverage': 'Events, tracking, lineups, metadata',
                'multiple_leagues': 'Bundesliga, La Liga, Premier League, etc.',
                'multiple_seasons': '2023/2024, 2022/2023, etc.'
            }
        }
        
        print(json.dumps(summary, indent=2))
        
        return summary
    
    def generate_integration_recommendations(self):
        """Generate recommendations for integrating StatsBomb data with our TDA analysis"""
        print("=== Integration Recommendations ===")
        
        recommendations = [
            "1. Data Format Adaptation:",
            "   - Parse StatsBomb JSON format for events and tracking",
            "   - Extract player positions from freeze_frame data",
            "   - Handle team identification using teammate flags",
            "   - Process visible_area for field boundaries",
            "",
            "2. TDA Pipeline Enhancement:",
            "   - Adapt existing TDA code for StatsBomb format",
            "   - Implement freeze_frame position extraction",
            "   - Add event correlation with tracking data",
            "   - Integrate lineup information for player identification",
            "",
            "3. Multi-League Analysis:",
            "   - Compare tactical patterns across different leagues",
            "   - Analyze formation evolution across seasons",
            "   - Identify league-specific tactical characteristics",
            "   - Validate TDA consistency across football cultures",
            "",
            "4. Advanced Applications:",
            "   - Event-correlated TDA analysis",
            "   - Formation change detection during matches",
            "   - Possession-based formation analysis",
            "   - Performance prediction using TDA metrics",
            "",
            "5. Implementation Priority:",
            "   - Start with matches that have both events and tracking",
            "   - Focus on high-quality leagues (Bundesliga, La Liga)",
            "   - Gradually expand to full dataset analysis",
            "   - Develop automated pipeline for batch processing"
        ]
        
        for rec in recommendations:
            print(rec)
    
    def run_full_exploration(self):
        """Run the complete data exploration"""
        print("StatsBomb Data Exploration")
        print("=" * 50)
        
        # Load competitions
        self.load_competitions()
        
        # Explore tracking data
        self.explore_tracking_data()
        
        # Explore events data
        self.explore_events_data()
        
        # Explore lineups data
        self.explore_lineups_data()
        
        # Find matches with tracking
        matches_with_tracking = self.find_matches_with_tracking()
        
        # Create summary
        self.create_data_summary()
        
        # Generate recommendations
        self.generate_integration_recommendations()
        
        return {
            'competitions': self.competitions,
            'event_matches': self.available_matches,
            'tracking_matches': self.tracking_matches,
            'matches_with_tracking': matches_with_tracking
        }

def main():
    """Main function to run the exploration"""
    explorer = StatsBombDataExplorer()
    results = explorer.run_full_exploration()
    
    print("\n=== Exploration Complete ===")
    print(f"Found {len(results['matches_with_tracking'])} matches with tracking data")
    print("Ready for TDA analysis integration!")

if __name__ == "__main__":
    main()
