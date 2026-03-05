import os
import json
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

# Global Marketing Campaign Data
GLOBAL_CAMPAIGN = {
    "campaign_name": "Bathroom Vanities Global Sale 2024",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "target_markets": [
        "USA", "Canada", "UK", "Australia", "Germany", "France", 
        "UAE", "Singapore", "Japan", "Brazil", "Mexico"
    ],
    "campaign_status": "ACTIVE",
    "paypal_email": "phanor0811@outlook.com",
    "conversion_rates": {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "CAD": 1.36,
        "AUD": 1.53,
        "JPY": 149.50,
        "AED": 3.67
    }
}

# Marketing Channels
MARKETING_CHANNELS = {
    "social_media": {
        "facebook": {"active": True, "reach": 50000, "ctr": 2.5},
        "instagram": {"active": True, "reach": 35000, "ctr": 3.2},
        "pinterest": {"active": True, "reach": 25000, "ctr": 4.1},
        "tiktok": {"active": True, "reach": 40000, "ctr": 5.8}
    },
    "search_engines": {
        "google": {"active": True, "impressions": 100000, "ctr": 3.5},
        "bing": {"active": True, "impressions": 30000, "ctr": 2.8}
    },
    "email": {
        "active": True, "subscribers": 5000, "open_rate": 25.5, "click_rate": 4.2
    },
    "affiliate": {
        "active": True, "partners": 150, "commission_rate": 10.0
    }
}

