# 🚀 NOVYA LMS Quick Start Guide

Get your Django backend with PostgreSQL up and running in minutes!

## 🎯 One-Command Setup

### Windows
```cmd
setup_windows.bat
```

### macOS
```bash
./setup_macos.sh
```

### Linux
```bash
./setup_linux.sh
```

## 📋 What These Scripts Do

1. **Check Prerequisites**: Verify Python and PostgreSQL installation
2. **Install Dependencies**: Install required Python packages
3. **Setup Database**: Create PostgreSQL database and run migrations
4. **Configure Environment**: Create .env file with proper settings
5. **Ready to Go**: Your Django backend is ready!

## 🔧 Manual Setup (Alternative)

If you prefer manual setup or the automated scripts don't work:

### 1. Install PostgreSQL
- **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql@15`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### 2. Start PostgreSQL
- **Windows**: `net start postgresql`
- **macOS**: `brew services start postgresql@15`
- **Linux**: `sudo systemctl start postgresql`

### 3. Run Setup Script
```bash
python setup_local_postgresql.py
```

### 4. Complete Setup
```bash
# Update .env file with your PostgreSQL password
# Then run:
python manage.py createsuperuser
python manage.py populate_initial_data
python manage.py runserver
```

## ✅ Verification

### Test Database Connection
```bash
python test_db_connection.py
```

### Access Your Application
- **Django Admin**: http://localhost:8000/admin/
- **API Endpoints**: http://localhost:8000/api/
- **API Documentation**: http://localhost:8000/api/docs/

## 🎉 You're Ready!

Your NOVYA LMS Django backend is now running with PostgreSQL! 

### Next Steps:
1. **Connect Frontend**: Update your React app to use the API endpoints
2. **Create Users**: Use the admin panel or API to create students, parents, and teachers
3. **Add Content**: Create courses, lessons, and quizzes
4. **Test Features**: Try the authentication, course enrollment, and quiz features

## 🆘 Need Help?

- **Detailed Setup**: See [LOCAL_POSTGRESQL_SETUP.md](LOCAL_POSTGRESQL_SETUP.md)
- **Full Documentation**: See [README.md](README.md)
- **Database Issues**: Run `python test_db_connection.py` for diagnostics

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - Get user profile

### Courses
- `GET /api/courses/` - List courses
- `POST /api/courses/{id}/enroll/` - Enroll in course
- `GET /api/courses/{id}/progress/` - Course progress

### Quizzes
- `GET /api/quizzes/` - List quizzes
- `POST /api/quizzes/{id}/start/` - Start quiz
- `POST /api/quizzes/{id}/submit/` - Submit quiz

### Progress
- `GET /api/progress/dashboard/` - Student dashboard
- `GET /api/progress/parent-dashboard/` - Parent dashboard

Happy coding! 🎓
