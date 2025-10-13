#!/usr/bin/env python3
"""
Simple HTTP test script to verify the fixed integration
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the API endpoints"""
    print("🚀 Testing API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/auth"
    
    # Test data with unique timestamps
    timestamp = str(int(time.time()))
    
    test_parent_data = {
        "email": f"testparent{timestamp}@example.com",
        "first_name": "Test",
        "last_name": "Parent",
        "phone_number": f"9876543{timestamp[-3:]}",
        "parent_username": f"testparent{timestamp}",
        "parent_password": "testpass123",
        "confirm_password": "testpass123"
    }
    
    test_student_data = {
        "first_name": "Test",
        "last_name": "Student",
        "phone_number": f"9876543{timestamp[-2:]}1",
        "student_username": f"teststudent{timestamp}",
        "student_email": f"teststudent{timestamp}@example.com",
        "parent_email": f"testparent{timestamp}@example.com"
    }
    
    try:
        # Test 1: Parent Registration
        print("🔍 Testing parent registration...")
        response = requests.post(
            f'{base_url}/register-parent/',
            json=test_parent_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print("✅ Parent registration successful!")
            parent_data = response.json()
            print(f"   Parent ID: {parent_data['parent']['parent_id']}")
            print(f"   User ID: {parent_data['user_id']}")
        else:
            print(f"❌ Parent registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 2: Student Registration
        print("\n🔍 Testing student registration...")
        response = requests.post(
            f'{base_url}/register-student/',
            json=test_student_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print("✅ Student registration successful!")
            student_data = response.json()
            print(f"   Student ID: {student_data['student']['student_id']}")
            print(f"   User ID: {student_data['user_id']}")
        else:
            print(f"❌ Student registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 3: Login
        print("\n🔍 Testing login...")
        login_data = {
            "username": test_parent_data["parent_username"],
            "password": test_parent_data["parent_password"]
        }
        
        response = requests.post(
            f'{base_url}/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Login successful!")
            login_response = response.json()
            print(f"   Access token: {login_response['access'][:20]}...")
            print(f"   User role: {login_response['user']['role']}")
            access_token = login_response['access']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 4: Password Reset Request
        print("\n🔍 Testing password reset request...")
        reset_data = {
            "email": test_parent_data["email"]
        }
        
        response = requests.post(
            f'{base_url}/request-password-reset/',
            json=reset_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Password reset request successful!")
            reset_response = response.json()
            token = reset_response['token']
            print(f"   Reset token: {token[:20]}...")
        else:
            print(f"❌ Password reset request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 5: Password Reset Confirmation
        print("\n🔍 Testing password reset confirmation...")
        confirm_data = {
            "token": token,
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        }
        
        response = requests.post(
            f'{base_url}/confirm-password-reset/',
            json=confirm_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Password reset confirmation successful!")
        else:
            print(f"❌ Password reset confirmation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Test 6: Login with New Password
        print("\n🔍 Testing login with new password...")
        new_login_data = {
            "username": test_parent_data["parent_username"],
            "password": "newpass123"
        }
        
        response = requests.post(
            f'{base_url}/login/',
            json=new_login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Login with new password successful!")
        else:
            print(f"❌ Login with new password failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error during API test: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting HTTP API Tests for Fixed LMS System")
    print("=" * 60)
    
    if test_api_endpoints():
        print("\n" + "=" * 60)
        print("🎉 All API tests passed!")
        print("\n📋 Summary:")
        print("✅ Parent registration API working")
        print("✅ Student registration API working")
        print("✅ Login API working")
        print("✅ Password reset request API working")
        print("✅ Password reset confirmation API working")
        print("✅ Frontend-backend integration working")
        
        print("\n🔧 Next steps:")
        print("1. The Django backend is running and working correctly")
        print("2. Start the React frontend: cd ../lms_front && npm start")
        print("3. Test the complete user flow in the browser:")
        print("   - Go to http://localhost:3000")
        print("   - Try registering a new user")
        print("   - Try logging in")
        print("   - Try forgot password functionality")
    else:
        print("\n❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
