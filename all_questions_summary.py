import pandas as pd
import time

def print_header(title):
    print("\n" + "="*80)
    print(f"ANALYSIS: {title}")
    print("="*80)

def question_1_matches_per_season(df):
    print_header("Total Matches per IPL Season (2008-2023)")
    
    matches_per_season = df.groupby('season')['match_id'].nunique().sort_index()
    
    print("\nTotal matches played in each IPL season:")
    print("-" * 50)
    for season, matches in matches_per_season.items():
        if pd.notna(season):
            print(f"Season {int(season)}: {matches} matches")
    
    print(f"\nTotal seasons: {len(matches_per_season)}")
    print(f"Total matches: {matches_per_season.sum()}")

def question_2_team_records(df):
    print_header("Team Win-Loss Records Across All Seasons")
    
    # Get total runs scored by each team in each innings
    innings_totals = df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()
    
    # Create match results
    match_results = []
    unique_matches = innings_totals['match_id'].unique()
    
    for match_id in unique_matches:
        match_data = innings_totals[innings_totals['match_id'] == match_id]
        
        if len(match_data) >= 2:
            innings = match_data.sort_values('innings')
            
            if len(innings) == 2:
                team1 = innings.iloc[0]['batting_team']
                score1 = innings.iloc[0]['runs_off_bat']
                team2 = innings.iloc[1]['batting_team']
                score2 = innings.iloc[1]['runs_off_bat']
                
                if score1 > score2:
                    match_results.append({'match_id': match_id, 'winner': team1, 'loser': team2})
                elif score2 > score1:
                    match_results.append({'match_id': match_id, 'winner': team2, 'loser': team1})
    
    results_df = pd.DataFrame(match_results)
    
    # Calculate team records
    team_records = {}
    all_teams = df['batting_team'].unique()
    
    for team in all_teams:
        wins = len(results_df[results_df['winner'] == team])
        losses = len(results_df[results_df['loser'] == team])
        total_matches = wins + losses
        
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0
        team_records[team] = {'wins': wins, 'losses': losses, 'win_rate': win_rate, 'total_matches': total_matches}
    
    print("\nTeam Win-Loss Records (Wins - Losses):")
    print("-" * 60)
    for team, record in sorted(team_records.items(), key=lambda x: x[1]['wins'], reverse=True):
        if record['total_matches'] > 0:
            print(f"{team}: {record['wins']} wins, {record['losses']} losses (Win Rate: {record['win_rate']:.1f}%)")

def question_4_top_run_scorers(df):
    print_header("Top 5 Run-Scorers in IPL History")
    
    # Calculate runs scored by each player
    player_runs = df.groupby('striker')['runs_off_bat'].sum().reset_index()
    player_runs = player_runs.rename(columns={'striker': 'player', 'runs_off_bat': 'total_runs'})
    
    # Calculate dismissals for each player
    player_dismissals = df[df['wicket_type'].notna() & (df['wicket_type'] != '')].groupby('player_dismissed').size().reset_index()
    player_dismissals = player_dismissals.rename(columns={'player_dismissed': 'player', 0: 'dismissals'})
    
    # Calculate balls faced by each player
    player_balls = df.groupby('striker').size().reset_index()
    player_balls = player_balls.rename(columns={'striker': 'player', 0: 'balls_faced'})
    
    # Merge all statistics
    player_stats = player_runs.merge(player_balls, on='player', how='left')
    player_stats = player_stats.merge(player_dismissals, on='player', how='left')
    player_stats['dismissals'] = player_stats['dismissals'].fillna(0)
    
    # Calculate batting average
    player_stats['batting_average'] = player_stats['total_runs'] / player_stats['dismissals']
    player_stats['batting_average'] = player_stats['batting_average'].replace([float('inf'), float('-inf')], 0)
    
    # Get top 5 run-scorers
    top_scorers = player_stats.nlargest(5, 'total_runs')
    
    print("\nTop 5 Run-Scorers:")
    print("-" * 50)
    for idx, row in top_scorers.iterrows():
        player = row['player']
        runs = int(row['total_runs'])
        avg = row['batting_average']
        dismissals = int(row['dismissals'])
        balls = int(row['balls_faced'])
        
        print(f"{player}: {runs:,} runs, {balls:,} balls, {dismissals} dismissals, Avg: {avg:.2f}")

