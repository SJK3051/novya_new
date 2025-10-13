#!/usr/bin/env python
"""
Test script to verify authentication endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_signup():
    """Test user signup"""
    print("Testing user signup...")
    
    signup_data = {
        'username': 'testuser999',
        'email': 'testuser999@example.com',
        'firstname': 'Test',
        'lastname': 'User',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'role': 'Student',
        'phonenumber': '+1234567890'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=signup_data)
        print(f'Signup Status: {response.status_code}')
        
        if response.status_code == 201:
            data = response.json()
            print('✅ Signup successful!')
            print(f'User ID: {data.get("user", {}).get("id")}')
            print(f'Access Token: {data.get("tokens", {}).get("access", "")[:50]}...')
            return data.get("tokens", {}).get("access")
        else:
            print('❌ Signup failed!')
            print(f'Response: {response.text}')
            return None
            
    except Exception as e:
        print(f'❌ Signup error: {str(e)}')
        return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        'username': 'testuser999',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        print(f'Login Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print('✅ Login successful!')
            print(f'User: {data.get("user", {}).get("username")}')
            print(f'Role: {data.get("user", {}).get("role")}')
            print(f'Access Token: {data.get("access", "")[:50]}...')
            return data.get("access")
        else:
            print('❌ Login failed!')
            print(f'Response: {response.text}')
            return None
            
    except Exception as e:
        print(f'❌ Login error: {str(e)}')
        return None

def test_profile(token):
    """Test getting user profile"""
    print("\nTesting user profile...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
        print(f'Profile Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print('✅ Profile retrieved successfully!')
            print(f'User: {data.get("username")}')
            print(f'Email: {data.get("email")}')
            print(f'Role: {data.get("role")}')
        else:
            print('❌ Profile retrieval failed!')
            print(f'Response: {response.text}')
            
    except Exception as e:
        print(f'❌ Profile error: {str(e)}')

if __name__ == '__main__':
    print("🚀 Testing LMS Authentication System")
    print("=" * 50)
    
    # Test signup
    token = test_signup()
    
    # Test login
    login_token = test_login()
    
    # Test profile with login token
    if login_token:
        test_profile(login_token)
    
    print("\n" + "=" * 50)
    print("✅ Authentication testing completed!")
