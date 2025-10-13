# Static Quiz System Integration Guide

## Overview
This guide explains how to integrate the static quiz system for 7th class Mathematics and Science subjects into your frontend application.

## Available Subjects and Topics

### Mathematics (7th Class)
1. **Integers** - Understanding positive and negative numbers (5 questions)
2. **Fractions and Decimals** - Understanding fractions, decimals, and their operations (5 questions)
3. **Algebra Basics** - Introduction to variables and simple equations (5 questions)

### Science (7th Class)
1. **Nutrition in Plants and Animals** - Understanding how plants and animals obtain and process food (5 questions)
2. **Respiration in Organisms** - Understanding how different organisms respire (5 questions)
3. **Transportation in Plants and Animals** - Understanding how materials are transported in living organisms (5 questions)

## API Endpoints

### 1. Get All Subjects
```
GET /api/quizzes/static/subjects/
```
**Response:**
```json
{
  "subjects": [
    {
      "subject_key": "mathematics",
      "subject_name": "Mathematics",
      "class": "7th",
      "topics_count": 3
    },
    {
      "subject_key": "science",
      "subject_name": "Science",
      "class": "7th",
      "topics_count": 3
    }
  ],
  "total_subjects": 2
}
```

### 2. Get Topics for a Subject
```
GET /api/quizzes/static/subjects/{subject}/topics/
```
**Example:** `/api/quizzes/static/subjects/mathematics/topics/`

**Response:**
```json
{
  "subject": "mathematics",
  "topics": [
    {
      "topic_key": "integers",
      "topic_name": "Integers",
      "description": "Understanding positive and negative numbers",
      "questions_count": 5
    }
  ],
  "total_topics": 3
}
```

### 3. Get Quiz Questions
```
GET /api/quizzes/static/subjects/{subject}/topics/{topic}/
```
**Example:** `/api/quizzes/static/subjects/mathematics/topics/integers/`

**Response:**
```json
{
  "subject": "mathematics",
  "topic": "integers",
  "topic_name": "Integers",
  "description": "Understanding positive and negative numbers",
  "questions": [
    {
      "question_id": 1,
      "question_text": "What is the sum of -15 and 23?",
      "question_type": "multiple_choice",
      "points": 1,
      "options": [
        {"option_id": "a", "option_text": "8"},
        {"option_id": "b", "option_text": "-8"},
        {"option_id": "c", "option_text": "38"},
        {"option_id": "d", "option_text": "-38"}
      ]
    }
  ],
  "total_questions": 5,
  "total_points": 6
}
```

### 4. Submit Quiz Answers
```
POST /api/quizzes/static/subjects/{subject}/topics/{topic}/submit/
```
**Request Body:**
```json
{
  "answers": [
    {"question_id": 1, "selected_option": "a"},
    {"question_id": 2, "selected_option": "b"},
    {"question_id": 3, "selected_option": "b"},
    {"question_id": 4, "selected_option": "a"},
    {"question_id": 5, "selected_option": "b"}
  ],
  "submitted_at": "2025-09-18T08:00:00Z"
}
```

**Response:**
```json
{
  "subject": "mathematics",
  "topic": "integers",
  "user_id": 75,
  "username": "srinivas123",
  "score_info": {
    "total_questions": 5,
    "correct_answers": 5,
    "wrong_answers": 0,
    "total_score": 6,
    "percentage": 100.0,
    "is_passed": true
  },
  "detailed_results": [
    {
      "question_id": 1,
      "question_text": "What is the sum of -15 and 23?",
      "selected_option": "a",
      "correct_option": "a",
      "is_correct": true,
      "points_earned": 1,
      "explanation": "To add -15 and 23: -15 + 23 = 8"
    }
  ],
  "submitted_at": "2025-09-18T08:00:00Z"
}
```

