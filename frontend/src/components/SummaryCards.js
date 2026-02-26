import React from 'react';
import AnimatedCounter from './AnimatedCounter';
import './SummaryCards.css';

function SummaryCards({ summary, loading }) {
  if (loading) {
    return (
      <div className="summary-cards">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="summary-card loading">
            <div className="loading-shimmer"></div>
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'Total Scans',
      value: summary.total_scans || 0,
      icon: '📊',
      color: '#6366f1'
    },
    {
      title: 'High Risk',
      value: summary.high_risk || 0,
      icon: '⚠️',
      color: '#ef4444'
    },
    {
      title: 'Medium Risk',
      value: summary.medium_risk || 0,
      icon: '⚡',
      color: '#f59e0b'
    },
    {
      title: 'Low Risk',
      value: summary.low_risk || 0,
      icon: '✅',
      color: '#10b981'
    }
  ];

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div key={index} className="summary-card" style={{ borderTopColor: card.color }}>
          <div className="card-icon" style={{ background: `${card.color}20` }}>
            <span>{card.icon}</span>
          </div>
          <div className="card-content">
            <div className="card-title">{card.title}</div>
            <div className="card-value">
              <AnimatedCounter value={card.value} duration={1000} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;
