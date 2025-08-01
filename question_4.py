import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 4: Who are the top 5 run-scorers in IPL history (2008–2023), and what are their career batting averages?
print("\n" + "="*60)
print("QUESTION 4: Who are the top 5 run-scorers in IPL history (2008–2023), and what are their career batting averages?")
print("="*60)

# Calculate runs scored by each player
player_runs = df.groupby('striker')['runs_off_bat'].sum().reset_index()
player_runs = player_runs.rename(columns={'striker': 'player', 'runs_off_bat': 'total_runs'})

# Calculate dismissals (wickets) for each player
player_dismissals = df[df['wicket_type'].notna() & (df['wicket_type'] != '')].groupby('player_dismissed').size().reset_index()
player_dismissals = player_dismissals.rename(columns={'player_dismissed': 'player', 0: 'dismissals'})

# Calculate balls faced by each player
player_balls = df.groupby('striker').size().reset_index()
player_balls = player_balls.rename(columns={'striker': 'player', 0: 'balls_faced'})

# Merge all statistics
player_stats = player_runs.merge(player_balls, on='player', how='left')
player_stats = player_stats.merge(player_dismissals, on='player', how='left')
player_stats['dismissals'] = player_stats['dismissals'].fillna(0)

# Calculate batting average
player_stats['batting_average'] = player_stats['total_runs'] / player_stats['dismissals']
player_stats['batting_average'] = player_stats['batting_average'].replace([float('inf'), float('-inf')], 0)

# Get top 5 run-scorers
top_scorers = player_stats.nlargest(5, 'total_runs')

print("\nTop 5 Run-Scorers in IPL History:")
print("-" * 60)
for idx, row in top_scorers.iterrows():
    player = row['player']
    runs = int(row['total_runs'])
    avg = row['batting_average']
    dismissals = int(row['dismissals'])
    balls = int(row['balls_faced'])
    
    print(f"{player}:")
    print(f"  Total Runs: {runs:,}")
    print(f"  Balls Faced: {balls:,}")
    print(f"  Dismissals: {dismissals}")
    print(f"  Batting Average: {avg:.2f}")
    print()

print(f"Total players analyzed: {len(player_stats)}") 