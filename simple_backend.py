import os
import json
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, origins=os.getenv("CORS_ORIGIN", "*"))

# Mock data and services
class TradingService:
    def get_portfolio_analytics(self, user_id):
        """Get comprehensive portfolio analytics"""
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
            'top_performers': [
                {'symbol': 'AAPL', 'gain': 15.2},
                {'symbol': 'BTC', 'gain': 28.5},
                {'symbol': 'VZ', 'gain': 8.7}
            ],
            'worst_performers': [
                {'symbol': 'TSLA', 'loss': -12.3},
                {'symbol': 'ETH', 'loss': -5.8}
            ],
            'sharpe_ratio': 1.45,
            'max_drawdown': 8.2,
            'volatility': 12.5
        }
        return portfolio
    
    def get_risk_assessment(self, portfolio_value, risk_tolerance='moderate'):
        """Get risk assessment and recommendations"""
        risk_profiles = {
            'conservative': {'max_volatility': 10, 'max_drawdown': 5, 'recommended_allocation': {'stocks': 40, 'bonds': 40, 'crypto': 10, 'cash': 10}},
            'moderate': {'max_volatility': 15, 'max_drawdown': 10, 'recommended_allocation': {'stocks': 60, 'bonds': 20, 'crypto': 15, 'cash': 5}},
            'aggressive': {'max_volatility': 25, 'max_drawdown': 20, 'recommended_allocation': {'stocks': 80, 'bonds': 10, 'crypto': 7, 'cash': 3}}
        }
        
        profile = risk_profiles.get(risk_tolerance, risk_profiles['moderate'])
        
        return {
            'risk_tolerance': risk_tolerance,
            'current_risk_score': min(100, portfolio_value * 0.0001 + 35),
            'recommendations': [
                f"Maximum volatility should be under {profile['max_volatility']}%",
                f"Maximum drawdown should be under {profile['max_drawdown']}%",
                f"Recommended allocation: {profile['recommended_allocation']}"
            ],
            'rebalancing_suggestions': self.generate_rebalancing_suggestions(profile['recommended_allocation'])
        }
    
    def generate_rebalancing_suggestions(self, target_allocation):
        """Generate portfolio rebalancing suggestions"""
        suggestions = []
        
        for asset_class, target_percentage in target_allocation.items():
            current_percentage = np.random.uniform(target_percentage - 10, target_percentage + 10)
            suggestions.append({
                'asset_class': asset_class,
                'target_percentage': target_percentage,
                'current_percentage': current_percentage,
                'action': 'buy' if current_percentage < target_percentage else 'sell',
                'amount_to_rebalance': abs(target_percentage - current_percentage)
            })
        
        return suggestions

class RealEstateService:
    def search_properties(self, location, property_type='multi_family', min_price=None, max_price=None):
        """Search for real estate properties"""
        properties = [
            {
                'id': '1',
                'address': f'123 Main St, {location}',
                'type': 'multi_family',
                'price': 750000,
                'bedrooms': 4,
                'bathrooms': 3,
                'square_feet': 2400,
                'cap_rate': 8.5,
                'cash_flow': 3200,
                'owner_financing': True
            },
            {
                'id': '2',
                'address': f'456 Oak Ave, {location}',
                'type': 'multi_family',
                'price': 925000,
                'bedrooms': 6,
                'bathrooms': 4,
                'square_feet': 3200,
                'cap_rate': 9.2,
                'cash_flow': 4500,
                'owner_financing': False
            }
        ]
        
        if min_price:
            properties = [p for p in properties if p['price'] >= min_price]
        if max_price:
            properties = [p for p in properties if p['price'] <= max_price]
        
        return properties

# Initialize services
trading_service = TradingService()
real_estate_service = RealEstateService()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

# Portfolio Analytics Endpoints
@app.route('/api/portfolio/analytics/<user_id>', methods=['GET'])
def get_portfolio_analytics(user_id):
    try:
        analytics = trading_service.get_portfolio_analytics(user_id)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/risk-assessment', methods=['POST'])
def get_risk_assessment():
    try:
        data = request.get_json()
        portfolio_value = data.get('portfolio_value')
        risk_tolerance = data.get('risk_tolerance', 'moderate')
        
        assessment = trading_service.get_risk_assessment(portfolio_value, risk_tolerance)
        return jsonify(assessment)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/rebalance', methods=['POST'])
def rebalance_portfolio():
    try:
        data = request.get_json()
        target_allocation = data.get('target_allocation', {})
        
        suggestions = trading_service.generate_rebalancing_suggestions(target_allocation)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Real Estate Endpoints
@app.route('/api/real-estate/search', methods=['POST'])
def search_properties():
    try:
        data = request.get_json()
        location = data.get('location')
        property_type = data.get('property_type', 'multi_family')
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        
        properties = real_estate_service.search_properties(location, property_type, min_price, max_price)
        return jsonify(properties)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Trading strategy endpoints
@app.route('/api/trading/strategy/<symbol>/<strategy_type>', methods=['GET'])
def execute_trading_strategy(symbol, strategy_type):
    try:
        # Mock strategy results
        strategies = {
            'momentum': {'action': 'buy', 'confidence': 0.75, 'reason': 'Positive momentum detected'},
            'mean_reversion': {'action': 'sell', 'confidence': 0.65, 'reason': 'Overbought conditions'},
            'ai_ml': {'action': 'hold', 'confidence': 0.80, 'reason': 'AI analysis suggests waiting'}
        }
        
        result = strategies.get(strategy_type, {'error': 'Invalid strategy'})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )
