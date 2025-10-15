from nba_api.stats.endpoints import playergamelog, playeronoffdetails
import pandas as pd
import time

# LeBron's player ID
lebron_id = "2544"

print("🏀 Pulling LeBron's data...")

# Get basic game log
gamelog = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023-24')
games_df = gamelog.get_data_frames()[0]

print(f"✅ Found {len(games_df)} games for LeBron")
print("\nLast 5 games basic stats:")
print(games_df[['GAME_DATE', 'MATCHUP', 'PTS', 'AST', 'STL', 'BLK', 'MIN']].head())

# Save basic data
games_df.to_csv('lebron_games.csv', index=False)
print("\n💾 Saved to lebron_games.csv")