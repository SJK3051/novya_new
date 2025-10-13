# 🚀 NOVYA LMS API Endpoints

Complete list of all available API endpoints for your Django backend.

## 🔐 Authentication Endpoints (`/api/auth/`)

### User Authentication
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout (blacklist refresh token)
- `POST /api/auth/token/refresh/` - Refresh JWT access token

### Password Management
- `POST /api/auth/change-password/` - Change user password
- `POST /api/auth/request-password-reset/` - Request password reset
- `POST /api/auth/confirm-password-reset/` - Confirm password reset

### Profile Management
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/update/` - Update user profile
- `GET /api/auth/dashboard/` - Get dashboard data based on user role

### User Management
- `GET /api/auth/students/` - List all students
- `GET /api/auth/parents/` - List all parents
- `GET /api/auth/teachers/` - List all teachers

## 📚 Course Endpoints (`/api/courses/`)

### Subjects
- `GET /api/courses/subjects/` - List all subjects
- `POST /api/courses/subjects/` - Create new subject
- `GET /api/courses/subjects/{id}/` - Get subject details
- `PUT /api/courses/subjects/{id}/` - Update subject
- `DELETE /api/courses/subjects/{id}/` - Delete subject

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Get course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course
- `POST /api/courses/{id}/enroll/` - Enroll in course
- `GET /api/courses/{id}/progress/` - Get course progress

### Chapters
- `GET /api/courses/{course_id}/chapters/` - List course chapters
- `POST /api/courses/{course_id}/chapters/` - Create new chapter
- `GET /api/courses/chapters/{id}/` - Get chapter details
- `PUT /api/courses/chapters/{id}/` - Update chapter
- `DELETE /api/courses/chapters/{id}/` - Delete chapter

### Lessons
- `GET /api/courses/chapters/{chapter_id}/lessons/` - List chapter lessons
- `POST /api/courses/chapters/{chapter_id}/lessons/` - Create new lesson
- `GET /api/courses/lessons/{id}/` - Get lesson details
- `PUT /api/courses/lessons/{id}/` - Update lesson
- `DELETE /api/courses/lessons/{id}/` - Delete lesson
- `POST /api/courses/lessons/{id}/progress/` - Update lesson progress

### Course Materials
- `GET /api/courses/{course_id}/materials/` - List course materials
- `POST /api/courses/{course_id}/materials/` - Add course material
- `GET /api/courses/materials/{id}/` - Get material details
- `PUT /api/courses/materials/{id}/` - Update material
- `DELETE /api/courses/materials/{id}/` - Delete material

### Student Course Management
- `GET /api/courses/my-courses/` - Get student's enrolled courses
- `GET /api/courses/my-progress/` - Get student's overall progress

## 📝 Assignment Endpoints (`/api/progress/assignments/`)

### Assignments
- `GET /api/progress/assignments/` - List all assignments
- `POST /api/progress/assignments/` - Create new assignment
- `GET /api/progress/assignments/{id}/` - Get assignment details
- `PUT /api/progress/assignments/{id}/` - Update assignment
- `DELETE /api/progress/assignments/{id}/` - Delete assignment
- `POST /api/progress/assignments/{id}/submit/` - Submit assignment

### Student Assignments
- `GET /api/progress/my-assignments/` - Get student's assignments

## 🧠 Quiz Endpoints (`/api/quizzes/`)

### Quizzes
- `GET /api/quizzes/` - List all quizzes
- `POST /api/quizzes/` - Create new quiz
- `GET /api/quizzes/{id}/` - Get quiz details
- `PUT /api/quizzes/{id}/` - Update quiz
- `DELETE /api/quizzes/{id}/` - Delete quiz
- `POST /api/quizzes/{id}/start/` - Start quiz attempt
- `POST /api/quizzes/{id}/submit/` - Submit quiz answers

### Quiz Questions
- `GET /api/quizzes/{quiz_id}/questions/` - List quiz questions
- `POST /api/quizzes/{quiz_id}/questions/` - Add quiz question
- `GET /api/quizzes/questions/{id}/` - Get question details
- `PUT /api/quizzes/questions/{id}/` - Update question
- `DELETE /api/quizzes/questions/{id}/` - Delete question

### Quiz Attempts
- `GET /api/quizzes/attempts/` - List quiz attempts
- `GET /api/quizzes/attempts/{id}/` - Get attempt details
- `GET /api/quizzes/attempts/{id}/result/` - Get detailed quiz result

### Student Quiz Management
- `GET /api/quizzes/my-attempts/` - Get student's quiz attempts
- `GET /api/quizzes/stats/` - Get student's quiz statistics
- `GET /api/quizzes/available/` - Get available quizzes for student

## 📊 Progress Endpoints (`/api/progress/`)

### Attendance
- `GET /api/progress/attendance/` - List attendance records
- `POST /api/progress/attendance/` - Create attendance record
- `GET /api/progress/attendance/{id}/` - Get attendance details
- `PUT /api/progress/attendance/{id}/` - Update attendance
- `DELETE /api/progress/attendance/{id}/` - Delete attendance
- `GET /api/progress/attendance/summary/` - Get attendance summary

### Grades
- `GET /api/progress/grades/` - List all grades
- `POST /api/progress/grades/` - Create new grade
- `GET /api/progress/grades/{id}/` - Get grade details
- `PUT /api/progress/grades/{id}/` - Update grade
- `DELETE /api/progress/grades/{id}/` - Delete grade
- `GET /api/progress/my-grades/` - Get student's grades

### Study Plans
- `GET /api/progress/study-plans/` - List study plans
- `POST /api/progress/study-plans/` - Create study plan
- `GET /api/progress/study-plans/{id}/` - Get study plan details
- `PUT /api/progress/study-plans/{id}/` - Update study plan
- `DELETE /api/progress/study-plans/{id}/` - Delete study plan
- `GET /api/progress/study-plans/{id}/items/` - List study plan items
- `POST /api/progress/study-plans/{id}/items/` - Add study plan item
- `GET /api/progress/study-plan-items/{id}/` - Get study plan item details
- `PUT /api/progress/study-plan-items/{id}/` - Update study plan item
- `DELETE /api/progress/study-plan-items/{id}/` - Delete study plan item
- `POST /api/progress/study-plan-items/{id}/complete/` - Mark item as completed

### Student Progress
- `GET /api/progress/student-progress/` - List student progress records
- `POST /api/progress/student-progress/` - Create progress record
- `GET /api/progress/student-progress/{id}/` - Get progress details
- `PUT /api/progress/student-progress/{id}/` - Update progress
- `DELETE /api/progress/student-progress/{id}/` - Delete progress
- `GET /api/progress/my-progress/` - Get current user's progress

### Achievements
- `GET /api/progress/achievements/` - List achievements
- `POST /api/progress/achievements/` - Create achievement
- `GET /api/progress/achievements/{id}/` - Get achievement details
- `PUT /api/progress/achievements/{id}/` - Update achievement
- `DELETE /api/progress/achievements/{id}/` - Delete achievement
- `GET /api/progress/my-achievements/` - Get student's achievements

### Dashboards
- `GET /api/progress/dashboard/` - Get student dashboard data
- `GET /api/progress/parent-dashboard/` - Get parent dashboard data

## 🔔 Notification Endpoints (`/api/notifications/`)

### Events
- `GET /api/notifications/events/` - List all events
- `POST /api/notifications/events/` - Create new event
- `GET /api/notifications/events/{id}/` - Get event details
- `PUT /api/notifications/events/{id}/` - Update event
- `DELETE /api/notifications/events/{id}/` - Delete event
- `POST /api/notifications/events/{id}/register/` - Register for event
- `GET /api/notifications/my-events/` - Get user's registered events

### Notifications
- `GET /api/notifications/` - List user notifications
- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{id}/` - Get notification details
- `PUT /api/notifications/{id}/` - Update notification
- `DELETE /api/notifications/{id}/` - Delete notification
- `POST /api/notifications/{id}/read/` - Mark notification as read
- `POST /api/notifications/mark-all-read/` - Mark all notifications as read
- `GET /api/notifications/unread-count/` - Get unread notification count

