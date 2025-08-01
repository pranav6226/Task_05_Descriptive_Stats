import pandas as pd

# Load the data with proper handling of mixed types
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)

# Convert season to numeric, handling any non-numeric values
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 1: How many total matches were played in each IPL season from 2008 to 2023?
print("\n" + "="*60)
print("QUESTION 1: How many total matches were played in each IPL season from 2008 to 2023?")
print("="*60)

# Count unique matches per season
matches_per_season = df.groupby('season')['match_id'].nunique().sort_index()

print("\nTotal matches played in each IPL season:")
print("-" * 40)
for season, matches in matches_per_season.items():
    if pd.notna(season):  # Only print valid seasons
        print(f"Season {int(season)}: {matches} matches")

print(f"\nTotal seasons analyzed: {len(matches_per_season)}")
print(f"Total matches across all seasons: {matches_per_season.sum()}") 