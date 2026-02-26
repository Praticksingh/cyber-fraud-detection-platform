# Quick Reference Card

## 🚀 Start Commands

```bash
# Backend
uvicorn main:app --reload

# Frontend
cd frontend && npm start

# Docker
docker-compose up -d
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:8000/admin

## 🔑 Default API Keys

- **Public**: `public123`
- **Admin**: `admin123`

## 📡 Key Endpoints

### Public (No Auth)
```bash
GET  /analytics/summary
GET  /analytics/distribution
GET  /analytics/trends?days=30
GET  /graph?limit=100
```

### Authenticated (Public Key)
```bash
POST /analyze
  -H "X-API-KEY: public123"
  -d '{"phone_number": "+1234567890", "message_content": "..."}'
```

### Admin Only (Admin Key)
```bash
GET  /stats
GET  /history/{phone}
GET  /blacklist
POST /retrain
GET  /admin
```

## 🧪 Test Commands

```bash
# Backend tests
python test_api.py
python test_saas_platform.py

# Frontend tests
cd frontend && npm test
```

## 🐳 Docker Commands

```bash
# Build
docker build -t fraud-api .
cd frontend && docker build -t fraud-frontend .

# Run
docker run -p 8000:8000 fraud-api
docker run -p 80:80 fraud-frontend

# Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 📁 Important Files

### Configuration
- `.env` - Backend environment variables
- `frontend/.env` - Frontend environment variables
- `config.py` - Configuration loader

### Database
- `fraud.db` - SQLite database
- `model.pkl` - ML model

### Logs
- `fraud_logs.txt` - Text logs

## 🎨 Frontend Routes

- `/` - Dashboard
- `/analyze` - Analyze page

## 📊 Risk Levels

- **0-30**: Low (Green)
- **31-60**: Medium (Yellow)
- **61-85**: High (Orange)
- **86-100**: Critical (Red)

## 🔧 Environment Variables

### Backend
```bash
PUBLIC_API_KEY=public123
ADMIN_API_KEY=admin123
ALERT_EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_password
ALERT_WEBHOOK_URL=https://webhook.com
```

### Frontend
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=public123
```

## 🆘 Troubleshooting

### Port in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### CORS errors
- Check backend is running
- Verify REACT_APP_API_URL in frontend/.env
- Check CORS middleware in main.py

### Database locked
```bash
rm fraud.db-journal
```

### Module not found
```bash
pip install -r requirements.txt
```

### npm errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 Documentation

- **Getting Started**: GETTING_STARTED.md
- **Deployment**: DEPLOYMENT_GUIDE.md
- **Configuration**: CONFIGURATION.md
- **Production**: PRODUCTION_CHECKLIST.md
- **Upgrade Details**: UPGRADE_SUMMARY.md

## 🔍 Example API Call

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "X-API-KEY: public123" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "message_content": "URGENT! Your account has been suspended!"
  }'
```

## 📈 Graph Colors

- **Green**: Low risk (0-30)
- **Yellow**: Medium risk (31-70)
- **Red**: High risk (71-100)

## 🎯 Quick Tips

1. Always start backend before frontend
2. Check API docs at /docs for endpoint details
3. Use admin key for dashboard access
4. Graph updates after analyzing messages
5. Refresh dashboard to see latest data
6. Use filters to narrow down data
7. Drag graph nodes to explore relationships
8. Check browser console for errors

## 📞 Support

- Check logs in terminal
- Review API docs at /docs
- See troubleshooting in GETTING_STARTED.md
- Verify environment variables are set

---

**Quick Start**: `uvicorn main:app --reload` → `cd frontend && npm start` → Open http://localhost:3000
