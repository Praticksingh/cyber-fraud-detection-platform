# Production Deployment Guide - Render + Vercel

## Current Status

✅ **Backend (Render)**: Configured and ready
✅ **Frontend (Vercel)**: Code ready, needs environment variable setup
✅ **CORS**: Properly configured to allow all origins
✅ **API Configuration**: Centralized and environment-aware

---

## Issue: Login/Registration Not Working

### Root Cause
Your Vercel frontend doesn't have the environment variable set, so it's trying to connect to `http://localhost:8000` instead of your Render backend at `https://cyber-fraud-api.onrender.com`.

---

## SOLUTION: Set Vercel Environment Variable

### Step 1: Go to Vercel Dashboard

1. Open: https://vercel.com/dashboard
2. Click on your project (cyber-fraud-detection-platform)
3. Click **Settings** tab
4. Click **Environment Variables** in the left sidebar

### Step 2: Add Environment Variable

Click **"Add New"** and enter:

```
Name: REACT_APP_API_URL
Value: https://cyber-fraud-api.onrender.com
```

**Important**: Select ALL environments:
- ✅ Production
- ✅ Preview  
- ✅ Development

Click **Save**

### Step 3: Redeploy Frontend

After adding the environment variable, you MUST redeploy:

**Option A - Automatic (Recommended)**:
```bash
git commit --allow-empty -m "Trigger Vercel redeploy"
git push origin main
```

**Option B - Manual**:
1. Go to Vercel Dashboard → Deployments
2. Click "..." on the latest deployment
3. Click "Redeploy"
4. Wait for deployment to complete

### Step 4: Test the Connection

1. Open your Vercel URL
2. Press F12 (open Developer Tools)
3. Go to Console tab
4. Try to register a new user
5. Check Network tab - API calls should go to `https://cyber-fraud-api.onrender.com`

---

## Verification Checklist

### Backend (Render) ✅
- [x] CORS configured to allow all origins
- [x] Service is running
- [x] URL: `https://cyber-fraud-api.onrender.com`

Test backend:
```bash
curl https://cyber-fraud-api.onrender.com/
```

Expected response:
```json
{
  "message": "Welcome to Cyber Fraud Detection System",
  "version": "2.0.0"
}
```

### Frontend (Vercel) - Action Required
- [ ] Set `REACT_APP_API_URL` environment variable
- [ ] Redeploy after setting variable
- [ ] Test registration/login

---

## Database Management Features

Yes! Your project has comprehensive database management:

### 1. Command-Line Tool: `manage_users.py`

**List all users:**
```bash
python manage_users.py list
```

**Delete user by username:**
```bash
python manage_users.py delete <username>
```

**Delete user by email:**
```bash
python manage_users.py delete-email <email>
```

**Create admin user:**
```bash
python manage_users.py create-admin <username> <email> <password>
```

**Clear all users (careful!):**
```bash
python manage_users.py clear-all
```

### 2. Admin Panel (Web UI)

Access at: `https://your-vercel-url.vercel.app/admin`

**Features:**
- View system statistics (total scans, high risk count, critical alerts)
- Monitor recent activity
- Search and filter fraud logs
- View audit logs
- API key management
- Real-time API status

**Requirements:**
- Must be logged in as admin user
- Admin role required (set via `manage_users.py`)

### 3. Blacklist Management

Access at: `https://your-vercel-url.vercel.app/blacklist`

**Features:**
- View all blacklisted phone numbers
- Add new numbers to blacklist
- Remove numbers from blacklist
- See blacklist reasons and timestamps

**Requirements:**
- Admin role required

### 4. Database Tables

Your project manages three main tables:

**Users Table:**
- id, username, email, hashed_password, role, created_at
- Stores user accounts (regular users and admins)

**Fraud Logs Table:**
- id, phone_number, risk_score, risk_level, threat_category, confidence, timestamp
- Stores all fraud analysis results

**Blacklist Table:**
- id, phone_number, reason, added_at
- Stores blacklisted phone numbers

---

## Quick Start After Environment Variable Setup

### 1. Create Admin User (Backend)

```bash
python manage_users.py create-admin admin admin@example.com Admin@123
```

### 2. Test Registration (Frontend)

1. Go to your Vercel URL
2. Click "Register"
3. Fill in:
   - Username: testuser
   - Email: test@example.com
   - Password: Test@1234
4. Click "Create Account"
5. Should see success message

### 3. Login as Admin

1. Go to your Vercel URL
2. Click "Login"
3. Enter admin credentials
4. Should redirect to dashboard

### 4. Access Admin Panel

1. Click "Admin Panel" in navigation
2. View system statistics
3. Monitor recent activity
4. Manage blacklist

---

## Troubleshooting

### Issue: Still getting "Network Error"

**Check 1: Environment Variable**
```bash
# In Vercel dashboard, verify:
REACT_APP_API_URL = https://cyber-fraud-api.onrender.com
```

**Check 2: Redeployed?**
- Environment variables only take effect after redeployment
- Check Vercel Deployments tab for latest deployment

**Check 3: Browser Console**
- Press F12
- Go to Network tab
- Check if API calls go to correct URL
- Look for CORS errors

### Issue: Backend not responding

**Check Render Service:**
1. Go to Render dashboard
2. Check if service is "Live" (green dot)
3. Check logs for errors
4. Verify URL is accessible

**Test directly:**
```bash
curl https://cyber-fraud-api.onrender.com/
```

### Issue: CORS Error

Backend is already configured to allow all origins. If you still see CORS errors:

1. Check Render logs for errors
2. Verify backend is running
3. Try in incognito mode (clear cache)

### Issue: 401 Unauthorized

This is actually good - means connection works!
- Just need to register/login with correct credentials

---

## Environment Variables Reference

### Vercel (Frontend)
```
REACT_APP_API_URL=https://cyber-fraud-api.onrender.com
REACT_APP_API_KEY=public123
```

### Render (Backend)
```
DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
FRONTEND_URL=https://your-vercel-url.vercel.app (optional)
```

---

## Testing Checklist

After setting up environment variables:

- [ ] Backend responds at `https://cyber-fraud-api.onrender.com`
- [ ] Frontend deployed on Vercel
- [ ] Environment variable `REACT_APP_API_URL` is set
- [ ] Frontend redeployed after setting variable
- [ ] Registration works (no network error)
- [ ] Login works (redirects to dashboard)
- [ ] Admin panel accessible (for admin users)
- [ ] Blacklist management works
- [ ] Fraud analysis works
- [ ] No CORS errors in browser console

---

## Summary

**What's Working:**
✅ Backend CORS configuration
✅ Frontend API configuration code
✅ Database management tools
✅ Admin panel UI
✅ Blacklist management UI

**What You Need to Do:**
1. Set `REACT_APP_API_URL` in Vercel environment variables
2. Redeploy frontend on Vercel
3. Test registration and login
4. Create admin user using `manage_users.py`
5. Access admin panel and blacklist management

**Expected Result:**
🎉 Login and registration will work perfectly!

---

## Support Commands

**Test backend health:**
```bash
curl https://cyber-fraud-api.onrender.com/
```

**Test registration:**
```bash
curl -X POST https://cyber-fraud-api.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test@1234"}'
```

**List users:**
```bash
python manage_users.py list
```

**Create admin:**
```bash
python manage_users.py create-admin admin admin@example.com Admin@123
```

---

**Last Updated**: Context Transfer
**Status**: Ready for deployment - just needs Vercel environment variable
