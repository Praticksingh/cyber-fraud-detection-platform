/**
 * Centralized API Configuration
 * 
 * This file manages the backend API URL for all environments.
 * 
 * Environment Variables:
 * - REACT_APP_API_URL: Backend API base URL
 * 
 * Development: http://localhost:8000
 * Production: Set via Vercel environment variable
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default API_BASE_URL;
