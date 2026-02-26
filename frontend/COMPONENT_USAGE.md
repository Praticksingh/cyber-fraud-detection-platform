# Component Usage Guide

Quick reference for using the new components in the Fraud Detection Platform.

## LoadingOverlay

### Import
```javascript
import LoadingOverlay from '../components/LoadingOverlay';
```

### Usage
```javascript
function MyComponent() {
  const [loading, setLoading] = useState(false);
  
  return (
    <div>
      {loading && <LoadingOverlay message="Processing..." />}
      {/* Your content */}
    </div>
  );
}
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| message | string | "Loading..." | Text displayed below spinner |

### Features
- Full-screen overlay with backdrop blur
- Prevents user interaction during loading
- Smooth fade-in animation
- Centered spinner with glow effect

---

## Toast Notifications

### Setup (Already done in App.js)
```javascript
import { ToastProvider } from './context/ToastContext';

function App() {
  return (
    <ToastProvider>
      {/* Your app */}
    </ToastProvider>
  );
}
```

### Usage in Components
```javascript
import { useToast } from '../context/ToastContext';

function MyComponent() {
  const { showToast } = useToast();
  
  const handleSuccess = () => {
    showToast('Operation completed successfully!', 'success');
  };
  
  const handleError = () => {
    showToast('Something went wrong', 'error');
  };
  
  return (
    <div>
      <button onClick={handleSuccess}>Success</button>
      <button onClick={handleError}>Error</button>
    </div>
  );
}
```

### API
```javascript
showToast(message, type)
```

**Parameters:**
- `message` (string): The notification message
- `type` (string): 'success' or 'error'

### Features
- Auto-dismiss after 4 seconds
- Manual close button
- Stacks multiple toasts
- Slide-in animation
- Color-coded by type
- Responsive design

---

## RiskGauge

### Import
```javascript
import RiskGauge from '../components/RiskGauge';
```

### Usage
```javascript
function AnalysisResult({ riskScore, riskLevel }) {
  return (
    <div>
      <RiskGauge score={riskScore} level={riskLevel} />
    </div>
  );
}
```

### Props
| Prop | Type | Required | Description |
|------|------|----------|-------------|
| score | number | Yes | Risk score (0-100) |
| level | string | Yes | Risk level label (Low, Medium, High, Critical) |

### Color Mapping
- **0-30**: Green (#10b981) - Low Risk
- **31-60**: Yellow (#f59e0b) - Medium Risk
- **61-80**: Orange (#fb923c) - High Risk
- **81-100**: Red (#ef4444) - Critical Risk

### Features
- Circular SVG progress meter
- Animates from 0 to score (1.5s)
- Glow effect on progress ring
- Scale-in animation for score
- Fade-in animation for label
- Responsive sizing

---

## API Service

### Import
```javascript
import { fraudAPI } from '../services/api';
```

### Available Methods

#### Get Analytics Summary
```javascript
const response = await fraudAPI.getSummary();
// Returns: { total_scans, high_risk, medium_risk, low_risk }
```

#### Get Risk Distribution
```javascript
const response = await fraudAPI.getDistribution();
// Returns: { critical, high, medium, low }
```

#### Get Trends
```javascript
const response = await fraudAPI.getTrends(30); // days
// Returns: [{ date, count }, ...]
```

#### Get Knowledge Graph
```javascript
const response = await fraudAPI.getGraph(100); // limit
// Returns: { nodes, edges, statistics }
```

#### Analyze Message
```javascript
const data = {
  phone_number: '+1234567890',
  message_content: 'Your message here'
};
const response = await fraudAPI.analyze(data);
// Returns: { risk_score, risk_level, confidence, ... }
```

### Error Handling
```javascript
try {
  const response = await fraudAPI.analyze(data);
  // Handle success
} catch (err) {
  const errorMessage = err.response?.data?.detail || 
                      err.response?.data?.message || 
                      'Default error message';
  // Handle error
}
```

---

## Environment Variables

### Required Variables
Create `.env` file in `frontend/` directory:

```env
# Backend API base URL
REACT_APP_API_BASE=http://127.0.0.1:8000

