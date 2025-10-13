# Quiz PDF Upload Guide

## 📁 **Where to Upload Your Quiz PDFs**

### **Backend Media Folder Structure**
```
novya_latest/LMS_BACK/media/quiz_pdfs/
├── class7/
│   ├── maths/
│   │   ├── maths_integers_quiz.pdf
│   │   ├── maths_fractions_quiz.pdf
│   │   ├── maths_algebra_quiz.pdf
│   │   ├── maths_geometry_quiz.pdf
│   │   └── maths_statistics_quiz.pdf
│   ├── science/
│   │   ├── science_nutrition_quiz.pdf
│   │   ├── science_respiration_quiz.pdf
│   │   ├── science_transportation_quiz.pdf
│   │   ├── science_reproduction_quiz.pdf
│   │   └── science_motion_quiz.pdf
│   ├── english/
│   │   ├── english_grammar_quiz.pdf
│   │   ├── english_vocabulary_quiz.pdf
│   │   ├── english_comprehension_quiz.pdf
│   │   ├── english_writing_quiz.pdf
│   │   └── english_literature_quiz.pdf
│   ├── social/
│   │   ├── social_history_quiz.pdf
│   │   ├── social_geography_quiz.pdf
│   │   ├── social_civics_quiz.pdf
│   │   ├── social_economics_quiz.pdf
│   │   └── social_culture_quiz.pdf
│   └── computer/
│       ├── computer_basics_quiz.pdf
│       ├── computer_programming_quiz.pdf
│       ├── computer_internet_quiz.pdf
│       ├── computer_security_quiz.pdf
│       └── computer_applications_quiz.pdf
├── class8/
│   ├── maths/
│   ├── science/
│   ├── english/
│   ├── social/
│   └── computer/
├── class9/
│   ├── maths/
│   ├── science/
│   ├── english/
│   ├── social/
│   └── computer/
└── class10/
    ├── maths/
    ├── science/
    ├── english/
    ├── social/
    └── computer/
```

## 🎯 **How to Upload**

### **Method 1: Direct File Copy**
1. Navigate to `novya_latest/LMS_BACK/media/quiz_pdfs/`
2. Create the appropriate folder structure if needed
3. Copy your quiz PDFs to the correct folders
4. Use the exact filenames specified above

### **Method 2: Using File Explorer**
1. Open File Explorer
2. Navigate to `E:\cursornov\novya_latest\LMS_BACK\media\quiz_pdfs\`
3. Create folders as needed
4. Drag and drop your PDF files

### **Method 3: Using Command Line**
```bash
# Navigate to the backend directory
cd novya_latest/LMS_BACK

# Copy your PDFs to the appropriate folders
copy "path\to\your\quiz.pdf" "media\quiz_pdfs\class7\maths\maths_integers_quiz.pdf"
```

## 📋 **File Naming Convention**

### **Class 7 Quiz PDFs**
- **Mathematics**: `maths_[topic]_quiz.pdf`
- **Science**: `science_[topic]_quiz.pdf`
- **English**: `english_[topic]_quiz.pdf`
- **Social Studies**: `social_[topic]_quiz.pdf`
- **Computer Science**: `computer_[topic]_quiz.pdf`

### **Examples**
- `maths_integers_quiz.pdf`
- `science_nutrition_quiz.pdf`
- `english_grammar_quiz.pdf`
- `social_history_quiz.pdf`
- `computer_basics_quiz.pdf`

## ✅ **After Uploading**

1. **Restart Django Server**:
   ```bash
   python manage.py runserver 8001
   ```

2. **Test the Upload**:
   - Visit: `http://localhost:8001/api/quizzes/pdf/structure/`
   - Check if your PDFs are detected as available

3. **Access in Frontend**:
   - Your quiz PDFs will appear in the quiz section
   - Students can download and take the quizzes

## 🔧 **Adding More Classes/Subjects**

To add more classes or subjects:

1. **Create the folder structure**:
   ```bash
   mkdir media\quiz_pdfs\class8\maths
   mkdir media\quiz_pdfs\class8\science
   # ... etc
   ```

2. **Update the PDF_STRUCTURE** in `quizzes/pdf_quiz_views.py`

3. **Add your PDFs** with the correct filenames

4. **Restart the server**

## 📊 **Current Status**

- ✅ **Folder Structure**: Created
- ✅ **Backend Integration**: Ready
- ✅ **API Endpoints**: Working
- ⏳ **PDF Upload**: Waiting for your quiz PDFs

## 🎮 **How It Works**

1. **Upload**: Place your quiz PDFs in the media folder
2. **Detection**: System automatically detects available PDFs
3. **API**: PDFs are served through REST API endpoints
4. **Frontend**: PDFs appear in your quiz section
5. **Download**: Students can download and take quizzes
6. **Interactive**: PDFs can be made interactive through the system

## 💡 **Benefits of Backend Approach**

- ✅ **Centralized Management**: All quiz PDFs in one place
- ✅ **Easy Updates**: Just replace PDF files
- ✅ **No Frontend Changes**: Works with existing UI
- ✅ **Scalable**: Easy to add more classes/subjects
- ✅ **Secure**: PDFs served through authenticated API
- ✅ **Organized**: Clear folder structure by class/subject

## 🚀 **Next Steps**

1. **Upload your quiz PDFs** to the appropriate folders
2. **Use the exact filenames** specified above
3. **Restart the Django server**
4. **Test the system** through the API endpoints
5. **Integrate with frontend** using the provided examples

Your quiz PDFs will then be available in the quiz section and students can download and take them interactively! 🎉
