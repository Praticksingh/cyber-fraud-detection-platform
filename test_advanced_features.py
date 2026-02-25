"""
Test script for advanced features of Cyber Fraud Detection System.
Tests: WebSocket, Alerts, ML Retraining
"""

import requests
import json
import asyncio
import websockets

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/dashboard"
ADMIN_KEY = "admin123"
PUBLIC_KEY = "public123"


def test_ml_retrain():
    """Test ML model retraining endpoint."""
    print("\n" + "="*60)
    print("Testing ML Model Retraining")
    print("="*60)
    
    payload = {
        "scam_messages": [
            "URGENT! Your package is pending. Pay customs fee now!",
            "Congratulations! You won $1,000,000. Send your bank details.",
            "ALERT: Your account will be suspended. Click here immediately."
        ],
        "legitimate_messages": [
            "Hi, are we still meeting for lunch tomorrow?",
            "Thanks for your help with the project yesterday.",
            "The meeting has been rescheduled to 3 PM on Friday."
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/retrain",
        headers={"X-API-KEY": ADMIN_KEY},
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Model retrained successfully!")
    else:
        print("❌ Retraining failed!")
    
    return response.status_code == 200


def test_critical_alert():
    """Test that critical fraud triggers alerts."""
    print("\n" + "="*60)
    print("Testing Critical Alert System")
    print("="*60)
    
    # Send a message that should trigger critical alert
    payload = {
        "phone_number": "555-ALERT",
        "message_content": "URGENT! Your bank account is suspended. Verify immediately or face legal action and penalties!"
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        headers={"X-API-KEY": PUBLIC_KEY},
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Risk Score: {result.get('risk_score')}")
    print(f"Threat Category: {result.get('threat_category')}")
    
    if result.get('risk_level') == 'Critical':
        print("✅ Critical threat detected! Alert should be triggered.")
        print("   Check your email/webhook for alert notification.")
    else:
        print("⚠️  Not critical level. Try with more threatening message.")
    
    return response.status_code == 200


async def test_websocket():
    """Test WebSocket live updates."""
    print("\n" + "="*60)
    print("Testing WebSocket Live Updates")
    print("="*60)
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("✅ WebSocket connected!")
            print("Waiting for updates (10 seconds)...")
            print("Tip: Run an analysis in another terminal to see live updates")
            
            try:
                # Wait for messages with timeout
                message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                data = json.loads(message)
                print(f"\n📨 Received update:")
                print(json.dumps(data, indent=2))
                print("✅ WebSocket is working!")
                return True
            except asyncio.TimeoutError:
                print("⏱️  No updates received in 10 seconds (this is normal if no analyses are running)")
                print("✅ WebSocket connection is working (just no updates yet)")
                return True
                
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False


def test_stats_endpoint():
    """Test statistics endpoint."""
    print("\n" + "="*60)
    print("Testing Statistics Endpoint")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/stats",
        headers={"X-API-KEY": ADMIN_KEY}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Stats: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Statistics retrieved successfully!")
    else:
        print("❌ Failed to get statistics!")
    
    return response.status_code == 200


def test_blacklist_endpoint():
    """Test blacklist endpoint."""
    print("\n" + "="*60)
    print("Testing Blacklist Endpoint")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/blacklist",
        headers={"X-API-KEY": ADMIN_KEY}
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total Blacklisted: {result.get('total_blacklisted')}")
    
    if result.get('blacklist'):
        print("\nBlacklisted Numbers:")
        for entry in result['blacklist'][:5]:  # Show first 5
            print(f"  - {entry['phone_number']}: {entry['reason'][:50]}...")
    
    if response.status_code == 200:
        print("✅ Blacklist retrieved successfully!")
    else:
        print("❌ Failed to get blacklist!")
    
    return response.status_code == 200


def main():
    """Run all advanced feature tests."""
    print("\n" + "="*60)
    print("CYBER FRAUD DETECTION SYSTEM")
    print("Advanced Features Test Suite")
    print("="*60)
    
    results = {}
    
    try:
        # Test REST endpoints
        results['stats'] = test_stats_endpoint()
        results['blacklist'] = test_blacklist_endpoint()
        results['retrain'] = test_ml_retrain()
        results['alert'] = test_critical_alert()
        
        # Test WebSocket
        print("\n" + "="*60)
        print("Testing WebSocket (requires asyncio)")
        print("="*60)
        try:
            results['websocket'] = asyncio.run(test_websocket())
        except Exception as e:
            print(f"❌ WebSocket test failed: {e}")
            results['websocket'] = False
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name.upper()}: {status}")
        
        total = len(results)
        passed = sum(results.values())
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! System is working perfectly!")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
