import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from notifications.utils.email_service import email_service
from accounts.models import User

print('=== TESTING EMAIL SERVICE ===\n')

# Get a test user
try:
    user = User.objects.get(email='candidate@talentbridge.com')
    print(f'Test user: {user.email}')
    print(f'API Key configured: {bool(email_service.api_key)}')
    print(f'API Key: {email_service.api_key[:20]}...' if email_service.api_key else 'None')
    print()

    print('Sending test email...')
    result = email_service.send_application_submitted_email(
        user=user,
        job_title='Test Job Title',
        application_id=1
    )

    print(f'\nEmail send result: {"SUCCESS" if result else "FAILED"}')

except User.DoesNotExist:
    print('Test user not found')
except Exception as e:
    print(f'Error: {str(e)}')
    import traceback
    traceback.print_exc()
