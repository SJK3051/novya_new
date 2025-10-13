# 🎓 NOVYA Learning Platform - Integrated System

Welcome to the NOVYA Learning Platform! This is a complete Learning Management System (LMS) with AI-powered features for students in Classes 7-10.

## 📋 System Architecture

This project uses a **microservices architecture** with:

```
┌─────────────────────────────────────────────────────────────┐
│                    NOVYA Learning Platform                  │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
        ┌───────▼────────┐         ┌───────▼────────┐
        │   Frontend     │         │   Frontend     │
        │   (novya-f)    │         │  (lms_front)   │
        │   Port: 3000   │         │  Port: 3001    │
        │   React App    │         │   React App    │
        └───────┬────────┘         └───────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
            ┌───────▼───────┐    ┌──────▼──────┐
            │ Django Backend│    │ AI Backend  │
            │  (LMS_BACK)   │    │(AI_BACKEND) │
            │  Port: 8001   │    │ Port: 8000  │
            │   Database    │    │   FastAPI   │
            │  Operations   │    │ AI Features │
            └───────────────┘    └─────────────┘
```

### Components:

#### 1. **novya-f** (Main Frontend) ✅ ACTIVE
- **Technology**: React 19
- **Port**: 3000
- **Purpose**: Modern, updated UI for the learning platform
- **Features**: Student dashboard, courses, quizzes, mock tests, AI chatbot

#### 2. **LMS_BACK** (Django Backend) ✅ ACTIVE
- **Technology**: Django 4.2 + Django REST Framework
- **Port**: 8001
- **Database**: PostgreSQL
- **Purpose**: Core backend for database operations
- **Features**:
  - User authentication (students, parents, teachers)
  - Course management
  - Database-based quizzes (static, PDF-based)
  - Progress tracking
  - Notifications
  - User profiles

#### 3. **AI_BACKEND** (FastAPI Backend) ✅ ACTIVE
- **Technology**: FastAPI + OpenRouter API
- **Port**: 8000
- **Purpose**: AI-powered features (stateless)
- **Features**:
  - 🤖 AI Quiz Generation (adaptive difficulty)
  - 📝 AI Mock Test Generation (50 questions)
  - 💬 AI Chatbot (student tutor)
  - 📚 AI Study Plan Generator
  - 📖 AI Notes Generator
  - 🌐 Multi-language support (6 languages)

#### 4. **lms_front** (Old Frontend) ⚠️ LEGACY
- **Status**: Kept for reference, use `novya-f` instead
- **Port**: 3001 (if needed)

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (for Django backend)
- OpenRouter API Key (for AI features)

### Step 1: Setup AI Backend (FastAPI)

```bash
# Navigate to AI Backend
cd novya_latest/AI_BACKEND

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add your OpenRouter API key
# OPENROUTER_API_KEY=your_key_here

# Start the server
python app.py
```

✅ AI Backend will run on **http://localhost:8000**

### Step 2: Setup Django Backend

```bash
# Navigate to Django Backend
cd novya_latest/LMS_BACK

# Install dependencies
pip install -r requirements.txt

# Configure database in config/settings.py
# Default: PostgreSQL

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver 8001
```

✅ Django Backend will run on **http://localhost:8001**

### Step 3: Setup Frontend (novya-f)

```bash
# Navigate to frontend
cd novya-f

# Install dependencies (if not already done)
npm install --legacy-peer-deps

# Create .env file
copy .env.example .env

# Start the development server
npm start
```

✅ Frontend will run on **http://localhost:3000**

### 🎯 Quick Start (All at Once)

For Windows, use the convenience script:

```bash
cd novya_latest
start_all_backends.bat
```

Then in a separate terminal:
```bash
cd novya-f
npm start
```

---

## 📁 Project Structure

```
novya_latest/
├── AI_BACKEND/              # FastAPI - AI Features
│   ├── app.py              # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   ├── start.bat           # Windows startup script
│   └── README.md           # AI Backend documentation
│
├── LMS_BACK/               # Django - Database Operations
│   ├── config/             # Django settings
│   ├── authentication/     # User auth module
│   ├── courses/            # Course management
│   ├── quizzes/            # Quiz system
│   ├── progress/           # Progress tracking
│   ├── notifications/      # Notifications
│   ├── manage.py           # Django management
│   ├── requirements.txt    # Python dependencies
│   ├── start.bat           # Windows startup script
│   └── [various docs]      # API documentation
│
├── lms_front/              # Old React Frontend (legacy)
│   └── [React app files]
│
├── start_all_backends.bat  # Start both backends
└── README.md               # This file

novya-f/                    # Main React Frontend (ACTIVE)
├── src/
│   ├── config/
│   │   └── api.js          # API configuration for both backends
│   ├── modules/
│   │   ├── home/           # Landing pages
│   │   ├── login/          # Authentication
│   │   ├── student/        # Student dashboard
│   │   └── parent/         # Parent dashboard
│   ├── i18n/               # Internationalization
│   └── App.js              # Main app component
├── package.json
├── .env.example
└── README.md
```

