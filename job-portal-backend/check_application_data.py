import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from jobs.models import Application
from accounts.models import CandidateProfile

print("\n" + "="*80)
print("APPLICATION DATA CHECK")
print("="*80 + "\n")

applications = Application.objects.all()

if not applications:
    print("No applications found in the database.")
else:
    for app in applications:
        print(f"Application ID: {app.id}")
        print(f"Job: {app.job.title}")
        print(f"Candidate Email: {app.candidate.email}")
        print(f"Candidate Name: {app.candidate.first_name} {app.candidate.last_name}")
        print(f"Status: {app.status}")
        print(f"Applied At: {app.applied_at}")

        # Check candidate profile
        try:
            profile = CandidateProfile.objects.get(user=app.candidate)
            print(f"\nCandidate Profile Data:")
            print(f"  - Phone: '{profile.phone}'")
            print(f"  - Location: '{profile.location}'")
            print(f"  - Skills: '{profile.skills}'")
            print(f"  - Experience Years: {profile.experience_years}")
            print(f"  - College Name: '{profile.college_name}'")
            print(f"  - Passout Year: {profile.passout_year}")
            print(f"  - LinkedIn: '{profile.linkedin_url}'")
            print(f"  - LeetCode: '{profile.leetcode_url}'")
            print(f"  - GitHub: '{profile.github_url}'")
            print(f"  - Has Resume: {bool(profile.resume_file)}")
        except CandidateProfile.DoesNotExist:
            print("\nNo candidate profile found!")

        print("-" * 80)

print("\n" + "="*80)
print(f"Total Applications: {applications.count()}")
print("="*80 + "\n")
