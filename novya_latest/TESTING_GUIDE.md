# 🧪 Testing Guide - Dual Backend System

## Pre-Testing Checklist

Before starting, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] All dependencies installed
- [ ] OpenRouter API key ready

---

## Step-by-Step Testing Process

### Phase 1: Backend Setup & Testing

#### 1.1 Setup AI Backend (FastAPI)

```bash
# Navigate to AI Backend
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya_latest\AI_BACKEND

# Create .env file
copy .env.example .env
```

**Edit `.env` file and add your API key:**
```env
OPENROUTER_API_KEY=your_actual_api_key_here
```

**Get API Key**: https://openrouter.ai/keys

#### 1.2 Install AI Backend Dependencies

```bash
# Still in AI_BACKEND directory
pip install -r requirements.txt
```

Expected packages:
- fastapi
- uvicorn
- python-dotenv
- openai

#### 1.3 Test AI Backend Alone

```bash
# Start AI Backend
python app.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test in Browser:**
1. Open: http://localhost:8000
   - Should see: `{"message": "AI Learning Assistant API is running"}`

2. Open API Docs: http://localhost:8000/docs
   - Should see Swagger UI with all endpoints

3. Test an endpoint: http://localhost:8000/classes
   - Should return: `{"classes": ["7th", "8th", "9th", "10th"]}`

**✅ If all above work, AI Backend is ready!**

Press `Ctrl+C` to stop the server (we'll restart it with Django)

---

#### 1.4 Setup Django Backend

```bash
# Navigate to Django Backend
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya_latest\LMS_BACK

# Install dependencies (if not already done)
pip install -r requirements.txt
```

#### 1.5 Configure Django Database

Check `config/settings.py` - Update database settings if needed:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Or use SQLite for testing:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 1.6 Run Django Migrations

```bash
# Still in LMS_BACK directory
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

#### 1.7 Test Django Backend Alone

```bash
# Start Django on port 8001
python manage.py runserver 8001
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8001/
Quit the server with CTRL-BREAK.
```

**Test in Browser:**
1. Open: http://localhost:8001/api/
   - Should see Django REST Framework browsable API

2. Check endpoints:
   - http://localhost:8001/api/auth/
   - http://localhost:8001/api/courses/
   - http://localhost:8001/api/quizzes/

**✅ If Django loads successfully, it's ready!**

