"""
Simple test script to verify the application works.
Run this after setting up to test all endpoints.
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root endpoint failed: {str(e)}")
        return False

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health endpoint failed: {str(e)}")
        return False

def test_ping():
    """Test the ping endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/ping", timeout=5)
        print(f"✅ Ping endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Ping endpoint failed: {str(e)}")
        return False

def test_api_root():
    """Test the API v1 root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/", timeout=5)
        print(f"✅ API v1 root: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API v1 root failed: {str(e)}")
        return False

def test_api_health():
    """Test the API v1 health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        print(f"✅ API v1 health: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API v1 health failed: {str(e)}")
        return False

def test_api_ping():
    """Test the API v1 ping endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ping", timeout=5)
        print(f"✅ API v1 ping: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API v1 ping failed: {str(e)}")
        return False

def test_swagger():
    """Test if Swagger UI loads."""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"✅ Swagger UI: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Swagger UI failed: {str(e)}")
        return False

def test_openapi():
    """Test if OpenAPI schema loads."""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        print(f"✅ OpenAPI schema: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ OpenAPI schema failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing ProfitPilot AI Pro API")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print("Make sure the server is running!")
    print("=" * 60)
    
    # Wait for server to start
    time.sleep(1)
    
    results = []
    
    print("\nRunning tests...\n")
    
    # Root endpoints (no /api/v1 prefix)
    results.append(("Root endpoint (/)", test_root()))
    results.append(("Health endpoint (/health)", test_health()))
    results.append(("Ping endpoint (/ping)", test_ping()))
    
    # API v1 endpoints (with /api/v1 prefix)
    results.append(("API v1 root (/api/v1/)", test_api_root()))
    results.append(("API v1 health (/api/v1/health)", test_api_health()))
    results.append(("API v1 ping (/api/v1/ping)", test_api_ping()))
    
    # Documentation
    results.append(("Swagger UI (/docs)", test_swagger()))
    results.append(("OpenAPI schema (/openapi.json)", test_openapi()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, test_passed in results:
        status = "✅ PASSED" if test_passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if test_passed:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Total: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 All tests passed! Phase 1 is complete and working.")
        print("\n📝 Available endpoints:")
        print("   - GET  /              (Root - Welcome message)")
        print("   - GET  /health        (Health check)")
        print("   - GET  /ping          (Ping test)")
        print("   - GET  /api/v1/       (API v1 Root)")
        print("   - GET  /api/v1/health (API v1 Health)")
        print("   - GET  /api/v1/ping   (API v1 Ping)")
        print("   - GET  /docs          (Swagger UI)")
        print("   - GET  /redoc         (ReDoc)")
        print("   - GET  /openapi.json  (OpenAPI Schema)")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)