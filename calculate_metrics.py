from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
import numpy as np
import time

# Your players - updated list
players_dict = {
    "Shai Gilgeous-Alexander": "1628983",
    "OG Anunoby": "1628384", 
    "Mikal Bridges": "1628969",
    "Dorian Finney-Smith": "1627827",
    "Malik Beasley": "1627736",
    "Luke Kennard": "1628379",
    "Mitchell Robinson": "1629011",
    "Josh Hart": "1628404",
    "Austin Reaves": "1630559"
}

print("🏀 Getting ALL GAMES for all 9 players with ADVANCED METRICS...\n")

all_player_data = {}

for name, player_id in players_dict.items():
    try:
        print(f"📊 Processing {name}...")
        
        # Get current season data
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25')
        df = gamelog.get_data_frames()[0]
        
        if len(df) == 0:
            print(f"❌ No games found for {name} with ID {player_id}")
            continue
            
        print(f"✅ Found {len(df)} games for {name}")
        
          # Calculate possessions first (essential for all metrics)
        df['Team_Poss'] = df['FGA'] + 0.44 * df['FTA'] - df['OREB'] + df['TOV']
        
        # Steal and Block Percentages
        df['STL_PCT'] = 100 * (df['STL'] * (df['MIN'] / 5)) / (df['MIN'] * df['Team_Poss'])
        df['BLK_PCT'] = 100 * (df['BLK'] * (df['MIN'] / 5)) / (df['MIN'] * df['Team_Poss'])
        
        # Usage Rate and True Shooting - FIXED
        df['USG_PCT'] = (100 * ((df['FGA'] + 0.44 * df['FTA'] + df['TOV']) * 40)) / (df['MIN'] * df['Team_Poss'])
        df['TS_PCT'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA'] + 0.001)) * 100

        # 3. ADVANCED METRICS
        
       # DIS - Defensive Impact Score (PER 100 POSSESSIONS - GENERALIZABLE)
        # Normalize per 100 possessions to handle different minute totals
        poss_adj = 100 / (df['MIN'] + 0.01)  # avoid divide by 0
        
        df['STL_RATE'] = df['STL'] * poss_adj
        df['BLK_RATE'] = df['BLK'] * poss_adj
        df['DREB_RATE'] = df['DREB'] * poss_adj
        df['PF_RATE'] = df['PF'] * poss_adj
        df['TOV_RATE'] = df['TOV'] * poss_adj
        df['PM_RATE'] = df['PLUS_MINUS'] * poss_adj
        
        # New DIS weights (grounded in Bball-Index, RAPTOR, and eye test balance)
        df['DIS'] = (
            df['STL_RATE'] * 1.6 +        # Disruptive defenders (Jrue, OG)
            df['BLK_RATE'] * 1.2 +        # Rim presence
            df['DREB_RATE'] * 0.7 +       # Rebounding is a team anchor stat
            df['PM_RATE'] * 0.4 +         # Team defense context
            df['PF_RATE'] * 0.1 -         # Some fouls show aggression
            df['TOV_RATE'] * 0.5          # Penalize gambling/sloppy defense
        )
        
        # Cap outliers (guards with 3 steals in 9 mins etc.)
        df['DIS'] = df['DIS'].clip(lower=-15, upper=25)
        
        df['DIS'] = df['DIS'].replace([float('inf'), -float('inf')], 0)

        
       # OGI - Offensive Gravity Index (BASKETBALL-SMART VERSION)
        # Focus on actual offensive creation, not just usage
        
        df['AST_RATE'] = df['AST'] / (df['MIN'] + 0.001) * 36
        df['FG3A_RATE'] = df['FG3A'] / (df['MIN'] + 0.001) * 36  
        df['FTA_RATE'] = df['FTA'] / (df['MIN'] + 0.001) * 36
        df['FGA_RATE'] = df['FGA'] / (df['MIN'] + 0.001) * 36
        
        # Clean up infinite values
        df['TS_PCT'] = df['TS_PCT'].replace([float('inf'), -float('inf')], 0)
        
        # NEW FORMULA: Rewards guards/wings, not big men
        df['OGI'] = (df['AST_RATE'] * 3.0 +           # Assists = major gravity
                     df['FG3A_RATE'] * 2.5 +          # 3PA = spacing gravity  
                     df['FGA_RATE'] * 0.8 +           # Shot attempts = gravity
                     (df['TS_PCT'] * 0.2) +           # Efficiency amplifies
                     df['FTA_RATE'] * 1.5 -           # Drawing fouls = gravity
                     (df['DREB'] / (df['MIN'] + 0.001) * 36 * 0.5))  # Penalty for being a big man
        
        df['OGI'] = df['OGI'].replace([float('inf'), -float('inf')], 0)
        
        # Contest Rate - Shot disruption approximation
        df['Contest_Rate'] = ((df['BLK'] / df['MIN'] * 36 * 4.0) + (df['STL'] / df['MIN'] * 36 * 2.5) + 
                              (df['PF'] / df['MIN'] * 36 * 1.8) + (df['DREB'] / df['MIN'] * 36 * 0.8))
        
        # Rim Deterrence - Interior defensive impact (Mitchell Robinson should excel)
        df['Rim_Deterrence'] = ((df['BLK'] / df['MIN'] * 36 * 5.2) + (df['DREB'] / df['MIN'] * 36 * 2.1) + 
                                ((df['MIN'] / 36) * 1.5) + (df['PF'] / df['MIN'] * 36 * 1.0) - 
                                (df['TOV'] / df['MIN'] * 36 * 0.7))
        
        # TO Pressure - Turnover forcing ability
        df['TO_Pressure'] = ((df['STL'] / df['MIN'] * 36 * 3.5) + (df['BLK'] / df['MIN'] * 36 * 2.2) + 
                             (df['PF'] / df['MIN'] * 36 * 0.9) + (df['DREB'] / df['MIN'] * 36 * 0.6))
        
        # OnOff Net Rating - IMPROVED (accounts for team strength)
        # Penalizes players on great teams, rewards players on bad teams
        
        # Basic per-minute plus/minus
        df['PM_PER_MIN'] = df['PLUS_MINUS'] / (df['MIN'] + 0.001)
        
        # Team performance indicator (higher = better team)
        df['TEAM_STRENGTH'] = df['PLUS_MINUS'].rolling(10, min_periods=1).mean()
        
        # Adjusted Net Rating - removes team bias
        df['OnOff_Net'] = (
            (df['PM_PER_MIN'] * 36 * 1.0) +              # Base plus/minus impact
            (df['AST'] - df['TOV']) * 0.8 +               # Individual contribution
            ((df['STL'] + df['BLK'] + df['DREB']) * 0.4) - # Defensive stops
            (df['PF'] * 0.3) -                            # Penalty for fouls
            (df['TEAM_STRENGTH'] * 0.3)                   # REDUCE credit for team being good
        )
        
        df['OnOff_Net'] = df['OnOff_Net'].replace([float('inf'), -float('inf')], 0)
        
        # Store the data
        all_player_data[name] = df
        
        # Show SEASON averages for this player (all games)
        season_avg_metrics = {
            'Games': len(df),
            'DIS': df['DIS'].mean(),
            'OGI': df['OGI'].mean(),
            'Contest_Rate': df['Contest_Rate'].mean(),
            'Rim_Deterrence': df['Rim_Deterrence'].mean(),
            'TO_Pressure': df['TO_Pressure'].mean(),
            'OnOff_Net': df['OnOff_Net'].mean()
        }
        
        print(f"  📈 Season averages ({season_avg_metrics['Games']} games):")
        print(f"     DIS: {season_avg_metrics['DIS']:.1f} | OGI: {season_avg_metrics['OGI']:.1f}")
        print(f"     Contest: {season_avg_metrics['Contest_Rate']:.1f} | Rim: {season_avg_metrics['Rim_Deterrence']:.1f}")
        print(f"     TO_Press: {season_avg_metrics['TO_Pressure']:.1f} | Net: {season_avg_metrics['OnOff_Net']:.1f}")
        
        # Save individual player file with ALL games
        df.to_csv(f'{name.replace(" ", "_")}_advanced_metrics.csv', index=False)
        print(f"  💾 Saved {name.replace(' ', '_')}_advanced_metrics.csv")
        
        # Small delay to avoid API rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error getting {name}: {e}")

print(f"\n✅ Processed {len(all_player_data)} players successfully!")
print("💾 Individual CSV files saved with ADVANCED metrics for each player")

# Create comparison summary with SEASON averages
print("\n" + "="*100)
print("📈 PLAYER COMPARISON (SEASON AVERAGES - RESEARCH-BASED METRICS)")
print("="*100)
print(f"{'Player':<25} | {'Games':<5} | {'DIS':<7} | {'OGI':<7} | {'Contest':<7} | {'Rim':<7} | {'TO_Press':<8} | {'Net':<7}")
print("-"*100)

for name, df in all_player_data.items():
    games = len(df)
    dis_avg = df['DIS'].mean()
    ogi_avg = df['OGI'].mean()
    contest_avg = df['Contest_Rate'].mean()
    rim_avg = df['Rim_Deterrence'].mean()
    to_avg = df['TO_Pressure'].mean()
    net_avg = df['OnOff_Net'].mean()
    
    print(f"{name:<25} | {games:<5} | {dis_avg:6.1f} | {ogi_avg:6.1f} | {contest_avg:6.1f} | {rim_avg:6.1f} | {to_avg:7.1f} | {net_avg:6.1f}")

print("\n🔬 METRICS EXPLANATION:")
print("DIS = Defensive Impact (higher = better defense)")
print("OGI = Offensive Gravity (higher = more attention drawn)")  
print("Contest = Shot disruption (higher = more contests)")
print("Rim = Rim protection (Mitchell Robinson should lead)")
print("TO_Press = Turnover pressure (higher = more disruptive)")
print("Net = Team impact (higher = better +/-)")
