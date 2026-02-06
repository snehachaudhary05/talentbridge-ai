import logging
from django.conf import settings
from ..models import Notification
from .email_service import email_service

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service to create and send notifications
    Handles both in-app and email notifications
    """

    @staticmethod
    def create_notification(
        recipient,
        notification_type,
        title,
        message,
        link=None,
        job_id=None,
        application_id=None,
        send_email=True
    ):
        """
        Create a notification and optionally send email

        Args:
            recipient: User instance
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            link: Optional link to relevant page
            job_id: Optional related job ID
            application_id: Optional related application ID
            send_email: Whether to send email notification

        Returns:
            Notification instance
        """
        # Create in-app notification
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
            job_id=job_id,
            application_id=application_id
        )

        logger.info(f"Created notification: {notification.id} for {recipient.email}")

        # Send email if requested
        if send_email:
            notification_service.send_notification_email(notification)

        return notification

    @staticmethod
    def send_notification_email(notification):
        """Send email for a notification based on type"""
        try:
            notification_type = notification.notification_type

            if notification_type == 'application_submitted':
                # Get job title from notification message or parse it
                job_title = notification.message.split("for ")[-1].split(" has")[0]
                success = email_service.send_application_submitted_email(
                    notification.recipient,
                    job_title,
                    notification.application_id
                )

            elif notification_type == 'application_status_changed':
                # Parse message for job title and status
                # Assuming message format: "Your application for {job} status changed to {status}"
                parts = notification.message.split("for ")
                if len(parts) > 1:
                    job_title = parts[1].split(" status")[0]
                    new_status = parts[1].split("to ")[-1].strip()
                    success = email_service.send_application_status_changed_email(
                        notification.recipient,
                        job_title,
                        "",  # old status not needed
                        new_status,
                        notification.application_id
                    )
                else:
                    success = False

            elif notification_type == 'new_application':
                # Parse candidate name and job title from message
                parts = notification.message.split(" applied for ")
                if len(parts) > 1:
                    candidate_name = parts[0].replace("New application: ", "")
                    job_title = parts[1]
                    success = email_service.send_new_application_email(
                        notification.recipient,
                        candidate_name,
                        job_title,
                        notification.application_id
                    )
                else:
                    success = False

            elif notification_type == 'job_match':
                # Parse job details from message
                # For now, use generic email or skip
                success = False  # Implement when needed
            else:
                success = False

            if success:
                notification.mark_as_emailed()
                logger.info(f"Email sent for notification {notification.id}")
            else:
                logger.warning(f"Email not sent for notification {notification.id}")

        except Exception as e:
            logger.error(f"Error sending email for notification {notification.id}: {str(e)}")


# Global instance
notification_service = NotificationService()
