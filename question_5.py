import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 5: List the top 5 wicket-takers and their economy rates over the same period.
print("\n" + "="*60)
print("QUESTION 5: List the top 5 wicket-takers and their economy rates over the same period.")
print("="*60)

# Calculate wickets taken by each bowler
bowler_wickets = df[df['wicket_type'].notna() & (df['wicket_type'] != '')].groupby('bowler').size().reset_index()
bowler_wickets = bowler_wickets.rename(columns={'bowler': 'player', 0: 'wickets'})

# Calculate balls bowled by each bowler
bowler_balls = df.groupby('bowler').size().reset_index()
bowler_balls = bowler_balls.rename(columns={'bowler': 'player', 0: 'balls_bowled'})

# Calculate runs conceded by each bowler
bowler_runs = df.groupby('bowler')['runs_off_bat'].sum().reset_index()
bowler_runs = bowler_runs.rename(columns={'bowler': 'player', 'runs_off_bat': 'runs_conceded'})

# Calculate extras conceded by each bowler
bowler_extras = df.groupby('bowler')['extras'].sum().reset_index()
bowler_extras = bowler_extras.rename(columns={'bowler': 'player', 'extras': 'extras_conceded'})

# Merge all bowling statistics
bowler_stats = bowler_wickets.merge(bowler_balls, on='player', how='left')
bowler_stats = bowler_stats.merge(bowler_runs, on='player', how='left')
bowler_stats = bowler_stats.merge(bowler_extras, on='player', how='left')

# Fill NaN values
bowler_stats['wickets'] = bowler_stats['wickets'].fillna(0)
bowler_stats['runs_conceded'] = bowler_stats['runs_conceded'].fillna(0)
bowler_stats['extras_conceded'] = bowler_stats['extras_conceded'].fillna(0)

# Calculate total runs conceded (including extras)
bowler_stats['total_runs_conceded'] = bowler_stats['runs_conceded'] + bowler_stats['extras_conceded']

# Calculate overs bowled (balls / 6)
bowler_stats['overs_bowled'] = bowler_stats['balls_bowled'] / 6

# Calculate economy rate
bowler_stats['economy_rate'] = bowler_stats['total_runs_conceded'] / bowler_stats['overs_bowled']
bowler_stats['economy_rate'] = bowler_stats['economy_rate'].replace([float('inf'), float('-inf')], 0)

# Get top 5 wicket-takers
top_wicket_takers = bowler_stats.nlargest(5, 'wickets')

print("\nTop 5 Wicket-Takers in IPL History:")
print("-" * 60)
for idx, row in top_wicket_takers.iterrows():
    player = row['player']
    wickets = int(row['wickets'])
    economy = row['economy_rate']
    overs = row['overs_bowled']
    runs = int(row['total_runs_conceded'])
    
    print(f"{player}:")
    print(f"  Wickets: {wickets}")
    print(f"  Overs Bowled: {overs:.1f}")
    print(f"  Runs Conceded: {runs:,}")
    print(f"  Economy Rate: {economy:.2f}")
    print()

print(f"Total bowlers analyzed: {len(bowler_stats)}") 