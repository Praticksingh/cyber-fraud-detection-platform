import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useToast } from '../context/ToastContext';
import axios from 'axios';
import './Register.css';

// Get API base URL from environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Password validation regex
const PASSWORD_REGEX = {
  minLength: /.{8,}/,
  maxLength: /^.{0,72}$/,
  uppercase: /[A-Z]/,
  lowercase: /[a-z]/,
  number: /\d/,
  special: /[@$!%*?&]/
};

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordErrors, setPasswordErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { showToast } = useToast();

  const validatePassword = (password) => {
    const errors = [];
    
    if (!PASSWORD_REGEX.minLength.test(password)) {
      errors.push('At least 8 characters');
    }
    if (!PASSWORD_REGEX.maxLength.test(password)) {
      errors.push('Maximum 72 characters');
    }
    if (!PASSWORD_REGEX.uppercase.test(password)) {
      errors.push('One uppercase letter');
    }
    if (!PASSWORD_REGEX.lowercase.test(password)) {
      errors.push('One lowercase letter');
    }
    if (!PASSWORD_REGEX.number.test(password)) {
      errors.push('One number');
    }
    if (!PASSWORD_REGEX.special.test(password)) {
      errors.push('One special character (@$!%*?&)');
    }
    
    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
    
    // Validate password in real-time
    if (name === 'password') {
      const errors = validatePassword(value);
      setPasswordErrors(errors);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const toggleConfirmPasswordVisibility = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
      showToast('All fields are required', 'error');
      return;
    }

    // Validate password
    const errors = validatePassword(formData.password);
    if (errors.length > 0) {
      showToast(`Password requirements not met: ${errors.join(', ')}`, 'error');
      return;
    }

    // Check password length in bytes (bcrypt limitation)
    const passwordBytes = new TextEncoder().encode(formData.password).length;
    if (passwordBytes > 72) {
      showToast('Password exceeds 72 bytes (bcrypt limitation)', 'error');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      showToast('Passwords do not match', 'error');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/register`, {
        username: formData.username,
        email: formData.email,
        password: formData.password
      });

      showToast(response.data.message || 'Registration successful!', 'success');
      
      // Redirect to login after successful registration
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (err) {
      console.error('Registration error:', err);
      console.error('Error response:', err.response);
      console.error('Error response data:', err.response?.data);
      console.error('Error message:', err.message);
      console.error('API URL:', API_BASE_URL);
      
      // Extract detailed error message from backend
      let errorMessage = 'Registration failed. Please try again.';
      
      // Check for network errors
      if (err.message === 'Network Error' || !err.response) {
        errorMessage = `Cannot connect to server at ${API_BASE_URL}. Please ensure the backend is running on port 8000.`;
        console.error('Network error detected. Backend might not be running.');
      } else if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          // Pydantic validation errors
          const validationErrors = err.response.data.detail
            .map(e => e.msg || e.message)
            .join(', ');
          errorMessage = validationErrors;
        } else {
          // Simple error message
          errorMessage = err.response.data.detail;
        }
      } else if (err.message) {
        errorMessage = `Registration failed: ${err.message}`;
      }
      
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  const getPasswordStrengthColor = () => {
    const errors = passwordErrors.length;
    if (errors === 0 && formData.password.length > 0) return '#10b981'; // Green
    if (errors <= 2) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-header">
          <div className="register-logo">🛡️</div>
          <h1 className="register-title">Create Account</h1>
          <p className="register-subtitle">Join FraudGuard AI</p>
        </div>

        <div className="register-card">
          <form onSubmit={handleSubmit} className="register-form">
            <div className="form-group">
              <label className="form-label">Username</label>
              <input
                type="text"
                name="username"
                className="form-input"
                placeholder="Choose a username"
                value={formData.username}
                onChange={handleChange}
                disabled={loading}
                autoComplete="username"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Email</label>
              <input
                type="email"
                name="email"
                className="form-input"
                placeholder="your@email.com"
                value={formData.email}
                onChange={handleChange}
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <div className="password-input-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  className="form-input"
                  placeholder="Enter a strong password"
                  value={formData.password}
                  onChange={handleChange}
                  disabled={loading}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={togglePasswordVisibility}
                  disabled={loading}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              
              {/* Password Requirements */}
              <div className="password-requirements">
                <div className="requirements-title">Password Requirements:</div>
                <ul className="requirements-list">
                  <li className={PASSWORD_REGEX.minLength.test(formData.password) ? 'valid' : ''}>
                    ✓ 8-72 characters
                  </li>
                  <li className={PASSWORD_REGEX.uppercase.test(formData.password) ? 'valid' : ''}>
                    ✓ At least one uppercase letter
                  </li>
                  <li className={PASSWORD_REGEX.lowercase.test(formData.password) ? 'valid' : ''}>
                    ✓ At least one lowercase letter
                  </li>
                  <li className={PASSWORD_REGEX.number.test(formData.password) ? 'valid' : ''}>
                    ✓ At least one number
                  </li>
                  <li className={PASSWORD_REGEX.special.test(formData.password) ? 'valid' : ''}>
                    ✓ At least one special character (@$!%*?&)
                  </li>
                </ul>
                <div className="requirements-note">
                  Maximum 72 characters (bcrypt limitation)
                </div>
              </div>
              
              {/* Password Strength Indicator */}
              {formData.password && (
                <div className="password-strength">
                  <div className="strength-bar">
                    <div 
                      className="strength-fill"
                      style={{
                        width: `${((6 - passwordErrors.length) / 6) * 100}%`,
                        backgroundColor: getPasswordStrengthColor()
                      }}
                    ></div>
                  </div>
                  <div className="strength-text" style={{ color: getPasswordStrengthColor() }}>
                    {passwordErrors.length === 0 ? 'Strong' : 
                     passwordErrors.length <= 2 ? 'Medium' : 'Weak'}
                  </div>
                </div>
              )}
            </div>

            <div className="form-group">
              <label className="form-label">Confirm Password</label>
              <div className="password-input-wrapper">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  name="confirmPassword"
                  className="form-input"
                  placeholder="Re-enter your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  disabled={loading}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={toggleConfirmPasswordVisibility}
                  disabled={loading}
                  aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                >
                  {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {formData.confirmPassword && formData.password !== formData.confirmPassword && (
                <div className="validation-error">
                  Passwords do not match
                </div>
              )}
            </div>

            <button 
              type="submit" 
              className="register-button"
              disabled={loading || passwordErrors.length > 0}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="register-footer">
            <p className="register-link-text">
              Already have an account?{' '}
              <Link to="/login" className="register-link">
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
