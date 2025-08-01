import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 6: Which player has the highest strike rate (min. 200 balls faced) in a single season, and in which year?
print("\n" + "="*60)
print("QUESTION 6: Which player has the highest strike rate (min. 200 balls faced) in a single season, and in which year?")
print("="*60)

# Calculate runs scored by each player in each season
player_season_runs = df.groupby(['striker', 'season'])['runs_off_bat'].sum().reset_index()
player_season_runs = player_season_runs.rename(columns={'striker': 'player', 'runs_off_bat': 'runs_scored'})

# Calculate balls faced by each player in each season
player_season_balls = df.groupby(['striker', 'season']).size().reset_index()
player_season_balls = player_season_balls.rename(columns={'striker': 'player', 0: 'balls_faced'})

# Merge runs and balls data
player_season_stats = player_season_runs.merge(player_season_balls, on=['player', 'season'], how='left')

# Calculate strike rate (runs per 100 balls)
player_season_stats['strike_rate'] = (player_season_stats['runs_scored'] / player_season_stats['balls_faced']) * 100

# Filter for players with minimum 200 balls faced
qualified_players = player_season_stats[player_season_stats['balls_faced'] >= 200]

# Get the player with highest strike rate
highest_strike_rate = qualified_players.loc[qualified_players['strike_rate'].idxmax()]

print("\nPlayer with Highest Strike Rate in a Single Season (min. 200 balls):")
print("-" * 70)
print(f"Player: {highest_strike_rate['player']}")
print(f"Season: {int(highest_strike_rate['season'])}")
print(f"Runs Scored: {int(highest_strike_rate['runs_scored']):,}")
print(f"Balls Faced: {int(highest_strike_rate['balls_faced']):,}")
print(f"Strike Rate: {highest_strike_rate['strike_rate']:.2f}")

# Show top 10 players with highest strike rates
print(f"\nTop 10 Players by Strike Rate (min. 200 balls faced):")
print("-" * 70)
top_strike_rates = qualified_players.nlargest(10, 'strike_rate')
for idx, row in top_strike_rates.iterrows():
    print(f"{row['player']} ({int(row['season'])}): {row['strike_rate']:.2f}")

print(f"\nTotal qualified players analyzed: {len(qualified_players)}") 