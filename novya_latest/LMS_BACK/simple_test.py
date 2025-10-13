#!/usr/bin/env python
"""
Simple API test script
"""

import requests
import time

def test_api():
    """Test API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    # Test endpoints
    endpoints = [
        "/api/auth/",
        "/api/courses/",
        "/api/quizzes/",
        "/api/progress/",
        "/api/notifications/",
    ]
    
    print("🧪 Testing NOVYA LMS API Endpoints")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"Testing: {url}")
            response = requests.get(url, timeout=5)
            print(f"✅ Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.text[:100]}...")
            print()
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed - Server not running on {base_url}")
            print()
        except Exception as e:
            print(f"❌ Error: {e}")
            print()

if __name__ == "__main__":
    test_api()
