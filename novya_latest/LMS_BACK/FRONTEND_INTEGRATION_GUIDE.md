# 🔗 Frontend Integration Guide for PDF Quizzes

## 📍 **Where to Find Quizzes in Frontend:**

### **Current Location:**
- **Student Portal** → **Quizzes** section
- **URL**: `http://localhost:3000` (after login) → Navigate to Quizzes

### **Current Status:**
- ✅ Frontend has Quizzes section with 10 questions per topic
- ❌ Frontend is NOT connected to backend API yet
- ❌ Frontend uses hardcoded questions instead of PDF-extracted questions

## 🔧 **Integration Required:**

The frontend `Quizzes.jsx` needs to be updated to:

1. **Call backend API** instead of using hardcoded questions
2. **Load questions** from your uploaded PDFs
3. **Submit answers** to backend for scoring
4. **Display results** with explanations

## 📊 **Question Count Comparison:**

### **Current Frontend (Hardcoded):**
- **10 questions per topic** (130 total questions)
- **13 topics** including Computer Science
- **Static questions** that don't change

### **New Backend (PDF-based):**
- **2-3 questions per topic** (extracted from your PDFs)
- **5 Computer Science topics** from your uploaded PDFs
- **Dynamic questions** that can be updated by uploading new PDFs

## 🎯 **Integration Steps:**

### **Step 1: Update Frontend API Calls**
Replace hardcoded questions with API calls to:
```
GET /api/quizzes/pdf/class7/computer/programming_language/questions/
POST /api/quizzes/pdf/class7/computer/programming_language/submit/
```

### **Step 2: Map Topic Names**
Map frontend topic names to backend endpoints:
- "MS Word Pictures" → "microsoft_word"
- "Text Editing" → "microsoft_word" 
- "Programming Basics" → "programming_language"

### **Step 3: Handle New Response Format**
Backend returns questions in this format:
```json
{
  "topic_name": "Programming Language",
  "total_questions": 3,
  "questions": [
    {
      "id": 1,
      "question_text": "What is a programming language?",
      "options": [
        {"option_id": "a", "option_text": "A way to communicate with computers", "is_correct": true},
        {"option_id": "b", "option_text": "A type of computer hardware", "is_correct": false}
      ],
      "correct_option": "a",
      "explanation": "A programming language is a formal language...",
      "points": 1
    }
  ]
}
```

## 🚀 **Quick Integration Option:**

### **Option 1: Keep Current Frontend + Add PDF Quizzes**
- Keep existing 10-question topics as they are
- Add new "PDF Quizzes" section for your uploaded content
- Students can choose between static quizzes or PDF-based quizzes

### **Option 2: Replace with PDF Quizzes**
- Replace hardcoded questions with PDF-extracted questions
- Update all topics to use backend API
- Students get questions from your uploaded PDFs

## 🧪 **Testing the Current System:**

### **To Test Backend API:**
```bash
# Get questions
curl -H "Authorization: Bearer <token>" \
  http://localhost:8001/api/quizzes/pdf/class7/computer/programming_language/questions/

# Submit answers
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"answers": [{"question_id": 1, "selected_option": "a"}]}' \
  http://localhost:8001/api/quizzes/pdf/class7/computer/programming_language/submit/
```

### **To Test Frontend:**
1. **Login** to student portal
2. **Navigate** to Quizzes section
3. **Select** any Computer Science topic
4. **Take quiz** with current hardcoded questions

## 🎯 **Recommendation:**

**Start with Option 1** - Add a new "PDF Quizzes" section alongside the existing quizzes. This way:
- ✅ Students keep access to current 10-question quizzes
- ✅ Students also get access to your PDF-based quizzes
- ✅ No risk of breaking existing functionality
- ✅ Easy to test and compare both systems

## 📝 **Next Steps:**

1. **Test current frontend** to see existing quiz functionality
2. **Choose integration approach** (Option 1 or 2)
3. **Update frontend code** to call backend API
4. **Test integrated system** with your PDF quizzes
5. **Deploy** for students to use

Would you like me to help implement the frontend integration?
