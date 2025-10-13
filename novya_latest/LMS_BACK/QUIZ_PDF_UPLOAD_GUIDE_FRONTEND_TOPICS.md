# 📚 Quiz PDF Upload Guide - Frontend Topic Names

## 🎯 **Overview**
This guide shows you exactly where to upload your quiz PDFs so they match the topic names in your frontend `Quizzes.jsx` component.

## 📁 **Backend Upload Location**
```
E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\
```

## 📋 **Exact Filenames to Upload**

### **Mathematics (maths/)**
Upload these files to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\maths\`

| Frontend Topic Name | Backend Filename | Description |
|-------------------|------------------|-------------|
| Lines and Angles | `maths_lines_and_angles_quiz.pdf` | Quiz questions about lines, angles, and geometry |
| Fractions | `maths_fractions_quiz.pdf` | Quiz questions about fractions, decimals, and percentages |

### **Science (science/)**
Upload these files to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\science\`

| Frontend Topic Name | Backend Filename | Description |
|-------------------|------------------|-------------|
| Electricity | `science_electricity_quiz.pdf` | Quiz questions about electrical circuits, current, voltage |
| Metals and Non-Metals | `science_metals_and_non_metals_quiz.pdf` | Quiz questions about properties of metals and non-metals |
| Human Biology | `science_human_biology_quiz.pdf` | Quiz questions about human body systems, organs, functions |

### **English (english/)**
Upload these files to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\english\`

| Frontend Topic Name | Backend Filename | Description |
|-------------------|------------------|-------------|
| Nutrition in Animals | `english_nutrition_in_animals_quiz.pdf` | Quiz questions about animal nutrition and digestive systems |
| Grammar | `english_grammar_quiz.pdf` | Quiz questions about English grammar, tenses, parts of speech |

### **Social Studies (social/)**
Upload these files to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\social\`

| Frontend Topic Name | Backend Filename | Description |
|-------------------|------------------|-------------|
| Indian History | `social_indian_history_quiz.pdf` | Quiz questions about Indian history, dynasties, events |
| World Geography | `social_world_geography_quiz.pdf` | Quiz questions about world geography, countries, capitals |

### **Computer Science (computer/)**
Upload these files to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\computer\`

| Frontend Topic Name | Backend Filename | Description |
|-------------------|------------------|-------------|
| MS Word Pictures | `computer_ms_word_pictures_quiz.pdf` | Quiz questions about MS Word, inserting pictures, formatting |
| Text Editing | `computer_text_editing_quiz.pdf` | Quiz questions about text editing, copy-paste, formatting |
| Programming Basics | `computer_programming_basics_quiz.pdf` | Quiz questions about basic programming concepts, variables, loops |

## 🚀 **How to Upload**

### **Method 1: Direct File Copy**
1. Navigate to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\`
2. Open the appropriate subject folder (maths, science, english, social, computer)
3. Copy your quiz PDF files with the exact filenames listed above

### **Method 2: Using File Explorer**
1. Open File Explorer
2. Go to: `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\class7\`
3. Navigate to the subject folder
4. Paste your PDF files and rename them to match the exact filenames

## 📝 **Important Notes**

### **File Naming Rules**
- ✅ **Use exact filenames** as listed above
- ✅ **Keep the `.pdf` extension**
- ✅ **Use lowercase letters and underscores**
- ❌ **Don't change the filenames** - they must match exactly

### **PDF Content Requirements**
- Your PDFs should contain **quiz questions** (not study material)
- Questions should be **multiple choice** format
- Include **correct answers** and **explanations**
- Make sure questions are **interactive and engaging**

### **Directory Structure**
```
media/quiz_pdfs/class7/
├── maths/
│   ├── maths_lines_and_angles_quiz.pdf
│   └── maths_fractions_quiz.pdf
├── science/
│   ├── science_electricity_quiz.pdf
│   ├── science_metals_and_non_metals_quiz.pdf
│   └── science_human_biology_quiz.pdf
├── english/
│   ├── english_nutrition_in_animals_quiz.pdf
│   └── english_grammar_quiz.pdf
├── social/
│   ├── social_indian_history_quiz.pdf
│   └── social_world_geography_quiz.pdf
└── computer/
    ├── computer_ms_word_pictures_quiz.pdf
    ├── computer_text_editing_quiz.pdf
    └── computer_programming_basics_quiz.pdf
```

## 🔗 **Frontend Integration**

Once you upload the PDFs, they will be accessible through these API endpoints:

- **Get all subjects**: `GET /api/quizzes/pdf/class7/subjects/`
- **Get topics for a subject**: `GET /api/quizzes/pdf/class7/{subject}/topics/`
- **Get quiz info**: `GET /api/quizzes/pdf/class7/{subject}/{topic}/info/`
- **Download PDF**: `GET /api/quizzes/pdf/class7/{subject}/{topic}/download/`

## 🧪 **Testing**

After uploading, you can test the system by:

1. **Starting the backend server**: `python manage.py runserver 8001`
2. **Testing API endpoints** using the test script
3. **Checking frontend integration** in the Quizzes section

## ❓ **FAQ**

**Q: Can I upload PDFs with different names?**
A: No, the filenames must match exactly as listed above for the system to work.

**Q: What if I have more topics than listed?**
A: You can add more topics by updating the `PDF_STRUCTURE` in `quizzes/pdf_quiz_views.py`.

**Q: Can I upload PDFs for other classes?**
A: Yes, you can create similar structures for class8, class9, class10, etc.

**Q: What format should the quiz questions be in?**
A: The PDFs should contain multiple-choice questions with options A, B, C, D and correct answers.

---

## 🎉 **Ready to Upload!**

Now you know exactly where to upload your quiz PDFs and what to name them. The system will automatically detect them and make them available in your frontend quiz section!

**Total files to upload: 12 quiz PDFs**
- Mathematics: 2 files
- Science: 3 files  
- English: 2 files
- Social Studies: 2 files
- Computer Science: 3 files
