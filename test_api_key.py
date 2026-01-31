#!/usr/bin/env python3
"""Test if API key is properly configured and Gemini connection works."""

import os
import sys

print("="*70)
print("Testing API Key Configuration")
print("="*70)

# Check if API key is set
api_key = os.getenv("GOOGLE_API_KEY", "")
if api_key:
    print("\n✅ GOOGLE_API_KEY is SET")
    print(f"   First 20 chars: {api_key[:20]}...")
    print(f"   Last 10 chars: ...{api_key[-10:]}")
    print(f"   Total length: {len(api_key)} characters")
else:
    print("\n❌ GOOGLE_API_KEY is NOT SET")
    print("   Please set it with: $env:GOOGLE_API_KEY='your-key-here'")
    sys.exit(1)

# Try importing Gemini SDK
print("\nTesting Gemini SDK import...")
try:
    import google.genai as genai
    from google.genai import types
    print("✅ Successfully imported google.genai")
except ImportError as e:
    print(f"❌ Failed to import google.genai: {e}")
    sys.exit(1)

# Try creating a client
print("\nTesting Gemini client creation...")
try:
    client = genai.Client(api_key=api_key)
    print("✅ Successfully created Gemini client")
except Exception as e:
    print(f"❌ Failed to create client: {e}")
    sys.exit(1)

# Try a simple API call
print("\nTesting simple Gemini API call...")
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say 'Hello from Gemini!' in exactly those words and nothing else."
    )
    if response and response.candidates:
        print("✅ Gemini API call successful!")
        print(f"   Response: {response.candidates[0].content.parts[0].text}")
    else:
        print("❌ Empty response from Gemini")
except Exception as e:
    print(f"❌ Gemini API call failed: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL TESTS PASSED - System is ready to use!")
print("="*70)
print("\nNext step: Run 'python ai_service.py' to start the AI assistant")
