# SaaS AI Fraud Detection Platform 🛡️

A production-ready, full-stack fraud detection platform with AI-powered analysis, knowledge graph capabilities, and modern React dashboard. Built with FastAPI and React.

![Platform](https://img.shields.io/badge/Platform-SaaS-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Frontend](https://img.shields.io/badge/Frontend-React-blue)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

## 🚀 Quick Start

```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` for the dashboard!

📖 **Detailed Guide**: See [GETTING_STARTED.md](GETTING_STARTED.md)

## ✨ Features

### Core Detection
- ✅ AI-powered fraud detection with ML classification
- ✅ Rule-based keyword analysis (urgency, financial, threats)
- ✅ Phone number pattern analysis
- ✅ IP address analysis
- ✅ Blacklist checking with auto-blacklisting
- ✅ Rate limiting and historical tracking
- ✅ Confidence scoring and explainable AI

### SaaS Platform Features
- 🎯 **Knowledge Graph**: Entity relationship tracking with risk propagation
- 📊 **Analytics Dashboard**: Real-time metrics and visualizations
- 🔄 **Live Updates**: WebSocket-powered real-time dashboard
- 🚨 **Alert System**: Email and webhook notifications
- 🔐 **API Authentication**: Public and admin API keys
- 🎨 **Modern UI**: Dark-themed React dashboard
- 📈 **Trend Analysis**: Historical fraud detection patterns
- 🌐 **Interactive Graph**: D3.js force-directed visualization

### Production Ready
- 🐳 Docker support with Docker Compose
- 🔒 Environment-based configuration
- 💾 SQLite database with SQLAlchemy ORM
- 📝 Comprehensive logging and monitoring
- 🔄 ML model retraining endpoint
- 📚 Auto-generated API documentation

## 🖥️ Platform Overview

### Dashboard
![Dashboard Features](https://via.placeholder.com/800x400/1a1f3a/ffffff?text=Dashboard+with+Analytics+%26+Knowledge+Graph)

- **Summary Cards**: Total scans, risk level breakdown
- **Risk Distribution**: Visual breakdown of threat levels
- **Trend Charts**: 30-day fraud detection patterns
- **Knowledge Graph**: Interactive entity relationship visualization
- **Filters**: Risk level and time period filtering

### Analyze Page
![Analyze Features](https://via.placeholder.com/800x400/1a1f3a/ffffff?text=Real-time+Fraud+Analysis)

- **Input Form**: Phone number and message analysis
- **Risk Scoring**: 0-100 score with confidence level
- **Threat Categorization**: Financial Scam, Extortion, etc.
- **Detailed Explanations**: Contributing factors and recommendations
- **Real-time Results**: Instant analysis with visual feedback

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  Dashboard | Analyze | Charts | Knowledge Graph             │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST API + WebSocket
┌─────────────────────▼───────────────────────────────────────┐
│                   FastAPI Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Detection   │  │  ML Model    │  │  Knowledge   │     │
│  │  Engine      │  │  (Sklearn)   │  │  Graph       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Risk        │  │  Alert       │  │  Analytics   │     │
│  │  Scorer      │  │  Service     │  │  Engine      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              SQLite Database                                │
│  fraud_logs | blacklist | graph_entities                   │
└─────────────────────────────────────────────────────────────┘
```

## 📡 API Endpoints

### Public Endpoints (No Auth)
- `GET /` - Welcome and API info
- `GET /analytics/summary` - Dashboard summary
- `GET /analytics/distribution` - Risk distribution
- `GET /analytics/trends` - Fraud trends over time
- `GET /graph` - Knowledge graph data

### Authenticated Endpoints
- `POST /analyze` - Analyze message (Public key)
- `GET /stats` - Statistics (Admin key)
- `GET /history/{phone}` - Analysis history (Admin key)
- `GET /blacklist` - Blacklist entries (Admin key)
- `POST /retrain` - Retrain ML model (Admin key)
- `GET /admin` - Admin dashboard (Admin key)
- `WS /ws/dashboard` - Live updates (WebSocket)

📚 **Full API Docs**: `http://localhost:8000/docs`

## 🔧 Configuration

### Backend (.env)
```bash
# API Keys
PUBLIC_API_KEY=public123
ADMIN_API_KEY=admin123

# Email Alerts
ALERT_EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Webhook Alerts
ALERT_WEBHOOK_URL=https://your-webhook-url.com
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=public123
```

📖 **Configuration Guide**: See [CONFIGURATION.md](CONFIGURATION.md)

## 🐳 Docker Deployment

```bash
# Full stack with Docker Compose
docker-compose up -d

# Backend only
docker build -t fraud-api .
docker run -p 8000:8000 fraud-api

# Frontend only
cd frontend
docker build -t fraud-frontend .
docker run -p 80:80 fraud-frontend
```

📖 **Deployment Guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🧪 Testing

```bash
# Test backend API
python test_api.py

# Test SaaS features
python test_saas_platform.py

# Test configuration
python test_config.py

# Frontend tests
cd frontend
npm test
```

## 📊 Example Usage

### Analyze a Message

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "X-API-KEY: public123" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "message_content": "URGENT! Your bank account has been compromised. Send $500 immediately!"
  }'
```

### Response

```json
{
  "risk_score": 95,
  "risk_level": "Critical",
  "confidence": 85,
  "threat_category": "Financial Scam",
  "primary_reason": "Contains threatening language and urgency indicators",
  "contributing_factors": [
    "Urgency keywords: urgent, immediately",
    "Financial keywords: bank, account",
    "Threat keywords: compromised"
  ],
  "recommendation": "CRITICAL THREAT. Do not engage. Block sender immediately and report to authorities"
}
```

## 📁 Project Structure

```
cyber-fraud-system/
├── Backend (FastAPI)
│   ├── main.py                    # FastAPI application
│   ├── detection_engine.py        # Fraud detection logic
│   ├── risk_scorer.py             # Risk calculation
│   ├── explainable_ai.py          # Explanation generation
│   ├── graph_service.py           # Knowledge graph
│   ├── ml_model.py                # ML classifier
│   ├── alert_service.py           # Alert notifications
│   ├── database.py                # Database config
│   ├── db_models.py               # SQLAlchemy models
│   ├── security.py                # Authentication
│   └── config.py                  # Configuration
│
├── Frontend (React)
│   ├── src/
│   │   ├── components/            # Reusable components
│   │   │   ├── Navbar.js
│   │   │   ├── SummaryCards.js
│   │   │   ├── RiskDistributionChart.js
│   │   │   ├── TrendChart.js
│   │   │   ├── GraphView.js
│   │   │   └── FiltersPanel.js
│   │   ├── pages/                 # Page components
│   │   │   ├── Dashboard.js
│   │   │   └── Analyze.js
│   │   ├── services/              # API services
│   │   │   └── api.js
│   │   └── App.js                 # Main app
│   ├── package.json
│   └── Dockerfile
│
├── Documentation
│   ├── README.md                  # This file
│   ├── GETTING_STARTED.md         # Quick start guide
│   ├── DEPLOYMENT_GUIDE.md        # Deployment instructions
│   ├── CONFIGURATION.md           # Configuration details
│   ├── UPGRADE_SUMMARY.md         # SaaS upgrade details
│   └── PRODUCTION_CHECKLIST.md    # Production readiness
│
├── Docker
│   ├── Dockerfile                 # Backend container
│   ├── docker-compose.yml         # Full stack orchestration
│   └── .dockerignore
│
└── Tests
    ├── test_api.py                # API tests
    ├── test_saas_platform.py      # SaaS feature tests
    └── test_config.py             # Configuration tests
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Scikit-learn** - Machine learning
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Recharts** - Chart library
- **D3.js** - Graph visualization

### Infrastructure
- **Docker** - Containerization
- **SQLite** - Database (PostgreSQL-ready)
- **Nginx** - Frontend serving

## 📈 Risk Scoring Algorithm

```
Final Score = (Rule-based Score × 0.6) + (ML Probability × 40)
            + IP Risk Adjustment
            + Blacklist Boost
            + Rate Limit Boost
            + Historical Risk Boost
            (capped at 100)

Risk Levels:
- 0-30:   Low
- 31-60:  Medium
- 61-85:  High
- 86-100: Critical
```

## 🔐 Security Features

- API key authentication (public + admin)
- Environment-based secrets management
- CORS configuration
- Rate limiting
- Input validation with Pydantic
- SQL injection protection (SQLAlchemy)
- XSS protection (React)

## 📚 Documentation

- [Getting Started Guide](GETTING_STARTED.md) - Setup in 10 minutes
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment
- [Configuration Guide](CONFIGURATION.md) - Environment variables
- [Production Checklist](PRODUCTION_CHECKLIST.md) - Pre-launch checklist
- [Upgrade Summary](UPGRADE_SUMMARY.md) - SaaS platform features
- [Dependencies](DEPENDENCIES.md) - Package information

## 🤝 Contributing

This is a production-ready fraud detection platform. To extend:

1. **Add Detection Rules**: Edit `detection_engine.py`
2. **Enhance ML Model**: Update `ml_model.py`
3. **Add Endpoints**: Extend `main.py`
4. **Add UI Components**: Create in `frontend/src/components/`
5. **Add Analytics**: Extend graph service and analytics endpoints

## 📝 License

This project is provided as-is for fraud detection purposes.

## 🆘 Support

- **Issues**: Check [GETTING_STARTED.md](GETTING_STARTED.md) troubleshooting
- **API Docs**: `http://localhost:8000/docs`
- **Configuration**: See [CONFIGURATION.md](CONFIGURATION.md)
- **Deployment**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🎯 Roadmap

- [ ] PostgreSQL support
- [ ] Neo4j integration for knowledge graph
- [ ] User authentication and multi-tenancy
- [ ] Advanced ML models (BERT, transformers)
- [ ] Real-time streaming analysis
- [ ] Mobile app
- [ ] Advanced reporting and exports
- [ ] Integration with external threat intelligence

## ⭐ Key Highlights

- **Production Ready**: Docker, environment config, comprehensive docs
- **Full Stack**: Complete backend + frontend solution
- **Modern Tech**: FastAPI, React, D3.js, SQLAlchemy
- **AI Powered**: ML classification + rule-based detection
- **Scalable**: Knowledge graph, analytics, real-time updates
- **Secure**: API authentication, input validation, CORS
- **Documented**: Extensive guides and API documentation

---

**Built with ❤️ for fraud prevention**

🚀 **Get Started**: [GETTING_STARTED.md](GETTING_STARTED.md)
📖 **Deploy**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
🔧 **Configure**: [CONFIGURATION.md](CONFIGURATION.md)
