try:
    from nba_api.stats.endpoints import playergamelog
    print("✅ NBA API imported successfully!")
    
    # Test with LeBron
    lebron_id = "2544"
    print(f"🏀 Attempting to get LeBron's data (ID: {lebron_id})...")
    
    gamelog = playergamelog.PlayerGameLog(player_id=lebron_id, season='2023-24')
    print("✅ API call successful!")
    
    df = gamelog.get_data_frames()[0]
    print(f"✅ Found {len(df)} games")
    print("First game data:")
    print(df.iloc[0]['GAME_DATE'], df.iloc[0]['PTS'], "points")
    
except Exception as e:
    print(f"❌ Error: {e}")