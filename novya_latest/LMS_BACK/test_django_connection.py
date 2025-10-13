import requests
import json

print("🔍 Testing Django Server Connection...")

try:
    # Test basic Django server response
    response = requests.get("http://localhost:8001/")
    print(f"✅ Django Server Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Django server is running and accessible")
    else:
        print(f"⚠️ Django server returned status: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Django server not reachable on port 8001")
    print("   Make sure Django is running with: python manage.py runserver 8001")
except Exception as e:
    print(f"❌ Error connecting to Django: {e}")

print("\n🔍 Testing Quiz Endpoint...")

try:
    # Test quiz endpoint
    response = requests.post(
        "http://localhost:8001/api/quizzes/submit-attempt/",
        json={
            "quizType": "ai_generated",
            "subject": "Test",
            "subtopic": "Test Topic",
            "className": "7th",
            "difficultyLevel": "simple",
            "language": "English",
            "totalQuestions": 1,
            "correctAnswers": 1,
            "wrongAnswers": 0,
            "unansweredQuestions": 0,
            "timeTakenSeconds": 30,
            "score": 10.0,
            "quizQuestions": [{"question": "Test?", "options": ["A", "B", "C", "D"], "answer": "A"}],
            "userAnswers": ["A"]
        },
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"📊 Quiz Endpoint Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Quiz submission successful!")
        print(f"📝 Response: {response.json()}")
    elif response.status_code == 500:
        print("❌ 500 Internal Server Error - Check Django logs")
    else:
        print(f"⚠️ Unexpected status: {response.status_code}")
        print(f"📝 Response: {response.text[:200]}...")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to quiz endpoint")
except Exception as e:
    print(f"❌ Error testing quiz endpoint: {e}")
