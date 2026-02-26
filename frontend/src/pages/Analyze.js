import React, { useState } from 'react';
import { fraudAPI } from '../services/api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import TopBar from '../components/TopBar';
import LoadingOverlay from '../components/LoadingOverlay';
import ExplainableAIPanel from '../components/ExplainableAIPanel';
import './Analyze.css';

function Analyze() {
  const [formData, setFormData] = useState({
    phone_number: '',
    message_content: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();
  const { addAuditLog } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fraudAPI.analyze(formData);
      setResult(response.data);
      showToast('Analysis completed successfully!', 'success');
      
      // Log the analyze action
      addAuditLog(
        'ANALYZE',
        `Analyzed ${formData.phone_number || 'message'} - Risk: ${response.data.risk_level}`
      );
    } catch (err) {
      console.error('Error analyzing message:', err);
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          'Failed to analyze message. Please check your connection and try again.';
      showToast(errorMessage, 'error');
      
      // Log the failed attempt
      addAuditLog('ANALYZE_FAILED', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
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

  return (
    <div className="analyze-page">
      {loading && <LoadingOverlay message="Analyzing message..." />}
      
      <TopBar title="Analyze Message" subtitle="Check phone numbers and messages for fraud indicators" />

      <div className="analyze-container">
        <div className="analyze-form-section">
          <form onSubmit={handleSubmit} className="analyze-form">
            <div className="form-group">
              <label className="form-label">
                <span className="label-icon">📱</span>
                Phone Number
              </label>
              <input
                type="text"
                name="phone_number"
                className="form-input"
                placeholder="+1234567890"
                value={formData.phone_number}
                onChange={handleChange}
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                <span className="label-icon">💬</span>
                Message Content
              </label>
              <textarea
                name="message_content"
                className="form-textarea"
                placeholder="Enter the message to analyze..."
                rows="8"
                value={formData.message_content}
                onChange={handleChange}
                disabled={loading}
              />
            </div>

            <button 
              type="submit" 
              className="submit-button"
              disabled={loading || (!formData.phone_number && !formData.message_content)}
            >
              {loading ? (
                <>
                  <span className="button-spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>
                  <span className="button-icon">🔍</span>
                  Analyze Message
                </>
              )}
            </button>
          </form>
        </div>

        <div className="analyze-result-section">
          {result && <ExplainableAIPanel result={result} />}

          {!result && !loading && (
            <div className="result-placeholder">
              <span className="placeholder-icon">📊</span>
              <h3>No Analysis Yet</h3>
              <p>Enter a phone number or message and click Analyze to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Analyze;
