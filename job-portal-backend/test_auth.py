import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

print('=== TESTING AUTHENTICATION ===\n')

# Test accounts
test_accounts = [
    ('recruiter.test@talentbridge.ai', 'Test@123'),
    ('test_recruiter@example.com', 'Test@123'),
    ('recruiter@example.com', 'Test@123'),
]

for email, password in test_accounts:
    print(f'Testing: {email}')

    # Check if user exists
    user_exists = User.objects.filter(email=email).exists()
    print(f'  User exists: {user_exists}')

    if user_exists:
        user = User.objects.get(email=email)
        print(f'  Role: {user.role}')
        print(f'  Active: {user.is_active}')

        # Test authentication
        auth_user = authenticate(username=email, password=password)
        if auth_user:
            print(f'  Auth: SUCCESS')
        else:
            print(f'  Auth: FAILED')
    else:
        print(f'  Auth: USER NOT FOUND')

    print()

print('\n=== CREATING FRESH TEST ACCOUNTS ===\n')

# Create fresh test accounts
accounts_to_create = [
    {
        'email': 'recruiter@talentbridge.com',
        'password': 'Test@123',
        'role': 'recruiter',
        'first_name': 'John',
        'last_name': 'Recruiter'
    },
    {
        'email': 'candidate@talentbridge.com',
        'password': 'Test@123',
        'role': 'candidate',
        'first_name': 'Jane',
        'last_name': 'Candidate'
    }
]

for account in accounts_to_create:
    email = account['email']
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'role': account['role'],
            'first_name': account['first_name'],
            'last_name': account['last_name'],
            'is_active': True
        }
    )
    user.set_password(account['password'])
    user.save()

    status = 'CREATED' if created else 'UPDATED'
    print(f'{status}: {email}')
    print(f'  Password: {account["password"]}')
    print(f'  Role: {account["role"]}')

    # Verify authentication works
    auth_user = authenticate(username=email, password=account['password'])
    print(f'  Auth Test: {"SUCCESS" if auth_user else "FAILED"}')
    print()

print('\n=== SUMMARY ===')
print('Use these accounts to login:')
print('  Recruiter: recruiter@talentbridge.com / Test@123')
print('  Candidate: candidate@talentbridge.com / Test@123')
