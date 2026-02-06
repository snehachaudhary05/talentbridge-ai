from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Stores conversation sessions between users and AI assistant"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_conversations'
    )
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id} - {self.user.email}"


class Message(models.Model):
    """Individual messages within a conversation"""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional data like token count, model used, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class AIAnalytics(models.Model):
    """Track AI usage analytics for monitoring and optimization"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_analytics'
    )
    action_type = models.CharField(
        max_length=50,
        help_text="Type of AI action (e.g., resume_analysis, job_match, etc.)"
    )
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    response_time_ms = models.IntegerField(help_text="Response time in milliseconds")
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.action_type} - {self.created_at}"
