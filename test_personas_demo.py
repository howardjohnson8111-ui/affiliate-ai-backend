#!/usr/bin/env python3
"""
Demo script showcasing the 6-Persona Affiliate AI Pro System with Language Support
This demonstrates how each persona can be invoked and how language assistance works.
"""

import json

print("\n" + "="*80)
print("🚀 AFFILIATE AI PRO - 6 Persona Executive Assistant Demo")
print("="*80)

# Display all available personas
personas = {
    "campaign_manager": {
        "emoji": "🎯",
        "name": "Campaign Manager",
        "description": "Manage marketing campaigns across platforms",
        "examples": [
            "Create a new Instagram campaign called 'Summer Sale'",
            "Show me all my Facebook campaigns",
            "Update the Pinterest campaign to 'active' status"
        ]
    },
    "stock_analyst": {
        "emoji": "📈",
        "name": "Stock Market Analyst",
        "description": "Track investments, stocks, and dividends",
        "examples": [
            "Log my Apple stock purchase: 10 shares at $150",
            "Show me my portfolio summary",
            "Record a dividend payment of $50 from Microsoft"
        ]
    },
    "learning_manager": {
        "emoji": "🎓",
        "name": "Learning & Development Manager",
        "description": "Track courses and skill development",
        "examples": [
            "Create a new course: 'Advanced Python' from Udemy",
            "Update my 'AI Tools' module to 50% progress",
            "Show me all my learning modules"
        ]
    },
    "financial_assistant": {
        "emoji": "💰",
        "name": "Financial Assistant",
        "description": "Log all financial transactions",
        "examples": [
            "Log an affiliate payout of $500 via PayPal",
            "Record a bank deposit of $1000",
            "Log a crypto withdrawal of 0.5 BTC"
        ]
    },
    "app_customizer": {
        "emoji": "⚙️",
        "name": "App Customizer",
        "description": "Customize application settings",
        "examples": [
            "Set my theme to dark mode",
            "Change my default view to 'Transactions'",
            "Set my preferred currency to EUR"
        ]
    },
    "language_assistant": {
        "emoji": "🌍",
        "name": "Language Assistant",
        "description": "Multilingual support - 65+ languages",
        "examples": [
            "Translate 'Hello World' to Spanish",
            "Generate a campaign caption in French",
            "Set my preferred language to German"
        ]
    }
}

print("\n📋 AVAILABLE PERSONAS:\n")
for key, persona in personas.items():
    print(f"{persona['emoji']} {persona['name']}")
    print(f"   └─ {persona['description']}")
    print()

print("\n" + "="*80)
print("📚 HOW TO INVOKE EACH PERSONA:")
print("="*80 + "\n")

for key, persona in personas.items():
    print(f"{persona['emoji']} {persona['name'].upper()}")
    print(f"   • Explicit: 'Hey {persona['name']}, {persona['examples'][0]}'")
    print(f"   • Implicit: '{persona['examples'][0]}'")
    print("\n   Example Commands:")
    for i, example in enumerate(persona['examples'], 1):
        print(f"   {i}. {example}")
    print()

print("="*80)
print("🌐 LANGUAGE SUPPORT (65+ Languages):")
print("="*80 + "\n")

