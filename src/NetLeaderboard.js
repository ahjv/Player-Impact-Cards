import React from 'react';
import Leaderboards from './Leaderboards';

const NetLeaderboard = () => {
  return (
    <Leaderboards 
      metric="OnOff_Net"
      title="📊 Net Impact Leaders"
      description="Players with the highest Net Impact - those who most improve their team's performance"
    />
  );
};

export default NetLeaderboard;
