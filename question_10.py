import pandas as pd

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 10: Team average runs scored/conceded per match and differential")
print("="*70)

# Aggregate innings totals per match and team
innings_totals = (
    df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat']
      .sum()
      .reset_index()
)

# Keep only first two innings for T20 matches
innings_totals = innings_totals.sort_values(['match_id', 'innings'])

# Build per-match team vs opponent totals
match_pairs = []
for match_id, g in innings_totals.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) < 2:
        continue
    team1, runs1 = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    team2, runs2 = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    match_pairs.append({'match_id': match_id, 'team': team1, 'runs_scored': runs1, 'runs_conceded': runs2})
    match_pairs.append({'match_id': match_id, 'team': team2, 'runs_scored': runs2, 'runs_conceded': runs1})

per_match = pd.DataFrame(match_pairs)

team_stats = (
    per_match.groupby('team')[['runs_scored', 'runs_conceded']]
    .mean()
    .rename(columns={'runs_scored': 'avg_scored', 'runs_conceded': 'avg_conceded'})
)
team_stats['differential'] = team_stats['avg_scored'] - team_stats['avg_conceded']

best_team = team_stats['differential'].idxmax()
best_row = team_stats.loc[best_team]

print("\nTeam averages (top 10 by differential):")
print("-"*70)
for team, row in team_stats.sort_values('differential', ascending=False).head(10).iterrows():
    print(f"{team}: scored {row['avg_scored']:.2f} / conceded {row['avg_conceded']:.2f} / diff {row['differential']:.2f}")

print("\nLargest positive differential:")
print(f"{best_team}: diff {best_row['differential']:.2f} (scored {best_row['avg_scored']:.2f}, conceded {best_row['avg_conceded']:.2f})")
