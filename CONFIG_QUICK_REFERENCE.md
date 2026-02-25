# Configuration Quick Reference

## 🚀 Quick Start

### Run with Defaults (No Setup)
```bash
uvicorn main:app --reload
# Uses: public123 / admin123
```

### Run with Custom Config
```bash
export PUBLIC_API_KEY="my-key"
export ADMIN_API_KEY="my-admin"
uvicorn main:app --reload
```

### Run with Docker
```bash
docker-compose up -d
# Reads .env file automatically
```

---

## 📋 Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `PUBLIC_API_KEY` | `public123` | No | Public API key |
| `ADMIN_API_KEY` | `admin123` | No | Admin API key |
| `ALERT_EMAIL_ENABLED` | `false` | No | Enable email alerts |
| `SMTP_HOST` | `smtp.gmail.com` | No | SMTP server |
| `SMTP_PORT` | `587` | No | SMTP port |
| `SMTP_USER` | `` | Yes* | SMTP username |
| `SMTP_PASSWORD` | `` | Yes* | SMTP password |
| `ALERT_EMAIL_TO` | `admin@example.com` | No | Alert recipient |
| `ALERT_WEBHOOK_URL` | `` | No | Webhook URL |
| `DATABASE_URL` | `sqlite:///fraud.db` | No | Database URL |
| `HOST` | `0.0.0.0` | No | Server host |
| `PORT` | `8000` | No | Server port |
| `ENVIRONMENT` | `development` | No | Environment mode |

*Required only if `ALERT_EMAIL_ENABLED=true`

---

## 🔑 Generate Secure Keys

```bash
# Method 1: OpenSSL
openssl rand -hex 32

# Method 2: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Method 3: UUID
python -c "import uuid; print(str(uuid.uuid4()))"
```

---

## 📝 .env File Template

```bash
# Copy and customize
cp .env.example .env

# Edit .env
nano .env
```

**Minimal .env:**
```bash
PUBLIC_API_KEY=your-public-key
ADMIN_API_KEY=your-admin-key
```

**Full .env:**
```bash
ENVIRONMENT=production
PUBLIC_API_KEY=your-secure-key
ADMIN_API_KEY=your-admin-key
ALERT_EMAIL_ENABLED=true
SMTP_USER=alerts@company.com
SMTP_PASSWORD=your-password
ALERT_WEBHOOK_URL=https://webhook.com/alerts
DATABASE_URL=sqlite:///fraud.db
```

---

## 🐳 Docker Configuration

**Option 1: .env file**
```bash
# Create .env
# Run
docker-compose up -d
```

**Option 2: Inline**
```bash
PUBLIC_API_KEY=key1 ADMIN_API_KEY=key2 docker-compose up -d
```

**Option 3: docker-compose.yml**
```yaml
environment:
  - PUBLIC_API_KEY=your-key
  - ADMIN_API_KEY=your-admin
```

---

## ✅ Verify Configuration

```bash
# Check config endpoint
curl -H "X-API-KEY: admin123" http://localhost:8000/config

# Response shows:
# - Environment
# - Alert settings
# - Database type
# - Server settings
# (No sensitive data exposed)
```

---

## 🔧 Common Configurations

### Local Development
```bash
# No config needed - uses defaults
uvicorn main:app --reload
```

### Production
```bash
export ENVIRONMENT=production
export PUBLIC_API_KEY="$(openssl rand -hex 32)"
export ADMIN_API_KEY="$(openssl rand -hex 32)"
uvicorn main:app
```

### With Email Alerts
```bash
export ALERT_EMAIL_ENABLED=true
export SMTP_USER=alerts@gmail.com
export SMTP_PASSWORD=your-app-password
export ALERT_EMAIL_TO=admin@company.com
```

### With Webhook
```bash
export ALERT_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### PostgreSQL Database
```bash
export DATABASE_URL=postgresql://user:pass@localhost/fraud
```

---

## 🧪 Test Configuration

```bash
# Run test suite
python test_config.py

# Tests:
# ✓ Default values
# ✓ Environment loading
# ✓ Security integration
# ✓ Alert integration
```

---

## 🆘 Troubleshooting

### Config not loading?
```bash
# Check variable is set
echo $PUBLIC_API_KEY

# Check spelling (case-sensitive!)
env | grep API_KEY
```

### Still using defaults?
```bash
# Export variables
export PUBLIC_API_KEY="my-key"

# Restart app
uvicorn main:app --reload
```

### Docker not using .env?
```bash
# Check .env location
ls -la .env

# Rebuild
docker-compose up -d --build
```

---

## 📚 Documentation

- **Full Guide**: `CONFIGURATION.md`
- **Refactoring**: `REFACTORING_SUMMARY.md`
- **Deployment**: `DEPLOYMENT.md`
- **Quick Start**: `QUICKSTART.md`

---

## 🔒 Security Checklist

- [ ] Change default API keys
- [ ] Use strong random keys (32+ chars)
- [ ] Never commit .env to git
- [ ] Set file permissions: `chmod 600 .env`
- [ ] Rotate keys every 90 days
- [ ] Use different keys per environment
- [ ] Enable alerts in production
- [ ] Use HTTPS in production

---

**Quick Help:**
```bash
# View all environment variables
env

# View specific variable
echo $PUBLIC_API_KEY

# Set variable (Linux/Mac)
export KEY=value

# Set variable (Windows PowerShell)
$env:KEY="value"

# Unset variable
unset KEY
```

---

**Last Updated:** 2026-02-26
