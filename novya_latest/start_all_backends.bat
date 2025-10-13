@echo off
echo ========================================
echo   NOVYA Learning Platform - Backend Starter
echo ========================================
echo.
echo Starting both backend services...
echo.
echo [1/2] Starting AI Backend (FastAPI) on port 8000...
start "AI Backend (FastAPI)" cmd /k "cd AI_BACKEND && python app.py"
timeout /t 3 >nul

echo [2/2] Starting Django Backend (LMS) on port 8001...
start "Django Backend (LMS)" cmd /k "cd LMS_BACK && python manage.py runserver 8001"

echo.
echo ========================================
echo   Both backends are starting!
echo ========================================
echo.
echo AI Backend (FastAPI):     http://localhost:8000
echo Django Backend (LMS):     http://localhost:8001/api
echo.
echo Two new terminal windows have been opened.
echo Press any key to exit this window...
pause >nul

