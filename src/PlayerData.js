// PlayerData.js - All 50 NBA Players

const PLAYER_FILES = [
  { name: "Nikola Jokic", file: "Nikola_Jokic_data.json", team: "DEN Nuggets" },
  { name: "Shai Gilgeous-Alexander", file: "Shai_Gilgeous-Alexander_data.json", team: "OKC Thunder" },
  { name: "Giannis Antetokounmpo", file: "Giannis_Antetokounmpo_data.json", team: "MIL Bucks" },
  { name: "Luka Doncic", file: "Luka_Doncic_data.json", team: "DAL Mavericks" },
  { name: "Stephen Curry", file: "Stephen_Curry_data.json", team: "GSW Warriors" },
  { name: "Anthony Edwards", file: "Anthony_Edwards_data.json", team: "MIN Timberwolves" },
  { name: "Tyrese Haliburton", file: "Tyrese_Haliburton_data.json", team: "IND Pacers" },
  { name: "Donovan Mitchell", file: "Donovan_Mitchell_data.json", team: "CLE Cavaliers" },
  { name: "Jalen Brunson", file: "Jalen_Brunson_data.json", team: "NYK Knicks" },
  { name: "Jayson Tatum", file: "Jayson_Tatum_data.json", team: "BOS Celtics" },
  { name: "Victor Wembanyama", file: "Victor_Wembanyama_data.json", team: "SAS Spurs" },
  { name: "LeBron James", file: "LeBron_James_data.json", team: "LAL Lakers" },
  { name: "Anthony Davis", file: "Anthony_Davis_data.json", team: "DAL Mavericks" },
  { name: "Kevin Durant", file: "Kevin_Durant_data.json", team: "PHX Suns" },
  { name: "Kawhi Leonard", file: "Kawhi_Leonard_data.json", team: "LAC Clippers" },
  { name: "Cade Cunningham", file: "Cade_Cunningham_data.json", team: "DET Pistons" },
  { name: "Evan Mobley", file: "Evan_Mobley_data.json", team: "CLE Cavaliers" },
  { name: "Karl-Anthony Towns", file: "Karl-Anthony_Towns_data.json", team: "NYK Knicks" },
  { name: "Devin Booker", file: "Devin_Booker_data.json", team: "PHX Suns" },
  { name: "Jalen Williams", file: "Jalen_Williams_data.json", team: "OKC Thunder" },
  { name: "Jaylen Brown", file: "Jaylen_Brown_data.json", team: "BOS Celtics" },
  { name: "Paolo Banchero", file: "Paolo_Banchero_data.json", team: "ORL Magic" },
  { name: "Pascal Siakam", file: "Pascal_Siakam_data.json", team: "IND Pacers" },
  { name: "Jimmy Butler", file: "Jimmy_Butler_data.json", team: "GSW Warriors" },
  { name: "Jaren Jackson Jr", file: "Jaren_Jackson_Jr_data.json", team: "MEM Grizzlies" },
  { name: "De'Aaron Fox", file: "De'Aaron_Fox_data.json", team: "SAC Kings" },
  { name: "Chet Holmgren", file: "Chet_Holmgren_data.json", team: "OKC Thunder" },
  { name: "Darius Garland", file: "Darius_Garland_data.json", team: "CLE Cavaliers" },
  { name: "Jamal Murray", file: "Jamal_Murray_data.json", team: "DEN Nuggets" },
  { name: "James Harden", file: "James_Harden_data.json", team: "LAC Clippers" },
  { name: "Domantas Sabonis", file: "Domantas_Sabonis_data.json", team: "SAC Kings" },
  { name: "Bam Adebayo", file: "Bam_Adebayo_data.json", team: "MIA Heat" },
  { name: "Trae Young", file: "Trae_Young_data.json", team: "ATL Hawks" },
  { name: "Ja Morant", file: "Ja_Morant_data.json", team: "MEM Grizzlies" },
  { name: "Ivica Zubac", file: "Ivica_Zubac_data.json", team: "LAC Clippers" },
  { name: "Alperen Sengun", file: "Alperen_Sengun_data.json", team: "HOU Rockets" },
  { name: "Franz Wagner", file: "Franz_Wagner_data.json", team: "ORL Magic" },
  { name: "Derrick White", file: "Derrick_White_data.json", team: "BOS Celtics" },
  { name: "Tyrese Maxey", file: "Tyrese_Maxey_data.json", team: "PHI 76ers" },
  { name: "OG Anunoby", file: "OG_Anunoby_data.json", team: "NYK Knicks" },
  { name: "Amen Thompson", file: "Amen_Thompson_data.json", team: "HOU Rockets" },
  { name: "Aaron Gordon", file: "Aaron_Gordon_data.json", team: "DEN Nuggets" },
  { name: "Damian Lillard", file: "Damian_Lillard_data.json", team: "MIL Bucks" },
  { name: "Kyrie Irving", file: "Kyrie_Irving_data.json", team: "DAL Mavericks" },
  { name: "Zion Williamson", file: "Zion_Williamson_data.json", team: "NOP Pelicans" },
  { name: "Scottie Barnes", file: "Scottie_Barnes_data.json", team: "TOR Raptors" },
  { name: "Desmond Bane", file: "Desmond_Bane_data.json", team: "MEM Grizzlies" },
  { name: "Jalen Johnson", file: "Jalen_Johnson_data.json", team: "ATL Hawks" },
  { name: "LaMelo Ball", file: "LaMelo_Ball_data.json", team: "CHA Hornets" },
  { name: "Draymond Green", file: "Draymond_Green_data.json", team: "GSW Warriors" }
];

export const loadPlayerData = async (playerName) => {
  const playerInfo = PLAYER_FILES.find(p => p.name === playerName);
  if (!playerInfo) return null;

  try {
    const response = await fetch(`/${playerInfo.file}`);
    const data = await response.json();
    
    return {
      name: playerInfo.name,
      team: playerInfo.team,
      games: data.totalGames,
      ...data.seasonAverages,
      recentGames: data.recentGames || []
    };
  } catch (error) {
    console.error(`Error loading data for ${playerName}:`, error);
    return null;
  }
};

export const getAllPlayerNames = () => PLAYER_FILES.map(p => p.name);

export const getAllPlayerData = async () => {
  const allData = [];
  for (const playerInfo of PLAYER_FILES) {
    const data = await loadPlayerData(playerInfo.name);
    if (data) allData.push(data);
  }
  return allData;
};