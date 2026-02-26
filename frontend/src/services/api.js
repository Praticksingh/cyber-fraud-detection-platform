import axios from 'axios';

// Get base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_KEY = process.env.REACT_APP_API_KEY || 'public123';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-KEY': API_KEY,
  },
});

// Function to set auth token
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Export API base URL for use in other files
export const API_URL = API_BASE_URL;

// API endpoints
export const fraudAPI = {
  // Analytics endpoints (public)
  getSummary: () => api.get('/analytics/summary'),
  getDistribution: () => api.get('/analytics/distribution'),
  getTrends: (days = 30) => api.get(`/analytics/trends?days=${days}`),
  getGraph: (limit = 100) => api.get(`/graph?limit=${limit}`),
  getRecentActivity: (limit = 10) => api.get(`/stats?limit=${limit}`),
  getHistory: () => api.get('/history'),
  
  // Analysis endpoint
  analyze: (data) => api.post('/analyze', data),
};

export default api;
