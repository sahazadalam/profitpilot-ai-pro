"""
Test script for Phase 8 Intelligence Engine.
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
    
    client = pymongo.MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    users_collection = db["users"]
    
    # Signup
    admin_data = {
        "full_name": "Admin User",
        "email": admin_email,
        "password": "Test@123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=admin_data)
    if response.status_code != 201:
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


def test_customer_segments(token):
    """Test customer segmentation."""
    print_test_header("Customer Segments")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/customer-segments", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Customer segments retrieved (count: {data.get('count', 0)})")
        return True
    return False


def test_anomalies(token):
    """Test anomaly detection."""
    print_test_header("Anomaly Detection")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/anomalies", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Anomalies detected (count: {data.get('count', 0)})")
        return True
    return False


def test_simulation(token):
    """Test business simulation."""
    print_test_header("Business Simulation")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "scenario_type": "price_increase",
        "percentage": 10,
        "days": 30
    }
    
    response = requests.post(
        f"{BASE_URL}/intelligence/simulate",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Simulation completed")
        if data.get('data', {}).get('projected'):
            print(f"   Projected Revenue: ${data['data']['projected'].get('revenue', 0):,.2f}")
        return True
    return False


def test_explain(token):
    """Test explainable AI."""
    print_test_header("Explainable AI")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/explain", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        print(f"✅ Explanation generated")
        return True
    return False


def test_seasonality(token):
    """Test seasonality detection."""
    print_test_header("Seasonality Detection")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/seasonality", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Seasonality detection completed")
        if data.get('data', {}).get('has_seasonality'):
            print(f"   Seasonality: Detected")
        return True
    return False


def test_market_trends(token):
    """Test market trends."""
    print_test_header("Market Trends")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/market-trends", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Market trends generated")
        if data.get('data', {}).get('industries'):
            print(f"   Industries: {len(data['data']['industries'])}")
        return True
    return False


def test_risk_prediction(token):
    """Test risk prediction."""
    print_test_header("Risk Prediction")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/risk-prediction", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Risk prediction completed")
        if data.get('data', {}).get('overall_risk'):
            print(f"   Overall Risk: {data['data']['overall_risk'].get('level', 'Unknown')}")
        return True
    return False


def test_insights(token):
    """Test AI insights."""
    print_test_header("AI Insights")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/intelligence/insights", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Insights generated (count: {data.get('count', 0)})")
        for insight in data.get('data', [])[:3]:
            print(f"   - [{insight.get('type', 'INFO').upper()}] {insight.get('message', '')}")
        return True
    return False


def test_compare_scenarios(token):
    """Test scenario comparison."""
    print_test_header("Scenario Comparison")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "scenario_a": {"type": "price_increase", "percentage": 10},
        "scenario_b": {"type": "price_decrease", "percentage": 10},
        "days": 30
    }
    
    response = requests.post(
        f"{BASE_URL}/intelligence/compare-scenarios",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Scenario comparison completed")
        if data.get('data', {}).get('recommendation'):
            print(f"   Recommendation: {data['data']['recommendation'].get('better_scenario', 'N/A')}")
        return True
    return False


def test_unauthorized_access():
    """Test unauthorized access."""
    print_test_header("Unauthorized Access")
    
    response = requests.get(f"{BASE_URL}/intelligence/customer-segments")
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    return False


def run_all_tests():
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 8 INTELLIGENCE TESTS")
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
    result = test_customer_segments(admin_token)
    results.append(("Customer Segments", result))
    
    result = test_anomalies(admin_token)
    results.append(("Anomaly Detection", result))
    
    result = test_simulation(admin_token)
    results.append(("Business Simulation", result))
    
    result = test_explain(admin_token)
    results.append(("Explainable AI", result))
    
    result = test_seasonality(admin_token)
    results.append(("Seasonality", result))
    
    result = test_market_trends(admin_token)
    results.append(("Market Trends", result))
    
    result = test_risk_prediction(admin_token)
    results.append(("Risk Prediction", result))
    
    result = test_insights(admin_token)
    results.append(("AI Insights", result))
    
    result = test_compare_scenarios(admin_token)
    results.append(("Scenario Comparison", result))
    
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
        print("\n🎉 ALL TESTS PASSED! Intelligence engine is working.")
        print("\n📝 Available Intelligence Endpoints:")
        print("   - GET  /api/v1/intelligence/customer-segments  (Customer Segmentation)")
        print("   - GET  /api/v1/intelligence/anomalies         (Anomaly Detection)")
        print("   - POST /api/v1/intelligence/simulate          (Business Simulation)")
        print("   - GET  /api/v1/intelligence/explain           (Explainable AI)")
        print("   - GET  /api/v1/intelligence/seasonality       (Seasonality Detection)")
        print("   - GET  /api/v1/intelligence/market-trends     (Market Trends)")
        print("   - GET  /api/v1/intelligence/risk-prediction   (Risk Prediction)")
        print("   - GET  /api/v1/intelligence/insights          (AI Insights)")
        print("   - POST /api/v1/intelligence/compare-scenarios (Scenario Comparison)")
        print("\n🔒 All endpoints require JWT authentication")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()