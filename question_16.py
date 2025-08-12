import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

print("\n" + "="*70)
print("QUESTION 16: Logistic regression - predict win from venue, first-innings score, opponent strength")
print("="*70)

# Build per-match team view with features
innings_totals = df.groupby(['match_id','innings','batting_team'])['runs_off_bat'].sum().reset_index()
venue = df.groupby('match_id')['venue'].first().reset_index()

rows = []
for match_id, g in innings_totals.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) != 2:
        continue
    t1, r1 = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    t2, r2 = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    winner = t1 if r1>r2 else (t2 if r2>r1 else None)
    rows.append({'match_id': match_id, 'team': t1, 'opp': t2, 'first_runs': r1, 'chasing': 0, 'win': 1 if winner==t1 else 0})
    rows.append({'match_id': match_id, 'team': t2, 'opp': t1, 'first_runs': r1, 'chasing': 1, 'win': 1 if winner==t2 else 0})

Xy = pd.DataFrame(rows).dropna(subset=['win'])
Xy = Xy.merge(venue, on='match_id', how='left')

# Opponent strength proxy: historical win rate of opponent
df_res = []
for match_id, g in innings_totals.groupby('match_id'):
    g = g.sort_values('innings')
    if len(g) != 2:
        continue
    t1, r1 = g.iloc[0]['batting_team'], g.iloc[0]['runs_off_bat']
    t2, r2 = g.iloc[1]['batting_team'], g.iloc[1]['runs_off_bat']
    if r1==r2:
        continue
    winner = t1 if r1>r2 else t2
    loser = t2 if r1>r2 else t1
    df_res.append({'match_id': match_id, 'winner': winner, 'loser': loser})
res = pd.DataFrame(df_res)
winrate = (res['winner'].value_counts() / (res['winner'].value_counts() + res['loser'].value_counts())).fillna(0)
Xy['opp_strength'] = Xy['opp'].map(winrate).fillna(0.5)

features = ['venue', 'first_runs', 'chasing', 'opp_strength']
X = Xy[features]
y = Xy['win']

pre = ColumnTransformer([
    ('venue', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['venue'])
], remainder='passthrough')

model = Pipeline([
    ('pre', pre),
    ('clf', LogisticRegression(max_iter=200, n_jobs=1))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, proba)

# Feature importance (approximate) via coefficients on numeric features after one-hot
clf = model.named_steps['clf']
enc = model.named_steps['pre']
num_names = ['first_runs','chasing','opp_strength']
coef = clf.coef_[0]
# Last three correspond to numeric passthrough at the end
num_coef = coef[-len(num_names):]

print(f"\nTest AUC: {auc:.3f}")
print("Numeric feature coefficients (log-odds impact):")
for name, c in zip(num_names, num_coef):
    print(f"- {name}: {c:.3f}")

print("\nInterpretation: higher absolute coefficient suggests stronger predictor among numeric features.")
