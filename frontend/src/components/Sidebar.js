import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Sidebar.css';

function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <span className="logo-icon">🛡️</span>
          <span className="logo-text">FraudGuard AI</span>
        </div>
        {user && (
          <div className="user-info">
            <div className="user-name">{user.username}</div>
            <div className="user-badge">
              <span className={`role-indicator role-${user.role}`}>
                {user.role === 'admin' ? '👑' : '👤'}
              </span>
              <span className="role-text">{user.role}</span>
            </div>
          </div>
        )}
      </div>
      
      <nav className="sidebar-nav">
        <Link 
          to="/" 
          className={`sidebar-link ${location.pathname === '/' ? 'active' : ''}`}
        >
          <span className="link-icon">📊</span>
          <span className="link-text">Dashboard</span>
        </Link>
        
        <Link 
          to="/analyze" 
          className={`sidebar-link ${location.pathname === '/analyze' ? 'active' : ''}`}
        >
          <span className="link-icon">🔍</span>
          <span className="link-text">Analyze</span>
        </Link>
        
        {user?.role === 'admin' && (
          <>
            <Link 
              to="/admin" 
              className={`sidebar-link ${location.pathname === '/admin' ? 'active' : ''}`}
            >
              <span className="link-icon">⚙️</span>
              <span className="link-text">Admin</span>
            </Link>
            
            <Link 
              to="/admin/blacklist" 
              className={`sidebar-link ${location.pathname === '/admin/blacklist' ? 'active' : ''}`}
            >
              <span className="link-icon">🚫</span>
              <span className="link-text">Blacklist</span>
            </Link>
          </>
        )}
      </nav>
      
      <div className="sidebar-footer">
        <div className="api-status">
          <span className="status-dot"></span>
          <span className="status-text">API Connected</span>
        </div>
        {user && (
          <button className="logout-button" onClick={handleLogout}>
            <span className="logout-icon">🚪</span>
            <span className="logout-text">Logout</span>
          </button>
        )}
      </div>
    </div>
  );
}

export default Sidebar;
