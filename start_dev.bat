@echo off
echo 🚀 Starting Affiliate AI Backend - Development Mode
echo.
echo 📋 Available Debug Endpoints:
echo   - http://localhost:5000/health
echo   - http://localhost:5000/debug/routes
echo   - http://localhost:5000/debug/config
echo   - http://localhost:5000/debug/test/portfolio
echo.
echo 🌐 Frontend should connect to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

set DEBUG=true
set PORT=5000
set CORS_ORIGIN=http://localhost:3000

python simple_backend.py
