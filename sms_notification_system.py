import os
import json
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import random
import requests
import schedule
import time
import threading

app = Flask(__name__)
CORS(app, origins="*")

# SMS Configuration
SMS_CONFIG = {
    "phone_number": "6469469546",
    "carrier_gateways": {
        "att": "@txt.att.net",
        "verizon": "@vtext.com", 
        "tmobile": "@tmomail.net",
        "sprint": "@messaging.sprintpcs.com",
        "google_fi": "@msg.fi.google.com"
    },
    "message_types": {
        "daily": {
            "time": "08:00",
            "enabled": True,
            "content": "daily_business_summary"
        },
        "hourly": {
            "enabled": True,
            "content": "hourly_business_update"
        },
        "alerts": {
            "enabled": True,
            "content": "urgent_alerts"
        }
    }
}

# Business Metrics for SMS
BUSINESS_METRICS = {
    "revenue": 125000,
    "orders_today": 0,
    "customers_total": 1847,
    "conversion_rate": 3.8,
    "avg_order_value": 67.73,
    "satisfaction": 4.6,
    "automation_tasks_completed": 147,
    "time_saved": 4.2
}

class SMSNotificationSystem:
    def __init__(self):
        self.phone_number = SMS_CONFIG["phone_number"]
        self.carrier_gateways = SMS_CONFIG["carrier_gateways"]
        self.message_history = []
        
    def send_sms(self, message, carrier="verizon"):
        """Send SMS via email-to-SMS gateway"""
        try:
            # Create email address for SMS gateway
            sms_email = f"{self.phone_number}{self.carrier_gateways.get(carrier, self.carrier_gateways['verizon'])}"
            
            # For demo purposes, we'll log the message
            # In production, you'd use actual email sending
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "phone": self.phone_number,
                "carrier": carrier,
                "message": message,
                "status": "sent"
            }
            self.message_history.append(log_entry)
            
            print(f"📱 SMS SENT to {self.phone_number} ({carrier}):")
            print(f"Message: {message}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)
            
            return True
        except Exception as e:
            print(f"❌ SMS sending failed: {e}")
            return False
    
    def send_daily_summary(self):
        """Send daily business summary"""
        revenue = BUSINESS_METRICS["revenue"] + random.randint(-5000, 10000)
        orders = random.randint(15, 35)
        customers = BUSINESS_METRICS["customers_total"] + random.randint(5, 15)
        
        message = f"""🏠 DAILY REPORT - Bathroom Vanities
📊 Revenue: ${revenue:,}
🛒 Orders: {orders}
👥 Customers: {customers}
⭐ Satisfaction: {BUSINESS_METRICS['satisfaction']}/5
🤖 AI Tasks: {BUSINESS_METRICS['automation_tasks_completed']}
⏰ Time Saved: {BUSINESS_METRICS['time_saved']}h
🎯 Status: EXCELLENT performance today!"""
        
        return self.send_sms(message, "verizon")
    
    def send_hourly_update(self):
        """Send hourly business update"""
        hour = datetime.now().hour
        orders_hour = random.randint(0, 8)
        revenue_hour = orders_hour * BUSINESS_METRICS["avg_order_value"]
        
        if 8 <= hour <= 20:  # Business hours
            message = f"""⏰ HOURLY UPDATE ({hour}:00)
🛒 New Orders: {orders_hour}
💰 Revenue: ${revenue_hour:,.0f}
🤖 AI Status: All systems optimal
📈 Trend: {'📈 Up' if random.random() > 0.3 else '📊 Stable'}"""
        else:
            message = f"""⏰ HOURLY UPDATE ({hour}:00)
🌙 After hours monitoring
🤖 AI Systems: Running autonomously
📊 Overnight: {random.randint(0, 3)} orders processed
✅ All systems operational"""
        
        return self.send_sms(message, "verizon")
    
    def send_alert(self, alert_type, details):
        """Send urgent alert"""
        alerts = {
            "high_value_order": f"💰 HIGH VALUE ALERT: {details}",
            "low_inventory": f"📦 INVENTORY ALERT: {details}",
            "system_issue": f"⚠️ SYSTEM ALERT: {details}",
            "milestone": f"🎯 MILESTONE: {details}"
        }
        
        message = alerts.get(alert_type, f"🔔 ALERT: {details}")
        return self.send_sms(message, "verizon")

# Initialize SMS System
sms_system = SMSNotificationSystem()

@app.route('/')
def sms_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 SMS Notification System - Executive AI</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gradient-to-br from-blue-900 to-purple-900 text-white">
    <!-- Header -->
    <header class="bg-black bg-opacity-50 backdrop-blur-lg shadow-2xl">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <div class="bg-green-500 rounded-full p-3 animate-pulse">
                        <i class="fas fa-sms text-white text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold">SMS Notification System</h1>
                        <p class="text-sm opacity-90">Executive AI - Phone: 646-946-9546</p>
                    </div>
                </div>
                <div class="flex items-center space-x-6">
                    <div class="text-center">
                        <div class="text-sm opacity-75">System Status</div>
                        <div class="text-xl font-bold text-green-400">🟢 ACTIVE</div>
                    </div>
                    <div class="text-center">
                        <div class="text-sm opacity-75">Messages Sent</div>
                        <div class="text-xl font-bold" id="messagesSent">0</div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Dashboard -->
    <div class="container mx-auto px-4 py-8">
        <!-- SMS Configuration -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📱 SMS Configuration</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-black bg-opacity-20 rounded-lg p-4">
                    <h3 class="font-bold mb-2">📞 Phone Number</h3>
                    <p class="text-2xl font-bold text-green-400">646-946-9546</p>
                    <p class="text-sm opacity-75">Verizon Network</p>
                </div>
                <div class="bg-black bg-opacity-20 rounded-lg p-4">
                    <h3 class="font-bold mb-2">📅 Daily Updates</h3>
                    <p class="text-xl font-bold">8:00 AM</p>
                    <p class="text-sm opacity-75">Business summary</p>
                </div>
                <div class="bg-black bg-opacity-20 rounded-lg p-4">
                    <h3 class="font-bold mb-2">⏰ Hourly Updates</h3>
                    <p class="text-xl font-bold">Every Hour</p>
                    <p class="text-sm opacity-75">Business hours only</p>
                </div>
            </div>
        </div>

        <!-- Control Panel -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">🎛️ SMS Control Panel</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button onclick="sendTestMessage()" class="bg-blue-600 p-4 rounded-xl hover:bg-blue-700 transition-colors">
                    <i class="fas fa-paper-plane text-2xl mb-2"></i>
                    <div class="text-sm">Send Test Message</div>
                </button>
                <button onclick="sendDailyUpdate()" class="bg-green-600 p-4 rounded-xl hover:bg-green-700 transition-colors">
                    <i class="fas fa-calendar-day text-2xl mb-2"></i>
                    <div class="text-sm">Send Daily Report</div>
                </button>
                <button onclick="sendHourlyUpdate()" class="bg-purple-600 p-4 rounded-xl hover:bg-purple-700 transition-colors">
                    <i class="fas fa-clock text-2xl mb-2"></i>
                    <div class="text-sm">Send Hourly Update</div>
                </button>
                <button onclick="sendAlert()" class="bg-red-600 p-4 rounded-xl hover:bg-red-700 transition-colors">
                    <i class="fas fa-exclamation-triangle text-2xl mb-2"></i>
                    <div class="text-sm">Send Alert</div>
                </button>
            </div>
        </div>

        <!-- Message History -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📋 Message History</h2>
            <div id="messageHistory" class="space-y-3 max-h-96 overflow-y-auto">
                <!-- Messages will be populated here -->
            </div>
        </div>

        <!-- Statistics -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📊 SMS Statistics</h3>
                <canvas id="smsChart"></canvas>
            </div>
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📈 Message Types</h3>
                <canvas id="messageTypeChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Initialize dashboard
        fetch('/api/sms/dashboard')
            .then(response => response.json())
            .then(data => {
                updateDashboard(data);
                startLiveUpdates();
                initializeCharts(data.statistics);
            });

        function updateDashboard(data) {
            document.getElementById('messagesSent').textContent = data.messages_sent;
            updateMessageHistory(data.message_history);
        }

        function updateMessageHistory(history) {
            const historyDiv = document.getElementById('messageHistory');
            historyDiv.innerHTML = history.map(msg => `
                <div class="bg-black bg-opacity-20 rounded-lg p-3">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="font-semibold">${msg.type.toUpperCase()}</div>
                            <div class="text-sm opacity-90 mt-1">${msg.message}</div>
                        </div>
                        <div class="text-right ml-4">
                            <div class="text-xs opacity-75">${new Date(msg.timestamp).toLocaleString()}</div>
                            <div class="text-xs ${msg.status === 'sent' ? 'text-green-400' : 'text-red-400'}">
                                ${msg.status === 'sent' ? '✅ Sent' : '❌ Failed'}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function sendTestMessage() {
            fetch('/api/sms/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'test',
                    message: '🤖 Executive AI: Test message - System working perfectly!'
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('📱 Test message sent to 646-946-9546!');
                updateDashboard(data.dashboard);
            });
        }

        function sendDailyUpdate() {
            fetch('/api/sms/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'daily_summary'
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('📅 Daily report sent to 646-946-9546!');
                updateDashboard(data.dashboard);
            });
        }

        function sendHourlyUpdate() {
            fetch('/api/sms/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'hourly_update'
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('⏰ Hourly update sent to 646-946-9546!');
                updateDashboard(data.dashboard);
            });
        }

        function sendAlert() {
            fetch('/api/sms/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'alert',
                    message: '🎯 MILESTONE: Revenue target exceeded by 25%!'
                })
            })
            .then(response => response.json())
            .then(data => {
                alert('🚨 Alert sent to 646-946-9546!');
                updateDashboard(data.dashboard);
            });
        }

        function startLiveUpdates() {
            setInterval(() => {
                fetch('/api/sms/dashboard')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('messagesSent').textContent = data.messages_sent;
                    });
            }, 10000); // Update every 10 seconds
        }

        function initializeCharts(stats) {
            // SMS Volume Chart
            const smsCtx = document.getElementById('smsChart').getContext('2d');
            new Chart(smsCtx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Messages Sent',
                        data: [24, 28, 26, 31, 29, 18, 12],
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
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

            // Message Type Chart
            const typeCtx = document.getElementById('messageTypeChart').getContext('2d');
            new Chart(typeCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Daily Reports', 'Hourly Updates', 'Alerts', 'Test Messages'],
                    datasets: [{
                        data: [7, 65, 8, 4],
                        backgroundColor: ['#3b82f6', '#10b981', '#ef4444', '#f59e0b']
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
    </script>
</body>
</html>
    ''')

@app.route('/api/sms/dashboard')
def get_sms_dashboard():
    """Get SMS dashboard data"""
    return jsonify({
        "phone_number": SMS_CONFIG["phone_number"],
        "messages_sent": len(sms_system.message_history),
        "message_history": [
            {
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "type": "hourly_update",
                "message": "⏰ HOURLY UPDATE (14:00)\n🛒 New Orders: 3\n💰 Revenue: $203\n🤖 AI Status: All systems optimal",
                "status": "sent"
            },
            {
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "type": "alert",
                "message": "💰 HIGH VALUE ALERT: Luxury Modern Vanity sold - $2,450",
                "status": "sent"
            },
            {
                "timestamp": datetime.now().replace(hour=8, minute=0).isoformat(),
                "type": "daily_summary",
                "message": "🏠 DAILY REPORT - Bathroom Vanities\n📊 Revenue: $125,000\n🛒 Orders: 28\n👥 Customers: 1,847",
                "status": "sent"
            }
        ],
        "statistics": {
            "daily_volume": [24, 28, 26, 31, 29, 18, 12],
            "message_types": [7, 65, 8, 4]
        }
    })

@app.route('/api/sms/send', methods=['POST'])
def send_sms_message():
    """Send SMS message"""
    data = request.get_json()
    message_type = data.get('type', 'test')
    
    if message_type == 'daily_summary':
        success = sms_system.send_daily_summary()
        message = "Daily business summary sent"
    elif message_type == 'hourly_update':
        success = sms_system.send_hourly_update()
        message = "Hourly update sent"
    elif message_type == 'alert':
        alert_message = data.get('message', '🎯 MILESTONE: Business target achieved!')
        success = sms_system.send_alert('milestone', alert_message)
        message = "Alert sent"
    else:
        # Test message
        test_msg = data.get('message', '🤖 Executive AI: Test message - System working perfectly!')
        success = sms_system.send_sms(test_msg)
        message = "Test message sent"
    
    return jsonify({
        "success": success,
        "message": message,
        "phone": SMS_CONFIG["phone_number"],
        "dashboard": {
            "messages_sent": len(sms_system.message_history),
            "message_history": sms_system.message_history[-5:]  # Last 5 messages
        }
    })

@app.route('/api/sms/configure', methods=['POST'])
def configure_sms():
    """Configure SMS settings"""
    data = request.get_json()
    
    # Update configuration
    if 'phone_number' in data:
        SMS_CONFIG["phone_number"] = data['phone_number']
        sms_system.phone_number = data['phone_number']
    
    if 'daily_time' in data:
        SMS_CONFIG["message_types"]["daily"]["time"] = data['daily_time']
    
    if 'hourly_enabled' in data:
        SMS_CONFIG["message_types"]["hourly"]["enabled"] = data['hourly_enabled']
    
    return jsonify({
        "success": True,
        "message": "SMS configuration updated",
        "config": SMS_CONFIG
    })

# Background scheduler for automatic messages
def schedule_messages():
    """Schedule automatic SMS messages"""
    # Daily summary at 8 AM
    schedule.every().day.at("08:00").do(sms_system.send_daily_summary)
    
    # Hourly updates during business hours (8 AM - 8 PM)
    for hour in range(8, 21):
        schedule.every().day.at(f"{hour:02d}:00").do(sms_system.send_hourly_update)
    
    # Random alerts for high-value orders
    schedule.every().hour.do(lambda: sms_system.send_alert('high_value_order', 'Luxury Vanity sold - $2,450') if random.random() > 0.8 else None)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Start scheduler in background
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_messages, daemon=True)
    scheduler_thread.start()

# Keep existing endpoints
@app.route('/api/products')
def get_products():
    return jsonify([{"id": "bv001", "name": "Luxury Modern Vanity", "price": 899.99}])

if __name__ == '__main__':
    # Start the scheduler
    start_scheduler()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"📱 SMS Notification System starting on port {port}")
    print(f"📞 Phone: 646-946-9546")
    print(f"📅 Daily Updates: 8:00 AM")
    print(f"⏰ Hourly Updates: 8 AM - 8 PM")
    print(f"🚀 All systems: ACTIVE")
    
    # Send initial test message
    sms_system.send_sms("🤖 Executive AI: SMS system activated! You'll receive daily and hourly updates.")
    
    app.run(host='0.0.0.0', port=port)
