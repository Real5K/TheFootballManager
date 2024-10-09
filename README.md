# TheFootballManager

A comprehensive football (soccer) management system that simulates team management, matches, transfers, and provides detailed analytics.

## Table of Contents
1. [System Overview](#system-overview)
2. [Features](#features)
3. [Technical Requirements](#technical-requirements)
4. [Data Structure](#data-structure)
5. [Core Components](#core-components)
6. [Usage Guide](#usage-guide)
7. [Component Details](#component-details)
8. [Error Handling](#error-handling)
9. [Menu System](#menu-system)

## System Overview

The Advanced Football Management System is a command-line application that provides a complete solution for managing football teams, players, matches, and analyzing performance data. The system simulates real-world football management scenarios with sophisticated algorithms for match simulation, player valuations, and performance analytics.

## Features

### Core Features
- Team and player management
- Real-time match simulations with detailed events
- Dynamic transfer market with intelligent player valuation
- Advanced performance analytics and statistics
- Complete league management
- Historical data tracking and analysis

### Key Capabilities
- Player search and filtering
- Realistic match simulations with play-by-play events
- Market value calculations based on multiple factors
- Comprehensive team and player statistics
- Data persistence and backup functionality

## Technical Requirements

### Software Requirements
- Python 3.6 or higher
- Required Python packages:
  - json (built-in)
  - random (built-in)
  - math (built-in)
  - datetime (built-in)
  - pathlib (built-in)
  - typing (built-in)

## Data Structure

### Main Data File (data.json)
```json
{
    "teams": [
        {
            "name": "string",
            "league_position": "integer",
            "points": "integer",
            "other_attributes": "various"
        }
    ],
    "players": [
        {
            "name": "string",
            "team": "string",
            "position": "string",
            "age": "integer",
            "rating": "integer",
            "stats": {
                "goals": "integer",
                "assists": "integer",
                "minutes_played": "integer",
                "shots_on_target": "integer"
            }
        }
    ]
}
```

## Core Components

### 1. TransferMarket Class
```python
class TransferMarket:
    - calculate_player_value(): Determines market value based on:
        * Base value (rating × 2,000,000)
        * Age factor (peak at 26 years)
        * Performance metrics
    - transfer_player(): Handles player transfers between teams
```

### 2. MatchEngine Class
```python
class MatchEngine:
    - simulate_match(): Creates realistic match simulations
    - generate_match_events(): Produces detailed match events
    - calculate_team_strength(): Determines team performance potential
    - update_stats(): Maintains player and team statistics
```

### 3. Analytics Class
```python
class Analytics:
    - calculate_player_efficiency(): Computes advanced player metrics
    - generate_team_report(): Creates comprehensive team analysis
```

## Usage Guide

### Initial Setup
1. Create a `data.json` file with team and player data
2. Ensure the file follows the specified data structure
3. Run the program:
```bash
python main.py
```

### Basic Operations
1. Player Management:
   ```python
   # Search for players
   results = [p for p in data['players'] 
             if name.lower() in p['name'].lower()]
   ```

2. Transfer Operations:
   ```python
   # Transfer a player
   transfer = transfer_market.transfer_player("Player Name", "New Team")
   ```

3. Match Simulation:
   ```python
   # Simulate a match
   result = match_engine.simulate_match("Home Team", "Away Team")
   ```

## Component Details

### 1. Player Valuation System
The system calculates player values using multiple factors:
- Base value from player rating
- Age coefficient (peaks at 26 years)
- Performance metrics:
  * Goals: €500,000 per goal
  * Assists: €300,000 per assist
  * Playing time: €100,000 per 90 minutes

### 2. Match Simulation Engine
Simulates matches with:
- Team strength calculations
- Home advantage factor (1.1×)
- Goal simulation using Gaussian distribution
- Detailed event generation:
  * Goals
  * Assists
  * Minute-by-minute events

### 3. Analytics System
Provides detailed analytics including:
- Goals per 90 minutes
- Assists per 90 minutes
- Shot conversion rates
- Team performance metrics
- Squad analysis

## Error Handling

The system implements comprehensive error handling for:

### Data Loading/Saving
```python
try:
    data = load_data('data.json')
except FileNotFoundError:
    # Handle missing file
except json.JSONDecodeError:
    # Handle invalid JSON
```

### Runtime Operations
- Player not found
- Team not found
- Invalid transfer operations
- Match simulation errors
- Data validation errors

### Data Backup
- Automatic backup on keyboard interrupt
- Saves to `data_backup.json`

## Menu System

### Main Menu
1. Player Management
2. Transfer Market
3. Match Simulation
4. Analytics
5. Save & Exit

### Submenu Examples

#### Player Management
1. Search Players
2. View Player Details
3. Update Player Stats
4. Back to Main Menu

#### Transfer Market
1. View Player Value
2. Transfer Player
3. View Transfer History
4. Back to Main Menu

#### Match Simulation
1. Simulate Single Match
2. View Match History
3. Back to Main Menu

#### Analytics
1. Player Efficiency Analysis
2. Team Report
3. Back to Main Menu

### Example Usage Flow
```text
Main Menu > Transfer Market > Transfer Player
1. Enter player name
2. Enter new team
3. Review transfer details
4. Confirm transfer
```
