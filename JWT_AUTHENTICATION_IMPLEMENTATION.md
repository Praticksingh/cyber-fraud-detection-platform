# JWT Authentication Implementation

## Overview
Implemented comprehensive JWT-based authentication flow with localStorage persistence, route protection, and role-based access control.

## Frontend Changes

### 1. Auth Utility (`frontend/src/utils/auth.js`) - NEW FILE
Created utility functions for JWT token management:

```javascript
// Token Management
- setToken(token) - Store JWT in localStorage
- getToken() - Retrieve JWT from localStorage
- removeToken() - Clear JWT from localStorage
- isAuthenticated() - Check if user has valid token

// User Management
- setUser(user) - Store user data in localStorage
- getUser() - Retrieve user data from localStorage

// Token Operations
- decodeToken(token) - Decode JWT payload (client-side only)
- isTokenExpired(token) - Check if token is expired
- getUserRole() - Get user role from token
- isAdmin() - Check if user has admin role
- clearAuth() - Clear all auth data
```

### 2. AuthContext Updates (`frontend/src/context/AuthContext.js`)
Enhanced authentication context with localStorage persistence:

**Key Changes:**
- Added `loading` state for initialization
- Initialize auth state from localStorage on mount
- Check token expiration on app load
- Store token and user data in localStorage on login
- Clear localStorage on logout
- Auto-restore session if token is valid

**New Features:**
```javascript
// Initialize from localStorage
useEffect(() => {
  const storedToken = getStoredToken();
  const storedUser = getStoredUser();
  
  if (storedToken && storedUser) {
    if (!isTokenExpired(storedToken)) {
      // Restore session
      setToken(storedToken);
      setUser(storedUser);
      setIsAuthenticated(true);
    } else {
      // Clear expired session
      clearAuth();
    }
  }
  setLoading(false);
}, []);
```

### 3. ProtectedRoute Component (`frontend/src/components/ProtectedRoute.js`)
Enhanced route protection with better UX:

**Features:**
- Loading state while checking authentication
- Redirect to login if not authenticated
- Access denied page for non-admin users on admin routes
- Styled error pages matching app theme

**Access Denied Page:**
```
🚫
Access Denied
You don't have permission to access this page.
[Go to Dashboard]
```

### 4. Sidebar Component (`frontend/src/components/Sidebar.js`)
Added user information display:

**New Elements:**
- Username display at top
- Role badge (Admin 👑 / User 👤)
- Logout button with icon
- Conditional admin link visibility

**User Info Section:**
```
FraudGuard AI
─────────────
username
[👑 admin] or [👤 user]
```

### 5. Sidebar Styles (`frontend/src/components/Sidebar.css`)
Added styles for user info section:

```css
.user-info - Container for user details
.user-name - Username display
.user-badge - Role badge styling
.logout-button - Logout button with hover effects
```

### 6. App Component (`frontend/src/App.js`)
Added loading state handling:

- Show loading screen while checking auth
- Prevent flash of wrong content
- Smooth transition to authenticated state

## Route Protection

### Protected Routes
All routes except `/login` and `/register` require authentication:

1. **Dashboard** (`/`) - All authenticated users
2. **Analyze** (`/analyze`) - All authenticated users
3. **Admin Panel** (`/admin`) - Admin users only

### Auto-Redirect Logic
- Logged-in users visiting `/login` or `/register` → Redirect to `/`
- Non-authenticated users visiting protected routes → Redirect to `/login`
- Non-admin users visiting `/admin` → Show "Access Denied" page

## Backend Verification

### JWT-Protected Endpoints
✅ `/admin` - Requires admin role
✅ `/history` - Requires authentication
✅ `/history/{phone_number}` - Requires authentication
✅ `/stats` - Requires authentication
✅ `/config` - Requires admin role
✅ `/blacklist` - Requires admin role

### Public Endpoints
✅ `/` - Welcome page
✅ `/register` - User registration
✅ `/login` - User login
✅ `/analyze` - Fraud analysis (API key protected)
✅ `/analytics/*` - Analytics endpoints
✅ `/graph` - Knowledge graph data

## Security Features

### Token Storage
- **Location**: localStorage (persistent across sessions)
- **Key**: `token` for JWT, `user` for user data
- **Expiration**: Checked on app initialization
- **Cleanup**: Cleared on logout

### Token Validation
- Client-side expiration check on app load
- Server-side validation on every protected request
- Automatic session restoration if token valid
- Automatic logout if token expired

