import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import PlayerCards from './PlayerCards';
import DISLeaderboard from './DISLeaderboard';
import OGILeaderboard from './OGILeaderboard';
import NetLeaderboard from './NetLeaderboard';
import PressureLeaderboard from './PressureLeaderboard';
import RimLeaderboard from './RimLeaderboard';
import ContestLeaderboard from './ContestLeaderboard';
import './App.css';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/players" element={<PlayerCards />} />
        <Route path="/defenders" element={<DISLeaderboard />} />
        <Route path="/offense" element={<OGILeaderboard />} />
        <Route path="/impact" element={<NetLeaderboard />} />
        <Route path="/pressure" element={<PressureLeaderboard />} />
        <Route path="/rim" element={<RimLeaderboard />} />
        <Route path="/contest" element={<ContestLeaderboard />} />
      </Routes>
    </div>
  );
}

export default App;
