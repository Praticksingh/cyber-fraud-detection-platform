# Deployment Configuration

## Quick Reference

### Environment Variables

| Variable | Development | Production |
|----------|-------------|------------|
| `REACT_APP_API_URL` | `http://localhost:8000` | `https://cyber-fraud-api.onrender.com` |
| `REACT_APP_API_KEY` | `public123` | `public123` |

### Files

- `.env.development` - Local development settings
- `.env.production` - Production deployment settings
- `.env.example` - Template for new developers

### Usage in Code

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## Local Development

```bash
npm start
```

Uses `.env.development` automatically.

## Production Build

```bash
npm run build
```

Uses `.env.production` automatically.

## Vercel Deployment

1. Connect GitHub repository
2. Set root directory: `frontend`
3. Add environment variables in Vercel dashboard
4. Deploy

See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed instructions.

## Testing

### Check Environment Variable
```javascript
console.log('API URL:', process.env.REACT_APP_API_URL);
```

### Test API Connection
Open browser console and check Network tab for API calls.

## Important Notes

⚠️ **Environment variables are embedded at build time**
- Changes require rebuild
- Not available at runtime
- Must start with `REACT_APP_`

✅ **No hardcoded URLs**
- All API calls use environment variables
- Works in both dev and production
- Easy to update

🔒 **Security**
- Never commit `.env` files
- Use different keys for dev/prod
- Rotate keys regularly

## Support

For issues:
1. Check Vercel build logs
2. Verify environment variables
3. Check browser console
4. Review Network tab

---

**Status**: ✅ Ready for Deployment
