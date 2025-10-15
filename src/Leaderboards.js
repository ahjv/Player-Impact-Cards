import React, { useState, useEffect } from 'react';
import { getAllPlayerData } from './PlayerData';
import './Leaderboards.css';

const Leaderboards = ({ metric, title, description }) => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const allPlayers = await getAllPlayerData();

      console.log("Sample player keys:", Object.keys(allPlayers[0] || {}));
      console.log("Trying to filter for metric:", metric);

      const sortedPlayers = allPlayers
        .filter(player =>
          player[metric] !== undefined &&
          player[metric] !== null &&
          typeof player[metric] === 'number' &&
          !isNaN(player[metric])
        )
        .sort((a, b) => b[metric] - a[metric])
        .slice(0, 10);

      console.log("Filtered players:", sortedPlayers);
      setPlayers(sortedPlayers);
      setLoading(false);
    };

    loadData();
  }, [metric]);

  if (loading) {
    return (
      <div className="leaderboard-container">
        <h1>{title}</h1>
        <div className="loading">Loading leaderboard...</div>
      </div>
    );
  }

  return (
    <div className="leaderboard-container">
      <h1>{title}</h1>
      <p className="leaderboard-description">{description}</p>

      <div className="leaderboard-grid">
        {players.map((player, index) => (
          <div key={player.name} className={`leaderboard-card rank-${index + 1}`}>
            <div className="rank-badge">#{index + 1}</div>
            <div className="player-info">
              <h3>{player.name}</h3>
              <p className="team">{player.team}</p>
              <div className="metric-value">
                {metric}: <span className="value">{player[metric]}</span>
              </div>
              <div className="games-info">{player.games} games</div>
            </div>
          </div>
        ))}
      </div>

      <div className="back-to-home">
        <button onClick={() => window.location.href = '/'}>
          ← Back to Home
        </button>
      </div>
    </div>
  );
};

export default Leaderboards;
