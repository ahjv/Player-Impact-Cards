import React from 'react';
import Leaderboards from './Leaderboards';

const OGILeaderboard = () => {
  return (
    <Leaderboards 
      metric="OGI"
      title="⚡ Offensive Engines (OGI)"
      description="Players with the highest Offensive Gravity Index - creators who command defensive attention"
    />
  );
};

export default OGILeaderboard;