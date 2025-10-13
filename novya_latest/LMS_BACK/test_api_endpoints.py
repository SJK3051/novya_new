#!/usr/bin/env python
"""
API Endpoints Test Script for NOVYA LMS
This script tests all the API endpoints to ensure they're working correctly.
"""

import os
import sys
import django
import requests
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

def print_header():
    """Print test header"""
    print("🧪 NOVYA LMS API Endpoints Test")
    print("=" * 50)

def test_server_running():
    """Test if Django server is running"""
    print("🔍 Testing Django server...")
    
    try:
        response = requests.get('http://localhost:8000/api/auth/', timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running")
            return True
        else:
            print(f"⚠️ Django server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Django server is not running: {e}")
        print("Please start the server with: python manage.py runserver")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API endpoints...")
    
    base_url = "http://localhost:8000/api"
    
    # Test endpoints that don't require authentication
    public_endpoints = [
        "/auth/login/",
        "/auth/register/",
        "/courses/",
        "/quizzes/",
        "/progress/assignments/",
        "/notifications/events/",
    ]
    
    success_count = 0
    total_count = len(public_endpoints)
    
    for endpoint in public_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 401, 405]:  # 401 = auth required, 405 = method not allowed
                print(f"✅ {endpoint} - Status: {response.status_code}")
                success_count += 1
            else:
                print(f"⚠️ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    print(f"\n📊 Endpoint Test Results: {success_count}/{total_count} endpoints accessible")
    return success_count == total_count

def test_authentication():
    """Test authentication endpoints"""
    print("\n🔐 Testing authentication...")
    
    base_url = "http://localhost:8000/api/auth"
    
    # Test login endpoint
    try:
        response = requests.post(f"{base_url}/login/", json={
            "username": "test_user",
            "password": "test_password"
        }, timeout=5)
        
        if response.status_code == 401:
            print("✅ Login endpoint working (returns 401 for invalid credentials)")
            return True
        elif response.status_code == 400:
            print("✅ Login endpoint working (returns 400 for missing data)")
            return True
        else:
            print(f"⚠️ Login endpoint returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Login endpoint error: {e}")
        return False

def test_database_connection():
    """Test database connection through API"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def show_available_endpoints():
    """Show all available endpoints"""
    print("\n📋 Available API Endpoints:")
    print("=" * 50)
    
    endpoints = {
        "Authentication": [
            "POST /api/auth/login/",
            "POST /api/auth/register/",
            "POST /api/auth/logout/",
            "GET /api/auth/profile/",
            "GET /api/auth/dashboard/",
        ],
        "Courses": [
            "GET /api/courses/",
            "GET /api/courses/{id}/",
            "POST /api/courses/{id}/enroll/",
            "GET /api/courses/{id}/progress/",
            "GET /api/courses/my-courses/",
        ],
        "Assignments": [
            "GET /api/progress/assignments/",
            "GET /api/progress/assignments/{id}/",
            "POST /api/progress/assignments/{id}/submit/",
            "GET /api/progress/my-assignments/",
        ],
        "Quizzes": [
            "GET /api/quizzes/",
            "GET /api/quizzes/{id}/",
            "POST /api/quizzes/{id}/start/",
            "POST /api/quizzes/{id}/submit/",
            "GET /api/quizzes/my-attempts/",
            "GET /api/quizzes/stats/",
        ],
        "Progress": [
            "GET /api/progress/dashboard/",
            "GET /api/progress/parent-dashboard/",
            "GET /api/progress/attendance/",
            "GET /api/progress/grades/",
        ],
        "Notifications": [
            "GET /api/notifications/",
            "GET /api/notifications/events/",
            "GET /api/notifications/announcements/",
            "GET /api/notifications/messages/",
        ],
    }
    
    for category, endpoint_list in endpoints.items():
        print(f"\n🔹 {category}:")
        for endpoint in endpoint_list:
            print(f"  {endpoint}")

def main():
    """Main test function"""
    print_header()
    
    # Test Django server
    if not test_server_running():
        print("\n❌ Please start the Django server first:")
        print("python manage.py runserver")
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Please check your database setup.")
        sys.exit(1)
    
    # Test API endpoints
    if not test_api_endpoints():
        print("\n⚠️ Some API endpoints are not accessible. Check your URL configuration.")
    
    # Test authentication
    if not test_authentication():
        print("\n⚠️ Authentication endpoints may have issues.")
    
    # Show available endpoints
    show_available_endpoints()
    
    print("\n🎉 API testing completed!")
    print("\n📋 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Access Django admin: http://localhost:8000/admin/")
    print("3. Test API endpoints with your frontend")
    print("4. Check API documentation: API_ENDPOINTS.md")

if __name__ == "__main__":
    main()
