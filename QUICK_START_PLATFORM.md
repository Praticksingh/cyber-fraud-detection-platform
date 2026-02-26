# Quick Start Guide - Complete Platform

## Prerequisites
- Python 3.9+
- Node.js 14+
- npm or yarn

## Installation

### 1. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

Backend will run on `http://127.0.0.1:8000`

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## First Time Setup

### Create Admin User
```python
# Run this Python script
from database import SessionLocal
from auth import create_user

db = SessionLocal()
create_user(db, "admin", "admin@example.com", "AdminPass123!", "admin")
db.close()
print("Admin user created!")
```

### Create Regular User
Option 1: Use the registration page at `/register`

Option 2: Python script:
```python
from database import SessionLocal
from auth import create_user

db = SessionLocal()
create_user(db, "user1", "user@example.com", "UserPass123!", "user")
db.close()
print("User created!")
```

## Quick Tour

### 1. Login
- Go to `http://localhost:3000/login`
- Enter credentials
- Click "Sign In"

### 2. Dashboard
- View real-time analytics
- See fraud statistics
- Monitor trends
- Export reports (CSV/JSON/PDF)
- Auto-refreshes every 30 seconds

### 3. Analyze Messages
- Go to Analyze page
- Enter phone number and/or message
- Click "Analyze Message"
- View detailed XAI results:
  - Risk score
  - Why flagged
  - Contributing factors
  - Recommendations
  - Technical details

### 4. Admin Features (Admin Only)

**Admin Panel** (`/admin`):
- System statistics
- API key management
- Audit logs

**Blacklist Management** (`/admin/blacklist`):
- View blacklisted numbers
- Add new numbers
- Remove numbers
- Search/filter

## Key Features

### Explainable AI
- Detailed risk analysis
- Clear explanations
- Contributing factors
- Actionable recommendations

### Export Reports
- CSV format for spreadsheets
- JSON format for data processing
- PDF format for documents
- Automatic timestamps

### Blacklist Management
- Add/remove phone numbers
- Search functionality
- Audit trail
- Admin-only access

### Activity Logging
- All actions logged
- Timestamps recorded
- User tracking
- Audit compliance

## Common Tasks

### Analyze a Message
```
1. Go to /analyze
2. Enter: Phone: +1234567890
3. Enter: Message: "Congratulations! You won $1000!"
4. Click "Analyze Message"
5. View XAI results
```

### Export Dashboard Data
```
1. Go to /
2. Click "Export Report"
3. Select format (CSV/JSON/PDF)
4. File downloads automatically
```

### Add to Blacklist (Admin)
```
1. Go to /admin/blacklist
2. Click "Add to Blacklist"
3. Enter phone number
4. Enter reason
5. Click "Add to Blacklist"
```

### View Audit Logs (Admin)
```
1. Go to /admin
2. Scroll to "Audit Logs" section
3. View all user actions
```

## API Testing

### Test Analysis Endpoint
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: public123" \
  -d '{
    "phone_number": "+1234567890",
    "message_content": "Congratulations! You won $1000!"
  }'
```

### Test Login
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "AdminPass123!"
  }'
```

### Test Blacklist (with JWT)
```bash
TOKEN="your_jwt_token_here"

curl -X GET http://127.0.0.1:8000/blacklist \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### Backend Not Starting
```bash
# Check if port 8000 is in use
netstat -an | grep 8000

# Try different port
uvicorn main:app --port 8001
```

### Frontend Not Starting
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Try different port
PORT=3001 npm start
```

### Database Issues
```bash
# Delete and recreate database
rm fraud.db
python main.py
```

### Login Not Working
- Check JWT token in localStorage
- Verify backend is running
- Check browser console for errors
- Try clearing localStorage

### Export Not Working
- Check browser allows downloads
- Verify data exists
- Try different format
- Check console for errors

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-change-in-production
PUBLIC_API_KEY=public123
ADMIN_API_KEY=admin123
DATABASE_URL=sqlite:///./fraud.db
```

### Frontend (.env)
```env
REACT_APP_API_BASE=http://127.0.0.1:8000
REACT_APP_API_KEY=public123
```

## Default Credentials

### For Testing Only
```
Admin:
Username: admin
Password: AdminPass123!

User:
Username: user1
Password: UserPass123!
```

**⚠️ Change these in production!**

## Next Steps

1. ✅ Create admin user
2. ✅ Login to platform
3. ✅ Test analysis feature
4. ✅ View dashboard
5. ✅ Export a report
6. ✅ Add number to blacklist (admin)
7. ✅ Check audit logs (admin)
8. ✅ Test all features

## Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
# Build for production
npm run build

# Serve with nginx or similar
# Files in: frontend/build/
```

### Security Checklist
- [ ] Change JWT secret key
- [ ] Change API keys
- [ ] Use HTTPS
- [ ] Configure CORS properly
- [ ] Set up firewall
- [ ] Enable rate limiting
- [ ] Regular backups
- [ ] Monitor logs

## Support

### Documentation
- `PLATFORM_UPGRADE_COMPLETE.md` - Full feature documentation
- `JWT_AUTHENTICATION_IMPLEMENTATION.md` - Auth details
- `BCRYPT_FIX_SUMMARY.md` - Password hashing
- `AUTH_QUICK_REFERENCE.md` - Auth quick reference

### Common Issues
1. Port already in use → Change port
2. Module not found → Run `pip install -r requirements.txt`
3. CORS errors → Check backend CORS settings
4. 401 errors → Check JWT token
5. 403 errors → Check user role

### Getting Help
1. Check browser console
2. Check backend logs
3. Verify all services running
4. Review documentation
5. Check network tab in DevTools

## Success Criteria

Platform is working when:
- ✅ Backend responds on port 8000
- ✅ Frontend loads on port 3000
- ✅ Can login successfully
- ✅ Dashboard shows data
- ✅ Analysis works
- ✅ Export downloads files
- ✅ Blacklist management works (admin)
- ✅ No console errors

## Quick Commands

```bash
# Start everything
python main.py &
cd frontend && npm start

# Stop everything
pkill -f "python main.py"
pkill -f "npm start"

# Reset database
rm fraud.db
python main.py

# Clear frontend cache
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

**Platform Status**: ✅ Ready for Use
**Version**: 2.0.0
**Last Updated**: Current Session
