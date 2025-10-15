import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta

# NBA API endpoints
PLAYER_INFO_URL = "https://stats.nba.com/stats/commonplayerinfo"
PLAYER_GAMES_URL = "https://stats.nba.com/stats/playergamelog"
TEAM_GAMES_URL = "https://stats.nba.com/stats/teamgamelog"

# Headers to mimic browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nba.com/',
    'Connection': 'keep-alive',
}

# Our 50 NBA players with their OFFICIAL NBA.com player IDs
NBA_PLAYERS = {
    "Nikola_Jokic": "203999",
    "Shai_Gilgeous-Alexander": "1628983", 
    "Giannis_Antetokounmpo": "203507",
    "Luka_Doncic": "1629029",
    "Stephen_Curry": "201939",
    "Anthony_Edwards": "1630162",
    "Tyrese_Haliburton": "1630169",
    "Donovan_Mitchell": "1628378",
    "Jalen_Brunson": "1628973",
    "Jayson_Tatum": "1628369",
    "Victor_Wembanyama": "1641705",
    "LeBron_James": "2544",
    "Anthony_Davis": "203076",
    "Kevin_Durant": "201142",
    "Kawhi_Leonard": "202695",
    "Cade_Cunningham": "1630595",
    "Evan_Mobley": "1630596",
    "Karl-Anthony_Towns": "1626157",
    "Devin_Booker": "1626164",
    "Jalen_Williams": "1631094",
    "Jaylen_Brown": "1627759",
    "Paolo_Banchero": "1630591",
    "Pascal_Siakam": "1627783",
    "Jimmy_Butler": "202710",
    "Jaren_Jackson_Jr": "1628991",
    "De'Aaron_Fox": "1628368",
    "Chet_Holmgren": "1631166",
    "Darius_Garland": "1629636",
    "Jamal_Murray": "1627750",
    "James_Harden": "201935",
    "Domantas_Sabonis": "1627734",
    "Bam_Adebayo": "1628389",
    "Trae_Young": "1629027",
    "Ja_Morant": "1629630",
    "Ivica_Zubac": "1627826",
    "Alperen_Sengun": "1630578",
    "Franz_Wagner": "1630532",
    "Derrick_White": "1628401",
    "Tyrese_Maxey": "1630178",
    "OG_Anunoby": "1628384",
    "Amen_Thompson": "1641720",
    "Aaron_Gordon": "203932",
    "Damian_Lillard": "203081",
    "Kyrie_Irving": "202681",
    "Zion_Williamson": "1629627",
    "Scottie_Barnes": "1630567",
    "Desmond_Bane": "1630217",
    "Jalen_Johnson": "1630550",
    "LaMelo_Ball": "1630163",
    "Draymond_Green": "203110"
}

def get_player_game_log(player_id, season="2024-25"):
    """Get player's game log for the season"""
    params = {
        'PlayerID': player_id,
        'Season': season,
        'SeasonType': 'Regular Season'
    }
    
    try:
        response = requests.get(PLAYER_GAMES_URL, headers=HEADERS, params=params)
        data = response.json()
        
        if data['resultSets'] and len(data['resultSets']) > 0:
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            return pd.DataFrame(rows, columns=headers)
        return None
        
    except Exception as e:
        print(f"Error fetching data for player {player_id}: {e}")
        return None

def calculate_advanced_metrics(df):
    """Calculate advanced impact metrics with realistic NBA ranges"""
    if df is None or df.empty:
        return df
    
    # Estimate possessions per player
    df['MIN'] = df['MIN'].astype(float)
    df['Poss'] = df['MIN'] * 0.8  # Approximation
    
    # --- Defensive Impact Score (DIS) --- Target range: 5-35
    df['STL_RATE'] = df['STL'] / (df['Poss'] + 0.001)
    df['BLK_RATE'] = df['BLK'] / (df['Poss'] + 0.001)
    df['DREB_RATE'] = df['DREB'] / (df['Poss'] + 0.001)
    df['PF_RATE'] = df['PF'] / (df['Poss'] + 0.001)
    df['TOV_RATE'] = df['TOV'] / (df['Poss'] + 0.001)
    df['PM_RATE'] = df['PLUS_MINUS'] / (df['Poss'] + 0.001)
    
    df['DIS'] = (
        df['STL_RATE'] * 300.0 +
        df['BLK_RATE'] * 250.0 +
        df['DREB_RATE'] * 80.0 -
        df['PF_RATE'] * 40.0 +
        df['PM_RATE'] * 15.0 -
        df['TOV_RATE'] * 30.0
    )
    
    # --- Offensive Gravity Index (OGI) --- Target range: 10-60
    df['AST_RATE'] = df['AST'] / (df['Poss'] + 0.001)
    df['FG3A_RATE'] = df['FG3A'] / (df['Poss'] + 0.001)
    df['FTA_RATE'] = df['FTA'] / (df['Poss'] + 0.001)
    df['FGA_RATE'] = df['FGA'] / (df['Poss'] + 0.001)
    
    df['OGI'] = (
        df['AST_RATE'] * 70.0 +       # LOWERED from 120
        df['FG3A_RATE'] * 50.0 +      # LOWERED from 80
        df['FTA_RATE'] * 35.0 +       # LOWERED from 60
        df['FGA_RATE'] * 25.0         # LOWERED from 40
    )
    
    # --- Other Metrics ---
    df['Contest_Rate'] = ((df['BLK'] + df['STL']) / (df['MIN'] + 0.001)) * 48
    df['Rim_Deterrence'] = df['BLK_RATE'] * 200.0 + df['DREB_RATE'] * 25.0
    df['TO_Pressure'] = df['STL_RATE'] * 200.0
    df['OnOff_Net'] = df['PM_RATE'] * 10.0 + (df['AST_RATE'] * 20.0) - (df['TOV_RATE'] * 15.0)
    
    # Replace any crazy outliers
    df.replace([float('inf'), -float('inf')], 0, inplace=True)
    df.fillna(0, inplace=True)
    
    return df

def process_player(player_name, player_id):
    """Process a single player's data"""
    print(f"Processing {player_name}...")
    
    # Get game log
    game_log = get_player_game_log(player_id)
    if game_log is None:
        print(f"Failed to get data for {player_name}")
        return False
    
    # Calculate advanced metrics
    processed_data = calculate_advanced_metrics(game_log)
    
    # Save to CSV
    filename = f"{player_name}_advanced_metrics.csv"
    processed_data.to_csv(filename, index=False)
    print(f"Saved {filename}")
    
    # Add delay to avoid rate limiting
    time.sleep(1)
    return True

def main():
    """Main function to process all players"""
    print("🏀 Starting NBA Data Collection for 50 Players...")
    
    successful = 0
    failed = 0
    
    for player_name, player_id in NBA_PLAYERS.items():
        if process_player(player_name, player_id):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Complete! {successful} players processed successfully, {failed} failed.")

if __name__ == "__main__":
    main()