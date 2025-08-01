import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 8: In season 2023 specifically, which team had the best batting power-play performance (runs scored per over in overs 1–6)?
print("\n" + "="*60)
print("QUESTION 8: In season 2023 specifically, which team had the best batting power-play performance?")
print("="*60)

# Filter for 2023 season
df_2023 = df[df['season'] == 2023].copy()

# Extract over number from ball column (e.g., 0.1 -> 0, 1.2 -> 1, etc.)
df_2023['over'] = df_2023['ball'].astype(str).str.split('.').str[0].astype(int)

# Filter for power-play overs (1-6)
powerplay_data = df_2023[df_2023['over'].between(1, 6)]

# Calculate runs scored by each team in power-play
powerplay_runs = powerplay_data.groupby('batting_team')['runs_off_bat'].sum().reset_index()
powerplay_runs = powerplay_runs.rename(columns={'batting_team': 'team', 'runs_off_bat': 'total_runs'})

# Calculate balls faced by each team in power-play
powerplay_balls = powerplay_data.groupby('batting_team').size().reset_index()
powerplay_balls = powerplay_balls.rename(columns={'batting_team': 'team', 0: 'balls_faced'})

# Merge runs and balls
powerplay_stats = powerplay_runs.merge(powerplay_balls, on='team', how='left')

# Calculate overs (balls / 6)
powerplay_stats['overs_faced'] = powerplay_stats['balls_faced'] / 6

# Calculate runs per over
powerplay_stats['runs_per_over'] = powerplay_stats['total_runs'] / powerplay_stats['overs_faced']

# Sort by runs per over (descending)
powerplay_stats = powerplay_stats.sort_values('runs_per_over', ascending=False)

print("\n2023 IPL Power-Play Performance (Runs per Over in Overs 1-6):")
print("-" * 70)
for idx, row in powerplay_stats.iterrows():
    team = row['team']
    runs = int(row['total_runs'])
    balls = int(row['balls_faced'])
    overs = row['overs_faced']
    rpo = row['runs_per_over']
    
    print(f"{team}: {runs} runs in {overs:.1f} overs ({rpo:.2f} runs per over)")

print(f"\nTotal teams analyzed: {len(powerplay_stats)}")
print(f"Best power-play team: {powerplay_stats.iloc[0]['team']} ({powerplay_stats.iloc[0]['runs_per_over']:.2f} runs per over)") 