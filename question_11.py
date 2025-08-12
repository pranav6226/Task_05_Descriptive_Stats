import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 11: Correlation between first-innings total and probability of winning")
print("="*70)

# Compute innings totals per match
innings_totals = (
    df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat']
      .sum()
      .reset_index()
)

# Keep matches with 2 innings
first_second = (
    innings_totals.sort_values(['match_id', 'innings'])
)

rows = []
for match_id, g in first_second.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) != 2:
        continue
    first_team, first_runs = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    second_team, second_runs = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    winner = first_team if first_runs > second_runs else (second_team if second_runs > first_runs else None)
    rows.append({
        'match_id': match_id,
        'first_team': first_team,
        'first_runs': first_runs,
        'won_first_team': 1 if winner == first_team else (0 if winner is not None else np.nan)
    })

m = pd.DataFrame(rows).dropna(subset=['won_first_team'])

# Bin first-innings totals and compute win rate per bin
m['bin'] = pd.cut(m['first_runs'], bins=[0,120,140,160,180,200,999], right=True)
win_rate_by_bin = m.groupby('bin')['won_first_team'].mean().reset_index()

# Pearson correlation between continuous first_runs and win (0/1)
corr = m['first_runs'].corr(m['won_first_team'])

print("\nWin rate by first-innings total bin:")
print("-"*70)
for _, r in win_rate_by_bin.iterrows():
    print(f"{str(r['bin']).ljust(14)} -> win% = {100*r['won_first_team']:.1f}%")

print(f"\nPearson correlation (first_runs vs win): {corr:.3f}")
