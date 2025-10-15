import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

const PlayerRadarChart = ({ player }) => {
  if (!player) return null;

  const data = [
    { metric: 'DIS', value: Math.min(player.DIS, 25), fullMark: 25 },
    { metric: 'OGI', value: Math.min(player.OGI, 40), fullMark: 40 },
    { metric: 'Contest', value: Math.min(player.Contest_Rate, 20), fullMark: 20 },
    { metric: 'Rim', value: Math.min(player.Rim_Deterrence, 30), fullMark: 30 },
    { metric: 'TO Press', value: Math.min(player.TO_Pressure, 15), fullMark: 15 },
    { metric: 'Net', value: Math.min(player.OnOff_Net + 10, 20), fullMark: 20 }
  ];

  return (
    <div className="radar-container">
      <ResponsiveContainer width="100%" height={200}>
        <RadarChart data={data}>
          <PolarGrid stroke="#ffffff40" />
          <PolarAngleAxis 
            dataKey="metric" 
            tick={{ fontSize: 10, fill: 'white' }}
          />
          <PolarRadiusAxis 
            tick={false}
            domain={[0, 'dataMax']}
          />
          <Radar
            name="Player"
            dataKey="value"
            stroke="#00ff88"
            fill="#00ff8840"
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlayerRadarChart;