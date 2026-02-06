from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'is_emailed', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_emailed', 'created_at']
    search_fields = ['recipient__email', 'title', 'message']
    readonly_fields = ['created_at', 'updated_at', 'email_sent_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Recipient', {
            'fields': ('recipient',)
        }),
        ('Notification Details', {
            'fields': ('notification_type', 'title', 'message', 'link')
        }),
        ('Related Objects', {
            'fields': ('job_id', 'application_id')
        }),
        ('Status', {
            'fields': ('is_read', 'is_emailed', 'email_sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
