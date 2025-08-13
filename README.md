# Task_05_Descriptive_Stats: IPL Data Analysis

## Project Overview

This repository contains a comprehensive analysis of Indian Premier League (IPL) cricket data from 2008-2023, comparing Python-based statistical analysis with ChatGPT responses. The project explores the capabilities and limitations of Large Language Models (LLMs) in sports data analysis.

## Research Objective

The primary goal is to evaluate how well LLMs can answer natural language questions about sports data, particularly cricket statistics. This involves:

- Comparing Python-based analysis with ChatGPT responses
- Identifying strengths and limitations of LLM data analysis
- Developing complex prompts for advanced analytical questions
- Exploring the research-oriented nature of LLM-assisted data analysis

## Dataset

The analysis uses ball-by-ball IPL match data containing:
- Match details (ID, season, venue, date)
- Ball-by-ball information (runs, extras, wickets)
- Player statistics (batsmen, bowlers, dismissals)
- Team performance metrics

**Note**: The dataset file (`match_data.csv`) is not included in this repository due to size constraints.

## Repository Structure

```
Task_05_Descriptive_Stats/
├── README.md                           # This file
├── comparison_results.md               # Detailed comparison of Python vs ChatGPT results
├── all_questions_summary.py            # Comprehensive analysis script
├── question_1.py                       # Matches per season analysis
├── question_2_fixed.py                 # Team win-loss records
├── question_4.py                       # Top run-scorers analysis
├── question_5.py                       # Top wicket-takers analysis
├── question_6.py                       # Highest strike rate analysis
├── question_7.py                       # Head-to-head records
├── question_8_fixed.py                 # 2023 power-play performance
├── question_9.py                       # Home venue effects (2020-2021)
├── question_10.py                      # Team avg scored/conceded and differentials
├── question_11.py                      # 1st-innings total vs win probability (correlation)
├── question_12.py                      # Highest scoring season + extras proxy
├── question_13.py                      # Player impact score (global ranking)
├── question_14.py                      # 2022 most improved (rolling 5-match)
├── question_15.py                      # Coach recommendation & game-changer
└── question_16.py                      # Logistic regression predictor strength
```

## Key Questions Analyzed

### A. Basic Descriptive Questions
1. **Total matches per IPL season (2008-2023)**
2. **Team win-loss records across all seasons**
3. **Toss analysis** (limited by data availability)

### B. Player-Level Insights
4. **Top 5 run-scorers and batting averages**
5. **Top 5 wicket-takers and economy rates**
6. **Highest strike rate in a single season**

### C. Team-Level & Head-to-Head Analysis
7. **Head-to-head records between franchises**
8. **2023 power-play performance**
9. **Home venue effects during bio-bubble seasons**

## Key Findings

### Python Analysis Results
- **Total Matches**: 846 matches across 13 seasons (2009-2023)
- **Top Run-Scorer**: V Kohli (7,273 runs, Avg: 37.30)
- **Top Wicket-Taker**: DJ Bravo (207 wickets, Econ: 8.08)
- **Best Power-Play 2023**: Chennai Super Kings (9.03 runs per over)
- **Most Successful Team**: Chennai Super Kings (57.1% win rate)

### ChatGPT Comparison
- **Strengths**: Honest about data limitations, consistent run totals, clear communication
- **Concerns**: Inconsistent match counts, varying player statistics, different dataset versions
- **Data Awareness**: Correctly identified missing toss information

## Usage

### Prerequisites
```bash
pip install pandas numpy
```

### Running Individual Analyses
```bash
# Run comprehensive analysis
python all_questions_summary.py

# Run specific questions
python question_1.py      # Matches per season
python question_2_fixed.py # Team records
python question_4.py      # Top run-scorers
python question_5.py      # Top wicket-takers
python question_6.py      # Highest strike rate
python question_7.py      # Head-to-head records
python question_8_fixed.py # 2023 power-play
python question_9.py      # Venue effects

# Advanced analyses
python question_10.py     # Team avg scored/conceded and differential
python question_11.py     # 1st-innings total vs win probability
python question_12.py     # Highest scoring season + extras proxy
python question_13.py     # Player impact score (top 5)
python question_14.py     # 2022 most improved (rolling 5)
python question_15.py     # Coach strategy & game-changer
python question_16.py     # Logistic regression predictors
```

### Data Requirements
Place the `match_data.csv` file in the repository directory before running the scripts. The file should contain ball-by-ball IPL data with columns:
- match_id, season, start_date, venue
- innings, ball, batting_team, bowling_team
- striker, non_striker, bowler
- runs_off_bat, extras, wicket_type, player_dismissed

