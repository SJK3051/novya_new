import requests
import json

# Test without any authentication headers
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
        }
    ],
    "userAnswers": ["-8"]
}

print("🧪 Testing without authentication...")
response = requests.post(
    "http://localhost:8001/api/quizzes/submit-attempt/",
    json=quiz_data,
    headers={'Content-Type': 'application/json'},
    timeout=10
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    print("✅ SUCCESS! Quiz submitted without authentication!")
else:
    print("❌ Still requires authentication")
