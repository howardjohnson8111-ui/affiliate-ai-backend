@echo off
echo 🚀 Starting Affiliate AI Pro - Complete App
echo.
echo 📋 Features Available:
echo   ✅ Portfolio Analytics
echo   ✅ Trading Strategies  
echo   ✅ Real Estate Tools
echo   ✅ Business Formation
echo   ✅ Payment Integration
echo.
echo 🌐 App will be available at: http://localhost:5000
echo 📱 Frontend: https://affiliate-ai-frontend.vercel.app
echo.
echo Installing dependencies...
pip install flask flask-cors numpy pandas requests >nul 2>&1
echo.
echo Starting server...
python app.py
pause
