# Quick Start - Authentication System

## 🚀 Start the Application

### 1. Install Backend Dependencies
```bash
# Install authentication packages
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-multipart==0.0.6

# Or install all requirements
pip install -r requirements.txt
```

### 2. Start Backend
```bash
uvicorn main:app --reload
```

Backend will run on: `http://127.0.0.1:8000`

### 3. Start Frontend
```bash
cd frontend
npm start
```

Frontend will run on: `http://localhost:3000`

## 👤 First Time Setup

### Register Your First User
1. Navigate to `http://localhost:3000/register`
2. Fill in the registration form:
   - Username: your_username
   - Email: your@email.com
   - Password: (min 6 characters)
   - Confirm Password: (must match)
3. Click "Create Account"
4. You'll be redirected to login

### Login
1. Navigate to `http://localhost:3000/login`
2. Enter your credentials
3. Click "Sign In"
4. You'll be redirected to the dashboard

### Create Admin User (Optional)
After registering, make yourself admin:

```python
# Run this Python script
from database import SessionLocal
from db_models import User

db = SessionLocal()
user = db.query(User).filter(User.username == "your_username").first()
user.role = "admin"
db.commit()
print(f"User {user.username} is now an admin!")
```

Or create admin directly:
```python
from auth import create_user
from database import SessionLocal

db = SessionLocal()
admin = create_user(
    db=db,
    username="admin",
    email="admin@example.com",
    password="admin123",
    role="admin"
)
print(f"Admin created: {admin.username}")
```

## 🔑 API Endpoints

### Public Endpoints
- `POST /register` - Register new user
- `POST /login` - Login and get JWT token
- `POST /analyze` - Analyze fraud (API key)
- `GET /analytics/*` - Public analytics

### Protected Endpoints (JWT Required)
- `GET /history` - View all history
- `GET /stats` - View statistics

### Admin Endpoints (JWT + Admin Role)
- `GET /admin` - Admin dashboard
- `GET /blacklist` - Manage blacklist
- `POST /retrain` - Retrain ML model

## 📝 Example API Calls

### Register
```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "user",
  "username": "testuser"
}
```

### Access Protected Endpoint
```bash
curl -X GET http://127.0.0.1:8000/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🎯 User Flow

### New User
1. Visit `/register`
2. Create account
3. Redirected to `/login`
4. Login with credentials
5. Access dashboard

### Returning User
1. Visit `/login`
2. Enter credentials
3. Access dashboard
4. Token valid for 24 hours

### Logout
1. Click logout button in sidebar
2. Token cleared from memory
3. Redirected to login

## 🔒 Security Notes

- Passwords hashed with bcrypt
- JWT tokens expire after 24 hours
- Tokens stored in memory (not localStorage)
- Admin routes protected by role check
- All protected endpoints require valid JWT

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Invalid credentials" on login
- Check username and password
- Ensure user is registered
- Check backend logs for errors

### "401 Unauthorized" on API calls
- Token may have expired (24h)
- Login again to get new token
- Check Authorization header format

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check REACT_APP_API_BASE in frontend/.env
- Check CORS settings in main.py

## 📚 Documentation

- Full documentation: `AUTHENTICATION_BACKEND_INTEGRATION.md`
- API docs: `http://127.0.0.1:8000/docs`
- Alternative docs: `http://127.0.0.1:8000/redoc`

---

**Quick Links:**
- Register: `http://localhost:3000/register`
- Login: `http://localhost:3000/login`
- Dashboard: `http://localhost:3000/`
- API Docs: `http://127.0.0.1:8000/docs`
