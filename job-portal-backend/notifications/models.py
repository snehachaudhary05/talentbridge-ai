from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Notification model to store in-app and email notifications
    """
    NOTIFICATION_TYPES = (
        ('application_submitted', 'Application Submitted'),
        ('application_status_changed', 'Application Status Changed'),
        ('new_application', 'New Application Received'),
        ('job_match', 'New Job Match'),
        ('resume_viewed', 'Resume Viewed'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_cancelled', 'Interview Cancelled'),
        ('interview_rescheduled', 'Interview Rescheduled'),
        ('job_expiring', 'Job Posting Expiring Soon'),
        ('system', 'System Notification'),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, null=True)  # Link to relevant page

    is_read = models.BooleanField(default=False)
    is_emailed = models.BooleanField(default=False)  # Track if email was sent
    email_sent_at = models.DateTimeField(null=True, blank=True)

    # Optional: related objects for context
    job_id = models.IntegerField(null=True, blank=True)
    application_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read']),
        ]

    def __str__(self):
        return f"{self.recipient.email} - {self.title}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read', 'updated_at'])

    def mark_as_emailed(self):
        """Mark that email was sent"""
        from django.utils import timezone
        if not self.is_emailed:
            self.is_emailed = True
            self.email_sent_at = timezone.now()
            self.save(update_fields=['is_emailed', 'email_sent_at', 'updated_at'])
