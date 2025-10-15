import os
import json
import pandas as pd

# Team mappings for our players
# CORRECTED Team mappings for 2024-25 season
TEAM_MAPPINGS = {
    "Nikola_Jokic": "DEN Nuggets",
    "Shai_Gilgeous-Alexander": "OKC Thunder", 
    "Giannis_Antetokounmpo": "MIL Bucks",
    "Luka_Doncic": "LAL Lakers",  # FIXED - Luka to Lakers
    "Stephen_Curry": "GSW Warriors",
    "Anthony_Edwards": "MIN Timberwolves",
    "Tyrese_Haliburton": "IND Pacers",
    "Donovan_Mitchell": "CLE Cavaliers",
    "Jalen_Brunson": "NYK Knicks",
    "Jayson_Tatum": "BOS Celtics",
    "Victor_Wembanyama": "SAS Spurs",
    "LeBron_James": "LAL Lakers",
    "Anthony_Davis": "DAL Mavericks",  # FIXED - AD to Mavs
    "Kevin_Durant": "HOU Rockets",  # FIXED - KD to Rockets
    "Kawhi_Leonard": "LAC Clippers",
    "Cade_Cunningham": "DET Pistons",
    "Evan_Mobley": "CLE Cavaliers",
    "Karl-Anthony_Towns": "NYK Knicks",
    "Devin_Booker": "PHX Suns",
    "Jalen_Williams": "OKC Thunder",
    "Jaylen_Brown": "BOS Celtics",
    "Paolo_Banchero": "ORL Magic",
    "Pascal_Siakam": "IND Pacers",
    "Jimmy_Butler": "GSW Warriors",  # FIXED - Jimmy to Warriors
    "Jaren_Jackson_Jr": "MEM Grizzlies",
    "De'Aaron_Fox": "SAS Spurs",  # FIXED - Fox to Spurs
    "Chet_Holmgren": "OKC Thunder",
    "Darius_Garland": "CLE Cavaliers",
    "Jamal_Murray": "DEN Nuggets",
    "James_Harden": "LAC Clippers",
    "Domantas_Sabonis": "SAC Kings",
    "Bam_Adebayo": "MIA Heat",
    "Trae_Young": "ATL Hawks",
    "Ja_Morant": "MEM Grizzlies",
    "Ivica_Zubac": "LAC Clippers",
    "Alperen_Sengun": "HOU Rockets",
    "Franz_Wagner": "ORL Magic",
    "Derrick_White": "BOS Celtics",
    "Tyrese_Maxey": "PHI 76ers",
    "OG_Anunoby": "NYK Knicks",
    "Amen_Thompson": "HOU Rockets",
    "Aaron_Gordon": "DEN Nuggets",
    "Damian_Lillard": "MIL Bucks",  # Keeping as Buck like you said
    "Kyrie_Irving": "DAL Mavericks",
    "Zion_Williamson": "NOP Pelicans",
    "Scottie_Barnes": "TOR Raptors",
    "Desmond_Bane": "ORL Magic",  # FIXED - Bane to Magic
    "Jalen_Johnson": "ATL Hawks",
    "LaMelo_Ball": "CHA Hornets",
    "Draymond_Green": "GSW Warriors"
}

def calculate_average(games, metric):
    """Calculate average for a metric"""
    values = []
    for game in games:
        try:
            val = float(game.get(metric, 0))
            if not pd.isna(val):
                values.append(val)
        except:
            continue
    
    if len(values) == 0:
        return 0
    
    avg = sum(values) / len(values)
    return round(avg, 1)

def convert_csv_to_json(csv_filename):
    """Convert a CSV file to JSON format"""
    try:
        # Read CSV
        df = pd.read_csv(csv_filename)
        
        # Get player name from filename
        player_name = csv_filename.replace('_advanced_metrics.csv', '').replace('_', ' ')
        
        # Get team from mapping
        team = TEAM_MAPPINGS.get(csv_filename.replace('_advanced_metrics.csv', ''), "Unknown Team")
        
        # Convert to list of dictionaries
        games = df.to_dict('records')
        
        # Calculate season averages
        season_averages = {
            'DIS': calculate_average(games, 'DIS'),
            'OGI': calculate_average(games, 'OGI'),
            'Contest_Rate': calculate_average(games, 'Contest_Rate'),
            'Rim_Deterrence': calculate_average(games, 'Rim_Deterrence'),
            'TO_Pressure': calculate_average(games, 'TO_Pressure'),
            'OnOff_Net': calculate_average(games, 'OnOff_Net')
        }
        
        # Format recent games (last 5)
        recent_games = []
        for i, game in enumerate(games[:5]):
            recent_games.append({
                'date': game.get('GAME_DATE', 'Unknown'),
                'opponent': game.get('MATCHUP', 'vs OPP'),
                'DIS': str(round(float(game.get('DIS', 0)), 1)),
                'OGI': str(round(float(game.get('OGI', 0)), 1)),
                'points': game.get('PTS', 0),
                'assists': game.get('AST', 0)
            })
        
        # Create final JSON structure
        player_data = {
            'name': player_name,
            'team': team,
            'totalGames': len(games),
            'games': games,
            'seasonAverages': season_averages,
            'recentGames': recent_games
        }
        
        # Save JSON file
        json_filename = csv_filename.replace('_advanced_metrics.csv', '_data.json')
        with open(json_filename, 'w') as f:
            json.dump(player_data, f, indent=2)
        
        print(f"✅ Converted {csv_filename} to {json_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {csv_filename}: {e}")
        return False

def main():
    """Convert all CSV files to JSON"""
    print("🔄 Converting all CSV files to JSON...")
    
    # Find all CSV files
    csv_files = [f for f in os.listdir('.') if f.endswith('_advanced_metrics.csv')]
    
    successful = 0
    failed = 0
    
    for csv_file in csv_files:
        if convert_csv_to_json(csv_file):
            successful += 1
        else:
            failed += 1
    
    print(f"\n🎉 Conversion complete! {successful} files converted successfully, {failed} failed.")

if __name__ == "__main__":
    main()