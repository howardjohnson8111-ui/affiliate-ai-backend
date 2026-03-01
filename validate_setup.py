#!/usr/bin/env python3
"""
End-to-End Validation Script for Gemini API Backend
Validates: API key, SDK, Node backend, and full integration
"""

import os
import sys
import requests
import json
import subprocess
from datetime import datetime

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_status(condition, message):
    """Print a checkmark or X based on condition"""
    status = "✓ PASS" if condition else "✗ FAIL"
    print(f"  [{status}] {message}")
    return condition

# ============ STEP 1: Environment & SDK ============
print_section("STEP 1: Verify Environment & SDK")

# Check API Key
api_key_set = bool(os.getenv("GOOGLE_API_KEY"))
check_status(api_key_set, "GOOGLE_API_KEY environment variable is set")
if not api_key_set:
    print("\n  ⚠️  ACTION REQUIRED:")
    print("     Windows (PowerShell): $env:GOOGLE_API_KEY = 'your-api-key'")
    print("     Windows (CMD): set GOOGLE_API_KEY=your-api-key")
    print("     Linux/Mac: export GOOGLE_API_KEY='your-api-key'\n")

# Check Python version
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
check_status(True, f"Python version: {python_version}")

# Check installed packages
print("\n  Checking Google AI SDK...")
try:
    import google.genai as genai
    from google.genai import types
    print(f"    ✓ google.genai imported successfully")
    print(f"    ✓ google.genai.types imported successfully")
    check_status(True, "Google Generative AI SDK is installed")
except ImportError as e:
    check_status(False, f"Google Generative AI SDK: {e}")
    print("\n  ⚠️  ACTION REQUIRED:")
    print("     Install: pip install google-genai")
    sys.exit(1)

# Check requests package
try:
    import requests
    check_status(True, "Requests library is installed")
except ImportError:
    check_status(False, "Requests library not found")
    print("\n  ⚠️  ACTION REQUIRED:")
    print("     Install: pip install requests")
    sys.exit(1)

# ============ STEP 2: Node Backend Health Check ============
print_section("STEP 2: Test Node Backend Health Check")

node_url = "http://localhost:3001"
node_campaigns_url = f"{node_url}/api/campaigns"

try:
    response = requests.get(node_campaigns_url, timeout=5)
    node_running = response.status_code in [200, 404]
    check_status(node_running, f"Node backend is running at {node_url}")
except requests.exceptions.ConnectionError:
    check_status(False, f"Cannot connect to Node backend at {node_url}")
    print("\n  ⚠️  ACTION REQUIRED:")
    print("     Start Node server: npm start (in server.js directory)")
    print("     Or: node server.js")
except requests.exceptions.Timeout:
    check_status(False, f"Node backend timeout at {node_url}")

# ============ STEP 3: Smoke Test - Campaign Creation ============
print_section("STEP 3: Smoke Test - Campaign Creation via HTTP")

test_campaign = {
    "name": "Test Campaign - Validation",
    "platform": "Facebook",
    "affiliate_link": "https://example.com/affiliate",
    "content": "Test content for validation",
    "status": "draft",
    "tags": ["validation", "test"]
}

try:
    print(f"  Sending POST request to {node_campaigns_url}")
    print(f"  Payload: {json.dumps(test_campaign, indent=2)}\n")
    
    response = requests.post(node_campaigns_url, json=test_campaign, timeout=5)
    
    if response.status_code == 201:
        campaign = response.json()
        check_status(True, f"Campaign created successfully with ID: {campaign.get('id')}")
        print(f"    Created campaign: {json.dumps(campaign, indent=4)}")
    else:
        check_status(False, f"Campaign creation failed with status {response.status_code}")
        print(f"    Response: {response.text}")
except requests.exceptions.RequestException as e:
    check_status(False, f"Campaign creation request failed: {e}")

# ============ STEP 4: Inspect Gemini SDK ============
print_section("STEP 4: Inspect Gemini SDK Function Signatures")

try:
    # Try to access the SDK's type structures
    tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="test_function",
                description="Test function to verify SDK structure",
                parameters=types.Schema(
                    type_="OBJECT",
                    properties={
                        "param1": types.Schema(type_="STRING", description="Test parameter")
                    }
                )
            )
        ]
    )
    check_status(True, "types.Tool and function_declarations are valid")
    check_status(True, "types.FunctionDeclaration is accessible")
    check_status(True, "types.Schema type definition works")
    
except Exception as e:
    check_status(False, f"Gemini SDK type validation failed: {e}")
    print(f"\n  ⚠️  SDK Structure Issue: {e}")

# ============ STEP 5: Quick Checklist ============
print_section("STEP 5: Quick Verification Checklist")

checklist = [
    (api_key_set, "GOOGLE_API_KEY is set in environment"),
    (True, f"Python interpreter: {sys.executable}"),
    (node_running if 'node_running' in locals() else False, 
     f"Node backend running at http://localhost:3001"),
]

all_passed = True
for condition, message in checklist:
    if not check_status(condition, message):
        all_passed = False

# ============ FINAL SUMMARY ============
print_section("VALIDATION SUMMARY")

if all_passed and api_key_set and node_running:
    print("  ✅ All basic checks PASSED!")
    print("\n  Next Steps:")
    print("    1. Run the interactive assistant:")
    print("       python ai_service.py")
    print("    2. Try a simple command:")
    print("       'Create a new Facebook campaign called Test Campaign'")
    print("    3. Monitor logs for:")
    print("       - Function call from Gemini")
    print("       - HTTP POST to Node backend")
    print("       - Supabase storage (if configured)")
    print("       - Final text response from Gemini\n")
else:
    print("  ⚠️  Some checks FAILED - see above for action items\n")

print(f"  Validation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
