# Getting Started - SaaS Fraud Detection Platform

Quick start guide to get your fraud detection platform up and running in minutes.

## Prerequisites

- Python 3.11+
- Node.js 16+
- npm or yarn
- Git

## Step 1: Backend Setup (5 minutes)

### 1.1 Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 1.2 Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred text editor
# Minimal configuration for local development:
# PUBLIC_API_KEY=public123
# ADMIN_API_KEY=admin123
```

### 1.3 Start Backend Server

```bash
# Run the FastAPI server
uvicorn main:app --reload
```

✅ Backend is now running at: `http://localhost:8000`
📚 API Documentation: `http://localhost:8000/docs`

## Step 2: Frontend Setup (5 minutes)

### 2.1 Install Node Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install
```

### 2.2 Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# The default values should work for local development:
# REACT_APP_API_URL=http://localhost:8000
# REACT_APP_API_KEY=public123
```

### 2.3 Start Frontend Server

```bash
# Start React development server
npm start
```

✅ Frontend is now running at: `http://localhost:3000`

## Step 3: Test the Platform (2 minutes)

### 3.1 Test Backend

Open your browser and visit:
- API Docs: `http://localhost:8000/docs`
- Root endpoint: `http://localhost:8000/`

Or use the test script:
```bash
# From project root
python test_saas_platform.py
```

### 3.2 Test Frontend

1. Open `http://localhost:3000` in your browser
2. You should see the Dashboard with:
   - Summary cards (may show 0 if no data yet)
   - Risk distribution chart
   - Trend chart
   - Knowledge graph

3. Click "Analyze" in the navigation
4. Enter a test message:
   ```
   Phone: +1234567890
   Message: URGENT! Your bank account has been compromised. Send $500 immediately!
   ```
5. Click "Analyze" button
6. View the results showing risk score, threat category, and recommendations

### 3.3 Verify Graph Integration

1. After analyzing a few messages, return to Dashboard
2. Scroll to the Knowledge Graph section
3. You should see nodes representing phone numbers
4. Drag nodes to explore relationships
5. Zoom in/out with mouse wheel

## Step 4: Explore Features

### Dashboard Features

- **Summary Cards**: Overview of total scans and risk levels
- **Risk Distribution**: Bar chart showing risk level breakdown
- **Trend Chart**: Line chart showing fraud detection over time
- **Knowledge Graph**: Interactive visualization of entity relationships
- **Filters**: Filter by risk level and time period
- **Graph Statistics**: Entity and connection counts

### Analyze Features

- **Phone Analysis**: Detect suspicious phone patterns
- **Message Analysis**: Identify fraud keywords and patterns
- **Risk Scoring**: 0-100 risk score with confidence level
- **Threat Categorization**: Financial Scam, Extortion, etc.
- **Explanations**: Detailed reasons for risk assessment
- **Recommendations**: Actionable next steps

## Common Commands

### Backend

```bash
# Start backend
uvicorn main:app --reload

# Run tests
python test_api.py
python test_saas_platform.py

# Check configuration
python -c "from config import config; print(config.get_config_summary())"
```

### Frontend

```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests (if configured)
npm test
```

### Docker

```bash
# Backend only
docker build -t fraud-api .
docker run -p 8000:8000 fraud-api

# Full stack
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### Backend won't start

**Issue**: Port 8000 already in use
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

**Issue**: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start

**Issue**: Port 3000 already in use
```bash
# Set different port
# Windows:
set PORT=3001 && npm start

# Linux/Mac:
PORT=3001 npm start
```

**Issue**: Dependencies error
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

**Issue**: Frontend can't connect to backend

1. Verify backend is running: `http://localhost:8000`
2. Check `.env` in frontend has correct `REACT_APP_API_URL`
3. Verify CORS is enabled in `main.py` (it should be by default)

### API Key Errors

**Issue**: 401 or 403 errors

1. Check `X-API-KEY` header is being sent
2. Verify API key matches between frontend `.env` and backend `.env`
3. Default keys: `public123` (public), `admin123` (admin)

## Next Steps

### For Development

1. **Customize Detection Rules**: Edit `detection_engine.py` to add custom fraud patterns
2. **Enhance ML Model**: Retrain with your own data using `/retrain` endpoint
3. **Add Custom Features**: Extend the platform with new endpoints and components
4. **Configure Alerts**: Set up email/webhook alerts in `.env`

### For Production

1. **Review Security**: See `PRODUCTION_CHECKLIST.md`
2. **Deploy Backend**: See `DEPLOYMENT_GUIDE.md` - Backend section
3. **Deploy Frontend**: See `DEPLOYMENT_GUIDE.md` - Frontend section
4. **Set Up Monitoring**: Configure logging and alerting
5. **Database Migration**: Move from SQLite to PostgreSQL

## Documentation

- **API Documentation**: `http://localhost:8000/docs` (when backend is running)
- **Configuration Guide**: `CONFIGURATION.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Production Checklist**: `PRODUCTION_CHECKLIST.md`
- **Upgrade Summary**: `UPGRADE_SUMMARY.md`
- **Dependencies**: `DEPENDENCIES.md`

## Sample API Requests

### Analyze a Message

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "X-API-KEY: public123" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "message_content": "URGENT! Your account has been compromised!"
  }'
```

### Get Analytics Summary

```bash
curl "http://localhost:8000/analytics/summary"
```

### Get Knowledge Graph

```bash
curl "http://localhost:8000/graph?limit=50"
```

### Get Statistics (Admin)

```bash
curl "http://localhost:8000/stats" \
  -H "X-API-KEY: admin123"
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs in terminal/console
3. Verify all prerequisites are installed
4. Check that ports 8000 and 3000 are available
5. Ensure environment variables are set correctly

## Success Checklist

- [ ] Backend running at `http://localhost:8000`
- [ ] Frontend running at `http://localhost:3000`
- [ ] Can access API docs at `http://localhost:8000/docs`
- [ ] Dashboard loads with charts
- [ ] Can analyze messages on Analyze page
- [ ] Results show risk score and recommendations
- [ ] Knowledge graph displays after analyzing messages
- [ ] No CORS errors in browser console

**Congratulations!** 🎉 Your SaaS Fraud Detection Platform is ready to use!

---

**Quick Links:**
- Dashboard: `http://localhost:3000`
- Analyze: `http://localhost:3000/analyze`
- API Docs: `http://localhost:8000/docs`
- Admin Dashboard: `http://localhost:8000/admin` (requires admin key)
