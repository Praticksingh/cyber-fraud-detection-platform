import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="brand-icon">🛡️</span>
          <span className="brand-text">Fraud Detection AI</span>
        </div>
        <div className="navbar-links">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Dashboard
          </Link>
          <Link 
            to="/analyze" 
            className={`nav-link ${location.pathname === '/analyze' ? 'active' : ''}`}
          >
            Analyze
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
