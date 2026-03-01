#!/usr/bin/env python3
"""
Demo script showcasing all 6 AI personas and their capabilities.
This demonstrates persona detection and routing without needing the actual Gemini API.
"""

import json

# Persona definitions (same as in ai_service.py)
PERSONAS = {
    "campaign_manager": {
        "name": "Campaign Manager",
        "emoji": "🎯",
        "description": "Manages marketing campaigns across platforms",
    },
    "stock_analyst": {
        "name": "Stock Market Analyst",
        "emoji": "📈",
        "description": "Tracks stock investments and dividends",
    },
    "learning_manager": {
        "name": "Learning & Development Manager",
        "emoji": "🎓",
        "description": "Tracks educational progress",
    },
    "financial_assistant": {
        "name": "Financial Assistant",
        "emoji": "💰",
        "description": "Logs financial transactions",
    },
    "app_customizer": {
        "name": "App Customizer",
        "emoji": "⚙️",
        "description": "Manages app settings and preferences",
    },
    "language_assistant": {
        "name": "Language Assistant",
        "emoji": "🌍",
        "description": "Provides translation and multilingual support (65+ languages)",
    }
}

# Persona detection keywords
PERSONA_KEYWORDS = {
    "campaign_manager": ["campaign", "marketing", "ads", "instagram", "facebook", "tiktok", "twitter", "platform", "pinterest"],
    "stock_analyst": ["stock", "dividend", "invest", "share", "portfolio", "market", "nasdaq"],
    "learning_manager": ["learning", "course", "education", "training", "skill", "progress", "module"],
    "financial_assistant": ["transaction", "deposit", "withdrawal", "payout", "payment", "finance", "paypal"],
    "app_customizer": ["theme", "settings", "view", "customize", "dark", "light"],
    "language_assistant": ["translate", "language", "spanish", "french", "german", "chinese", "japanese"],
}


def detect_persona(user_message: str) -> str:
    """Detects which persona should handle the request."""
    message_lower = user_message.lower()
    
    # Check for explicit persona mentions
    for persona_key, persona_data in PERSONAS.items():
        persona_name = persona_data["name"].lower()
        if persona_name in message_lower or persona_key.replace("_", " ") in message_lower:
            return persona_key
    
    # Check for keyword matches
    persona_scores = {persona: 0 for persona in PERSONAS.keys()}
    
    for persona_key, keywords in PERSONA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                persona_scores[persona_key] += 1
    
    # Return persona with highest score
    best_persona = max(persona_scores, key=persona_scores.get)
    if persona_scores[best_persona] > 0:
        return best_persona
    
    # Default fallback
    return "campaign_manager"


# Demo test cases
DEMO_REQUESTS = [
    {
        "request": "Create a new Instagram campaign called Summer Sale",
        "expected_persona": "campaign_manager"
    },
    {
        "request": "Hey Stock Analyst, log my Apple stock purchase: 10 shares at $150",
        "expected_persona": "stock_analyst"
    },
    {
        "request": "Learning Manager, update my AI Tools course to 50% progress",
        "expected_persona": "learning_manager"
    },
    {
        "request": "Log an affiliate payout of $500 via PayPal",
        "expected_persona": "financial_assistant"
    },
    {
        "request": "Set my application theme to dark mode",
        "expected_persona": "app_customizer"
    },
    {
        "request": "Language Assistant, translate this to Spanish: Hello, how are you?",
        "expected_persona": "language_assistant"
    },
    {
        "request": "I want to purchase 5 shares of Microsoft at $300 each",
        "expected_persona": "stock_analyst"
    },
    {
        "request": "Create a Facebook ad campaign for my new product launch",
        "expected_persona": "campaign_manager"
    },
    {
        "request": "Translate my campaign description to French",
        "expected_persona": "language_assistant"
    },
    {
        "request": "Record a deposit of $1000 to my account",
        "expected_persona": "financial_assistant"
    },
]


def run_demo():
    """Run demonstration of all 6 personas."""
    print("\n" + "="*80)
    print("🤖 AFFILIATE AI PRO - MULTI-PERSONA DEMO")
    print("="*80)
    print("\nThis demo shows how the AI detects and routes requests to the correct persona.")
    print("\n" + "-"*80)
    
    success_count = 0
    total_count = len(DEMO_REQUESTS)
    
    for idx, test_case in enumerate(DEMO_REQUESTS, 1):
        user_request = test_case["request"]
        expected_persona = test_case["expected_persona"]
        
        # Detect persona
        detected_persona = detect_persona(user_request)
        persona_data = PERSONAS[detected_persona]
        
        # Check if detection was correct
        is_correct = detected_persona == expected_persona
        if is_correct:
            success_count += 1
        
        # Display result
        status_icon = "✅" if is_correct else "❌"
        print(f"\n[Test {idx}/{total_count}] {status_icon}")
        print(f"User Request: \"{user_request}\"")
        print(f"Expected: {PERSONAS[expected_persona]['name']} {PERSONAS[expected_persona]['emoji']}")
        print(f"Detected: {persona_data['name']} {persona_data['emoji']}")
        
        if not is_correct:
            print(f"⚠️  Expected {expected_persona}, but got {detected_persona}")
    
    # Summary
    print("\n" + "="*80)
    print(f"RESULTS: {success_count}/{total_count} persona detections correct ({success_count/total_count*100:.1f}%)")
    print("="*80)
    
    # Show all personas
    print("\n📋 ALL AVAILABLE PERSONAS:\n")
    for persona_key, persona_data in PERSONAS.items():
        print(f"  {persona_data['emoji']} {persona_data['name']}")
        print(f"      └─ {persona_data['description']}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    run_demo()
