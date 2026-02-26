# JWT Authentication Testing Guide

## Quick Start Testing

### 1. Start Backend
```bash
cd cyber-fraud-system
python main.py
```

Backend should be running on `http://127.0.0.1:8000`

### 2. Start Frontend
```bash
cd frontend
npm start
```

Frontend should open at `http://localhost:3000`

## Test Scenarios

### Scenario 1: New User Registration
1. Navigate to `http://localhost:3000/register`
2. Fill in registration form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `TestPass123!`
   - Confirm Password: `TestPass123!`
3. Click "Register"
4. ✅ Should see success message
5. ✅ Should redirect to login page

### Scenario 2: User Login
1. Navigate to `http://localhost:3000/login`
2. Enter credentials:
   - Username: `testuser`
   - Password: `TestPass123!`
3. Click "Sign In"
4. ✅ Should see welcome toast
5. ✅ Should redirect to dashboard
6. ✅ Sidebar should show username "testuser"
7. ✅ Sidebar should show "👤 user" badge
8. ✅ Should see Dashboard and Analyze links
9. ✅ Should NOT see Admin link

### Scenario 3: Session Persistence
1. Login as user (see Scenario 2)
2. Close browser tab
3. Open new tab to `http://localhost:3000`
4. ✅ Should automatically be logged in
5. ✅ Should see dashboard (not login page)
6. ✅ Username and role should be displayed

### Scenario 4: Protected Routes
1. Logout (click logout button in sidebar)
2. Try to access `http://localhost:3000/`
3. ✅ Should redirect to `/login`
4. Try to access `http://localhost:3000/analyze`
5. ✅ Should redirect to `/login`
6. Try to access `http://localhost:3000/admin`
7. ✅ Should redirect to `/login`

### Scenario 5: Admin Access
1. Create admin user (backend):
   ```python
   from database import SessionLocal
   from auth import create_user
   
   db = SessionLocal()
   create_user(db, "admin", "admin@example.com", "AdminPass123!", "admin")
   db.close()
   ```
2. Login with admin credentials
3. ✅ Sidebar should show "👑 admin" badge
4. ✅ Should see Admin link in sidebar
5. Click Admin link
6. ✅ Should access admin panel
7. ✅ Should see system stats and controls

### Scenario 6: Non-Admin Accessing Admin Route
1. Login as regular user (testuser)
2. Try to access `http://localhost:3000/admin`
3. ✅ Should see "Access Denied" page
4. ✅ Should show 🚫 icon
5. ✅ Should have "Go to Dashboard" button
6. Click "Go to Dashboard"
7. ✅ Should navigate to dashboard

### Scenario 7: Auto-Redirect When Logged In
1. Login as user
2. Try to access `http://localhost:3000/login`
3. ✅ Should redirect to dashboard
4. Try to access `http://localhost:3000/register`
5. ✅ Should redirect to dashboard

### Scenario 8: Logout
1. Login as user
2. Click logout button in sidebar
3. ✅ Should redirect to login page
4. ✅ Sidebar should disappear
5. Try to access `http://localhost:3000/`
6. ✅ Should redirect to login page
7. Check localStorage in browser DevTools
8. ✅ Token should be removed

### Scenario 9: Token in API Requests
1. Login as user
2. Open browser DevTools → Network tab
3. Navigate to Analyze page
4. Submit fraud analysis
5. Check request headers
6. ✅ Should see `Authorization: Bearer <token>`
7. ✅ Request should succeed

### Scenario 10: Expired Token Handling
1. Login as user
2. Open browser DevTools → Application → Local Storage
3. Find `token` key
4. Manually edit token to invalid value
5. Refresh page
6. ✅ Should redirect to login
7. ✅ Invalid token should be cleared

## Browser DevTools Inspection

### Check localStorage
1. Open DevTools (F12)
2. Go to Application tab
3. Expand Local Storage
4. Click on `http://localhost:3000`
5. Should see:
   - `token`: JWT token string
   - `user`: JSON object with username and role

### Check Token Payload
1. Copy token from localStorage
2. Go to https://jwt.io
3. Paste token in "Encoded" section
4. Check decoded payload:
   ```json
   {
     "sub": "testuser",
     "role": "user",
     "exp": 1234567890
   }
   ```

