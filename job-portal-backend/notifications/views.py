from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for notifications
    - List: Get all notifications for current user
    - Retrieve: Get specific notification
    - mark_as_read: Mark notification as read
    - mark_all_as_read: Mark all notifications as read
    - unread_count: Get count of unread notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notifications for current user only"""
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a specific notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({
            'success': True,
            'message': 'Notification marked as read'
        })

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for current user"""
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({
            'success': True,
            'message': f'{count} notifications marked as read',
            'count': count
        })

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({
            'count': count
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent unread notifications (last 10)"""
        notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )[:10]
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
