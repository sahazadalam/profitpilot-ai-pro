"""
Complete test script for Phase 4 Sales Module.
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


def test_create_product_for_sale(token):
    """Create a product to use in sales tests."""
    print_test_header("Create Product for Sale")
    
    headers = {"Authorization": f"Bearer {token}"}
    product_data = {
        "name": f"Sale Test Product {int(time.time())}",
        "category": "Electronics",
        "sku": f"ST-{int(time.time())}",
        "purchase_price": 100.00,
        "selling_price": 150.00,
        "stock": 50,
        "minimum_stock": 5,
        "status": "active"
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers=headers
    )
    
    print_response(response, 201)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Product created: {data['name']} (ID: {data['id']})")
        return data['id'], data['sku']
    return None, None


def test_create_sale(token, product_id):
    """Test 1: Create a sale."""
    print_test_header("Create Sale")
    
    headers = {"Authorization": f"Bearer {token}"}
    sale_data = {
        "product_id": product_id,
        "quantity": 2,
        "customer_name": "John Doe",
        "payment_method": "card",
        "invoice_number": f"INV-{int(time.time())}"
    }
    
    response = requests.post(
        f"{BASE_URL}/sales",
        json=sale_data,
        headers=headers
    )
    
    print_response(response, 201)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Sale created: {data['invoice_number']} (ID: {data['id']})")
        print(f"   Revenue: ${data['total_sale_amount']}")
        print(f"   Profit: ${data['profit']}")
        return data['id']
    return None


def test_get_sales(token):
    """Test 2: Get all sales."""
    print_test_header("Get All Sales")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['data'])} sales")
        return True
    return False


def test_get_sale_by_id(token, sale_id):
    """Test 3: Get sale by ID."""
    print_test_header("Get Sale by ID")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/sales/{sale_id}", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sale found: {data['invoice_number']}")
        return True
    return False


def test_get_dashboard_summary(token):
    """Test 4: Get dashboard summary."""
    print_test_header("Get Dashboard Summary")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Dashboard summary retrieved")
        print(f"   Total Products: {data['data']['total_products']}")
        print(f"   Total Sales: {data['data']['total_sales']}")
        print(f"   Revenue: ${data['data']['revenue']}")
        print(f"   Profit: ${data['data']['profit']}")
        return True
    return False


def test_top_products(token):
    """Test 5: Get top products."""
    print_test_header("Get Top Products")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/top-products", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['count']} top products")
        return True
    return False


def test_recent_sales(token):
    """Test 6: Get recent sales."""
    print_test_header("Get Recent Sales")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/recent-sales", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['count']} recent sales")
        return True
    return False


def test_revenue_chart(token):
    """Test 7: Get revenue chart data."""
    print_test_header("Get Revenue Chart")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/dashboard/revenue-chart?days=30",
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Revenue chart data retrieved")
        print(f"   Days: {len(data['data']['labels'])}")
        return True
    return False


def test_profit_summary(token):
    """Test 8: Get profit summary."""
    print_test_header("Get Profit Summary")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/profit-summary", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Profit summary retrieved")
        print(f"   Daily Profit: ${data['data']['daily']['profit']}")
        print(f"   Weekly Profit: ${data['data']['weekly']['profit']}")
        print(f"   Monthly Profit: ${data['data']['monthly']['profit']}")
        return True
    return False


def test_delete_sale_admin(token, sale_id):
    """Test 9: Delete sale as admin."""
    print_test_header("Delete Sale (Admin)")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/sales/{sale_id}", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        print("✅ Sale deleted successfully")
        return True
    return False


def test_unauthorized_access():
    """Test 10: Access without token."""
    print_test_header("Unauthorized Access")
    
    response = requests.get(f"{BASE_URL}/sales")
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    return False


def run_all_tests():
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 4 SALES TESTS")
    print("="*60)
    
    # Get admin token
    print("\n🔐 Creating admin user...")
    admin_token = create_admin_user()
    
    if not admin_token:
        print("❌ Failed to get admin token")
        return
    
    print("✅ Admin user created and logged in")
    
    results = []
    
    # Create product for testing
    product_id, product_sku = test_create_product_for_sale(admin_token)
    results.append(("Create Product", product_id is not None))
    
    if not product_id:
        print("\n❌ Test suite stopped due to product creation failure")
        print_results(results)
        return
    
    # Run sales tests
    sale_id = test_create_sale(admin_token, product_id)
    results.append(("Create Sale", sale_id is not None))
    
    if sale_id:
        # Test sales endpoints
        result = test_get_sales(admin_token)
        results.append(("Get Sales", result))
        
        result = test_get_sale_by_id(admin_token, sale_id)
        results.append(("Get Sale by ID", result))
        
        # Test dashboard endpoints
        result = test_get_dashboard_summary(admin_token)
        results.append(("Dashboard Summary", result))
        
        result = test_top_products(admin_token)
        results.append(("Top Products", result))
        
        result = test_recent_sales(admin_token)
        results.append(("Recent Sales", result))
        
        result = test_revenue_chart(admin_token)
        results.append(("Revenue Chart", result))
        
        result = test_profit_summary(admin_token)
        results.append(("Profit Summary", result))
        
        # Test delete sale
        result = test_delete_sale_admin(admin_token, sale_id)
        results.append(("Delete Sale (Admin)", result))
    else:
        print("\n❌ Test suite stopped due to sale creation failure")
    
    # Test unauthorized access
    result = test_unauthorized_access()
    results.append(("Unauthorized Access", result))
    
    print_results(results)


def print_results(results):
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
        print("\n🎉 ALL TESTS PASSED! Sales module is working perfectly.")
        print("\n📝 Available Sales & Dashboard Endpoints:")
        print("   - POST   /api/v1/sales                  (Create Sale)")
        print("   - GET    /api/v1/sales                  (List Sales)")
        print("   - GET    /api/v1/sales/{id}             (Get Sale by ID)")
        print("   - DELETE /api/v1/sales/{id}             (Delete Sale - Admin)")
        print("   - GET    /api/v1/dashboard              (Dashboard Summary)")
        print("   - GET    /api/v1/dashboard/top-products (Top Products)")
        print("   - GET    /api/v1/dashboard/recent-sales (Recent Sales)")
        print("   - GET    /api/v1/dashboard/revenue-chart (Revenue Chart)")
        print("   - GET    /api/v1/dashboard/profit-summary (Profit Summary)")
        print("\n🔒 Admin only: Delete Sale")


if __name__ == "__main__":
    run_all_tests()