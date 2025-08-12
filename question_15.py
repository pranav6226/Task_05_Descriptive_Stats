import pandas as pd

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 15: Coaching focus and single game-changer recommendation")
print("="*70)

# Build per-match team totals
innings_totals = df.groupby(['match_id','innings','batting_team'])['runs_off_bat'].sum().reset_index()
rows = []
for match_id, g in innings_totals.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) != 2:
        continue
    t1, r1 = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    t2, r2 = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    winner = t1 if r1>r2 else (t2 if r2>r1 else None)
    rows.append({'match_id': match_id, 'team': t1, 'runs_scored': r1, 'runs_conceded': r2, 'win': 1 if winner==t1 else 0})
    rows.append({'match_id': match_id, 'team': t2, 'runs_scored': r2, 'runs_conceded': r1, 'win': 1 if winner==t2 else 0})

tm = pd.DataFrame(rows).dropna(subset=['win'])

# Logistic-style insight without ML: marginal effect of +10 batting vs -10 bowling on win prob via local slope
# Bin by net run differential and compute win rate
import numpy as np

tm['net'] = tm['runs_scored'] - tm['runs_conceded']

# Approximate local slope using small deltas around zero
bins = pd.cut(tm['net'], bins=[-100,-60,-40,-20,-10,-5,-1,0,1,5,10,20,40,60,100])
win_by_bin = tm.groupby(bins)['win'].mean().reset_index()

print("\nWin rate by net run differential bin (proxy for impact of batting minus bowling):")
print("-"*70)
for _, r in win_by_bin.iterrows():
    print(f"{str(r['net']).ljust(18)} -> win% {100*r['win']:.1f}%")

# Identify game-changer: player with high impact on team win% when appearing and strong base stats
# Reuse logic from impact score (simplified)
player_runs = df.groupby('striker')['runs_off_bat'].sum().rename('runs').reset_index().rename(columns={'striker':'player'})
player_wkts = df[df['wicket_type'].notna() & (df['wicket_type']!='')].groupby('bowler').size().rename('wickets').reset_index().rename(columns={'bowler':'player'})
player_match_team = df.groupby(['match_id','striker'])['batting_team'].agg(lambda x: x.mode().iat[0] if len(x.mode()) else x.iloc[0]).reset_index().rename(columns={'striker':'player','batting_team':'team'})

# Merge with team results
res = tm[['match_id','team','win']]
appear = player_match_team.merge(res, on=['match_id','team'], how='left')
appear_agg = appear.groupby('player')['win'].mean().rename('team_win_with_player').reset_index()

base = player_runs.merge(player_wkts, on='player', how='outer').fillna(0)
base['base_score'] = base['runs'] + 20*base['wickets']  # weight wickets

cand = base.merge(appear_agg, on='player', how='left').fillna(0)
# Filter reasonable activity
player_games = player_match_team.groupby('player')['match_id'].nunique().rename('matches').reset_index()
cand = cand.merge(player_games, on='player', how='left').fillna(0)
cand = cand[cand['matches']>=20]

cand['game_changer_score'] = cand['base_score'] * cand['team_win_with_player']

best = cand.sort_values('game_changer_score', ascending=False).head(1).iloc[0]

print("\nRecommendation:")
print("- Strengthen areas that increase net run differential; historically, both raising first-innings totals and suppressing opponent totals strongly lift win%.")
print(f"- Suggested game-changer: {best['player']} | matches {int(best['matches'])} | team-win% when appearing {100*best['team_win_with_player']:.1f}% | base score {best['base_score']:.1f}")
