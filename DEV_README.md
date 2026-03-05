# 🚀 Affiliate AI Backend - Development Guide

## Quick Start Development

### Option 1: Use the startup script (Windows)
```bash
start_dev.bat
```

### Option 2: Manual start
```bash
# Set environment variables
set DEBUG=true
set PORT=5000
set CORS_ORIGIN=http://localhost:3000

# Start the server
python simple_backend.py
```

## 🐛 Debug Mode Features

When `DEBUG=true`, the following endpoints are available:

### Health Check
- `GET /health` - Server status

### Debug Tools
- `GET /debug/routes` - List all available API endpoints
- `GET /debug/config` - Show current configuration
- `GET /debug/test/<endpoint>` - Test any endpoint with mock data
- `POST /debug/test/<endpoint>` - Test POST endpoints

### Main API Endpoints
- `GET /api/portfolio/analytics/<user_id>` - Portfolio analytics
- `POST /api/portfolio/risk-assessment` - Risk assessment
- `POST /api/portfolio/rebalance` - Rebalancing suggestions
- `POST /api/real-estate/search` - Property search
- `GET /api/trading/strategy/<symbol>/<strategy_type>` - Trading strategies

## 🔧 Environment Variables

### Development (.env.development)
```
DEBUG=true
PORT=5000
CORS_ORIGIN=http://localhost:3000
API_BASE_URL=http://localhost:3001/api
```

### Production (Render)
```
DEBUG=false
PORT=${PORT}
CORS_ORIGIN=https://affiliate-ai-frontend.vercel.app
```

## 📊 Testing the Backend

### Test Portfolio Analytics
```bash
curl http://localhost:5000/api/portfolio/analytics/user123
```

### Test Risk Assessment
```bash
curl -X POST http://localhost:5000/api/portfolio/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"portfolio_value": 125000, "risk_tolerance": "moderate"}'
```

### Test Property Search
```bash
curl -X POST http://localhost:5000/api/real-estate/search \
  -H "Content-Type: application/json" \
  -d '{"location": "New York", "min_price": 500000}'
```

## 🌐 Frontend Connection

Make sure your frontend is configured to connect to:
- Development: `http://localhost:5000`
- Production: `https://affiliate-ai-backend.onrender.com`

## 📝 Development Notes

- Debug mode provides detailed logging and error messages
- All changes auto-reload when debug is enabled
- CORS is configured for local development
- Mock data is used for all API responses
- No external API keys required for development
