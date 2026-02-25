# Deployment Guide - Cyber Fraud Detection System

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Environment Variables](#environment-variables)
4. [WebSocket Live Updates](#websocket-live-updates)
5. [Alert Configuration](#alert-configuration)
6. [ML Model Retraining](#ml-model-retraining)

---

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

4. **Access the application:**
- API: http://localhost:8000
- Admin Dashboard: http://localhost:8000/admin (requires admin API key)
- API Docs: http://localhost:8000/docs

---

## Docker Deployment

### Quick Start

1. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

2. **View logs:**
```bash
docker-compose logs -f fraud-api
```

3. **Stop the service:**
```bash
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t fraud-detection-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e PUBLIC_API_KEY=public123 \
  -e ADMIN_API_KEY=admin123 \
  --name fraud-api \
  fraud-detection-api
```

### Data Persistence

The Docker setup uses volumes to persist:
- **Database**: `./data/fraud.db`
- **Logs**: `./logs/fraud_logs.txt`
- **ML Model**: `./data/model.pkl`

---

## Environment Variables

### API Keys
```bash
PUBLIC_API_KEY=public123      # Key for /analyze endpoint
ADMIN_API_KEY=admin123        # Key for admin endpoints
```

### Email Alerts
```bash
ALERT_EMAIL_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_TO=admin@example.com
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password as SMTP_PASSWORD

### Webhook Alerts
```bash
ALERT_WEBHOOK_URL=https://your-webhook-url.com/alerts
```

**Webhook Payload Format:**
```json
{
  "alert_type": "critical_fraud",
  "phone_number": "555-1234",
  "risk_score": 95,
  "risk_level": "Critical",
  "threat_category": "Financial Scam",
  "primary_reason": "Contains threatening language",
  "action": "automatically_blacklisted"
}
```

---

## WebSocket Live Updates

The admin dashboard uses WebSocket for real-time updates.

### Connection
- **Endpoint**: `ws://localhost:8000/ws/dashboard`
- **Protocol**: WebSocket
- **Authentication**: Not required for WebSocket (admin page already protected)

### Message Format
```json
{
  "type": "update",
  "stats": {
    "total_requests": 150,
    "critical_count": 12,
    "high_count": 25,
    "blacklisted_count": 8
  },
  "latest_entry": {
    "phone_number": "555-1234",
    "risk_score": 95,
    "risk_level": "Critical",
    "threat_category": "Financial Scam",
    "confidence": 85,
    "timestamp": "2026-02-26 10:30:00"
  }
}
```

### Features
- Auto-reconnects on disconnect
- Updates stats cards in real-time
- Adds new entries to Recent Threats table
- No page refresh needed

---

## Alert Configuration

### When Alerts Trigger
Alerts are sent when:
- `risk_level == "Critical"`
- Phone number is automatically blacklisted

### Alert Types

#### 1. Email Alert
- Sent via SMTP
- Requires email configuration in environment
- Non-blocking (runs in background)

#### 2. Webhook Alert
- HTTP POST to configured URL
- JSON payload with fraud details
- 5-second timeout
- Non-blocking (runs in background)

### Testing Alerts

```bash
# Test with critical fraud message
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: public123" \
  -d '{
    "phone_number": "555-9999",
    "message_content": "URGENT! Your bank account suspended. Verify immediately or face legal action!"
  }'
```

---

## ML Model Retraining

### Endpoint
```
POST /retrain
```

### Authentication
Requires admin API key: `X-API-KEY: admin123`

### Request Format
```json
{
  "scam_messages": [
    "URGENT! Click here to claim your prize",
    "Your account will be closed. Verify now"
  ],
  "legitimate_messages": [
    "Hi, are we still meeting for lunch?",
    "Thanks for your help with the project"
  ]
}
```

### Response
```json
{
  "status": "Model retrained successfully",
  "new_training_samples": 4,
  "scam_samples": 2,
  "legitimate_samples": 2
}
```

### Example
```bash
curl -X POST "http://localhost:8000/retrain" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: admin123" \
  -d '{
    "scam_messages": [
      "URGENT! Your package is pending. Pay now!",
      "You won the lottery! Send your bank details"
    ],
    "legitimate_messages": [
      "Meeting rescheduled to 3 PM",
      "Great job on the presentation"
    ]
  }'
```

### Notes
- Model is saved to `model.pkl`
- Takes effect immediately
- Previous model is overwritten
- Recommended: Retrain with at least 10 samples per class

---

## Production Checklist

- [ ] Change default API keys
- [ ] Configure email alerts (if needed)
- [ ] Configure webhook alerts (if needed)
- [ ] Set up SSL/TLS (use reverse proxy like nginx)
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Regular database backups
- [ ] Test alert system
- [ ] Document custom configurations

---

## Troubleshooting

### WebSocket not connecting
- Check firewall allows WebSocket connections
- Verify server is running
- Check browser console for errors

### Alerts not sending
- Verify environment variables are set
- Check SMTP credentials (for email)
- Test webhook URL manually
- Check server logs for errors

### Docker container not starting
- Check logs: `docker-compose logs fraud-api`
- Verify port 8000 is available
- Check environment variables in docker-compose.yml

### Database locked error
- Stop all running instances
- Delete `fraud.db-journal` if exists
- Restart application

---

## Support

For issues or questions:
1. Check logs: `fraud_logs.txt` or `docker-compose logs`
2. Review API documentation: http://localhost:8000/docs
3. Verify environment configuration
