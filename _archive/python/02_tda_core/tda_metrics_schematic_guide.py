#!/usr/bin/env python3
"""
TDA Metrics Schematic Guide
Visual explanations of TDA concepts for non-technical audiences
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
from matplotlib.collections import LineCollection
import seaborn as sns

# Set professional style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class TDAMetricsSchematic:
    def __init__(self):
        """Initialize schematic guide"""
        self.colors = {
            'players': '#FF6B6B',
            'clusters': '#4ECDC4', 
            'connections': '#45B7D1',
            'formations': '#96CEB4',
            'text': '#2C3E50'
        }
    
    def create_h0_explanation_schematic(self):
        """Create schematic explaining H0 (Connected Components)"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('H0 (Connected Components): What Does It Mean?', 
                     fontsize=18, fontweight='bold')
        
        # Panel 1: Individual Players (Before Clustering)
        ax1 = axes[0, 0]
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw individual players as dots
        player_positions = [(2, 8), (3, 7), (4, 6), (6, 8), (7, 7), (8, 6), 
                           (2, 3), (3, 2), (4, 1), (6, 3), (7, 2), (8, 1)]
        
        for i, (x, y) in enumerate(player_positions):
            circle = Circle((x, y), 0.3, color=self.colors['players'], alpha=0.8)
            ax1.add_patch(circle)
            ax1.text(x, y-0.6, f'P{i+1}', ha='center', va='top', fontsize=8, fontweight='bold')
        
        ax1.set_title('Individual Players\n(22 separate points)', fontsize=14, fontweight='bold')
        ax1.text(5, 0.5, 'H0 = 22 (Artifact: Just counting players)', 
                ha='center', va='center', fontsize=12, color='red', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Panel 2: Clustered Players (After GPS-Aware Clustering)
        ax2 = axes[0, 1]
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        # Define clusters
        clusters = [
            {'center': (2.5, 7), 'players': [(2, 8), (3, 7), (4, 6)], 'color': '#FF6B6B'},
            {'center': (7, 7), 'players': [(6, 8), (7, 7), (8, 6)], 'color': '#4ECDC4'},
            {'center': (2.5, 2), 'players': [(2, 3), (3, 2), (4, 1)], 'color': '#45B7D1'},
            {'center': (7, 2), 'players': [(6, 3), (7, 2), (8, 1)], 'color': '#96CEB4'},
            {'center': (5, 5), 'players': [(5, 5)], 'color': '#FFEAA7'}
        ]
        
        for i, cluster in enumerate(clusters):
            # Draw cluster boundary
            cluster_circle = Circle(cluster['center'], 1.2, 
                                   fill=False, color=cluster['color'], 
                                   linewidth=3, alpha=0.8)
            ax2.add_patch(cluster_circle)
            
            # Draw players in cluster
            for x, y in cluster['players']:
                player_circle = Circle((x, y), 0.3, color=cluster['color'], alpha=0.8)
                ax2.add_patch(player_circle)
            
            # Label cluster
            ax2.text(cluster['center'][0], cluster['center'][1], f'C{i+1}', 
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
        
        ax2.set_title('GPS-Aware Clustering\n(5 distinct groups)', fontsize=14, fontweight='bold')
        ax2.text(5, 0.5, 'H0 = 5 (Meaningful: Number of player groups)', 
                ha='center', va='center', fontsize=12, color='green', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Panel 3: Real Football Example
        ax3 = axes[1, 0]
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        # Draw football field
        field = Rectangle((1, 1), 8, 8, fill=False, color='black', linewidth=2)
        ax3.add_patch(field)
        
        # Draw goal areas
        goal1 = Rectangle((0.5, 3), 0.5, 4, fill=False, color='black', linewidth=2)
        goal2 = Rectangle((9, 3), 0.5, 4, fill=False, color='black', linewidth=2)
        ax3.add_patch(goal1)
        ax3.add_patch(goal2)
        
        # Draw player formations
        # Home team (blue)
        home_positions = [(2, 2), (2.5, 3), (2, 4), (2.5, 5), (2, 6), (2.5, 7), (2, 8)]
        for x, y in home_positions:
            circle = Circle((x, y), 0.2, color='blue', alpha=0.8)
            ax3.add_patch(circle)
        
        # Away team (red)
        away_positions = [(8, 2), (7.5, 3), (8, 4), (7.5, 5), (8, 6), (7.5, 7), (8, 8)]
        for x, y in away_positions:
            circle = Circle((x, y), 0.2, color='red', alpha=0.8)
            ax3.add_patch(circle)
        
        # Draw cluster boundaries
        home_cluster = Circle((2.25, 5), 1.5, fill=False, color='blue', linewidth=2, alpha=0.6)
        away_cluster = Circle((7.75, 5), 1.5, fill=False, color='red', linewidth=2, alpha=0.6)
        ax3.add_patch(home_cluster)
        ax3.add_patch(away_cluster)
        
        ax3.set_title('Real Football Example\nH0 = 2 (Home vs Away formations)', 
                     fontsize=14, fontweight='bold')
        ax3.text(5, 0.5, 'H0 tells us how many distinct\nteam formations exist', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        ax3.set_xticks([])
        ax3.set_yticks([])
        
        # Panel 4: Interpretation Guide
        ax4 = axes[1, 1]
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        # Create interpretation boxes
        interpretations = [
            {'text': 'H0 = 1\nSingle formation\n(All players together)', 'y': 8, 'color': 'lightgreen'},
            {'text': 'H0 = 2-3\nFew formations\n(Simple tactics)', 'y': 6, 'color': 'lightblue'},
            {'text': 'H0 = 4-6\nMultiple formations\n(Complex tactics)', 'y': 4, 'color': 'lightyellow'},
            {'text': 'H0 = 7+\nMany formations\n(Very complex tactics)', 'y': 2, 'color': 'lightcoral'}
        ]
        
        for interp in interpretations:
            box = Rectangle((1, interp['y']-0.5), 8, 1, 
                           facecolor=interp['color'], alpha=0.7, edgecolor='black')
            ax4.add_patch(box)
            ax4.text(5, interp['y'], interp['text'], ha='center', va='center', 
                    fontsize=11, fontweight='bold')
        
        ax4.set_title('H0 Interpretation Guide\nWhat the numbers mean', 
                     fontsize=14, fontweight='bold')
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('h0_explanation_schematic.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_h1_explanation_schematic(self):
        """Create schematic explaining H1 (Formation Complexity)"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('H1 (Formation Complexity): What Does It Mean?', 
                     fontsize=18, fontweight='bold')
        
        # Panel 1: Simple Formation (H1 = 0)
        ax1 = axes[0, 0]
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw simple line formation
        positions = [(2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5)]
        for i, (x, y) in enumerate(positions):
            circle = Circle((x, y), 0.3, color=self.colors['players'], alpha=0.8)
            ax1.add_patch(circle)
            ax1.text(x, y-0.6, f'P{i+1}', ha='center', va='top', fontsize=8, fontweight='bold')
        
        # Draw connections
        for i in range(len(positions)-1):
            ax1.plot([positions[i][0], positions[i+1][0]], 
                    [positions[i][1], positions[i+1][1]], 
                    'k-', linewidth=2, alpha=0.6)
        
        ax1.set_title('Simple Formation\n(Straight line)', fontsize=14, fontweight='bold')
        ax1.text(5, 1, 'H1 = 0\n(No holes or loops)', 
                ha='center', va='center', fontsize=12, color='green', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Panel 2: Complex Formation (H1 = 1)
        ax2 = axes[0, 1]
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        # Draw triangular formation
        positions = [(3, 7), (5, 5), (7, 7), (4, 3), (6, 3)]
        for i, (x, y) in enumerate(positions):
            circle = Circle((x, y), 0.3, color=self.colors['players'], alpha=0.8)
            ax2.add_patch(circle)
            ax1.text(x, y-0.6, f'P{i+1}', ha='center', va='top', fontsize=8, fontweight='bold')
        
        # Draw triangular connections
        triangle_edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 1)]
        for start, end in triangle_edges:
            ax2.plot([positions[start][0], positions[end][0]], 
                    [positions[start][1], positions[end][1]], 
                    'k-', linewidth=2, alpha=0.6)
        
        # Highlight the hole
        hole = Circle((5, 5.5), 0.8, fill=False, color='red', linewidth=3, alpha=0.8)
        ax2.add_patch(hole)
        ax2.text(5, 5.5, 'HOLE', ha='center', va='center', fontsize=10, 
                color='red', fontweight='bold')
        
        ax2.set_title('Complex Formation\n(Triangular with hole)', fontsize=14, fontweight='bold')
        ax2.text(5, 1, 'H1 = 1\n(1 hole in formation)', 
                ha='center', va='center', fontsize=12, color='orange', fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.7))
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Panel 3: Football Formation Examples
        ax3 = axes[1, 0]
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        # Draw football field
        field = Rectangle((1, 1), 8, 8, fill=False, color='black', linewidth=2)
        ax3.add_patch(field)
        
        # Draw 4-4-2 formation
        # Back line
        back_line = [(2, 2), (3, 2), (4, 2), (5, 2)]
        # Midfield
        midfield = [(2, 4), (3, 4), (4, 4), (5, 4)]
        # Forwards
        forwards = [(3, 6), (4, 6)]
        
        all_positions = back_line + midfield + forwards
        
        for i, (x, y) in enumerate(all_positions):
            circle = Circle((x, y), 0.15, color='blue', alpha=0.8)
            ax3.add_patch(circle)
        
        # Draw formation lines
        ax3.plot([2, 5], [2, 2], 'b-', linewidth=2, alpha=0.6)  # Back line
        ax3.plot([2, 5], [4, 4], 'b-', linewidth=2, alpha=0.6)  # Midfield
        ax3.plot([3, 4], [6, 6], 'b-', linewidth=2, alpha=0.6)  # Forwards
        
        ax3.set_title('4-4-2 Formation\nH1 = 2 (2 holes between lines)', 
                     fontsize=14, fontweight='bold')
        ax3.text(5, 0.5, 'H1 measures formation\nstructural complexity', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        ax3.set_xticks([])
        ax3.set_yticks([])
        
        # Panel 4: H1 Interpretation Guide
        ax4 = axes[1, 1]
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        interpretations = [
            {'text': 'H1 = 0\nSimple formations\n(Straight lines)', 'y': 8, 'color': 'lightgreen'},
            {'text': 'H1 = 1-2\nModerate complexity\n(Basic shapes)', 'y': 6, 'color': 'lightblue'},
            {'text': 'H1 = 3-4\nComplex formations\n(Multiple holes)', 'y': 4, 'color': 'lightyellow'},
            {'text': 'H1 = 5+\nVery complex\n(Many structural holes)', 'y': 2, 'color': 'lightcoral'}
        ]
        
        for interp in interpretations:
            box = Rectangle((1, interp['y']-0.5), 8, 1, 
                           facecolor=interp['color'], alpha=0.7, edgecolor='black')
            ax4.add_patch(box)
            ax4.text(5, interp['y'], interp['text'], ha='center', va='center', 
                    fontsize=11, fontweight='bold')
        
        ax4.set_title('H1 Interpretation Guide\nFormation complexity levels', 
                     fontsize=14, fontweight='bold')
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('h1_explanation_schematic.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_complexity_index_explanation(self):
        """Create schematic explaining Complexity Index"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Complexity Index: Combining H0 and H1', 
                     fontsize=18, fontweight='bold')
        
        # Panel 1: Formula Explanation
        ax1 = axes[0, 0]
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw formula
        ax1.text(5, 8, 'Complexity Index =', ha='center', va='center', 
                fontsize=16, fontweight='bold')
        ax1.text(5, 6.5, 'H0 + H1', ha='center', va='center', 
                fontsize=20, fontweight='bold', color='blue')
        ax1.text(5, 5, 'Point Cloud Size', ha='center', va='center', 
                fontsize=16, fontweight='bold')
        
        # Draw division line
        ax1.plot([2, 8], [5.5, 5.5], 'k-', linewidth=3)
        
        # Add explanation
        ax1.text(5, 3, 'Measures overall tactical complexity\nper player in the formation', 
                ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        
        ax1.set_title('Complexity Index Formula', fontsize=14, fontweight='bold')
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Panel 2: Example Calculation
        ax2 = axes[0, 1]
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        # Example values
        h0_example = 5
        h1_example = 3
        point_cloud_size = 22
        
        complexity = (h0_example + h1_example) / point_cloud_size
        
        ax2.text(5, 8, 'Example Calculation:', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        ax2.text(5, 6.5, f'H0 = {h0_example}', ha='center', va='center', 
                fontsize=16, fontweight='bold', color='green')
        ax2.text(5, 5.5, f'H1 = {h1_example}', ha='center', va='center', 
                fontsize=16, fontweight='bold', color='orange')
        ax2.text(5, 4.5, f'Point Cloud Size = {point_cloud_size}', ha='center', va='center', 
                fontsize=16, fontweight='bold', color='blue')
        
        ax2.plot([2, 8], [4, 4], 'k-', linewidth=3)
        
        ax2.text(5, 3, f'Complexity = {complexity:.4f}', ha='center', va='center', 
                fontsize=18, fontweight='bold', color='red',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
        
        ax2.set_title('Example Calculation', fontsize=14, fontweight='bold')
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Panel 3: Complexity Levels
        ax3 = axes[1, 0]
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        complexity_levels = [
            {'range': '0.00 - 0.05', 'description': 'Very Simple\n(Basic formations)', 'color': 'lightgreen'},
            {'range': '0.05 - 0.10', 'description': 'Simple\n(Standard tactics)', 'color': 'lightblue'},
            {'range': '0.10 - 0.15', 'description': 'Moderate\n(Complex tactics)', 'color': 'lightyellow'},
            {'range': '0.15 - 0.20', 'description': 'Complex\n(Advanced tactics)', 'color': 'lightcoral'},
            {'range': '0.20+', 'description': 'Very Complex\n(Elite tactics)', 'color': 'lightpink'}
        ]
        
        for i, level in enumerate(complexity_levels):
            y_pos = 8 - i * 1.5
            box = Rectangle((1, y_pos-0.4), 8, 0.8, 
                           facecolor=level['color'], alpha=0.7, edgecolor='black')
            ax3.add_patch(box)
            ax3.text(2, y_pos, level['range'], ha='left', va='center', 
                    fontsize=12, fontweight='bold')
            ax3.text(6, y_pos, level['description'], ha='center', va='center', 
                    fontsize=11, fontweight='bold')
        
        ax3.set_title('Complexity Index Levels', fontsize=14, fontweight='bold')
        ax3.set_xticks([])
        ax3.set_yticks([])
        
        # Panel 4: Real-World Example
        ax4 = axes[1, 1]
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        # Draw football field
        field = Rectangle((1, 1), 8, 8, fill=False, color='black', linewidth=2)
        ax4.add_patch(field)
        
        # Draw formation with complexity
        # Multiple clusters (H0 = 4)
        clusters = [
            {'center': (2, 2), 'size': 0.3, 'color': 'blue'},  # Defense
            {'center': (5, 4), 'size': 0.3, 'color': 'blue'},  # Midfield
            {'center': (3, 6), 'size': 0.3, 'color': 'blue'},  # Attack
            {'center': (7, 6), 'size': 0.3, 'color': 'blue'}   # Wing
        ]
        
        for i, cluster in enumerate(clusters):
            circle = Circle(cluster['center'], cluster['size'], 
                          color=cluster['color'], alpha=0.8)
            ax4.add_patch(circle)
            ax4.text(cluster['center'][0], cluster['center'][1]-0.6, f'C{i+1}', 
                    ha='center', va='top', fontsize=10, fontweight='bold')
        
        # Draw connections (H1 = 2)
        connections = [(0, 1), (1, 2), (1, 3)]
        cluster_positions = [cluster['center'] for cluster in clusters]
        
        for start, end in connections:
            ax4.plot([cluster_positions[start][0], cluster_positions[end][0]], 
                    [cluster_positions[start][1], cluster_positions[end][1]], 
                    'k-', linewidth=2, alpha=0.6)
        
        ax4.set_title('Real Formation Example\nH0=4, H1=2, Complexity=0.27', 
                     fontsize=14, fontweight='bold')
        ax4.text(5, 0.5, 'High complexity formation\nwith multiple tactical elements', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('complexity_index_explanation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_quantum_states_explanation(self):
        """Create schematic explaining Quantum States (Tactical States)"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Tactical States: What Are They?', 
                     fontsize=18, fontweight='bold')
        
        # Panel 1: State Concept
        ax1 = axes[0, 0]
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw state diagram
        states = [
            {'name': 'State 0\nDefensive', 'pos': (2, 8), 'color': '#FF6B6B'},
            {'name': 'State 1\nCounter-Attack', 'pos': (8, 8), 'color': '#4ECDC4'},
            {'name': 'State 2\nPossession', 'pos': (2, 2), 'color': '#45B7D1'},
            {'name': 'State 3\nHigh Press', 'pos': (8, 2), 'color': '#96CEB4'},
            {'name': 'State 4\nTransition', 'pos': (5, 5), 'color': '#FFEAA7'}
        ]
        
        for state in states:
            circle = Circle(state['pos'], 0.8, color=state['color'], alpha=0.8)
            ax1.add_patch(circle)
            ax1.text(state['pos'][0], state['pos'][1], state['name'], 
                    ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw transitions
        transitions = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3)]
        for start, end in transitions:
            ax1.plot([states[start]['pos'][0], states[end]['pos'][0]], 
                    [states[start]['pos'][1], states[end]['pos'][1]], 
                    'k--', linewidth=1, alpha=0.5)
        
        ax1.set_title('Tactical States\n(Team formation patterns)', fontsize=14, fontweight='bold')
        ax1.text(5, 0.5, 'Teams switch between different\ntactical states during matches', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Panel 2: State Frequencies
        ax2 = axes[0, 1]
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        state_names = ['Defensive', 'Counter\nAttack', 'Possession', 'High Press', 'Transition']
        frequencies = [0.234, 0.198, 0.187, 0.201, 0.180]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        y_positions = np.arange(1, 6) * 1.5
        
        for i, (name, freq, color, y) in enumerate(zip(state_names, frequencies, colors, y_positions)):
            bar_width = freq * 8
            bar = Rectangle((1, y-0.3), bar_width, 0.6, 
                           facecolor=color, alpha=0.8, edgecolor='black')
            ax2.add_patch(bar)
            ax2.text(0.5, y, name, ha='right', va='center', fontsize=10, fontweight='bold')
            ax2.text(bar_width + 1.2, y, f'{freq:.3f}', ha='left', va='center', 
                    fontsize=10, fontweight='bold')
        
        ax2.set_title('State Frequencies\n(How often each state occurs)', 
                     fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 8)
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Panel 3: Energy Landscapes
        ax3 = axes[1, 0]
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        # Draw energy landscape
        x = np.linspace(0, 10, 100)
        y = 5 + 2 * np.sin(x * 0.8) + 0.5 * np.sin(x * 2.5)
        
        ax3.plot(x, y, 'b-', linewidth=3, alpha=0.8)
        ax3.fill_between(x, y, alpha=0.3, color='blue')
        
        # Mark state positions
        state_x = [2, 4, 6, 8, 5]
        state_y = [5 + 2 * np.sin(x * 0.8) + 0.5 * np.sin(x * 2.5) for x in state_x]
        
        for i, (x_pos, y_pos) in enumerate(zip(state_x, state_y)):
            circle = Circle((x_pos, y_pos), 0.2, color=colors[i], alpha=0.8)
            ax3.add_patch(circle)
            ax3.text(x_pos, y_pos-0.5, f'S{i}', ha='center', va='top', 
                    fontsize=10, fontweight='bold')
        
        ax3.set_title('Energy Landscapes\n(State stability)', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Tactical Configuration')
        ax3.set_ylabel('Energy Level')
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Transition Probabilities
        ax4 = axes[1, 1]
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        # Draw transition matrix visualization
        transitions = [
            {'from': 'Defensive', 'to': 'Counter', 'prob': 0.234, 'color': '#FF6B6B'},
            {'from': 'Counter', 'to': 'Possession', 'prob': 0.198, 'color': '#4ECDC4'},
            {'from': 'Possession', 'to': 'High Press', 'prob': 0.187, 'color': '#45B7D1'},
            {'from': 'High Press', 'to': 'Transition', 'prob': 0.201, 'color': '#96CEB4'},
            {'from': 'Transition', 'to': 'Defensive', 'prob': 0.180, 'color': '#FFEAA7'}
        ]
        
        y_positions = np.arange(1, 6) * 1.5
        
        for i, (trans, y) in enumerate(zip(transitions, y_positions)):
            # Draw transition arrow
            ax4.arrow(2, y, 4, 0, head_width=0.2, head_length=0.3, 
                     fc=trans['color'], ec=trans['color'], alpha=0.8)
            
            # Draw probability bar
            bar_width = trans['prob'] * 3
            bar = Rectangle((6.5, y-0.2), bar_width, 0.4, 
                           facecolor=trans['color'], alpha=0.8, edgecolor='black')
            ax4.add_patch(bar)
            
            # Labels
            ax4.text(1, y, f"{trans['from']} →", ha='right', va='center', 
                    fontsize=9, fontweight='bold')
            ax4.text(6.5 + bar_width + 0.2, y, f'{trans["prob"]:.3f}', 
                    ha='left', va='center', fontsize=9, fontweight='bold')
        
        ax4.set_title('Transition Probabilities\n(How states change)', 
                     fontsize=14, fontweight='bold')
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 8)
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('quantum_states_explanation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def create_nash_equilibrium_explanation(self):
        """Create schematic explaining Nash Equilibrium"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Nash Equilibrium: What Does It Mean?', 
                     fontsize=18, fontweight='bold')
        
        # Panel 1: Game Theory Concept
        ax1 = axes[0, 0]
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw payoff matrix
        ax1.text(5, 9, 'Game Theory: Team Formation Strategies', 
                ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Draw matrix
        matrix_x = 2
        matrix_y = 6
        matrix_width = 6
        matrix_height = 3
        
        # Matrix background
        matrix_bg = Rectangle((matrix_x, matrix_y), matrix_width, matrix_height, 
                             facecolor='lightblue', alpha=0.3, edgecolor='black', linewidth=2)
        ax1.add_patch(matrix_bg)
        
        # Matrix labels
        ax1.text(matrix_x + 1, matrix_y + 2.5, 'Home Team', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(matrix_x + 3, matrix_y + 2.5, 'Narrow\n(11.44m)', ha='center', va='center', 
                fontsize=10, fontweight='bold')
        ax1.text(matrix_x + 5, matrix_y + 2.5, 'Wide\n(12.90m)', ha='center', va='center', 
                fontsize=10, fontweight='bold')
        
        ax1.text(matrix_x + 0.5, matrix_y + 1.5, 'Away\nTeam', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(matrix_x + 0.5, matrix_y + 0.5, 'Narrow', ha='center', va='center', 
                fontsize=10, fontweight='bold')
        
        # Payoff values
        ax1.text(matrix_x + 3, matrix_y + 1.5, '3, 3', ha='center', va='center', 
                fontsize=12, fontweight='bold', color='green')
        ax1.text(matrix_x + 5, matrix_y + 1.5, '1, 4', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(matrix_x + 3, matrix_y + 0.5, '4, 1', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        ax1.text(matrix_x + 5, matrix_y + 0.5, '2, 2', ha='center', va='center', 
                fontsize=12, fontweight='bold')
        
        # Highlight Nash equilibrium
        nash_box = Rectangle((matrix_x + 2.5, matrix_y + 1), 1, 1, 
                           fill=False, color='red', linewidth=3)
        ax1.add_patch(nash_box)
        
        ax1.text(5, 3, 'Nash Equilibrium: Both teams choose optimal strategies\n(11.44m vs 12.90m formation width)', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        
        ax1.set_title('Game Theory Matrix', fontsize=14, fontweight='bold')
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # Panel 2: Formation Width Visualization
        ax2 = axes[0, 1]
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        # Draw football field
        field = Rectangle((1, 1), 8, 8, fill=False, color='black', linewidth=2)
        ax2.add_patch(field)
        
        # Draw home team formation (narrow)
        home_positions = [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)]
        for x, y in home_positions:
            circle = Circle((x, y), 0.2, color='blue', alpha=0.8)
            ax2.add_patch(circle)
        
        # Draw away team formation (wide)
        away_positions = [(8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
        for x, y in away_positions:
            circle = Circle((x, y), 0.2, color='red', alpha=0.8)
            ax2.add_patch(circle)
        
        # Draw formation width lines
        ax2.plot([1.5, 1.5], [1, 9], 'b-', linewidth=3, alpha=0.6, label='Home: 11.44m')
        ax2.plot([8.5, 8.5], [1, 9], 'r-', linewidth=3, alpha=0.6, label='Away: 12.90m')
        
        ax2.set_title('Nash Equilibrium Formations\n(Optimal strategies)', fontsize=14, fontweight='bold')
        ax2.text(5, 0.5, 'Each team chooses the formation width\nthat maximizes their advantage', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        ax2.legend()
        ax2.set_xticks([])
        ax2.set_yticks([])
        
        # Panel 3: Zero-Sum Relationship
        ax3 = axes[1, 0]
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        
        # Draw zero-sum relationship
        time_points = np.arange(0, 10, 0.5)
        home_spread = 11.44 + 2 * np.sin(time_points * 0.5)
        away_spread = 12.90 - 2 * np.sin(time_points * 0.5)
        total_spread = home_spread + away_spread
        
        ax3.plot(time_points, home_spread, 'b-', linewidth=3, label='Home Team Spread', alpha=0.8)
        ax3.plot(time_points, away_spread, 'r-', linewidth=3, label='Away Team Spread', alpha=0.8)
        ax3.plot(time_points, total_spread, 'purple', linewidth=3, label='Total Strategy', alpha=0.8)
        
        ax3.axhline(y=24.34, color='purple', linestyle='--', alpha=0.7,
                   label=f'Conservation Law: {24.34:.2f}m')
        
        ax3.set_xlabel('Time (minutes)')
        ax3.set_ylabel('Formation Width (metres)')
        ax3.set_title('Zero-Sum Relationship\n(Competitive balance)', fontsize=14, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Competitive Balance
        ax4 = axes[1, 1]
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        
        # Draw balance scale
        scale_center = (5, 7)
        scale_arm_length = 3
        
        # Draw scale
        ax4.plot([scale_center[0] - scale_arm_length, scale_center[0] + scale_arm_length], 
                [scale_center[1], scale_center[1]], 'k-', linewidth=4)
        ax4.plot([scale_center[0], scale_center[0]], [scale_center[1], scale_center[1] - 2], 
                'k-', linewidth=4)
        
        # Draw pans
        left_pan = Circle((scale_center[0] - scale_arm_length, scale_center[1] - 0.5), 0.8, 
                         fill=False, color='blue', linewidth=3)
        right_pan = Circle((scale_center[0] + scale_arm_length, scale_center[1] - 0.5), 0.8, 
                          fill=False, color='red', linewidth=3)
        ax4.add_patch(left_pan)
        ax4.add_patch(right_pan)
        
        # Add weights
        ax4.text(scale_center[0] - scale_arm_length, scale_center[1] - 1.5, '11.44m', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='blue')
        ax4.text(scale_center[0] + scale_arm_length, scale_center[1] - 1.5, '12.90m', 
                ha='center', va='center', fontsize=12, fontweight='bold', color='red')
        
        ax4.set_title('Competitive Balance\n(Zero-sum equilibrium)', fontsize=14, fontweight='bold')
        ax4.text(5, 2, 'Teams maintain competitive balance\nthrough optimal strategy choices', 
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('nash_equilibrium_explanation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def generate_all_schematics(self):
        """Generate all metric explanation schematics"""
        print("🎨 Generating TDA metrics schematic guide...")
        
        print("📊 Creating H0 explanation schematic...")
        self.create_h0_explanation_schematic()
        
        print("📈 Creating H1 explanation schematic...")
        self.create_h1_explanation_schematic()
        
        print("🧮 Creating complexity index explanation...")
        self.create_complexity_index_explanation()
        
        print("⚛️ Creating quantum states explanation...")
        self.create_quantum_states_explanation()
        
        print("🎮 Creating Nash equilibrium explanation...")
        self.create_nash_equilibrium_explanation()
        
        print("✅ All metric schematics generated successfully!")
        print("📁 Files saved:")
        print("   - h0_explanation_schematic.png")
        print("   - h1_explanation_schematic.png")
        print("   - complexity_index_explanation.png")
        print("   - quantum_states_explanation.png")
        print("   - nash_equilibrium_explanation.png")

def main():
    """Main execution function"""
    print("🚀 TDA Metrics Schematic Guide")
    print("=" * 35)
    
    # Initialize schematic guide
    schematic_guide = TDAMetricsSchematic()
    
    # Generate all schematics
    schematic_guide.generate_all_schematics()
    
    print("\n🎯 Schematic guide complete!")
    print("These visualisations explain:")
    print("✅ H0 (Connected Components) - What it means")
    print("✅ H1 (Formation Complexity) - How it works")
    print("✅ Complexity Index - How it's calculated")
    print("✅ Tactical States - What they represent")
    print("✅ Nash Equilibrium - Why it matters")

if __name__ == "__main__":
    main()
