"""
Test script for Phase 9 AI Business Assistant.
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


def test_chat_question(token):
    """Test chat with a question."""
    print_test_header("Chat - Business Question")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "Which product is performing best?"}
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Chat response received")
            print(f"   Question: {payload['question']}")
            print(f"   Answer: {data.get('data', {}).get('answer', 'N/A')[:200]}...")
            print(f"   Confidence: {data.get('data', {}).get('confidence', 0)}%")
            return True
    return False


def test_chat_sales_question(token):
    """Test chat with a sales question."""
    print_test_header("Chat - Sales Question")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "What is my total revenue?"}
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Sales question answered")
            return True
    return False


def test_chat_forecast_question(token):
    """Test chat with a forecast question."""
    print_test_header("Chat - Forecast Question")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "Predict next month's revenue"}
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Forecast question answered")
            return True
    return False


def test_chat_inventory_question(token):
    """Test chat with an inventory question."""
    print_test_header("Chat - Inventory Question")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "What should I restock?"}
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Inventory question answered")
            return True
    return False


def test_chat_with_history(token):
    """Test chat with conversation history."""
    print_test_header("Chat - With History")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # First question
    payload1 = {"question": "Show me top products"}
    response1 = requests.post(f"{BASE_URL}/chat", json=payload1, headers=headers)
    
    if response1.status_code != 200:
        print("❌ First question failed")
        return False
    
    conversation_id = response1.json().get('data', {}).get('conversation_id')
    
    # Follow-up question
    payload2 = {"question": "Why are they performing well?", "conversation_id": conversation_id}
    response2 = requests.post(f"{BASE_URL}/chat", json=payload2, headers=headers)
    
    print_response(response2, 200)
    
    if response2.status_code == 200:
        data = response2.json()
        if data.get('success'):
            print(f"✅ Follow-up question answered with context")
            print(f"   Conversation ID: {conversation_id}")
            return True
    return False


def test_daily_report(token):
    """Test daily report."""
    print_test_header("Daily Report")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/chat/reports/daily", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Daily report generated")
            return True
    return False


def test_weekly_report(token):
    """Test weekly report."""
    print_test_header("Weekly Report")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/chat/reports/weekly", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Weekly report generated")
            return True
    return False


def test_executive_summary(token):
    """Test executive summary."""
    print_test_header("Executive Summary")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/chat/reports/executive", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Executive summary generated")
            return True
    return False


def test_alerts(token):
    """Test business alerts."""
    print_test_header("Business Alerts")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/chat/alerts", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            alert_data = data.get('data', {})
            print(f"✅ Business alerts retrieved")
            print(f"   Total Alerts: {alert_data.get('counts', {}).get('total', 0)}")
            return True
    return False


def test_action_plan(token):
    """Test action plan."""
    print_test_header("Action Plan")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/chat/action-plan", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            action_data = data.get('data', {})
            print(f"✅ Action plan generated")
            print(f"   Total Actions: {action_data.get('total_actions', 0)}")
            return True
    return False


def test_unauthorized_access():
    """Test unauthorized access."""
    print_test_header("Unauthorized Access")
    
    response = requests.post(f"{BASE_URL}/chat", json={"question": "test"})
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    return False


def run_all_tests():
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 9 CHAT TESTS")
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
    result = test_chat_question(admin_token)
    results.append(("Chat - Business Question", result))
    
    result = test_chat_sales_question(admin_token)
    results.append(("Chat - Sales Question", result))
    
    result = test_chat_forecast_question(admin_token)
    results.append(("Chat - Forecast Question", result))
    
    result = test_chat_inventory_question(admin_token)
    results.append(("Chat - Inventory Question", result))
    
    result = test_chat_with_history(admin_token)
    results.append(("Chat - With History", result))
    
    result = test_daily_report(admin_token)
    results.append(("Daily Report", result))
    
    result = test_weekly_report(admin_token)
    results.append(("Weekly Report", result))
    
    result = test_executive_summary(admin_token)
    results.append(("Executive Summary", result))
    
    result = test_alerts(admin_token)
    results.append(("Business Alerts", result))
    
    result = test_action_plan(admin_token)
    results.append(("Action Plan", result))
    
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
        print("\n🎉 ALL TESTS PASSED! AI Business Assistant is working.")
        print("\n📝 Available Chat & Report Endpoints:")
        print("   - POST /api/v1/chat                    (Chat with AI Assistant)")
        print("   - POST /api/v1/chat/query             (Chat Query Alias)")
        print("   - GET  /api/v1/chat/history           (Get Chat History)")
        print("   - DELETE /api/v1/chat/history         (Clear Chat History)")
        print("   - GET  /api/v1/chat/reports/daily     (Daily Report)")
        print("   - GET  /api/v1/chat/reports/weekly    (Weekly Report)")
        print("   - GET  /api/v1/chat/reports/monthly   (Monthly Report)")
        print("   - GET  /api/v1/chat/reports/quarterly (Quarterly Report)")
        print("   - GET  /api/v1/chat/reports/yearly    (Yearly Report)")
        print("   - GET  /api/v1/chat/reports/executive (Executive Summary)")
        print("   - GET  /api/v1/chat/alerts            (Business Alerts)")
        print("   - GET  /api/v1/chat/action-plan       (Action Plan)")
        print("\n🔒 All endpoints require JWT authentication")
        print("\n💬 The AI Business Assistant can answer questions about:")
        print("   - Business performance and metrics")
        print("   - Inventory management")
        print("   - Sales and revenue analysis")
        print("   - Profitability and growth")
        print("   - Forecasting and predictions")
        print("   - Business recommendations")
        print("   - Risk assessment")
        print("   - Business health")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()