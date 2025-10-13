#!/usr/bin/env python
import requests
import json
import time

def test_complete_auth():
    print("🚀 Complete LMS Authentication Test")
    print("=" * 50)
    
    # Test 1: Signup
    print("1. Testing User Signup...")
    signup_data = {
        'username': 'test_student_001',
        'email': 'student001@example.com',
        'firstname': 'John',
        'lastname': 'Doe',
        'password': 'MySecurePass123!',
        'confirm_password': 'MySecurePass123!',
        'role': 'Student',
        'phonenumber': '+1555123456'
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/register/', json=signup_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Signup successful!")
            data = response.json()
            print(f"   User ID: {data.get('user', {}).get('id')}")
            print(f"   Username: {data.get('user', {}).get('username')}")
            print(f"   Role: {data.get('user', {}).get('role')}")
            print(f"   Email: {data.get('user', {}).get('email')}")
            signup_success = True
        else:
            print(f"   ❌ Signup failed: {response.text[:200]}")
            signup_success = False
    except Exception as e:
        print(f"   ❌ Signup error: {str(e)}")
        signup_success = False
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        'username': 'test_student_001',
        'password': 'MySecurePass123!'
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful!")
            data = response.json()
            print(f"   User: {data.get('user', {}).get('username')}")
            print(f"   Role: {data.get('user', {}).get('role')}")
            print(f"   Access Token: {data.get('access', '')[:50]}...")
            access_token = data.get('access')
            login_success = True
        else:
            print(f"   ❌ Login failed: {response.text[:200]}")
            login_success = False
            access_token = None
    except Exception as e:
        print(f"   ❌ Login error: {str(e)}")
        login_success = False
        access_token = None
    
    # Test 3: Profile Access
    if access_token:
        print("\n3. Testing Profile Access...")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get('http://localhost:8000/api/auth/profile/', headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Profile access successful!")
                data = response.json()
                print(f"   Username: {data.get('username')}")
                print(f"   Email: {data.get('email')}")
                print(f"   Role: {data.get('role')}")
                profile_success = True
            else:
                print(f"   ❌ Profile access failed: {response.text[:200]}")
                profile_success = False
        except Exception as e:
            print(f"   ❌ Profile error: {str(e)}")
            profile_success = False
    else:
        print("\n3. Skipping Profile Test (no access token)")
        profile_success = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"   Signup: {'✅ PASS' if signup_success else '❌ FAIL'}")
    print(f"   Login:  {'✅ PASS' if login_success else '❌ FAIL'}")
    print(f"   Profile: {'✅ PASS' if profile_success else '❌ FAIL'}")
    
    if signup_success and login_success and profile_success:
        print("\n🎉 ALL TESTS PASSED! Authentication system is working correctly!")
        print("✅ Frontend can now connect to backend for signup and login")
        print("✅ Data is being stored in and retrieved from database")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    return signup_success and login_success and profile_success

if __name__ == '__main__':
    test_complete_auth()