def question_5_top_wicket_takers(df):
    print_header("Top 5 Wicket-Takers in IPL History")
    
    # Calculate wickets taken by each bowler
    bowler_wickets = df[df['wicket_type'].notna() & (df['wicket_type'] != '')].groupby('bowler').size().reset_index()
    bowler_wickets = bowler_wickets.rename(columns={'bowler': 'player', 0: 'wickets'})
    
    # Calculate balls bowled by each bowler
    bowler_balls = df.groupby('bowler').size().reset_index()
    bowler_balls = bowler_balls.rename(columns={'bowler': 'player', 0: 'balls_bowled'})
    
    # Calculate runs conceded by each bowler
    bowler_runs = df.groupby('bowler')['runs_off_bat'].sum().reset_index()
    bowler_runs = bowler_runs.rename(columns={'bowler': 'player', 'runs_off_bat': 'runs_conceded'})
    
    # Calculate extras conceded by each bowler
    bowler_extras = df.groupby('bowler')['extras'].sum().reset_index()
    bowler_extras = bowler_extras.rename(columns={'bowler': 'player', 'extras': 'extras_conceded'})
    
    # Merge all bowling statistics
    bowler_stats = bowler_wickets.merge(bowler_balls, on='player', how='left')
    bowler_stats = bowler_stats.merge(bowler_runs, on='player', how='left')
    bowler_stats = bowler_stats.merge(bowler_extras, on='player', how='left')
    
    # Fill NaN values
    bowler_stats['wickets'] = bowler_stats['wickets'].fillna(0)
    bowler_stats['runs_conceded'] = bowler_stats['runs_conceded'].fillna(0)
    bowler_stats['extras_conceded'] = bowler_stats['extras_conceded'].fillna(0)
    
    # Calculate total runs conceded and economy rate
    bowler_stats['total_runs_conceded'] = bowler_stats['runs_conceded'] + bowler_stats['extras_conceded']
    bowler_stats['overs_bowled'] = bowler_stats['balls_bowled'] / 6
    bowler_stats['economy_rate'] = bowler_stats['total_runs_conceded'] / bowler_stats['overs_bowled']
    bowler_stats['economy_rate'] = bowler_stats['economy_rate'].replace([float('inf'), float('-inf')], 0)
    
    # Get top 5 wicket-takers
    top_wicket_takers = bowler_stats.nlargest(5, 'wickets')
    
    print("\nTop 5 Wicket-Takers:")
    print("-" * 50)
    for idx, row in top_wicket_takers.iterrows():
        player = row['player']
        wickets = int(row['wickets'])
        economy = row['economy_rate']
        overs = row['overs_bowled']
        runs = int(row['total_runs_conceded'])
        
        print(f"{player}: {wickets} wickets, {overs:.1f} overs, {runs:,} runs, Econ: {economy:.2f}")

