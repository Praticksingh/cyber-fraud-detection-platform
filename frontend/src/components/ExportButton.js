import React, { useState } from 'react';
import { exportToCSV, exportToJSON, exportToPDF } from '../utils/export';
import { useToast } from '../context/ToastContext';
import './ExportButton.css';

function ExportButton({ data, filename = 'export', formatData, title = 'Report' }) {
  const [showMenu, setShowMenu] = useState(false);
  const { showToast } = useToast();

  const handleExport = (format) => {
    try {
      if (!data || data.length === 0) {
        showToast('No data to export', 'error');
        return;
      }

      const formattedData = formatData ? formatData(data) : data;
      const timestamp = new Date().toISOString().split('T')[0];
      const fullFilename = `${filename}_${timestamp}`;

      switch (format) {
        case 'csv':
          exportToCSV(formattedData, `${fullFilename}.csv`);
          showToast('Exported as CSV successfully', 'success');
          break;
        case 'json':
          exportToJSON(formattedData, `${fullFilename}.json`);
          showToast('Exported as JSON successfully', 'success');
          break;
        case 'pdf':
          exportToPDF(formattedData, `${fullFilename}.pdf`, title);
          showToast('Exported as PDF successfully', 'success');
          break;
        default:
          showToast('Invalid export format', 'error');
      }

      setShowMenu(false);
    } catch (error) {
      console.error('Export error:', error);
      showToast('Failed to export data', 'error');
    }
  };

  return (
    <div className="export-button-container">
      <button 
        className="export-button"
        onClick={() => setShowMenu(!showMenu)}
      >
        <span className="button-icon">📥</span>
        Export Report
        <span className="dropdown-arrow">{showMenu ? '▲' : '▼'}</span>
      </button>

      {showMenu && (
        <>
          <div 
            className="export-backdrop" 
            onClick={() => setShowMenu(false)}
          />
          <div className="export-menu">
            <button 
              className="export-option"
              onClick={() => handleExport('csv')}
            >
              <span className="option-icon">📊</span>
              <div className="option-content">
                <div className="option-title">Export as CSV</div>
                <div className="option-desc">Spreadsheet format</div>
              </div>
            </button>

            <button 
              className="export-option"
              onClick={() => handleExport('json')}
            >
              <span className="option-icon">📄</span>
              <div className="option-content">
                <div className="option-title">Export as JSON</div>
                <div className="option-desc">Structured data format</div>
              </div>
            </button>

            <button 
              className="export-option"
              onClick={() => handleExport('pdf')}
            >
              <span className="option-icon">📑</span>
              <div className="option-content">
                <div className="option-title">Export as PDF</div>
                <div className="option-desc">Document format</div>
              </div>
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ExportButton;
