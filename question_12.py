import pandas as pd

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 12: Which season saw the highest overall scoring (total runs per match)?")
print("="*70)

# Normalize season to numeric where possible
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Compute per-match totals (sum of both innings runs_off_bat)
match_totals = df.groupby(['match_id', 'season'])['runs_off_bat'].sum().reset_index()
per_season = match_totals.groupby('season')['runs_off_bat'].mean().reset_index(name='avg_runs_per_match')
per_season = per_season.dropna(subset=['season']).sort_values('avg_runs_per_match', ascending=False)

print("\nTop seasons by average total runs per match:")
print("-"*70)
for _, r in per_season.head(10).iterrows():
    print(f"Season {int(r['season'])}: {r['avg_runs_per_match']:.1f} runs/match")

best = per_season.iloc[0]
print("\nHighest scoring season:")
print(f"Season {int(best['season'])}: {best['avg_runs_per_match']:.1f} runs/match")

# Possible factor proxy: extras per match
extras_per_season = df.groupby('season')['extras'].sum() / df.groupby('season')['match_id'].nunique()
print("\nExtras per match (proxy for discipline/conditions) for top 5 seasons:")
for s in per_season.head(5)['season']:
    print(f"Season {int(s)}: {extras_per_season.loc[s]:.1f} extras/match")
