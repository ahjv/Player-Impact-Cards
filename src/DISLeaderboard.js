import React from 'react';
import Leaderboards from './Leaderboards';

const DISLeaderboard = () => {
  return (
    <Leaderboards 
      metric="DIS"
      title="🛡️ Best Defenders (DIS)"
      description="Players with the highest Defensive Impact Score - elite defenders who disrupt opposing offenses"
    />
  );
};

export default DISLeaderboard;