import pandas as pd
from itertools import combinations

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 7: For each pair of franchises (e.g., MI vs SRH), what is their head-to-head win–loss record?
print("\n" + "="*60)
print("QUESTION 7: For each pair of franchises, what is their head-to-head win–loss record?")
print("="*60)

# Get total runs scored by each team in each innings
innings_totals = df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()

# Create match results by comparing innings
match_results = []
unique_matches = innings_totals['match_id'].unique()

for match_id in unique_matches:
    match_data = innings_totals[innings_totals['match_id'] == match_id]
    
    if len(match_data) >= 2:  # Need at least 2 innings for a complete match
        innings = match_data.sort_values('innings')
        
        if len(innings) == 2:
            team1 = innings.iloc[0]['batting_team']
            score1 = innings.iloc[0]['runs_off_bat']
            team2 = innings.iloc[1]['batting_team']
            score2 = innings.iloc[1]['runs_off_bat']
            
            # Determine winner
            if score1 > score2:
                match_results.append({'match_id': match_id, 'winner': team1, 'loser': team2})
            elif score2 > score1:
                match_results.append({'match_id': match_id, 'winner': team2, 'loser': team1})

# Convert to DataFrame
results_df = pd.DataFrame(match_results)

# Get unique teams
teams = sorted(df['batting_team'].unique())

# Calculate head-to-head records
head_to_head = {}

for team1, team2 in combinations(teams, 2):
    # Matches where team1 won against team2
    team1_wins = len(results_df[(results_df['winner'] == team1) & (results_df['loser'] == team2)])
    # Matches where team2 won against team1
    team2_wins = len(results_df[(results_df['winner'] == team2) & (results_df['loser'] == team1)])
    
    if team1_wins > 0 or team2_wins > 0:  # Only show pairs that have played against each other
        head_to_head[f"{team1} vs {team2}"] = {
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'total_matches': team1_wins + team2_wins
        }

print("\nHead-to-Head Records (Team1 Wins - Team2 Wins):")
print("-" * 70)

# Sort by total matches played
sorted_h2h = sorted(head_to_head.items(), key=lambda x: x[1]['total_matches'], reverse=True)

for matchup, record in sorted_h2h:
    team1, team2 = matchup.split(" vs ")
    team1_wins = record['team1_wins']
    team2_wins = record['team2_wins']
    total = record['total_matches']
    
    print(f"{matchup}: {team1_wins} - {team2_wins} ({total} matches)")

print(f"\nTotal head-to-head matchups analyzed: {len(head_to_head)}")
print(f"Total teams: {len(teams)}") 