#!/usr/bin/env python3
"""
Test script - Creates a campaign via the AI assistant
"""
import os
import sys

# Set API key
api_key = 'AIzaSyBpPjvvrVwVXr9MRC5lv3ZqoxbXetnLS3E'
os.environ['GOOGLE_API_KEY'] = api_key

print("=" * 70)
print("  TEST: Creating a Campaign via Gemini AI")
print("=" * 70)

from ai_service import AffiliateAIExecutive

try:
    print("\n✓ Initializing AI Executive Assistant...")
    assistant = AffiliateAIExecutive()
    
    print("\n" + "=" * 70)
    print("  Running Test Command")
    print("=" * 70)
    
    # Test command
    test_command = "Create a new Facebook campaign called Test Campaign for validation"
    print(f"\n[Command]: {test_command}\n")
    
    # Run the command
    response = assistant.chat(test_command)
    
    print("\n" + "=" * 70)
    print("  Test Complete!")
    print("=" * 70)
    print(f"\nFinal Response:\n{response}")
    
except Exception as e:
    print(f"\n✗ Test failed with error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
