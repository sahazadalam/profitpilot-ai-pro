"""
Test script for Phase 7 Recommendation Engine.
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"


def print_test_header(test_name: str):
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*60}")


def print_response(response, expected_status=None):
    print(f"Status: {response.status_code}")
    if expected_status:
        print(f"Expected: {expected_status}")
    try:
        data = response.json()
        print("Response:")
        print(json.dumps(data, indent=2)[:800] + "..." if len(json.dumps(data)) > 800 else json.dumps(data, indent=2))
    except:
        print(f"Response: {response.text}")


def create_admin_user():
    """Create an admin user for testing."""
    import pymongo
    from app.core.config import settings
    
    timestamp = int(time.time())
    admin_email = f"admin_{timestamp}@example.com"
    
    try:
        client = pymongo.MongoClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        users_collection = db["users"]
    except:
        print("❌ Could not connect to MongoDB")
        return None
    
    # Signup
    admin_data = {
        "full_name": "Admin User",
        "email": admin_email,
        "password": "Test@123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=admin_data)
    if response.status_code != 201:
        print(f"❌ Signup failed: {response.status_code}")
        return None
    
    # Update role to admin
    users_collection.update_one(
        {"email": admin_email},
        {"$set": {"role": "admin"}}
    )
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": admin_email,
        "password": "Test@123"
    })
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def test_restock(token):
    """Test restock recommendations."""
    print_test_header("Restock Recommendations")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/restock", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        # Check if we got a response, even if empty
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Restock recommendations retrieved (count: {count})")
            return True
        else:
            print("❌ Response indicated failure")
            return False
    else:
        print(f"❌ Failed with status: {response.status_code}")
        return False


def test_pricing(token):
    """Test pricing recommendations."""
    print_test_header("Pricing Recommendations")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/pricing", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Pricing recommendations retrieved (count: {count})")
            return True
        return False
    return False


def test_dead_stock(token):
    """Test dead stock analysis."""
    print_test_header("Dead Stock Analysis")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/dead-stock", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Dead stock analysis completed (count: {count})")
            return True
        return False
    return False


def test_loss_products(token):
    """Test loss products analysis."""
    print_test_header("Loss Products Analysis")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/loss-products", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Loss products analysis completed (count: {count})")
            return True
        return False
    return False


def test_bundles(token):
    """Test bundle recommendations."""
    print_test_header("Bundle Recommendations")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/bundles", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Bundle recommendations retrieved (count: {count})")
            return True
        return False
    return False


def test_performance(token):
    """Test performance scores."""
    print_test_header("Performance Scores")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/performance", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Performance scores retrieved (count: {count})")
            if data.get('data') and len(data['data']) > 0:
                top = data['data'][0]
                print(f"   Top Product: {top.get('product_name', 'Unknown')} - Score: {top.get('score', 0)}/100")
            return True
        else:
            print(f"❌ API returned success=False")
            return False
    else:
        print(f"❌ Failed with status: {response.status_code}")
        return False


def test_business_risk(token):
    """Test business risk analysis."""
    print_test_header("Business Risk Analysis")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/business-risk", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            risk_data = data.get('data', {})
            print(f"✅ Business risk analysis completed")
            print(f"   Risk Score: {risk_data.get('risk_score', 'N/A')}")
            print(f"   Risk Level: {risk_data.get('risk_level', 'Unknown')}")
            return True
        return False
    return False


def test_optimization(token):
    """Test optimization suggestions."""
    print_test_header("Optimization Suggestions")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/optimization", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            count = data.get('count', 0)
            print(f"✅ Optimization suggestions retrieved (count: {count})")
            return True
        return False
    return False


def test_executive_summary(token):
    """Test executive summary."""
    print_test_header("Executive Summary")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/recommend/executive-summary", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success') == True:
            summary_data = data.get('data', {})
            print(f"✅ Executive summary generated")
            print(f"   Total Recommendations: {summary_data.get('total_recommendations', 0)}")
            print(f"   Business Risk: {summary_data.get('business_risk', 'Unknown')}")
            return True
        else:
            print(f"❌ API returned success=False")
            return False
    else:
        print(f"❌ Failed with status: {response.status_code}")
        return False


def test_unauthorized_access():
    """Test unauthorized access."""
    print_test_header("Unauthorized Access")
    
    response = requests.get(f"{BASE_URL}/recommend/restock")
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    return False


def run_all_tests():
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 7 RECOMMENDATION TESTS")
    print("="*60)
    
    # Get admin token
    print("\n🔐 Creating admin user...")
    admin_token = create_admin_user()
    
    if not admin_token:
        print("❌ Failed to get admin token")
        return
    
    print("✅ Admin user created and logged in")
    
    results = []
    
    # Run tests
    result = test_restock(admin_token)
    results.append(("Restock Recommendations", result))
    
    result = test_pricing(admin_token)
    results.append(("Pricing Recommendations", result))
    
    result = test_dead_stock(admin_token)
    results.append(("Dead Stock", result))
    
    result = test_loss_products(admin_token)
    results.append(("Loss Products", result))
    
    result = test_bundles(admin_token)
    results.append(("Bundle Recommendations", result))
    
    result = test_performance(admin_token)
    results.append(("Performance Scores", result))
    
    result = test_business_risk(admin_token)
    results.append(("Business Risk", result))
    
    result = test_optimization(admin_token)
    results.append(("Optimization Suggestions", result))
    
    result = test_executive_summary(admin_token)
    results.append(("Executive Summary", result))
    
    result = test_unauthorized_access()
    results.append(("Unauthorized Access", result))
    
    # Print summary
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
        print("\n🎉 ALL TESTS PASSED! Recommendation engine is working.")
        print("\n📝 Available Recommendation Endpoints:")
        print("   - GET /api/v1/recommend/restock        (Restock Recommendations)")
        print("   - GET /api/v1/recommend/pricing        (Pricing Recommendations)")
        print("   - GET /api/v1/recommend/dead-stock     (Dead Stock Analysis)")
        print("   - GET /api/v1/recommend/loss-products  (Loss Products)")
        print("   - GET /api/v1/recommend/bundles        (Bundle Recommendations)")
        print("   - GET /api/v1/recommend/performance    (Performance Scores)")
        print("   - GET /api/v1/recommend/business-risk  (Business Risk)")
        print("   - GET /api/v1/recommend/optimization   (Optimization Suggestions)")
        print("   - GET /api/v1/recommend/executive-summary (Executive Summary)")
        print("\n🔒 All endpoints require JWT authentication")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()