#!/usr/bin/env python
"""
Quick Database Storage Check
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quizzes.models import QuizAttempt, QuizQuestion, QuizAnswer

def check_quiz_storage():
    """Quick check of quiz data storage"""
    
    print("🔍 QUIZ DATA STORAGE CHECK")
    print("=" * 40)
    
    try:
        # Check total quiz attempts
        total_attempts = QuizAttempt.objects.count()
        print(f"📊 Total Quiz Attempts: {total_attempts}")
        
        if total_attempts > 0:
            # Show recent attempts
            recent = QuizAttempt.objects.all().order_by('-attempted_at')[:3]
            print(f"\n📋 Recent Attempts:")
            for attempt in recent:
                print(f"   - ID: {attempt.attempt_id}")
                print(f"     Type: {attempt.quiz_type}")
                print(f"     Subject: {attempt.subject}")
                print(f"     Subtopic: {attempt.subtopic}")
                print(f"     Score: {attempt.score}")
                print(f"     Date: {attempt.attempted_at}")
                print()
            
            # Check questions and answers
            total_questions = QuizQuestion.objects.count()
            total_answers = QuizAnswer.objects.count()
            print(f"📊 Database Storage:")
            print(f"   - Total Questions: {total_questions}")
            print(f"   - Total Answers: {total_answers}")
            
            if total_questions > 0 and total_answers > 0:
                print(f"✅ Quiz data is being stored properly!")
            else:
                print(f"⚠️ Questions/Answers not being stored individually")
        else:
            print(f"💡 No quiz attempts found yet")
            print(f"   This is normal if no quizzes have been submitted")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_quiz_storage()
