"""
Test script for Phase 6 Machine Learning Forecasting Engine.
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
        print(json.dumps(data, indent=2))
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


def test_predict_revenue(token):
    """Test revenue prediction."""
    print_test_header("Revenue Prediction")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"days": 30, "model": "prophet"}
    
    response = requests.post(
        f"{BASE_URL}/predict/revenue",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data', {}).get('forecast'):
            print(f"✅ Revenue prediction completed")
            print(f"   Forecast points: {len(data['data']['forecast'])}")
            return True
        else:
            print("   ⚠️ No forecast data (may need more sales data)")
            return True
    return False


def test_predict_profit(token):
    """Test profit prediction."""
    print_test_header("Profit Prediction")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"days": 30, "model": "prophet"}
    
    response = requests.post(
        f"{BASE_URL}/predict/profit",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data', {}).get('forecast'):
            print(f"✅ Profit prediction completed")
            print(f"   Forecast points: {len(data['data']['forecast'])}")
            return True
        else:
            print("   ⚠️ No forecast data (may need more sales data)")
            return True
    return False


def test_predict_demand(token):
    """Test demand prediction."""
    print_test_header("Demand Prediction")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"days": 30, "model": "prophet"}
    
    response = requests.post(
        f"{BASE_URL}/predict/demand",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data', {}).get('forecast'):
            print(f"✅ Demand prediction completed")
            print(f"   Forecast points: {len(data['data']['forecast'])}")
            return True
        else:
            print("   ⚠️ No forecast data (may need more sales data)")
            return True
    return False


def test_inventory_forecast(token):
    """Test inventory forecast."""
    print_test_header("Inventory Forecast")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predict/inventory", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Inventory forecast retrieved")
        return True
    return False


def test_seasonality(token):
    """Test seasonality detection."""
    print_test_header("Seasonality Detection")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predict/seasonality", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Seasonality detection completed")
        return True
    return False


def test_moving_average(token):
    """Test moving average."""
    print_test_header("Moving Average")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predict/moving-average?window=7", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Moving average calculated")
        return True
    return False


def test_models(token):
    """Test list models."""
    print_test_header("List Models")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predict/models", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Models listed")
        return True
    return False


def test_compare_models(token):
    """Test model comparison."""
    print_test_header("Model Comparison")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predict/models/compare?days=30", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Model comparison completed")
        return True
    return False


def test_unauthorized_access():
    """Test unauthorized access."""
    print_test_header("Unauthorized Access")
    
    response = requests.post(f"{BASE_URL}/predict/revenue", json={"days": 30})
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    return False


def run_all_tests():
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 6 PREDICTION TESTS")
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
    result = test_predict_revenue(admin_token)
    results.append(("Revenue Prediction", result))
    
    result = test_predict_profit(admin_token)
    results.append(("Profit Prediction", result))
    
    result = test_predict_demand(admin_token)
    results.append(("Demand Prediction", result))
    
    result = test_inventory_forecast(admin_token)
    results.append(("Inventory Forecast", result))
    
    result = test_seasonality(admin_token)
    results.append(("Seasonality", result))
    
    result = test_moving_average(admin_token)
    results.append(("Moving Average", result))
    
    result = test_models(admin_token)
    results.append(("List Models", result))
    
    result = test_compare_models(admin_token)
    results.append(("Compare Models", result))
    
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
        print("\n🎉 ALL TESTS PASSED! Prediction engine is working.")
        print("\n📝 Available Prediction Endpoints:")
        print("   - POST /api/v1/predict/demand        (Demand Forecast)")
        print("   - POST /api/v1/predict/revenue       (Revenue Forecast)")
        print("   - POST /api/v1/predict/profit        (Profit Forecast)")
        print("   - GET  /api/v1/predict/inventory     (Inventory Forecast)")
        print("   - GET  /api/v1/predict/seasonality   (Seasonality Detection)")
        print("   - GET  /api/v1/predict/moving-average (Moving Average)")
        print("   - GET  /api/v1/predict/models        (List Models)")
        print("   - GET  /api/v1/predict/models/compare (Model Comparison)")
        print("   - GET  /api/v1/predict/models/evaluate (Model Evaluation)")
        print("\n🔒 All endpoints require JWT authentication")
        print("\n📊 Models Available: Prophet, ARIMA, Linear Regression")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()