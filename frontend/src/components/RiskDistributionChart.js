import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import './RiskDistributionChart.css';

function RiskDistributionChart({ distribution, loading }) {
  if (loading) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Risk Distribution</h3>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  const data = [
    { name: 'Low', value: distribution.low || 0, color: '#10b981' },
    { name: 'Medium', value: distribution.medium || 0, color: '#f59e0b' },
    { name: 'High', value: distribution.high || 0, color: '#ef4444' },
    { name: 'Critical', value: distribution.critical || 0, color: '#dc2626' }
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{payload[0].payload.name}</p>
          <p className="tooltip-value">{payload[0].value} scans</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-card">
      <h3 className="chart-title">Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2f4a" />
          <XAxis dataKey="name" stroke="#a0a0b0" />
          <YAxis stroke="#a0a0b0" />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }} />
          <Bar 
            dataKey="value" 
            radius={[8, 8, 0, 0]}
            animationBegin={0}
            animationDuration={800}
            animationEasing="ease-out"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RiskDistributionChart;