Press `Ctrl+C` to stop (we'll use the batch script next)

---

### Phase 2: Run Both Backends Together

#### 2.1 Start Both Backends Using Batch Script

```bash
# Navigate to novya_latest
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya_latest

# Run the master start script
start_all_backends.bat
```

**This will open TWO terminal windows:**

**Window 1: AI Backend (FastAPI)**
```
========================================
Starting AI Backend (FastAPI) on Port 8000
========================================
...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Window 2: Django Backend (LMS)**
```
========================================
Starting Django Backend (LMS) on Port 8001
========================================
...
Starting development server at http://127.0.0.1:8001/
```

#### 2.2 Verify Both Backends Are Running

Open these URLs in your browser:

**AI Backend (FastAPI):**
- ✅ http://localhost:8000 → Should show: `{"message": "AI Learning Assistant API is running"}`
- ✅ http://localhost:8000/docs → Should show Swagger API docs
- ✅ http://localhost:8000/classes → Should return class list

**Django Backend:**
- ✅ http://localhost:8001/api/ → Should show Django REST framework page
- ✅ http://localhost:8001/api/quizzes/ → Should show quizzes endpoint

**✅ If both respond, backends are running successfully!**

---

### Phase 3: Frontend Testing

#### 3.1 Verify Frontend Configuration

Check `novya-f/.env` exists (create from template if not):

```bash
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya-f

# Create .env if it doesn't exist
copy .env.example .env
```

**Contents should be:**
```env
REACT_APP_DJANGO_URL=http://localhost:8001/api
REACT_APP_FASTAPI_URL=http://localhost:8000
```

#### 3.2 Start Frontend

```bash
# In novya-f directory
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view lms_project in the browser.

  Local:            http://localhost:3000
```

**✅ Frontend should open in browser at http://localhost:3000**

---

### Phase 4: Feature Testing

Now test each feature to ensure backend integration works:

#### 4.1 Test Quick Practice (AI Quiz Generation)

1. **Navigate to Quick Practice** in the app
2. **Select**:
   - Class: 7th
   - Subject: Mathematics (or any subject)
   - Topic: Any topic from the dropdown
   - Language: English

3. **Click "Generate Quiz"**

**Expected Behavior:**
- ✅ Loading indicator appears
- ✅ 10 questions load
- ✅ Questions are in selected language
- ✅ Options are shuffled
- ✅ Can answer questions

**Check Browser Console (F12):**
```javascript
// Should see:
Fetching quiz with URL: http://localhost:8000/quiz?...
Language being sent: English
Quiz data received: {quiz: Array(10), currentLevel: 1}
```

**✅ If quiz generates, AI Backend integration works!**

---

#### 4.2 Test Mock Test (AI Mock Test Generation)

1. **Navigate to Mock Test** in the app
2. **Select**:
   - Class: 7th
   - Subject: Maths
   - Chapter: Any chapter
   - Language: English

3. **Click "Start Mock Test"**

**Expected Behavior:**
- ✅ Instructions screen appears
- ✅ Can start full-screen mode
- ✅ 50 questions load
- ✅ Timer starts (20 minutes)
- ✅ Can navigate between questions

**Check Browser Console (F12):**
```javascript
// Should see API call to:
http://localhost:8000/mock_test?class_name=7th&subject=Maths&...
```

**✅ If mock test generates with 50 questions, it works!**

---

#### 4.3 Test Language Support

Test Quick Practice with different languages:

1. **Select Hindi (हिंदी)**
   - Questions should be in Hindi script

2. **Select Telugu (తెలుగు)**
   - Questions should be in Telugu script

3. **Select Tamil (தமிழ்)**
   - Questions should be in Tamil script

**✅ If questions appear in different languages, multi-language support works!**

---

#### 4.4 Test Difficulty Progression

In Quick Practice:
1. Complete first quiz (Level 1 - Simple)
2. Generate another quiz for same topic
3. Check if difficulty increases (Level 2 - Medium)
4. Complete and generate again (Level 3 - Hard)

**✅ If difficulty increases, adaptive system works!**

---

### Phase 5: Error Handling Tests

#### 5.1 Test Network Error Handling

**Test 1: Stop AI Backend**
- Stop the FastAPI server (Ctrl+C in its window)
- Try to generate a Quick Practice quiz
- **Expected**: Error message appears gracefully

**Test 2: Stop Django Backend**
- Stop Django server (Ctrl+C in its window)
- Try to access courses or login
- **Expected**: Error message appears gracefully

**Restart both backends** after testing.

---

#### 5.2 Test Invalid API Key

1. Edit `AI_BACKEND/.env` with invalid key
2. Restart AI Backend
3. Try to generate quiz
4. **Expected**: Error message about API key

**Fix:** Restore correct API key and restart

---

### Phase 6: Performance Tests

#### 6.1 Quiz Generation Speed

**Quick Practice:**
- Time how long it takes to generate 10 questions
- **Expected**: 3-10 seconds (depends on AI API)

**Mock Test:**
- Time how long it takes to generate 50 questions
- **Expected**: 10-30 seconds

**✅ If responses come within reasonable time, performance is good!**

---

#### 6.2 Multiple Concurrent Requests

1. Open 2-3 browser tabs with the app
2. Generate quizzes simultaneously in all tabs
3. **Expected**: All should work without errors

**✅ If all tabs work, concurrency handling is good!**

---

## Testing Checklist

### Backend Testing ✅
- [ ] AI Backend starts on port 8000
- [ ] AI Backend API docs accessible
- [ ] AI Backend /classes endpoint works
- [ ] Django Backend starts on port 8001
- [ ] Django Backend API browsable
- [ ] Both backends run simultaneously
- [ ] No port conflicts

### Frontend Testing ✅
- [ ] Frontend starts on port 3000
- [ ] API configuration file loads
- [ ] Environment variables work
- [ ] No console errors on load

### Feature Testing ✅
- [ ] Quick Practice loads classes
- [ ] Quick Practice loads subjects
- [ ] Quick Practice loads topics
- [ ] Quick Practice generates 10 questions
- [ ] Mock Test loads classes
- [ ] Mock Test loads subjects
- [ ] Mock Test loads chapters
- [ ] Mock Test generates 50 questions
- [ ] Timer works in mock test
- [ ] Questions display correctly
- [ ] Options are shuffled
- [ ] Answers can be selected

### Language Testing ✅
- [ ] English questions work
- [ ] Hindi questions work
- [ ] Telugu questions work
- [ ] Tamil questions work
- [ ] Kannada questions work
- [ ] Malayalam questions work

### Difficulty Testing ✅
- [ ] Level 1 (Simple) questions generate
- [ ] Level 2 (Medium) questions after first attempt
- [ ] Level 3 (Hard) questions after second attempt
- [ ] Difficulty labels display correctly

### Error Handling ✅
- [ ] Network errors handled gracefully
- [ ] Loading states show correctly
- [ ] Error messages display properly
- [ ] Can retry after errors

### Performance ✅
- [ ] Quiz generation < 10 seconds
- [ ] Mock test generation < 30 seconds
- [ ] No lag in UI
- [ ] Memory usage reasonable

---

## Common Issues & Solutions

### Issue 1: "Port 8000 already in use"
**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill the process or choose different port
```

### Issue 2: "Module not found: API_CONFIG"
**Solution:**
- Check `novya-f/src/config/api.js` exists
- Restart React development server
- Clear browser cache

### Issue 3: "OPENROUTER_API_KEY not found"
**Solution:**
- Check `.env` file exists in `AI_BACKEND/`
- Verify API key is correct (no quotes needed)
- Restart AI Backend

### Issue 4: "CORS error"
**Solution:**
- Ensure both backends are running
- Check CORS is configured in both backends
- Clear browser cache

### Issue 5: "Empty quiz returned"
**Solution:**
- Check AI Backend logs for errors
- Verify API key has credits
- Check internet connection

### Issue 6: "Database error" (Django)
**Solution:**
- Run migrations: `python manage.py migrate`
- Check database connection settings
- Use SQLite for testing

---

## Success Criteria

Your system is **FULLY WORKING** if:

✅ Both backends start without errors
✅ Frontend loads without console errors
✅ Quick Practice generates quizzes
✅ Mock Tests generate 50 questions
✅ Multiple languages work
✅ Difficulty progression works
✅ No crashes or freezes
✅ Error messages are user-friendly

---

## Next Steps After Testing

Once everything works:

1. **Document any issues** encountered
2. **Note performance metrics**
3. **Plan for production deployment**
4. **Consider adding**:
   - User authentication integration
   - Quiz result saving to database
   - Analytics and tracking
   - More subjects/topics

---

## Getting Help

If you encounter issues:

1. **Check Backend Logs**:
   - AI Backend window for FastAPI errors
   - Django window for Django errors

2. **Check Browser Console** (F12):
   - Network tab for failed requests
   - Console tab for JavaScript errors

3. **Review Documentation**:
   - `README.md` for overview
   - `SETUP_COMPLETE.md` for setup
   - `INTEGRATION_STATUS.md` for status

4. **Test Endpoints Directly**:
   - Use browser or Postman
   - Check http://localhost:8000/docs
   - Check http://localhost:8001/api/

---

## Testing Complete! 🎉

If all tests pass, your NOVYA Learning Platform is:
- ✅ **Fully Integrated**
- ✅ **Production Ready**
- ✅ **Feature Complete**
- ✅ **Performance Optimized**

**Congratulations! Your dual-backend system is working!** 🚀

---

*Happy Testing!* 🧪✨

