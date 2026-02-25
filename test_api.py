"""
Test script for Cyber Fraud Detection System API with authentication.
Run this after starting the server with: uvicorn main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# API Keys
PUBLIC_KEY = "public123"
ADMIN_KEY = "admin123"
INVALID_KEY = "invalid123"


def test_no_api_key():
    """Test request without API key - should return 401"""
    print("\n1. Testing /analyze without API key...")
    response = requests.post(
        f"{BASE_URL}/analyze",
        json={"message_content": "Test message"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 401


def test_invalid_api_key():
    """Test request with invalid API key - should return 403"""
    print("\n2. Testing /analyze with invalid API key...")
    response = requests.post(
        f"{BASE_URL}/analyze",
        headers={"X-API-KEY": INVALID_KEY},
        json={"message_content": "Test message"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 403


def test_public_key_analyze():
    """Test /analyze with public key - should work"""
    print("\n3. Testing /analyze with public key...")
    response = requests.post(
        f"{BASE_URL}/analyze",
        headers={"X-API-KEY": PUBLIC_KEY},
        json={
            "phone_number": "555-1234",
            "message_content": "URGENT! Your bank account is suspended. Verify now!"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_public_key_admin_endpoint():
    """Test admin endpoint with public key - should return 403"""
    print("\n4. Testing /stats with public key (should fail)...")
    response = requests.get(
        f"{BASE_URL}/stats",
        headers={"X-API-KEY": PUBLIC_KEY}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 403


def test_admin_key_stats():
    """Test /stats with admin key - should work"""
    print("\n5. Testing /stats with admin key...")
    response = requests.get(
        f"{BASE_URL}/stats",
        headers={"X-API-KEY": ADMIN_KEY}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_admin_key_blacklist():
    """Test /blacklist with admin key - should work"""
    print("\n6. Testing /blacklist with admin key...")
    response = requests.get(
        f"{BASE_URL}/blacklist",
        headers={"X-API-KEY": ADMIN_KEY}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_root_endpoint():
    """Test root endpoint - no auth required"""
    print("\n7. Testing / endpoint (no auth required)...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


if __name__ == "__main__":
    print("=" * 60)
    print("Cyber Fraud Detection System - API Authentication Tests")
    print("=" * 60)
    
    try:
        test_root_endpoint()
        test_no_api_key()
        test_invalid_api_key()
        test_public_key_analyze()
        test_public_key_admin_endpoint()
        test_admin_key_stats()
        test_admin_key_blacklist()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
