"""
Test script to verify registration endpoint is working
"""
import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration with valid password"""
    
    # Test data
    test_user = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    
    print("Testing registration endpoint...")
    print(f"URL: {API_BASE_URL}/register")
    print(f"Data: {json.dumps(test_user, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✅ Registration successful!")
        else:
            print(f"\n❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend!")
        print("Make sure the backend is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_registration()