def question_6_highest_strike_rate(df):
    print_header("Highest Strike Rate in a Single Season (min. 200 balls)")
    
    # Calculate runs scored by each player in each season
    player_season_runs = df.groupby(['striker', 'season'])['runs_off_bat'].sum().reset_index()
    player_season_runs = player_season_runs.rename(columns={'striker': 'player', 'runs_off_bat': 'runs_scored'})
    
    # Calculate balls faced by each player in each season
    player_season_balls = df.groupby(['striker', 'season']).size().reset_index()
    player_season_balls = player_season_balls.rename(columns={'striker': 'player', 0: 'balls_faced'})
    
    # Merge runs and balls data
    player_season_stats = player_season_runs.merge(player_season_balls, on=['player', 'season'], how='left')
    
    # Calculate strike rate
    player_season_stats['strike_rate'] = (player_season_stats['runs_scored'] / player_season_stats['balls_faced']) * 100
    
    # Filter for players with minimum 200 balls faced
    qualified_players = player_season_stats[player_season_stats['balls_faced'] >= 200]
    
    # Get the player with highest strike rate
    highest_strike_rate = qualified_players.loc[qualified_players['strike_rate'].idxmax()]
    
    print(f"\nPlayer with Highest Strike Rate:")
    print(f"Player: {highest_strike_rate['player']}")
    print(f"Season: {int(highest_strike_rate['season'])}")
    print(f"Runs: {int(highest_strike_rate['runs_scored']):,}")
    print(f"Balls: {int(highest_strike_rate['balls_faced']):,}")
    print(f"Strike Rate: {highest_strike_rate['strike_rate']:.2f}")

def question_7_head_to_head(df):
    print_header("Head-to-Head Records Between Teams")
    
    # Get total runs scored by each team in each innings
    innings_totals = df.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()
    
    # Create match results
    match_results = []
    unique_matches = innings_totals['match_id'].unique()
    
    for match_id in unique_matches:
        match_data = innings_totals[innings_totals['match_id'] == match_id]
        
        if len(match_data) >= 2:
            innings = match_data.sort_values('innings')
            
            if len(innings) == 2:
                team1 = innings.iloc[0]['batting_team']
                score1 = innings.iloc[0]['runs_off_bat']
                team2 = innings.iloc[1]['batting_team']
                score2 = innings.iloc[1]['runs_off_bat']
                
                if score1 > score2:
                    match_results.append({'match_id': match_id, 'winner': team1, 'loser': team2})
                elif score2 > score1:
                    match_results.append({'match_id': match_id, 'winner': team2, 'loser': team1})
    
    results_df = pd.DataFrame(match_results)
    
    # Get unique teams
    teams = sorted(df['batting_team'].unique())
    
    # Calculate head-to-head records
    head_to_head = {}
    
    for team1, team2 in [(t1, t2) for t1 in teams for t2 in teams if t1 < t2]:
        team1_wins = len(results_df[(results_df['winner'] == team1) & (results_df['loser'] == team2)])
        team2_wins = len(results_df[(results_df['winner'] == team2) & (results_df['loser'] == team1)])
        
        if team1_wins > 0 or team2_wins > 0:
            head_to_head[f"{team1} vs {team2}"] = {
                'team1_wins': team1_wins,
                'team2_wins': team2_wins,
                'total_matches': team1_wins + team2_wins
            }
    
    # Sort by total matches played
    sorted_h2h = sorted(head_to_head.items(), key=lambda x: x[1]['total_matches'], reverse=True)
    
    print("\nTop 10 Head-to-Head Matchups:")
    print("-" * 50)
    for matchup, record in sorted_h2h[:10]:
        team1, team2 = matchup.split(" vs ")
        team1_wins = record['team1_wins']
        team2_wins = record['team2_wins']
        total = record['total_matches']
        
        print(f"{matchup}: {team1_wins} - {team2_wins} ({total} matches)")

def question_8_2023_powerplay(df):
    print_header("2023 IPL Power-Play Performance")
    
    # Filter for 2023 season
    df_2023 = df[df['season'] == 2023].copy()
    
    # Extract over number from ball column
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
    
    # Calculate overs and runs per over
    powerplay_stats['overs_faced'] = powerplay_stats['balls_faced'] / 6
    powerplay_stats['runs_per_over'] = powerplay_stats['total_runs'] / powerplay_stats['overs_faced']
    
    # Sort by runs per over (descending)
    powerplay_stats = powerplay_stats.sort_values('runs_per_over', ascending=False)
    
    print("\n2023 Power-Play Performance (Runs per Over):")
    print("-" * 50)
    for idx, row in powerplay_stats.iterrows():
        team = row['team']
        runs = int(row['total_runs'])
        overs = row['overs_faced']
        rpo = row['runs_per_over']
        
        print(f"{team}: {runs} runs in {overs:.1f} overs ({rpo:.2f} runs per over)")