## Research Methodology

### Python Analysis Approach
1. **Data Loading**: Pandas-based CSV processing with error handling
2. **Match Result Calculation**: Aggregating innings totals to determine winners
3. **Player Statistics**: Calculating runs, wickets, averages, and rates
4. **Team Analysis**: Win-loss records and head-to-head comparisons
5. **Seasonal Analysis**: Power-play performance and venue effects

### ChatGPT Prompt Strategy
- Direct questions about specific statistics
- Requests for structured tabular responses
- Validation of data availability before analysis
- Comparison with known cricket statistics

## Future Research Directions

### Complex Prompts for Next Phase
1. **Advanced Statistical Measures**
   - Player improvement metrics over seasons
   - Clutch performance analysis
   - Momentum and form calculations

2. **Predictive Analysis**
   - "As a coach, if I wanted to win two more games this coming season, should I focus on offense or defense?"
   - "What is the one player I should work with to be a game changer and why?"

3. **Complex Metrics Development**
   - Defining "most improved player" with quantifiable measures
   - Creating composite performance indices
   - Analyzing situational performance

4. **Visualization Requests**
   - Requesting charts and graphs directly from the LLM
   - Performance trend analysis
   - Comparative visualizations

5. **Strategic Analysis**
   - Team composition optimization
   - Match strategy recommendations
   - Player role analysis

## Technical Details

### Data Processing
- **Dataset Size**: 243,817 ball-by-ball records
- **Time Period**: 2008-2023 (13 seasons)
- **Teams Analyzed**: 18 franchises
- **Players Analyzed**: 637 batsmen, 436 bowlers

### Analysis Performance
- **Data Loading Time**: ~0.36 seconds
- **Total Analysis Time**: ~1.04 seconds
- **Memory Usage**: Optimized for large dataset processing

## Limitations and Considerations

### Dataset Limitations
- Missing seasons: 2008, 2010 not in current dataset
- No toss information available
- Incomplete 2021 season data
- Ball-by-ball granularity may miss some match-level details

### Analysis Limitations
- Win-loss calculation based on innings totals
- Player statistics may vary due to different counting methods
- Venue analysis limited to available match data

## Contributing

This is a research project focused on LLM capabilities in sports data analysis. Contributions should focus on:
- Improving analytical methodologies
- Developing more sophisticated prompts
- Enhancing data validation techniques
- Expanding comparative analysis frameworks

## License

This project is for educational and research purposes. The IPL data used is publicly available cricket statistics.

## Contact

For questions about this research project, please refer to the course instructor or use the provided email contact in the course materials.

---

**Note**: This repository is part of a research task exploring LLM capabilities in sports data analysis. The focus is on understanding how well Large Language Models can process and analyze complex sports statistics through natural language queries.

## Additional Analyses (Q10–Q16)

These scripts extend the analysis with advanced, metric-driven, and strategic questions. Summaries below are based on the current dataset and code logic.

- Q10: Team average runs scored/conceded per match and differential
  - Largest positive differential: Gujarat Titans (~+8.18 runs/match). Chennai Super Kings and Mumbai Indians also positive.

- Q11: Correlation between first-innings total and probability of winning
  - Win rate rises with higher first-innings bins (e.g., >200 ≈ 94% win). Pearson correlation ≈ 0.322.

- Q12: Highest overall scoring season (avg total runs/match) and factors
  - Highest: 2023 (~330.1 runs/match). Extras/match among top seasons elevated, suggesting batting-friendly conditions and/or discipline/rule effects.

- Q13: Player impact score
  - Definition: (runs + wickets) / matches × (team win% with player / team overall win%).
  - Example top 5: CA Lynn, AJ Finch, S Dhawan, KL Rahul, AM Rahane.

- Q14: Most improved (2022) with rolling 5-match windows
  - Batsman example: RD Gaikwad (≈ +25.5 runs/match).
  - Bowler example: DR Sams (≈ −20.9 runs conceded/match).
  - Improvement defined as last − first (batting runs rolling mean); first − last (bowling runs conceded rolling mean).

- Q15: Coach strategy and game-changer
  - Win% increases with net run differential (runs scored − conceded). Recommendation: improve batting totals and suppress opponent scoring.
  - Suggested game-changer example: S Dhawan (high base output; strong team win% when appearing).

- Q16: Logistic regression (venue, first_runs, opponent strength)
  - Test AUC ≈ 0.572. Strongest numeric predictors by |coef|: opponent strength, chasing; first_runs smaller after one-hot venue encoding.

Re-run locally with your `match_data.csv` to refresh these summaries.
