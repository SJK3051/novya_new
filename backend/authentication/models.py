# courses/models.py
from django.db import models
from django.utils import timezone


class Course(models.Model):
    """
    Course model matching the database schema
    """
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    class_field = models.ForeignKey(
        'authentication.Class', 
        on_delete=models.CASCADE, 
        db_column='class_id'
    )
    teacher_id = models.IntegerField(blank=True, null=True)  # Using IntegerField instead of ForeignKey to avoid circular imports
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course_name
    
    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseMaterial(models.Model):
    """
    Course Material model for storing course-related files and materials
    """
    material_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='materials'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.course_name}"
    
    class Meta:
        db_table = 'course_material'
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'


class Assignment(models.Model):
    """
    Assignment model for course assignments
    """
    assignment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='assignments'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    max_points = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.course_name}"
    
    def is_past_due(self):
        return timezone.now() > self.due_date
    
    class Meta:
        db_table = 'assignment'
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class StudentAssignment(models.Model):
    """
    Student Assignment submission model
    """
    SUBMISSION_STATUS = [
        ('not_submitted', 'Not Submitted'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    submission_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='submissions'
    )
    student_id = models.IntegerField()  # Using IntegerField instead of ForeignKey
    submission_file = models.CharField(max_length=500, blank=True, null=True)
    submission_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=SUBMISSION_STATUS, 
        default='not_submitted'
    )
    
    def __str__(self):
        return f"Submission {self.submission_id} - Assignment {self.assignment.assignment_id}"
    
    class Meta:
        db_table = 'student_assignment'
        verbose_name = 'Student Assignment'
        verbose_name_plural = 'Student Assignments'
        unique_together = ['assignment', 'student_id']


class Enrollment(models.Model):
    """
    Student enrollment in courses
    """
    enrollment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    student_id = models.IntegerField()  # Using IntegerField instead of ForeignKey
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Student {self.student_id} in {self.course.course_name}"
    
    class Meta:
        db_table = 'enrollment'
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ['course', 'student_id']


class Grade(models.Model):
    """
    Student grades for courses
    """
    grade_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='grades'
    )
    student_id = models.IntegerField()  # Using IntegerField instead of ForeignKey
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='assignment_grades'
    )
    grade_value = models.DecimalField(max_digits=5, decimal_places=2)
    grade_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    graded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Grade {self.grade_value} for Student {self.student_id}"
    
    class Meta:
        db_table = 'grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'


class Attendance(models.Model):
    """
    Student attendance for courses
    """
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    attendance_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='attendance_records'
    )
    student_id = models.IntegerField()  # Using IntegerField instead of ForeignKey
    date = models.DateField()
    status = models.CharField(
        max_length=10, 
        choices=ATTENDANCE_STATUS, 
        default='present'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Attendance {self.date} - Student {self.student_id}"
    
    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ['course', 'student_id', 'date']


class Announcement(models.Model):
    """
    Course announcements
    """
    announcement_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='announcements'
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'announcement'
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-is_pinned', '-created_at']
