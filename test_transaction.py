#!/usr/bin/env python3
"""
Simple test script to verify transaction endpoints are working
without requiring the Gemini API key
"""

import requests
import json

BASE_URL = "http://localhost:3001/api"

def test_create_transaction():
    """Test creating a transaction"""
    print("\n" + "="*70)
    print("TEST: Create a transaction (affiliate payout)")
    print("="*70)
    
    transaction_data = {
        "amount": 500,
        "type": "affiliate_payout",
        "description": "January commissions",
        "payment_method": "paypal",
        "status": "completed"
    }
    
    print(f"\nSending POST request to {BASE_URL}/transactions")
    print(f"Payload: {json.dumps(transaction_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/transactions", json=transaction_data)
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_all_transactions():
    """Test retrieving all transactions"""
    print("\n" + "="*70)
    print("TEST: Get all transactions")
    print("="*70)
    
    print(f"\nSending GET request to {BASE_URL}/transactions")
    
    try:
        response = requests.get(f"{BASE_URL}/transactions")
        print(f"\n✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"Response ({len(data)} transaction(s)):")
        print(json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("\n🚀 Testing Transaction Endpoints")
    print("="*70)
    
    # Create a transaction
    created = test_create_transaction()
    
    # Get all transactions
    all_trans = test_get_all_transactions()
    
    print("\n" + "="*70)
    print("✅ Transaction endpoint tests completed!")
    print("="*70 + "\n")
