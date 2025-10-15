import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const leaderboards = [
    {
      title: "Best Defenders",
      icon: "🛡️",
      description: "Elite defenders who disrupt opposing offenses",
      path: "/defenders",
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    {
      title: "Offensive Engines", 
      icon: "⚡",
      description: "Creators who command defensive attention",
      path: "/offense",
      gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    },
    {
      title: "Rim Protectors",
      icon: "🏀", 
      description: "Elite shot blockers who protect the paint",
      path: "/rim",
      gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    },
    {
      title: "Contest Machines",
      icon: "👁️",
      description: "Defenders who aggressively contest shots", 
      path: "/contest",
      gradient: "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
    },
    {
      title: "Turnover Pressure",
      icon: "🖐️", 
      description: "Disruptors who force turnovers",
      path: "/pressure",
      gradient: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
    },
    {
      title: "Net Impact",
      icon: "📊",
      description: "Players who most improve team performance",
      path: "/impact", 
      gradient: "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
    }
  ];

  return (
    <div className="home-container">
      <div className="hero-section">
        <h1 className="hero-title">
          🏀 NBA Player Impact Analytics
        </h1>
        <p className="hero-subtitle">
          Advanced metrics and AI-powered analysis for the top 50 NBA players
        </p>
        <div className="hero-stats">
          <div className="stat-item">
            <span className="stat-number">50</span>
            <span className="stat-label">Elite Players</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">6</span>
            <span className="stat-label">Metric Categories</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">AI</span>
            <span className="stat-label">Powered Analysis</span>
          </div>
        </div>
      </div>

      <div className="leaderboards-grid">
        {leaderboards.map((board, index) => (
          <Link 
            key={board.path} 
            to={board.path} 
            className="leaderboard-card"
            style={{ background: board.gradient }}
          >
            <div className="card-icon">{board.icon}</div>
            <h3 className="card-title">{board.title}</h3>
            <p className="card-description">{board.description}</p>
            <div className="card-arrow">→</div>
          </Link>
        ))}
      </div>

      <div className="player-cards-section">
        <h2>Individual Player Analysis</h2>
        <p>Explore detailed impact cards with AI scouting reports</p>
        <Link to="/players" className="players-button">
          View Player Cards
        </Link>
      </div>

      <footer className="home-footer">
        <p>Advanced NBA Analytics Platform • Built with React & AI</p>
      </footer>
    </div>
  );
};

export default HomePage;