# Deployment Guide - SaaS Fraud Detection Platform

Complete guide for deploying the full-stack fraud detection platform to production.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Full Stack Deployment](#full-stack-deployment)
5. [Production Checklist](#production-checklist)

---

## Quick Start

### Local Development

**Backend:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run backend
uvicorn main:app --reload
```

Backend available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

**Frontend:**
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env:
# REACT_APP_API_URL=http://localhost:8000
# REACT_APP_API_KEY=public123

# Run frontend
npm start
```

Frontend available at: `http://localhost:3000`

---

## Backend Deployment

### Option 1: Docker (Recommended)

**1. Build Docker image:**
```bash
docker build -t fraud-detection-api .
```

**2. Run container:**
```bash
docker run -d \
  -p 8000:8000 \
  -e PUBLIC_API_KEY=your_public_key \
  -e ADMIN_API_KEY=your_admin_key \
  -e ALERT_EMAIL_ENABLED=true \
  -e SMTP_SERVER=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your_email@gmail.com \
  -e SMTP_PASSWORD=your_app_password \
  -e ALERT_WEBHOOK_URL=https://your-webhook-url.com \
  -v $(pwd)/fraud.db:/app/fraud.db \
  --name fraud-api \
  fraud-detection-api
```

**3. Using Docker Compose:**
```bash
# Edit docker-compose.yml with your environment variables
docker-compose up -d
```

### Option 2: Cloud Platforms

#### AWS EC2

**1. Launch EC2 instance:**
- Ubuntu 22.04 LTS
- t2.medium or larger
- Open ports: 22 (SSH), 8000 (API)

**2. SSH into instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**3. Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

**4. Clone and setup:**
```bash
git clone your-repo-url
cd cyber-fraud-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Configure environment:**
```bash
cp .env.example .env
nano .env  # Edit with your values
```

**6. Run with Gunicorn:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**7. Setup systemd service:**
```bash
sudo nano /etc/systemd/system/fraud-api.service
```

```ini
[Unit]
Description=Fraud Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/cyber-fraud-system
Environment="PATH=/home/ubuntu/cyber-fraud-system/venv/bin"
EnvironmentFile=/home/ubuntu/cyber-fraud-system/.env
ExecStart=/home/ubuntu/cyber-fraud-system/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable fraud-api
sudo systemctl start fraud-api
sudo systemctl status fraud-api
```

#### DigitalOcean App Platform

**1. Create new app**
**2. Connect GitHub repository**
**3. Configure:**
- Build Command: `pip install -r requirements.txt`
- Run Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
**4. Add environment variables in dashboard**
**5. Deploy**

#### Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Set environment variables
heroku config:set PUBLIC_API_KEY=your_key
heroku config:set ADMIN_API_KEY=your_admin_key

# Deploy
git push heroku main
```

---

## Frontend Deployment

### Option 1: Netlify (Easiest)

**1. Build locally:**
```bash
cd frontend
npm run build
```

**2. Deploy:**
- Go to [netlify.com](https://netlify.com)
- Drag and drop `build/` folder
- Or connect GitHub repo

**3. Configure environment:**
- Site settings → Environment variables
- Add `REACT_APP_API_URL` and `REACT_APP_API_KEY`

**4. Configure redirects:**
Create `frontend/public/_redirects`:
```
/*    /index.html   200
```

### Option 2: Vercel

**1. Install Vercel CLI:**
```bash
npm install -g vercel
```

**2. Deploy:**
```bash
cd frontend
vercel
```

**3. Configure environment:**
```bash
vercel env add REACT_APP_API_URL
vercel env add REACT_APP_API_KEY
```

### Option 3: AWS S3 + CloudFront

**1. Build:**
```bash
cd frontend
npm run build
```

**2. Create S3 bucket:**
```bash
aws s3 mb s3://your-bucket-name
aws s3 sync build/ s3://your-bucket-name
```

**3. Configure bucket for static hosting:**
- Enable static website hosting
- Set index.html as index document
- Make bucket public

**4. Create CloudFront distribution:**
- Origin: S3 bucket
- Default root object: index.html
- Error pages: 404 → /index.html (for React Router)

### Option 4: Docker + Nginx

**1. Build Docker image:**
```bash
cd frontend
docker build -t fraud-detection-frontend .
```

**2. Run container:**
```bash
docker run -d -p 80:80 fraud-detection-frontend
```

**3. Or with environment variables:**
```bash
docker run -d \
  -p 80:80 \
  -e REACT_APP_API_URL=https://your-api-url.com \
  -e REACT_APP_API_KEY=your_key \
  fraud-detection-frontend
```

---

## Full Stack Deployment

### Option 1: Single Server with Docker Compose

**1. Create production docker-compose.yml:**
```yaml
version: '3.8'

services:
  fraud-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PUBLIC_API_KEY=${PUBLIC_API_KEY}
      - ADMIN_API_KEY=${ADMIN_API_KEY}
      - ALERT_EMAIL_ENABLED=${ALERT_EMAIL_ENABLED}
      - SMTP_SERVER=${SMTP_SERVER}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USERNAME=${SMTP_USERNAME}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - ALERT_WEBHOOK_URL=${ALERT_WEBHOOK_URL}
    volumes:
      - ./fraud.db:/app/fraud.db
      - ./model.pkl:/app/model.pkl
    restart: unless-stopped

  fraud-frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://your-domain.com:8000
      - REACT_APP_API_KEY=${PUBLIC_API_KEY}
    depends_on:
      - fraud-api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - fraud-api
      - fraud-frontend
    restart: unless-stopped
```

**2. Deploy:**
```bash
docker-compose up -d
```

### Option 2: Separate Deployments

**Backend:** Deploy to AWS EC2, DigitalOcean, or Heroku
**Frontend:** Deploy to Netlify, Vercel, or AWS S3

**Advantages:**
- Independent scaling
- Better separation of concerns
- Easier to manage

---

## Production Checklist

### Security

- [ ] Change default API keys
- [ ] Use strong, unique passwords
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for specific domains only
- [ ] Set up firewall rules
- [ ] Use environment variables for all secrets
- [ ] Enable rate limiting
- [ ] Set up API key rotation policy
- [ ] Review and restrict file permissions
- [ ] Enable security headers

### Database

- [ ] Migrate from SQLite to PostgreSQL for production
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Enable query logging
- [ ] Set up monitoring

### Monitoring

- [ ] Set up application monitoring (e.g., Sentry)
- [ ] Configure log aggregation (e.g., ELK stack)
- [ ] Set up uptime monitoring (e.g., UptimeRobot)
- [ ] Configure alerts for errors
- [ ] Monitor API response times
- [ ] Track resource usage

### Performance

- [ ] Enable gzip compression
- [ ] Configure caching headers
- [ ] Use CDN for frontend assets
- [ ] Optimize database queries
- [ ] Set up load balancing (if needed)
- [ ] Configure auto-scaling

### Backup

- [ ] Automated database backups
- [ ] Backup ML model files
- [ ] Backup configuration files
- [ ] Test restore procedures
- [ ] Document backup locations

### Documentation

- [ ] API documentation (Swagger/OpenAPI)
- [ ] Deployment procedures
- [ ] Incident response plan
- [ ] User guides
- [ ] Admin guides

---

## Environment Variables Reference

### Backend (.env)
```bash
# API Keys
PUBLIC_API_KEY=your_public_key_here
ADMIN_API_KEY=your_admin_key_here

# Email Alerts
ALERT_EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Webhook Alerts
ALERT_WEBHOOK_URL=https://your-webhook-url.com

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/fraud_db
```

### Frontend (.env)
```bash
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_API_KEY=your_public_key_here
```

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

**Database locked:**
```bash
# Stop all processes using database
# Delete fraud.db-journal if exists
rm fraud.db-journal
```

### Frontend Issues

**CORS errors:**
- Verify backend CORS configuration
- Check API URL in .env
- Ensure backend is running

**Build fails:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## Support

For issues or questions:
1. Check logs: `docker logs fraud-api` or `journalctl -u fraud-api`
2. Review API docs: `http://your-domain:8000/docs`
3. Check environment variables are set correctly
4. Verify network connectivity between services

---

## Next Steps

After deployment:
1. Test all endpoints
2. Run security audit
3. Set up monitoring dashboards
4. Configure automated backups
5. Document any custom configurations
6. Train team on system usage
7. Set up incident response procedures

---

**Congratulations!** Your SaaS Fraud Detection Platform is now deployed and ready for production use.
