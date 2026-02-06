from django.contrib import admin
from .models import Conversation, Message, AIAnalytics


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'role', 'content_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'conversation__user__email']
    readonly_fields = ['created_at']

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = 'Content'


@admin.register(AIAnalytics)
class AIAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'action_type', 'input_tokens', 'output_tokens',
        'response_time_ms', 'success', 'created_at'
    ]
    list_filter = ['action_type', 'success', 'created_at']
    search_fields = ['user__email', 'action_type', 'error_message']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        # Analytics are auto-generated, not manually created
        return False
