import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 14: Most improved batsman and bowler in season 2022 (rolling 5-match)")
print("="*70)

# Normalize season
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Batting: runs per player per match
df_bat = (
    df.groupby(['match_id','striker'])['runs_off_bat']
      .sum().reset_index()
      .rename(columns={'striker':'player','runs_off_bat':'runs'})
)

# Bowling: wickets and runs conceded per match
wickets = (
    df[df['wicket_type'].notna() & (df['wicket_type']!='')]
      .groupby(['match_id','bowler']).size()
      .rename('wickets').reset_index()
      .rename(columns={'bowler':'player'})
)
runs_conc = (
    df.groupby(['match_id','bowler'])['runs_off_bat']
      .sum().rename('runs_conceded').reset_index()
      .rename(columns={'bowler':'player'})
)
df_bowl = pd.merge(wickets, runs_conc, on=['match_id','player'], how='outer').fillna(0)

# Season per match
match_season = df.groupby('match_id')['season'].first().reset_index()

bat = df_bat.merge(match_season, on='match_id', how='left')
bowl = df_bowl.merge(match_season, on='match_id', how='left')

# Filter 2022
bat_22 = bat[bat['season']==2022].copy()
bowl_22 = bowl[bowl['season']==2022].copy()

# Sort and compute rolling windows
bat_22 = bat_22.sort_values(['player','match_id'])
bowl_22 = bowl_22.sort_values(['player','match_id'])

bat_22['runs_rolling5'] = bat_22.groupby('player')['runs'].transform(lambda s: s.rolling(5, min_periods=3).mean())

bat_improve = (
    bat_22.groupby('player')
      .agg(first=('runs_rolling5','first'), last=('runs_rolling5','last'), matches=('match_id','nunique'))
      .dropna()
)
bat_improve['improvement'] = bat_improve['last'] - bat_improve['first']
bat_improve = bat_improve[bat_improve['matches']>=5].sort_values('improvement', ascending=False)

# Bowling improvement: decrease in runs conceded per match (rolling)
bowl_22['runs_conc_rolling5'] = bowl_22.groupby('player')['runs_conceded'].transform(lambda s: s.rolling(5, min_periods=3).mean())
bowl_improve = (
    bowl_22.groupby('player')
      .agg(first=('runs_conc_rolling5','first'), last=('runs_conc_rolling5','last'), matches=('match_id','nunique'))
      .dropna()
)
bowl_improve['improvement'] = bowl_improve['first'] - bowl_improve['last']
bowl_improve = bowl_improve[bowl_improve['matches']>=5].sort_values('improvement', ascending=False)

print("\nMost improved batsmen (top 5):")
print("-"*70)
if len(bat_improve)==0:
    print("No qualified players (need >=5 matches with rolling windows)")
else:
    for player, r in bat_improve.head(5).iterrows():
        print(f"{player}: +{r['improvement']:.2f} runs/match (from {r['first']:.2f} to {r['last']:.2f}) over {int(r['matches'])} matches")

print("\nMost improved bowlers (top 5, lower runs conceded per match):")
print("-"*70)
if len(bowl_improve)==0:
    print("No qualified players (need >=5 matches with rolling windows)")
else:
    for player, r in bowl_improve.head(5).iterrows():
        print(f"{player}: -{r['improvement']:.2f} runs conceded/match (from {r['first']:.2f} to {r['last']:.2f}) over {int(r['matches'])} matches")

print("\nDefinition of improvement:")
print("- Batsman: increase in 5-match rolling average of runs per match (last minus first).")
print("- Bowler: decrease in 5-match rolling average of runs conceded per match (first minus last).")
