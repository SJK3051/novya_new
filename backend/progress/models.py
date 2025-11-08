from django.db import models
from authentication.models import User, Student
from courses.models import Course, Chapter

# -----------------------------
# Student Performance model
# -----------------------------
class StudentPerformance(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='performance')

    # Overall statistics
    total_quizzes_attempted = models.PositiveIntegerField(default=0)
    total_questions_answered = models.PositiveIntegerField(default=0)
    total_correct_answers = models.PositiveIntegerField(default=0)
    overall_average_score = models.FloatField(default=0.0)

    # Subject-wise performance
    mathematics_score = models.FloatField(default=0.0)
    science_score = models.FloatField(default=0.0)
    english_score = models.FloatField(default=0.0)
    computers_score = models.FloatField(default=0.0)

    # Class-wise performance
    class_7_score = models.FloatField(default=0.0)
    class_8_score = models.FloatField(default=0.0)
    class_9_score = models.FloatField(default=0.0)
    class_10_score = models.FloatField(default=0.0)

    # Difficulty-wise performance
    simple_difficulty_score = models.FloatField(default=0.0)
    medium_difficulty_score = models.FloatField(default=0.0)
    hard_difficulty_score = models.FloatField(default=0.0)

    # Time and consistency
    average_time_per_question = models.FloatField(default=0.0)
    completion_rate = models.FloatField(default=0.0)
    improvement_trend = models.FloatField(default=0.0)

    # Achievements and badges
    achievements_json = models.TextField(null=True, blank=True)
    badges_earned = models.PositiveIntegerField(default=0)

    # Last updated
    last_updated = models.DateTimeField(auto_now=True)
    last_quiz_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.firstname} - Performance"

    class Meta:
        db_table = 'student_performance'
        verbose_name = 'Student Performance'
        verbose_name_plural = 'Student Performances'

