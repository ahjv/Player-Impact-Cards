import React from 'react';
import Leaderboards from './Leaderboards';

const PressureLeaderboard = () => {
  return (
    <Leaderboards 
      metric="TO_Pressure"
      title="🖐️ Turnover Pressure Leaders"
      description="Players with the highest Turnover Pressure - disruptors who force turnovers with active hands"
    />
  );
};

export default PressureLeaderboard;