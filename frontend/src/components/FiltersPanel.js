import React from 'react';
import './FiltersPanel.css';

function FiltersPanel({ filters, onFilterChange }) {
  return (
    <div className="filters-panel">
      <h3 className="filters-title">Filters</h3>
      
      <div className="filter-group">
        <label className="filter-label">Risk Level</label>
        <select 
          className="filter-select"
          value={filters.riskLevel}
          onChange={(e) => onFilterChange({ ...filters, riskLevel: e.target.value })}
        >
          <option value="all">All Levels</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Time Period</label>
        <select 
          className="filter-select"
          value={filters.days}
          onChange={(e) => onFilterChange({ ...filters, days: parseInt(e.target.value) })}
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
        </select>
      </div>

      <button 
        className="filter-reset"
        onClick={() => onFilterChange({ riskLevel: 'all', days: 30 })}
      >
        Reset Filters
      </button>
    </div>
  );
}

export default FiltersPanel;
