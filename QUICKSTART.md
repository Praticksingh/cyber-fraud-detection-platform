# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Local Development (Fastest)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload

# 3. Open admin dashboard
# Visit: http://localhost:8000/admin
# Add header: X-API-KEY: admin123
```

### Option 2: Docker (Production-Ready)

```bash
# 1. Start with Docker Compose
docker-compose up -d

# 2. Check logs
docker-compose logs -f

# 3. Access the API
# http://localhost:8000
```

---

## 📝 First API Call

```bash
# Analyze a suspicious message
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: public123" \
  -d '{
    "phone_number": "555-1234",
    "message_content": "URGENT! Your bank account is suspended. Verify now!"
  }'
```

**Response:**
```json
{
  "risk_score": 85,
  "risk_level": "High",
  "confidence": 65,
  "threat_category": "Financial Scam",
  "explanation": "High risk. Combines financial requests with urgency tactics",
  "recommendation": "High risk of fraud. Do not respond or click any links."
}
```

---

## 🎯 Key Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | None | Welcome & API info |
| `/analyze` | POST | Public/Admin | Analyze message |
| `/admin` | GET | Admin | Dashboard UI |
| `/stats` | GET | Admin | Statistics |
| `/blacklist` | GET | Admin | Blacklisted numbers |
| `/retrain` | POST | Admin | Retrain ML model |
| `/ws/dashboard` | WS | None | Live updates |

---

## 🔑 API Keys

- **Public Key**: `public123` - For `/analyze` endpoint
- **Admin Key**: `admin123` - For all admin endpoints

**Usage:**
```bash
-H "X-API-KEY: public123"  # Public access
-H "X-API-KEY: admin123"   # Admin access
```

---

## 📊 Admin Dashboard

1. **Access**: http://localhost:8000/admin
2. **Auth**: Add header `X-API-KEY: admin123`
3. **Features**:
   - Real-time statistics
   - Risk distribution chart
   - Recent threats table
   - Blacklisted numbers
   - Live WebSocket updates

**Tip**: Use a browser extension like "ModHeader" to add the API key header.

---

## 🔔 Enable Alerts (Optional)

### Email Alerts

```bash
# Create .env file
cat > .env << EOF
ALERT_EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_TO=admin@example.com
EOF

# Restart server
uvicorn main:app --reload
```

### Webhook Alerts

```bash
# Add to .env
echo "ALERT_WEBHOOK_URL=https://your-webhook.com/alerts" >> .env

# Restart server
```

---

## 🧠 Retrain ML Model

```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: admin123" \
  -d '{
    "scam_messages": [
      "URGENT! Click here to claim your prize",
      "Your account will be closed. Verify now"
    ],
    "legitimate_messages": [
      "Hi, are we still meeting for lunch?",
      "Thanks for your help with the project"
    ]
  }'
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f fraud-api

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Access container shell
docker exec -it fraud-detection-api bash
```

---

## 🧪 Test the System

```bash
# Run test script
python test_api.py
```

This will test:
- ✅ Authentication (missing, invalid, valid keys)
- ✅ Public endpoint access
- ✅ Admin endpoint access
- ✅ Fraud analysis
- ✅ Statistics retrieval

---

## 📁 Project Structure

```
.
├── main.py                 # FastAPI application
├── database.py             # SQLAlchemy setup
├── db_models.py            # Database models
├── security.py             # API key authentication
├── alert_service.py        # Email & webhook alerts
├── ml_model.py             # ML model (Logistic Regression)
├── detection_engine.py     # Keyword detection
├── risk_scorer.py          # Risk calculation
├── explainable_ai.py       # Explanation generation
├── templates/
│   └── admin.html          # Admin dashboard
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker Compose config
├── requirements.txt        # Python dependencies
└── .env.example            # Environment template
```

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --port 8001
```

### Database locked
```bash
# Stop all instances
pkill -f uvicorn

# Remove lock file
rm fraud.db-journal

# Restart
uvicorn main:app --reload
```

### WebSocket not connecting
- Check browser console for errors
- Verify server is running
- Try refreshing the page

### Alerts not sending
- Check `.env` file exists and has correct values
- Verify SMTP credentials (for email)
- Test webhook URL manually
- Check server logs for errors

---

## 📚 Next Steps

1. **Customize API Keys**: Change default keys in `.env`
2. **Configure Alerts**: Set up email/webhook notifications
3. **Add Training Data**: Retrain model with your data
4. **Deploy to Production**: Use Docker Compose with SSL
5. **Monitor Logs**: Check `fraud_logs.txt` regularly

---

## 🆘 Need Help?

- **API Docs**: http://localhost:8000/docs
- **Deployment Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Full README**: See [README.md](README.md)

---

**Happy Fraud Detection! 🛡️**
