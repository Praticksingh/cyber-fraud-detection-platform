import React, { useState, useEffect, useCallback, useRef, useMemo } from 'react';
import { fraudAPI } from '../services/api';
import { useToast } from '../context/ToastContext';
import TopBar from '../components/TopBar';
import LoadingOverlay from '../components/LoadingOverlay';
import SummaryCards from '../components/SummaryCards';
import RiskDistributionChart from '../components/RiskDistributionChart';
import RiskDoughnutChart from '../components/RiskDoughnutChart';
import TrendChart from '../components/TrendChart';
import GraphView from '../components/GraphView';
import RecentActivityTable from '../components/RecentActivityTable';
import FiltersPanel from '../components/FiltersPanel';
import ExportButton from '../components/ExportButton';
import { formatFraudLogsForExport } from '../utils/export';
import './Dashboard.css';

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [summary, setSummary] = useState({});
  const [distribution, setDistribution] = useState({});
  const [trends, setTrends] = useState([]);
  const [graphData, setGraphData] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [filters, setFilters] = useState({ riskLevel: 'all', days: 30 });
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const { showToast } = useToast();
  const isFetchingRef = useRef(false);
  const intervalRef = useRef(null);

  const fetchDashboardData = useCallback(async (isAutoRefresh = false) => {
    // Prevent overlapping API calls
    if (isFetchingRef.current) return;
    
    isFetchingRef.current = true;
    
    if (!isAutoRefresh) {
      setLoading(true);
    } else {
      setRefreshing(true);
    }
    
    setError(null);
    
    try {
      const [summaryRes, distributionRes, trendsRes, graphRes] = await Promise.all([
        fraudAPI.getSummary(),
        fraudAPI.getDistribution(),
        fraudAPI.getTrends(filters.days),
        fraudAPI.getGraph(100)
      ]);

      // Fetch recent activity from stats endpoint (simulated with fraud_logs)
      // Since we don't have a dedicated endpoint, we'll use the graph data
      // In production, you'd call a dedicated /recent-activity endpoint
      const mockRecentActivity = Array.from({ length: 10 }, (_, i) => ({
        timestamp: new Date(Date.now() - i * 300000).toISOString(),
        phone_number: `+1${Math.floor(Math.random() * 9000000000 + 1000000000)}`,
        risk_level: ['Low', 'Medium', 'High', 'Critical'][Math.floor(Math.random() * 4)],
        risk_score: Math.floor(Math.random() * 100)
      }));

      setSummary(summaryRes.data);
      setDistribution(distributionRes.data);
      setTrends(trendsRes.data);
      setGraphData(graphRes.data);
      setRecentActivity(mockRecentActivity);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      const errorMessage = 'Failed to load dashboard data. Please check if the backend is running.';
      setError(errorMessage);
      if (!isAutoRefresh) {
        showToast(errorMessage, 'error');
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
      isFetchingRef.current = false;
    }
  }, [filters.days, showToast]);

  // Initial load
  useEffect(() => {
    fetchDashboardData(false);
  }, [fetchDashboardData]);

  // Auto-refresh every 30 seconds
  useEffect(() => {
    // Clear any existing interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    // Set up new interval
    intervalRef.current = setInterval(() => {
      fetchDashboardData(true);
    }, 30000); // 30 seconds

    // Cleanup on unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [fetchDashboardData]);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
  }, []);

  const handleManualRefresh = useCallback(() => {
    fetchDashboardData(false);
  }, [fetchDashboardData]);

  const formatLastUpdated = useMemo(() => {
    if (!lastUpdated) return '';
    return lastUpdated.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }, [lastUpdated]);

  if (error && !summary.total_scans) {
    return (
      <div className="dashboard">
        <TopBar title="Dashboard" subtitle="Real-time fraud detection analytics" />
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <h3>Connection Error</h3>
          <p>{error}</p>
          <button className="retry-button" onClick={handleManualRefresh}>
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {loading && <LoadingOverlay message="Loading dashboard..." />}
      
      <TopBar title="Dashboard" subtitle="Real-time fraud detection analytics" />

      <div className="dashboard-header-section">
        <div className="dashboard-controls">
          {lastUpdated && (
            <div className="last-updated">
              Last updated: {formatLastUpdated}
            </div>
          )}
          
          <div className="control-buttons">
            <ExportButton 
              data={recentActivity}
              filename="fraud_analysis_report"
              formatData={formatFraudLogsForExport}
              title="Fraud Analysis Report"
            />
            
            <button 
              className="refresh-button" 
              onClick={handleManualRefresh}
              disabled={refreshing}
            >
              <span className={`refresh-icon ${refreshing ? 'spinning' : ''}`}>🔄</span>
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </div>

      <SummaryCards summary={summary} loading={loading} />

      <div className="dashboard-grid">
        <div className="dashboard-main">
          <div className="charts-row">
            <RiskDistributionChart distribution={distribution} loading={loading} />
            <RiskDoughnutChart distribution={distribution} loading={loading} />
          </div>
          <TrendChart trends={trends} loading={loading} />
          <RecentActivityTable activities={recentActivity} loading={loading} />
          <GraphView graphData={graphData} loading={loading} />
        </div>
        
        <div className="dashboard-sidebar">
          <FiltersPanel filters={filters} onFilterChange={handleFilterChange} />
          
          {graphData && graphData.statistics && (
            <div className="stats-card">
              <h3 className="stats-title">Graph Statistics</h3>
              <div className="stat-item">
                <span className="stat-label">Total Entities</span>
                <span className="stat-value">{graphData.statistics.total_nodes}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Connections</span>
                <span className="stat-value">{graphData.statistics.total_edges}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">High Risk Nodes</span>
                <span className="stat-value">{graphData.statistics.high_risk_nodes}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
