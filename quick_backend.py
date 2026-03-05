import os
import json
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/')
def home():
    return jsonify({"message": "Affiliate AI Backend - Working!", "timestamp": datetime.now().isoformat()})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/portfolio/analytics/<user_id>')
def get_portfolio_analytics(user_id):
    portfolio = {
        'total_value': 125000,
        'total_invested': 100000,
        'total_gain_loss': 25000,
        'gain_loss_percentage': 25.0,
        'dividend_income': 3200,
        'crypto_value': 15000,
        'stock_value': 85000,
        'real_estate_value': 25000,
        'cash_balance': 5000,
        'risk_score': 65,
        'diversification_score': 78,
        'monthly_returns': [2.1, 1.8, -0.5, 3.2, 1.1, 2.8],
        'sharpe_ratio': 1.45,
        'max_drawdown': 8.2,
        'volatility': 12.5,
        'top_performers': [
            {'symbol': 'AAPL', 'gain': 15.2},
            {'symbol': 'BTC', 'gain': 28.5},
            {'symbol': 'VZ', 'gain': 8.7}
        ]
    }
    return jsonify(portfolio)

@app.route('/api/portfolio/risk-assessment', methods=['POST'])
def risk_assessment():
    data = request.get_json() or {}
    portfolio_value = data.get('portfolio_value', 100000)
    risk_tolerance = data.get('risk_tolerance', 'moderate')
    
    return jsonify({
        'risk_tolerance': risk_tolerance,
        'current_risk_score': min(100, portfolio_value * 0.0001 + 35),
        'recommendations': [
            f"Maximum volatility should be under {15 if risk_tolerance == 'moderate' else 10}%",
            f"Maximum drawdown should be under {10 if risk_tolerance == 'moderate' else 5}%",
            f"Recommended allocation: {{'stocks': 60, 'bonds': 20, 'crypto': 15, 'cash': 5}}"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
