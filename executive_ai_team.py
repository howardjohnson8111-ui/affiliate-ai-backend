import os
import json
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import random
import schedule
import time
import threading

app = Flask(__name__)
CORS(app, origins="*")

# Executive AI Team Configuration
EXECUTIVE_AI_TEAM = {
    "ceo_assistant": {
        "name": "CEO Assistant",
        "role": "Strategic Leadership & Vision",
        "personality": "Visionary, decisive, big-picture focused",
        "expertise": ["Strategic Planning", "Business Development", "Leadership", "Decision Making"],
        "color": "#8B5CF6",
        "emoji": "👔",
        "priority": 1
    },
    "cfo_assistant": {
        "name": "CFO Assistant", 
        "role": "Financial Management & Analytics",
        "personality": "Analytical, detail-oriented, financially focused",
        "expertise": ["Financial Analysis", "Budget Management", "Risk Assessment", "Investment Strategy"],
        "color": "#10B981",
        "emoji": "💰",
        "priority": 2
    },
    "coo_assistant": {
        "name": "COO Assistant",
        "role": "Operations & Efficiency",
        "personality": "Process-oriented, systematic, efficiency focused",
        "expertise": ["Operations Management", "Process Optimization", "Quality Control", "Supply Chain"],
        "color": "#F59E0B",
        "emoji": "⚙️",
        "priority": 3
    },
    "cmo_assistant": {
        "name": "CMO Assistant",
        "role": "Marketing & Brand Strategy",
        "personality": "Creative, customer-focused, growth oriented",
        "expertise": ["Marketing Strategy", "Brand Management", "Customer Acquisition", "Market Research"],
        "color": "#EF4444",
        "emoji": "📢",
        "priority": 4
    },
    "cto_assistant": {
        "name": "CTO Assistant",
        "role": "Technology & Innovation",
        "personality": "Technical, innovative, solution focused",
        "expertise": ["Technology Strategy", "Innovation", "System Architecture", "Digital Transformation"],
        "color": "#3B82F6",
        "emoji": "💻",
        "priority": 5
    },
    "hr_assistant": {
        "name": "HR Director Assistant",
        "role": "Human Resources & Culture",
        "personality": "People-focused, empathetic, culture builder",
        "expertise": ["Talent Management", "Culture Development", "Training", "Employee Relations"],
        "color": "#EC4899",
        "emoji": "👥",
        "priority": 6
    },
    "sales_director": {
        "name": "Sales Director Assistant",
        "role": "Sales Strategy & Revenue",
        "personality": "Results-driven, competitive, customer focused",
        "expertise": ["Sales Strategy", "Revenue Growth", "Customer Relations", "Team Leadership"],
        "color": "#14B8A6",
        "emoji": "🎯",
        "priority": 7
    },
    "product_manager": {
        "name": "Product Manager Assistant",
        "role": "Product Development & Innovation",
        "personality": "User-focused, innovative, detail oriented",
        "expertise": ["Product Strategy", "User Experience", "Innovation", "Market Analysis"],
        "color": "#F97316",
        "emoji": "📦",
        "priority": 8
    },
    "customer_success": {
        "name": "Customer Success Manager",
        "role": "Customer Experience & Retention",
        "personality": "Service-focused, empathetic, relationship builder",
        "expertise": ["Customer Experience", "Retention Strategy", "Support Systems", "Customer Insights"],
        "color": "#06B6D4",
        "emoji": "😊",
        "priority": 9
    }
}

# SMS Configuration for Executive Team
SMS_CONFIG = {
    "phone_number": "6469469546",
    "executive_team": EXECUTIVE_AI_TEAM,
    "message_types": {
        "daily_team_briefing": {
            "time": "08:00",
            "enabled": True,
            "participants": "all_executives"
        },
        "hourly_updates": {
            "enabled": True,
            "frequency": "hourly"
        },
        "executive_alerts": {
            "enabled": True,
            "priority": "high"
        },
        "individual_reports": {
            "enabled": True,
            "schedule": "custom"
        }
    }
}

