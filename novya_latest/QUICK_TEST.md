# ⚡ Quick Test - 5 Minutes

**Fast test to verify everything works!**

## 1. Add API Key (30 seconds)

```bash
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya_latest\AI_BACKEND
copy .env.example .env
```

Edit `.env` and add your OpenRouter API key.

## 2. Start Backends (1 minute)

```bash
cd C:\Users\chavi\OneDrive\Desktop\novoo\novya_latest
start_all_backends.bat
```

**Two windows will open. Wait for:**
- Window 1: `Uvicorn running on http://0.0.0.0:8000`
- Window 2: `Starting development server at http://127.0.0.1:8001/`

## 3. Test Backends (1 minute)

Open in browser:
- ✅ http://localhost:8000 → Should show API message
- ✅ http://localhost:8001/api/ → Should show Django API

## 4. Start Frontend (1 minute)

Your frontend is already running on http://localhost:3000
Just **refresh the page**.

## 5. Test Features (2 minutes)

### Quick Practice:
1. Go to Quick Practice
2. Select: 7th → Mathematics → Any topic
3. Click "Generate Quiz"
4. ✅ Should load 10 questions

### Mock Test:
1. Go to Mock Test
2. Select: 7th → Maths → Any chapter
3. Click "Start Test"
4. ✅ Should load 50 questions

## ✅ Done!

If both features work, **your system is fully functional!** 🎉

---

**For detailed testing, see:** `TESTING_GUIDE.md`

