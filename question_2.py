import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 2: What is the overall win-loss record for each team across all seasons?
print("\n" + "="*60)
print("QUESTION 2: What is the overall win-loss record for each team across all seasons?")
print("="*60)

# Since we have ball-by-ball data, we need to determine match results
# We'll aggregate runs by match and team to determine winners

# Get total runs scored by each team in each match
match_results = df.groupby(['match_id', 'batting_team'])['runs_off_bat'].sum().reset_index()
match_results = match_results.rename(columns={'batting_team': 'team', 'runs_off_bat': 'runs_scored'})

# Pivot to get both teams' scores for each match
match_scores = match_results.pivot(index='match_id', columns='team', values='runs_scored').fillna(0)

# Get unique teams
teams = df['batting_team'].unique()

# Calculate win-loss records
team_records = {}

for team in teams:
    wins = 0
    losses = 0
    
    # For each match, determine if this team won
    for match_id in match_scores.index:
        if team in match_scores.columns:
            team_score = match_scores.loc[match_id, team]
            # Find the opponent's score (highest score among other teams)
            other_scores = match_scores.loc[match_id].drop(team)
            if len(other_scores) > 0:
                opponent_score = other_scores.max()
                
                if team_score > opponent_score:
                    wins += 1
                elif team_score < opponent_score:
                    losses += 1
                # If scores are equal, it's a tie (not counted in wins/losses)
    
    team_records[team] = {'wins': wins, 'losses': losses, 'win_rate': wins/(wins+losses)*100 if (wins+losses) > 0 else 0}

print("\nTeam Win-Loss Records (Wins - Losses):")
print("-" * 50)
for team, record in sorted(team_records.items(), key=lambda x: x[1]['wins'], reverse=True):
    print(f"{team}: {record['wins']} wins, {record['losses']} losses (Win Rate: {record['win_rate']:.1f}%)")

print(f"\nTotal teams analyzed: {len(team_records)}") 