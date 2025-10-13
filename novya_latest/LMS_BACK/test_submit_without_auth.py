#!/usr/bin/env python
"""
Test Quiz Submission Without Authentication
Temporarily allows quiz submissions to test data storage
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

def test_quiz_submission_without_auth():
    """Test quiz submission by temporarily modifying permissions"""
    
    print("🔧 TESTING QUIZ SUBMISSION WITHOUT AUTHENTICATION")
    print("=" * 60)
    
    # Sample quiz data
    quiz_data = {
        "quizType": "ai_generated",
        "subject": "Mathematics",
        "chapter": "",
        "topic": "Test Topic",
        "subtopic": "Multiplication of integers",
        "className": "7th",
        "difficultyLevel": "simple",
        "language": "English",
        "totalQuestions": 10,
        "correctAnswers": 8,
        "wrongAnswers": 2,
        "unansweredQuestions": 0,
        "timeTakenSeconds": 300,
        "score": 8.0,
        "quizQuestions": [
            {
                "question": "What is (-4) x 2?",
                "options": ["-8", "8", "-6", "6"],
                "answer": "-8"
            },
            {
                "question": "Calculate 3 x (-5)",
                "options": ["15", "-15", "8", "-8"],
                "answer": "-15"
            }
        ],
        "userAnswers": ["-8", "-15"]
    }
    
    print("📝 Testing with sample quiz data...")
    print(f"   - Subtopic: {quiz_data['subtopic']}")
    print(f"   - Score: {quiz_data['score']}")
    
    # Import the view function directly
    from quizzes.views import submit_quiz_attempt
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    from authentication.models import StudentRegistration
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.post('/api/quizzes/submit-attempt/', 
                          data=json.dumps(quiz_data), 
                          content_type='application/json')
    
    # Set an anonymous user (no authentication)
    request.user = AnonymousUser()
    
    # Try to find a test student
    try:
        test_student = StudentRegistration.objects.first()
        if test_student:
            print(f"   📊 Using test student: {test_student.student_username}")
            # Temporarily modify the user to match a student
            class MockUser:
                def __init__(self, username):
                    self.username = username
                    self.is_authenticated = True
            
            request.user = MockUser(test_student.student_username)
        else:
            print("   ⚠️ No test students found in database")
            return
    except Exception as e:
        print(f"   ❌ Error finding test student: {e}")
        return
    
    # Call the view function directly
    try:
        from rest_framework.response import Response
        from rest_framework import status
        
        response = submit_quiz_attempt(request)
        
        if hasattr(response, 'status_code'):
            print(f"   📊 Response Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ SUCCESS! Quiz submitted successfully")
                response_data = response.data
                print(f"   📈 Attempt ID: {response_data.get('attempt_id', 'N/A')}")
                print(f"   📊 Score: {response_data.get('score', 'N/A')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   📝 Response: {response.data}")
        else:
            print(f"   📝 Response: {response}")
            
    except Exception as e:
        print(f"   ❌ Error calling view: {e}")
        import traceback
        traceback.print_exc()
    
    # Check database storage
    print(f"\n🔍 Checking Database Storage...")
    from quizzes.models import QuizAttempt
    
    try:
        total_attempts = QuizAttempt.objects.count()
        recent_attempts = QuizAttempt.objects.all().order_by('-attempted_at')[:3]
        
        print(f"   📊 Total Quiz Attempts: {total_attempts}")
        print(f"   📋 Recent Attempts:")
        
        for attempt in recent_attempts:
            print(f"      - ID: {attempt.attempt_id}")
            print(f"        Type: {attempt.quiz_type}")
            print(f"        Subtopic: {attempt.subtopic}")
            print(f"        Score: {attempt.score}")
            print(f"        Date: {attempt.attempted_at}")
            print()
            
    except Exception as e:
        print(f"   ❌ Error checking database: {e}")

if __name__ == "__main__":
    test_quiz_submission_without_auth()
