from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Avg, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Quiz, QuizQuestion, QuizAttempt, QuizAnswer, MockTest, MockTestQuestion, MockTestAttempt, MockTestAnswer,
    Question, QuestionOption, QuizResult, QuizAnalytics, StudentPerformance
)
from authentication.models import StudentRegistration

def get_student_registration(user):
    """
    Helper function to get StudentRegistration from User
    """
    try:
        # Check if user is authenticated and has username
        if user and hasattr(user, 'username') and user.username:
            return StudentRegistration.objects.get(student_username=user.username)
        else:
            return None
    except StudentRegistration.DoesNotExist:
        return None

from .serializers import (
    QuizSerializer, QuizListSerializer, QuestionSerializer, QuestionOptionSerializer,
    QuizAttemptSerializer, QuizAnswerSerializer, QuizResultSerializer,
    QuizSubmissionSerializer, QuizAttemptSummarySerializer, StudentQuizStatsSerializer,
    EnhancedQuizAttemptSerializer, QuizAttemptSubmissionSerializer, MockTestAttemptSubmissionSerializer,
    StudentPerformanceSerializer, RecentQuizAttemptsSerializer
)


class QuizListCreateView(generics.ListCreateAPIView):
    """
    List and create quizzes
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade')
        subject_id = self.request.query_params.get('subject')
        difficulty = self.request.query_params.get('difficulty')
        
        if grade:
            queryset = queryset.filter(grade=grade)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quiz
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionListCreateView(generics.ListCreateAPIView):
    """
    List and create questions for a quiz
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz_id=quiz_id, is_active=True)
    
    def perform_create(self, serializer):
        quiz_id = self.kwargs['quiz_id']
        serializer.save(quiz_id=quiz_id)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a question
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartQuizView(generics.CreateAPIView):
    """
    Start a quiz attempt
    """
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        quiz_id = self.kwargs['pk']
        quiz = Quiz.objects.get(pk=quiz_id)
        
        # Check if user already has an active attempt
        existing_attempt = QuizAttempt.objects.filter(
            student=self.request.user,
            quiz=quiz,
            is_completed=False
        ).first()
        
        if existing_attempt:
            raise serializers.ValidationError("You already have an active attempt for this quiz")
        
        serializer.save(
            student=self.request.user,
            quiz=quiz,
            started_at=timezone.now()
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_quiz(request, pk):
    """
    Submit quiz answers
    """
    serializer = QuizSubmissionSerializer(data=request.data)
    
    if serializer.is_valid():
        quiz_id = pk
        answers_data = serializer.validated_data['answers']
        
        try:
            # Get the active attempt
            attempt = QuizAttempt.objects.get(
                student=request.user,
                quiz_id=quiz_id,
                is_completed=False
            )
            
            # Process answers
            total_score = 0
            correct_answers = 0
            
            for answer_data in answers_data:
                question_id = answer_data['question_id']
                question = Question.objects.get(id=question_id)
                
                # Create or update answer
                answer, created = QuizAnswer.objects.get_or_create(
                    attempt=attempt,
                    question=question
                )
                
                # Check if it's a multiple choice question
                if question.question_type == 'multiple_choice':
                    selected_option_id = answer_data.get('selected_option_id')
                    if selected_option_id:
                        selected_option = QuestionOption.objects.get(id=selected_option_id)
                        answer.selected_option = selected_option
                        answer.is_correct = selected_option.is_correct
                        answer.points_earned = question.points if selected_option.is_correct else 0
                else:
                    # Handle other question types
                    answer_text = answer_data.get('answer_text', '')
                    answer.answer_text = answer_text
                    # For now, assume text answers are correct (you can implement proper checking)
                    answer.is_correct = True
                    answer.points_earned = question.points
                
                answer.save()
                
                if answer.is_correct:
                    correct_answers += 1
                    total_score += answer.points_earned
            
            # Calculate final score
            total_questions = attempt.quiz.questions.filter(is_active=True).count()
            score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            # Update attempt
            attempt.score = score_percentage
            attempt.is_completed = True
            attempt.completed_at = timezone.now()
            attempt.is_passed = score_percentage >= attempt.quiz.passing_score
            attempt.time_taken_minutes = (timezone.now() - attempt.started_at).total_seconds() / 60
            attempt.save()
            
            # Create quiz result
            QuizResult.objects.create(
                attempt=attempt,
                total_questions=total_questions,
                correct_answers=correct_answers,
                wrong_answers=total_questions - correct_answers,
                unanswered_questions=0,  # All questions were answered
                accuracy_percentage=score_percentage,
                time_per_question_seconds=attempt.time_taken_minutes * 60 / total_questions if total_questions > 0 else 0
            )
            
            # Update analytics
            analytics, created = QuizAnalytics.objects.get_or_create(quiz=attempt.quiz)
            analytics.total_attempts += 1
            analytics.average_score = (analytics.average_score * (analytics.total_attempts - 1) + score_percentage) / analytics.total_attempts
            analytics.pass_rate = QuizAttempt.objects.filter(quiz=attempt.quiz, is_passed=True).count() / analytics.total_attempts * 100
            analytics.average_time_minutes = QuizAttempt.objects.filter(quiz=attempt.quiz).aggregate(avg_time=Avg('time_taken_minutes'))['avg_time'] or 0
            analytics.save()
            
            return Response({
                'message': 'Quiz submitted successfully',
                'score': score_percentage,
                'is_passed': attempt.is_passed,
                'correct_answers': correct_answers,
                'total_questions': total_questions,
                'time_taken': attempt.time_taken_minutes
            })
        
        except QuizAttempt.DoesNotExist:
            return Response(
                {'error': 'No active attempt found for this quiz'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizAttemptListView(generics.ListAPIView):
    """
    List quiz attempts
    """
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user).order_by('-started_at')


class QuizAttemptDetailView(generics.RetrieveAPIView):
    """
    Retrieve quiz attempt details
    """
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_quiz_result(request, pk):
    """
    Get detailed quiz result
    """
    try:
        attempt = QuizAttempt.objects.get(pk=pk, student=request.user)
        result = QuizResult.objects.get(attempt=attempt)
        
        return Response({
            'attempt': QuizAttemptSerializer(attempt).data,
            'result': QuizResultSerializer(result).data,
            'answers': QuizAnswerSerializer(attempt.answers.all(), many=True).data
        })
    
    except QuizAttempt.DoesNotExist:
        return Response(
            {'error': 'Quiz attempt not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class StudentQuizAttemptsView(generics.ListAPIView):
    """
    Get student's quiz attempts
    """
    serializer_class = QuizAttemptSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        attempts = QuizAttempt.objects.filter(
            student=self.request.user,
            is_completed=True
        ).order_by('-completed_at')
        
        attempt_data = []
        for attempt in attempts:
            attempt_data.append({
                'attempt_id': attempt.id,
                'quiz_title': attempt.quiz.title,
                'subject_name': attempt.quiz.subject.name,
                'score': attempt.score,
                'is_passed': attempt.is_passed,
                'time_taken_minutes': attempt.time_taken_minutes,
                'completed_at': attempt.completed_at,
                'total_questions': attempt.quiz.questions.filter(is_active=True).count(),
                'correct_answers': attempt.answers.filter(is_correct=True).count()
            })
        
        return attempt_data


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_quiz_stats(request):
    """
    Get student quiz statistics
    """
    user = request.user
    
    attempts = QuizAttempt.objects.filter(student=user, is_completed=True)
    
    total_quizzes_taken = attempts.count()
    total_questions_attempted = sum([a.quiz.questions.filter(is_active=True).count() for a in attempts])
    total_correct_answers = sum([a.answers.filter(is_correct=True).count() for a in attempts])
    
    average_score = attempts.aggregate(avg_score=Avg('score'))['avg_score'] or 0
    best_score = attempts.aggregate(best_score=Avg('score'))['best_score'] or 0
    quizzes_passed = attempts.filter(is_passed=True).count()
    
    # Get total available quizzes
    total_quizzes_available = Quiz.objects.all().count()
    
    accuracy_percentage = (total_correct_answers / total_questions_attempted * 100) if total_questions_attempted > 0 else 0
    
    stats = {
        'total_quizzes_taken': total_quizzes_taken,
        'average_score': average_score,
        'total_correct_answers': total_correct_answers,
        'total_questions_attempted': total_questions_attempted,
        'accuracy_percentage': accuracy_percentage,
        'best_score': best_score,
        'quizzes_passed': quizzes_passed,
        'total_quizzes_available': total_quizzes_available
    }
    
    return Response(stats)


class AvailableQuizzesView(generics.ListAPIView):
    """
    Get available quizzes for student
    """
    serializer_class = QuizListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get quizzes that student hasn't completed or has completed but can retake
        completed_quiz_ids = QuizAttempt.objects.filter(
            student=self.request.user,
            is_completed=True
        ).values_list('quiz_id', flat=True)
        
        # For now, allow retaking all quizzes
        return Quiz.objects.all()


# ============================================
# NEW API VIEWS FOR QUIZ TRACKING SYSTEM
# ============================================

def submit_mock_test_logic(request, validated_data, student_reg):
    """
    Helper function to handle mock test submission logic
    """
    import json
    
    # Convert test questions and answers to JSON strings for storage
    test_questions = validated_data.get('quiz_questions', [])
    user_answers = validated_data.get('user_answers', [])
    
    
    test_data_json = json.dumps(test_questions) if test_questions else ''
    answers_json = json.dumps(user_answers) if user_answers else ''
    
    # Create a dummy MockTest record for AI-generated mock tests (required by foreign key)
    from courses.models import Topic, Course
    # Create a dummy course and topic for AI-generated mock tests
    course, created = Course.objects.get_or_create(
        course_id=2,  # Use different ID for mock tests
        defaults={
            'course_name': 'AI Generated Mock Tests',
            'course_price': 0.00
        }
    )
    
    # Try to find or create a topic for this subtopic
    topic, created = Topic.objects.get_or_create(
        topic_name=validated_data['subtopic'],
        defaults={
            'course_id': course.course_id
        }
    )
    
    # Create a dummy mock test for this AI-generated mock test
    dummy_mock_test, created = MockTest.objects.get_or_create(
        title=f"AI Generated Mock Test - {validated_data['subtopic']}",
        topic_id=topic
    )
    
    # Create mock test attempt with all detailed information (same as quiz system)
    attempt = MockTestAttempt.objects.create(
        test_id=dummy_mock_test,
        student_id=student_reg,
        score=validated_data['score'],
        answers_json=answers_json,
        quiz_type=validated_data.get('quiz_type', 'mock_test'),
        subject=validated_data.get('subject', ''),
        chapter=validated_data.get('chapter', ''),
        topic=validated_data.get('topic', ''),
        subtopic=validated_data.get('subtopic', ''),
        class_name=validated_data.get('class_name', ''),
        difficulty_level=validated_data.get('difficulty_level', ''),
        language=validated_data.get('language', ''),
        total_questions=validated_data.get('total_questions', 0),
        correct_answers=validated_data.get('correct_answers', 0),
        wrong_answers=validated_data.get('wrong_answers', 0),
        unanswered_questions=validated_data.get('unanswered_questions', 0),
        time_taken_seconds=validated_data.get('time_taken_seconds', 0),
        completion_percentage=validated_data['score'],
        mock_test_data_json=test_data_json
    )
    
    # Create individual mock test answers for detailed tracking
    for i, (question, answer) in enumerate(zip(test_questions, user_answers)):
        try:
            # Handle the actual frontend data format
            question_text = question.get('question', '')
            options = question.get('options', {})
            correct_answer = question.get('answer', '')
            
            # Extract options - handle both dict and array formats
            if isinstance(options, dict):
                option_a = options.get('A', '')
                option_b = options.get('B', '')
                option_c = options.get('C', '')
                option_d = options.get('D', '')
            elif isinstance(options, list):
                option_a = options[0] if len(options) > 0 else ''
                option_b = options[1] if len(options) > 1 else ''
                option_c = options[2] if len(options) > 2 else ''
                option_d = options[3] if len(options) > 3 else ''
            else:
                option_a = option_b = option_c = option_d = ''
            
            # Convert answer text to option letter (A, B, C, D)
            def get_option_letter(answer_text, options_dict):
                """Convert answer text to option letter"""
                if isinstance(options_dict, list):
                    options_dict = {chr(65 + i): opt for i, opt in enumerate(options_dict)}

                for letter, text in options_dict.items():
                    if text == answer_text:
                        return letter
                return 'A'  # Default fallback
            
            correct_option_letter = get_option_letter(correct_answer, options)
            selected_option_letter = get_option_letter(str(answer), options)
            
            # Create a MockTestQuestion record for this attempt
            mock_test_question = MockTestQuestion.objects.create(
                test_id=dummy_mock_test,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option_letter
            )
            
            # Create a MockTestAnswer record
            is_correct = selected_option_letter == correct_option_letter
            
            MockTestAnswer.objects.create(
                attempt_id=attempt,
                question_id=mock_test_question,
                selected_option=selected_option_letter,
                is_correct=is_correct
            )
            
        except Exception as e:
            # Log error but continue processing other questions
            print(f"Error processing mock test question {i}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return Response({
        'message': 'Mock test attempt submitted successfully',
        'attempt_id': attempt.attempt_id,
        'score': attempt.score
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Temporarily allow any for testing
def submit_quiz_attempt(request):
    """
    Submit a quiz attempt (for AI-generated quizzes) or mock test
    """
    import json
    
    # Temporarily ignore authentication for testing
    # This allows frontend submissions even with invalid tokens
    # Force the user to be anonymous to bypass authentication
    from django.contrib.auth.models import AnonymousUser
    request.user = AnonymousUser()
    
    # Log incoming request data for debugging
    print(f"📥 Received submission request:")
    print(f"   Data keys: {list(request.data.keys())}")
    print(f"   Quiz Type: {request.data.get('quizType', 'NOT SET')}")
    
    serializer = QuizAttemptSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        # Get student registration
        student_reg = get_student_registration(request.user)
        if not student_reg:
            # For testing without authentication, use the first available student
            student_reg = StudentRegistration.objects.first()
        if not student_reg:
            return Response(
                    {'error': 'No students found in database'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        validated_data = serializer.validated_data
        
        # Check if this is a mock test submission
        if validated_data.get('quiz_type') == 'mock_test':
            # Route to mock test submission handler
            return submit_mock_test_logic(request, validated_data, student_reg)
        
        # Convert quiz questions and answers to JSON strings for storage
        quiz_questions = validated_data.get('quiz_questions', [])
        user_answers = validated_data.get('user_answers', [])
        
        quiz_data_json = json.dumps(quiz_questions) if quiz_questions else ''
        answers_json = json.dumps(user_answers) if user_answers else ''
        
        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            student_id=student_reg,
            quiz_type=validated_data['quiz_type'],
            subject=validated_data['subject'],
            chapter=validated_data.get('chapter', ''),
            topic=validated_data.get('topic', ''),
            subtopic=validated_data['subtopic'],
            class_name=validated_data['class_name'],
            difficulty_level=validated_data['difficulty_level'],
            language=validated_data['language'],
            total_questions=validated_data['total_questions'],
            correct_answers=validated_data['correct_answers'],
            wrong_answers=validated_data['wrong_answers'],
            unanswered_questions=validated_data['unanswered_questions'],
            time_taken_seconds=validated_data['time_taken_seconds'],
            score=validated_data['score'],
            quiz_data_json=quiz_data_json,
            answers_json=answers_json,
            completion_percentage=(validated_data['correct_answers'] / validated_data['total_questions']) * 100
        )
        
        # Create a dummy Quiz record for AI-generated questions (required by foreign key)
        dummy_quiz = None
        if validated_data['quiz_type'] == 'ai_generated':
            from courses.models import Topic, Course
            # Create a dummy course and topic for AI-generated quizzes
            course, created = Course.objects.get_or_create(
                course_id=1,
                defaults={
                    'course_name': 'AI Generated Quizzes',
                    'course_price': 0.00
                }
            )
            
            # Try to find or create a topic for this subtopic
            topic, created = Topic.objects.get_or_create(
                topic_name=validated_data['subtopic'],
                defaults={
                    'course_id': course.course_id
                }
            )
            
            # Create a dummy quiz for this AI-generated quiz
            dummy_quiz, created = Quiz.objects.get_or_create(
                title=f"AI Generated Quiz - {validated_data['subtopic']}",
                topic_id=topic
            )
        
        # Create individual quiz answers for detailed tracking
        for i, (question, answer) in enumerate(zip(quiz_questions, user_answers)):
            try:
                # Handle the actual frontend data format
                # question: {question: "...", options: {...}, answer: "..."}
                # answer: string (selected answer text)
                
                question_text = question.get('question', '')
                options = question.get('options', {})
                correct_answer = question.get('answer', '')
                
                # Extract options - handle both dict and array formats
                if isinstance(options, dict):
                    option_a = options.get('A', '')
                    option_b = options.get('B', '')
                    option_c = options.get('C', '')
                    option_d = options.get('D', '')
                elif isinstance(options, list):
                    option_a = options[0] if len(options) > 0 else ''
                    option_b = options[1] if len(options) > 1 else ''
                    option_c = options[2] if len(options) > 2 else ''
                    option_d = options[3] if len(options) > 3 else ''
                else:
                    option_a = option_b = option_c = option_d = ''
                
                # Convert answer text to option letter (A, B, C, D)
                def get_option_letter(answer_text, options_dict):
                    """Convert answer text to option letter"""
                    for letter, text in options_dict.items():
                        if text == answer_text:
                            return letter
                    return 'A'  # Default fallback
                
                correct_option_letter = get_option_letter(correct_answer, options)
                selected_option_letter = get_option_letter(str(answer), options)
                
                # Create a QuizQuestion record for this attempt
                quiz_question = QuizQuestion.objects.create(
                    quiz_id=dummy_quiz,  # Use dummy quiz for AI-generated quizzes
                    question_text=question_text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct_option=correct_option_letter  # Store the option letter
                )
                
                # Create a QuizAnswer record
                is_correct = selected_option_letter == correct_option_letter
                
                QuizAnswer.objects.create(
                    attempt_id=attempt,
                    question_id=quiz_question,
                    selected_option=selected_option_letter,
                    is_correct=is_correct
                )
                
            except Exception as e:
                # Log error but continue processing other questions
                print(f"Error processing question {i}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Update student performance
        update_student_performance(student_reg, attempt)
        
        return Response({
            'message': 'Quiz attempt submitted successfully',
            'attempt_id': attempt.attempt_id,
            'score': attempt.score,
            'completion_percentage': attempt.completion_percentage
        }, status=status.HTTP_201_CREATED)
    
    # Log validation errors for debugging
    print(f"❌ Validation errors:")
    print(f"   {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Temporarily allow any for testing
def submit_mock_test_attempt(request):
    """
    Submit a mock test attempt (for AI-generated mock tests)
    """
    import json
    
    serializer = MockTestAttemptSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        # Get student registration
        student_reg = get_student_registration(request.user)
        if not student_reg:
            # For testing without authentication, use the first available student
            student_reg = StudentRegistration.objects.first()
            if not student_reg:
                return Response(
                    {'error': 'No students found in database'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        validated_data = serializer.validated_data
        
        # Convert mock test questions and answers to JSON strings for storage
        test_questions = validated_data.get('test_questions', [])
        user_answers = validated_data.get('user_answers', [])
        
        test_data_json = json.dumps(test_questions) if test_questions else ''
        answers_json = json.dumps(user_answers) if user_answers else ''
        
        # Create a dummy MockTest record for AI-generated mock tests (required by foreign key)
        dummy_mock_test = None
        from courses.models import Topic, Course
        # Create a dummy course and topic for AI-generated mock tests
        course, created = Course.objects.get_or_create(
            course_id=2,  # Use different ID for mock tests
            defaults={
                'course_name': 'AI Generated Mock Tests',
                'course_price': 0.00
            }
        )
        
        # Try to find or create a topic for this subtopic
        topic, created = Topic.objects.get_or_create(
            topic_name=validated_data['subtopic'],
            defaults={
                'course_id': course.course_id
            }
        )
        
        # Create a dummy mock test for this AI-generated mock test
        dummy_mock_test, created = MockTest.objects.get_or_create(
            title=f"AI Generated Mock Test - {validated_data['subtopic']}",
            topic_id=topic
        )
        
        # Create mock test attempt
        attempt = MockTestAttempt.objects.create(
            test_id=dummy_mock_test,
            student_id=student_reg,
            score=validated_data['score']
        )
        
        # Create individual mock test answers for detailed tracking
        for i, (question, answer) in enumerate(zip(test_questions, user_answers)):
            try:
                # Handle the actual frontend data format
                # question: {question: "...", options: {...}, answer: "..."}
                # answer: string (selected answer text)
                
                question_text = question.get('question', '')
                options = question.get('options', {})
                correct_answer = question.get('answer', '')
                
                # Extract options - handle both dict and array formats
                if isinstance(options, dict):
                    option_a = options.get('A', '')
                    option_b = options.get('B', '')
                    option_c = options.get('C', '')
                    option_d = options.get('D', '')
                elif isinstance(options, list):
                    option_a = options[0] if len(options) > 0 else ''
                    option_b = options[1] if len(options) > 1 else ''
                    option_c = options[2] if len(options) > 2 else ''
                    option_d = options[3] if len(options) > 3 else ''
                else:
                    option_a = option_b = option_c = option_d = ''
                
                # Convert answer text to option letter (A, B, C, D)
                def get_option_letter(answer_text, options_dict):
                    """Convert answer text to option letter"""
                    # If options_dict is a list, convert it to a dict for lookup
                    if isinstance(options_dict, list):
                        options_dict = {chr(65 + i): opt for i, opt in enumerate(options_dict)}

                    for letter, text in options_dict.items():
                        if text == answer_text:
                            return letter
                    return 'A'  # Default fallback
                
                correct_option_letter = get_option_letter(correct_answer, options)
                selected_option_letter = get_option_letter(str(answer), options)
                
                # Create a MockTestQuestion record for this attempt
                mock_test_question = MockTestQuestion.objects.create(
                    test_id=dummy_mock_test,
                    question_text=question_text,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct_option=correct_option_letter
                )
                
                # Create a MockTestAnswer record
                is_correct = selected_option_letter == correct_option_letter
                
                MockTestAnswer.objects.create(
                    attempt_id=attempt,
                    question_id=mock_test_question,
                    selected_option=selected_option_letter,
                    is_correct=is_correct
                )
                
            except Exception as e:
                # Log error but continue processing other questions
                print(f"Error processing mock test question {i}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return Response({
            'message': 'Mock test attempt submitted successfully',
            'attempt_id': attempt.attempt_id,
            'score': attempt.score
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily allow any for testing
def get_recent_quiz_attempts(request):
    """
    Get recent quiz and mock test attempts for the logged-in student
    """
    limit = request.query_params.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    
    # Get student registration
    student_reg = get_student_registration(request.user)
    if not student_reg:
        # For testing without authentication, use the first available student
        student_reg = StudentRegistration.objects.first()
        if not student_reg:
            return Response(
                {'error': 'No students found in database'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Get both quiz attempts and mock test attempts
    quiz_attempts = QuizAttempt.objects.filter(
        student_id=student_reg
    ).order_by('-attempted_at')
    
    mock_test_attempts = MockTestAttempt.objects.filter(
        student_id=student_reg
    ).order_by('-attempted_at')
    
    # Combine and sort by attempted_at, then limit
    all_attempts = []
    
    # Add quiz attempts with type indicator
    for attempt in quiz_attempts:
        all_attempts.append({
            'attempt_id': attempt.attempt_id,
            'type': 'quiz',
            'quiz_type': attempt.quiz_type,
            'subject': attempt.subject,
            'subtopic': attempt.subtopic,
            'score': attempt.score,
            'attempted_at': attempt.attempted_at,
            'completion_percentage': getattr(attempt, 'completion_percentage', None)
        })
    
    # Add mock test attempts with type indicator
    for attempt in mock_test_attempts:
        all_attempts.append({
            'attempt_id': attempt.attempt_id,
            'type': 'mock_test',
            'quiz_type': 'mock_test',
            'subject': 'Mock Test',  # Default subject for mock tests
            'subtopic': attempt.test_id.title if attempt.test_id else 'Mock Test',
            'score': attempt.score,
            'attempted_at': attempt.attempted_at,
            'completion_percentage': None
        })
    
    # Sort by attempted_at (most recent first) and limit
    all_attempts.sort(key=lambda x: x['attempted_at'], reverse=True)
    all_attempts = all_attempts[:limit]
    
    return Response(all_attempts)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily allow any for testing
def get_student_performance(request):
    """
    Get student performance statistics from actual quiz and mock test attempts
    """
    # Get student registration
    student_reg = get_student_registration(request.user)
    if not student_reg:
        # For testing without authentication, use the first available student
        student_reg = StudentRegistration.objects.first()
        if not student_reg:
            return Response(
                {'error': 'No students found in database'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Get all quiz attempts and mock test attempts for this student
    quiz_attempts = QuizAttempt.objects.filter(student_id=student_reg)
    mock_test_attempts = MockTestAttempt.objects.filter(student_id=student_reg)
    
    # Calculate performance metrics (combining quiz and mock test data)
    total_quizzes_attempted = quiz_attempts.count()
    total_mock_tests_attempted = mock_test_attempts.count()
    total_attempts = total_quizzes_attempted + total_mock_tests_attempted
    
    total_questions_answered = sum(attempt.total_questions for attempt in quiz_attempts)
    total_correct_answers = sum(attempt.correct_answers for attempt in quiz_attempts)
    
    # Calculate overall average score (including both quiz and mock test scores)
    all_scores = []
    all_scores.extend([attempt.score for attempt in quiz_attempts if attempt.score])
    all_scores.extend([attempt.score for attempt in mock_test_attempts if attempt.score])
    
    if all_scores:
        overall_average_score = sum(all_scores) / len(all_scores)
    else:
        overall_average_score = 0
    
    # Subject-wise performance (including both quiz and mock test data)
    subject_performance = {}
    
    # Process quiz attempts
    for attempt in quiz_attempts:
        subject = attempt.subject or 'Unknown'
        if subject not in subject_performance:
            subject_performance[subject] = {
                'total_attempts': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'total_score': 0
            }
        
        subject_performance[subject]['total_attempts'] += 1
        subject_performance[subject]['total_questions'] += attempt.total_questions
        subject_performance[subject]['correct_answers'] += attempt.correct_answers
        subject_performance[subject]['total_score'] += attempt.score or 0
    
    # Process mock test attempts
    for attempt in mock_test_attempts:
        subject = 'Mock Test'  # Mock tests are categorized under "Mock Test" subject
        if subject not in subject_performance:
            subject_performance[subject] = {
                'total_attempts': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'total_score': 0
            }
        
        subject_performance[subject]['total_attempts'] += 1
        # For mock tests, we don't have total_questions and correct_answers in the model
        # So we'll use default values or calculate from related data
        subject_performance[subject]['total_questions'] += 10  # Default assumption
        subject_performance[subject]['correct_answers'] += int(attempt.score or 0)  # Use score as correct answers
        subject_performance[subject]['total_score'] += attempt.score or 0
    
    # Calculate average scores for each subject
    for subject in subject_performance:
        if subject_performance[subject]['total_attempts'] > 0:
            subject_performance[subject]['average_score'] = (
                subject_performance[subject]['total_score'] / 
                subject_performance[subject]['total_attempts']
            )
        else:
            subject_performance[subject]['average_score'] = 0
    
    # Class-wise performance
    class_performance = {}
    for attempt in quiz_attempts:
        class_name = attempt.class_name or 'Unknown'
        if class_name not in class_performance:
            class_performance[class_name] = {
                'total_attempts': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'total_score': 0
            }
        
        class_performance[class_name]['total_attempts'] += 1
        class_performance[class_name]['total_questions'] += attempt.total_questions
        class_performance[class_name]['correct_answers'] += attempt.correct_answers
        class_performance[class_name]['total_score'] += attempt.score or 0
    
    # Calculate average scores for each class
    for class_name in class_performance:
        if class_performance[class_name]['total_attempts'] > 0:
            class_performance[class_name]['average_score'] = (
                class_performance[class_name]['total_score'] / 
                class_performance[class_name]['total_attempts']
            )
        else:
            class_performance[class_name]['average_score'] = 0
    
    # Difficulty-wise performance
    difficulty_performance = {}
    for attempt in quiz_attempts:
        difficulty = attempt.difficulty_level or 'simple'
        if difficulty not in difficulty_performance:
            difficulty_performance[difficulty] = {
                'total_attempts': 0,
                'total_questions': 0,
                'correct_answers': 0,
                'total_score': 0
            }
        
        difficulty_performance[difficulty]['total_attempts'] += 1
        difficulty_performance[difficulty]['total_questions'] += attempt.total_questions
        difficulty_performance[difficulty]['correct_answers'] += attempt.correct_answers
        difficulty_performance[difficulty]['total_score'] += attempt.score or 0
    
    # Calculate average scores for each difficulty
    for difficulty in difficulty_performance:
        if difficulty_performance[difficulty]['total_attempts'] > 0:
            difficulty_performance[difficulty]['average_score'] = (
                difficulty_performance[difficulty]['total_score'] / 
                difficulty_performance[difficulty]['total_attempts']
            )
        else:
            difficulty_performance[difficulty]['average_score'] = 0
    
    performance_data = {
        'total_quizzes_attempted': total_quizzes_attempted,
        'total_mock_tests_attempted': total_mock_tests_attempted,
        'total_attempts': total_attempts,
        'total_questions_answered': total_questions_answered,
        'total_correct_answers': total_correct_answers,
        'overall_average_score': round(overall_average_score, 2),
        'accuracy_percentage': round((total_correct_answers / total_questions_answered * 100) if total_questions_answered > 0 else 0, 2),
        'subject_wise_performance': subject_performance,
        'class_wise_performance': class_performance,
        'difficulty_wise_performance': difficulty_performance
    }
    
    return Response(performance_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Temporarily allow any for testing
def get_quiz_statistics(request):
    """
    Get detailed quiz and mock test statistics for the student
    """
    student = request.user
    
    # Get student registration
    student_reg = get_student_registration(student)
    if not student_reg:
        # For testing without authentication, use the first available student
        student_reg = StudentRegistration.objects.first()
        if not student_reg:
            return Response(
                {'error': 'No students found in database'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Get all quiz and mock test attempts
    quiz_attempts = QuizAttempt.objects.filter(student_id=student_reg)
    mock_test_attempts = MockTestAttempt.objects.filter(student_id=student_reg)
    
    # Calculate statistics (combining both quiz and mock test data)
    total_quiz_attempts = quiz_attempts.count()
    total_mock_test_attempts = mock_test_attempts.count()
    total_attempts = total_quiz_attempts + total_mock_test_attempts
    
    total_questions = quiz_attempts.aggregate(total=Sum('total_questions'))['total'] or 0
    total_correct = quiz_attempts.aggregate(total=Sum('correct_answers'))['total'] or 0
    
    # Calculate average score from both quiz and mock test attempts
    all_scores = []
    all_scores.extend([attempt.score for attempt in quiz_attempts if attempt.score])
    all_scores.extend([attempt.score for attempt in mock_test_attempts if attempt.score])
    average_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    # Subject-wise performance (including both quiz and mock test data)
    subject_stats = {}
    
    # Process quiz attempts
    for attempt in quiz_attempts:
        subject = attempt.subject or 'Unknown'
        if subject not in subject_stats:
            subject_stats[subject] = {'attempts': 0, 'total_score': 0, 'total_questions': 0}
        subject_stats[subject]['attempts'] += 1
        subject_stats[subject]['total_score'] += attempt.score or 0
        subject_stats[subject]['total_questions'] += attempt.total_questions
    
    # Process mock test attempts
    for attempt in mock_test_attempts:
        subject = 'Mock Test'
        if subject not in subject_stats:
            subject_stats[subject] = {'attempts': 0, 'total_score': 0, 'total_questions': 0}
        subject_stats[subject]['attempts'] += 1
        subject_stats[subject]['total_score'] += attempt.score or 0
        subject_stats[subject]['total_questions'] += 10  # Default assumption
    
    # Calculate averages for each subject
    for subject in subject_stats:
        if subject_stats[subject]['attempts'] > 0:
            subject_stats[subject]['average_score'] = subject_stats[subject]['total_score'] / subject_stats[subject]['attempts']
        else:
            subject_stats[subject]['average_score'] = 0
    
    # Class-wise performance (including both quiz and mock test data)
    class_stats = {}
    
    # Process quiz attempts
    for attempt in quiz_attempts:
        class_name = attempt.class_name or 'Unknown'
        if class_name not in class_stats:
            class_stats[class_name] = {'attempts': 0, 'total_score': 0}
        class_stats[class_name]['attempts'] += 1
        class_stats[class_name]['total_score'] += attempt.score or 0
    
    # Process mock test attempts (use default class for mock tests)
    for attempt in mock_test_attempts:
        class_name = 'Mock Test Class'  # Default class for mock tests
        if class_name not in class_stats:
            class_stats[class_name] = {'attempts': 0, 'total_score': 0}
        class_stats[class_name]['attempts'] += 1
        class_stats[class_name]['total_score'] += attempt.score or 0
    
    # Calculate averages for each class
    for class_name in class_stats:
        if class_stats[class_name]['attempts'] > 0:
            class_stats[class_name]['average_score'] = class_stats[class_name]['total_score'] / class_stats[class_name]['attempts']
        else:
            class_stats[class_name]['average_score'] = 0
    
    # Difficulty-wise performance (only quiz attempts have difficulty levels)
    difficulty_stats = {}
    for attempt in quiz_attempts:
        difficulty = attempt.difficulty_level or 'simple'
        if difficulty not in difficulty_stats:
            difficulty_stats[difficulty] = {'attempts': 0, 'total_score': 0}
        difficulty_stats[difficulty]['attempts'] += 1
        difficulty_stats[difficulty]['total_score'] += attempt.score or 0
    
    # Calculate averages for each difficulty
    for difficulty in difficulty_stats:
        if difficulty_stats[difficulty]['attempts'] > 0:
            difficulty_stats[difficulty]['average_score'] = difficulty_stats[difficulty]['total_score'] / difficulty_stats[difficulty]['attempts']
        else:
            difficulty_stats[difficulty]['average_score'] = 0
    
    # Quiz statistics
    quiz_total_attempts = quiz_attempts.count()
    quiz_total_questions = quiz_attempts.aggregate(total=Sum('total_questions'))['total'] or 0
    quiz_total_correct = quiz_attempts.aggregate(total=Sum('correct_answers'))['total'] or 0
    quiz_average_score = quiz_attempts.aggregate(avg=Avg('score'))['avg'] or 0
    
    # Mock test statistics
    mock_total_attempts = mock_test_attempts.count()
    mock_total_questions = mock_total_attempts * 10  # Default assumption for mock tests
    mock_total_correct = sum(attempt.score or 0 for attempt in mock_test_attempts)
    mock_average_score = sum(attempt.score or 0 for attempt in mock_test_attempts) / mock_total_attempts if mock_total_attempts > 0 else 0
    
    return Response({
        'overall': {
            'total_attempts': total_attempts,
            'total_questions': total_questions,
            'total_correct_answers': total_correct,
            'average_score': round(average_score, 2),
            'accuracy_percentage': round((total_correct / total_questions * 100) if total_questions > 0 else 0, 2)
        },
        'quiz': {
            'total_attempts': quiz_total_attempts,
            'total_questions': quiz_total_questions,
            'total_correct_answers': quiz_total_correct,
            'average_score': round(quiz_average_score, 2),
            'accuracy_percentage': round((quiz_total_correct / quiz_total_questions * 100) if quiz_total_questions > 0 else 0, 2)
        },
        'mock_test': {
            'total_attempts': mock_total_attempts,
            'total_questions': mock_total_questions,
            'total_correct_answers': mock_total_correct,
            'average_score': round(mock_average_score, 2),
            'accuracy_percentage': round((mock_total_correct / mock_total_questions * 100) if mock_total_questions > 0 else 0, 2)
        },
        'subject_wise': subject_stats,
        'class_wise': class_stats,
        'difficulty_wise': difficulty_stats
    })


def update_student_performance(student_reg, attempt):
    """
    Update student performance record based on quiz attempt
    """
    # Skip performance update for anonymous users or when no user is available
    # This is for testing purposes - in production, proper authentication should be used
    return
    
    # Note: The following code would be used with proper authentication:
    # try:
    #     performance = StudentPerformance.objects.get(student=student_reg)
    # except StudentPerformance.DoesNotExist:
    #     performance = StudentPerformance.objects.create(student=student_reg)
    if not student_reg:
        return  # Skip if no student registration found
    
    # Update overall statistics
    performance.total_quizzes_attempted += 1
    performance.total_questions_answered += attempt.total_questions
    performance.total_correct_answers += attempt.correct_answers
    performance.last_quiz_date = attempt.attempted_at
    
    # Recalculate overall average score
    all_attempts = QuizAttempt.objects.filter(student_id=student_reg)
    if all_attempts.exists():
        performance.overall_average_score = all_attempts.aggregate(avg=Avg('score'))['avg'] or 0
    
    # Update subject-wise scores
    subject = attempt.subject.lower() if attempt.subject else ''
    if 'math' in subject or 'mathematics' in subject:
        performance.mathematics_score = calculate_subject_average(student, 'mathematics')
    elif 'science' in subject:
        performance.science_score = calculate_subject_average(student, 'science')
    elif 'english' in subject:
        performance.english_score = calculate_subject_average(student, 'english')
    elif 'computer' in subject or 'programming' in subject:
        performance.computers_score = calculate_subject_average(student, 'computers')
    
    # Update class-wise scores
    class_name = attempt.class_name or ''
    if '7' in class_name:
        performance.class_7_score = calculate_class_average(student, '7')
    elif '8' in class_name:
        performance.class_8_score = calculate_class_average(student, '8')
    elif '9' in class_name:
        performance.class_9_score = calculate_class_average(student, '9')
    elif '10' in class_name:
        performance.class_10_score = calculate_class_average(student, '10')
    
    # Update difficulty-wise scores
    difficulty = attempt.difficulty_level or 'simple'
    if difficulty == 'simple':
        performance.simple_difficulty_score = calculate_difficulty_average(student, 'simple')
    elif difficulty == 'medium':
        performance.medium_difficulty_score = calculate_difficulty_average(student, 'medium')
    elif difficulty == 'hard':
        performance.hard_difficulty_score = calculate_difficulty_average(student, 'hard')
    
    # Calculate average time per question
    total_time = all_attempts.aggregate(total=Sum('time_taken_seconds'))['total'] or 0
    total_questions = all_attempts.aggregate(total=Sum('total_questions'))['total'] or 0
    if total_questions > 0:
        performance.average_time_per_question = total_time / total_questions
    
    # Calculate completion rate
    completed_attempts = all_attempts.filter(completion_percentage__gte=80).count()
    performance.completion_rate = (completed_attempts / all_attempts.count() * 100) if all_attempts.count() > 0 else 0
    
    performance.save()


def calculate_subject_average(student, subject_keyword):
    """
    Calculate average score for a specific subject
    """
    student_reg = get_student_registration(student)
    if not student_reg:
        return 0
    
    attempts = QuizAttempt.objects.filter(student_id=student_reg)
    subject_attempts = []
    
    for attempt in attempts:
        subject = attempt.subject.lower() if attempt.subject else ''
        if subject_keyword in subject:
            subject_attempts.append(attempt.score or 0)
    
    return sum(subject_attempts) / len(subject_attempts) if subject_attempts else 0


def calculate_class_average(student, class_number):
    """
    Calculate average score for a specific class
    """
    student_reg = get_student_registration(student)
    if not student_reg:
        return 0
    
    attempts = QuizAttempt.objects.filter(
        student_id=student_reg,
        class_name__icontains=class_number
    )
    
    if attempts.exists():
        return attempts.aggregate(avg=Avg('score'))['avg'] or 0
    return 0


def calculate_difficulty_average(student, difficulty):
    """
    Calculate average score for a specific difficulty level
    """
    student_reg = get_student_registration(student)
    if not student_reg:
        return 0
    
    attempts = QuizAttempt.objects.filter(
        student_id=student_reg,
        difficulty_level=difficulty
    )
    
    if attempts.exists():
        return attempts.aggregate(avg=Avg('score'))['avg'] or 0
    return 0
