# Local Development Fix - Connection Error

## Problem
When running the platform locally, you're seeing:
```
Cannot connect to server at https://cyber-fraud-api.onrender.com
Please ensure the backend is running on port 8000.
```

This means the frontend is trying to connect to the production URL instead of localhost.

## Root Cause
React's environment variables are cached. Even though `.env.development` is set correctly, the app might be using cached values or the wrong environment file.

## Solution

### Step 1: Stop the Frontend
Press `Ctrl+C` in the terminal where the frontend is running.

### Step 2: Clear React Cache
```bash
cd frontend
rm -rf node_modules/.cache
```

Or on Windows:
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules\.cache
```

### Step 3: Verify Environment Files

I've created/updated these files:

**frontend/.env** (for local development):
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=public123
```

**frontend/.env.development** (for npm start):
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=public123
```

**frontend/.env.production** (for npm build):
```
REACT_APP_API_URL=https://cyber-fraud-api.onrender.com
REACT_APP_API_KEY=public123
```

### Step 4: Restart Frontend
```bash
cd frontend
npm start
```

### Step 5: Verify Backend is Running

In another terminal:
```bash
# Check if backend is running
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Welcome to Cyber Fraud Detection System",
  "version": "2.0.0"
}
```

If backend is NOT running, start it:
```bash
# In the root directory
python main.py
```

Or use uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Quick Fix Commands

### Windows PowerShell:
```powershell
# Stop frontend (Ctrl+C first)
cd frontend
Remove-Item -Recurse -Force node_modules\.cache
npm start
```

### Linux/Mac:
```bash
# Stop frontend (Ctrl+C first)
cd frontend
rm -rf node_modules/.cache
npm start
```

## Verification

After restarting:

1. **Check Browser Console** (F12):
   - Should see API calls to `http://localhost:8000`
   - NOT to `https://cyber-fraud-api.onrender.com`

2. **Check Network Tab**:
   - API calls should go to localhost
   - Status should be 200/201 (not network error)

3. **Test Registration**:
   - Go to http://localhost:3000/register
   - Fill in the form
   - Should work without connection errors

## Environment Variable Priority

React uses environment files in this order:

1. `.env.local` (highest priority, not tracked in git)
2. `.env.development` or `.env.production` (based on NODE_ENV)
3. `.env` (default fallback)

For local development:
- `npm start` uses `.env.development`
- `npm run build` uses `.env.production`

## Alternative: Use .env.local

If the issue persists, create `.env.local` (this overrides everything):

```bash
cd frontend
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
echo "REACT_APP_API_KEY=public123" >> .env.local
```

Then restart the frontend.

## Troubleshooting

### Issue 1: Still connecting to production URL

**Solution:**
1. Stop frontend completely
2. Delete `.cache` folder
3. Check if there's a `.env.local` file with wrong URL
4. Restart frontend

### Issue 2: Backend not running

**Check:**
```bash
curl http://localhost:8000/
```

**Start backend:**
```bash
python main.py
```

Or:
```bash
uvicorn main:app --reload --port 8000
```

### Issue 3: Port 8000 already in use

**Find and kill process:**

Windows:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Linux/Mac:
```bash
lsof -i :8000
kill -9 <PID>
```

### Issue 4: Environment variables not loading

**Debug:**
1. Add this to `frontend/src/config/api.js`:
```javascript
console.log('API_BASE_URL:', process.env.REACT_APP_API_URL);
```

2. Check browser console
3. Should show `http://localhost:8000`

## Complete Restart Procedure

### Terminal 1 (Backend):
```bash
# In root directory
python main.py
```

Wait for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 (Frontend):
```bash
cd frontend
rm -rf node_modules/.cache  # Clear cache
npm start
```

Wait for:
```
Compiled successfully!
You can now view fraud-detection-frontend in the browser.
Local: http://localhost:3000
```

### Test:
1. Open http://localhost:3000
2. Go to /register
3. Try to register
4. Should work without connection errors

## Files Modified

✅ `frontend/.env` - Created for local development
✅ `frontend/.env.development` - Updated with comments
✅ `frontend/.env.production` - Updated with comments

## Summary

**Problem:** Frontend using production URL locally
**Cause:** Cached environment variables
**Solution:** Clear cache and restart frontend
**Result:** Frontend connects to localhost:8000

---

**Quick Fix:**
```bash
cd frontend
rm -rf node_modules/.cache
npm start
```

That's it! 🎉
