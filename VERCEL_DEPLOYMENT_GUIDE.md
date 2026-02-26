# Vercel Deployment Guide

## Overview
This guide covers deploying the FraudGuard AI frontend to Vercel with proper environment configuration.

## Environment Configuration

### Environment Files Created

1. **`.env.development`** - Local development
   ```env
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_API_KEY=public123
   ```

2. **`.env.production`** - Production deployment
   ```env
   REACT_APP_API_URL=https://cyber-fraud-api.onrender.com
   REACT_APP_API_KEY=public123
   ```

3. **`.env.example`** - Template for new developers
   ```env
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_API_KEY=public123
   ```

### Files Updated

1. ✅ `frontend/src/services/api.js`
   - Changed `REACT_APP_API_BASE` to `REACT_APP_API_URL`
   - Changed default from `127.0.0.1:8000` to `localhost:8000`
   - Exported `API_URL` for use in other files

2. ✅ `frontend/src/context/AuthContext.js`
   - Updated to use `REACT_APP_API_URL`
   - Changed default to `localhost:8000`

3. ✅ `frontend/src/pages/Register.js`
   - Updated to use `REACT_APP_API_URL`
   - Changed default to `localhost:8000`

## Vercel Deployment Steps

### 1. Prerequisites
- GitHub repository with your code
- Vercel account (free tier works)
- Backend API deployed on Render

### 2. Connect Repository to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the repository

### 3. Configure Project Settings

**Framework Preset**: Create React App

**Root Directory**: `frontend`

**Build Command**: 
```bash
npm run build
```

**Output Directory**: 
```bash
build
```

**Install Command**: 
```bash
npm install
```

### 4. Set Environment Variables

In Vercel project settings → Environment Variables, add:

| Name | Value | Environment |
|------|-------|-------------|
| `REACT_APP_API_URL` | `https://cyber-fraud-api.onrender.com` | Production |
| `REACT_APP_API_KEY` | `public123` | Production |

**Important**: 
- Environment variables must start with `REACT_APP_` to be accessible in React
- They are embedded at build time, not runtime
- Changes require a rebuild

### 5. Deploy

Click "Deploy" and wait for the build to complete.

## Environment Variable Usage

### In Code

All API calls now use the environment variable:

```javascript
// api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// AuthContext.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Register.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### Fallback Behavior

If environment variable is not set:
- Development: Falls back to `http://localhost:8000`
- Production: Uses value from Vercel environment variables

## Testing

### Local Development

```bash
cd frontend
npm start
```

Should connect to `http://localhost:8000`

### Production Build Locally

```bash
cd frontend
npm run build
npm install -g serve
serve -s build
```

Should connect to production API (if `.env.production` is set)

### Verify Environment Variables

Add this temporarily to check:

```javascript
console.log('API URL:', process.env.REACT_APP_API_URL);
```

## CORS Configuration

Ensure your backend (Render) allows requests from Vercel domain:

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Vercel Configuration File (Optional)

Create `frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "devCommand": "npm start",
  "installCommand": "npm install",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## Deployment Checklist

### Pre-Deployment
- [x] Environment files created
- [x] All hardcoded URLs removed
- [x] API calls use environment variables
- [x] .gitignore configured correctly
- [x] Backend CORS configured

### Vercel Setup
- [ ] Repository connected
- [ ] Root directory set to `frontend`
- [ ] Environment variables added
- [ ] Build settings configured

### Post-Deployment
- [ ] Test login functionality
- [ ] Test registration
- [ ] Test fraud analysis
- [ ] Test dashboard data loading
- [ ] Test admin features
- [ ] Test export functionality
- [ ] Verify API calls in Network tab

## Troubleshooting

### Issue: API calls fail with CORS error

**Solution**: Update backend CORS to allow Vercel domain

```python
allow_origins=["https://your-app.vercel.app"]
```

### Issue: Environment variables not working

**Solution**: 
1. Verify variables start with `REACT_APP_`
2. Rebuild the project (variables are embedded at build time)
3. Check Vercel dashboard → Settings → Environment Variables

### Issue: 404 on page refresh

**Solution**: Add rewrite rule in `vercel.json` (see above)

### Issue: Build fails

**Solution**: 
1. Check build logs in Vercel
2. Verify `package.json` scripts
3. Ensure all dependencies are in `package.json`
4. Try building locally first

## Environment-Specific Behavior

### Development (`npm start`)
- Uses `.env.development`
- API URL: `http://localhost:8000`
- Hot reload enabled
- Source maps available

### Production (`npm run build`)
- Uses `.env.production`
- API URL: `https://cyber-fraud-api.onrender.com`
- Optimized build
- Minified code

## Custom Domain (Optional)

1. Go to Vercel project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update backend CORS to include custom domain

## Monitoring

### Vercel Analytics
- Enable in project settings
- Track page views, performance
- Monitor Core Web Vitals

### Error Tracking
Consider adding:
- Sentry for error tracking
- LogRocket for session replay
- Google Analytics for usage

## Continuous Deployment

Vercel automatically deploys:
- **Production**: Pushes to `main` branch
- **Preview**: Pull requests and other branches

### Branch Configuration
- `main` → Production deployment
- `develop` → Preview deployment
- Feature branches → Preview deployments

## Security Best Practices

1. **Never commit `.env` files** (already in .gitignore)
2. **Use different API keys** for dev/prod
3. **Rotate API keys** regularly
4. **Use HTTPS** only in production
5. **Enable Vercel password protection** for staging

## Performance Optimization

### Vercel Automatically Provides:
- Global CDN
- Automatic HTTPS
- Image optimization
- Compression (gzip/brotli)
- Edge caching

### Additional Optimizations:
- Code splitting (already enabled with CRA)
- Lazy loading routes
- Image optimization
- Bundle size analysis

## Rollback

If deployment fails:
1. Go to Vercel dashboard
2. Select previous deployment
3. Click "Promote to Production"

## Support

### Vercel Documentation
- [Vercel Docs](https://vercel.com/docs)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Create React App on Vercel](https://vercel.com/guides/deploying-react-with-vercel)

### Project-Specific
- Check Vercel build logs
- Review browser console
- Check Network tab for API calls
- Verify environment variables in Vercel dashboard

## Summary

✅ **Completed**:
- Environment-based configuration
- Removed hardcoded URLs
- Created environment files
- Updated all API calls
- Documented deployment process

🚀 **Ready for**:
- Vercel deployment
- Production use
- Continuous deployment
- Multiple environments

---

**Status**: Ready for Deployment
**Last Updated**: Current Session
**Deployment Platform**: Vercel
**Backend**: Render (https://cyber-fraud-api.onrender.com)
