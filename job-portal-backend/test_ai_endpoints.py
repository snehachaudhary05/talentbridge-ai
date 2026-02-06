import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from ai_assistant.handlers.candidate_handler import CandidateHandler

# Get a candidate user
try:
    candidate = User.objects.filter(role='candidate').first()
    if not candidate:
        print("[ERROR] No candidate found in database")
        exit(1)

    print(f"[OK] Testing with candidate: {candidate.email}")

    # Test 1: Job Matching
    print("\n" + "="*80)
    print("TEST 1: Job Matching")
    print("="*80)
    try:
        handler = CandidateHandler(candidate)
        skills = ['Python', 'Django', 'React']
        result = handler.suggest_jobs(skills, limit=5)
        print(f"[OK] Job Matching works! Found {len(result)} job recommendations")
        if result:
            print(f"   First match: {result[0]['title']} - {result[0]['match_score']}% match")
    except Exception as e:
        print(f"[ERROR] Job Matching failed: {str(e)}")
        import traceback
        traceback.print_exc()

    # Test 2: Skills Recommendations
    print("\n" + "="*80)
    print("TEST 2: Skills Recommendations")
    print("="*80)
    try:
        handler = CandidateHandler(candidate)
        result = handler.recommend_skills(
            current_skills=['Python', 'Django'],
            target_role='Senior Backend Engineer'
        )
        print(f"[OK] Skills Recommendations works!")
        print(f"   Result type: {type(result)}")
        print(f"   Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"[ERROR] Skills Recommendations failed: {str(e)}")
        import traceback
        traceback.print_exc()

    # Test 3: Resume Analysis
    print("\n" + "="*80)
    print("TEST 3: Resume Analysis")
    print("="*80)
    try:
        handler = CandidateHandler(candidate)
        resume_text = """
        John Doe
        Senior Software Engineer

        Skills: Python, Django, React, PostgreSQL, Docker
        Experience: 5 years of backend development
        """
        result = handler.analyze_resume(resume_text)
        print(f"[OK] Resume Analysis works!")
        print(f"   Result type: {type(result)}")
        print(f"   Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    except Exception as e:
        print(f"[ERROR] Resume Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

except Exception as e:
    print(f"[ERROR] General error: {str(e)}")
    import traceback
    traceback.print_exc()