### 5. Get Quiz Statistics
```
GET /api/quizzes/static/statistics/
```
**Response:**
```json
{
  "total_subjects": 2,
  "total_topics": 6,
  "total_questions": 30,
  "subjects": [
    {
      "subject_key": "mathematics",
      "subject_name": "Mathematics",
      "class": "7th",
      "topics_count": 3,
      "questions_count": 15,
      "topics": [
        {
          "topic_key": "integers",
          "topic_name": "Integers",
          "questions_count": 5
        }
      ]
    }
  ]
}
```

## Frontend Integration Example

### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

const QuizComponent = ({ subject, topic }) => {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch quiz questions
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await fetch(
          `/api/quizzes/static/subjects/${subject}/topics/${topic}/`,
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
              'Content-Type': 'application/json'
            }
          }
        );
        const data = await response.json();
        setQuestions(data.questions);
      } catch (error) {
        console.error('Error fetching quiz:', error);
      }
    };

    fetchQuiz();
  }, [subject, topic]);

  // Handle answer selection
  const handleAnswerSelect = (questionId, optionId) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  // Submit quiz
  const submitQuiz = async () => {
    setLoading(true);
    try {
      const answersArray = Object.entries(answers).map(([questionId, optionId]) => ({
        question_id: parseInt(questionId),
        selected_option: optionId
      }));

      const response = await fetch(
        `/api/quizzes/static/subjects/${subject}/topics/${topic}/submit/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            answers: answersArray,
            submitted_at: new Date().toISOString()
          })
        }
      );

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error submitting quiz:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="quiz-container">
      {!results ? (
        <div>
          <h2>Quiz: {questions.length > 0 ? questions[0].topic_name : 'Loading...'}</h2>
          {questions.map((question) => (
            <div key={question.question_id} className="question">
              <h3>Q{question.question_id}: {question.question_text}</h3>
              <div className="options">
                {question.options.map((option) => (
                  <label key={option.option_id}>
                    <input
                      type="radio"
                      name={`question_${question.question_id}`}
                      value={option.option_id}
                      checked={answers[question.question_id] === option.option_id}
                      onChange={() => handleAnswerSelect(question.question_id, option.option_id)}
                    />
                    {option.option_id}. {option.option_text}
                  </label>
                ))}
              </div>
            </div>
          ))}
          <button onClick={submitQuiz} disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Quiz'}
          </button>
        </div>
      ) : (
        <div className="results">
          <h2>Quiz Results</h2>
          <div className="score-summary">
            <p>Score: {results.score_info.percentage}%</p>
            <p>Correct: {results.score_info.correct_answers}/{results.score_info.total_questions}</p>
            <p>Status: {results.score_info.is_passed ? 'Passed' : 'Failed'}</p>
          </div>
          <div className="detailed-results">
            {results.detailed_results.map((result) => (
              <div key={result.question_id} className={`result-item ${result.is_correct ? 'correct' : 'incorrect'}`}>
                <h4>Q{result.question_id}: {result.question_text}</h4>
                <p>Your Answer: {result.selected_option}</p>
                <p>Correct Answer: {result.correct_option}</p>
                <p>Explanation: {result.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizComponent;
```

## Features

### ✅ Interactive User Experience
- Multiple choice questions with radio button selection
- Real-time answer tracking
- Immediate feedback after submission
- Detailed explanations for each answer

### ✅ Comprehensive Scoring
- Points-based scoring system
- Percentage calculation
- Pass/Fail determination (60% passing criteria)
- Detailed result breakdown

### ✅ Educational Content
- 30 carefully crafted questions across 6 topics
- Covers essential 7th class curriculum
- Includes explanations for better understanding
- Progressive difficulty levels

### ✅ No Database Required
- All quiz data is stored in static Python files
- Easy to modify and extend
- No database migrations needed
- Fast response times

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Error Handling
The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid data)
- `401`: Unauthorized (missing/invalid token)
- `404`: Not Found (subject/topic doesn't exist)
- `500`: Internal Server Error

## Extending the System
To add more questions or topics:

1. Edit `quizzes/static_quiz_data.py`
2. Add new questions to existing topics or create new topics
3. Follow the existing question format
4. Restart the Django server

The system is designed to be easily extensible for additional subjects, classes, and topics.
