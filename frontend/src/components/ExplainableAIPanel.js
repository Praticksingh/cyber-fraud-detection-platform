import React, { useState } from 'react';
import './ExplainableAIPanel.css';

function ExplainableAIPanel({ result }) {
  const [showTechnical, setShowTechnical] = useState(false);

  if (!result) return null;

  const getRiskColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'low': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'high': return '#ef4444';
      case 'critical': return '#dc2626';
      default: return '#6366f1';
    }
  };

  const highlightSuspiciousWords = (text, factors) => {
    if (!text || !factors) return text;
    
    // Extract suspicious keywords from factors
    const suspiciousWords = factors
      .filter(f => f.toLowerCase().includes('keyword') || f.toLowerCase().includes('pattern'))
      .flatMap(f => {
        const match = f.match(/'([^']+)'/g);
        return match ? match.map(m => m.replace(/'/g, '')) : [];
      });

    if (suspiciousWords.length === 0) return text;

    let highlightedText = text;
    suspiciousWords.forEach(word => {
      const regex = new RegExp(`(${word})`, 'gi');
      highlightedText = highlightedText.replace(
        regex,
        '<span class="suspicious-word">$1</span>'
      );
    });

    return highlightedText;
  };

  return (
    <div className="xai-panel">
      <div className="xai-header">
        <h3>Analysis Results</h3>
        <span className="xai-timestamp">
          {new Date().toLocaleString()}
        </span>
      </div>

      <div className="xai-main-results">
        <div className="xai-score-card">
          <div className="score-label">Risk Score</div>
          <div 
            className="score-value" 
            style={{ color: getRiskColor(result.risk_level) }}
          >
            {result.risk_score}
            <span className="score-max">/100</span>
          </div>
        </div>

        <div className="xai-metrics">
          <div className="metric-item">
            <span className="metric-label">Risk Level</span>
            <span 
              className={`metric-badge risk-${result.risk_level?.toLowerCase()}`}
              style={{ 
                background: `${getRiskColor(result.risk_level)}20`,
                color: getRiskColor(result.risk_level),
                border: `1px solid ${getRiskColor(result.risk_level)}40`
              }}
            >
              {result.risk_level}
            </span>
          </div>

          <div className="metric-item">
            <span className="metric-label">Confidence</span>
            <span className="metric-value">{result.confidence}%</span>
          </div>

          <div className="metric-item">
            <span className="metric-label">Threat Category</span>
            <span className="metric-value">{result.threat_category || 'Unknown'}</span>
          </div>
        </div>
      </div>

      <div className="xai-section">
        <h4 className="section-title">
          <span className="section-icon">🔍</span>
          Why was this flagged?
        </h4>
        <div className="xai-reason">
          <p className="primary-reason">{result.primary_reason}</p>
        </div>
      </div>

      {result.contributing_factors && result.contributing_factors.length > 0 && (
        <div className="xai-section">
          <h4 className="section-title">
            <span className="section-icon">⚠️</span>
            Contributing Factors
          </h4>
          <ul className="factors-list">
            {result.contributing_factors.map((factor, index) => (
              <li key={index} className="factor-item">
                <span className="factor-bullet">•</span>
                {factor}
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.recommendation && (
        <div className="xai-section recommendation-section">
          <h4 className="section-title">
            <span className="section-icon">💡</span>
            Recommendation
          </h4>
          <p className="recommendation-text">{result.recommendation}</p>
        </div>
      )}

      <div className="xai-section">
        <button 
          className="technical-toggle"
          onClick={() => setShowTechnical(!showTechnical)}
        >
          <span className="toggle-icon">{showTechnical ? '▼' : '▶'}</span>
          Technical Details
        </button>
        
        {showTechnical && (
          <div className="technical-details">
            <div className="detail-row">
              <span className="detail-label">Model Version:</span>
              <span className="detail-value">v2.0.0</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Analysis Timestamp:</span>
              <span className="detail-value">{new Date().toISOString()}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Detection Engine:</span>
              <span className="detail-value">Rule-based + ML Hybrid</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Confidence Score:</span>
              <span className="detail-value">{result.confidence}%</span>
            </div>
            {result.explanation && (
              <div className="detail-row">
                <span className="detail-label">Explanation:</span>
                <span className="detail-value">{result.explanation}</span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ExplainableAIPanel;
