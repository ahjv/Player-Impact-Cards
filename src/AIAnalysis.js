export const generatePlayerSummary = (player) => {
  if (!player || !player.recentGames) return "Loading player analysis...";
  
  const { DIS, OGI, Contest_Rate, Rim_Deterrence, TO_Pressure, OnOff_Net, name } = player;
  
  // Calculate average PPG from recent games
  const avgPPG = player.recentGames.reduce((sum, game) => sum + parseInt(game.points || 0), 0) / player.recentGames.length;
  
  // FIXED scoring tiers for 2024-25 NBA season
  const scoring = {
    superstar: avgPPG >= 28,          // Luka, Shai, Giannis level
    allStar: avgPPG >= 22,            // Clear all-stars
    primaryScorer: avgPPG >= 18,      // FIXED: Paolo level (26 PPG)
    solidScorer: avgPPG >= 14,        // Good scorers
    role: avgPPG >= 8,                // Role players
    limited: avgPPG < 8               // Bench players
  };
  
  const offense = {
    elite: OGI > 50,                  // Elite offensive players
    good: OGI > 35,                   // Good offensive players  
    solid: OGI > 25,                  // Solid contributors
    limited: OGI <= 25                // Limited offense
  };
  
  const defense = {
    elite: DIS > 25,                  // Elite defenders
    good: DIS > 15,                   // Good defenders
    solid: DIS > 8,                   // Solid defenders
    limited: DIS <= 8                 // Limited defense
  };
  
  // Determine role with FIXED thresholds
  let role = "";
  let description = "";
  
  // Superstars
  if (scoring.superstar && offense.elite) {
    role = "Superstar";
    description = "elite scorer who dominates offensive possessions";
  } else if (scoring.superstar) {
    role = "Elite scorer";
    description = "primary offensive weapon who can take over games";
  }
  
  // All-Stars and Primary Scorers
  else if (scoring.allStar && offense.good) {
    role = "All-Star caliber player";
    description = "high-level scorer with excellent offensive creation";
  } else if (scoring.primaryScorer) {  // FIXED: 18+ PPG = primary scorer
    role = "Primary scoring option";
    description = "go-to offensive player who provides consistent production";
  } else if (scoring.allStar) {
    role = "All-Star contributor";
    description = "reliable scorer who impacts winning";
  }
  
  // Good players
  else if (scoring.solidScorer && offense.good) {
    role = "Versatile scorer";
    description = "reliable offensive threat who creates quality shots";
  } else if (scoring.solidScorer && defense.good) {
    role = "Two-way contributor";
    description = "balanced player who impacts both ends effectively";
  } else if (scoring.solidScorer) {
    role = "Solid contributor";
    description = "consistent scoring option who knows their role";
  }
  
  // Defense-first players
  else if (defense.elite) {
    role = "Defensive specialist";
    description = "elite defender who anchors team defense";
  } else if (defense.good) {
    role = "Defensive contributor";
    description = "active defender who brings energy and effort";
  }
  
  // Role players
  else if (scoring.role) {
    role = "Role player";
    description = "valuable contributor who fills specific team needs";
  } else {
    role = "Bench contributor";
    description = "provides depth and specific skills when called upon";
  }
  
  // Add specific context without revealing numbers
  let context = "";
  if (defense.elite) {
    context = " Elite defensive impact.";
  } else if (defense.good) {
    context = " Solid defensive presence.";
  } else if (offense.elite) {
    context = " Exceptional offensive creation.";
  } else if (offense.good) {
    context = " Strong offensive contributor.";
  }
  
  return `${role} who is a ${description}.${context}`;
};