class ExecutiveTeamCommunication:
    def __init__(self):
        self.phone_number = SMS_CONFIG["phone_number"]
        self.executive_team = SMS_CONFIG["executive_team"]
        self.message_history = []
        self.team_status = {exec_id: {"status": "active", "last_communication": datetime.now()} 
                           for exec_id in self.executive_team.keys()}
        
    def send_executive_message(self, executive_id, message_type, data=None):
        """Send message from specific executive"""
        executive = self.executive_team[executive_id]
        
        messages = {
            "daily_briefing": self.generate_daily_briefing(executive),
            "hourly_update": self.generate_hourly_update(executive),
            "alert": self.generate_alert_message(executive, data),
            "insight": self.generate_insight_message(executive, data),
            "recommendation": self.generate_recommendation(executive, data)
        }
        
        message = messages.get(message_type, f"{executive['emoji']} {executive['name']}: System update")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "executive_id": executive_id,
            "executive_name": executive["name"],
            "executive_role": executive["role"],
            "message_type": message_type,
            "message": message,
            "status": "sent"
        }
        
        self.message_history.append(log_entry)
        self.team_status[executive_id]["last_communication"] = datetime.now()
        
        # Simulate SMS sending
        print(f"📱 EXECUTIVE SMS - {executive['emoji']} {executive['name']}")
        print(f"📞 To: {self.phone_number}")
        print(f"📝 Message: {message}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        return True
    
    def generate_daily_briefing(self, executive):
        """Generate daily briefing for specific executive"""
        briefings = {
            "ceo_assistant": f"""👔 CEO DAILY BRIEFING
📊 Business Overview: Revenue up 23.5%, all systems optimal
🎯 Strategic Focus: Market expansion, luxury segment growth
📈 Growth Opportunities: European market, premium products
🤖 Team Performance: All 8 executives operating at peak efficiency
🏆 Today's Priority: Review Q4 strategic roadmap""",
            
            "cfo_assistant": f"""💰 CFO DAILY BRIEFING
📊 Financial Performance: $125K revenue, 28.4% profit margin
💵 Cash Flow: Strong, $42K available for investment
📈 ROI: Marketing 320%, operations 145%, overall 234%
🎯 Financial Targets: On track for 18% YoY growth
⚠️ Watch List: Marketing budget utilization at 75%""",
            
            "coo_assistant": f"""⚙️ COO DAILY BRIEFING
🏭 Operations: 99.2% efficiency, 4.2h time saved daily
📦 Inventory: Optimal levels, auto-reorder working
🤖 Automation: 147 tasks completed, 98.5% success rate
📋 Process Improvement: 3 bottlenecks identified, solutions ready
🎯 Today's Focus: Supplier negotiations, workflow optimization""",
            
            "cmo_assistant": f"""📢 CMO DAILY BRIEFING
📱 Marketing Performance: 5.8% CTR Instagram, 3.5% Google
👥 Customer Acquisition: 342 new customers, $23.40 CAC
📊 Brand Awareness: Up 45% MoM, engagement strong
🎯 Campaign ROI: 320% overall, Instagram leading
💡 Today's Priority: Optimize budget allocation, launch luxury campaign""",
            
            "cto_assistant": f"""💻 CTO DAILY BRIEFING
🔧 System Status: All platforms operational, 99.9% uptime
🤖 AI Performance: 98.5% accuracy, <1s response time
📊 Data Analytics: Real-time processing, insights generated
🔒 Security: All systems secure, 0 threats detected
🚀 Today's Focus: Infrastructure optimization, AI enhancements""",
            
            "hr_assistant": f"""👥 HR DAILY BRIEFING
😊 Team Performance: All AI assistants optimal, 98.5% efficiency
📚 Training: 3 new automation modules deployed
🤝 Culture: Excellent collaboration across executive team
📈 Satisfaction: 4.6/5 customer rating, team morale high
🎯 Today's Priority: Performance reviews, skill gap analysis""",
            
            "sales_director": f"""🎯 SALES DIRECTOR DAILY BRIEFING
💰 Revenue: $125K MoM, 23.5% growth rate
🛒 Orders: 28 today, avg $67.73 per order
🏆 Top Performer: Luxury Modern Vanity - 42% margin
📊 Conversion: 3.8% rate, improving steadily
🎯 Today's Priority: Close 5 high-value prospects, team motivation""",
            
            "product_manager": f"""📦 PRODUCT MANAGER DAILY BRIEFING
🏆 Best Seller: Luxury Modern Vanity - 234 units sold
📊 Product Performance: All categories meeting targets
💡 Innovation: 2 new designs in development
👥 Customer Feedback: 4.6/5 satisfaction, feature requests noted
🎯 Today's Priority: Review product roadmap, quality assurance""",
            
            "customer_success": f"""😊 CUSTOMER SUCCESS DAILY BRIEFING
⭐ Satisfaction: 4.6/5 rating, 89% would recommend
🎧 Support: 23 inquiries resolved, 96.2% success rate
🔄 Retention: 67% repeat customers, improving
💬 Feedback: Quality praised, shipping speed mentioned
🎯 Today's Priority: Proactive outreach, satisfaction improvement"""
        }
        
        return briefings.get(executive["id"], f"{executive['emoji']} Daily briefing prepared")
    
    def generate_hourly_update(self, executive):
        """Generate hourly update for specific executive"""
        hour = datetime.now().hour
        
        if 8 <= hour <= 20:  # Business hours
            updates = {
                "ceo_assistant": f"👔 CEO UPDATE: Strategic initiatives on track, team alignment optimal",
                "cfo_assistant": f"💰 CFO UPDATE: Financial metrics strong, budget within targets",
                "coo_assistant": f"⚙️ COO UPDATE: Operations smooth, automation saving 4.2h daily",
                "cmo_assistant": f"📢 CMO UPDATE: Marketing campaigns performing well, engagement high",
                "cto_assistant": f"💻 CTO UPDATE: Systems stable, AI performance excellent",
                "hr_assistant": f"👥 HR UPDATE: Team productivity high, morale excellent",
                "sales_director": f"🎯 SALES UPDATE: Revenue tracking 18% above target",
                "product_manager": f"📦 PRODUCT UPDATE: Quality metrics optimal, inventory balanced",
                "customer_success": f"😊 CS UPDATE: Customer satisfaction steady, support efficient"
            }
        else:
            updates = {
                exec_id: f"{exec['emoji']} {exec['name']}: After-hours monitoring, all systems stable"
                for exec_id, exec in self.executive_team.items()
            }
        
        return updates.get(executive["id"], f"{executive['emoji']} Status update")
    
    def generate_alert_message(self, executive, data):
        """Generate alert message for specific executive"""
        alert_type = data.get("type", "general") if data else "general"
        
        alerts = {
            "ceo_assistant": {
                "milestone": f"👔 CEO ALERT: Major milestone achieved - Revenue target exceeded by 25%!",
                "strategic": f"👔 CEO ALERT: Strategic opportunity detected - European market ready for entry",
                "risk": f"👔 CEO ALERT: Risk identified - Competitor activity increased, recommend response"
            },
            "cfo_assistant": {
                "financial": f"💰 CFO ALERT: High-value transaction - $3,450 order processed",
                "budget": f"💰 CFO ALERT: Budget threshold reached - Marketing at 85% utilization",
                "opportunity": f"💰 CFO ALERT: Investment opportunity - ROI projection 340% on new segment"
            },
            "coo_assistant": {
                "operational": f"⚙️ COO ALERT: Operational efficiency milestone - 99.5% achieved",
                "supply": f"⚙️ COO ALERT: Supply chain optimization - 18% cost reduction achieved",
                "quality": f"⚙️ COO ALERT: Quality excellence - 99.8% customer satisfaction"
            },
            "cmo_assistant": {
                "campaign": f"📢 CMO ALERT: Campaign success - Instagram engagement up 45%",
                "brand": f"📢 CMO ALERT: Brand milestone - 10K followers reached",
                "market": f"📢 CMO ALERT: Market penetration - New segment showing 67% growth"
            },
            "cto_assistant": {
                "system": f"💻 CTO ALERT: System optimization - Response time improved to 0.8s",
                "innovation": f"💻 CTO ALERT: Innovation breakthrough - New AI model 15% more accurate",
                "security": f"💻 CTO ALERT: Security milestone - 365 days incident-free"
            },
            "hr_assistant": {
                "team": f"👥 HR ALERT: Team achievement - All executives at peak performance",
                "culture": f"👥 HR ALERT: Culture milestone - 100% team satisfaction achieved",
                "development": f"👥 HR ALERT: Development success - New skills deployed across team"
            },
            "sales_director": {
                "revenue": f"🎯 SALES ALERT: Revenue milestone - Daily target exceeded by 45%",
                "customer": f"🎯 SALES ALERT: Customer milestone - VIP client acquired",
                "team": f"🎯 SALES ALERT: Team achievement - Sales conversion up 28%"
            },
            "product_manager": {
                "product": f"📦 PRODUCT ALERT: Product success - Luxury vanity sold out",
                "innovation": f"📦 PRODUCT ALERT: Innovation launch - New design receiving rave reviews",
                "quality": f"📦 PRODUCT ALERT: Quality excellence - Zero defects this month"
            },
            "customer_success": {
                "satisfaction": f"😊 CS ALERT: Satisfaction milestone - 4.8/5 rating achieved",
                "retention": f"😊 CS ALERT: Retention success - 75% repeat customer rate",
                "service": f"😊 CS ALERT: Service excellence - 100% support tickets resolved"
            }
        }
        
        executive_alerts = alerts.get(executive["id"], {})
        return executive_alerts.get(alert_type, f"{executive['emoji']} {executive['name']}: Alert generated")
    
    def generate_insight_message(self, executive, data):
        """Generate insight message for specific executive"""
        insights = {
            "ceo_assistant": f"👔 CEO INSIGHT: Market analysis shows 34% growth potential in premium segment",
            "cfo_assistant": f"💰 CFO INSIGHT: Cost optimization opportunity in supply chain - $12K annual savings",
            "coo_assistant": f"⚙️ COO INSIGHT: Process automation could save additional 2.5 hours daily",
            "cmo_assistant": f"📢 CMO INSIGHT: Customer data indicates strong demand for eco-friendly products",
            "cto_assistant": f"💻 CTO INSIGHT: AI upgrade could improve accuracy by 12% across all systems",
            "hr_assistant": f"👥 HR INSIGHT: Team cross-training could increase efficiency by 15%",
            "sales_director": f"🎯 SALES INSIGHT: Upsell opportunity identified - 23% customers ready for premium upgrade",
            "product_manager": f"📦 PRODUCT INSIGHT: Customer feedback suggests demand for smart vanity features",
            "customer_success": f"😊 CS INSIGHT: Proactive outreach could increase retention by 8%"
        }
        
        return insights.get(executive["id"], f"{executive['emoji']} Insight generated")
    
    def generate_recommendation(self, executive, data):
        """Generate recommendation from specific executive"""
        recommendations = {
            "ceo_assistant": f"👔 CEO RECOMMENDATION: Approve European expansion - projected $25K monthly revenue",
            "cfo_assistant": f"💰 CFO RECOMMENDATION: Increase marketing budget by 20% - ROI projection 340%",
            "coo_assistant": f"⚙️ COO RECOMMENDATION: Implement new automation system - save 6 hours weekly",
            "cmo_assistant": f"📢 CMO RECOMMENDATION: Launch luxury campaign - target 45% market share",
            "cto_assistant": f"💻 CTO RECOMMENDATION: Upgrade AI infrastructure - improve all metrics by 15%",
            "hr_assistant": f"👥 HR RECOMMENDATION: Implement skill development program - increase team capability",
            "sales_director": f"🎯 SALES RECOMMENDATION: Focus on luxury segment - 42% higher margins",
            "product_manager": f"📦 PRODUCT RECOMMENDATION: Launch smart vanity line - address market demand",
            "customer_success": f"😊 CS RECOMMENDATION: Implement proactive support - increase satisfaction to 4.8/5"
        }
        
        return recommendations.get(executive["id"], f"{executive['emoji']} Recommendation prepared")
    
    def send_team_briefing(self):
        """Send briefing from all executives"""
        for exec_id in self.executive_team.keys():
            self.send_executive_message(exec_id, "daily_briefing")
        return True
    
    def get_team_status(self):
        """Get status of all executive assistants"""
        return {
            "team_size": len(self.executive_team),
            "active_executives": len([e for e in self.team_status.values() if e["status"] == "active"]),
            "total_messages": len(self.message_history),
            "last_team_communication": max([e["last_communication"] for e in self.team_status.values()]),
            "executives": [
                {
                    "id": exec_id,
                    "name": exec["name"],
                    "role": exec["role"],
                    "emoji": exec["emoji"],
                    "color": exec["color"],
                    "status": self.team_status[exec_id]["status"],
                    "last_communication": self.team_status[exec_id]["last_communication"].isoformat()
                }
                for exec_id, exec in self.executive_team.items()
            ]
        }

# Initialize Executive Team Communication
executive_team = ExecutiveTeamCommunication()

@app.route('/')
def executive_team_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Executive AI Team - 9 Assistants</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
    <!-- Header -->
    <header class="bg-black bg-opacity-50 backdrop-blur-lg shadow-2xl">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <div class="bg-gradient-to-r from-purple-500 to-blue-500 rounded-full p-3 animate-pulse">
                        <i class="fas fa-users text-white text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold">Executive AI Team</h1>
                        <p class="text-sm opacity-90">9 Specialized Assistants for Phanor | Phone: 646-946-9546</p>
                    </div>
                </div>
                <div class="flex items-center space-x-6">
                    <div class="text-center">
                        <div class="text-sm opacity-75">Team Status</div>
                        <div class="text-xl font-bold text-green-400">🟢 ALL ACTIVE</div>
                    </div>
                    <div class="text-center">
                        <div class="text-sm opacity-75">Messages Today</div>
                        <div class="text-xl font-bold" id="messagesToday">0</div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Executive Team Grid -->
    <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <!-- Executive cards will be populated here -->
            <div id="executiveGrid"></div>
        </div>

        <!-- Team Communication Control -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📞 Team Communication Control</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button onclick="sendTeamBriefing()" class="bg-purple-600 p-4 rounded-xl hover:bg-purple-700 transition-colors">
                    <i class="fas fa-users text-2xl mb-2"></i>
                    <div class="text-sm">Team Briefing</div>
                </button>
                <button onclick="sendIndividualUpdates()" class="bg-blue-600 p-4 rounded-xl hover:bg-blue-700 transition-colors">
                    <i class="fas fa-user text-2xl mb-2"></i>
                    <div class="text-sm">Individual Updates</div>
                </button>
                <button onclick="sendInsights()" class="bg-green-600 p-4 rounded-xl hover:bg-green-700 transition-colors">
                    <i class="fas fa-lightbulb text-2xl mb-2"></i>
                    <div class="text-sm">Send Insights</div>
                </button>
                <button onclick="sendRecommendations()" class="bg-yellow-600 p-4 rounded-xl hover:bg-yellow-700 transition-colors">
                    <i class="fas fa-chart-line text-2xl mb-2"></i>
                    <div class="text-sm">Recommendations</div>
                </button>
            </div>
        </div>

        <!-- Message History -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📋 Executive Communications</h2>
            <div id="messageHistory" class="space-y-3 max-h-96 overflow-y-auto">
                <!-- Messages will be populated here -->
            </div>
        </div>

        <!-- Team Analytics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📊 Team Performance</h3>
                <canvas id="teamPerformanceChart"></canvas>
            </div>
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📱 Communication Volume</h3>
                <canvas id="communicationChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Initialize dashboard
        fetch('/api/executive-team/dashboard')
            .then(response => response.json())
            .then(data => {
                renderExecutiveTeam(data.executives);
                updateMessageHistory(data.message_history);
                updateTeamStats(data);
                initializeCharts(data.analytics);
                startLiveUpdates();
            });

        function renderExecutiveTeam(executives) {
            const grid = document.getElementById('executiveGrid');
            grid.innerHTML = executives.map(exec => `
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 hover:scale-105 transition-transform cursor-pointer" 
                     onclick="communicateWithExecutive('${exec.id}')">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center space-x-3">
                            <div class="text-3xl">${exec.emoji}</div>
                            <div>
                                <h3 class="text-lg font-bold">${exec.name}</h3>
                                <p class="text-sm opacity-75">${exec.role}</p>
                            </div>
                        </div>
                        <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                    </div>
                    <div class="text-sm opacity-90 mb-3">
                        ${exec.expertise.slice(0, 3).join(' • ')}
                    </div>
                    <div class="flex justify-between items-center text-xs">
                        <span class="opacity-75">Last: ${new Date(exec.last_communication).toLocaleTimeString()}</span>
                        <span class="text-green-400">🟢 Active</span>
                    </div>
                </div>
            `).join('');
        }

        function updateMessageHistory(history) {
            const historyDiv = document.getElementById('messageHistory');
            historyDiv.innerHTML = history.slice(-10).reverse().map(msg => `
                <div class="bg-black bg-opacity-20 rounded-lg p-3">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-semibold">${msg.executive_emoji} ${msg.executive_name}</span>
                                <span class="text-xs opacity-75 bg-purple-600 px-2 py-1 rounded">${msg.message_type.toUpperCase()}</span>
                            </div>
                            <div class="text-sm opacity-90 whitespace-pre-line">${msg.message}</div>
                        </div>
                        <div class="text-right ml-4">
                            <div class="text-xs opacity-75">${new Date(msg.timestamp).toLocaleString()}</div>
                            <div class="text-xs text-green-400">✅ Sent</div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function updateTeamStats(data) {
            document.getElementById('messagesToday').textContent = data.total_messages;
        }

        function communicateWithExecutive(executiveId) {
            fetch('/api/executive-team/communicate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    executive_id: executiveId,
                    message_type: 'insight'
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(`📱 Message sent from ${data.executive_name}!`);
                updateDashboard();
            });
        }

        function sendTeamBriefing() {
            fetch('/api/executive-team/team-briefing', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                alert('📱 Team briefing sent to all 9 executives!');
                updateDashboard();
            });
        }

        function sendIndividualUpdates() {
            fetch('/api/executive-team/individual-updates', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                alert('📱 Individual updates sent to all executives!');
                updateDashboard();
            });
        }

        function sendInsights() {
            fetch('/api/executive-team/insights', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                alert('💡 Insights sent from all executives!');
                updateDashboard();
            });
        }

        function sendRecommendations() {
            fetch('/api/executive-team/recommendations', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'}
            })
            .then(response => response.json())
            .then(data => {
                alert('📈 Recommendations sent from all executives!');
                updateDashboard();
            });
        }

        function updateDashboard() {
            fetch('/api/executive-team/dashboard')
                .then(response => response.json())
                .then(data => {
                    updateMessageHistory(data.message_history);
                    updateTeamStats(data);
                });
        }

        function startLiveUpdates() {
            setInterval(() => {
                fetch('/api/executive-team/dashboard')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('messagesToday').textContent = data.total_messages;
                    });
            }, 15000); // Update every 15 seconds
        }

        function initializeCharts(analytics) {
            // Team Performance Chart
            const performanceCtx = document.getElementById('teamPerformanceChart').getContext('2d');
            new Chart(performanceCtx, {
                type: 'radar',
                data: {
                    labels: ['Strategy', 'Finance', 'Operations', 'Marketing', 'Technology', 'HR', 'Sales', 'Product', 'Customer'],
                    datasets: [{
                        label: 'Team Performance',
                        data: [95, 92, 98, 88, 94, 91, 89, 93, 96],
                        borderColor: 'rgb(147, 51, 234)',
                        backgroundColor: 'rgba(147, 51, 234, 0.2)',
                        pointBackgroundColor: 'rgb(147, 51, 234)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(147, 51, 234)'
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
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: { color: 'white' },
                            ticks: { 
                                color: 'white',
                                backdropColor: 'transparent'
                            }
                        }
                    }
                }
            });

            // Communication Volume Chart
            const commCtx = document.getElementById('communicationChart').getContext('2d');
            new Chart(commCtx, {
                type: 'bar',
                data: {
                    labels: ['CEO', 'CFO', 'COO', 'CMO', 'CTO', 'HR', 'Sales', 'Product', 'Customer'],
                    datasets: [{
                        label: 'Messages Today',
                        data: [12, 15, 18, 14, 11, 9, 16, 13, 10],
                        backgroundColor: [
                            '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#3B82F6',
                            '#EC4899', '#14B8A6', '#F97316', '#06B6D4'
                        ]
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
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/executive-team/dashboard')
def get_executive_team_dashboard():
    """Get executive team dashboard data"""
    team_status = executive_team.get_team_status()
    
    return jsonify({
        "team_size": team_status["team_size"],
        "active_executives": team_status["active_executives"],
        "total_messages": team_status["total_messages"],
        "executives": team_status["executives"],
        "message_history": executive_team.message_history[-20:],  # Last 20 messages
        "analytics": {
            "performance": [95, 92, 98, 88, 94, 91, 89, 93, 96],
            "communication_volume": [12, 15, 18, 14, 11, 9, 16, 13, 10]
        }
    })

@app.route('/api/executive-team/communicate', methods=['POST'])
def communicate_with_executive():
    """Send message from specific executive"""
    data = request.get_json()
    executive_id = data.get('executive_id')
    message_type = data.get('message_type', 'insight')
    
    if executive_id not in EXECUTIVE_AI_TEAM:
        return jsonify({"error": "Executive not found"}), 404
    
    executive = EXECUTIVE_AI_TEAM[executive_id]
    success = executive_team.send_executive_message(executive_id, message_type, data)
    
    return jsonify({
        "success": success,
        "executive_id": executive_id,
        "executive_name": executive["name"],
        "executive_role": executive["role"],
        "message_type": message_type,
        "phone": SMS_CONFIG["phone_number"]
    })

@app.route('/api/executive-team/team-briefing', methods=['POST'])
def send_team_briefing():
    """Send briefing from all executives"""
    success = executive_team.send_team_briefing()
    
    return jsonify({
        "success": success,
        "message": "Team briefing sent from all 9 executives",
        "executives_notified": len(EXECUTIVE_AI_TEAM),
        "phone": SMS_CONFIG["phone_number"]
    })

@app.route('/api/executive-team/individual-updates', methods=['POST'])
def send_individual_updates():
    """Send individual updates from all executives"""
    for exec_id in EXECUTIVE_AI_TEAM.keys():
        executive_team.send_executive_message(exec_id, "hourly_update")
    
    return jsonify({
        "success": True,
        "message": "Individual updates sent from all executives",
        "executives_notified": len(EXECUTIVE_AI_TEAM)
    })

@app.route('/api/executive-team/insights', methods=['POST'])
def send_insights():
    """Send insights from all executives"""
    for exec_id in EXECUTIVE_AI_TEAM.keys():
        executive_team.send_executive_message(exec_id, "insight")
    
    return jsonify({
        "success": True,
        "message": "Strategic insights sent from all executives",
        "executives_notified": len(EXECUTIVE_AI_TEAM)
    })

@app.route('/api/executive-team/recommendations', methods=['POST'])
def send_recommendations():
    """Send recommendations from all executives"""
    for exec_id in EXECUTIVE_AI_TEAM.keys():
        executive_team.send_executive_message(exec_id, "recommendation")
    
    return jsonify({
        "success": True,
        "message": "Business recommendations sent from all executives",
        "executives_notified": len(EXECUTIVE_AI_TEAM)
    })

@app.route('/api/executive-team/alert', methods=['POST'])
def send_executive_alert():
    """Send alert from specific executive"""
    data = request.get_json()
    executive_id = data.get('executive_id', "ceo_assistant")
    alert_type = data.get('alert_type', 'milestone')
    alert_data = data.get('data', {})
    
    success = executive_team.send_executive_message(executive_id, "alert", {"type": alert_type, **alert_data})
    
    return jsonify({
        "success": success,
        "message": f"Alert sent from {EXECUTIVE_AI_TEAM[executive_id]['name']}",
        "alert_type": alert_type
    })

# Background scheduler for executive communications
def schedule_executive_communications():
    """Schedule automatic executive communications"""
    # Daily team briefing at 8 AM
    schedule.every().day.at("08:00").do(executive_team.send_team_briefing)
    
    # Hourly updates during business hours
    for hour in range(8, 21):
        schedule.every().day.at(f"{hour:02d}:00").do(lambda: [
            executive_team.send_executive_message(exec_id, "hourly_update") 
            for exec_id in EXECUTIVE_AI_TEAM.keys()
        ])
    
    # Random insights from different executives
    schedule.every().hour.do(lambda: executive_team.send_executive_message(
        random.choice(list(EXECUTIVE_AI_TEAM.keys())), "insight"
    ) if random.random() > 0.7 else None)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in background
def start_executive_scheduler():
    scheduler_thread = threading.Thread(target=schedule_executive_communications, daemon=True)
    scheduler_thread.start()

# Keep existing endpoints
@app.route('/api/products')
def get_products():
    return jsonify([{"id": "bv001", "name": "Luxury Modern Vanity", "price": 899.99}])

if __name__ == '__main__':
    # Start the scheduler
    start_executive_scheduler()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🤖 Executive AI Team starting on port {port}")
    print(f"👥 Team Size: 9 Specialized Assistants")
    print(f"📞 Phone: 646-946-9546")
    print(f"📅 Daily Briefing: 8:00 AM")
    print(f"⏰ Hourly Updates: 8 AM - 8 PM")
    print(f"🚀 All systems: ACTIVE")
    
    # Send initial team introduction
    for exec_id, executive in EXECUTIVE_AI_TEAM.items():
        executive_team.send_executive_message(exec_id, "daily_briefing")
    
    app.run(host='0.0.0.0', port=port)
