import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 13: Player Impact Score (global ranking, all seasons)")
print("="*70)

# Compute match winners from innings totals
innings_totals = df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()
results = []
for match_id, g in innings_totals.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) != 2:
        continue
    t1, r1 = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    t2, r2 = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    if r1 == r2:
        continue
    winner = t1 if r1 > r2 else t2
    loser = t2 if r1 > r2 else t1
    results.append({'match_id': match_id, 'winner': winner, 'loser': loser})
res_df = pd.DataFrame(results)

# Team overall win %
team_wins = res_df['winner'].value_counts().rename('wins')
team_losses = res_df['loser'].value_counts().rename('losses')
team_records = pd.concat([team_wins, team_losses], axis=1).fillna(0)
team_records['matches'] = team_records['wins'] + team_records['losses']
team_records['win_pct_overall'] = team_records['wins'] / team_records['matches']

# Player matches played and team when appearing
# Approximate player's team by most frequent batting_team when listed as striker in a match
player_match_team = (
    df.groupby(['match_id', 'striker'])['batting_team']
      .agg(lambda x: x.mode().iat[0] if len(x.mode()) else x.iloc[0])
      .reset_index()
      .rename(columns={'striker': 'player', 'batting_team': 'team'})
)

# Runs per player (career)
player_runs = df.groupby('striker')['runs_off_bat'].sum().rename('runs').reset_index().rename(columns={'striker':'player'})

# Wickets per player (bowling)
player_wickets = (
    df[df['wicket_type'].notna() & (df['wicket_type'] != '')]
      .groupby('bowler').size().rename('wickets').reset_index()
      .rename(columns={'bowler': 'player'})
)

# Matches played per player
matches_played = player_match_team.groupby('player')['match_id'].nunique().rename('matches_played').reset_index()

# Team win % when player appears
player_team = player_match_team.merge(res_df, on='match_id', how='left')
player_team['team_win'] = (player_team['team'] == player_team['winner']).astype(float)
player_appear_win = player_team.groupby(['player','team'])['team_win'].mean().rename('win_pct_when_player').reset_index()

# Merge all
player_stats = matches_played.merge(player_runs, on='player', how='left')
player_stats = player_stats.merge(player_wickets, on='player', how='left')
player_stats['runs'] = player_stats['runs'].fillna(0)
player_stats['wickets'] = player_stats['wickets'].fillna(0)

# Attach player's primary team (most frequent)
primary_team = player_match_team.groupby('player')['team'].agg(lambda x: x.mode().iat[0] if len(x.mode()) else x.iloc[0]).rename('primary_team').reset_index()
player_stats = player_stats.merge(primary_team, on='player', how='left')

# Attach team win % overall
player_stats = player_stats.merge(team_records['win_pct_overall'], left_on='primary_team', right_index=True, how='left')

# Attach win % when player appears (use player's primary team row)
player_stats = player_stats.merge(player_appear_win[['player','win_pct_when_player']], on='player', how='left')

# Compute impact score
player_stats['base'] = (player_stats['runs'] + player_stats['wickets']) / player_stats['matches_played']
ratio = player_stats['win_pct_when_player'] / player_stats['win_pct_overall']
player_stats['impact_score'] = player_stats['base'] * ratio

# Filter reasonable sample size (>= 20 matches)
player_stats = player_stats[(player_stats['matches_played'] >= 20) & player_stats['win_pct_overall'].notna() & player_stats['win_pct_when_player'].notna()]

top5 = player_stats.sort_values('impact_score', ascending=False).head(5)

print("\nTop 5 players by Impact Score:")
print("-"*70)
for _, r in top5.iterrows():
    print(f"{r['player']}: impact {r['impact_score']:.2f} | base {(r['base']):.2f} | team {r['primary_team']} | matches {int(r['matches_played'])}")
