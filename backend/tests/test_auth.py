"""
Simplified test script for Phase 2 Authentication system.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_server():
    """Test if server is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        print(f"✅ Server is running! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Server is not running: {str(e)}")
        print("\nPlease start the server first with:")
        print("uvicorn app.main:app --reload")
        return False

def test_signup():
    """Test user registration."""
    print("\n" + "="*50)
    print("TEST: User Registration")
    print("="*50)
    
    # Use unique email with timestamp
    timestamp = int(time.time())
    test_data = {
        "full_name": "Test User",
        "email": f"test_{timestamp}@example.com",
        "password": "Test@123"
    }
    
    print(f"Request: POST {BASE_URL}/auth/signup")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=test_data,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Signup successful!")
            return test_data["email"], True
        else:
            print("❌ Signup failed!")
            return None, False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error! Make sure the server is running.")
        return None, False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, False

def test_login(email):
    """Test user login."""
    print("\n" + "="*50)
    print("TEST: User Login")
    print("="*50)
    
    login_data = {
        "email": email,
        "password": "Test@123"
    }
    
    print(f"Request: POST {BASE_URL}/auth/login")
    print(f"Data: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            return data.get("access_token"), True
        else:
            print("❌ Login failed!")
            return None, False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, False

def test_get_me(token):
    """Test getting current user."""
    print("\n" + "="*50)
    print("TEST: Get Current User")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Request: GET {BASE_URL}/auth/me")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Get user successful!")
            return True
        else:
            print("❌ Get user failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 2 AUTHENTICATION TESTS")
    print("="*60)
    
    # Check if server is running
    if not test_server():
        return
    
    results = []
    
    # Test 1: Signup
    email, success = test_signup()
    results.append(("Signup", success))
    
    if not email:
        print("\n❌ Test stopped due to signup failure.")
        print_results(results)
        return
    
    # Test 2: Login
    token, success = test_login(email)
    results.append(("Login", success))
    
    if not token:
        print("\n❌ Test stopped due to login failure.")
        print_results(results)
        return
    
    # Test 3: Get Current User
    success = test_get_me(token)
    results.append(("Get User", success))
    
    # Print final results
    print_results(results)

def print_results(results):
    """Print test results summary."""
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("="*60)
    print(f"Total: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Authentication is working.")
        print("\n📝 Available Auth Endpoints:")
        print("   - POST /api/v1/auth/signup  (Register)")
        print("   - POST /api/v1/auth/login   (Login)")
        print("   - GET  /api/v1/auth/me      (Profile)")
        print("\n🔒 Use Bearer token in Authorization header")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()