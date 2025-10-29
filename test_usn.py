#!/usr/bin/env python3
import requests
import json

def test_usn_scan(usn):
    """Test USN-based scanning"""
    url = 'http://localhost:3000/api/scan'
    
    # Test data
    data = {
        'qrData': usn
    }
    
    try:
        response = requests.post(url, json=data)
        
        print(f"Testing USN: {usn}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
        
    except Exception as e:
        print(f"Error testing USN {usn}: {e}")
        return None

def test_usn_functionality():
    print("🧪 Testing USN-based manual entry functionality\n")
    
    # Test cases
    test_cases = [
        "ABOOBAKKARDS22",  # Should work
        "ADARSHDS22",      # Should work 
        "INVALIDUSN123",   # Should fail
        "aboobakkards22",  # Should work (case insensitive)
    ]
    
    for usn in test_cases:
        result = test_usn_scan(usn)
        
        if result and result.get('success'):
            print(f"✅ {usn}: SUCCESS")
            user = result.get('user', {})
            print(f"   Name: {user.get('name')}")
            print(f"   Food: {user.get('food_preference')}")
            print(f"   Class: {user.get('class_name')}")
        elif result and 'error' in result:
            print(f"❌ {usn}: {result['error']}")
        else:
            print(f"❓ {usn}: Unknown response")
        
        print()

if __name__ == "__main__":
    test_usn_functionality()
