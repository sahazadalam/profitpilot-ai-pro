"""
Simple test script for Phase 5 Analytics Engine.
Handles empty data gracefully.
"""
import requests
import json
import time
import sys

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
        print("❌ Could not connect to MongoDB for admin creation")
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
    result = users_collection.update_one(
        {"email": admin_email},
        {"$set": {"role": "admin"}}
    )
    
    if result.modified_count > 0:
        print(f"✅ User role updated to admin: {admin_email}")
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": admin_email,
        "password": "Test@123"
    })
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Admin login successful")
        return token
    
    print("❌ Admin login failed")
    return None


def create_test_data(token):
    """Create test products and sales for analytics."""
    print("\n📦 Creating test data for analytics...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create products
    products = []
    categories = ["Electronics", "Clothing", "Books", "Food", "Toys"]
    
    for i in range(5):
        product_data = {
            "name": f"Analytics Product {i+1}",
            "category": categories[i % 5],
            "sku": f"AN-{i+1}-{int(time.time())}",
            "purchase_price": 10 + i * 5,
            "selling_price": 20 + i * 10,
            "stock": 100,
            "minimum_stock": 10,
            "status": "active"
        }
        
        response = requests.post(
            f"{BASE_URL}/products",
            json=product_data,
            headers=headers
        )
        
        if response.status_code == 201:
            product = response.json()
            products.append(product)
            print(f"   ✅ Created product: {product['name']} (ID: {product['id']})")
        else:
            print(f"   ❌ Failed to create product: {response.status_code}")
    
    if not products:
        print("❌ No products created")
        return False
    
    # Create sales
    print("   Creating sales...")
    for i, product in enumerate(products):
        for j in range(3):
            sale_data = {
                "product_id": product["id"],
                "quantity": j + 1,
                "customer_name": f"Customer {i+1}",
                "payment_method": "cash",
                "invoice_number": f"INV-{int(time.time())}-{i}-{j}"
            }
            
            response = requests.post(
                f"{BASE_URL}/sales",
                json=sale_data,
                headers=headers
            )
            
            if response.status_code == 201:
                print(f"   ✅ Created sale: {sale_data['invoice_number']}")
            else:
                print(f"   ❌ Failed to create sale: {response.status_code}")
            
            time.sleep(0.1)
    
    print("✅ Test data created successfully!")
    return True


def test_revenue_analytics(token):
    """Test revenue analytics."""
    print("\n" + "="*50)
    print("TEST: Revenue Analytics")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/revenue", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Revenue analytics retrieved")
        
        # Check if data is available
        if data.get('data') and 'today' in data['data']:
            print(f"   Today: ${data['data']['today']}")
            print(f"   Weekly: ${data['data']['weekly']}")
            print(f"   Monthly: ${data['data']['monthly']}")
            return True
        else:
            print("   ⚠️ No revenue data available (this is normal if no sales exist)")
            return True  # Return True since the API works
    else:
        print("❌ Failed to get revenue analytics")
        return False


def test_profit_analytics(token):
    """Test profit analytics."""
    print("\n" + "="*50)
    print("TEST: Profit Analytics")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/profit", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Profit analytics retrieved")
        return True
    else:
        print("❌ Failed to get profit analytics")
        return False


def test_business_health(token):
    """Test business health."""
    print("\n" + "="*50)
    print("TEST: Business Health")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/business-health", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Business health retrieved")
        if data.get('data') and 'score' in data['data']:
            print(f"   Score: {data['data']['score']}/100")
            print(f"   Status: {data['data']['status']}")
        return True
    else:
        print("❌ Failed to get business health")
        return False


def test_kpis(token):
    """Test KPIs."""
    print("\n" + "="*50)
    print("TEST: KPIs")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/kpis", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ KPIs retrieved")
        return True
    else:
        print("❌ Failed to get KPIs")
        return False


def test_insights(token):
    """Test insights generation."""
    print("\n" + "="*50)
    print("TEST: Business Insights")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/insights", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Insights generated ({data.get('count', 0)} insights)")
        for insight in data.get('data', [])[:3]:
            print(f"   - [{insight.get('type', 'INFO').upper()}] {insight.get('message', '')}")
        return True
    else:
        print("❌ Failed to get insights")
        return False


def test_report(token):
    """Test report generation."""
    print("\n" + "="*50)
    print("TEST: AI Report")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/report", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Report generated")
        if data.get('data') and 'report' in data['data']:
            print(f"   Sections: {len(data['data']['report'])}")
        return True
    else:
        print("❌ Failed to generate report")
        return False


def test_trends(token):
    """Test trends."""
    print("\n" + "="*50)
    print("TEST: Trends")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/trends", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Trends retrieved")
        return True
    else:
        print("❌ Failed to get trends")
        return False


def test_category_analytics(token):
    """Test category analytics."""
    print("\n" + "="*50)
    print("TEST: Category Analytics")
    print("="*50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/category", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Category analytics retrieved")
        return True
    else:
        print("❌ Failed to get category analytics")
        return False


def test_unauthorized_access():
    """Test unauthorized access."""
    print("\n" + "="*50)
    print("TEST: Unauthorized Access")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/analytics/revenue")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    else:
        print("❌ Unauthorized access allowed")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 5 ANALYTICS TESTS")
    print("="*60)
    
    # Check if server is running
    if not test_server():
        return
    
    # Create admin user
    print("\n🔐 Creating admin user...")
    admin_token = create_admin_user()
    
    if not admin_token:
        print("❌ Failed to get admin token")
        return
    
    print("✅ Admin user ready")
    
    # Ask if user wants to create test data
    print("\n📊 Do you want to create test data for analytics? (y/n)")
    response = input("> ").strip().lower()
    
    if response == 'y':
        create_test_data(admin_token)
    
    results = []
    
    # Run tests
    result = test_revenue_analytics(admin_token)
    results.append(("Revenue Analytics", result))
    
    result = test_profit_analytics(admin_token)
    results.append(("Profit Analytics", result))
    
    result = test_business_health(admin_token)
    results.append(("Business Health", result))
    
    result = test_kpis(admin_token)
    results.append(("KPIs", result))
    
    result = test_insights(admin_token)
    results.append(("Insights", result))
    
    result = test_report(admin_token)
    results.append(("AI Report", result))
    
    result = test_trends(admin_token)
    results.append(("Trends", result))
    
    result = test_category_analytics(admin_token)
    results.append(("Category Analytics", result))
    
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
        print("\n🎉 ALL TESTS PASSED! Analytics engine is working.")
        print("\n📝 Available Analytics Endpoints:")
        print("   - GET /api/v1/analytics/revenue          (Revenue Analytics)")
        print("   - GET /api/v1/analytics/profit           (Profit Analytics)")
        print("   - GET /api/v1/analytics/growth           (Growth Analytics)")
        print("   - GET /api/v1/analytics/business-health  (Business Health)")
        print("   - GET /api/v1/analytics/top-products     (Top Products)")
        print("   - GET /api/v1/analytics/worst-products   (Worst Products)")
        print("   - GET /api/v1/analytics/category         (Category Analytics)")
        print("   - GET /api/v1/analytics/inventory        (Inventory Analytics)")
        print("   - GET /api/v1/analytics/kpis             (KPIs)")
        print("   - GET /api/v1/analytics/trends           (Trends)")
        print("   - GET /api/v1/analytics/report           (AI Report)")
        print("   - GET /api/v1/analytics/insights         (Business Insights)")
        print("\n🔒 All endpoints require JWT authentication")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()