#!/usr/bin/env python3
"""
Comprehensive Authentication Test Suite for Affiliate AI Pro
Tests all authentication flows and security protocols
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:3001/api"
TEST_EMAIL = f"testuser{int(datetime.now().timestamp())}@example.com"
TEST_PASSWORD = "TestPassword123!"

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{BLUE}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️  {text}{RESET}")

def print_test(text):
    print(f"{BLUE}▶ {text}{RESET}")

class AuthTester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.tests_passed = 0
        self.tests_failed = 0

    def test_signup(self):
        """Test user registration"""
        print_test("Testing signup...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )

            if response.status_code == 201:
                data = response.json()
                self.user_id = data["user"]["id"]
                print_success(f"User registered: {TEST_EMAIL}")
                print_info(f"User ID: {self.user_id}")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Signup failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Signup exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_login(self):
        """Test user login"""
        print_test("Testing login...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )

            if response.status_code == 200:
                data = response.json()
                self.access_token = data["session"]["access_token"]
                self.refresh_token = data["session"]["refresh_token"]
                print_success(f"Login successful for {TEST_EMAIL}")
                print_info(f"Access token: {self.access_token[:20]}...")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Login failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Login exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_invalid_login(self):
        """Test login with wrong password"""
        print_test("Testing invalid login (wrong password)...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": "WrongPassword123!"
                }
            )

            if response.status_code == 401:
                print_success("Invalid login correctly rejected (401)")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 401, got {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_protected_route_without_token(self):
        """Test accessing protected route without token"""
        print_test("Testing protected route without token...")
        
        try:
            response = requests.get(f"{BASE_URL}/campaigns")

            if response.status_code == 401:
                print_success("Protected route correctly requires authentication (401)")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 401, got {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_protected_route_with_token(self):
        """Test accessing protected route with valid token"""
        print_test("Testing protected route with valid token...")
        
        if not self.access_token:
            print_error("No access token available")
            self.tests_failed += 1
            return False

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"{BASE_URL}/campaigns", headers=headers)

            if response.status_code == 200:
                data = response.json()
                print_success("Protected route accessible with valid token (200)")
                print_info(f"Campaigns count: {data.get('count', 0)}")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 200, got {response.status_code}")
                print_error(f"Response: {response.text}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_create_campaign(self):
        """Test creating a campaign with authenticated user"""
        print_test("Testing campaign creation with auth...")
        
        if not self.access_token:
            print_error("No access token available")
            self.tests_failed += 1
            return False

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            campaign_data = {
                "name": "Test Campaign",
                "platform": "Instagram",
                "content": "Test content for authentication",
                "status": "draft"
            }
            response = requests.post(
                f"{BASE_URL}/campaigns",
                json=campaign_data,
                headers=headers
            )

            if response.status_code == 201:
                data = response.json()
                print_success("Campaign created successfully (201)")
                print_info(f"Campaign ID: {data['campaign']['id']}")
                print_info(f"Campaign user_id: {data['campaign']['user_id']}")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 201, got {response.status_code}")
                print_error(f"Response: {response.text}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_create_transaction(self):
        """Test creating a transaction with authenticated user"""
        print_test("Testing transaction creation with auth...")
        
        if not self.access_token:
            print_error("No access token available")
            self.tests_failed += 1
            return False

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            transaction_data = {
                "amount": 100.50,
                "type": "affiliate_payout",
                "description": "Test affiliate payout",
                "payment_method": "paypal",
                "status": "completed"
            }
            response = requests.post(
                f"{BASE_URL}/transactions",
                json=transaction_data,
                headers=headers
            )

            if response.status_code == 201:
                data = response.json()
                print_success("Transaction created successfully (201)")
                print_info(f"Transaction ID: {data['transaction']['id']}")
                print_info(f"Amount: ${data['transaction']['amount']}")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 201, got {response.status_code}")
                print_error(f"Response: {response.text}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_invalid_token(self):
        """Test accessing protected route with invalid token"""
        print_test("Testing protected route with invalid token...")
        
        try:
            headers = {"Authorization": "Bearer invalid.token.here"}
            response = requests.get(f"{BASE_URL}/campaigns", headers=headers)

            if response.status_code == 401:
                print_success("Invalid token correctly rejected (401)")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 401, got {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_logout(self):
        """Test logout endpoint"""
        print_test("Testing logout...")
        
        if not self.access_token:
            print_error("No access token available")
            self.tests_failed += 1
            return False

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)

            if response.status_code == 200:
                print_success("Logout successful (200)")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 200, got {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def test_health_check(self):
        """Test health check endpoint"""
        print_test("Testing health check...")
        
        try:
            response = requests.get(f"{BASE_URL}/health")

            if response.status_code == 200:
                data = response.json()
                print_success("Health check successful (200)")
                print_info(f"Server: {data['server']}")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Expected 200, got {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Exception: {str(e)}")
            self.tests_failed += 1
            return False

    def run_all_tests(self):
        """Run all authentication tests"""
        print_header("🔐 AFFILIATE AI PRO - AUTHENTICATION TEST SUITE")
        
        print_info(f"Test Email: {TEST_EMAIL}")
        print_info(f"Test Password: {TEST_PASSWORD}")
        print_info(f"API Base URL: {BASE_URL}\n")

        # Run tests in sequence
        self.test_health_check()
        self.test_signup()
        self.test_invalid_login()
        self.test_login()
        self.test_protected_route_without_token()
        self.test_protected_route_with_token()
        self.test_create_campaign()
        self.test_create_transaction()
        self.test_invalid_token()
        self.test_logout()

        # Print summary
        print_header("📊 TEST SUMMARY")
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print_success(f"Passed: {self.tests_passed}")
        if self.tests_failed > 0:
            print_error(f"Failed: {self.tests_failed}")
        print_info(f"Success Rate: {percentage:.1f}%")

        if self.tests_failed == 0:
            print_header("🎉 ALL TESTS PASSED! Security protocols are working correctly.")
            return 0
        else:
            print_header("⚠️  SOME TESTS FAILED. Review errors above.")
            return 1

if __name__ == "__main__":
    tester = AuthTester()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
