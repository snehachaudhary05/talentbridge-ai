import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.models import Notification
from notifications.utils.email_service import email_service

print('=== SENDING PENDING NOTIFICATION EMAILS ===\n')

# Get all notifications that haven't been emailed yet
pending_notifications = Notification.objects.filter(is_emailed=False).order_by('-created_at')

print(f'Found {pending_notifications.count()} pending notifications\n')

# For Resend testing, all emails will go to: chaudharysneha693@gmail.com
# (the Resend account owner's email)

for notification in pending_notifications:
    print(f'Processing notification {notification.id}...')
    print(f'  Type: {notification.notification_type}')
    print(f'  Recipient: {notification.recipient.email}')
    print(f'  Title: {notification.title}')

    # Send email based on notification type
    success = False

    if notification.notification_type == 'application_submitted':
        if notification.job_id:
            from jobs.models import Job
            try:
                job = Job.objects.get(id=notification.job_id)
                success = email_service.send_application_submitted_email(
                    notification.recipient,
                    job.title,
                    notification.application_id
                )
            except Job.DoesNotExist:
                print('  Job not found')

    elif notification.notification_type == 'new_application':
        if notification.application_id:
            from jobs.models import Application
            try:
                application = Application.objects.get(id=notification.application_id)
                candidate_name = application.candidate.first_name or application.candidate.email.split('@')[0]
                success = email_service.send_new_application_email(
                    notification.recipient,
                    candidate_name,
                    application.job.title,
                    notification.application_id
                )
            except Application.DoesNotExist:
                print('  Application not found')

    if success:
        notification.mark_as_emailed()
        print('  Email sent: SUCCESS')
    else:
        print('  Email sent: FAILED')

    print()

print('Done!')