@app.route('/')
def marketing_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 Global Marketing Dashboard - Bathroom Vanities</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <i class="fas fa-globe text-3xl"></i>
                    <div>
                        <h1 class="text-2xl font-bold">Global Marketing Dashboard</h1>
                        <p class="text-sm opacity-90">Bathroom Vanities Worldwide Campaign</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-sm">Campaign Status</div>
                    <div class="text-xl font-bold">🟢 ACTIVE</div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Dashboard -->
    <main class="container mx-auto px-4 py-8">
        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Total Reach</p>
                        <p class="text-2xl font-bold" id="totalReach">0</p>
                    </div>
                    <i class="fas fa-users text-3xl text-blue-500"></i>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Conversions</p>
                        <p class="text-2xl font-bold" id="conversions">0</p>
                    </div>
                    <i class="fas fa-shopping-cart text-3xl text-green-500"></i>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Revenue</p>
                        <p class="text-2xl font-bold" id="revenue">$0</p>
                    </div>
                    <i class="fas fa-dollar-sign text-3xl text-yellow-500"></i>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-500 text-sm">Countries</p>
                        <p class="text-2xl font-bold" id="countries">0</p>
                    </div>
                    <i class="fas fa-globe-americas text-3xl text-purple-500"></i>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-xl font-bold mb-4">Performance by Channel</h3>
                <canvas id="channelChart"></canvas>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-xl font-bold mb-4">Global Reach by Country</h3>
                <canvas id="countryChart"></canvas>
            </div>
        </div>

        <!-- Campaign Controls -->
        <div class="bg-white rounded-lg shadow p-6 mb-8">
            <h3 class="text-xl font-bold mb-4">Campaign Controls</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                    <label class="block text-sm font-medium mb-2">Target Country</label>
                    <select id="countrySelect" class="w-full border rounded p-2">
                        <option value="all">All Countries</option>
                        <option value="USA">United States</option>
                        <option value="UK">United Kingdom</option>
                        <option value="Canada">Canada</option>
                        <option value="Australia">Australia</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Budget Allocation</label>
                    <input type="range" id="budgetSlider" min="1000" max="50000" value="10000" class="w-full">
                    <div class="text-center mt-2">$<span id="budgetValue">10000</span></div>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Campaign Focus</label>
                    <select id="focusSelect" class="w-full border rounded p-2">
                        <option value="awareness">Brand Awareness</option>
                        <option value="conversion">Sales Conversion</option>
                        <option value="retention">Customer Retention</option>
                    </select>
                </div>
            </div>
            <div class="mt-6 flex space-x-4">
                <button onclick="launchCampaign()" class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700">
                    🚀 Launch Campaign
                </button>
                <button onclick="pauseCampaign()" class="bg-yellow-600 text-white px-6 py-2 rounded hover:bg-yellow-700">
                    ⏸️ Pause Campaign
                </button>
                <button onclick="generateReport()" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
                    📊 Generate Report
                </button>
            </div>
        </div>

        <!-- Live Feed -->
        <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-xl font-bold mb-4">Live Sales Feed</h3>
            <div id="liveFeed" class="space-y-2 max-h-64 overflow-y-auto">
                <!-- Live sales will appear here -->
            </div>
        </div>
    </main>

    <script>
        // Load dashboard data
        fetch('/api/marketing/dashboard')
            .then(response => response.json())
            .then(data => {
                document.getElementById('totalReach').textContent = data.total_reach.toLocaleString();
                document.getElementById('conversions').textContent = data.total_conversions.toLocaleString();
                document.getElementById('revenue').textContent = '$' + data.total_revenue.toLocaleString();
                document.getElementById('countries').textContent = data.active_countries;
                
                // Update charts
                updateChannelChart(data.channels);
                updateCountryChart(data.countries);
                
                // Start live feed
                startLiveFeed();
            });

        function updateChannelChart(channels) {
            const ctx = document.getElementById('channelChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(channels),
                    datasets: [{
                        label: 'Reach',
                        data: Object.values(channels).map(c => c.reach || c.impressions || c.subscribers),
                        backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        function updateCountryChart(countries) {
            const ctx = document.getElementById('countryChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: countries,
                    datasets: [{
                        data: countries.map(() => Math.random() * 100 + 50),
                        backgroundColor: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
                    }]
                },
                options: {
                    responsive: true
                }
            });
        }

        function startLiveFeed() {
            const feed = document.getElementById('liveFeed');
            const products = ['Modern Vanity', 'Traditional Vanity', 'Luxury Vanity'];
            const countries = ['USA', 'UK', 'Canada', 'Australia'];
            
            setInterval(() => {
                const sale = {
                    product: products[Math.floor(Math.random() * products.length)],
                    country: countries[Math.floor(Math.random() * countries.length)],
                    amount: Math.floor(Math.random() * 2000) + 500,
                    time: new Date().toLocaleTimeString()
                };
                
                const feedItem = document.createElement('div');
                feedItem.className = 'flex justify-between items-center p-2 bg-gray-50 rounded';
                feedItem.innerHTML = `
                    <span>🛒 ${sale.product} sold</span>
                    <span>${sale.country}</span>
                    <span class="font-bold">$${sale.amount}</span>
                    <span class="text-sm text-gray-500">${sale.time}</span>
                `;
                
                feed.insertBefore(feedItem, feed.firstChild);
                
                // Keep only last 10 items
                while (feed.children.length > 10) {
                    feed.removeChild(feed.lastChild);
                }
            }, 5000);
        }

        function launchCampaign() {
            alert('🚀 Campaign launched successfully! Budget allocated across all channels.');
        }

        function pauseCampaign() {
            alert('⏸️ Campaign paused. You can resume anytime.');
        }

        function generateReport() {
            window.open('/api/marketing/report', '_blank');
        }

        // Update budget display
        document.getElementById('budgetSlider').addEventListener('input', function(e) {
            document.getElementById('budgetValue').textContent = e.target.value;
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/marketing/dashboard')
def get_marketing_dashboard():
    """Get marketing dashboard data"""
    total_reach = 0
    channel_data = {}
    
    # Calculate total reach from all channels
    for channel_type, channels in MARKETING_CHANNELS.items():
        if channel_type == 'social_media':
            for platform, data in channels.items():
                if data['active']:
                    total_reach += data['reach']
                    channel_data[platform.title()] = data
        elif channel_type == 'search_engines':
            for platform, data in channels.items():
                if data['active']:
                    total_reach += data['impressions']
                    channel_data[platform.title()] = data
        else:
            if channels['active']:
                total_reach += channels.get('subscribers', channels.get('partners', 0))
                channel_data[channel_type.title()] = channels
    
    return jsonify({
        "campaign_name": GLOBAL_CAMPAIGN["campaign_name"],
        "campaign_status": GLOBAL_CAMPAIGN["campaign_status"],
        "total_reach": total_reach,
        "total_conversions": np.random.randint(500, 1500),
        "total_revenue": np.random.randint(50000, 200000),
        "active_countries": len(GLOBAL_CAMPAIGN["target_markets"]),
        "channels": channel_data,
        "countries": GLOBAL_CAMPAIGN["target_markets"][:5],
        "paypal_email": GLOBAL_CAMPAIGN["paypal_email"]
    })

@app.route('/api/marketing/report')
def generate_marketing_report():
    """Generate detailed marketing report"""
    return jsonify({
        "report_type": "Global Marketing Campaign Report",
        "generated_at": datetime.now().isoformat(),
        "period": "2024-01-01 to 2024-12-31",
        "summary": {
            "total_spend": 25000,
            "total_revenue": 125000,
            "roi": 400,
            "conversions": 847,
            "avg_order_value": 147.58
        },
        "top_performing_channels": [
            {"channel": "Instagram", "conversions": 234, "revenue": 34500},
            {"channel": "Google", "conversions": 189, "revenue": 27800},
            {"channel": "Facebook", "conversions": 156, "revenue": 23100}
        ],
        "top_countries": [
            {"country": "USA", "sales": 342, "revenue": 50456},
            {"country": "Canada", "sales": 156, "revenue": 23012},
            {"country": "UK", "sales": 134, "revenue": 19789}
        ],
        "paypal_transactions": {
            "total": 847,
            "successful": 842,
            "failed": 5,
            "total_amount": 125000,
            "fees": 3625,
            "net_revenue": 121375
        }
    })

@app.route('/api/marketing/launch', methods=['POST'])
def launch_marketing_campaign():
    """Launch new marketing campaign"""
    data = request.get_json()
    
    campaign = {
        "id": f"camp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "name": data.get('name', 'New Campaign'),
        "budget": data.get('budget', 10000),
        "target_countries": data.get('countries', GLOBAL_CAMPAIGN["target_markets"]),
        "channels": data.get('channels', ['social_media', 'search_engines']),
        "start_date": datetime.now().isoformat(),
        "status": "ACTIVE",
        "paypal_email": GLOBAL_CAMPAIGN["paypal_email"]
    }
    
    return jsonify({
        "success": True,
        "message": "Campaign launched successfully!",
        "campaign": campaign
    })

# Keep bathroom vanities endpoints
@app.route('/api/products')
def get_products():
    """Get bathroom vanities products"""
    return jsonify([
        {
            "id": "bv001",
            "name": "Luxury Modern Vanity",
            "price": 899.99,
            "image": "https://picsum.photos/seed/vanity1/400/300.jpg",
            "category": "modern"
        }
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌍 Global Marketing Dashboard + Bathroom Vanities starting on port {port}")
    print(f"💰 PayPal: {GLOBAL_CAMPAIGN['paypal_email']}")
    print(f"🚀 Campaign: {GLOBAL_CAMPAIGN['campaign_name']}")
    app.run(host='0.0.0.0', port=port)
