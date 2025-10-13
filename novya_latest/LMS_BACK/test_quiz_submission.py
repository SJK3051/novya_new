#!/usr/bin/env python
"""
Test Quiz Submission to Django Backend
Simulates a quiz submission to check if data is being stored
"""
import requests
import json

def test_quiz_submission():
    """Test quiz submission to Django backend"""
    
    print("🧪 TESTING QUIZ SUBMISSION TO DJANGO BACKEND")
    print("=" * 60)
    
    # Sample quiz data (as frontend would send)
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
        "userAnswers": ["-8", "-15"]  # User's selected answers
    }
    
    print("📝 Sample Quiz Data:")
    print(f"   - Subtopic: {quiz_data['subtopic']}")
    print(f"   - Score: {quiz_data['score']}")
    print(f"   - Questions: {len(quiz_data['quizQuestions'])}")
    
    # Test submission endpoint
    print(f"\n🚀 Testing Submission to Django Backend...")
    
    try:
        django_url = "http://localhost:8001/api/quizzes/submit-attempt/"
        
        response = requests.post(
            django_url,
            json=quiz_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test-token'  # Add auth token for testing
            },
            timeout=10
        )
        
        print(f"   📊 Response Status: {response.status_code}")
        print(f"   📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS! Quiz submitted successfully")
            print(f"   📈 Attempt ID: {result.get('attempt_id', 'N/A')}")
            print(f"   📊 Score: {result.get('score', 'N/A')}")
            print(f"   📝 Response: {result}")
            
        elif response.status_code == 401:
            print(f"   🔐 Authentication Required (Expected)")
            print(f"   📝 Response: {response.text[:200]}...")
            print(f"   💡 This is normal - need proper authentication")
            
        elif response.status_code == 400:
            print(f"   ⚠️ Bad Request - Data format issue")
            print(f"   📝 Response: {response.text[:200]}...")
            
        else:
            print(f"   ❌ Unexpected Response: {response.status_code}")
            print(f"   📝 Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    # Check if data was stored
    print(f"\n🔍 Checking Database Storage...")
    try:
        # Try to check recent attempts
        check_url = "http://localhost:8001/api/quizzes/recent-attempts/"
        response = requests.get(check_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            attempts = data.get('attempts', [])
            print(f"   📊 Recent Attempts: {len(attempts)}")
            if attempts:
                latest = attempts[0]
                print(f"   📝 Latest: {latest.get('subtopic', 'N/A')} - Score: {latest.get('score', 'N/A')}")
        else:
            print(f"   ⚠️ Cannot check recent attempts: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking storage: {e}")
    
    print(f"\n🎯 DIAGNOSIS:")
    print("=" * 60)
    print("1. If you see 'Authentication Required' - this is normal")
    print("2. The frontend needs to send proper authentication tokens")
    print("3. Check if user is logged in properly in the frontend")
    print("4. Verify the submission URL and data format match frontend expectations")

if __name__ == "__main__":
    test_quiz_submission()
