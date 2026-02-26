import React, { useState, useEffect, useCallback } from 'react';
import { fraudAPI } from '../services/api';
import { useToast } from '../context/ToastContext';
import TopBar from '../components/TopBar';
import AnimatedCounter from '../components/AnimatedCounter';
import './AdminPanel.css';

function AdminPanel() {
  const [stats, setStats] = useState({
    totalScans: 0,
    highRiskCount: 0,
    criticalAlerts: 0,
    apiStatus: 'Connected'
  });
  const [activities, setActivities] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [apiKey, setApiKey] = useState('public123');
  const [loading, setLoading] = useState(true);
  const [auditLogs, setAuditLogs] = useState([]);
  const { showToast } = useToast();

  const loadData = useCallback(async () => {
    try {
      const [summaryRes, historyRes] = await Promise.all([
        fraudAPI.getSummary(),
        fraudAPI.getHistory()
      ]);

      const summary = summaryRes.data;
      setStats({
        totalScans: summary.total_analyses || 0,
        highRiskCount: (summary.high_risk_count || 0) + (summary.critical_risk_count || 0),
        criticalAlerts: summary.critical_risk_count || 0,
        apiStatus: 'Connected'
      });

      setActivities(historyRes.data || []);
    } catch (err) {
      console.error('Error loading admin data:', err);
      setStats(prev => ({ ...prev, apiStatus: 'Disconnected' }));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    
    // Load audit logs from sessionStorage
    const logs = JSON.parse(sessionStorage.getItem('auditLogs') || '[]');
    setAuditLogs(logs);
  }, [loadData]);

  const handleRegenerateKey = () => {
    const newKey = 'public' + Math.random().toString(36).substring(2, 9);
    setApiKey(newKey);
    showToast('API Key regenerated successfully!', 'success');
  };

  const maskPhone = (phone) => {
    if (!phone || phone.length < 4) return phone;
    return '***' + phone.slice(-4);
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

  const filteredActivities = activities.filter(activity => {
    const matchesSearch = searchTerm === '' || 
      activity.phone_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      activity.message_content?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterRisk === 'all' || 
      activity.risk_level?.toLowerCase() === filterRisk.toLowerCase();
    
    return matchesSearch && matchesFilter;
  });

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="admin-panel">
      <TopBar title="Admin Panel" subtitle="System control and monitoring" />

      {/* System Stats */}
      <div className="admin-stats-grid">
        <div className="admin-stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-label">Total Scans</div>
            <div className="stat-value">
              {loading ? '...' : <AnimatedCounter end={stats.totalScans} />}
            </div>
          </div>
        </div>

        <div className="admin-stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <div className="stat-label">High Risk Count</div>
            <div className="stat-value">
              {loading ? '...' : <AnimatedCounter end={stats.highRiskCount} />}
            </div>
          </div>
        </div>

        <div className="admin-stat-card">
          <div className="stat-icon">🚨</div>
          <div className="stat-content">
            <div className="stat-label">Critical Alerts</div>
            <div className="stat-value">
              {loading ? '...' : <AnimatedCounter end={stats.criticalAlerts} />}
            </div>
          </div>
        </div>

        <div className="admin-stat-card">
          <div className="stat-icon">🔌</div>
          <div className="stat-content">
            <div className="stat-label">API Status</div>
            <div className={`stat-status ${stats.apiStatus === 'Connected' ? 'connected' : 'disconnected'}`}>
              {stats.apiStatus}
            </div>
          </div>
        </div>
      </div>

      {/* API Key Management */}
      <div className="admin-section">
        <h3 className="section-title">API Key Management</h3>
        <div className="api-key-card">
          <div className="api-key-display">
            <label>Current API Key</label>
            <div className="api-key-value">
              {apiKey.substring(0, 6)}{'*'.repeat(10)}
            </div>
          </div>
          <button className="regenerate-button" onClick={handleRegenerateKey}>
            <span className="button-icon">🔄</span>
            Regenerate Key
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="admin-section">
        <h3 className="section-title">Recent Activity</h3>
        
        <div className="activity-controls">
          <input
            type="text"
            className="search-input"
            placeholder="Search by phone or message..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          
          <select 
            className="filter-select"
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
          >
            <option value="all">All Risk Levels</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </div>

        <div className="activity-table-container">
          <table className="activity-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Phone Number</th>
                <th>Risk Level</th>
                <th>Risk Score</th>
                <th>Threat Category</th>
              </tr>
            </thead>
            <tbody>
              {filteredActivities.length === 0 ? (
                <tr>
                  <td colSpan="5" className="no-data">
                    {loading ? 'Loading...' : 'No activity found'}
                  </td>
                </tr>
              ) : (
                filteredActivities.map((activity, index) => (
                  <tr key={index}>
                    <td>{formatTimestamp(activity.timestamp)}</td>
                    <td className="phone-cell">{maskPhone(activity.phone_number)}</td>
                    <td>
                      <span 
                        className="risk-badge-small"
                        style={{ 
                          background: `${getRiskColor(activity.risk_level)}20`,
                          color: getRiskColor(activity.risk_level),
                          borderColor: getRiskColor(activity.risk_level)
                        }}
                      >
                        {activity.risk_level}
                      </span>
                    </td>
                    <td className="score-cell">{activity.risk_score}</td>
                    <td>{activity.threat_category || 'N/A'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Audit Log */}
      <div className="admin-section">
        <h3 className="section-title">Audit Log</h3>
        <div className="audit-log-container">
          {auditLogs.length === 0 ? (
            <div className="no-data">No audit logs available</div>
          ) : (
            <table className="audit-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Action</th>
                  <th>Role</th>
                  <th>Details</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.slice().reverse().map((log, index) => (
                  <tr key={index}>
                    <td>{formatTimestamp(log.timestamp)}</td>
                    <td>
                      <span className="action-badge">{log.action}</span>
                    </td>
                    <td>
                      <span className={`role-badge role-${log.role}`}>{log.role}</span>
                    </td>
                    <td className="details-cell">{log.details || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminPanel;
