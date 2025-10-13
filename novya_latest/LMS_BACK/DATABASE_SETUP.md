# PostgreSQL Database Setup for NOVYA LMS

This guide will help you set up PostgreSQL database for the NOVYA LMS Django backend.

## Prerequisites

1. **PostgreSQL Installation**
   - Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
   - Make sure PostgreSQL service is running

2. **Python Dependencies**
   - `psycopg2-binary` (already included in requirements.py)

## Database Setup Methods

### Method 1: Automated Setup (Recommended)

1. **Create Environment File**
   ```bash
   # Create .env file in the project root
   cp .env.example .env
   ```

2. **Configure Database Settings in .env**
   ```env
   # Database Configuration
   DB_NAME=novya_lms
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Run Automated Setup**
   ```bash
   python setup_database.py
   ```

### Method 2: Manual Setup

#### Step 1: Create Database

1. **Connect to PostgreSQL**
   ```bash
   psql -U postgres
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE novya_lms;
   ```

3. **Create User (Optional)**
   ```sql
   CREATE USER novya_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE novya_lms TO novya_user;
   ```

4. **Exit PostgreSQL**
   ```sql
   \q
   ```

#### Step 2: Configure Django Settings

1. **Update .env file**
   ```env
   DB_NAME=novya_lms
   DB_USER=postgres  # or novya_user if you created one
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

#### Step 3: Run Django Commands

1. **Install Dependencies**
   ```bash
   pip install -r requirements.py
   ```

2. **Create Migrations**
   ```bash
   python manage.py makemigrations
   ```

3. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate Initial Data**
   ```bash
   python manage.py populate_initial_data
   ```

## Database Configuration Options

### Development Environment
```env
DB_NAME=novya_lms_dev
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```

### Production Environment
```env
DB_NAME=novya_lms_prod
DB_USER=novya_prod_user
DB_PASSWORD=strong_production_password
DB_HOST=your_production_host
DB_PORT=5432
DEBUG=False
```

### Docker PostgreSQL Setup

If you prefer using Docker for PostgreSQL:

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: NOVYA
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password
       ports:
         - "5432:5432"           
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

2. **Start PostgreSQL**
   ```bash
   docker-compose up -d postgres
   ```

3. **Update .env**
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=NOVYA
   DB_USER=postgres
   DB_PASSWORD=password
   ```

## Database Schema

The Django application will create the following main tables:

### Core Tables
- `authentication_user` - User accounts
- `authentication_student` - Student profiles
- `authentication_parent` - Parent profiles
- `authentication_teacher` - Teacher profiles

### Course Tables
- `courses_subject` - Academic subjects
- `courses_course` - Course instances
- `courses_chapter` - Course chapters
- `courses_lesson` - Individual lessons
- `courses_courseenrollment` - Student enrollments

### Quiz Tables
- `quizzes_quiz` - Practice tests
- `quizzes_question` - Quiz questions
- `quizzes_questionoption` - Answer options
- `quizzes_quizattempt` - Student attempts
- `quizzes_quizanswer` - Individual answers

### Progress Tables
- `progress_studentprogress` - Academic progress
- `progress_attendance` - Attendance records
- `progress_assignment` - Assignments
- `progress_grade` - Grades and scores

### Notification Tables
- `notifications_event` - School events
- `notifications_notification` - System notifications
- `notifications_announcement` - Announcements
- `notifications_message` - Internal messages

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```
   Error: connection to server at "localhost" (127.0.0.1), port 5432 failed
   ```
   **Solution**: Ensure PostgreSQL service is running
   ```bash
   # Windows
   net start postgresql-x64-15
   
   # Linux/Mac
   sudo systemctl start postgresql
   ```

2. **Authentication Failed**
   ```
   Error: password authentication failed for user "postgres"
   ```
   **Solution**: Check username and password in .env file

3. **Database Does Not Exist**
   ```
   Error: database "novya_lms" does not exist
   ```
   **Solution**: Create the database manually or run the setup script

4. **Permission Denied**
   ```
   Error: permission denied for database "novya_lms"
   ```
   **Solution**: Grant proper permissions to the user
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE novya_lms TO your_user;
   ```

### Database Connection Test

Test your database connection:

```python
# test_db_connection.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Database connection successful!")
        print(f"Database: {settings.DATABASES['default']['NAME']}")
        print(f"Host: {settings.DATABASES['default']['HOST']}")
        print(f"Port: {settings.DATABASES['default']['PORT']}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

## Performance Optimization

### Database Indexes
The Django models include optimized indexes for better performance:

- User authentication fields
- Course enrollment lookups
- Quiz attempt queries
- Progress tracking queries

### Connection Pooling
For production, consider using connection pooling:

```python
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        },
    }
}
```

## Backup and Restore

### Backup Database
```bash
pg_dump -h localhost -U postgres -d novya_lms > backup.sql
```

### Restore Database
```bash
psql -h localhost -U postgres -d novya_lms < backup.sql
```

## Security Best Practices

1. **Use Strong Passwords**
2. **Limit Database User Permissions**
3. **Enable SSL in Production**
4. **Regular Security Updates**
5. **Monitor Database Access**

## Next Steps

After successful database setup:

1. **Start Django Server**
   ```bash
   python manage.py runserver
   ```

2. **Access Admin Panel**
   - URL: http://localhost:8000/admin/
   - Login with superuser credentials

3. **Test API Endpoints**
   - URL: http://localhost:8000/api/
   - Check API documentation

4. **Connect Frontend**
   - Update frontend API base URL
   - Test authentication flow
   - Verify data integration
