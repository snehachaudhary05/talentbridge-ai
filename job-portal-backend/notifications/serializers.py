from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""

    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'link',
            'is_read',
            'is_emailed',
            'job_id',
            'application_id',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'is_emailed']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications (admin/internal use)"""

    class Meta:
        model = Notification
        fields = [
            'recipient',
            'notification_type',
            'title',
            'message',
            'link',
            'job_id',
            'application_id',
        ]
