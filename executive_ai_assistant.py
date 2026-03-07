import os
import json
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, origins="*")

# Executive AI Assistant Configuration
EXECUTIVE_AI = {
    "name": "Executive AI Assistant",
    "version": "2.0",
    "capabilities": [
        "Sales Management", "Financial Analytics", "Marketing Automation", 
        "Customer Service", "Inventory Management", "Strategic Planning"
    ],
    "personality": "Professional, efficient, proactive",
    "owner": "Phanor",
    "business": "Bathroom Vanities Global"
}

# AI Automation Tasks
AUTOMATION_TASKS = {
    "sales_monitoring": {
        "active": True,
        "frequency": "real-time",
        "alerts": ["low_stock", "high_value_sales", "unusual_activity"]
    },
    "customer_service": {
        "active": True,
        "auto_response": True,
        "escalation_threshold": 2
    },
    "marketing_optimization": {
        "active": True,
        "a_b_testing": True,
        "budget_reallocation": True
    },
    "financial_tracking": {
        "active": True,
        "daily_reports": True,
        "fraud_detection": True
    },
    "inventory_management": {
        "active": True,
        "auto_reorder": True,
        "supplier_negotiation": True
    }
}

# Business Intelligence Data
BUSINESS_INTELLIGENCE = {
    "total_revenue": 125000,
    "monthly_growth": 23.5,
    "total_customers": 1847,
    "conversion_rate": 3.8,
    "avg_order_value": 67.73,
    "customer_satisfaction": 4.6,
    "inventory_turnover": 4.2,
    "profit_margin": 28.4
}

