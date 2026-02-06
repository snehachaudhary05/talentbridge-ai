from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from jobs.models import Application, Interview
from .utils.notification_service import notification_service
from .utils.email_service import email_service
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Application)
def application_created_notification(sender, instance, created, **kwargs):
    """
    Send notification when a new application is created
    - Notify candidate: Application submitted
    - Notify recruiter: New application received
    """
    if created:
        # Notify candidate
        try:
            notification_service.create_notification(
                recipient=instance.candidate,
                notification_type='application_submitted',
                title='Application Submitted Successfully',
                message=f'Your application for {instance.job.title} has been submitted successfully!',
                link=f'/dashboard',
                job_id=instance.job.id,
                application_id=instance.id,
                send_email=True
            )
            logger.info(f"Candidate notification created for application {instance.id}")
        except Exception as e:
            logger.error(f"Error creating candidate notification: {str(e)}")

        # Notify recruiter
        try:
            candidate_name = instance.candidate.first_name or instance.candidate.email.split('@')[0]
            notification_service.create_notification(
                recipient=instance.job.recruiter,
                notification_type='new_application',
                title='New Application Received',
                message=f'New application: {candidate_name} applied for {instance.job.title}',
                link=f'/dashboard',
                job_id=instance.job.id,
                application_id=instance.id,
                send_email=True
            )
            logger.info(f"Recruiter notification created for application {instance.id}")
        except Exception as e:
            logger.error(f"Error creating recruiter notification: {str(e)}")


# Store original status before save
@receiver(pre_save, sender=Application)
def store_original_status(sender, instance, **kwargs):
    """Store the original status before update"""
    if instance.pk:  # Only for existing instances
        try:
            original = Application.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except Application.DoesNotExist:
            instance._original_status = None
    else:
        instance._original_status = None


@receiver(post_save, sender=Application)
def application_status_changed_notification(sender, instance, created, **kwargs):
    """
    Send notification when application status changes
    Only notify candidate
    """
    if not created and hasattr(instance, '_original_status'):
        original_status = instance._original_status
        new_status = instance.status

        # Only notify if status actually changed
        if original_status and original_status != new_status:
            try:
                notification_service.create_notification(
                    recipient=instance.candidate,
                    notification_type='application_status_changed',
                    title='Application Status Updated',
                    message=f'Your application for {instance.job.title} status changed to {new_status}',
                    link=f'/dashboard',
                    job_id=instance.job.id,
                    application_id=instance.id,
                    send_email=True
                )
                logger.info(f"Status change notification created for application {instance.id}")
            except Exception as e:
                logger.error(f"Error creating status change notification: {str(e)}")


# Store original status before interview save
@receiver(pre_save, sender=Interview)
def store_original_interview_status(sender, instance, **kwargs):
    """Store the original status before update"""
    if instance.pk:  # Only for existing instances
        try:
            original = Interview.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except Interview.DoesNotExist:
            instance._original_status = None
    else:
        instance._original_status = None


@receiver(post_save, sender=Interview)
def interview_notification(sender, instance, created, **kwargs):
    """
    Send notification when interview is scheduled or status changes
    """
    try:
        candidate = instance.application.candidate
        job_title = instance.application.job.title

        if created:
            # New interview scheduled
            notification_service.create_notification(
                recipient=candidate,
                notification_type='interview_scheduled',
                title='Interview Scheduled',
                message=f'Interview scheduled for {job_title} on {instance.scheduled_datetime.strftime("%B %d, %Y at %I:%M %p")}',
                link=f'/dashboard',
                job_id=instance.application.job.id,
                application_id=instance.application.id,
                send_email=False  # We'll send custom email below
            )

            # Send custom interview email
            email_service.send_interview_scheduled_email(
                candidate=candidate,
                job_title=job_title,
                interview_datetime=instance.scheduled_datetime,
                interview_type=instance.interview_type,
                location=instance.location,
                notes=instance.notes
            )

            logger.info(f"Interview scheduled notification sent for interview {instance.id}")

        elif hasattr(instance, '_original_status'):
            # Status changed
            original_status = instance._original_status
            new_status = instance.status

            if original_status and original_status != new_status:
                if new_status == 'cancelled':
                    # Interview cancelled
                    notification_service.create_notification(
                        recipient=candidate,
                        notification_type='interview_cancelled',
                        title='Interview Cancelled',
                        message=f'Your interview for {job_title} scheduled on {instance.scheduled_datetime.strftime("%B %d, %Y")} has been cancelled',
                        link=f'/dashboard',
                        job_id=instance.application.job.id,
                        application_id=instance.application.id,
                        send_email=False  # We'll send custom email below
                    )

                    # Send cancellation email
                    email_service.send_interview_cancelled_email(
                        candidate=candidate,
                        job_title=job_title,
                        interview_datetime=instance.scheduled_datetime
                    )

                    logger.info(f"Interview cancelled notification sent for interview {instance.id}")

    except Exception as e:
        logger.error(f"Error creating interview notification: {str(e)}")