### Role-Based Access Control
- User role stored in JWT payload
- Role checked on protected routes
- Admin routes require `role === 'admin'`
- Non-admin users see "Access Denied" page

## User Experience

### Login Flow
1. User enters credentials
2. Backend validates and returns JWT
3. Frontend stores token in localStorage
4. User redirected to dashboard
5. Sidebar shows username and role

### Session Persistence
1. User closes browser
2. User reopens app
3. App checks localStorage for token
4. If valid, auto-login
5. If expired, redirect to login

### Logout Flow
1. User clicks logout button
2. Token cleared from localStorage
3. User data cleared from state
4. Redirect to login page
5. Audit log recorded

## API Integration

### Authorization Header
All authenticated requests include:
```
Authorization: Bearer <jwt_token>
```

### API Service (`frontend/src/services/api.js`)
- `setAuthToken(token)` called on login
- Token added to all axios requests
- Token removed on logout

## Testing Checklist

### Authentication
- [x] Login with valid credentials
- [x] Login with invalid credentials
- [x] Register new user
- [x] Token stored in localStorage
- [x] Session persists after page refresh
- [x] Logout clears token

### Route Protection
- [x] Unauthenticated user redirected to login
- [x] Authenticated user can access dashboard
- [x] Authenticated user can access analyze
- [x] Admin user can access admin panel
- [x] Non-admin user sees "Access Denied" on admin route
- [x] Logged-in user redirected from login page

### UI Elements
- [x] Username displayed in sidebar
- [x] Role badge shows correct role
- [x] Admin link only visible to admins
- [x] Logout button works
- [x] Loading state shows during auth check

### Token Management
- [x] Token decoded correctly
- [x] Expired token triggers logout
- [x] Valid token restores session
- [x] Token sent with API requests

## Files Modified

### New Files
1. `frontend/src/utils/auth.js` - Auth utility functions

### Modified Files
1. `frontend/src/context/AuthContext.js` - localStorage integration
2. `frontend/src/components/ProtectedRoute.js` - Enhanced protection
3. `frontend/src/components/Sidebar.js` - User info display
4. `frontend/src/components/Sidebar.css` - User info styles
5. `frontend/src/App.js` - Loading state handling

## Environment Variables

```env
REACT_APP_API_BASE=http://127.0.0.1:8000
REACT_APP_API_KEY=public123
```

## Production Considerations

### Security
- Change JWT secret key in production
- Use HTTPS for all requests
- Set appropriate CORS origins
- Implement token refresh mechanism
- Add rate limiting on auth endpoints

### Token Expiration
- Current: 24 hours
- Consider: Shorter expiration + refresh tokens
- Implement: Auto-refresh before expiration

### Storage
- Current: localStorage (persistent)
- Alternative: sessionStorage (session-only)
- Consider: Secure httpOnly cookies

## Next Steps

### Recommended Enhancements
1. Implement refresh token mechanism
2. Add "Remember Me" option
3. Add password reset functionality
4. Implement 2FA for admin accounts
5. Add session timeout warning
6. Log all authentication events
7. Add device management
8. Implement IP-based restrictions

### Monitoring
1. Track failed login attempts
2. Monitor token expiration rates
3. Log suspicious activity
4. Alert on multiple failed logins
5. Track session duration

## Usage

### For Users
1. Register account at `/register`
2. Login at `/login`
3. Access dashboard automatically
4. Session persists across browser restarts
5. Click logout to end session

### For Admins
1. Login with admin credentials
2. Access admin panel at `/admin`
3. Manage system settings
4. View audit logs
5. Manage API keys

### For Developers
```javascript
// Check if user is authenticated
import { isAuthenticated, getToken, getUserRole } from './utils/auth';

if (isAuthenticated()) {
  const token = getToken();
  const role = getUserRole();
  // Make authenticated request
}

// Use auth context
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, logout } = useAuth();
  
  if (!isAuthenticated) {
    return <div>Please login</div>;
  }
  
  return <div>Welcome {user.username}</div>;
}
```

## Troubleshooting

### Token Not Persisting
- Check localStorage is enabled
- Check browser privacy settings
- Clear localStorage and re-login

### Access Denied on Admin Route
- Verify user role is 'admin'
- Check JWT payload contains role
- Re-login to refresh token

### Session Not Restoring
- Check token expiration
- Verify localStorage has token
- Check browser console for errors

### API Requests Failing
- Verify token is being sent
- Check Authorization header
- Verify backend JWT validation