supported_languages = [
    ("English", "en"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de"),
    ("Italian", "it"),
    ("Portuguese", "pt"),
    ("Dutch", "nl"),
    ("Polish", "pl"),
    ("Russian", "ru"),
    ("Japanese", "ja"),
    ("Mandarin Chinese", "zh"),
    ("Korean", "ko"),
    ("Arabic", "ar"),
    ("Hindi", "hi"),
    ("Thai", "th"),
    ("Vietnamese", "vi"),
    ("Indonesian", "id"),
    ("Turkish", "tr"),
    ("Swedish", "sv"),
    ("Danish", "da"),
    # Add more as needed...
]

cols = 2
for i in range(0, len(supported_languages), cols):
    lang_group = supported_languages[i:i+cols]
    line = "   ".join([f"• {lang[0]:20} ({lang[1]})" for lang in lang_group])
    print(line)

print("\n   ... and 45+ more languages!")

print("\n" + "="*80)
print("🎯 USAGE PATTERNS:")
print("="*80 + "\n")

patterns = [
    ("Explicit Persona Invocation", [
        "Campaign Manager, create a Pinterest campaign",
        "Stock Analyst, log my dividend",
        "Learning Manager, update my progress",
        "Financial Assistant, log a transaction",
        "App Customizer, set dark mode",
        "Language Assistant, translate this to Spanish"
    ]),
    ("Implicit Persona Detection", [
        "Create a new TikTok campaign",
        "Log an Apple stock purchase",
        "Update my course progress",
        "Record an affiliate payout",
        "Change my theme to light",
        "Translate 'Good morning' to French"
    ]),
    ("Combined Actions", [
        "Create a campaign and log the marketing budget as a transaction",
        "Buy stocks and set a notification reminder",
        "Complete a learning module and get a summary in Spanish"
    ])
]

for pattern_name, examples in patterns:
    print(f"📌 {pattern_name}:")
    for example in examples:
        print(f"   • {example}")
    print()

print("="*80)
print("🔧 TOOL ROUTING:")
print("="*80 + "\n")

tool_routes = {
    "Campaign Manager": [
        "create_campaign",
        "read_campaign",
        "update_campaign",
        "delete_campaign"
    ],
    "Stock Market Analyst": [
        "create_stock",
        "read_stock",
        "update_stock",
        "delete_stock",
        "create_transaction (for stock-related)"
    ],
    "Learning & Development Manager": [
        "create_learning_module",
        "read_learning_module",
        "update_learning_module",
        "delete_learning_module"
    ],
    "Financial Assistant": [
        "create_transaction"
    ],
    "App Customizer": [
        "update_app_settings",
        "get_app_settings"
    ],
    "Language Assistant": [
        "translate_content",
        "set_language",
        "get_supported_languages"
    ]
}

for persona, tools in tool_routes.items():
    print(f"🔹 {persona}:")
    for tool in tools:
        print(f"   ├─ {tool}")
    print()

print("="*80)
print("✨ KEY FEATURES:")
print("="*80 + "\n")

features = [
    ("🤖 Intelligent Persona Detection", "System automatically detects which persona to use based on keywords"),
    ("🔀 Seamless Switching", "Switch between personas mid-conversation without re-initialization"),
    ("🌍 Multilingual Support", "Commands in any of 65+ languages, responses in your preferred language"),
    ("🎯 Specialized Tools", "Each persona has access to its specific business domain tools"),
    ("💬 Natural Language", "Communicate naturally - no special syntax required"),
    ("📊 Unified Backend", "All operations route to your Node.js API and database"),
    ("⚙️ Customizable", "Persona behaviors and tools are fully customizable"),
    ("🔄 Stateful Conversations", "Full conversation history maintained for context")
]

for emoji_title, description in features:
    print(f"{emoji_title}")
    print(f"   {description}\n")

print("="*80)
print("🚀 GETTING STARTED:")
print("="*80 + "\n")

steps = [
    ("1. Start the system", "python ai_service.py"),
    ("2. Wait for initialization", "You'll see the welcome message"),
    ("3. Invoke a persona", "Type a command like the examples above"),
    ("4. Observe persona detection", "Check the console for detected persona"),
    ("5. View tool calls", "See which tools are being invoked"),
    ("6. Get results", "Results are displayed and saved to your backend")
]

for step, instruction in steps:
    print(f"{step}: {instruction}\n")

print("="*80)
print("📝 EXAMPLE SESSION:")
print("="*80 + "\n")

example_session = [
    ("You", "Create a new Instagram campaign called 'Black Friday Sale'"),
    ("System", "[Assistant Detected]: Campaign Manager 🎯"),
    ("System", "[Campaign Manager Tool Call]: create_campaign(...)"),
    ("System", "[Tool Output]: Campaign created with ID: 1234567"),
    ("AI", "✅ I've successfully created your 'Black Friday Sale' campaign on Instagram!"),
    ("", ""),
    ("You", "Now log an affiliate payout of $1500 via PayPal"),
    ("System", "[Assistant Detected]: Financial Assistant 💰"),
    ("System", "[Financial Assistant Tool Call]: create_transaction(...)"),
    ("System", "[Tool Output]: Transaction logged successfully"),
    ("AI", "✅ Transaction recorded: $1500 affiliate payout via PayPal"),
    ("", ""),
    ("You", "Language Assistant, translate the campaign message to Spanish"),
    ("System", "[Assistant Detected]: Language Assistant 🌍"),
    ("System", "[Language Assistant Tool Call]: translate_content(...)"),
    ("AI", "✅ Here's your message in Spanish: [translated text]"),
]

for speaker, text in example_session:
    if speaker:
        print(f"[{speaker}]: {text}")
    else:
        print()

print("\n" + "="*80)
print("💡 TIPS FOR BEST RESULTS:")
print("="*80 + "\n")

tips = [
    "Be specific in your requests - mention platforms, amounts, dates",
    "Use natural language - don't worry about exact phrasing",
    "You can explicitly name a persona for clarity",
    "The system learns from context - provide relevant details",
    "All transactions are logged to your backend in real-time",
    "Language switching is instant - no setup required",
]

for i, tip in enumerate(tips, 1):
    print(f"{i}. {tip}\n")

print("="*80)
print("✅ System Ready! Your 6-Persona Executive Assistant Awaits 🚀")
print("="*80 + "\n")
