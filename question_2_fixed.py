import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 2: What is the overall win-loss record for each team across all seasons?
print("\n" + "="*60)
print("QUESTION 2: What is the overall win-loss record for each team across all seasons?")
print("="*60)

# Get total runs scored by each team in each innings
innings_totals = df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()

# Create match results by comparing innings
match_results = []
unique_matches = innings_totals['match_id'].unique()

for match_id in unique_matches:
    match_data = innings_totals[innings_totals['match_id'] == match_id]
    
    if len(match_data) >= 2:  # Need at least 2 innings for a complete match
        # Get the two innings
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
            # If scores are equal, it's a tie (not counted)

# Convert to DataFrame
results_df = pd.DataFrame(match_results)

# Calculate team records
team_records = {}
all_teams = df['batting_team'].unique()

for team in all_teams:
    wins = len(results_df[results_df['winner'] == team])
    losses = len(results_df[results_df['loser'] == team])
    total_matches = wins + losses
    
    win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
    team_records[team] = {'wins': wins, 'losses': losses, 'win_rate': win_rate, 'total_matches': total_matches}

print("\nTeam Win-Loss Records (Wins - Losses):")
print("-" * 60)
for team, record in sorted(team_records.items(), key=lambda x: x[1]['wins'], reverse=True):
    if record['total_matches'] > 0:  # Only show teams that have played matches
        print(f"{team}: {record['wins']} wins, {record['losses']} losses (Win Rate: {record['win_rate']:.1f}%)")

print(f"\nTotal teams analyzed: {len([t for t in team_records.values() if t['total_matches'] > 0])}")
print(f"Total matches analyzed: {len(results_df)}") 