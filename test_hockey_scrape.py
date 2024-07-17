import pytest
from hockey_scrape import process_team_data, calculate_winner_loser

# Mock data
mock_team_data = [
    {'TeamName': 'Team A', 'Year': '1990', 'Win': 10, 'Losses': 5, 'OTLosses': 2, 'WinPercentage': '60%', 'GoalsFor(GF)': 50, 'GoalsAgainst(GA)': 40, '+/-': '+10'},
    {'TeamName': 'Team B', 'Year': '1990', 'Win': 12, 'Losses': 3, 'OTLosses': 1, 'WinPercentage': '75%', 'GoalsFor(GF)': 60, 'GoalsAgainst(GA)': 30, '+/-': '+30'},
    {'TeamName': 'Team C', 'Year': '1991', 'Win': 20, 'Losses': 10, 'OTLosses': 5, 'WinPercentage': '60%', 'GoalsFor(GF)': 70, 'GoalsAgainst(GA)': 50, '+/-': '+20'},
    {'TeamName': 'Team D', 'Year': '1991', 'Win': 15, 'Losses': 12, 'OTLosses': 3, 'WinPercentage': '55%', 'GoalsFor(GF)': 65, 'GoalsAgainst(GA)': 60, '+/-': '+5'}
]

def test_process_team_data():
    """Test the process_team_data function"""
    processed_data = process_team_data(mock_team_data)
    assert len(processed_data['TeamName']) == 4
    assert processed_data['TeamName'][0] == 'Team A'
    assert processed_data['Year'][1] == '1990'
    assert processed_data['Win'][2] == 20
    assert processed_data['GoalsFor(GF)'][3] == 65
    assert processed_data['+/-'][1] == '+30'

def test_calculate_winner_loser():
    """Test the calculate_winner_loser function"""
    winners_losers = calculate_winner_loser(mock_team_data)
    assert winners_losers['1990']['winner']['team'] == 'Team B'
    assert winners_losers['1990']['loser']['team'] == 'Team A'
    assert winners_losers['1991']['winner']['team'] == 'Team C'
    assert winners_losers['1991']['loser']['team'] == 'Team D'
