import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import {
  getToken as getStoredToken,
  setToken as setStoredToken,
  removeToken,
  getUser as getStoredUser,
  setUser as setStoredUser,
  isTokenExpired,
  decodeToken,
  clearAuth
} from '../utils/auth';

const AuthContext = createContext();

// Get API base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  // Initialize from localStorage
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initAuth = () => {
      const storedToken = getStoredToken();
      const storedUser = getStoredUser();

      if (storedToken && storedUser) {
        // Check if token is expired
        if (isTokenExpired(storedToken)) {
          // Token expired, clear auth
          clearAuth();
          setUser(null);
          setToken(null);
          setIsAuthenticated(false);
        } else {
          // Token valid, restore session
          setToken(storedToken);
          setUser(storedUser);
          setIsAuthenticated(true);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = useCallback(async (username, password) => {
    try {
      // Call backend login API
      const response = await axios.post(`${API_BASE_URL}/login`, {
        username,
        password
      });

      const { access_token, role, username: returnedUsername } = response.data;

      // Store token in localStorage
      setStoredToken(access_token);
      
      // Store user data
      const userData = {
        username: returnedUsername,
        role,
        loginTime: new Date().toISOString(),
      };
      setStoredUser(userData);
      
      // Update state
      setToken(access_token);
      setUser(userData);
      setIsAuthenticated(true);
      
      // Log audit event
      logAuditEvent('login', returnedUsername, role);
      
      return { success: true, user: userData };
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.detail || 'Invalid credentials';
      return { success: false, error: errorMessage };
    }
  }, []);

  const logout = useCallback(() => {
    if (user) {
      logAuditEvent('logout', user.username, user.role);
    }
    
    // Clear localStorage
    clearAuth();
    
    // Clear state
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  }, [user]);

  const hasRole = useCallback((requiredRole) => {
    if (!user) return false;
    if (requiredRole === 'admin') {
      return user.role === 'admin';
    }
    return true; // user role can access user-level routes
  }, [user]);

  const logAuditEvent = (action, username, role) => {
    const auditLogs = JSON.parse(sessionStorage.getItem('auditLogs') || '[]');
    auditLogs.unshift({
      id: Date.now(),
      timestamp: new Date().toISOString(),
      action,
      username,
      role,
    });
    // Keep only last 50 events
    sessionStorage.setItem('auditLogs', JSON.stringify(auditLogs.slice(0, 50)));
  };

  const getAuditLogs = useCallback(() => {
    return JSON.parse(sessionStorage.getItem('auditLogs') || '[]');
  }, []);

  const addAuditLog = useCallback((action, details = '') => {
    if (user) {
      const auditLogs = JSON.parse(sessionStorage.getItem('auditLogs') || '[]');
      auditLogs.unshift({
        id: Date.now(),
        timestamp: new Date().toISOString(),
        action,
        role: user.role,
        details,
      });
      sessionStorage.setItem('auditLogs', JSON.stringify(auditLogs.slice(0, 50)));
    }
  }, [user]);

  // Get token for API calls
  const getToken = useCallback(() => {
    return token;
  }, [token]);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated,
        loading,
        login,
        logout,
        hasRole,
        getAuditLogs,
        addAuditLog,
        getToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
