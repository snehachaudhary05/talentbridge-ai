from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Conversation, Message, AIAnalytics
from .serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer,
    ChatRequestSerializer,
    ResumeAnalysisRequestSerializer,
    JobMatchRequestSerializer,
    SkillRecommendationRequestSerializer,
    JobDescriptionRequestSerializer,
    InterviewQuestionsRequestSerializer,
    CandidateScreeningRequestSerializer,
    CandidateRankingRequestSerializer,
    ResumeSummaryRequestSerializer,
    SpamDetectionRequestSerializer,
    ModerationRequestSerializer,
    TrendAnalysisRequestSerializer,
    AIAnalyticsSerializer
)
from .handlers import CandidateHandler, RecruiterHandler, AdminHandler
from .utils.prompt_templates import get_system_prompt, format_conversation_history
from .utils.ai_client import get_ai_client
from accounts.permissions import IsRecruiter, IsCandidate, IsAdmin


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing AI conversations
    """
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in a conversation"""
        conversation = self.get_object()

        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data['message']

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )

        # Get conversation history
        messages = conversation.messages.all()
        formatted_messages = format_conversation_history(messages)

        # Generate AI response
        start_time = timezone.now()
        ai_client = get_ai_client()

        try:
            response = ai_client.generate_response(
                messages=formatted_messages,
                system_prompt=get_system_prompt(request.user.role)
            )

            assistant_content = response.get('content', '')
            usage = response.get('usage', {})

            # Save assistant message
            Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=assistant_content,
                metadata={'usage': usage}
            )

            # Track analytics
            response_time = int((timezone.now() - start_time).total_seconds() * 1000)
            AIAnalytics.objects.create(
                user=request.user,
                action_type='chat',
                input_tokens=usage.get('input_tokens', 0),
                output_tokens=usage.get('output_tokens', 0),
                response_time_ms=response_time,
                success=True
            )

            return Response({
                'message': assistant_content,
                'conversation_id': conversation.id,
                'usage': usage
            })

        except Exception as e:
            response_time = int((timezone.now() - start_time).total_seconds() * 1000)
            AIAnalytics.objects.create(
                user=request.user,
                action_type='chat',
                response_time_ms=response_time,
                success=False,
                error_message=str(e)
            )

            return Response(
                {'error': 'Failed to generate response', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CandidateAIViewSet(viewsets.ViewSet):
    """
    AI features for candidates
    """
    permission_classes = [IsCandidate]

    @action(detail=False, methods=['post'])
    def analyze_resume(self, request):
        """Analyze resume and extract information"""
        serializer = ResumeAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = CandidateHandler(request.user)

        try:
            # Extract resume text
            resume_text = serializer.validated_data.get('resume_text', '')
            resume_file = serializer.validated_data.get('resume_file')

            if resume_file:
                # Extract text from uploaded file
                from .utils.file_parser import extract_text_from_file
                resume_text = extract_text_from_file(resume_file)
                print(f"[DEBUG] Extracted text from file: {resume_file.name}, size: {len(resume_text)} chars")

            # Validate that we have resume text
            if not resume_text or len(resume_text.strip()) < 50:
                return Response(
                    {'error': 'Resume text is too short or empty. Please provide a complete resume.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log resume size for debugging
            resume_size = len(resume_text)
            word_count = len(resume_text.split())
            print(f"[DEBUG] Resume size: {resume_size:,} chars ({resume_size/1024:.1f}KB), {word_count:,} words")
            print(f"[DEBUG] First 200 chars: {resume_text[:200]}")
            print(f"[DEBUG] Last 200 chars: {resume_text[-200:]}")

            # Validate resume size (prevent oversized resumes that cause AI to fail)
            MAX_RESUME_SIZE = 15000  # ~15KB, roughly 3-4 page resume
            if resume_size > MAX_RESUME_SIZE:
                print(f"[WARNING] Resume too large: {resume_size} > {MAX_RESUME_SIZE}")
                return Response(
                    {
                        'error': 'Resume is too large',
                        'message': f'Your resume is {resume_size:,} characters ({resume_size/1024:.1f}KB). Maximum allowed is {MAX_RESUME_SIZE/1024:.0f}KB.',
                        'details': {
                            'resume_size': resume_size,
                            'max_allowed': MAX_RESUME_SIZE,
                            'word_count': word_count,
                            'first_100_chars': resume_text[:100],
                            'last_100_chars': resume_text[-100:]
                        },
                        'suggestions': [
                            'If you uploaded a PDF: Try saving it as plain text or copying the text directly',
                            'Check if your resume has duplicate content or hidden formatting',
                            'A typical 1-2 page resume should be 2,000-5,000 characters',
                            'Your resume appears to be much longer than typical - verify the content'
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = handler.analyze_resume(resume_text)

            # Track analytics
            AIAnalytics.objects.create(
                user=request.user,
                action_type='resume_analysis',
                input_tokens=result.get('usage', {}).get('input_tokens', 0),
                output_tokens=result.get('usage', {}).get('output_tokens', 0),
                response_time_ms=result.get('response_time_ms', 0),
                success=True
            )

            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to analyze resume', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def suggest_jobs(self, request):
        """Get job suggestions based on skills"""
        serializer = JobMatchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = CandidateHandler(request.user)

        try:
            # Extract skills if resume provided
            if 'resume_text' in serializer.validated_data:
                skills = handler.extract_skills(serializer.validated_data['resume_text'])
            else:
                skills = serializer.validated_data.get('skills', [])

            recommendations = handler.suggest_jobs(
                candidate_skills=skills,
                limit=serializer.validated_data.get('limit', 10)
            )

            return Response({
                'skills_used': skills,
                'recommendations': recommendations
            })

        except Exception as e:
            return Response(
                {'error': 'Failed to suggest jobs', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def job_match(self, request):
        """Analyze match with a specific job"""
        serializer = ResumeAnalysisRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'error': 'job_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        handler = CandidateHandler(request.user)

        try:
            result = handler.analyze_job_match(
                serializer.validated_data['resume_text'],
                job_id
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to analyze job match', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def resume_feedback(self, request):
        """Get resume improvement feedback"""
        serializer = ResumeAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = CandidateHandler(request.user)

        try:
            result = handler.get_resume_feedback(serializer.validated_data['resume_text'])
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to generate feedback', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def recommend_skills(self, request):
        """Get skill recommendations for target role"""
        serializer = SkillRecommendationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = CandidateHandler(request.user)

        try:
            result = handler.recommend_skills(
                serializer.validated_data['current_skills'],
                serializer.validated_data['target_role']
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to recommend skills', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def application_status(self, request):
        """Get application status information"""
        application_id = request.query_params.get('application_id')
        if not application_id:
            return Response(
                {'error': 'application_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        handler = CandidateHandler(request.user)

        try:
            result = handler.get_application_status_info(int(application_id))
            return Response({'status_info': result})

        except Exception as e:
            return Response(
                {'error': 'Failed to get status', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecruiterAIViewSet(viewsets.ViewSet):
    """
    AI features for recruiters
    """
    permission_classes = [IsRecruiter]

    @action(detail=False, methods=['post'])
    def generate_job_description(self, request):
        """Generate optimized job description"""
        serializer = JobDescriptionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = RecruiterHandler(request.user)

        try:
            result = handler.generate_job_description(serializer.validated_data)
            return Response({'job_description': result})

        except Exception as e:
            return Response(
                {'error': 'Failed to generate job description', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def interview_questions(self, request):
        """Generate interview questions for a job"""
        serializer = InterviewQuestionsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = RecruiterHandler(request.user)

        try:
            result = handler.generate_interview_questions(
                role=serializer.validated_data['role'],
                skills=serializer.validated_data['skills'],
                count=serializer.validated_data.get('count', 10)
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to generate questions', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def screen_candidate(self, request):
        """Screen a candidate against job requirements"""
        print(f"[DEBUG SCREEN] Request data: {request.data}")
        print(f"[DEBUG SCREEN] Request FILES: {request.FILES}")
        serializer = CandidateScreeningRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"[DEBUG SCREEN] Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = RecruiterHandler(request.user)

        try:
            # Extract resume text from file if provided
            resume_text = serializer.validated_data.get('resume_text', '')
            resume_file = serializer.validated_data.get('resume_file')

            if resume_file:
                # Extract text from file
                from .utils.file_parser import extract_text_from_file
                resume_text = extract_text_from_file(resume_file)

            result = handler.screen_candidate(
                job_requirements=serializer.validated_data['job_requirements'],
                resume_text=resume_text
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to screen candidate', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def rank_candidates(self, request):
        """Rank candidates for a job"""
        serializer = CandidateRankingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = RecruiterHandler(request.user)

        try:
            result = handler.rank_candidates(serializer.validated_data['job_id'])
            return Response({'ranked_candidates': result})

        except Exception as e:
            return Response(
                {'error': 'Failed to rank candidates', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def summarize_resume(self, request):
        """Summarize a candidate's resume"""
        serializer = ResumeSummaryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = RecruiterHandler(request.user)

        try:
            result = handler.summarize_resume(serializer.validated_data['application_id'])
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to summarize resume', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def hiring_insights(self, request):
        """Get hiring insights"""
        job_id = request.query_params.get('job_id')

        handler = RecruiterHandler(request.user)

        try:
            result = handler.get_hiring_insights(job_id=int(job_id) if job_id else None)
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to get insights', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminAIViewSet(viewsets.ViewSet):
    """
    AI features for admins
    """
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['get'])
    def platform_analytics(self, request):
        """Get platform analytics"""
        days = int(request.query_params.get('days', 30))

        handler = AdminHandler(request.user)

        try:
            result = handler.get_platform_analytics(days=days)
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to get analytics', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def detect_spam(self, request):
        """Detect spam content"""
        serializer = SpamDetectionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = AdminHandler(request.user)

        try:
            result = handler.detect_spam(
                serializer.validated_data['content_type'],
                serializer.validated_data['content_id']
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to detect spam', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def suspicious_activities(self, request):
        """Get suspicious user activities"""
        threshold = int(request.query_params.get('threshold', 10))

        handler = AdminHandler(request.user)

        try:
            result = handler.get_suspicious_activities(threshold=threshold)
            return Response({'activities': result})

        except Exception as e:
            return Response(
                {'error': 'Failed to get activities', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def recommend_moderation(self, request):
        """Get moderation action recommendation"""
        serializer = ModerationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = AdminHandler(request.user)

        try:
            result = handler.recommend_moderation_action(
                serializer.validated_data['user_id'],
                serializer.validated_data['reason']
            )
            return Response(result)

        except Exception as e:
            return Response(
                {'error': 'Failed to get recommendation', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def analyze_trends(self, request):
        """Analyze platform trends"""
        serializer = TrendAnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        handler = AdminHandler(request.user)

        try:
            result = handler.analyze_trends(
                metric=serializer.validated_data['metric'],
                days=serializer.validated_data['days']
            )
            return Response({'analysis': result})

        except Exception as e:
            return Response(
                {'error': 'Failed to analyze trends', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
