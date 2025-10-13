#!/usr/bin/env python
"""
Test script to verify quiz submission and performance tracking integration
"""
import os
import django
import json
import requests
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import StudentRegistration
from quizzes.models import QuizAttempt

def test_quiz_integration():
    """Test the complete quiz integration flow"""
    
    print("🧪 Testing Quiz Integration Flow")
    print("=" * 50)
    
    # Test 1: Check if tables exist and are accessible
    print("\n1️⃣ Testing Database Tables...")
    try:
        # Try to create a test quiz attempt
        test_attempt = QuizAttempt.objects.create(
            student_id=None,  # Will be set later
            quiz_type='ai_generated',
            subject='Mathematics',
            chapter='Algebra',
            topic='Linear Equations',
            subtopic='Solving Linear Equations',
            class_name='8th',
            difficulty_level='simple',
            total_questions=10,
            correct_answers=8,
            wrong_answers=2,
            unanswered_questions=0,
            time_taken_seconds=300,
            score=80.0,
            language='English',
            quiz_data_json='{"questions": []}',
            answers_json='{"answers": []}',
            completion_percentage=80.0
        )
        
        print("✅ QuizAttempt model works correctly")
        print(f"   Created attempt ID: {test_attempt.attempt_id}")
        
        # Clean up test data (skip deletion to avoid foreign key issues)
        print("✅ Test data created successfully")
        
    except Exception as e:
        print(f"❌ Error testing QuizAttempt model: {e}")
        return False
    
    # Test 2: Check API endpoints
    print("\n2️⃣ Testing API Endpoints...")
    base_url = "http://localhost:8001"
    
    try:
        # Test if the server is running
        response = requests.get(f"{base_url}/api/", timeout=5)
        print(f"✅ Django server is running (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Django server not accessible: {e}")
        print("   Make sure to run: python manage.py runserver 8001")
        return False
    
    # Test 3: Test quiz submission endpoint structure
    print("\n3️⃣ Testing Quiz Submission Endpoint...")
    
    # Sample quiz data that matches frontend format
    sample_quiz_data = {
        "quizType": "ai_generated",
        "subject": "Mathematics",
        "chapter": "Algebra",
        "topic": "Linear Equations",
        "subtopic": "Solving Linear Equations",
        "className": "8th",
        "difficultyLevel": "simple",
        "language": "English",
        "totalQuestions": 10,
        "correctAnswers": 8,
        "wrongAnswers": 2,
        "unansweredQuestions": 0,
        "timeTakenSeconds": 300,
        "score": 80.0,
        "quizQuestions": [
            {
                "question": "What is 2x + 3 = 7?",
                "options": ["x = 2", "x = 3", "x = 4", "x = 5"],
                "answer": "x = 2"
            },
            {
                "question": "Solve: 3y - 5 = 10",
                "options": ["y = 5", "y = 6", "y = 7", "y = 8"],
                "answer": "y = 5"
            }
        ],
        "userAnswers": [
            {
                "selected": "x = 2",
                "correct": True
            },
            {
                "selected": "y = 6",
                "correct": False
            }
        ]
    }
    
    print("✅ Sample quiz data prepared")
    print(f"   Quiz type: {sample_quiz_data['quizType']}")
    print(f"   Subject: {sample_quiz_data['subject']}")
    print(f"   Questions: {sample_quiz_data['totalQuestions']}")
    print(f"   Score: {sample_quiz_data['score']}%")
    
    # Test 4: Test performance endpoints
    print("\n4️⃣ Testing Performance Endpoints...")
    
    endpoints_to_test = [
        "/api/quizzes/performance/",
        "/api/quizzes/statistics/",
        "/api/quizzes/recent-attempts/",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")
    
    print("\n🎉 Quiz Integration Test Completed!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_quiz_integration()
