import React, { useEffect, useState } from 'react';
import './RiskGauge.css';

function RiskGauge({ score, level }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    // Animate from 0 to score
    const duration = 1500; // 1.5 seconds
    const steps = 60;
    const increment = score / steps;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= score) {
        setAnimatedScore(score);
        clearInterval(timer);
      } else {
        setAnimatedScore(Math.floor(current));
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [score]);

  const getColor = () => {
    if (score <= 30) return '#10b981'; // green
    if (score <= 60) return '#f59e0b'; // yellow
    if (score <= 80) return '#fb923c'; // orange
    return '#ef4444'; // red
  };

  const percentage = (animatedScore / 100) * 100;
  const circumference = 2 * Math.PI * 70; // radius = 70
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="risk-gauge">
      <svg className="gauge-svg" viewBox="0 0 160 160">
        {/* Background circle */}
        <circle
          className="gauge-background"
          cx="80"
          cy="80"
          r="70"
          fill="none"
          stroke="rgba(99, 102, 241, 0.1)"
          strokeWidth="12"
        />
        
        {/* Progress circle */}
        <circle
          className="gauge-progress"
          cx="80"
          cy="80"
          r="70"
          fill="none"
          stroke={getColor()}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          transform="rotate(-90 80 80)"
          style={{
            transition: 'stroke-dashoffset 0.5s ease-out',
            filter: `drop-shadow(0 0 8px ${getColor()})`
          }}
        />
      </svg>
      
      <div className="gauge-content">
        <div className="gauge-score" style={{ color: getColor() }}>
          {animatedScore}
        </div>
        <div className="gauge-label">{level}</div>
      </div>
    </div>
  );
}

export default RiskGauge;