# API authentication key
REACT_APP_API_KEY=public123
```

### Production Example
```env
REACT_APP_API_BASE=https://api.yourcompany.com
REACT_APP_API_KEY=prod_key_here
```

### Accessing in Code
```javascript
const apiBase = process.env.REACT_APP_API_BASE;
const apiKey = process.env.REACT_APP_API_KEY;
```

---

## Common Patterns

### Loading State with Toast
```javascript
import { useState } from 'react';
import { useToast } from '../context/ToastContext';
import LoadingOverlay from '../components/LoadingOverlay';
import { fraudAPI } from '../services/api';

function MyComponent() {
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();
  
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fraudAPI.getSummary();
      showToast('Data loaded successfully!', 'success');
      // Handle response
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to load data';
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      {loading && <LoadingOverlay message="Loading data..." />}
      <button onClick={fetchData} disabled={loading}>
        Load Data
      </button>
    </div>
  );
}
```

### Form with Validation
```javascript
function AnalyzeForm() {
  const [formData, setFormData] = useState({
    phone_number: '',
    message_content: ''
  });
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.phone_number && !formData.message_content) {
      showToast('Please enter phone number or message', 'error');
      return;
    }
    
    setLoading(true);
    try {
      const response = await fraudAPI.analyze(formData);
      showToast('Analysis completed!', 'success');
      // Handle response
    } catch (err) {
      showToast(err.response?.data?.detail || 'Analysis failed', 'error');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {loading && <LoadingOverlay message="Analyzing..." />}
      {/* Form fields */}
      <button type="submit" disabled={loading}>
        Analyze
      </button>
    </form>
  );
}
```

### Display Risk with Gauge
```javascript
import RiskGauge from '../components/RiskGauge';

function ResultDisplay({ result }) {
  return (
    <div className="result-container">
      <RiskGauge 
        score={result.risk_score} 
        level={result.risk_level} 
      />
      <div className="result-details">
        <p>Confidence: {result.confidence}%</p>
        <p>Category: {result.threat_category}</p>
      </div>
    </div>
  );
}
```

---

## Styling Guidelines

### Consistent with Dark Theme
All components use the existing color palette:

```css
/* Backgrounds */
--bg-overlay: rgba(10, 14, 39, 0.85);
--bg-card: linear-gradient(135deg, rgba(26, 31, 58, 0.98), rgba(21, 24, 41, 0.98));

/* Colors */
--success: #10b981;
--warning: #f59e0b;
--danger: #ef4444;
--primary: #6366f1;

/* Text */
--text-primary: #ffffff;
--text-secondary: #a0a0b0;
```

### Animation Timing
- Fast interactions: 0.2s
- Standard transitions: 0.3s
- Loading states: 0.5s
- Progress animations: 1.5s

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## Troubleshooting

### Toast not showing
- Ensure `ToastProvider` wraps your app in `App.js`
- Check that you're using `useToast()` hook correctly
- Verify component is inside `ToastProvider` tree

### LoadingOverlay not appearing
- Check that `loading` state is true
- Ensure component is rendered conditionally
- Verify CSS is imported

### RiskGauge not animating
- Ensure `score` prop is a number (0-100)
- Check that component re-renders with new score
- Verify browser supports CSS animations

### API calls failing
- Check `.env` file exists with correct variables
- Verify `REACT_APP_API_BASE` points to running backend
- Ensure `REACT_APP_API_KEY` matches backend key
- Check browser console for CORS errors

---

## Best Practices

1. **Always show loading state** during async operations
2. **Provide feedback** with toast notifications
3. **Disable buttons** during loading to prevent double-submission
4. **Extract error messages** from backend responses
5. **Use meaningful loading messages** for better UX
6. **Handle all error cases** with appropriate messages
7. **Keep toast messages concise** (under 100 characters)
8. **Test responsive behavior** on mobile devices

---

## Support

For issues or questions:
1. Check this guide first
2. Review component source code
3. Check browser console for errors
4. Verify environment variables are set
5. Ensure backend is running and accessible
