"""
TheFootballManager

Features:
- Team and player management
- Match simulations
- Transfer market
- Advanced statistics and analysis
- League management
- Historical data tracking
"""

import json
import csv
import random
import math
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
from pathlib import Path

class TransferMarket:
    def __init__(self, data: Dict):
        self.data = data
        self.transfer_history = []
        
    def calculate_player_value(self, player: Dict) -> int:
        """Calculate player's market value based on stats, age, and rating."""
        base_value = player['rating'] * 2000000  # Base value from rating
        
        #Age factor(peaks at 26)
        age_factor = 1 - (abs(26-player['age'])*0.05)
        
        #Performance factor
        stats = player['stats']
        performance_factor = (stats['goals']*500000 + stats['assists']*300000 + stats['minutes_played']/ 90 * 100000)
        
        return int(base_value*age_factor + performance_factor)
        
    def transfer_player(self, player_name: str, new_team: str) -> Dict:
        """Transfer a player to a new team."""
        player = next((p for p in self.data['players'] 
                      if p['name'].lower() == player_name.lower()), None)
        if not player:
            raise ValueError(f"Player {player_name} not found")
            
        team = next((t for t in self.data['teams'] if t['name'].lower() == new_team.lower()), None)
        if not team:
            raise ValueError(f"Team {new_team} not found")
            
        old_team = player['team']
        player['team'] = new_team
        
        transfer_fee = self.calculate_player_value(player)
        
        transfer_record = {
            'player': player['name'],
            'from_team': old_team,
            'to_team': new_team,
            'fee': transfer_fee,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.transfer_history.append(transfer_record)
        return transfer_record

class MatchEngine:
    def __init__(self, data: Dict):
        self.data = data
        self.match_history = []
        
    def calculate_team_strength(self, team_name: str) -> float:
        """Calculate overall team strength based on players."""
        team_players = [p for p in self.data['players'] if p['team'] == team_name]
        if not team_players:
            raise ValueError(f"No players found for team {team_name}")
            
        total_rating = sum(p['rating'] for p in team_players)
        return total_rating / len(team_players)
        
    def simulate_match(self, home_team: str, away_team: str) -> Dict:
        """Simulate a match between two teams."""
        home = next((t for t in self.data['teams'] if t['name'].lower() == home_team.lower()), None)
        away = next((t for t in self.data['teams'] if t['name'].lower() == away_team.lower()), None)
                    
        if not home or not away:
            raise ValueError("Team not found")
            
        home_strength = self.calculate_team_strength(home['name'])
        away_strength = self.calculate_team_strength(away['name'])
        
        # Home advantage factor
        home_strength *= 1.1
        
        # Simulate goals based on team strengths
        home_goals = max(0, int(random.gauss(home_strength/20, 1)))
        away_goals = max(0, int(random.gauss(away_strength/20, 1)))
        
        # Generate match events
        events = self.generate_match_events(home['name'], away['name'], home_goals, away_goals)
        
        match_result = {
            'home_team': home['name'],
            'away_team': away['name'],
            'home_goals': home_goals,
            'away_goals': away_goals,
            'events': events,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.match_history.append(match_result)
        self.update_stats(match_result)
        
        return match_result
        
    def generate_match_events(self, home_team: str, away_team: str, home_goals: int, away_goals: int) -> List[Dict]:
        """Generate detailed match events."""
        events = []
        home_players = [p for p in self.data['players'] if p['team'] == home_team]
        away_players = [p for p in self.data['players'] if p['team'] == away_team]
        
        # Generate goal events
        for _ in range(home_goals):
            minute = random.randint(1, 90)
            scorer = random.choice(home_players)
            assist = random.choice(home_players)
            while assist == scorer:
                assist = random.choice(home_players)
                
            events.append({
                'minute': minute,
                'type': 'goal',
                'team': home_team,
                'scorer': scorer['name'],
                'assist': assist['name']
            })
            
        for _ in range(away_goals):
            minute = random.randint(1, 90)
            scorer = random.choice(away_players)
            assist = random.choice(away_players)
            while assist == scorer:
                assist = random.choice(away_players)
                
            events.append({
                'minute': minute,
                'type': 'goal',
                'team': away_team,
                'scorer': scorer['name'],
                'assist': assist['name']
            })
            
        # Sort events by minute
        events.sort(key=lambda x: x['minute'])
        return events
        
    def update_stats(self, match_result: Dict) -> None:
        """Update player and team statistics after a match."""
        for event in match_result['events']:
            if event['type'] == 'goal':
                # Update scorer stats
                scorer = next(p for p in self.data['players'] if p['name'] == event['scorer'])
                scorer['stats']['goals'] += 1
                
                # Update assist stats
                assister = next(p for p in self.data['players'] if p['name'] == event['assist'])
                assister['stats']['assists'] += 1

class Analytics:
    def __init__(self, data: Dict):
        self.data = data
        
    def calculate_player_efficiency(self, player_name: str) -> Dict:
        """Calculate advanced efficiency metrics for a player."""
        player = next((p for p in self.data['players'] if p['name'].lower() == player_name.lower()), None)
        if not player:
            raise ValueError(f"Player {player_name} not found")
            
        stats = player['stats']
        minutes = stats['minutes_played']
        
        efficiency = {
            'goals_per_90': (stats['goals'] / minutes) * 90,
            'assists_per_90': (stats['assists'] / minutes) * 90,
            'goal_contributions': stats['goals'] + stats['assists'],
            'shots_conversion': (stats['goals'] / stats['shots_on_target'] * 100 if stats['shots_on_target'] > 0 else 0)
        }
        
        return efficiency
        
    def generate_team_report(self, team_name: str) -> Dict:
        """Generate comprehensive team analysis report."""
        team = next((t for t in self.data['teams'] if t['name'].lower() == team_name.lower()), None)
        if not team:
            raise ValueError(f"Team {team_name} not found")
            
        players = [p for p in self.data['players'] if p['team'] == team['name']]
        
        report = {
            'team_name': team['name'],
            'league_position': team['league_position'],
            'points': team['points'],
            'top_scorer': max(players, key=lambda p: p['stats']['goals']),
            'top_assister': max(players, key=lambda p: p['stats']['assists']),
            'squad_age_average': sum(p['age'] for p in players) / len(players),
            'squad_rating_average': sum(p['rating'] for p in players) / len(players)
        }
        
        return report

def load_data(filename: str) -> Dict:
    """Load football data from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        if not isinstance(data, dict):
            raise ValueError("Invalid data format: root must be a dictionary")
        if 'teams' not in data or 'players' not in data:
            raise ValueError("Invalid data format: missing teams or players")
            
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file '{filename}' not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in '{filename}': {str(e)}")

def save_data(data: Dict, filename: str) -> None:
    """Save football data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main() -> None:
    """Main function to run the Football Management System."""
    print("""
    ╔══════════════════════════════════════════════╗
    ║    Advanced Football Management System       ║
    ╚══════════════════════════════════════════════╝
    """)
    
    try:
        data = load_data('data.json')
        transfer_market = TransferMarket(data)
        match_engine = MatchEngine(data)
        analytics = Analytics(data)
        
        while True:
            print("\nMain Menu:")
            print("1. Player Management")
            print("2. Transfer Market")
            print("3. Match Simulation")
            print("4. Analytics")
            print("5. Save & Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                # Player Management Menu
                while True:
                    print("\nPlayer Management:")
                    print("1. Search Players")
                    print("2. View Player Details")
                    print("3. Update Player Stats")
                    print("4. Back to Main Menu")
                    
                    subchoice = input("\nEnter your choice (1-4): ")
                    
                    if subchoice == '1':
                        name = input("Enter player name (or press Enter to skip): ")
                        team = input("Enter team name (or press Enter to skip): ")
                        position = input("Enter position (or press Enter to skip): ")
                        rating_str = input("Enter minimum rating (or press Enter to skip): ")
                        
                        min_rating = int(rating_str) if rating_str.isdigit() else None
                        
                        results = [p for p in data['players'] 
                                 if (not name or name.lower() in p['name'].lower()) and
                                 (not team or team.lower() in p['team'].lower()) and
                                 (not position or position.lower() == p['position'].lower()) and
                                 (not min_rating or p['rating'] >= min_rating)]
                        
                        print("\nSearch Results:")
                        for player in results:
                            print(f"\n{player['name']} ({player['team']})")
                            print(f"Position: {player['position']}")
                            print(f"Rating: {player['rating']}")
                            
                    elif subchoice == '4':
                        break
                        
            elif choice == '2':
                # Transfer Market Menu
                while True:
                    print("\nTransfer Market:")
                    print("1. View Player Value")
                    print("2. Transfer Player")
                    print("3. View Transfer History")
                    print("4. Back to Main Menu")
                    
                    subchoice = input("\nEnter your choice (1-4): ")
                    
                    if subchoice == '1':
                        name = input("Enter player name: ")
                        try:
                            player = next(p for p in data['players'] 
                                        if p['name'].lower() == name.lower())
                            value = transfer_market.calculate_player_value(player)
                            print(f"\nEstimated value of {player['name']}: €{value:,}")
                        except StopIteration:
                            print(f"Player {name} not found")
                            
                    elif subchoice == '2':
                        player_name = input("Enter player name: ")
                        new_team = input("Enter new team: ")
                        try:
                            transfer = transfer_market.transfer_player(player_name, new_team)
                            print(f"\nTransfer completed:")
                            print(f"{transfer['player']} transferred from {transfer['from_team']} to {transfer['to_team']}")
                            print(f"Transfer fee: €{transfer['fee']:,}")
                        except ValueError as e:
                            print(f"Error: {e}")
                            
                    elif subchoice == '4':
                        break
                        
            elif choice == '3':
                # Match Simulation Menu
                while True:
                    print("\nMatch Simulation:")
                    print("1. Simulate Single Match")
                    print("2. View Match History")
                    print("3. Back to Main Menu")
                    
                    subchoice = input("\nEnter your choice (1-3): ")
                    
                    if subchoice == '1':
                        home_team = input("Enter home team: ")
                        away_team = input("Enter away team: ")
                        try:
                            result = match_engine.simulate_match(home_team, away_team)
                            print(f"\nMatch Result: {result['home_team']} {result['home_goals']} - {result['away_goals']} {result['away_team']}")
                            print("\nMatch Events:")
                            for event in result['events']:
                                if event['type'] == 'goal':
                                    print(f"{event['minute']}' - GOAL! {event['scorer']} (Assist: {event['assist']})")
                        except ValueError as e:
                            print(f"Error: {e}")
                            
                    elif subchoice == '3':
                        break
                        
            elif choice == '4':
                # Analytics Menu
                while True:
                    print("\nAnalytics:")
                    print("1. Player Efficiency Analysis")
                    print("2. Team Report")
                    print("3. Back to Main Menu")
                    
                    subchoice = input("\nEnter your choice (1-3): ")
                    
                    if subchoice == '1':
                        player_name = input("Enter player name: ")
                        efficiency = analytics.calculate_player_efficiency(player_name)
                        print(f"\nEfficiency Analysis for {player_name}:")
                        print(f"Goals per 90 minutes: {efficiency['goals_per_90']:.2f}")
                        print(f"Assists per 90 minutes: {efficiency['assists_per_90']:.2f}")
                        print(f"Total goal contributions: {efficiency['goal_contributions']}")
                        print(f"Shot conversion rate: {efficiency['shots_conversion']:.1f}%")
                            
                    elif subchoice == '2':
                        team_name = input("Enter team name: ")
                        report = analytics.generate_team_report(team_name)
                        print(f"\nTeam Report for {report['team_name']}:")
                        print("═" * 40)
                        print(f"League Position: {report['league_position']}")
                        print(f"Points: {report['points']}")
                        print(f"\nTop Scorer: {report['top_scorer']['name']} ({report['top_scorer']['stats']['goals']} goals)")
                        print(f"Top Assister: {report['top_assister']['name']} ({report['top_assister']['stats']['assists']} assists)")
                        print(f"Average Squad Age: {report['squad_age_average']:.1f} years")
                        print(f"Average Squad Rating: {report['squad_rating_average']:.1f}")
                            
                    elif subchoice == '3':
                        break
                        
            elif choice == '5':
                save_data(data, 'data.json')
                print("\nData saved successfully!")
                print("Thank you for using the Football Management System!")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        save_data(data, 'data_backup.json')
        print("Data backed up to 'data_backup.json'")
        return

if __name__ == "__main__":
    main()