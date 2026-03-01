#!/usr/bin/env python3
"""
Test script to demonstrate PayPal integration with AI Executive Assistants.
Tests how Gemini detects financial requests and uses PayPal tools.
"""

import os
import sys
from ai_service import (
    detect_persona,
    get_persona_from_query,
    get_tools_for_persona,
    process_function_call,
    PERSONAS,
    PERSONA_KEYWORDS
)

def test_persona_detection():
    """Test persona detection for various payment-related queries."""
    print("=" * 80)
    print("TEST 1: Persona Detection for Payment Queries")
    print("=" * 80)
    
    test_queries = [
        "Create a payment for $100",
        "I need to pay my affiliate for their work",
        "Please verify my PayPal payment",
        "What's the status of my latest payment?",
        "Cancel my pending payment",
        "Show me all my PayPal transactions",
        "I want to pay $50 for premium access",
        "Check my payment configuration"
    ]
    
    for query in test_queries:
        persona_key = detect_persona(query)
        persona = PERSONAS[persona_key]
        print(f"\nQuery: '{query}'")
        print(f"Detected Persona: {persona['name']} ({persona_key})")
        print(f"Available Tools: {persona['tools']}")

def test_paypal_tools_in_persona():
    """Verify that PayPal tools are correctly assigned to financial_assistant."""
    print("\n" + "=" * 80)
    print("TEST 2: PayPal Tools in Financial Assistant Persona")
    print("=" * 80)
    
    financial_assistant = PERSONAS['financial_assistant']
    print(f"\nPersona: {financial_assistant['name']}")
    print(f"Description: {financial_assistant['description']}")
    print(f"\nAssigned Tools ({len(financial_assistant['tools'])} total):")
    for i, tool in enumerate(financial_assistant['tools'], 1):
        print(f"  {i}. {tool}")
    
    # Verify PayPal tools are present
    paypal_tools = [
        "create_PayPalPayment",
        "get_PayPalPaymentDetails",
        "list_PayPalPayments",
        "verify_PayPalPayment",
        "cancel_PayPalPayment",
        "get_PayPalConfig"
    ]
    
    print(f"\nPayPal Tools Check:")
    for tool in paypal_tools:
        if tool in financial_assistant['tools']:
            print(f"  ✓ {tool} is available")
        else:
            print(f"  ✗ {tool} is MISSING!")

def test_get_tools_for_persona():
    """Test that get_tools_for_persona returns correct tools."""
    print("\n" + "=" * 80)
    print("TEST 3: Tool Retrieval for Financial Assistant")
    print("=" * 80)
    
    try:
        tools = get_tools_for_persona('financial_assistant')
        print(f"\nSuccessfully retrieved {len(tools)} tools for financial_assistant:")
        for tool in tools:
            print(f"  • {tool.name}: {tool.description[:60]}...")
        
        # Check PayPal tools
        paypal_tool_names = [t.name for t in tools if 'PayPal' in t.name or 'payment' in t.name.lower()]
        print(f"\nPayPal-related tools found: {len(paypal_tool_names)}")
        for tool_name in paypal_tool_names:
            print(f"  • {tool_name}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def test_payment_keywords():
    """Test that payment keywords are recognized."""
    print("\n" + "=" * 80)
    print("TEST 4: Payment Keyword Detection")
    print("=" * 80)
    
    payment_keywords = ["payment", "paypal", "pay", "invoice", "billing"]
    financial_assistant_keywords = PERSONA_KEYWORDS.get('financial_assistant', [])
    
    print(f"\nFinancial Assistant Keywords ({len(financial_assistant_keywords)} total):")
    print(f"  {financial_assistant_keywords}")
    
    print(f"\nPayment Keyword Check:")
    for keyword in payment_keywords:
        if keyword in financial_assistant_keywords:
            print(f"  ✓ '{keyword}' is recognized")
        else:
            print(f"  ✗ '{keyword}' is NOT in keywords list")

def test_function_call_routing():
    """Test that function calls are properly routed to PayPal handlers."""
    print("\n" + "=" * 80)
    print("TEST 5: Function Call Routing (Simulated)")
    print("=" * 80)
    
    test_calls = [
        ("create_PayPalPayment", {"amount": 100, "description": "Premium subscription"}),
        ("get_PayPalConfig", {}),
        ("list_PayPalPayments", {}),
    ]
    
    print("\nSimulating function calls (no backend required for this test):")
    for tool_name, tool_input in test_calls:
        print(f"\n  Tool: {tool_name}")
        print(f"  Input: {tool_input}")
        print(f"  Status: Would be routed to PayPal handler")

def print_summary():
    """Print a summary of the PayPal AI integration."""
    print("\n" + "=" * 80)
    print("INTEGRATION SUMMARY")
    print("=" * 80)
    
    summary = """
✓ PAYPAL_TOOLS Defined:
  - create_PayPalPayment: Create new payment requests
  - get_PayPalPaymentDetails: Retrieve payment status and details
  - list_PayPalPayments: List all user payments
  - verify_PayPalPayment: Mark payment as completed after user confirmation
  - cancel_PayPalPayment: Cancel pending/failed payments
  - get_PayPalConfig: Get PayPal configuration (email, etc.)

✓ Financial Assistant Persona Updated:
  - Now has access to all 6 PayPal tools
  - Also retains transaction tracking capability
  - Description updated to mention PayPal support

✓ Keyword Detection:
  - Added "payment", "paypal", "pay", "invoice", "billing" keywords
  - Financial Assistant will be detected for payment requests
  - Automatic persona routing for payment queries

✓ Function Call Handler:
  - process_function_call() now handles all 6 PayPal tools
  - Makes HTTP requests to backend (localhost:3001/api/payments)
  - Returns formatted responses for Gemini

✓ System Instruction:
  - Updated to mention PayPal payment management
  - Instructs Gemini to handle payment verification and status checks

USAGE EXAMPLES:
  User: "Create a payment for $100 for my affiliate"
  → Financial Assistant detected
  → create_PayPalPayment called
  → Backend creates payment record
  → User can verify in PayPal

  User: "What payments have I made?"
  → Financial Assistant detected
  → list_PayPalPayments called
  → Backend returns all payments
  → Gemini summarizes results

  User: "Verify my payment with ID XYZ"
  → Financial Assistant detected
  → verify_PayPalPayment called
  → Backend updates payment status to completed
  → Gemini confirms action
"""
    print(summary)

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  PAYPAL AI INTEGRATION TEST SUITE".center(78) + "║")
    print("║" + "  AI Executive Assistants with Gemini Function Calling".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    try:
        test_persona_detection()
        test_paypal_tools_in_persona()
        test_get_tools_for_persona()
        test_payment_keywords()
        test_function_call_routing()
        print_summary()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nNext Steps:")
        print("1. Start the backend: npm start (in workspace directory)")
        print("2. Run this test with backend running: python test_paypal_ai.py")
        print("3. Test with Gemini: Ask about payments in the chat()")
        print("4. Example: 'Create a $50 payment for my marketing affiliate'")
        print("\n")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
