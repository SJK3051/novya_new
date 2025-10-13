-- Create quiz tables according to the provided schema

-- 1. Quiz Master Table
CREATE TABLE IF NOT EXISTS quiz (
    quiz_id SERIAL PRIMARY KEY,
    topic_id INT,
    title VARCHAR(150) NOT NULL,
    total_marks INT,
    duration INT,                       -- in minutes
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);

-- 2. Quiz Question Table
CREATE TABLE IF NOT EXISTS quiz_question (
    question_id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('A','B','C','D')),
    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);

-- 3. Quiz Attempt Table
CREATE TABLE IF NOT EXISTS quiz_attempt (
    attempt_id SERIAL PRIMARY KEY,
    quiz_id INT,
    student_id INT NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score DOUBLE PRECISION,
    
    -- Enhanced tracking fields for AI-generated quizzes
    quiz_type VARCHAR(20) DEFAULT 'ai_generated',
    subject VARCHAR(100),
    chapter VARCHAR(100),
    topic VARCHAR(200),
    subtopic VARCHAR(200),
    class_name VARCHAR(50),
    difficulty_level VARCHAR(20) DEFAULT 'simple',
    total_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    wrong_answers INT DEFAULT 0,
    unanswered_questions INT DEFAULT 0,
    time_taken_seconds INT DEFAULT 0,
    completion_percentage DOUBLE PRECISION DEFAULT 0.0,
    language VARCHAR(10) DEFAULT 'English',
    quiz_data_json TEXT,
    answers_json TEXT,
    
    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id),
    FOREIGN KEY (student_id) REFERENCES student_registration(student_id)
);

-- 4. Quiz Answer Table (stores each question's selected option)
CREATE TABLE IF NOT EXISTS quiz_answer (
    answer_id SERIAL PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option CHAR(1) NOT NULL CHECK (selected_option IN ('A','B','C','D')),
    is_correct BOOLEAN,
    FOREIGN KEY (attempt_id) REFERENCES quiz_attempt(attempt_id),
    FOREIGN KEY (question_id) REFERENCES quiz_question(question_id)
);

-- 5. Mock Test Master Table
CREATE TABLE IF NOT EXISTS mock_test (
    test_id SERIAL PRIMARY KEY,
    topic_id INT,
    title VARCHAR(150) NOT NULL,
    total_marks INT,
    duration INT,                       -- in minutes
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);

-- 6. Mock Test Question Table
CREATE TABLE IF NOT EXISTS mock_test_question (
    question_id SERIAL PRIMARY KEY,
    test_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('A','B','C','D')),
    FOREIGN KEY (test_id) REFERENCES mock_test(test_id)
);

-- 7. Mock Test Attempt Table
CREATE TABLE IF NOT EXISTS mock_test_attempt (
    attempt_id SERIAL PRIMARY KEY,
    test_id INT NOT NULL,
    student_id INT NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    score DOUBLE PRECISION,
    FOREIGN KEY (test_id) REFERENCES mock_test(test_id),
    FOREIGN KEY (student_id) REFERENCES student_registration(student_id)
);