@app.route('/')
def executive_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Executive AI Assistant - Business Command Center</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-900 text-white">
    <!-- Header -->
    <header class="bg-gradient-to-r from-purple-800 to-blue-800 shadow-2xl">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <div class="bg-white rounded-full p-3">
                        <i class="fas fa-robot text-purple-600 text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold">Executive AI Assistant</h1>
                        <p class="text-sm opacity-90">Business Command Center for Phanor</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="text-right">
                        <div class="text-sm opacity-75">AI Status</div>
                        <div class="text-xl font-bold">🟢 ONLINE</div>
                    </div>
                    <div class="text-right">
                        <div class="text-sm opacity-75">Last Updated</div>
                        <div class="text-xl font-bold" id="lastUpdated">Just now</div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- AI Chat Interface -->
    <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- AI Assistant Chat -->
            <div class="lg:col-span-2">
                <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-2xl font-bold">🤖 AI Assistant</h2>
                        <div class="flex space-x-2">
                            <button onclick="clearChat()" class="bg-gray-700 px-3 py-1 rounded hover:bg-gray-600">
                                <i class="fas fa-trash"></i> Clear
                            </button>
                            <button onclick="exportChat()" class="bg-blue-600 px-3 py-1 rounded hover:bg-blue-700">
                                <i class="fas fa-download"></i> Export
                            </button>
                        </div>
                    </div>
                    
                    <div id="chatMessages" class="h-96 overflow-y-auto mb-4 space-y-3">
                        <div class="bg-purple-700 rounded-lg p-3 max-w-xs">
                            <p class="text-sm">🤖 Good morning Phanor! I'm your Executive AI Assistant. I'm monitoring all aspects of your bathroom vanities business in real-time.</p>
                        </div>
                        <div class="bg-purple-700 rounded-lg p-3 max-w-xs">
                            <p class="text-sm">📊 Current Status: Revenue up 23.5% this month, 1,847 customers served, 4.6/5 satisfaction rating.</p>
                        </div>
                        <div class="bg-purple-700 rounded-lg p-3 max-w-xs">
                            <p class="text-sm">🎯 Would you like me to focus on any specific area today? (Sales, Marketing, Operations, or Strategy)</p>
                        </div>
                    </div>
                    
                    <div class="flex space-x-2">
                        <input type="text" id="chatInput" placeholder="Ask me anything about your business..." 
                               class="flex-1 bg-gray-700 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500">
                        <button onclick="sendMessage()" class="bg-purple-600 px-6 py-2 rounded hover:bg-purple-700">
                            <i class="fas fa-paper-plane"></i> Send
                        </button>
                    </div>
                    
                    <!-- Quick Actions -->
                    <div class="mt-4 flex flex-wrap gap-2">
                        <button onclick="quickAction('sales_report')" class="bg-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-600">
                            📈 Sales Report
                        </button>
                        <button onclick="quickAction('marketing_status')" class="bg-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-600">
                            📢 Marketing Status
                        </button>
                        <button onclick="quickAction('inventory_alert')" class="bg-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-600">
                            📦 Inventory Alert
                        </button>
                        <button onclick="quickAction('customer_insights')" class="bg-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-600">
                            👥 Customer Insights
                        </button>
                        <button onclick="quickAction('automation_tasks')" class="bg-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-600">
                            🤖 Automation Tasks
                        </button>
                    </div>
                </div>
            </div>

            <!-- Business Metrics -->
            <div class="space-y-6">
                <!-- Key Performance Indicators -->
                <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">📊 Key Performance Indicators</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span>Total Revenue</span>
                            <span class="font-bold text-green-400" id="totalRevenue">$0</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Monthly Growth</span>
                            <span class="font-bold text-green-400" id="monthlyGrowth">0%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Total Customers</span>
                            <span class="font-bold text-blue-400" id="totalCustomers">0</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Conversion Rate</span>
                            <span class="font-bold text-yellow-400" id="conversionRate">0%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Avg Order Value</span>
                            <span class="font-bold text-purple-400" id="avgOrderValue">$0</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Satisfaction</span>
                            <span class="font-bold text-green-400" id="satisfaction">0/5</span>
                        </div>
                    </div>
                </div>

                <!-- Automation Status -->
                <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">🤖 Automation Status</h3>
                    <div class="space-y-2">
                        <div class="flex justify-between items-center">
                            <span>Sales Monitoring</span>
                            <span class="text-green-400">✅ Active</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Customer Service</span>
                            <span class="text-green-400">✅ Active</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Marketing Optimization</span>
                            <span class="text-green-400">✅ Active</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Financial Tracking</span>
                            <span class="text-green-400">✅ Active</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Inventory Management</span>
                            <span class="text-green-400">✅ Active</span>
                        </div>
                    </div>
                </div>

                <!-- Recent Alerts -->
                <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">🚨 Recent Alerts</h3>
                    <div id="alertsList" class="space-y-2">
                        <!-- Alerts will be populated here -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Advanced Analytics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
            <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📈 Revenue Analytics</h3>
                <canvas id="revenueChart"></canvas>
            </div>
            <div class="bg-gray-800 rounded-lg shadow-2xl p-6">
                <h3 class="text-xl font-bold mb-4">🌍 Geographic Distribution</h3>
                <canvas id="geoChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Initialize dashboard
        fetch('/api/executive/dashboard')
            .then(response => response.json())
            .then(data => {
                updateMetrics(data.business_intelligence);
                updateCharts(data.analytics);
                startLiveUpdates();
                generateAlerts();
            });

        function updateMetrics(bi) {
            document.getElementById('totalRevenue').textContent = '$' + bi.total_revenue.toLocaleString();
            document.getElementById('monthlyGrowth').textContent = bi.monthly_growth + '%';
            document.getElementById('totalCustomers').textContent = bi.total_customers.toLocaleString();
            document.getElementById('conversionRate').textContent = bi.conversion_rate + '%';
            document.getElementById('avgOrderValue').textContent = '$' + bi.avg_order_value.toFixed(2);
            document.getElementById('satisfaction').textContent = bi.customer_satisfaction + '/5';
        }

        function updateCharts(analytics) {
            // Revenue Chart
            const revenueCtx = document.getElementById('revenueChart').getContext('2d');
            new Chart(revenueCtx, {
                type: 'line',
                data: {
                    labels: analytics.months,
                    datasets: [{
                        label: 'Revenue',
                        data: analytics.revenue,
                        borderColor: 'rgb(147, 51, 234)',
                        backgroundColor: 'rgba(147, 51, 234, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    },
                    scales: {
                        y: { 
                            ticks: { color: 'white' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        x: { 
                            ticks: { color: 'white' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        }
                    }
                }
            });

            // Geographic Chart
            const geoCtx = document.getElementById('geoChart').getContext('2d');
            new Chart(geoCtx, {
                type: 'doughnut',
                data: {
                    labels: analytics.countries,
                    datasets: [{
                        data: analytics.sales_by_country,
                        backgroundColor: [
                            '#9333ea', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    }
                }
            });
        }

        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;

            addChatMessage(message, 'user');
            input.value = '';

            // Simulate AI response
            setTimeout(() => {
                const response = generateAIResponse(message);
                addChatMessage(response, 'ai');
            }, 1000);
        }

        function addChatMessage(message, sender) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = sender === 'user' ? 'bg-blue-600 rounded-lg p-3 max-w-xs ml-auto' : 'bg-purple-700 rounded-lg p-3 max-w-xs';
            messageDiv.innerHTML = `<p class="text-sm">${sender === 'user' ? '👤' : '🤖'} ${message}</p>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function generateAIResponse(message) {
            const responses = {
                'sales': '📈 Current sales are performing excellently! Revenue is up 23.5% this month with 1,847 customers. I recommend focusing on the luxury vanity segment as it has the highest profit margin.',
                'marketing': '📢 Marketing campaigns are performing well across all channels. Instagram has the highest engagement at 5.8% CTR. I suggest allocating more budget there.',
                'inventory': '📦 Inventory levels are optimal. The Modern Vanity collection is our bestseller with only 15 units left. I\'ve already set up auto-reorder.',
                'customer': '👥 Customer satisfaction is at 4.6/5. Recent feedback shows customers love our quick shipping and quality. 89% would recommend us.',
                'automation': '🤖 All automation systems are running smoothly. I\'ve processed 147 customer service inquiries automatically and optimized ad spend by 18%.'
            };

            for (const [key, response] of Object.entries(responses)) {
                if (message.toLowerCase().includes(key)) {
                    return response;
                }
            }

            return `🤖 I understand you're asking about "${message}". Let me analyze that for you and provide actionable insights for your bathroom vanities business.`;
        }

        function quickAction(action) {
            const actions = {
                'sales_report': '📊 Generating comprehensive sales report... Revenue: $125,000, Growth: 23.5%, Top product: Luxury Modern Vanity',
                'marketing_status': '📢 All marketing campaigns active. Instagram leading with 5.8% CTR. Budget optimization saved $2,340 this week.',
                'inventory_alert': '📦 Low stock alert: Modern Vanity (15 units left). Auto-reorder initiated. Expected delivery: 3 days.',
                'customer_insights': '👥 Customer insights: 67% repeat customers, avg. order value $67.73, satisfaction 4.6/5.',
                'automation_tasks': '🤖 23 automation tasks completed today. Saved 4.2 hours of manual work. Fraud prevention blocked 3 suspicious orders.'
            };

            addChatMessage(actions[action] || 'Processing your request...', 'ai');
        }

        function startLiveUpdates() {
            setInterval(() => {
                document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();
                
                // Simulate real-time updates
                if (Math.random() > 0.7) {
                    const events = [
                        '🛒 New order received - Luxury Modern Vanity',
                        '💰 Payment processed - $1,247',
                        '📦 Inventory updated - Traditional Vanity',
                        '👥 New customer registered - Canada',
                        '⭐ 5-star review received'
                    ];
                    
                    const event = events[Math.floor(Math.random() * events.length)];
                    generateAlert(event, 'info');
                }
            }, 5000);
        }

        function generateAlert(message, type = 'info') {
            const alertsList = document.getElementById('alertsList');
            const alertDiv = document.createElement('div');
            alertDiv.className = 'flex justify-between items-center p-2 bg-gray-700 rounded';
            
            const icon = type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
            alertDiv.innerHTML = `
                <span class="text-sm">${icon} ${message}</span>
                <span class="text-xs text-gray-400">${new Date().toLocaleTimeString()}</span>
            `;
            
            alertsList.insertBefore(alertDiv, alertsList.firstChild);
            
            // Keep only last 5 alerts
            while (alertsList.children.length > 5) {
                alertsList.removeChild(alertsList.lastChild);
            }
        }

        function generateAlerts() {
            generateAlert('📈 Revenue target achieved - 118% of goal', 'success');
            generateAlert('⚠️ Marketing budget 75% utilized', 'warning');
            generateAlert('📦 Low stock on Modern Vanity - 15 units left', 'warning');
            generateAlert('👥 New customer milestone - 1,847 total', 'success');
        }

        function clearChat() {
            document.getElementById('chatMessages').innerHTML = '';
        }

        function exportChat() {
            alert('Chat export feature coming soon! This will download your conversation history.');
        }

        // Handle Enter key in chat
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/executive/dashboard')
def get_executive_dashboard():
    """Get executive dashboard data"""
    return jsonify({
        "ai_assistant": EXECUTIVE_AI,
        "business_intelligence": BUSINESS_INTELLIGENCE,
        "automation_tasks": AUTOMATION_TASKS,
        "analytics": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "revenue": [85000, 92000, 98000, 105000, 115000, 125000],
            "countries": ["USA", "Canada", "UK", "Australia", "Germany"],
            "sales_by_country": [45000, 28000, 22000, 18000, 12000]
        }
    })

@app.route('/api/executive/chat', methods=['POST'])
def executive_chat():
    """AI Assistant chat interface"""
    data = request.get_json()
    message = data.get('message', '').lower()
    
    # AI Response Logic
    responses = {
        'sales': {
            'message': '📈 Sales Performance Analysis:\n• Total Revenue: $125,000 (+23.5% MoM)\n• 1,847 customers served\n• Conversion rate: 3.8%\n• Avg order value: $67.73\n\nRecommendation: Focus on luxury segment - highest margin at 42%',
            'action': 'generate_sales_report',
            'priority': 'high'
        },
        'marketing': {
            'message': '📢 Marketing Campaign Status:\n• Instagram: 5.8% CTR (best performer)\n• Facebook: 2.5% CTR\n• Google Ads: 3.5% CTR\n• Budget optimized: $2,340 saved this week\n\nAction: Shift 20% more budget to Instagram',
            'action': 'optimize_marketing',
            'priority': 'medium'
        },
        'inventory': {
            'message': '📦 Inventory Management:\n• Modern Vanity: 15 units left (auto-reorder initiated)\n• Traditional Vanity: 42 units\n• Luxury Vanity: 8 units (premium segment)\n• Total inventory value: $67,500\n\nAlert: Restock Modern Vanity within 3 days',
            'action': 'manage_inventory',
            'priority': 'high'
        },
        'customer': {
            'message': '👥 Customer Insights:\n• Satisfaction: 4.6/5 stars\n• 67% repeat customer rate\n• 89% would recommend\n• Top complaint: Shipping time (avg 3.2 days)\n\nAction: Implement express shipping option',
            'action': 'improve_customer_service',
            'priority': 'medium'
        },
        'automation': {
            'message': '🤖 Automation Status:\n• 147 customer service inquiries auto-resolved\n• 23 financial transactions auto-processed\n• 18% marketing budget optimization\n• 4.2 hours manual work saved today\n\nAll systems operating at optimal efficiency',
            'action': 'monitor_automation',
            'priority': 'low'
        }
    }
    
    # Find best matching response
    best_response = None
    for keyword, response in responses.items():
        if keyword in message:
            best_response = response
            break
    
    if not best_response:
        best_response = {
            'message': f'🤖 I understand you\'re asking about "{data.get("message", "")}". Let me analyze your business data and provide actionable insights for your bathroom vanities empire.',
            'action': 'general_assistance',
            'priority': 'medium'
        }
    
    return jsonify({
        'response': best_response['message'],
        'action': best_response['action'],
        'priority': best_response['priority'],
        'timestamp': datetime.now().isoformat(),
        'ai_confidence': 0.92
    })

@app.route('/api/executive/automation')
def get_automation_status():
    """Get automation tasks status"""
    return jsonify({
        'active_automations': AUTOMATION_TASKS,
        'tasks_completed_today': random.randint(20, 50),
        'hours_saved': random.uniform(3, 8),
        'efficiency_gain': f"{random.uniform(15, 25)}%",
        'error_rate': f"{random.uniform(0.1, 0.5)}%",
        'last_optimization': datetime.now().isoformat()
    })

@app.route('/api/executive/analytics')
def get_business_analytics():
    """Get comprehensive business analytics"""
    return jsonify({
        'revenue_analytics': {
            'daily': [2340, 2890, 3120, 2780, 3560, 4120, 3890],
            'weekly': [18500, 21300, 24700, 22900, 28900],
            'monthly': [85000, 92000, 98000, 105000, 115000, 125000],
            'growth_rate': 23.5
        },
        'customer_analytics': {
            'new_customers': 342,
            'returning_customers': 1505,
            'customer_lifetime_value': 287.50,
            'acquisition_cost': 23.40,
            'retention_rate': 67.0
        },
        'product_analytics': {
            'best_sellers': [
                {'name': 'Luxury Modern Vanity', 'sales': 234, 'revenue': 210540},
                {'name': 'Traditional Wood Vanity', 'sales': 189, 'revenue': 141765},
                {'name': 'Minimalist Floating Vanity', 'sales': 156, 'revenue': 109200}
            ],
            'low_stock': [
                {'name': 'Modern Vanity', 'stock': 15, 'reorder_point': 20},
                {'name': 'Luxury Vanity', 'stock': 8, 'reorder_point': 10}
            ]
        },
        'marketing_analytics': {
            'campaign_performance': {
                'instagram': {'ctr': 5.8, 'conversions': 89, 'cost_per_acquisition': 18.50},
                'facebook': {'ctr': 2.5, 'conversions': 67, 'cost_per_acquisition': 24.20},
                'google': {'ctr': 3.5, 'conversions': 112, 'cost_per_acquisition': 22.80}
            },
            'roi': 320,
            'budget_utilization': 75.3
        }
    })

@app.route('/api/executive/alerts')
def get_business_alerts():
    """Get business alerts and notifications"""
    alerts = [
        {
            'type': 'success',
            'title': 'Revenue Target Achieved',
            'message': 'Monthly revenue target exceeded by 18%',
            'timestamp': datetime.now().isoformat(),
            'priority': 'low'
        },
        {
            'type': 'warning',
            'title': 'Low Stock Alert',
            'message': 'Modern Vanity inventory below reorder point',
            'timestamp': (datetime.now() - timedelta(hours=2)).isoformat(),
            'priority': 'medium'
        },
        {
            'type': 'info',
            'title': 'New Customer Milestone',
            'message': 'Reached 1,847 total customers',
            'timestamp': (datetime.now() - timedelta(hours=4)).isoformat(),
            'priority': 'low'
        }
    ]
    
    return jsonify({'alerts': alerts})

# Keep existing endpoints
@app.route('/api/products')
def get_products():
    return jsonify([{"id": "bv001", "name": "Luxury Modern Vanity", "price": 899.99}])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🤖 Executive AI Assistant starting on port {port}")
    print(f"👤 Owner: Phanor")
    print(f"🏠 Business: Bathroom Vanities Global")
    print(f"🚀 All automation systems: ONLINE")
    app.run(host='0.0.0.0', port=port)
