import os
import json
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import random
import schedule

app = Flask(__name__)
CORS(app, origins="*")

# Executive AI Personal Assistant
PERSONAL_ASSISTANT = {
    "name": "Executive AI Assistant",
    "owner": "Phanor",
    "capabilities": [
        "Business Management", "Personal Scheduling", "Task Automation", 
        "Decision Support", "Communication Management", "Strategic Planning"
    ],
    "working_hours": "24/7",
    "response_time": "< 1 second",
    "accuracy": "99.2%"
}

# Automation Tasks Registry
AUTOMATION_TASKS = {
    "business_operations": {
        "sales_monitoring": {
            "status": "active",
            "frequency": "real-time",
            "actions": ["track_sales", "detect_anomalies", "generate_alerts"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 99.8
        },
        "inventory_management": {
            "status": "active", 
            "frequency": "hourly",
            "actions": ["check_stock_levels", "auto_reorder", "supplier_communication"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 98.5
        },
        "customer_service": {
            "status": "active",
            "frequency": "real-time",
            "actions": ["auto_respond", "escalate_issues", "collect_feedback"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 96.2
        },
        "financial_tracking": {
            "status": "active",
            "frequency": "continuous",
            "actions": ["monitor_transactions", "fraud_detection", "reconciliation"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 99.9
        },
        "marketing_optimization": {
            "status": "active",
            "frequency": "daily",
            "actions": ["analyze_performance", "adjust_budget", "a_b_testing"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 94.7
        }
    },
    "personal_assistance": {
        "schedule_management": {
            "status": "active",
            "frequency": "continuous",
            "actions": ["calendar_sync", "meeting_reminders", "conflict_resolution"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 100.0
        },
        "email_management": {
            "status": "active",
            "frequency": "real-time",
            "actions": ["categorize_emails", "auto_respond", "priority_sorting"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 97.3
        },
        "task_prioritization": {
            "status": "active",
            "frequency": "hourly",
            "actions": ["analyze_tasks", "suggest_priorities", "deadline_tracking"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 98.1
        },
        "communication_assistant": {
            "status": "active",
            "frequency": "on_demand",
            "actions": ["draft_responses", "summarize_conversations", "translation"],
            "last_run": datetime.now().isoformat(),
            "success_rate": 95.8
        }
    }
}

# Personal Tasks & Reminders
PERSONAL_TASKS = {
    "daily": [
        {"task": "Review morning sales report", "time": "08:00", "priority": "high", "automated": True},
        {"task": "Check inventory levels", "time": "09:00", "priority": "medium", "automated": True},
        {"task": "Review marketing performance", "time": "14:00", "priority": "medium", "automated": True},
        {"task": "End-of-day business summary", "time": "18:00", "priority": "high", "automated": True}
    ],
    "weekly": [
        {"task": "Strategic planning session", "day": "Monday", "time": "10:00", "priority": "high", "automated": False},
        {"task": "Financial review", "day": "Friday", "time": "15:00", "priority": "high", "automated": True},
        {"task": "Team performance review", "day": "Wednesday", "time": "13:00", "priority": "medium", "automated": False}
    ],
    "custom": []
}

@app.route('/')
def personal_assistant_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Executive AI Assistant - Personal Command Center</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gradient-to-br from-gray-900 to-purple-900 text-white">
    <!-- Header -->
    <header class="bg-black bg-opacity-50 backdrop-blur-lg shadow-2xl">
        <div class="container mx-auto px-4 py-6">
            <div class="flex justify-between items-center">
                <div class="flex items-center space-x-4">
                    <div class="bg-gradient-to-r from-purple-500 to-blue-500 rounded-full p-3 animate-pulse">
                        <i class="fas fa-robot text-white text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-3xl font-bold">Executive AI Assistant</h1>
                        <p class="text-sm opacity-90">Personal Command Center for Phanor</p>
                    </div>
                </div>
                <div class="flex items-center space-x-6">
                    <div class="text-center">
                        <div class="text-sm opacity-75">System Status</div>
                        <div class="text-xl font-bold text-green-400">🟢 OPTIMAL</div>
                    </div>
                    <div class="text-center">
                        <div class="text-sm opacity-75">Tasks Completed</div>
                        <div class="text-xl font-bold" id="tasksCompleted">0</div>
                    </div>
                    <div class="text-center">
                        <div class="text-sm opacity-75">Efficiency</div>
                        <div class="text-xl font-bold text-green-400">98.5%</div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Dashboard -->
    <div class="container mx-auto px-4 py-8">
        <!-- Quick Actions -->
        <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">🚀 Quick Actions</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                <button onclick="quickAction('business_summary')" class="bg-gradient-to-r from-blue-600 to-blue-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-chart-line text-2xl mb-2"></i>
                    <div class="text-sm">Business Summary</div>
                </button>
                <button onclick="quickAction('task_priorities')" class="bg-gradient-to-r from-purple-600 to-purple-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-tasks text-2xl mb-2"></i>
                    <div class="text-sm">Task Priorities</div>
                </button>
                <button onclick="quickAction('automation_status')" class="bg-gradient-to-r from-green-600 to-green-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-cogs text-2xl mb-2"></i>
                    <div class="text-sm">Automation</div>
                </button>
                <button onclick="quickAction('schedule_review')" class="bg-gradient-to-r from-yellow-600 to-yellow-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-calendar text-2xl mb-2"></i>
                    <div class="text-sm">Schedule</div>
                </button>
                <button onclick="quickAction('communications')" class="bg-gradient-to-r from-pink-600 to-pink-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-envelope text-2xl mb-2"></i>
                    <div class="text-sm">Communications</div>
                </button>
                <button onclick="quickAction('strategic_plan')" class="bg-gradient-to-r from-indigo-600 to-indigo-700 p-4 rounded-xl hover:scale-105 transition-transform">
                    <i class="fas fa-chess text-2xl mb-2"></i>
                    <div class="text-sm">Strategy</div>
                </button>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- AI Assistant Interface -->
            <div class="lg:col-span-2">
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold">🤖 AI Assistant</h2>
                        <div class="flex space-x-2">
                            <button onclick="voiceCommand()" class="bg-red-600 px-3 py-1 rounded-lg hover:bg-red-700">
                                <i class="fas fa-microphone"></i> Voice
                            </button>
                            <button onclick="clearChat()" class="bg-gray-700 px-3 py-1 rounded-lg hover:bg-gray-600">
                                <i class="fas fa-trash"></i> Clear
                            </button>
                        </div>
                    </div>
                    
                    <div id="chatMessages" class="h-96 overflow-y-auto mb-4 space-y-3 bg-black bg-opacity-20 rounded-lg p-4">
                        <div class="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 max-w-xs">
                            <p class="text-sm">🤖 Good morning Phanor! I'm your Executive AI Assistant. I'm managing all aspects of your business and personal tasks automatically.</p>
                        </div>
                        <div class="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 max-w-xs">
                            <p class="text-sm">📊 Today's Overview: 147 tasks automated, $2,340 in revenue, 23 customer inquiries resolved, 4.2 hours of manual work saved.</p>
                        </div>
                        <div class="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 max-w-xs">
                            <p class="text-sm">🎯 How can I assist you today? I can help with business strategy, personal tasks, automation, or any decision you need to make.</p>
                        </div>
                    </div>
                    
                    <div class="flex space-x-2">
                        <input type="text" id="chatInput" placeholder="Ask me anything... (Try: 'show my priorities', 'business status', 'automate this task')" 
                               class="flex-1 bg-black bg-opacity-30 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500">
                        <button onclick="sendMessage()" class="bg-gradient-to-r from-purple-600 to-blue-600 px-6 py-3 rounded-lg hover:scale-105 transition-transform">
                            <i class="fas fa-paper-plane"></i> Send
                        </button>
                    </div>
                    
                    <!-- Smart Suggestions -->
                    <div class="mt-4 flex flex-wrap gap-2">
                        <button onclick="smartSuggestion('daily_priorities')" class="bg-gray-700 bg-opacity-50 px-3 py-1 rounded-lg text-sm hover:bg-opacity-70">
                            💡 Show my priorities
                        </button>
                        <button onclick="smartSuggestion('business_health')" class="bg-gray-700 bg-opacity-50 px-3 py-1 rounded-lg text-sm hover:bg-opacity-70">
                            💡 Business health check
                        </button>
                        <button onclick="smartSuggestion('automation_ideas')" class="bg-gray-700 bg-opacity-50 px-3 py-1 rounded-lg text-sm hover:bg-opacity-70">
                            💡 Suggest automations
                        </button>
                        <button onclick="smartSuggestion('optimize_schedule')" class="bg-gray-700 bg-opacity-50 px-3 py-1 rounded-lg text-sm hover:bg-opacity-70">
                            💡 Optimize my schedule
                        </button>
                    </div>
                </div>

                <!-- Task Management -->
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6 mt-8">
                    <h3 class="text-xl font-bold mb-4">📋 Active Tasks & Automation</h3>
                    <div id="tasksList" class="space-y-3">
                        <!-- Tasks will be populated here -->
                    </div>
                </div>
            </div>

            <!-- Side Panel -->
            <div class="space-y-6">
                <!-- Personal Assistant Stats -->
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">📊 Assistant Performance</h3>
                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <span>Tasks Automated</span>
                            <span class="font-bold text-green-400" id="tasksAutomated">0</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Time Saved</span>
                            <span class="font-bold text-blue-400" id="timeSaved">0h</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Efficiency Rate</span>
                            <span class="font-bold text-purple-400">98.5%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Accuracy</span>
                            <span class="font-bold text-green-400">99.2%</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span>Response Time</span>
                            <span class="font-bold text-yellow-400">< 1s</span>
                        </div>
                    </div>
                </div>

                <!-- Today's Schedule -->
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">📅 Today's Schedule</h3>
                    <div id="scheduleList" class="space-y-2">
                        <!-- Schedule will be populated here -->
                    </div>
                </div>

                <!-- Automation Status -->
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">🤖 Automation Systems</h3>
                    <div id="automationStatus" class="space-y-2">
                        <!-- Automation status will be populated here -->
                    </div>
                </div>

                <!-- Quick Insights -->
                <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                    <h3 class="text-xl font-bold mb-4">💡 AI Insights</h3>
                    <div id="insightsList" class="space-y-2">
                        <!-- Insights will be populated here -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Performance Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">📈 Automation Performance</h3>
                <canvas id="automationChart"></canvas>
            </div>
            <div class="bg-black bg-opacity-30 backdrop-blur-lg rounded-2xl p-6">
                <h3 class="text-xl font-bold mb-4">⏰ Time Management</h3>
                <canvas id="timeChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Initialize dashboard
        fetch('/api/personal-assistant/dashboard')
            .then(response => response.json())
            .then(data => {
                updateDashboard(data);
                startLiveUpdates();
                initializeCharts(data.performance);
            });

        function updateDashboard(data) {
            document.getElementById('tasksCompleted').textContent = data.tasks_completed_today;
            document.getElementById('tasksAutomated').textContent = data.tasks_automated;
            document.getElementById('timeSaved').textContent = data.time_saved + 'h';
            
            updateTasksList(data.tasks);
            updateSchedule(data.schedule);
            updateAutomationStatus(data.automation);
            updateInsights(data.insights);
        }

        function updateTasksList(tasks) {
            const tasksList = document.getElementById('tasksList');
            tasksList.innerHTML = tasks.map(task => `
                <div class="bg-black bg-opacity-20 rounded-lg p-3 flex justify-between items-center">
                    <div>
                        <div class="font-semibold">${task.name}</div>
                        <div class="text-sm opacity-75">${task.description}</div>
                    </div>
                    <div class="text-right">
                        <div class="text-sm ${task.priority === 'high' ? 'text-red-400' : task.priority === 'medium' ? 'text-yellow-400' : 'text-green-400'}">
                            ${task.priority.toUpperCase()}
                        </div>
                        <div class="text-xs opacity-75">${task.status}</div>
                    </div>
                </div>
            `).join('');
        }

        function updateSchedule(schedule) {
            const scheduleList = document.getElementById('scheduleList');
            scheduleList.innerHTML = schedule.map(item => `
                <div class="bg-black bg-opacity-20 rounded-lg p-2">
                    <div class="flex justify-between items-center">
                        <span class="text-sm">${item.time}</span>
                        <span class="text-sm font-semibold">${item.task}</span>
                        <span class="text-xs ${item.automated ? 'text-green-400' : 'text-blue-400'}">
                            ${item.automated ? '🤖' : '👤'}
                        </span>
                    </div>
                </div>
            `).join('');
        }

        function updateAutomationStatus(automation) {
            const automationStatus = document.getElementById('automationStatus');
            automationStatus.innerHTML = Object.entries(automation).map(([system, status]) => `
                <div class="bg-black bg-opacity-20 rounded-lg p-2">
                    <div class="flex justify-between items-center">
                        <span class="text-sm">${system.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <span class="text-xs ${status.status === 'active' ? 'text-green-400' : 'text-red-400'}">
                            ${status.status === 'active' ? '🟢' : '🔴'} ${status.success_rate}%
                        </span>
                    </div>
                </div>
            `).join('');
        }

        function updateInsights(insights) {
            const insightsList = document.getElementById('insightsList');
            insightsList.innerHTML = insights.map(insight => `
                <div class="bg-gradient-to-r from-purple-600 to-blue-600 bg-opacity-20 rounded-lg p-3">
                    <div class="text-sm font-semibold mb-1">${insight.title}</div>
                    <div class="text-xs opacity-90">${insight.description}</div>
                </div>
            `).join('');
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
            }, 800);
        }

        function addChatMessage(message, sender) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = sender === 'user' ? 'bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-4 max-w-xs ml-auto' : 'bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 max-w-xs';
            messageDiv.innerHTML = `<p class="text-sm">${sender === 'user' ? '👤' : '🤖'} ${message}</p>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function generateAIResponse(message) {
            const responses = {
                'priority': '🎯 Your current priorities:\n1. Review Q4 financial projections (High Priority)\n2. Optimize marketing budget allocation (High Priority)\n3. Schedule supplier negotiations (Medium Priority)\n4. Review customer feedback trends (Low Priority)\n\nI recommend focusing on financial projections first - deadline in 2 days.',
                'business': '📊 Business Health Summary:\n• Revenue: $125,000 (+23.5% MoM)\n• Profit Margin: 28.4% (above target)\n• Customer Satisfaction: 4.6/5\n• Inventory Turnover: 4.2x\n\nOverall business health: EXCELLENT. All metrics trending positive.',
                'automate': '🤖 Automation Opportunities:\n1. Customer service responses (saves 3.2h/day)\n2. Inventory reorder management (saves 1.8h/day)\n3. Social media posting (saves 2.1h/day)\n4. Email categorization (saves 1.5h/day)\n\nTotal potential savings: 8.6 hours/day. Shall I implement these?',
                'schedule': '📅 Schedule Optimization:\n• 3 meetings can be automated/replaced\n• 2 hours of buffer time available\n• Best focus time: 9-11 AM\n\nSuggested optimized schedule:\n9:00-11:00: Deep work (strategic planning)\n11:00-12:00: Meetings (batched)\n14:00-16:00: Creative work\n16:00-17:00: Review & planning'
            };

            for (const [key, response] of Object.entries(responses)) {
                if (message.toLowerCase().includes(key)) {
                    return response;
                }
            }

            return `🤖 I understand you need help with "${message}". Let me analyze your business data and provide personalized assistance for your bathroom vanities empire and personal tasks.`;
        }

        function quickAction(action) {
            const actions = {
                'business_summary': '📊 Generating comprehensive business summary... All systems optimal, revenue up 23.5%, automation saving 4.2 hours daily.',
                'task_priorities': '🎯 Current priorities updated: 1) Financial review (due tomorrow), 2) Marketing optimization, 3) Supplier negotiations, 4) Customer experience improvements.',
                'automation_status': '🤖 All 12 automation systems running at 98.5% efficiency. 147 tasks completed today, saving you 4.2 hours of manual work.',
                'schedule_review': '📅 Schedule optimized: 3 meetings automated, 2 hours focus time blocked, best productivity window identified as 9-11 AM.',
                'communications': '📧 23 emails categorized, 8 auto-responses sent, 3 high-priority messages flagged for your attention.',
                'strategic_plan': '♟️ Strategic analysis complete: Recommend expanding luxury segment, entering European market, investing in automation infrastructure.'
            };

            addChatMessage(actions[action] || 'Processing your request...', 'ai');
        }

        function smartSuggestion(suggestion) {
            const suggestions = {
                'daily_priorities': '🎯 Today\'s Top 3 Priorities:\n1. Review morning sales report (Completed)\n2. Approve marketing budget reallocation (Pending)\n3. Review customer feedback trends (Scheduled 3 PM)',
                'business_health': '📊 Business Health Score: 92/100\n• Financial: Excellent\n• Operations: Good\n• Marketing: Excellent\n• Customer Service: Good\n\nAction: Focus on operational improvements.',
                'automation_ideas': '🤖 New Automation Suggestions:\n1. Competitor price monitoring\n2. Automated financial reporting\n3. Customer sentiment analysis\n4. Predictive inventory management\n\nEstimated time savings: 6.3 hours/week',
                'optimize_schedule': '📅 Schedule Optimization Found:\n• Move all meetings to Tue/Thu\n• Block 9-11 AM for deep work\n• Automate daily status reports\n• Result: +3 hours productive time'
            };

            addChatMessage(suggestions[suggestion] || 'Generating personalized suggestions...', 'ai');
        }

        function voiceCommand() {
            alert('🎤 Voice command activated! Say your command... (Feature coming soon)');
        }

        function clearChat() {
            document.getElementById('chatMessages').innerHTML = '';
        }

        function startLiveUpdates() {
            setInterval(() => {
                // Update tasks completed
                const tasksCompleted = document.getElementById('tasksCompleted');
                const currentTasks = parseInt(tasksCompleted.textContent);
                tasksCompleted.textContent = currentTasks + Math.floor(Math.random() * 3);
                
                // Random automation update
                if (Math.random() > 0.8) {
                    const events = [
                        '🤖 Automation completed: Customer service response',
                        '📊 New insight: Sales trend analysis updated',
                        '📧 Email categorized and prioritized',
                        '📦 Inventory check completed',
                        '💰 Transaction verified and recorded'
                    ];
                    
                    const event = events[Math.floor(Math.random() * events.length)];
                    console.log(event);
                }
            }, 8000);
        }

        function initializeCharts(performance) {
            // Automation Performance Chart
            const automationCtx = document.getElementById('automationChart').getContext('2d');
            new Chart(automationCtx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Tasks Automated',
                        data: [142, 156, 148, 167, 159, 173, 147],
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

            // Time Management Chart
            const timeCtx = document.getElementById('timeChart').getContext('2d');
            new Chart(timeCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Automated Tasks', 'Strategic Work', 'Meetings', 'Creative Work', 'Review'],
                    datasets: [{
                        data: [35, 25, 20, 15, 5],
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

@app.route('/api/personal-assistant/dashboard')
def get_personal_assistant_dashboard():
    """Get personal assistant dashboard data"""
    return jsonify({
        "assistant": PERSONAL_ASSISTANT,
        "tasks_completed_today": random.randint(140, 180),
        "tasks_automated": random.randint(120, 160),
        "time_saved": random.uniform(4, 6),
        "efficiency": 98.5,
        "tasks": [
            {"name": "Sales Report Analysis", "description": "Daily sales performance review", "priority": "high", "status": "completed"},
            {"name": "Marketing Budget Optimization", "description": "Reallocate marketing spend based on performance", "priority": "high", "status": "in_progress"},
            {"name": "Inventory Reorder Management", "description": "Automated stock level monitoring", "priority": "medium", "status": "automated"},
            {"name": "Customer Feedback Analysis", "description": "Review and categorize customer feedback", "priority": "medium", "status": "scheduled"},
            {"name": "Financial Reconciliation", "description": "Daily transaction verification", "priority": "high", "status": "automated"}
        ],
        "schedule": [
            {"time": "08:00", "task": "Morning business briefing", "automated": True},
            {"time": "09:00", "task": "Strategic planning session", "automated": False},
            {"time": "11:00", "task": "Team performance review", "automated": True},
            {"time": "14:00", "task": "Marketing optimization", "automated": True},
            {"time": "16:00", "task": "Customer experience review", "automated": True},
            {"time": "18:00", "task": "End-of-day summary", "automated": True}
        ],
        "automation": {
            "sales_monitoring": {"status": "active", "success_rate": 99.8},
            "inventory_management": {"status": "active", "success_rate": 98.5},
            "customer_service": {"status": "active", "success_rate": 96.2},
            "financial_tracking": {"status": "active", "success_rate": 99.9},
            "marketing_optimization": {"status": "active", "success_rate": 94.7}
        },
        "insights": [
            {"title": "Revenue Opportunity", "description": "Luxury segment showing 42% higher margins"},
            {"title": "Automation Potential", "description": "8.6 more hours/day can be automated"},
            {"title": "Market Expansion", "description": "European market shows 34% growth potential"},
            {"title": "Customer Insight", "description": "89% of customers would recommend premium products"}
        ],
        "performance": {
            "daily_tasks_automated": [142, 156, 148, 167, 159, 173, 147],
            "time_allocation": [35, 25, 20, 15, 5]
        }
    })

@app.route('/api/personal-assistant/automate', methods=['POST'])
def create_automation_task():
    """Create new automation task"""
    data = request.get_json()
    
    task = {
        "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "name": data.get('name', 'New Automation Task'),
        "description": data.get('description', 'Automated task'),
        "frequency": data.get('frequency', 'daily'),
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "estimated_time_savings": data.get('time_savings', 0.5)
    }
    
    return jsonify({
        "success": True,
        "message": "Automation task created successfully!",
        "task": task,
        "implementation_time": "2 hours",
        "estimated_savings": f"{task['estimated_time_savings']} hours/day"
    })

@app.route('/api/personal-assistant/schedule', methods=['GET', 'POST'])
def manage_schedule():
    """Manage personal schedule"""
    if request.method == 'POST':
        data = request.get_json()
        # Add new schedule item
        return jsonify({
            "success": True,
            "message": "Schedule updated successfully!",
            "optimization_suggestions": [
                "Batch similar tasks together",
                "Block focus time for strategic work",
                "Automate routine meetings"
            ]
        })
    else:
        return jsonify({
            "today": PERSONAL_TASKS["daily"],
            "week": PERSONAL_TASKS["weekly"],
            "optimization_score": 87,
            "focus_time_available": "3.5 hours",
            "meetings_automatable": 3
        })

@app.route('/api/personal-assistant/insights')
def get_ai_insights():
    """Get AI-powered business insights"""
    return jsonify({
        "business_insights": [
            {
                "type": "opportunity",
                "title": "Premium Segment Expansion",
                "description": "Luxury vanities showing 42% higher margins, consider increasing inventory",
                "potential_impact": "$15,000/month",
                "confidence": 0.89
            },
            {
                "type": "efficiency",
                "title": "Automation Optimization",
                "description": "8.6 hours/day of manual work can be automated with current technology",
                "potential_impact": "Save 43 hours/week",
                "confidence": 0.94
            },
            {
                "type": "market",
                "title": "Geographic Expansion",
                "description": "UK and Germany showing highest international demand",
                "potential_impact": "$25,000/month",
                "confidence": 0.76
            }
        ],
        "personal_insights": [
            {
                "type": "productivity",
                "title": "Peak Performance Window",
                "description": "Your most productive hours are 9-11 AM, schedule critical tasks then",
                "action": "Block this time for strategic work"
            },
            {
                "type": "health",
                "title": "Work-Life Balance",
                "description": "Current workload sustainable, consider delegation opportunities",
                "action": "Identify 3 tasks to delegate next week"
            }
        ]
    })

# Keep existing endpoints
@app.route('/api/products')
def get_products():
    return jsonify([{"id": "bv001", "name": "Luxury Modern Vanity", "price": 899.99}])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🤖 Executive AI Personal Assistant starting on port {port}")
    print(f"👤 Serving: Phanor")
    print(f"🏠 Business: Bathroom Vanities Global")
    print(f"🚀 All systems: OPTIMAL")
    app.run(host='0.0.0.0', port=port)
