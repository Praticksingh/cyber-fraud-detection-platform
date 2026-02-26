import React from 'react';
import './TopBar.css';

function TopBar({ title, subtitle }) {
  return (
    <div className="topbar">
      <div className="topbar-content">
        <div className="topbar-title-section">
          <h1 className="topbar-title">{title}</h1>
          {subtitle && <p className="topbar-subtitle">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
}

export default TopBar;
