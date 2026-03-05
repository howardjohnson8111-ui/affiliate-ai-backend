import os
import json
import numpy as np
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

# Enhanced data with more interactivity
portfolio_data = {
    'user123': {
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
        'monthly_returns': [2.1, 1.8, -0.5, 3.2, 1.1, 2.8, 1.5, -0.8, 2.9, 1.2],
        'sharpe_ratio': 1.45,
        'max_drawdown': 8.2,
        'volatility': 12.5,
        'top_performers': [
            {'symbol': 'AAPL', 'gain': 15.2, 'value': 25000},
            {'symbol': 'BTC', 'gain': 28.5, 'value': 15000},
            {'symbol': 'VZ', 'gain': 8.7, 'value': 8000}
        ],
        'worst_performers': [
            {'symbol': 'TSLA', 'loss': -12.3, 'value': 12000},
            {'symbol': 'ETH', 'loss': -5.8, 'value': 10000}
        ],
        'holdings': [
            {'symbol': 'AAPL', 'shares': 100, 'avg_cost': 150, 'current_price': 250, 'value': 25000, 'gain': 66.7},
            {'symbol': 'MSFT', 'shares': 50, 'avg_cost': 200, 'current_price': 380, 'value': 19000, 'gain': 90.0},
            {'symbol': 'GOOGL', 'shares': 30, 'avg_cost': 100, 'current_price': 140, 'value': 4200, 'gain': 40.0},
            {'symbol': 'BTC', 'shares': 0.5, 'avg_cost': 20000, 'current_price': 30000, 'value': 15000, 'gain': 50.0},
            {'symbol': 'ETH', 'shares': 5, 'avg_cost': 2000, 'current_price': 2000, 'value': 10000, 'gain': 0.0}
        ]
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "Affiliate AI Backend - Enhanced & Interactive!", 
        "version": "2.0",
        "features": ["Portfolio Analytics", "Real-time Updates", "Interactive Charts", "Risk Management"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "backend": "Enhanced Affiliate AI Pro"
    })

@app.route('/api/portfolio/analytics/<user_id>')
def get_portfolio_analytics(user_id):
    # Return user-specific data or default
    user_data = portfolio_data.get(user_id, portfolio_data['user123'])
    
    # Add dynamic calculations
    current_time = datetime.now()
    user_data['last_updated'] = current_time.isoformat()
    user_data['market_status'] = 'Open' if current_time.hour >= 9 and current_time.hour < 16 else 'Closed'
    
    return jsonify(user_data)

@app.route('/api/portfolio/risk-assessment', methods=['POST'])
def risk_assessment():
    data = request.get_json() or {}
    portfolio_value = data.get('portfolio_value', 100000)
    risk_tolerance = data.get('risk_tolerance', 'moderate')
    
    risk_profiles = {
        'conservative': {'max_volatility': 10, 'max_drawdown': 5, 'score': 30},
        'moderate': {'max_volatility': 15, 'max_drawdown': 10, 'score': 60},
        'aggressive': {'max_volatility': 25, 'max_drawdown': 20, 'score': 85}
    }
    
    profile = risk_profiles.get(risk_tolerance, risk_profiles['moderate'])
    
    return jsonify({
        'risk_tolerance': risk_tolerance,
        'current_risk_score': profile['score'],
        'portfolio_value': portfolio_value,
        'recommendations': [
            f"Maximum volatility should be under {profile['max_volatility']}%",
            f"Maximum drawdown should be under {profile['max_drawdown']}%",
            f"Recommended allocation: {{'stocks': {60 if risk_tolerance == 'moderate' else 40}, 'bonds': {20 if risk_tolerance == 'moderate' else 40}, 'crypto': {15 if risk_tolerance == 'moderate' else 10}, 'cash': {5 if risk_tolerance == 'moderate' else 10}}}"
        ],
        'risk_factors': [
            {'factor': 'Market Volatility', 'level': 'Medium', 'impact': 8},
            {'factor': 'Concentration Risk', 'level': 'Low', 'impact': 4},
            {'factor': 'Liquidity Risk', 'level': 'Low', 'impact': 3}
        ]
    })

@app.route('/api/portfolio/rebalance', methods=['POST'])
def rebalance_portfolio():
    data = request.get_json() or {}
    target_allocation = data.get('target_allocation', {'stocks': 60, 'bonds': 20, 'crypto': 15, 'cash': 5})
    
    suggestions = []
    for asset_class, target_percentage in target_allocation.items():
        current_percentage = np.random.uniform(target_percentage - 15, target_percentage + 15)
        action = 'buy' if current_percentage < target_percentage else 'sell'
        amount = abs(target_percentage - current_percentage)
        
        suggestions.append({
            'asset_class': asset_class,
            'target_percentage': target_percentage,
            'current_percentage': round(current_percentage, 1),
            'action': action,
            'amount_to_rebalance': round(amount, 1),
            'urgency': 'High' if amount > 10 else 'Medium' if amount > 5 else 'Low'
        })
    
    return jsonify({
        'suggestions': suggestions,
        'rebalancing_needed': any(s['amount_to_rebalance'] > 5 for s in suggestions),
        'estimated_cost': np.random.uniform(50, 200),
        'time_to_complete': f"{np.random.randint(1, 3)} business days"
    })

@app.route('/api/trading/strategy/<symbol>/<strategy_type>')
def execute_trading_strategy(symbol, strategy_type):
    strategies = {
        'momentum': {
            'action': np.random.choice(['buy', 'sell', 'hold']),
            'confidence': round(np.random.uniform(0.6, 0.9), 2),
            'reason': f"Momentum analysis for {symbol} shows {'bullish' if np.random.random() > 0.5 else 'bearish'} trend",
            'entry_price': round(np.random.uniform(100, 500), 2),
            'stop_loss': round(np.random.uniform(90, 450), 2),
            'target_price': round(np.random.uniform(120, 600), 2)
        },
        'mean_reversion': {
            'action': np.random.choice(['buy', 'sell', 'hold']),
            'confidence': round(np.random.uniform(0.6, 0.9), 2),
            'reason': f"{symbol} is {'oversold' if np.random.random() > 0.5 else 'overbought'} - mean reversion expected",
            'entry_price': round(np.random.uniform(100, 500), 2),
            'stop_loss': round(np.random.uniform(90, 450), 2),
            'target_price': round(np.random.uniform(120, 600), 2)
        },
        'ai_ml': {
            'action': np.random.choice(['buy', 'sell', 'hold']),
            'confidence': round(np.random.uniform(0.7, 0.95), 2),
            'reason': f"AI analysis for {symbol} indicates favorable risk-reward ratio",
            'entry_price': round(np.random.uniform(100, 500), 2),
            'stop_loss': round(np.random.uniform(90, 450), 2),
            'target_price': round(np.random.uniform(120, 600), 2),
            'ai_signals': ['Strong buy signal', 'Volume confirmation', 'Technical alignment']
        }
    }
    
    result = strategies.get(strategy_type, {'error': 'Invalid strategy'})
    result['symbol'] = symbol
    result['strategy'] = strategy_type
    result['timestamp'] = datetime.now().isoformat()
    
    return jsonify(result)

@app.route('/api/real-estate/search', methods=['POST'])
def search_properties():
    data = request.get_json() or {}
    location = data.get('location', 'New York')
    property_type = data.get('property_type', 'multi_family')
    min_price = data.get('min_price', 0)
    max_price = data.get('max_price', 2000000)
    
    properties = [
        {
            'id': '1',
            'address': f'123 Main St, {location}',
            'type': property_type,
            'price': np.random.uniform(500000, 1500000),
            'bedrooms': np.random.randint(2, 6),
            'bathrooms': np.random.randint(1, 4),
            'square_feet': np.random.randint(1500, 4000),
            'cap_rate': round(np.random.uniform(6, 12), 2),
            'cash_flow': round(np.random.uniform(2000, 8000), 0),
            'year_built': np.random.randint(1980, 2023),
            'owner_financing': np.random.choice([True, False]),
            'image_url': f'https://picsum.photos/seed/prop1/400/300.jpg',
            'description': f'Beautiful {property_type.replace("_", " ")} in the heart of {location}'
        },
        {
            'id': '2',
            'address': f'456 Oak Ave, {location}',
            'type': property_type,
            'price': np.random.uniform(400000, 1200000),
            'bedrooms': np.random.randint(2, 5),
            'bathrooms': np.random.randint(1, 3),
            'square_feet': np.random.randint(1200, 3500),
            'cap_rate': round(np.random.uniform(5, 11), 2),
            'cash_flow': round(np.random.uniform(1500, 6000), 0),
            'year_built': np.random.randint(1985, 2022),
            'owner_financing': np.random.choice([True, False]),
            'image_url': f'https://picsum.photos/seed/prop2/400/300.jpg',
            'description': f'Modern {property_type.replace("_", " ")} with great amenities in {location}'
        }
    ]
    
    # Filter by price
    if min_price:
        properties = [p for p in properties if p['price'] >= min_price]
    if max_price:
        properties = [p for p in properties if p['price'] <= max_price]
    
    return jsonify({
        'properties': properties,
        'total_found': len(properties),
        'search_criteria': {
            'location': location,
            'property_type': property_type,
            'price_range': f"${min_price:,} - ${max_price:,}"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Enhanced Affiliate AI Backend starting on port {port}")
    print("✨ Features: Interactive Portfolio, Real-time Analytics, Enhanced UI")
    app.run(host='0.0.0.0', port=port)
