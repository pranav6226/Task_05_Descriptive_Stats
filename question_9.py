import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('match_data.csv', low_memory=False)
df['season'] = pd.to_numeric(df['season'], errors='coerce')

# Question 9: How did shifting home venues (e.g., due to bio-bubbles) affect a team's home-win percentage in 2020 and 2021?
print("\n" + "="*60)
print("QUESTION 9: How did shifting home venues affect team performance in 2020 and 2021?")
print("="*60)

# Filter for 2020 and 2021 seasons
df_2020_2021 = df[df['season'].isin([2020, 2021])].copy()

# Get total runs scored by each team in each innings
innings_totals = df_2020_2021.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()

# Create match results by comparing innings
match_results = []
unique_matches = innings_totals['match_id'].unique()

for match_id in unique_matches:
    match_data = innings_totals[innings_totals['match_id'] == match_id]
    
    if len(match_data) >= 2:  # Need at least 2 innings for a complete match
        innings = match_data.sort_values('innings')
        
        if len(innings) == 2:
            team1 = innings.iloc[0]['batting_team']
            score1 = innings.iloc[0]['runs_off_bat']
            team2 = innings.iloc[1]['batting_team']
            score2 = innings.iloc[1]['runs_off_bat']
            
            # Determine winner
            if score1 > score2:
                match_results.append({'match_id': match_id, 'winner': team1, 'loser': team2})
            elif score2 > score1:
                match_results.append({'match_id': match_id, 'winner': team2, 'loser': team1})

# Convert to DataFrame
results_df = pd.DataFrame(match_results)

# Get venue information for each match
match_venues = df_2020_2021.groupby('match_id')['venue'].first().reset_index()

# Merge results with venue information
results_with_venues = results_df.merge(match_venues, on='match_id', how='left')

# Analyze venue patterns for each team
team_venue_analysis = {}

# Get unique teams
teams = df_2020_2021['batting_team'].unique()

for team in teams:
    # Get all matches where this team played
    team_matches = results_with_venues[
        (results_with_venues['winner'] == team) | 
        (results_with_venues['loser'] == team)
    ]
    
    if len(team_matches) > 0:
        # Count wins and total matches per venue
        venue_stats = {}
        for _, match in team_matches.iterrows():
            venue = match['venue']
            is_winner = match['winner'] == team
            
            if venue not in venue_stats:
                venue_stats[venue] = {'wins': 0, 'total': 0}
            
            venue_stats[venue]['total'] += 1
            if is_winner:
                venue_stats[venue]['wins'] += 1
        
        # Calculate win percentage per venue
        venue_percentages = {}
        for venue, stats in venue_stats.items():
            if stats['total'] > 0:
                win_percentage = (stats['wins'] / stats['total']) * 100
                venue_percentages[venue] = {
                    'wins': stats['wins'],
                    'total': stats['total'],
                    'win_percentage': win_percentage
                }
        
        team_venue_analysis[team] = venue_percentages

print("\nTeam Performance by Venue (2020-2021):")
print("-" * 70)

for team, venues in team_venue_analysis.items():
    print(f"\n{team}:")
    for venue, stats in venues.items():
        print(f"  {venue}: {stats['wins']}/{stats['total']} wins ({stats['win_percentage']:.1f}%)")

# Summary statistics
print(f"\nSummary:")
print(f"Total teams analyzed: {len(team_venue_analysis)}")
print(f"Total matches in 2020-2021: {len(results_df)}")

# Find teams with most venues played at
team_venue_counts = {team: len(venues) for team, venues in team_venue_analysis.items()}
most_venues_team = max(team_venue_counts.items(), key=lambda x: x[1])
print(f"Team that played at most venues: {most_venues_team[0]} ({most_venues_team[1]} venues)") 