### Check Network Requests
1. Open DevTools → Network tab
2. Login or make API request
3. Click on request
4. Check Headers tab
5. Should see:
   - `Authorization: Bearer eyJhbGc...`
   - `Content-Type: application/json`

## Common Issues

### Issue: "Access Denied" on Dashboard
**Cause**: Token expired or invalid
**Solution**: 
1. Clear localStorage
2. Re-login

### Issue: Session Not Persisting
**Cause**: localStorage disabled or browser privacy mode
**Solution**:
1. Check browser settings
2. Disable privacy mode
3. Allow localStorage

### Issue: API Requests Failing with 401
**Cause**: Token not being sent or invalid
**Solution**:
1. Check token in localStorage
2. Verify Authorization header in requests
3. Re-login to get fresh token

### Issue: Admin Link Not Showing
**Cause**: User role is not 'admin'
**Solution**:
1. Check user role in localStorage
2. Create admin user in backend
3. Login with admin credentials

### Issue: Infinite Redirect Loop
**Cause**: Auth state not initializing properly
**Solution**:
1. Clear localStorage
2. Clear browser cache
3. Restart frontend dev server

## API Endpoint Testing

### Test Login Endpoint
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'
```

Expected response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "role": "user",
  "username": "testuser"
}
```

### Test Protected Endpoint
```bash
# Get token from login response
TOKEN="eyJhbGc..."

curl -X GET http://127.0.0.1:8000/history \
  -H "Authorization: Bearer $TOKEN"
```

Expected: 200 OK with history data

### Test Admin Endpoint
```bash
# Login as admin first
TOKEN="<admin_token>"

curl -X GET http://127.0.0.1:8000/blacklist \
  -H "Authorization: Bearer $TOKEN"
```

Expected: 200 OK with blacklist data

## Performance Testing

### Load Time
1. Clear cache
2. Open DevTools → Network
3. Refresh page
4. Check load time
5. ✅ Should load in < 2 seconds

### Auth Check Time
1. With valid token in localStorage
2. Refresh page
3. Measure time to dashboard
4. ✅ Should be instant (< 100ms)

## Security Testing

### XSS Protection
1. Try to inject script in username field
2. ✅ Should be sanitized
3. Check rendered output
4. ✅ Should not execute script

### Token Tampering
1. Get valid token from localStorage
2. Modify payload (change role to admin)
3. Try to access admin route
4. ✅ Should fail (backend validates signature)

### CORS Testing
1. Try to make request from different origin
2. ✅ Should be blocked by CORS policy
3. Check backend CORS configuration

## Automated Testing Script

Create `test-auth.js`:
```javascript
// Test authentication flow
async function testAuth() {
  const API_BASE = 'http://127.0.0.1:8000';
  
  // Test registration
  const registerRes = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'testuser' + Date.now(),
      email: 'test@example.com',
      password: 'TestPass123!'
    })
  });
  console.log('Register:', registerRes.status === 201 ? '✅' : '❌');
  
  // Test login
  const loginRes = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'testuser',
      password: 'TestPass123!'
    })
  });
  const loginData = await loginRes.json();
  console.log('Login:', loginRes.status === 200 ? '✅' : '❌');
  
  // Test protected endpoint
  const historyRes = await fetch(`${API_BASE}/history`, {
    headers: { 'Authorization': `Bearer ${loginData.access_token}` }
  });
  console.log('Protected Route:', historyRes.status === 200 ? '✅' : '❌');
}

testAuth();
```

Run with: `node test-auth.js`

## Success Criteria

All tests should pass:
- ✅ User can register
- ✅ User can login
- ✅ Token stored in localStorage
- ✅ Session persists after refresh
- ✅ Protected routes require auth
- ✅ Admin routes require admin role
- ✅ Non-admin users see access denied
- ✅ Logout clears session
- ✅ Auto-redirect works
- ✅ Token sent with API requests
- ✅ Username and role displayed
- ✅ UI updates based on role

## Next Steps After Testing

1. Test with multiple users
2. Test concurrent sessions
3. Test token expiration (wait 24 hours)
4. Test on different browsers
5. Test on mobile devices
6. Load test with many requests
7. Security audit
8. Performance optimization
