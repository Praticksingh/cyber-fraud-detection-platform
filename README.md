# Cyber Fraud Detection System

A comprehensive FastAPI-based fraud detection system with machine learning, rule-based analysis, and persistent SQLite database storage.

## Features

- Rule-based keyword detection (urgency, financial, threat keywords)
- Machine learning classification using Logistic Regression
- Phone number pattern analysis
- IP address analysis
- Blacklist checking
- Rate limiting
- SQLite database for persistent storage
- Automatic blacklisting of critical threats
- Historical analysis tracking
- **API Key Authentication** for secure access
- **Beautiful Admin Dashboard** with real-time statistics
- **WebSocket Live Updates** - Real-time dashboard updates
- **Alert System** - Email and webhook notifications for critical threats
- **ML Model Retraining** - Update model with new training data
- **Docker Support** - Easy deployment with Docker and Docker Compose

## Authentication

The API uses API key authentication via the `X-API-KEY` header.

### API Keys

- **Public Key**: `public123` - Access to `/analyze` endpoint
- **Admin Key**: `admin123` - Full access to all endpoints including admin dashboard

### Usage

Include the API key in your request headers:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: public123" \
  -d '{"phone_number": "555-1234", "message_content": "URGENT! Verify your account"}'
```

For admin endpoints:

```bash
curl -X GET "http://localhost:8000/stats" \
  -H "X-API-KEY: admin123"
```

### Error Responses

- **401 Unauthorized**: Missing API key
- **403 Forbidden**: Invalid API key or admin access required

## Installation

### Local Development

```bash
pip install -r requirements.txt
```

### Docker Deployment

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or build manually
docker build -t fraud-detection-api .
docker run -d -p 8000:8000 fraud-detection-api
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### GET /
Welcome endpoint with API information.
**Authentication**: None required

### GET /admin
**Admin Dashboard** - Beautiful web interface with:
- Real-time statistics (Total Requests, Critical, High, Blacklisted)
- Risk distribution chart
- Recent threats table (last 10)
- Blacklisted numbers table
- Dark-themed, modern UI

**Authentication**: Admin key required (`X-API-KEY: admin123`)

Visit `http://localhost:8000/admin` in your browser. You'll need to add the admin key to your browser request (use a browser extension or tool like Postman).

### POST /analyze
Analyze a message for fraud indicators.

**Authentication**: Public or Admin key required (`X-API-KEY: public123` or `admin123`)

**Request:**
```json
{
  "phone_number": "555-1234",
  "message_content": "URGENT! Your bank account has been suspended."
}
```

**Response:**
```json
{
  "risk_score": 95,
  "risk_level": "Critical",
  "confidence": 85,
  "explanation": "Critical risk. Contains threatening language: suspended",
  "primary_reason": "Contains threatening language: suspended",
  "contributing_factors": ["Urgency keywords: urgent", "Financial keywords: bank, account"],
  "recommendation": "CRITICAL THREAT. Do not engage. Block sender immediately and report to authorities",
  "threat_category": "Financial Scam"
}
```

### GET /history/{phone_number}
Get fraud analysis history for a specific phone number from database.

**Authentication**: Admin key required

### GET /stats
Get overall fraud detection statistics.

**Authentication**: Admin key required

**Response:**
```json
{
  "total_requests": 150,
  "critical_count": 12,
  "high_count": 25,
  "blacklisted_count": 8
}
```

### POST /retrain
Retrain the ML model with new training data.

**Authentication**: Admin key required

**Request:**
```json
{
  "scam_messages": ["URGENT! Verify now", "You won!"],
  "legitimate_messages": ["Meeting at 3pm", "Thanks!"]
}
```

**Response:**
```json
{
  "status": "Model retrained successfully",
  "new_training_samples": 4
}
```

### WebSocket /ws/dashboard
Real-time updates for admin dashboard. Broadcasts:
- Updated statistics
- Latest fraud log entries

**Authentication**: None (dashboard page is protected)

## Advanced Features

### Real-Time Dashboard Updates
The admin dashboard uses WebSocket for live updates:
- Stats update automatically when new analyses complete
- Recent threats table updates in real-time
- No page refresh needed

### Alert System
Critical threats trigger automatic alerts:
- **Email alerts** via SMTP (configurable)
- **Webhook alerts** via HTTP POST (configurable)
- Alerts sent in background (non-blocking)

Configure via environment variables:
```bash
ALERT_EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
ALERT_WEBHOOK_URL=https://your-webhook.com/alerts
```

### ML Model Retraining
Update the fraud detection model with new data:
```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "X-API-KEY: admin123" \
  -H "Content-Type: application/json" \
  -d '{"scam_messages": [...], "legitimate_messages": [...]}'
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker deployment guide
- Environment variable configuration
- Alert system setup
- Production checklist
- Troubleshooting guide

**Response:**
```json
{
  "total_blacklisted": 8,
  "blacklist": [
    {
      "id": 1,
      "phone_number": "555-0000",
      "reason": "Automatically blacklisted due to Critical risk",
      "added_at": "2026-02-26 10:30:00"
    }
  ]
}
```

## How It Works

The system uses a hybrid approach combining:

1. **Rule-based Detection**: Keyword matching for urgency, financial, and threat indicators
2. **Machine Learning**: TF-IDF + Logistic Regression classifier
3. **Phone Analysis**: Pattern detection (repeated digits, sequential patterns)
4. **IP Analysis**: Localhost and private network detection
5. **Blacklist Checking**: Known scam numbers and keywords
6. **Rate Limiting**: Tracks request frequency per phone number
7. **Historical Analysis**: Flags previously identified high-risk numbers

### Risk Scoring

- Rule-based score: 60% weight
- ML probability: 40% weight
- Additional adjustments for IP, blacklist, rate limiting, history
- Final score capped at 100

### Risk Levels

- 0-30: Low
- 31-60: Medium
- 61-85: High
- 86-100: Critical

### Automatic Blacklisting

Phone numbers flagged as "Critical" risk are automatically added to the database blacklist.

## Database

The system uses SQLite (`fraud.db`) with two tables:

- `fraud_logs`: Stores all fraud analysis results
- `blacklist`: Stores blacklisted phone numbers

Tables are automatically created on first run.

## Project Structure

```
.
├── main.py                 # FastAPI application
├── database.py             # SQLAlchemy database configuration
├── db_models.py            # Database table models
├── models.py               # Pydantic request/response models
├── detection_engine.py     # Keyword detection
├── risk_scorer.py          # Risk score calculation
├── explainable_ai.py       # Explanation generation
├── phone_analyzer.py       # Phone pattern analysis
├── ml_model.py             # Machine learning model
├── ip_analyzer.py          # IP address analysis
├── blacklist.py            # In-memory blacklist checker
├── rate_limiter.py         # Request rate limiting
├── logger.py               # File logging
├── history_store.py        # In-memory history
├── requirements.txt        # Python dependencies
├── fraud.db                # SQLite database (auto-created)
├── fraud_logs.txt          # Text log file (auto-created)
└── model.pkl               # Trained ML model (auto-created)
```
