#!/usr/bin/env python
"""
Script to check quiz types in the system
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quizzes.models import Quiz, QuizAttempt
from django.db import connection

def check_quiz_types():
    """Check quiz types in the system"""
    
    print("🔍 Checking Quiz Types in System")
    print("=" * 60)
    
    try:
        # Check quiz attempts by type
        cursor = connection.cursor()
        cursor.execute("""
            SELECT quiz_type, COUNT(*) as count
            FROM quiz_attempt
            GROUP BY quiz_type
            ORDER BY count DESC;
        """)
        
        print("\n📊 Quiz Attempts by Type:")
        results = cursor.fetchall()
        if results:
            for quiz_type, count in results:
                print(f"  - {quiz_type}: {count} attempts")
        else:
            print("  - No quiz attempts found")
        
        # Check all quiz attempts
        print(f"\n📋 All Quiz Attempts:")
        attempts = QuizAttempt.objects.all().order_by('-attempted_at')[:10]
        for attempt in attempts:
            print(f"  - ID: {attempt.attempt_id}")
            print(f"    Type: {attempt.quiz_type}")
            print(f"    Subject: {attempt.subject}")
            print(f"    Subtopic: {attempt.subtopic}")
            print(f"    Class: {attempt.class_name}")
            print(f"    Score: {attempt.score}")
            print(f"    Date: {attempt.attempted_at}")
            print()
        
        # Check quiz master table
        print(f"\n📚 Quiz Master Records:")
        quizzes = Quiz.objects.all()
        print(f"  Total Quizzes: {quizzes.count()}")
        for quiz in quizzes:
            print(f"  - ID: {quiz.quiz_id}, Title: {quiz.title}, Topic: {quiz.topic_id}")
        
        # Summary
        print(f"\n📈 Summary:")
        print(f"  - Total Quiz Attempts: {QuizAttempt.objects.count()}")
        print(f"  - AI Generated Quizzes: {QuizAttempt.objects.filter(quiz_type='ai_generated').count()}")
        print(f"  - Database Quizzes: {QuizAttempt.objects.filter(quiz_type='database').count()}")
        print(f"  - Mock Tests: {QuizAttempt.objects.filter(quiz_type='mock_test').count()}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error checking quiz types: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_quiz_types()

