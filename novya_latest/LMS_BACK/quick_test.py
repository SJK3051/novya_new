#!/usr/bin/env python
import requests
import json

def test_auth():
    print("🚀 Testing LMS Authentication")
    print("=" * 40)
    
    # Test signup
    print("1. Testing Signup...")
    signup_data = {
        'username': 'new_user_123',
        'email': 'newuser@example.com',
        'firstname': 'Demo',
        'lastname': 'User',
        'password': 'demo123456',
        'confirm_password': 'demo123456',
        'role': 'Student',
        'phonenumber': '+1987654321'
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/register/', json=signup_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Signup successful!")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('username')}")
        else:
            print(f"   ❌ Signup failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test login
    print("\n2. Testing Login...")
    login_data = {
        'username': 'new_user_123',
        'password': 'demo123456'
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful!")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('username')}")
            print(f"   Role: {data.get('user', {}).get('role')}")
            return data.get('access')
        else:
            print(f"   ❌ Login failed: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    return None

if __name__ == '__main__':
    test_auth()