### Announcements
- `GET /api/notifications/announcements/` - List announcements
- `POST /api/notifications/announcements/` - Create announcement
- `GET /api/notifications/announcements/{id}/` - Get announcement details
- `PUT /api/notifications/announcements/{id}/` - Update announcement
- `DELETE /api/notifications/announcements/{id}/` - Delete announcement

### Messages
- `GET /api/notifications/messages/` - List user messages
- `POST /api/notifications/messages/` - Send message
- `GET /api/notifications/messages/{id}/` - Get message details
- `PUT /api/notifications/messages/{id}/` - Update message
- `DELETE /api/notifications/messages/{id}/` - Delete message
- `POST /api/notifications/messages/{id}/reply/` - Reply to message
- `GET /api/notifications/conversations/` - Get user conversations

### Feedback
- `GET /api/notifications/feedback/` - List feedback
- `POST /api/notifications/feedback/` - Submit feedback
- `GET /api/notifications/feedback/{id}/` - Get feedback details
- `PUT /api/notifications/feedback/{id}/` - Update feedback
- `DELETE /api/notifications/feedback/{id}/` - Delete feedback
- `GET /api/notifications/my-feedback/` - Get user's feedback

### Notification Dashboard
- `GET /api/notifications/dashboard/` - Get notification dashboard data

