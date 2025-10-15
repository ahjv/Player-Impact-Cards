import React from 'react';
import Leaderboards from './Leaderboards';

const ContestLeaderboard = () => {
  return (
    <Leaderboards 
      metric="Contest_Rate"
      title="👁️ Contest Machines"
      description="Players with the highest Contest Rate - defenders who aggressively contest shots"
    />
  );
};

export default ContestLeaderboard;