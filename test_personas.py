#!/usr/bin/env python3
"""
Persona Routing Test - Demonstrates the multi-persona AI system.
This tests the persona detection and tool routing without requiring the Gemini API key.
"""

import sys
sys.path.insert(0, '/c/Users/demon/Desktop/Gemini_api_backend')

from ai_service import detect_persona, PERSONAS, get_tools_for_persona

def test_persona_detection():
    """Test persona detection with various user inputs"""
    
    test_inputs = [
        "Create a new Instagram campaign called Summer Sale",
        "Hey Stock Analyst, show me my portfolio",
        "Learning Manager, update my progress on Python course to 75%",
        "Log an affiliate payout of $500 via PayPal",
        "I want to buy 10 shares of Apple at $150 each",
        "Set my app theme to dark mode",
        "Show me all my campaigns",
        "How much have I earned from dividends this year?",
        "I completed a course on Data Science",
        "Campaign Manager, let's create a TikTok viral marketing campaign"
    ]
    
    print("\n" + "="*80)
    print("MULTI-PERSONA AI ASSISTANT - Persona Detection Test")
    print("="*80)
    
    for user_input in test_inputs:
        detected_persona_key = detect_persona(user_input)
        persona_data = PERSONAS[detected_persona_key]
        persona_tools = get_tools_for_persona(detected_persona_key)
        
        print(f"\n{'─'*80}")
        print(f"User Input: '{user_input}'")
        print(f"{'─'*80}")
        print(f"Detected Persona: {persona_data['name']}")
        print(f"Description: {persona_data['description']}")
        print(f"Available Tools ({len(persona_tools)}):")
        for tool in persona_tools:
            print(f"  • {tool.name}: {tool.description[:60]}...")
        
    print(f"\n{'='*80}")
    print("✅ Persona detection test completed successfully!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    test_persona_detection()
