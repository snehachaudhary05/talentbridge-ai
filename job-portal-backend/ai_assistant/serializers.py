from rest_framework import serializers
from .models import Conversation, Message, AIAnalytics


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""

    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations"""
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title', 'messages', 'message_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for conversation listings"""
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'message_count', 'last_message', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'role': last_msg.role,
                'content': last_msg.content[:100],  # First 100 chars
                'created_at': last_msg.created_at
            }
        return None


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat requests"""
    message = serializers.CharField(required=True)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)


class ResumeAnalysisRequestSerializer(serializers.Serializer):
    """Serializer for resume analysis requests"""
    resume_text = serializers.CharField(required=False, allow_blank=True)
    resume_file = serializers.FileField(required=False)

    def validate(self, data):
        if not data.get('resume_text') and not data.get('resume_file'):
            raise serializers.ValidationError("Either resume_text or resume_file is required")
        return data


class JobMatchRequestSerializer(serializers.Serializer):
    """Serializer for job matching requests"""
    resume_text = serializers.CharField(required=False)
    skills = serializers.ListField(child=serializers.CharField(), required=False)
    limit = serializers.IntegerField(default=10, min_value=1, max_value=50)


class SkillRecommendationRequestSerializer(serializers.Serializer):
    """Serializer for skill recommendation requests"""
    current_skills = serializers.ListField(child=serializers.CharField(), required=True)
    target_role = serializers.CharField(required=True)


class JobDescriptionRequestSerializer(serializers.Serializer):
    """Serializer for job description generation"""
    position = serializers.CharField(required=True)
    company = serializers.CharField(required=True)
    requirements = serializers.CharField(required=True)
    additional_context = serializers.CharField(required=False, allow_blank=True)


class InterviewQuestionsRequestSerializer(serializers.Serializer):
    """Serializer for interview questions generation"""
    role = serializers.CharField(required=True, max_length=200)
    skills = serializers.CharField(required=True, max_length=500)
    count = serializers.IntegerField(required=False, default=10, min_value=1, max_value=20)


class CandidateScreeningRequestSerializer(serializers.Serializer):
    """Serializer for candidate screening requests"""
    job_requirements = serializers.CharField(required=True, max_length=2000)
    resume_text = serializers.CharField(required=False, allow_blank=True)
    resume_file = serializers.FileField(required=False)

    def validate(self, data):
        if not data.get('resume_text') and not data.get('resume_file'):
            raise serializers.ValidationError("Either resume_text or resume_file is required")
        return data


class CandidateRankingRequestSerializer(serializers.Serializer):
    """Serializer for candidate ranking requests"""
    job_id = serializers.IntegerField(required=True)


class ResumeSummaryRequestSerializer(serializers.Serializer):
    """Serializer for resume summary requests"""
    application_id = serializers.IntegerField(required=True)


class SpamDetectionRequestSerializer(serializers.Serializer):
    """Serializer for spam detection requests"""
    content_type = serializers.ChoiceField(choices=['job', 'application', 'user'], required=True)
    content_id = serializers.IntegerField(required=True)


class ModerationRequestSerializer(serializers.Serializer):
    """Serializer for moderation action requests"""
    user_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=True)


class TrendAnalysisRequestSerializer(serializers.Serializer):
    """Serializer for trend analysis requests"""
    metric = serializers.CharField(default='all')
    days = serializers.IntegerField(default=30, min_value=1, max_value=365)


class AIAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for AI analytics"""
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AIAnalytics
        fields = [
            'id', 'user', 'user_email', 'action_type',
            'input_tokens', 'output_tokens', 'response_time_ms',
            'success', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
