# Authentication System Testing Guide

## Quick Start

### 1. Start the Backend
```bash
# From project root
uvicorn main:app --reload
```

### 2. Start the Frontend
```bash
# From frontend directory
npm start
```

### 3. Access the Application
Open browser to: `http://localhost:3000`

## Test Scenarios

### Scenario 1: User Login Flow
1. Navigate to `http://localhost:3000`
2. Should automatically redirect to `/login`
3. Enter credentials:
   - Username: `user`
   - Password: `user123`
4. Click "Login"
5. Should redirect to Dashboard
6. Verify:
   - ✅ Sidebar shows user badge with 👤 icon
   - ✅ Role badge shows "user"
   - ✅ No "Admin" link in sidebar
   - ✅ Dashboard loads successfully

### Scenario 2: Admin Login Flow
1. If logged in, click "Logout" button
2. Enter admin credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click "Login"
4. Verify:
   - ✅ Sidebar shows admin badge with 👑 icon
   - ✅ Role badge shows "admin"
   - ✅ "Admin" link visible in sidebar
   - ✅ Dashboard loads successfully

### Scenario 3: Invalid Credentials
1. Logout if logged in
2. Enter invalid credentials:
   - Username: `test`
   - Password: `wrong`
3. Click "Login"
4. Verify:
   - ✅ Error toast appears
   - ✅ Message: "Invalid credentials"
   - ✅ Stays on login page

### Scenario 4: Protected Routes (Not Logged In)
1. Logout if logged in
2. Try to access directly:
   - `http://localhost:3000/`
   - `http://localhost:3000/analyze`
   - `http://localhost:3000/admin`
3. Verify:
   - ✅ All redirect to `/login`

### Scenario 5: Admin Panel Access (User Role)
1. Login as user (`user` / `user123`)
2. Try to access: `http://localhost:3000/admin`
3. Verify:
   - ✅ Redirects to `/dashboard` (or `/`)
   - ✅ Cannot access admin panel

### Scenario 6: Admin Panel Access (Admin Role)
1. Login as admin (`admin` / `admin123`)
2. Click "Admin" link in sidebar
3. Verify Admin Panel displays:
   - ✅ System stats cards (Total Scans, High Risk, Critical Alerts, API Status)
   - ✅ API Key Management section
   - ✅ Recent Activity table with search and filter
   - ✅ Audit Log viewer

### Scenario 7: Analyze with Audit Logging
1. Login as any user
2. Navigate to "Analyze" page
3. Enter test data:
   - Phone: `+1234567890`
   - Message: `Click here to claim your prize!`
4. Click "Analyze Message"
5. Wait for results
6. Login as admin and go to Admin Panel
7. Check Audit Log
8. Verify:
   - ✅ ANALYZE action logged
   - ✅ Shows phone number and risk level
   - ✅ Timestamp is correct
   - ✅ Role is displayed

### Scenario 8: Activity Search and Filter
1. Login as admin
2. Go to Admin Panel
3. In Recent Activity section:
   - Enter phone number in search box
   - Select risk level from dropdown
4. Verify:
   - ✅ Table filters correctly
   - ✅ Search works for phone numbers
   - ✅ Filter works for risk levels
   - ✅ "No activity found" shows when no matches

### Scenario 9: API Key Regeneration
1. Login as admin
2. Go to Admin Panel
3. Note current API key (first 6 chars visible)
4. Click "Regenerate Key" button
5. Verify:
   - ✅ Success toast appears
   - ✅ API key changes
   - ✅ New key is masked

### Scenario 10: Logout Flow
1. Login as any user
2. Click "Logout" button in sidebar footer
3. Verify:
   - ✅ Redirects to `/login`
   - ✅ Sidebar disappears
   - ✅ Cannot access protected routes
   - ✅ Logout action logged in audit (check after re-login as admin)

### Scenario 11: Page Transitions
1. Login as admin
2. Navigate between pages:
   - Dashboard → Analyze → Admin → Dashboard
3. Verify:
   - ✅ Smooth fade-in animations
   - ✅ No flickering
   - ✅ Active link highlighted in sidebar

### Scenario 12: Responsive Design
1. Login as any user
2. Resize browser window to mobile size (< 768px)
3. Verify:
   - ✅ Sidebar collapses to icon-only
   - ✅ Text labels hidden
   - ✅ Icons remain visible
   - ✅ Logout button shows icon only
   - ✅ All pages remain functional

### Scenario 13: Session Persistence
1. Login as any user
2. Refresh the page (F5)
3. Verify:
   - ✅ Redirects to login (auth is in memory, not persisted)
   - ✅ This is expected behavior for security

### Scenario 14: Multiple Login Attempts
1. Try logging in with wrong credentials 3 times
2. Check audit log (login as admin after)
3. Verify:
   - ✅ All failed attempts are logged
   - ✅ Timestamps are correct

## Visual Checks

### Login Page
- [ ] Dark gradient background
- [ ] Centered login card with glassmorphism
- [ ] Shield icon (🛡️) at top
- [ ] Input fields have focus glow
- [ ] Login button has gradient
- [ ] Smooth hover animations

### Sidebar
- [ ] Dark gradient background
- [ ] Logo with glow effect
- [ ] User/Admin badge visible
- [ ] Active link highlighted
- [ ] Hover effects on links
- [ ] API status indicator (green dot)
- [ ] Logout button styled correctly

### Admin Panel
- [ ] 4 stat cards in grid
- [ ] Animated counters
- [ ] API key masked correctly
- [ ] Tables have dark theme
- [ ] Search and filter inputs styled
- [ ] Risk badges color-coded
- [ ] Audit log table formatted

## Performance Checks
- [ ] Login response < 100ms (simulated)
- [ ] Page transitions smooth (no lag)
- [ ] No console errors
- [ ] No memory leaks (check DevTools)
- [ ] Build completes successfully

## Browser Compatibility
Test in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

## Known Limitations
1. Auth token stored in memory (cleared on refresh)
2. Demo credentials hardcoded (no real backend auth)
3. API key regeneration is frontend-only simulation
4. Audit logs stored in sessionStorage (cleared on browser close)
5. No password reset functionality
6. No session timeout

## Success Criteria
✅ All 14 test scenarios pass
✅ All visual checks complete
✅ No console errors
✅ Build succeeds
✅ Responsive on mobile

## Troubleshooting

### Issue: Redirects to login after refresh
**Expected**: Auth is stored in memory for security, not persisted

### Issue: Admin panel shows "No activity found"
**Solution**: Run some analyses first from the Analyze page

### Issue: Audit log is empty
**Solution**: Perform some actions (login, analyze) to generate logs

### Issue: Build warnings about unused imports
**Expected**: Minor warnings in TrendChart.js (pre-existing, not related to auth)

## Next Steps After Testing
1. Document any bugs found
2. Test edge cases
3. Perform security review
4. Consider adding real backend authentication
5. Add automated tests (Jest, React Testing Library)
