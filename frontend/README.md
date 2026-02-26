# Fraud Detection Platform - Frontend

Modern React-based frontend for the AI-powered Fraud Detection Platform.

## Features

- **Dashboard**: Real-time analytics with summary cards, risk distribution charts, trend analysis, and interactive knowledge graph
- **Analyze**: Submit phone numbers and messages for fraud detection analysis
- **Dark SaaS Theme**: Professional dark theme optimized for extended use
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Visualizations**: Charts powered by Recharts and D3.js

## Prerequisites

- Node.js 16+ and npm
- Backend API running (see main project README)

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment configuration:
```bash
cp .env.example .env
```

4. Edit `.env` and configure your backend URL and API key:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=public123
```

## Development

Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Production Build

Build for production:
```bash
npm run build
```

The optimized build will be in the `build/` directory.

## Deployment

### Option 1: Static Hosting (Netlify, Vercel, AWS S3)

1. Build the project:
```bash
npm run build
```

2. Deploy the `build/` directory to your hosting provider

3. Configure environment variables in your hosting platform:
   - `REACT_APP_API_URL`: Your backend API URL
   - `REACT_APP_API_KEY`: Your API key

### Option 2: Docker

Build and run with Docker:
```bash
docker build -t fraud-detection-frontend .
docker run -p 3000:3000 -e REACT_APP_API_URL=http://your-backend-url fraud-detection-frontend
```

### Option 3: Serve with Backend

Serve the built frontend from your FastAPI backend by placing the `build/` contents in a `static/` directory and configuring FastAPI to serve static files.

## Configuration

### Environment Variables

- `REACT_APP_API_URL`: Backend API base URL (default: `http://localhost:8000`)
- `REACT_APP_API_KEY`: API key for authentication (default: `public123`)

### API Endpoints Used

- `GET /analytics/summary`: Dashboard summary statistics
- `GET /analytics/distribution`: Risk level distribution
- `GET /analytics/trends`: Fraud detection trends over time
- `GET /graph`: Knowledge graph data
- `POST /analyze`: Analyze phone numbers and messages

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # Reusable components
│   │   ├── Navbar.js
│   │   ├── SummaryCards.js
│   │   ├── RiskDistributionChart.js
│   │   ├── TrendChart.js
│   │   ├── GraphView.js
│   │   └── FiltersPanel.js
│   ├── pages/              # Page components
│   │   ├── Dashboard.js
│   │   └── Analyze.js
│   ├── services/           # API services
│   │   └── api.js
│   ├── App.js              # Main app component
│   └── index.js            # Entry point
├── package.json
└── README.md
```

## Technologies

- **React 18**: UI framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Recharts**: Chart library
- **D3.js**: Graph visualization
- **React Scripts**: Build tooling

## Troubleshooting

### CORS Issues

If you encounter CORS errors, ensure your backend has CORS middleware configured:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Failed

1. Verify backend is running: `http://localhost:8000/docs`
2. Check `.env` file has correct `REACT_APP_API_URL`
3. Verify API key is correct
4. Check browser console for detailed error messages

## License

Part of the Cyber Fraud Detection System project.