## 🔧 Admin Endpoints

### Django Admin
- `GET /admin/` - Django admin interface
- `GET /admin/authentication/` - User management
- `GET /admin/courses/` - Course management
- `GET /admin/quizzes/` - Quiz management
- `GET /admin/progress/` - Progress management
- `GET /admin/notifications/` - Notification management

## 📋 Request/Response Examples

### User Login
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "student1",
    "password": "password123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "userid": 1,
        "username": "student1",
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com",
        "role": "Student"
    }
}
```

### Get Student Dashboard
```bash
GET /api/progress/dashboard/
Authorization: Bearer <access_token>

Response:
{
    "user": {
        "userid": 1,
        "username": "student1",
        "firstname": "John",
        "lastname": "Doe",
        "role": "Student"
    },
    "overall_progress": 75.5,
    "active_courses": 3,
    "completed_assignments": 12,
    "pending_assignments": 2,
    "quizzes_taken": 8,
    "average_quiz_score": 85.2,
    "attendance_percentage": 92.5,
    "recent_achievements": [...],
    "upcoming_assignments": [...],
    "study_plans": [...]
}
```

### Submit Quiz
```bash
POST /api/quizzes/1/submit/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "answers": [
        {
            "question_id": 1,
            "selected_option_id": 2
        },
        {
            "question_id": 2,
            "selected_option_id": 1
        }
    ]
}

Response:
{
    "message": "Quiz submitted successfully",
    "score": 85.0,
    "is_passed": true,
    "correct_answers": 17,
    "total_questions": 20,
    "time_taken": 25.5
}
```

## 🔒 Authentication

All API endpoints (except login and register) require JWT authentication:

```bash
Authorization: Bearer <your_access_token>
```

## 📊 Pagination

List endpoints support pagination:
- `?page=1` - Page number
- `?page_size=20` - Items per page

## 🔍 Filtering

Many endpoints support filtering:
- `?search=keyword` - Search functionality
- `?ordering=field` - Sort by field
- `?field=value` - Filter by specific field

## 🌐 Base URL

All endpoints are prefixed with your Django server URL:
- Development: `http://localhost:8000`
- Production: `https://yourdomain.com`

## 📱 Frontend Integration

Your React frontend can now connect to these endpoints:

```javascript
// Example API call
const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'student1',
        password: 'password123'
    })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
```

All your existing database data is now accessible through these comprehensive API endpoints! 🎉
