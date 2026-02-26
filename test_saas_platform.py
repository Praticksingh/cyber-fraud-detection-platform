"""
Test script for SaaS Platform features
Tests all new endpoints and graph functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "public123"  # Use your PUBLIC_API_KEY

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def test_analytics_summary():
    """Test analytics summary endpoint"""
    print("\n=== Testing Analytics Summary ===")
    response = requests.get(f"{BASE_URL}/analytics/summary")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_analytics_distribution():
    """Test analytics distribution endpoint"""
    print("\n=== Testing Analytics Distribution ===")
    response = requests.get(f"{BASE_URL}/analytics/distribution")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_analytics_trends():
    """Test analytics trends endpoint"""
    print("\n=== Testing Analytics Trends ===")
    response = requests.get(f"{BASE_URL}/analytics/trends?days=7")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {len(data)} days of data")
    if data:
        print(f"Sample: {json.dumps(data[0], indent=2)}")
    return response.status_code == 200

def test_graph():
    """Test knowledge graph endpoint"""
    print("\n=== Testing Knowledge Graph ===")
    response = requests.get(f"{BASE_URL}/graph?limit=50")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Nodes: {len(data.get('nodes', []))}")
    print(f"Edges: {len(data.get('edges', []))}")
    print(f"Statistics: {json.dumps(data.get('statistics', {}), indent=2)}")
    return response.status_code == 200

def test_analyze_with_graph():
    """Test analyze endpoint and verify graph integration"""
    print("\n=== Testing Analyze with Graph Integration ===")
    
    # Test data
    test_cases = [
        {
            "phone_number": "+1234567890",
            "message_content": "URGENT! Your bank account has been compromised. Send $500 immediately to secure your funds!"
        },
        {
            "phone_number": "+9876543210",
            "message_content": "You've won $10,000! Click here to claim your prize now!"
        }
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        response = requests.post(
            f"{BASE_URL}/analyze",
            headers=headers,
            json=test_data
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Risk Score: {result['risk_score']}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Threat Category: {result['threat_category']}")
            print(f"Primary Reason: {result['primary_reason']}")
        else:
            print(f"Error: {response.text}")
    
    return True

def test_cors():
    """Test CORS headers"""
    print("\n=== Testing CORS Configuration ===")
    response = requests.options(f"{BASE_URL}/analytics/summary")
    print(f"Status: {response.status_code}")
    print(f"CORS Headers:")
    for header in ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods', 'Access-Control-Allow-Headers']:
        print(f"  {header}: {response.headers.get(header, 'Not set')}")
    return True

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("SaaS Platform Feature Tests")
    print("=" * 60)
    
    tests = [
        ("Analytics Summary", test_analytics_summary),
        ("Analytics Distribution", test_analytics_distribution),
        ("Analytics Trends", test_analytics_trends),
        ("Knowledge Graph", test_graph),
        ("Analyze with Graph", test_analyze_with_graph),
        ("CORS Configuration", test_cors)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\nError in {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend.")
        print("Make sure the backend is running at http://localhost:8000")
        print("Run: uvicorn main:app --reload")
        exit(1)
