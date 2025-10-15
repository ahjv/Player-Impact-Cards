import React, { useState, useEffect } from 'react';
import { loadPlayerData, getAllPlayerNames } from './PlayerData';
import { generatePlayerSummary } from './AIAnalysis';
import PlayerRadarChart from './RadarChart';
import { Link } from 'react-router-dom';
import './PlayerCards.css';

function PlayerCard({ player }) {
  const [isFlipped, setIsFlipped] = useState(false);

  if (!player) {
    return (
      <div className="card-container">
        <div className="card loading-card">
          <div className="card-front">
            <h2>Loading...</h2>
          </div>
        </div>
      </div>
    );
  }

  // Generate AI summary directly
  const aiSummary = generatePlayerSummary(player);

  return (
    <div className="card-container" onClick={() => setIsFlipped(!isFlipped)}>
      <div className={`card ${isFlipped ? 'flipped' : ''}`}>
        <div className="card-front">
          <h2>{player.name}</h2>
          <p className="team">{player.team}</p>
          <p className="games-played">{player.games} games played</p>
          
          <div className="metrics-section">
            <PlayerRadarChart player={player} />
            
            <div className="metrics-summary">
              <div className="metric-row">
                <span>DIS: {player.DIS}</span>
                <span>OGI: {player.OGI}</span>
              </div>
              <div className="metric-row">
                <span>Contest: {player.Contest_Rate}</span>
                <span>Rim: {player.Rim_Deterrence}</span>
              </div>
              <div className="metric-row">
                <span>TO Press: {player.TO_Pressure}</span>
                <span>Net: {player.OnOff_Net}</span>
              </div>
            </div>
          </div>

          <div className="ai-summary">
            <h4>🧠 AI Scouting Report:</h4>
            <p className="summary-text">{aiSummary}</p>
          </div>
          
          <p className="flip-hint">Click to flip →</p>
        </div>

        <div className="card-back">
          <h3>Last 5 Games</h3>
          <div className="games-list">
            {player.recentGames && player.recentGames.map((game, index) => (
              <div key={index} className="game-row">
                <span className="game-date">{game.date}</span>
                <span className="game-opponent">{game.opponent}</span>
                <span className="game-stat">DIS: {game.DIS}</span>
                <span className="game-stat">OGI: {game.OGI}</span>
              </div>
            ))}
          </div>
          <p className="flip-hint">← Click to flip back</p>
        </div>
      </div>
    </div>
  );
}

function PlayerCards() {
  const [selectedPlayer, setSelectedPlayer] = useState("Shai Gilgeous-Alexander");
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(true);

  const playerNames = getAllPlayerNames();

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const data = await loadPlayerData(selectedPlayer);
      setPlayerData(data);
      setLoading(false);
    };

    loadData();
  }, [selectedPlayer]);

  return (
    <div className="player-cards-page">
      <div className="header">
        <Link to="/" className="back-button">← Back to Home</Link>
        <h1>🏀 Player Impact Cards</h1>
      </div>
      
      <div className="player-selector">
        <label htmlFor="player-select">Choose Player:</label>
        <select 
          id="player-select"
          value={selectedPlayer} 
          onChange={(e) => setSelectedPlayer(e.target.value)}
        >
          {playerNames.map(name => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="loading">Loading player data...</div>
      ) : (
        <PlayerCard player={playerData} />
      )}
    </div>
  );
}

export default PlayerCards;