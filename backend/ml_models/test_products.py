"""
Complete test script for Phase 3 Inventory Management.
Tests all product endpoints with various scenarios.
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"


def print_test_header(test_name: str):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"🧪 TEST: {test_name}")
    print(f"{'='*60}")


def print_response(response, expected_status=None):
    """Print response details."""
    print(f"Status: {response.status_code}")
    if expected_status:
        print(f"Expected: {expected_status}")
    try:
        data = response.json()
        print("Response:")
        print(json.dumps(data, indent=2))
    except:
        print(f"Response: {response.text}")


def login_and_get_token(email="test@example.com", password="Test@123"):
    """Login and get access token."""
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def create_admin_user():
    """Create an admin user for testing by directly setting role in database."""
    import pymongo
    from app.core.config import settings
    
    timestamp = int(time.time())
    admin_email = f"admin_{timestamp}@example.com"
    
    # Connect to MongoDB directly
    client = pymongo.MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    users_collection = db["users"]
    
    # Check if admin user already exists
    existing_admin = users_collection.find_one({"email": admin_email})
    if existing_admin:
        print(f"Admin user already exists: {admin_email}")
        token = login_and_get_token(admin_email, "Test@123")
        if token:
            return token
    
    # Step 1: Signup as regular user first
    admin_data = {
        "full_name": "Admin User",
        "email": admin_email,
        "password": "Test@123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=admin_data)
    if response.status_code != 201:
        print(f"❌ Failed to create admin user: {response.status_code}")
        print(response.text)
        return None
    
    print(f"✅ User created: {admin_email}")
    
    # Step 2: Update the user's role to admin in the database
    try:
        result = users_collection.update_one(
            {"email": admin_email},
            {"$set": {"role": "admin"}}
        )
        
        if result.modified_count > 0:
            print(f"✅ User role updated to admin: {admin_email}")
        else:
            print(f"⚠️ User role update failed or already admin")
    except Exception as e:
        print(f"❌ Failed to update user role: {str(e)}")
        return None
    
    # Step 3: Login as admin
    token = login_and_get_token(admin_email, "Test@123")
    
    if token:
        print(f"✅ Admin login successful")
        return token
    else:
        print(f"❌ Admin login failed")
        return None


def test_create_product_admin(token):
    """Test 1: Create product as admin."""
    print_test_header("Create Product - Admin")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Generate unique SKU
    sku = f"LAP-{int(time.time())}"
    
    product_data = {
        "name": f"Test Laptop {int(time.time())}",
        "description": "Test laptop for inventory",
        "category": "Electronics",
        "sku": sku,
        "supplier": "Test Supplier",
        "purchase_price": 500.00,
        "selling_price": 800.00,
        "stock": 50,
        "minimum_stock": 10,
        "status": "active",
        "image_url": "https://example.com/test.jpg"
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers=headers
    )
    
    print_response(response, 201)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Product created: {data['name']} (ID: {data['id']}, SKU: {data['sku']})")
        return data['id'], data['sku']
    else:
        print("❌ Failed to create product")
        return None, None


def test_create_product_duplicate_sku(token, original_sku):
    """Test 2: Create product with duplicate SKU."""
    print_test_header("Create Product - Duplicate SKU")
    
    headers = {"Authorization": f"Bearer {token}"}
    product_data = {
        "name": f"Duplicate Product {int(time.time())}",
        "description": "Duplicate SKU test",
        "category": "Test",
        "sku": original_sku,  # Use the original SKU to trigger duplicate
        "selling_price": 100.00,
        "stock": 10
    }
    
    print(f"Attempting to create product with existing SKU: {original_sku}")
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers=headers
    )
    
    print_response(response, 409)
    
    if response.status_code == 409:
        print("✅ Duplicate SKU blocked")
        return True
    else:
        print("❌ Duplicate SKU not blocked - This should return 409 Conflict")
        return False


def test_get_products(token):
    """Test 3: Get all products."""
    print_test_header("Get All Products")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['data'])} products")
        return True
    else:
        print("❌ Failed to get products")
        return False


def test_get_product_by_id(token, product_id):
    """Test 4: Get product by ID."""
    print_test_header("Get Product by ID")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products/{product_id}", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Product found: {data['name']}")
        return True
    else:
        print("❌ Failed to get product")
        return False


def test_update_product(token, product_id):
    """Test 5: Update product."""
    print_test_header("Update Product")
    
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "name": f"Updated Laptop {int(time.time())}",
        "selling_price": 900.00,
        "stock": 45
    }
    
    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        json=update_data,
        headers=headers
    )
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Product updated: {data['name']}")
        return True
    else:
        print("❌ Failed to update product")
        return False


def test_delete_product(token, product_id):
    """Test 6: Delete product."""
    print_test_header("Delete Product")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        print("✅ Product deleted successfully")
        return True
    else:
        print("❌ Failed to delete product")
        return False


def test_get_low_stock(token):
    """Test 7: Get low stock products."""
    print_test_header("Get Low Stock Products")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products/low-stock", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['count']} low stock products")
        return True
    else:
        print("❌ Failed to get low stock products")
        return False


def test_get_summary(token):
    """Test 8: Get product summary."""
    print_test_header("Get Product Summary")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products/summary", headers=headers)
    
    print_response(response, 200)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Summary: {json.dumps(data['data'], indent=2)}")
        return True
    else:
        print("❌ Failed to get summary")
        return False


def test_unauthorized_access():
    """Test 9: Access without token."""
    print_test_header("Unauthorized Access")
    
    response = requests.get(f"{BASE_URL}/products")
    
    print_response(response, 401)
    
    if response.status_code == 401:
        print("✅ Unauthorized access blocked")
        return True
    else:
        print("❌ Unauthorized access allowed")
        return False


def test_non_admin_create():
    """Test 10: Create product as non-admin user."""
    print_test_header("Create Product - Non-Admin")
    
    # Create regular user
    timestamp = int(time.time())
    user_data = {
        "full_name": "Regular User",
        "email": f"user_{timestamp}@example.com",
        "password": "Test@123"
    }
    
    # Signup
    response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
    if response.status_code != 201:
        print("❌ Failed to create regular user")
        return False
    
    # Login
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    
    if response.status_code != 200:
        print("❌ Failed to login as regular user")
        return False
    
    user_token = response.json().get("access_token")
    
    # Try to create product
    headers = {"Authorization": f"Bearer {user_token}"}
    product_data = {
        "name": f"User Product {int(time.time())}",
        "category": "Test",
        "sku": f"USER-{int(time.time())}",
        "selling_price": 100.00,
        "stock": 10
    }
    
    response = requests.post(
        f"{BASE_URL}/products",
        json=product_data,
        headers=headers
    )
    
    print_response(response, 403)
    
    if response.status_code == 403:
        print("✅ Non-admin creation blocked")
        return True
    else:
        print("❌ Non-admin creation allowed")
        return False


def run_all_tests():
    """Run all product tests."""
    print("\n" + "="*60)
    print("🚀 PROFITPILOT AI PRO - PHASE 3 PRODUCT TESTS")
    print("="*60)
    
    # Get admin token
    print("\n🔐 Creating admin user...")
    admin_token = create_admin_user()
    
    if not admin_token:
        print("❌ Failed to get admin token")
        return
    
    print("✅ Admin user created and logged in")
    
    results = []
    product_id = None
    product_sku = None
    
    # Run tests
    product_id, product_sku = test_create_product_admin(admin_token)
    results.append(("Create Product (Admin)", product_id is not None))
    
    if product_id and product_sku:
        # Test duplicate SKU - pass the SKU string, not the ID
        result = test_create_product_duplicate_sku(admin_token, product_sku)
        results.append(("Duplicate SKU", result))
        
        # Test get products
        result = test_get_products(admin_token)
        results.append(("Get Products", result))
        
        # Test get product by ID
        result = test_get_product_by_id(admin_token, product_id)
        results.append(("Get Product by ID", result))
        
        # Test update product
        result = test_update_product(admin_token, product_id)
        results.append(("Update Product", result))
        
        # Test low stock
        result = test_get_low_stock(admin_token)
        results.append(("Low Stock", result))
        
        # Test summary
        result = test_get_summary(admin_token)
        results.append(("Summary", result))
        
        # Test delete product
        result = test_delete_product(admin_token, product_id)
        results.append(("Delete Product", result))
    else:
        print("\n❌ Test suite stopped due to product creation failure")
    
    # Test unauthorized access
    result = test_unauthorized_access()
    results.append(("Unauthorized Access", result))
    
    # Test non-admin creation
    result = test_non_admin_create()
    results.append(("Non-Admin Creation", result))
    
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
        print("\n🎉 ALL TESTS PASSED! Inventory module is working perfectly.")
        print("\n📝 Available Product Endpoints:")
        print("   - POST   /api/v1/products              (Create - Admin only)")
        print("   - GET    /api/v1/products              (List all)")
        print("   - GET    /api/v1/products/{id}         (Get by ID)")
        print("   - PUT    /api/v1/products/{id}         (Update - Admin only)")
        print("   - DELETE /api/v1/products/{id}         (Delete - Admin only)")
        print("   - GET    /api/v1/products/low-stock    (Low stock products)")
        print("   - GET    /api/v1/products/summary      (Summary statistics)")
        print("\n🔒 Admin only endpoints require admin role")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    run_all_tests()