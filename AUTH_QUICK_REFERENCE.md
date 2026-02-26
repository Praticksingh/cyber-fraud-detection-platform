# Authentication Quick Reference

## For Users

### Register
1. Go to `/register`
2. Enter username, email, password
3. Password must have:
   - 8-72 characters
   - 1 uppercase letter
   - 1 lowercase letter
   - 1 number
   - 1 special character (@$!%*?&)

### Login
1. Go to `/login`
2. Enter username and password
3. Click "Sign In"
4. Redirected to dashboard

### Logout
1. Click logout button in sidebar
2. Session cleared
3. Redirected to login

## For Developers

### Check Authentication
```javascript
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { isAuthenticated, user } = useAuth();
  
  if (!isAuthenticated) {
    return <div>Please login</div>;
  }
  
  return <div>Welcome {user.username}</div>;
}
```

### Protect a Route
```javascript
import ProtectedRoute from './components/ProtectedRoute';

<Route 
  path="/my-route" 
  element={
    <ProtectedRoute>
      <MyComponent />
    </ProtectedRoute>
  } 
/>
```

### Protect Admin Route
```javascript
<Route 
  path="/admin-route" 
  element={
    <ProtectedRoute requireAdmin>
      <AdminComponent />
    </ProtectedRoute>
  } 
/>
```

### Make Authenticated API Call
```javascript
import api from './services/api';

// Token automatically included
const response = await api.get('/history');
```

### Get User Info
```javascript
import { useAuth } from './context/AuthContext';

const { user } = useAuth();
console.log(user.username); // "testuser"
console.log(user.role);     // "user" or "admin"
```

### Check User Role
```javascript
import { useAuth } from './context/AuthContext';

const { hasRole } = useAuth();

if (hasRole('admin')) {
  // Show admin features
}
```

### Manual Token Operations
```javascript
import { getToken, isAuthenticated, getUserRole } from './utils/auth';

const token = getToken();
const isLoggedIn = isAuthenticated();
const role = getUserRole();
```

## Backend Endpoints

### Public
- `POST /register` - Register new user
- `POST /login` - Login and get JWT
- `POST /analyze` - Analyze fraud (API key)
- `GET /analytics/*` - Analytics data
- `GET /graph` - Knowledge graph

### Authenticated (JWT Required)
- `GET /history` - All fraud logs
- `GET /history/{phone}` - Phone history
- `GET /stats` - Statistics

### Admin Only (JWT + Admin Role)
- `GET /admin` - Admin dashboard
- `GET /config` - Configuration
- `GET /blacklist` - Blacklist

## Token Format

### JWT Payload
```json
{
  "sub": "username",
  "role": "user",
  "exp": 1234567890
}
```

### Authorization Header
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## localStorage Keys

- `token` - JWT token string
- `user` - User object JSON
- `auditLogs` - Audit log array

## Common Tasks

### Create Admin User (Backend)
```python
from database import SessionLocal
from auth import create_user

db = SessionLocal()
create_user(db, "admin", "admin@example.com", "AdminPass123!", "admin")
db.close()
```

### Test Login (curl)
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'
```

### Test Protected Endpoint (curl)
```bash
TOKEN="your_jwt_token_here"

curl -X GET http://127.0.0.1:8000/history \
  -H "Authorization: Bearer $TOKEN"
```

### Clear Session (Browser Console)
```javascript
localStorage.clear();
location.reload();
```

## Troubleshooting

### Not Logged In After Refresh
```javascript
// Check localStorage
console.log(localStorage.getItem('token'));
console.log(localStorage.getItem('user'));

// If null, token was cleared or expired
```

### Access Denied
```javascript
// Check user role
import { getUserRole } from './utils/auth';
console.log(getUserRole()); // Should be "admin" for admin routes
```

### API 401 Error
```javascript
// Check token is being sent
import { getToken } from './utils/auth';
console.log(getToken()); // Should return JWT string

// Check in Network tab
// Authorization header should be present
```

## Environment Setup

### Frontend (.env)
```env
REACT_APP_API_BASE=http://127.0.0.1:8000
REACT_APP_API_KEY=public123
```

### Backend (config.py or .env)
```python
SECRET_KEY="change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
```

## Security Checklist

- [ ] JWT secret key changed from default
- [ ] HTTPS enabled in production
- [ ] CORS origins configured
- [ ] Password requirements enforced
- [ ] Rate limiting on auth endpoints
- [ ] Audit logging enabled
- [ ] Token expiration set appropriately
- [ ] Admin accounts use strong passwords

## File Structure

```
frontend/src/
├── utils/
│   └── auth.js              # Auth utility functions
├── context/
│   └── AuthContext.js       # Auth state management
├── components/
│   ├── ProtectedRoute.js    # Route protection
│   └── Sidebar.js           # User info display
├── pages/
│   ├── Login.js             # Login page
│   ├── Register.js          # Registration page
│   ├── Dashboard.js         # Protected route
│   ├── Analyze.js           # Protected route
│   └── AdminPanel.js        # Admin-only route
└── services/
    └── api.js               # API client with auth
```

## Quick Commands

### Start Development
```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Install Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Run Tests
```bash
# Backend
python -m pytest

# Frontend
cd frontend
npm test
```

## Status Codes

- `200` - Success
- `201` - Created (registration)
- `400` - Bad request (validation error)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `500` - Server error

## Support Resources

- **JWT_AUTHENTICATION_IMPLEMENTATION.md** - Full documentation
- **frontend/JWT_TESTING_GUIDE.md** - Testing procedures
- **AUTHENTICATION_COMPLETE.md** - Implementation summary
- **BCRYPT_FIX_SUMMARY.md** - Password hashing details
