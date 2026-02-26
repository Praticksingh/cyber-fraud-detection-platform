import React from 'react';
import './RecentActivityTable.css';

function RecentActivityTable({ activities, loading }) {
  const maskPhoneNumber = (phone) => {
    if (!phone || phone.length < 4) return phone;
    const lastFour = phone.slice(-4);
    const masked = '*'.repeat(Math.max(phone.length - 4, 0));
    return masked + lastFour;
  };

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'low': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'high': return '#ef4444';
      case 'critical': return '#dc2626';
      default: return '#6366f1';
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Recent Activity</h3>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (!activities || activities.length === 0) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Recent Activity</h3>
        <div className="empty-state">
          <span className="empty-icon">📋</span>
          <p>No recent activity</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-card">
      <h3 className="chart-title">Recent Activity</h3>
      <div className="table-container">
        <table className="activity-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Phone Number</th>
              <th>Risk Level</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity, index) => (
              <tr key={index} className="table-row">
                <td className="time-cell">{formatTime(activity.timestamp)}</td>
                <td className="phone-cell">{maskPhoneNumber(activity.phone_number)}</td>
                <td>
                  <span 
                    className="risk-badge"
                    style={{
                      background: `${getRiskColor(activity.risk_level)}20`,
                      color: getRiskColor(activity.risk_level),
                      borderColor: getRiskColor(activity.risk_level)
                    }}
                  >
                    {activity.risk_level}
                  </span>
                </td>
                <td className="score-cell">
                  <span 
                    className="score-value"
                    style={{ color: getRiskColor(activity.risk_level) }}
                  >
                    {activity.risk_score}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RecentActivityTable;
