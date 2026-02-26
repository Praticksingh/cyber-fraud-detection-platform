import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './context/ToastContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { setAuthToken } from './services/api';
import ProtectedRoute from './components/ProtectedRoute';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Analyze from './pages/Analyze';
import AdminPanel from './pages/AdminPanel';
import BlacklistManagement from './pages/BlacklistManagement';
import './App.css';

function AppContent() {
  const { user, token, loading } = useAuth();
  
  // Set auth token for API calls whenever it changes
  useEffect(() => {
    setAuthToken(token);
  }, [token]);
  
  // Show loading screen while checking auth
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        background: '#0a0e27',
        color: '#fff',
        fontSize: '18px'
      }}>
        <div>Loading...</div>
      </div>
    );
  }
  
  return (
    <div className="app">
      {user && <Sidebar />}
      <div className={`main-wrapper ${!user ? 'full-width' : ''}`}>
        <div className="main-content">
          <Routes>
            <Route 
              path="/login" 
              element={user ? <Navigate to="/" replace /> : <Login />} 
            />
            <Route 
              path="/register" 
              element={user ? <Navigate to="/" replace /> : <Register />} 
            />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/analyze" 
              element={
                <ProtectedRoute>
                  <Analyze />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin" 
              element={
                <ProtectedRoute requireAdmin>
                  <AdminPanel />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin/blacklist" 
              element={
                <ProtectedRoute requireAdmin>
                  <BlacklistManagement />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <ToastProvider>
      <Router>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </Router>
    </ToastProvider>
  );
}

export default App;
