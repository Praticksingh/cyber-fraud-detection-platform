import React, { useState, useEffect } from 'react';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import TopBar from '../components/TopBar';
import LoadingOverlay from '../components/LoadingOverlay';
import api from '../services/api';
import './BlacklistManagement.css';

function BlacklistManagement() {
  const [blacklist, setBlacklist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [newEntry, setNewEntry] = useState({ phone_number: '', reason: '' });
  const [submitting, setSubmitting] = useState(false);
  const { showToast } = useToast();
  const { addAuditLog } = useAuth();

  useEffect(() => {
    fetchBlacklist();
  }, []);

  const fetchBlacklist = async () => {
    setLoading(true);
    try {
      const response = await api.get('/blacklist');
      setBlacklist(response.data.blacklist || []);
    } catch (err) {
      console.error('Error fetching blacklist:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to load blacklist';
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAddBlacklist = async (e) => {
    e.preventDefault();
    
    if (!newEntry.phone_number || !newEntry.reason) {
      showToast('Please fill in all fields', 'error');
      return;
    }

    setSubmitting(true);
    try {
      await api.post('/blacklist', newEntry);
      showToast('Phone number added to blacklist', 'success');
      addAuditLog('BLACKLIST_ADD', `Added ${newEntry.phone_number} to blacklist`);
      setNewEntry({ phone_number: '', reason: '' });
      setShowAddModal(false);
      fetchBlacklist();
    } catch (err) {
      console.error('Error adding to blacklist:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to add to blacklist';
      showToast(errorMessage, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemoveBlacklist = async (id, phoneNumber) => {
    if (!window.confirm(`Remove ${phoneNumber} from blacklist?`)) {
      return;
    }

    try {
      await api.delete(`/blacklist/${id}`);
      showToast('Phone number removed from blacklist', 'success');
      addAuditLog('BLACKLIST_REMOVE', `Removed ${phoneNumber} from blacklist`);
      fetchBlacklist();
    } catch (err) {
      console.error('Error removing from blacklist:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to remove from blacklist';
      showToast(errorMessage, 'error');
    }
  };

  const filteredBlacklist = blacklist.filter(entry =>
    entry.phone_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
    entry.reason.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="blacklist-page">
      {loading && <LoadingOverlay message="Loading blacklist..." />}
      
      <TopBar 
        title="Blacklist Management" 
        subtitle="Manage blocked phone numbers and suspicious contacts"
      />

      <div className="blacklist-container">
        <div className="blacklist-header">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search phone numbers or reasons..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>

          <button 
            className="add-button"
            onClick={() => setShowAddModal(true)}
          >
            <span className="button-icon">➕</span>
            Add to Blacklist
          </button>
        </div>

        <div className="blacklist-stats">
          <div className="stat-card">
            <span className="stat-icon">🚫</span>
            <div className="stat-content">
              <div className="stat-value">{blacklist.length}</div>
              <div className="stat-label">Blacklisted Numbers</div>
            </div>
          </div>
        </div>

        <div className="blacklist-table-container">
          {filteredBlacklist.length > 0 ? (
            <table className="blacklist-table">
              <thead>
                <tr>
                  <th>Phone Number</th>
                  <th>Reason</th>
                  <th>Added Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredBlacklist.map((entry) => (
                  <tr key={entry.id}>
                    <td className="phone-cell">
                      <span className="phone-icon">📱</span>
                      {entry.phone_number}
                    </td>
                    <td className="reason-cell">{entry.reason}</td>
                    <td className="date-cell">
                      {new Date(entry.added_at).toLocaleDateString()}
                    </td>
                    <td className="actions-cell">
                      <button
                        className="remove-button"
                        onClick={() => handleRemoveBlacklist(entry.id, entry.phone_number)}
                      >
                        <span className="button-icon">🗑️</span>
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <span className="empty-icon">📋</span>
              <h3>No Blacklisted Numbers</h3>
              <p>
                {searchTerm 
                  ? 'No results found for your search'
                  : 'Add phone numbers to the blacklist to block them from analysis'}
              </p>
            </div>
          )}
        </div>
      </div>

      {showAddModal && (
        <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add to Blacklist</h3>
              <button 
                className="modal-close"
                onClick={() => setShowAddModal(false)}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddBlacklist} className="modal-form">
              <div className="form-group">
                <label className="form-label">Phone Number</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="+1234567890"
                  value={newEntry.phone_number}
                  onChange={(e) => setNewEntry({...newEntry, phone_number: e.target.value})}
                  required
                  disabled={submitting}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Reason</label>
                <textarea
                  className="form-textarea"
                  placeholder="Why is this number being blacklisted?"
                  rows="4"
                  value={newEntry.reason}
                  onChange={(e) => setNewEntry({...newEntry, reason: e.target.value})}
                  required
                  disabled={submitting}
                />
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={() => setShowAddModal(false)}
                  disabled={submitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="submit-button"
                  disabled={submitting}
                >
                  {submitting ? 'Adding...' : 'Add to Blacklist'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default BlacklistManagement;
