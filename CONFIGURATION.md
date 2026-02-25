# Configuration Guide

## Overview
The Cyber Fraud Detection System uses environment-based configuration for all settings. This allows for secure, flexible deployment across different environments without hardcoding secrets.

---

## Configuration Module

### config.py
Central configuration module that loads all settings from environment variables with sensible defaults for local development.

**Key Features:**
- ✅ Environment variable loading
- ✅ Type conversion (int, bool)
- ✅ Default fallback values
- ✅ Production mode detection
- ✅ Configuration summary (without secrets)

---

## Environment Variables

### API Keys

| Variable | Default (Dev) | Description |
|----------|---------------|-------------|
| `PUBLIC_API_KEY` | `public123` | API key for /analyze endpoint |
| `ADMIN_API_KEY` | `admin123` | API key for admin endpoints |

**Production:** Change these immediately!

### Email Alerts

| Variable | Default | Description |
|----------|---------|-------------|
| `ALERT_EMAIL_ENABLED` | `false` | Enable/disable email alerts |
| `SMTP_HOST` | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | `587` | SMTP server port |
| `SMTP_USER` | `` | SMTP username/email |
| `SMTP_PASSWORD` | `` | SMTP password/app password |
| `ALERT_EMAIL_TO` | `admin@example.com` | Alert recipient email |

### Webhook Alerts

| Variable | Default | Description |
|----------|---------|-------------|
| `ALERT_WEBHOOK_URL` | `` | Webhook URL for alerts |

### Database

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///fraud.db` | Database connection URL |

**Examples:**
- SQLite: `sqlite:///fraud.db`
- PostgreSQL: `postgresql://user:pass@localhost/dbname`
- MySQL: `mysql://user:pass@localhost/dbname`

### Server

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `ENVIRONMENT` | `development` | Environment mode |

---

## Configuration Methods

### Method 1: Environment Variables (Recommended for Production)

**Linux/Mac:**
```bash
export PUBLIC_API_KEY="your-secure-key-here"
export ADMIN_API_KEY="your-admin-key-here"
export ALERT_EMAIL_ENABLED="true"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

**Windows (PowerShell):**
```powershell
$env:PUBLIC_API_KEY="your-secure-key-here"
$env:ADMIN_API_KEY="your-admin-key-here"
$env:ALERT_EMAIL_ENABLED="true"
```

**Windows (CMD):**
```cmd
set PUBLIC_API_KEY=your-secure-key-here
set ADMIN_API_KEY=your-admin-key-here
set ALERT_EMAIL_ENABLED=true
```

### Method 2: .env File (Local Development)

1. **Create .env file:**
```bash
cp .env.example .env
```

2. **Edit .env:**
```bash
# .env
ENVIRONMENT=development
PUBLIC_API_KEY=my-public-key
ADMIN_API_KEY=my-admin-key
ALERT_EMAIL_ENABLED=true
SMTP_USER=myemail@gmail.com
SMTP_PASSWORD=mypassword
```

3. **Load .env (if using python-dotenv):**
```bash
pip install python-dotenv
```

Add to top of main.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Note:** The system works without .env file using defaults!

### Method 3: Docker Environment

**docker-compose.yml:**
```yaml
environment:
  - PUBLIC_API_KEY=your-key
  - ADMIN_API_KEY=your-admin-key
  - ALERT_EMAIL_ENABLED=true
```

**Or use .env file with Docker:**
```bash
# Docker automatically loads .env file
docker-compose up -d
```

---

## Usage Examples

### Local Development (No Configuration)

```bash
# Just run - uses defaults
uvicorn main:app --reload

# API keys: public123 / admin123
# No alerts enabled
# SQLite database: fraud.db
```

### Local Development (With Custom Config)

```bash
# Set environment variables
export PUBLIC_API_KEY="dev-public-key"
export ADMIN_API_KEY="dev-admin-key"

# Run
uvicorn main:app --reload
```

### Production Deployment

```bash
# Set production environment variables
export ENVIRONMENT=production
export PUBLIC_API_KEY="prod-secure-key-$(openssl rand -hex 16)"
export ADMIN_API_KEY="admin-secure-key-$(openssl rand -hex 16)"
export ALERT_EMAIL_ENABLED=true
export SMTP_USER="alerts@yourcompany.com"
export SMTP_PASSWORD="your-secure-password"
export ALERT_WEBHOOK_URL="https://your-webhook.com/alerts"

# Run
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Production

```bash
# Create .env file with production values
cat > .env << EOF
ENVIRONMENT=production
PUBLIC_API_KEY=your-secure-key
ADMIN_API_KEY=your-admin-key
ALERT_EMAIL_ENABLED=true
SMTP_USER=alerts@company.com
SMTP_PASSWORD=secure-password
ALERT_WEBHOOK_URL=https://webhook.com/alerts
DATABASE_URL=sqlite:////app/data/fraud.db
EOF

# Deploy
docker-compose up -d
```

---

## Configuration Verification

### Check Configuration (Admin Only)

