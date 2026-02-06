import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

print("\n" + "="*80)
print("ALL REGISTERED USERS")
print("="*80 + "\n")

users = User.objects.all()

if not users:
    print("No users found in the database.")
else:
    for user in users:
        print(f"Email: {user.email}")
        print(f"Role: {user.role.upper()}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Created: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 80)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total Users: {users.count()}")
print(f"Recruiters: {users.filter(role='recruiter').count()}")
print(f"Candidates: {users.filter(role='candidate').count()}")
print("="*80 + "\n")