---

## 🔌 API Endpoints Overview

### Django Backend (http://localhost:8001/api)

```
Authentication:
POST   /api/auth/login/
POST   /api/auth/register/
POST   /api/auth/logout/
GET    /api/auth/profile/

Courses:
GET    /api/courses/
GET    /api/courses/{id}/
POST   /api/courses/{id}/enroll/
GET    /api/courses/my-courses/

Quizzes:
GET    /api/quizzes/
GET    /api/quizzes/{id}/
POST   /api/quizzes/{id}/start/
POST   /api/quizzes/{id}/submit/
GET    /api/quizzes/my-attempts/

Progress:
GET    /api/progress/
GET    /api/progress/course/{id}/
POST   /api/progress/update/
```

### FastAPI Backend (http://localhost:8000)

```
Quick Practice:
GET    /classes
GET    /chapters?class_name={class}
GET    /subtopics?class_name={class}&subject={subject}
GET    /quiz?subtopic={topic}&language={lang}&currentLevel={level}

Mock Tests:
GET    /mock_classes
GET    /mock_subjects?class_name={class}
GET    /mock_chapters?class_name={class}&subject={subject}
GET    /mock_test?class_name={class}&subject={subject}&chapter={chapter}&language={lang}

AI Assistant:
POST   /ai-assistant/chat
POST   /ai-assistant/generate-study-plan
POST   /ai-assistant/generate-notes
```

---

## 🎨 Features

### For Students
- 📚 Browse and enroll in courses
- 📝 Take quizzes and mock tests
- 🤖 AI-generated practice questions
- 💬 Chat with AI tutor for help
- 📊 Track learning progress
- 🎯 Get personalized study plans
- 📖 AI-generated notes and summaries
- 🌐 Multi-language support

### For Parents
- 👀 Monitor child's progress
- 📈 View performance analytics
- 📅 Check attendance
- 💰 Manage fees
- 📚 Track homework completion

### For Administrators
- 👥 Manage users (students, parents, teachers)
- 📚 Create and manage courses
- 📝 Create database quizzes
- 📊 Generate reports
- 🔔 Send notifications

---

## 🛠️ Development

### Frontend Development (novya-f)
```bash
cd novya-f
npm start          # Development server
npm run build      # Production build
npm test           # Run tests
```

### Backend Development

**Django:**
```bash
cd novya_latest/LMS_BACK
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
python manage.py runserver 8001  # Development server
```

**FastAPI:**
```bash
cd novya_latest/AI_BACKEND
uvicorn app:app --reload --port 8000  # Development with auto-reload
```

---

## 🔐 Security & Environment Variables

### AI Backend (.env)
```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Django Backend (config/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Frontend (.env)
```env
REACT_APP_DJANGO_URL=http://localhost:8001/api
REACT_APP_FASTAPI_URL=http://localhost:8000
```

---

## 📦 Deployment

### Production Checklist

#### Backend (Django)
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up production database (PostgreSQL)
- [ ] Configure static files serving
- [ ] Set up CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up gunicorn/uwsgi
- [ ] Configure Nginx reverse proxy

#### Backend (FastAPI)
- [ ] Set up process manager (Supervisor/systemd)
- [ ] Configure Nginx reverse proxy
- [ ] Restrict CORS to your domain
- [ ] Monitor OpenRouter API usage
- [ ] Set up rate limiting

#### Frontend
- [ ] Build production bundle: `npm run build`
- [ ] Update environment variables for production
- [ ] Deploy to hosting (Vercel, Netlify, AWS, etc.)
- [ ] Configure CDN for static assets
- [ ] Set up proper domain and SSL

---

## 🐛 Troubleshooting

### Issue: CORS Errors
**Solution**: Both backends have CORS configured for development. In production, restrict to your domain.

### Issue: Database Connection Failed
**Solution**: Check PostgreSQL is running and credentials in `config/settings.py` are correct.

### Issue: AI Backend Returns Errors
**Solution**: Verify OPENROUTER_API_KEY is valid and has credits.

### Issue: Frontend Can't Connect to Backends
**Solution**: 
1. Check both backends are running
2. Verify `.env` file has correct URLs
3. Check browser console for specific errors

### Issue: npm install fails
**Solution**: Use `npm install --legacy-peer-deps` due to React 19 compatibility.

---

## 📝 API Documentation

- **Django API**: Available at `http://localhost:8001/api/` (Django REST Framework browsable API)
- **FastAPI API**: Available at `http://localhost:8000/docs` (Swagger UI)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

[Add your license here]

---

## 👥 Support

For issues, questions, or contributions:
- Check the documentation in each component's README
- Review API documentation
- Check troubleshooting section

---

## 🎉 Credits

Built with:
- React 19
- Django 4.2
- FastAPI
- PostgreSQL
- OpenRouter AI (Gemini 2.0 Flash)

---

**Happy Learning! 🎓✨**

