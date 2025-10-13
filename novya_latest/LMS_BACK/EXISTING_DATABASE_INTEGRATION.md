# 🔄 Existing Database Integration Guide

This guide helps you integrate your existing PostgreSQL database with the Django backend.

## 📋 Your Existing Schema

Your database already contains these tables:

### Core Tables
- `users` - User accounts with roles (Student, Parent)
- `class` - Class information
- `parent` - Parent profiles
- `student` - Student profiles with class and parent relationships

### Course Management
- `course` - Course information with pricing
- `topic` - Course topics
- `pdf_files` - PDF course materials
- `videofiles` - Video course materials

### Assignments & Quizzes
- `assignment` - Assignments linked to topics
- `assignmentquestion` - Assignment questions with multiple choice options
- `assignmentsubmission` - Student assignment submissions
- `assignmentanswer` - Individual question answers
- `quiz` - Quizzes with JSON questions
- `quizattempt` - Student quiz attempts
- `mocktest` - Mock tests

### Progress & Reviews
- `careerperformance` - Student performance tracking
- `mentorshipticket` - Mentorship support tickets
- `review` - Course and instructor reviews
- `rating` - Rating system
- `report` - Reporting system

## 🔧 Django Model Updates

I've updated all Django models to match your existing schema:

### Authentication Models (`authentication/models.py`)
```python
class User(AbstractUser):
    userid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[('Student', 'Student'), ('Parent', 'Parent')])
    createdat = models.DateTimeField(auto_now_add=True)
```

### Course Models (`courses/models.py`)
```python
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_price = models.DecimalField(max_digits=10, decimal_places=2)

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)
```

### Assignment Models (`progress/models.py`)
```python
class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateField()
    file_url = models.TextField()

class AssignmentQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1)
```

## 🚀 Integration Steps

### 1. Run Database Sync Script
```bash
python sync_existing_database.py
```

This script will:
- Check your database connection
- Verify existing tables
- Create missing Django tables
- Map your existing schema to Django models

### 2. Manual Integration (Alternative)

If the automated script doesn't work:

#### Step 1: Create Migrations
```bash
python manage.py makemigrations --empty authentication
python manage.py makemigrations --empty courses
python manage.py makemigrations --empty quizzes
python manage.py makemigrations --empty progress
python manage.py makemigrations --empty notifications
```

#### Step 2: Apply Migrations with Fake Initial
```bash
python manage.py migrate --fake-initial
```

#### Step 3: Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Verify Integration

#### Test Database Connection
```bash
python test_db_connection.py
```

#### Check Table Mapping
```sql
-- Connect to your database
psql -U postgres -d novya_lms

-- List all tables
\dt

-- Check specific table structure
\d users
\d course
\d assignment
```

## 🔍 Table Mapping

| Existing Table | Django Model | App |
|----------------|--------------|-----|
| `users` | `User` | authentication |
| `class` | `Class` | authentication |
| `parent` | `Parent` | authentication |
| `student` | `Student` | authentication |
| `course` | `Course` | courses |
| `topic` | `Topic` | courses |
| `pdf_files` | `PDFFiles` | courses |
| `videofiles` | `VideoFiles` | courses |
| `assignment` | `Assignment` | progress |
| `assignmentquestion` | `AssignmentQuestion` | progress |
| `assignmentsubmission` | `AssignmentSubmission` | progress |
| `assignmentanswer` | `AssignmentAnswer` | progress |
| `quiz` | `Quiz` | quizzes |
| `quizattempt` | `QuizAttempt` | quizzes |
| `mocktest` | `MockTest` | quizzes |
| `careerperformance` | `CareerPerformance` | progress |
| `mentorshipticket` | `MentorshipTicket` | progress |
| `review` | `Review` | notifications |
| `rating` | `Rating` | notifications |
| `report` | `Report` | notifications |

## 🎯 API Endpoints

Your existing data will be accessible through these API endpoints:

### Authentication
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{id}/` - Course details
- `GET /api/courses/{id}/topics/` - Course topics
- `GET /api/courses/{id}/materials/` - Course materials (PDFs, Videos)

### Assignments
- `GET /api/progress/assignments/` - List assignments
- `GET /api/progress/assignments/{id}/` - Assignment details
- `POST /api/progress/assignments/{id}/submit/` - Submit assignment
- `GET /api/progress/assignments/{id}/questions/` - Assignment questions

### Quizzes
- `GET /api/quizzes/` - List quizzes
- `GET /api/quizzes/{id}/` - Quiz details
- `POST /api/quizzes/{id}/start/` - Start quiz
- `POST /api/quizzes/{id}/submit/` - Submit quiz

### Progress
- `GET /api/progress/dashboard/` - Student dashboard
- `GET /api/progress/performance/` - Career performance
- `GET /api/progress/tickets/` - Mentorship tickets

## 🔧 Customization

### Adding New Fields
If you need to add new fields to existing tables:

1. **Update Django Model**:
```python
class User(AbstractUser):
    # Existing fields...
    new_field = models.CharField(max_length=100, blank=True, null=True)
```

2. **Create Migration**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Custom Queries
For complex queries that don't fit Django ORM:

```python
from django.db import connection

def custom_query():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.firstname, u.lastname, c.course_name, a.avg_assignment_score
            FROM users u
            JOIN student s ON u.userid = s.student_id
            JOIN course c ON s.class_id = c.class_id
            JOIN careerperformance a ON s.student_id = a.student_id
            WHERE a.avg_assignment_score > 80
        """)
        return cursor.fetchall()
```

## 🚨 Important Notes

### 1. Data Integrity
- Your existing data will remain intact
- Django will use your existing table names
- No data migration is required

### 2. User Authentication
- The `User` model now uses `userid` as primary key
- Username and email are unique
- Role is restricted to 'Student' and 'Parent'

### 3. Foreign Key Relationships
- All foreign keys are properly mapped
- Cascade deletes are configured
- Relationships match your existing schema

### 4. JSON Fields
- Quiz questions are stored as JSON
- Quiz answers are stored as JSON
- This matches your existing schema

## 🎉 Success Verification

After integration, you should be able to:

1. **Access Django Admin**: http://localhost:8000/admin/
2. **View Existing Data**: All your existing data should be visible
3. **Use API Endpoints**: All endpoints should work with your data
4. **Create New Records**: Add new users, courses, assignments, etc.

## 🆘 Troubleshooting

### Common Issues

1. **Table Not Found**
   - Check if table exists in database
   - Verify table name in Django model
   - Run `python manage.py showmigrations`

2. **Foreign Key Errors**
   - Check if referenced records exist
   - Verify foreign key field names
   - Check database constraints

3. **Permission Errors**
   - Ensure Django user has database access
   - Check PostgreSQL user permissions
   - Verify database connection settings

### Debug Commands
```bash
# Check migration status
python manage.py showmigrations

# Check database connection
python manage.py dbshell

# View SQL for migrations
python manage.py sqlmigrate app_name migration_number
```

Your existing database is now fully integrated with Django! 🎉