```bash
curl -X GET "http://localhost:8000/config" \
  -H "X-API-KEY: admin123"
```

**Response:**
```json
{
  "status": "Configuration loaded successfully",
  "config": {
    "environment": "development",
    "alert_email_enabled": true,
    "alert_webhook_enabled": true,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "database_url": "sqlite:///***",
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

**Note:** Sensitive data (passwords, full paths) is hidden.

---

## Security Best Practices

### 1. Never Commit Secrets
```bash
# Add to .gitignore
.env
.env.local
.env.production
```

### 2. Use Strong Keys in Production
```bash
# Generate secure random keys
openssl rand -hex 32
# or
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Rotate Keys Regularly
- Change API keys every 90 days
- Update SMTP passwords when compromised
- Rotate webhook URLs if exposed

### 4. Use Environment-Specific Configs
```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

### 5. Restrict File Permissions
```bash
chmod 600 .env
```

---

## Configuration by Environment

### Development
```bash
ENVIRONMENT=development
PUBLIC_API_KEY=public123
ADMIN_API_KEY=admin123
ALERT_EMAIL_ENABLED=false
DATABASE_URL=sqlite:///fraud.db
```

### Staging
```bash
ENVIRONMENT=staging
PUBLIC_API_KEY=staging-public-key
ADMIN_API_KEY=staging-admin-key
ALERT_EMAIL_ENABLED=true
SMTP_USER=staging-alerts@company.com
DATABASE_URL=postgresql://user:pass@staging-db/fraud
```

### Production
```bash
ENVIRONMENT=production
PUBLIC_API_KEY=prod-secure-key-xyz
ADMIN_API_KEY=admin-secure-key-abc
ALERT_EMAIL_ENABLED=true
SMTP_USER=alerts@company.com
SMTP_PASSWORD=secure-password
ALERT_WEBHOOK_URL=https://monitoring.company.com/webhooks/fraud
DATABASE_URL=postgresql://user:pass@prod-db/fraud
```

---

## Troubleshooting

### Configuration Not Loading

**Problem:** Environment variables not being read

**Solutions:**
1. Check variable names (case-sensitive)
2. Restart application after setting variables
3. Verify variables are exported:
   ```bash
   echo $PUBLIC_API_KEY
   ```
4. Check for typos in variable names

### Default Values Being Used

**Problem:** Custom values not taking effect

**Solutions:**
1. Ensure variables are set before starting app
2. Check for spaces in variable assignments
3. Verify .env file is in correct location
4. Use `python -c "import os; print(os.getenv('PUBLIC_API_KEY'))"`

### Docker Environment Issues

**Problem:** Docker not using environment variables

**Solutions:**
1. Check docker-compose.yml syntax
2. Verify .env file is in same directory as docker-compose.yml
3. Rebuild container: `docker-compose up -d --build`
4. Check container environment: `docker exec fraud-detection-api env`

### Email Alerts Not Working

**Problem:** Emails not being sent

**Solutions:**
1. Verify `ALERT_EMAIL_ENABLED=true`
2. Check SMTP credentials
3. For Gmail: Use App Password, not regular password
4. Check SMTP port (587 for TLS, 465 for SSL)
5. Review server logs for error messages

---

## Migration from Hardcoded Values

### Before (Hardcoded)
```python
# security.py
PUBLIC_API_KEY = "public123"
ADMIN_API_KEY = "admin123"
```

### After (Environment-Based)
```python
# security.py
from config import config

# Use config.PUBLIC_API_KEY
# Use config.ADMIN_API_KEY
```

### Migration Steps
1. ✅ Create config.py
2. ✅ Update all modules to import config
3. ✅ Remove hardcoded values
4. ✅ Update docker-compose.yml
5. ✅ Create .env.example
6. ✅ Test with default values
7. ✅ Test with custom values
8. ✅ Deploy to production

---

## API Endpoints

### GET /config
Get configuration summary (admin only)

**Authentication:** Admin key required

**Response:**
```json
{
  "status": "Configuration loaded successfully",
  "config": {
    "environment": "production",
    "alert_email_enabled": true,
    "alert_webhook_enabled": true,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "database_url": "sqlite:///***",
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

---

## Summary

### ✅ Benefits
- **Security**: No secrets in source code
- **Flexibility**: Easy environment switching
- **Portability**: Works across platforms
- **Maintainability**: Central configuration
- **Docker-Ready**: Environment-based deployment

### 📁 Files Modified
- `config.py` - New configuration module
- `security.py` - Uses config for API keys
- `alert_service.py` - Uses config for alerts
- `database.py` - Uses config for database URL
- `main.py` - Imports config, adds /config endpoint
- `docker-compose.yml` - Updated environment variables
- `.env.example` - Updated template

### 🔒 Security Improvements
- ✅ No hardcoded secrets
- ✅ Environment-based configuration
- ✅ Production-ready defaults
- ✅ Configuration verification endpoint
- ✅ Sensitive data hidden in responses

---

**Last Updated:** 2026-02-26
**Version:** 2.0.0
