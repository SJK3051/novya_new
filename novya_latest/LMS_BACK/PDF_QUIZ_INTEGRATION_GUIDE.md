# PDF Quiz Integration Guide

## Overview
This guide explains how to integrate the PDF-based quiz system with your existing frontend quiz section. The system serves your existing PDFs organized by class/subject/topic/chapter and integrates seamlessly with your current `Quizzes.jsx` component.

## Available PDF Structure

### Classes Available
- **Class 7**: 25 PDFs (5 subjects × 5 topics each)
- **Class 8**: 25 PDFs (5 subjects × 5 topics each)  
- **Class 9**: 25 PDFs (5 subjects × 5 topics each)
- **Class 10**: 25 PDFs (5 subjects × 5 topics each)

### Subjects per Class
- Mathematics
- Science
- English
- Social Studies
- Computer Science

### Topics per Subject
- **Class 7**: 5 chapters/units per subject
- **Class 8-10**: 5 chapters per subject

## API Endpoints

### 1. Get PDF Quiz Structure
```
GET /api/quizzes/pdf/structure/
```
**Response:**
```json
{
  "structure": {
    "class7": {
      "name": "Class 7",
      "subjects": {
        "maths": {
          "name": "Mathematics",
          "topics": {
            "chapter1": {
              "name": "Chapter 1",
              "file": "maths ch-1.pdf",
              "available": true
            }
          }
        }
      }
    }
  },
  "total_classes": 4,
  "total_subjects": 20,
  "total_topics": 100
}
```

### 2. Get Subjects for a Class
```
GET /api/quizzes/pdf/{class_name}/subjects/
```
**Example:** `/api/quizzes/pdf/class7/subjects/`

### 3. Get Topics for a Subject
```
GET /api/quizzes/pdf/{class_name}/{subject}/topics/
```
**Example:** `/api/quizzes/pdf/class7/maths/topics/`

### 4. Get PDF Quiz Info
```
GET /api/quizzes/pdf/{class_name}/{subject}/{topic}/info/
```
**Example:** `/api/quizzes/pdf/class7/maths/chapter1/info/`

### 5. Download PDF
```
GET /api/quizzes/pdf/{class_name}/{subject}/{topic}/download/
```
**Example:** `/api/quizzes/pdf/class7/maths/chapter1/download/`

### 6. Get Frontend Integration Data
```
GET /api/quizzes/pdf/{class_name}/{subject}/{topic}/
```
**Example:** `/api/quizzes/pdf/class7/maths/chapter1/`

**Response:**
```json
{
  "id": "class7-maths-chapter1",
  "name": "Chapter 1",
  "lesson": "Mathematics",
  "class": "Class 7",
  "subject": "maths",
  "topic": "chapter1",
  "file": "maths ch-1.pdf",
  "download_url": "/api/quizzes/pdf/class7/maths/chapter1/download/",
  "type": "pdf_quiz",
  "description": "PDF Quiz for Chapter 1 - Mathematics",
  "instructions": [
    "This is a PDF-based quiz",
    "Download the PDF to view the questions",
    "Answer the questions in the PDF",
    "Submit your answers through the system"
  ]
}
```

### 7. Search PDF Quizzes
```
GET /api/quizzes/pdf/search/?q={query}&class={class}&subject={subject}
```
**Example:** `/api/quizzes/pdf/search/?q=chapter&class=class7`

### 8. Get PDF Statistics
```
GET /api/quizzes/pdf/statistics/
```

## Frontend Integration

### Option 1: Extend Existing Quizzes.jsx Component

Add PDF quizzes to your existing `subjects` array in `Quizzes.jsx`:

```jsx
// Add this function to fetch PDF quizzes
const fetchPDFQuizzes = async () => {
  try {
    const response = await fetch('/api/quizzes/pdf/structure/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
      }
    });
    const data = await response.json();
    
    // Convert PDF structure to your existing format
    const pdfQuizzes = [];
    for (const [classKey, classData] of Object.entries(data.structure)) {
      for (const [subjectKey, subjectData] of Object.entries(classData.subjects)) {
        for (const [topicKey, topicData] of Object.entries(subjectData.topics)) {
          if (topicData.available) {
            pdfQuizzes.push({
              id: `${classKey}-${subjectKey}-${topicKey}`,
              name: topicData.name,
              lesson: subjectData.name,
              class: classData.name,
              type: 'pdf_quiz',
              image: getSubjectImage(subjectKey), // You can create this function
              color: getSubjectColor(subjectKey), // You can create this function
              download_url: `/api/quizzes/pdf/${classKey}/${subjectKey}/${topicKey}/download/`,
              instructions: [
                "This is a PDF-based quiz",
                "Download the PDF to view the questions",
                "Answer the questions in the PDF",
                "Submit your answers through the system"
              ]
            });
          }
        }
      }
    }
    
    return pdfQuizzes;
  } catch (error) {
    console.error('Error fetching PDF quizzes:', error);
    return [];
  }
};

// Update your subjects array to include PDF quizzes
const [subjects, setSubjects] = useState([]);

useEffect(() => {
  const loadQuizzes = async () => {
    const existingQuizzes = [
      // Your existing hardcoded quizzes
    ];
    
    const pdfQuizzes = await fetchPDFQuizzes();
    setSubjects([...existingQuizzes, ...pdfQuizzes]);
  };
  
  loadQuizzes();
}, []);
```

### Option 2: Create a Separate PDF Quiz Component

Create a new component `PDFQuizComponent.jsx`:

```jsx
import React, { useState, useEffect } from 'react';
import { Download, FileText, ArrowLeft } from 'lucide-react';

const PDFQuizComponent = ({ class_name, subject, topic, onBack }) => {
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuizData = async () => {
      try {
        const response = await fetch(
          `/api/quizzes/pdf/${class_name}/${subject}/${topic}/`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              'Content-Type': 'application/json'
            }
          }
        );
        const data = await response.json();
        setQuizData(data);
      } catch (error) {
        console.error('Error fetching quiz data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuizData();
  }, [class_name, subject, topic]);

  const handleDownload = () => {
    if (quizData) {
      window.open(quizData.download_url, '_blank');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!quizData) {
    return <div>Quiz not found</div>;
  }

  return (
    <div className="pdf-quiz-container">
      <div className="quiz-header">
        <button onClick={onBack} className="back-button">
          <ArrowLeft size={18} />
          Back to Quizzes
        </button>
        
        <div className="quiz-info">
          <h2>{quizData.name}</h2>
          <p>{quizData.lesson} - {quizData.class}</p>
        </div>
      </div>

      <div className="pdf-quiz-content">
        <div className="quiz-description">
          <h3>PDF Quiz Instructions</h3>
          <ul>
            {quizData.instructions.map((instruction, index) => (
              <li key={index}>{instruction}</li>
            ))}
          </ul>
        </div>

        <div className="download-section">
          <div className="download-card">
            <FileText size={48} className="pdf-icon" />
            <h4>{quizData.file}</h4>
            <p>Click the button below to download the PDF quiz</p>
            <button onClick={handleDownload} className="download-button">
              <Download size={18} />
              Download PDF Quiz
            </button>
          </div>
        </div>

        <div className="quiz-actions">
          <button onClick={handleDownload} className="btn-primary">
            Download & Start Quiz
          </button>
          <button onClick={onBack} className="btn-secondary">
            Back to Quiz List
          </button>
        </div>
      </div>
    </div>
  );
};

export default PDFQuizComponent;
```

### Option 3: Modify Existing Quiz Flow

Update your existing `handleSubjectSelect` function to handle PDF quizzes:

```jsx
const handleSubjectSelect = (subject) => {
  if (subject.type === 'pdf_quiz') {
    // Handle PDF quiz differently
    setSelectedSubject(subject);
    setShowPDFQuiz(true);
    return;
  }
  
  // Handle regular quizzes as before
  setSelectedSubject(subject);
  setCurrentQuestion(0);
  // ... rest of your existing logic
};

// Add state for PDF quiz
const [showPDFQuiz, setShowPDFQuiz] = useState(false);

// In your render method, add conditional rendering
if (showPDFQuiz && selectedSubject) {
  return (
    <PDFQuizComponent
      class_name={selectedSubject.class_key}
      subject={selectedSubject.subject}
      topic={selectedSubject.topic}
      onBack={() => {
        setShowPDFQuiz(false);
        setSelectedSubject(null);
      }}
    />
  );
}
```

## CSS Styling

Add these styles to your `Test.css`:

```css
.pdf-quiz-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.pdf-quiz-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.quiz-description {
  margin-bottom: 30px;
}

.quiz-description h3 {
  color: #333;
  margin-bottom: 15px;
}

.quiz-description ul {
  list-style-type: disc;
  padding-left: 20px;
}

.quiz-description li {
  margin-bottom: 8px;
  color: #666;
}

.download-section {
  margin-bottom: 30px;
}

.download-card {
  text-align: center;
  padding: 40px;
  border: 2px dashed #ddd;
  border-radius: 12px;
  background: #f9f9f9;
}

.pdf-icon {
  color: #e74c3c;
  margin-bottom: 15px;
}

.download-card h4 {
  color: #333;
  margin-bottom: 10px;
}

.download-card p {
  color: #666;
  margin-bottom: 20px;
}

.download-button {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.download-button:hover {
  background: #c0392b;
}

.quiz-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background: #7f8c8d;
}
```

## Features

### ✅ Complete PDF Organization
- Organized by class/subject/topic/chapter
- Automatic file availability checking
- File size information
- Download URLs

### ✅ Frontend Integration
- Seamless integration with existing quiz system
- Consistent UI/UX
- Download functionality
- Search capabilities

### ✅ Interactive Experience
- PDF download and viewing
- Clear instructions for students
- Progress tracking
- Results submission

### ✅ No Database Required
- Uses existing PDF files
- No additional storage needed
- Fast response times
- Easy to maintain

## Usage Examples

### Get All PDF Quizzes for Class 7
```javascript
const response = await fetch('/api/quizzes/pdf/class7/subjects/');
const data = await response.json();
console.log(data.subjects); // All subjects for Class 7
```

### Download a Specific PDF
```javascript
const downloadUrl = '/api/quizzes/pdf/class7/maths/chapter1/download/';
window.open(downloadUrl, '_blank');
```

### Search for PDF Quizzes
```javascript
const response = await fetch('/api/quizzes/pdf/search/?q=chapter&class=class7');
const data = await response.json();
console.log(data.results); // Search results
```

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Error Handling
The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found (PDF file doesn't exist)
- `500`: Internal Server Error

## Extending the System
To add more PDFs:
1. Add the PDF file to the appropriate folder structure
2. Update the `PDF_STRUCTURE` in `pdf_quiz_views.py`
3. Restart the Django server
4. The new PDFs will be immediately available

The system is designed to be easily extensible for additional classes, subjects, and topics.