def question_9_venue_analysis(df):
    print_header("Home Venue Effects in 2020-2021")
    
    # Filter for 2020 and 2021 seasons
    df_2020_2021 = df[df['season'].isin([2020, 2021])].copy()
    
    # Get total runs scored by each team in each innings
    innings_totals = df_2020_2021.groupby(['match_id', 'innings', 'batting_team'])['runs_off_bat'].sum().reset_index()
    
    # Create match results
    match_results = []
    unique_matches = innings_totals['match_id'].unique()
    
    for match_id in unique_matches:
        match_data = innings_totals[innings_totals['match_id'] == match_id]
        
        if len(match_data) >= 2:
            innings = match_data.sort_values('innings')
            
            if len(innings) == 2:
                team1 = innings.iloc[0]['batting_team']
                score1 = innings.iloc[0]['runs_off_bat']
                team2 = innings.iloc[1]['batting_team']
                score2 = innings.iloc[1]['runs_off_bat']
                
                if score1 > score2:
                    match_results.append({'match_id': match_id, 'winner': team1, 'loser': team2})
                elif score2 > score1:
                    match_results.append({'match_id': match_id, 'winner': team2, 'loser': team1})
    
    results_df = pd.DataFrame(match_results)
    
    # Get venue information for each match
    match_venues = df_2020_2021.groupby('match_id')['venue'].first().reset_index()
    
    # Merge results with venue information
    results_with_venues = results_df.merge(match_venues, on='match_id', how='left')
    
    # Analyze venue patterns for each team
    team_venue_analysis = {}
    teams = df_2020_2021['batting_team'].unique()
    
    for team in teams:
        team_matches = results_with_venues[
            (results_with_venues['winner'] == team) | 
            (results_with_venues['loser'] == team)
        ]
        
        if len(team_matches) > 0:
            venue_stats = {}
            for _, match in team_matches.iterrows():
                venue = match['venue']
                is_winner = match['winner'] == team
                
                if venue not in venue_stats:
                    venue_stats[venue] = {'wins': 0, 'total': 0}
                
                venue_stats[venue]['total'] += 1
                if is_winner:
                    venue_stats[venue]['wins'] += 1
            
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
    
    print(f"\nTeams played at multiple venues due to bio-bubble restrictions:")
    print("-" * 60)
    for team, venues in team_venue_analysis.items():
        if len(venues) > 1:  # Only show teams that played at multiple venues
            print(f"\n{team} ({len(venues)} venues):")
            for venue, stats in venues.items():
                print(f"  {venue}: {stats['wins']}/{stats['total']} wins ({stats['win_percentage']:.1f}%)")

# Main execution
if __name__ == "__main__":
    print("IPL DATA ANALYSIS - COMPREHENSIVE SUMMARY")
    print("="*80)
    print("Loading IPL match data...")
    
    start_time = time.time()
    df = pd.read_csv('match_data.csv', low_memory=False)
    df['season'] = pd.to_numeric(df['season'], errors='coerce')
    
    print(f"Data loaded successfully! Total records: {len(df):,}")
    print(f"Time taken to load data: {time.time() - start_time:.2f} seconds")
    
    # Run all analyses
    question_1_matches_per_season(df)
    question_2_team_records(df)
    question_4_top_run_scorers(df)
    question_5_top_wicket_takers(df)
    question_6_highest_strike_rate(df)
    question_7_head_to_head(df)
    question_8_2023_powerplay(df)
    question_9_venue_analysis(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"Total execution time: {time.time() - start_time:.2f} seconds") 