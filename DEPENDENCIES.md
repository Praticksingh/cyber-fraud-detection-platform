# Dependencies Documentation

## Overview
This document explains all external dependencies used in the Cyber Fraud Detection System.

---

## Production Dependencies

### Web Framework
- **fastapi** (0.104.1)
  - Modern, fast web framework for building APIs
  - Used for: All API endpoints, routing, dependency injection
  - Files: `main.py`, `security.py`

- **uvicorn[standard]** (0.24.0)
  - ASGI server for running FastAPI
  - Includes WebSocket support
  - Used for: Running the application server
  - Command: `uvicorn main:app --reload`

### Database
- **sqlalchemy** (2.0.23)
  - SQL toolkit and ORM
  - Used for: Database operations, models, queries
  - Files: `database.py`, `db_models.py`, `main.py`
  - Database: SQLite (fraud.db)

### Machine Learning
- **scikit-learn** (1.3.2)
  - Machine learning library
  - Used for: Logistic Regression, TF-IDF vectorization
  - Files: `ml_model.py`
  - Components: TfidfVectorizer, LogisticRegression, Pipeline

- **joblib** (1.3.2)
  - Efficient serialization for Python objects
  - Used for: Saving/loading ML model (model.pkl)
  - Files: `ml_model.py`

### Templating
- **jinja2** (3.1.2)
  - Template engine for Python
  - Used for: Admin dashboard HTML rendering
  - Files: `main.py`, `templates/admin.html`

### HTTP Requests
- **requests** (2.31.0)
  - HTTP library for Python
  - Used for: Webhook alerts, external API calls
  - Files: `alert_service.py`, `test_api.py`, `test_advanced_features.py`

### WebSocket
- **websockets** (12.0)
  - WebSocket client and server library
  - Used for: Real-time dashboard updates
  - Files: `main.py`, `test_advanced_features.py`

### Data Validation
- **pydantic** (2.5.0)
  - Data validation using Python type annotations
  - Required by FastAPI, but listed explicitly
  - Used for: Request/response models
  - Files: `models.py`, `main.py`

---

## Standard Library Dependencies (No Installation Required)

These are built into Python and don't need to be installed:

- **datetime** - Date and time operations
- **json** - JSON encoding/decoding
- **os** - Operating system interface
- **smtplib** - SMTP protocol client
- **email** - Email message handling
- **time** - Time access and conversions
- **collections** - Container datatypes (defaultdict)
- **typing** - Type hints support
- **asyncio** - Asynchronous I/O

---

## Development/Testing Dependencies

These are only needed for testing (not in requirements.txt):

- **requests** - Already in production requirements
- **websockets** - Already in production requirements
- **asyncio** - Standard library

---

## Installation

### Standard Installation
```bash
pip install -r requirements.txt
```

### With Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation
Dependencies are automatically installed in the Docker image:
```bash
docker-compose up -d
```

---

## Version Compatibility

### Python Version
- **Minimum**: Python 3.11+
- **Recommended**: Python 3.11 or 3.12
- **Tested on**: Python 3.11

### Operating Systems
- ✅ Windows
- ✅ macOS
- ✅ Linux
- ✅ Docker (any platform)

---

## Dependency Tree

```
Cyber Fraud Detection System
├── fastapi (Web Framework)
│   ├── pydantic (Data validation)
│   ├── starlette (ASGI framework)
│   └── typing-extensions
├── uvicorn (ASGI Server)
│   ├── click
│   ├── h11
│   └── websockets (for WebSocket support)
├── sqlalchemy (Database ORM)
│   └── greenlet
├── scikit-learn (Machine Learning)
│   ├── numpy
│   ├── scipy
│   ├── joblib
│   └── threadpoolctl
├── jinja2 (Templating)
│   └── MarkupSafe
├── requests (HTTP Client)
│   ├── charset-normalizer
│   ├── idna
│   ├── urllib3
│   └── certifi
└── websockets (WebSocket Library)
```

---

## Security Considerations

### Package Security
- All packages are from PyPI (official Python package index)
- Versions are pinned for reproducibility
- Regular updates recommended for security patches

### Update Strategy
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all packages (test thoroughly)
pip install --upgrade -r requirements.txt
```

### Known Vulnerabilities
Check for vulnerabilities:
```bash
pip install safety
safety check
```

---

## Troubleshooting

### Installation Issues

**Problem**: `pip install` fails
```bash
# Solution 1: Upgrade pip
python -m pip install --upgrade pip

# Solution 2: Use --no-cache-dir
pip install --no-cache-dir -r requirements.txt

# Solution 3: Install one by one
pip install fastapi
pip install uvicorn[standard]
# ... etc
```

**Problem**: scikit-learn installation fails
```bash
# Solution: Install build tools
# Windows: Install Visual C++ Build Tools
# Mac: xcode-select --install
# Linux: sudo apt-get install python3-dev
```

**Problem**: WebSocket not working
```bash
# Ensure uvicorn[standard] is installed (not just uvicorn)
pip install uvicorn[standard]
```

---

## Minimal Installation (Core Only)

For minimal installation without optional features:

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
scikit-learn==1.3.2
joblib==1.3.2
pydantic==2.5.0
```

This excludes:
- jinja2 (no admin dashboard)
- requests (no webhook alerts)
- websockets (no real-time updates)

---

## Production Recommendations

### For Production Deployment
```bash
# Install with exact versions
pip install -r requirements.txt

# Freeze exact versions (including sub-dependencies)
pip freeze > requirements-lock.txt

# Use requirements-lock.txt for production
pip install -r requirements-lock.txt
```

### Performance Optimization
```bash
# Install with optimizations
pip install --no-cache-dir --compile -r requirements.txt

# Use production ASGI server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## License Information

All dependencies are open-source with permissive licenses:
- FastAPI: MIT
- Uvicorn: BSD
- SQLAlchemy: MIT
- scikit-learn: BSD
- joblib: BSD
- Jinja2: BSD
- requests: Apache 2.0
- websockets: BSD
- Pydantic: MIT

---

## Support

For dependency-related issues:
1. Check this documentation
2. Review package documentation:
   - FastAPI: https://fastapi.tiangolo.com/
   - SQLAlchemy: https://www.sqlalchemy.org/
   - scikit-learn: https://scikit-learn.org/
3. Check GitHub issues for each package
4. Ensure Python version compatibility

---

**Last Updated**: 2026-02-26
**Python Version**: 3.11+
**Total Dependencies**: 8 (production)
