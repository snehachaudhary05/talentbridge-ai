"""
Quick test script to verify the FREE mock AI is working
Run this after setting up the database to test AI features
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from ai_assistant.utils.ai_client import get_ai_client


def test_mock_ai():
    """Test that mock AI is working correctly"""

    print("=" * 60)
    print("Testing FREE Mock AI (No API Key Required)")
    print("=" * 60)

    # Get AI client (should automatically use mock)
    client = get_ai_client()

    print(f"\n[OK] AI Client initialized")
    print(f"  Provider: {client.provider}")
    print(f"  Using Mock: {client.use_mock}")

    # Test 1: Resume Analysis
    print("\n" + "=" * 60)
    print("Test 1: Resume Analysis")
    print("=" * 60)

    messages = [{
        "role": "user",
        "content": "Analyze this resume: Software Engineer with 5 years Python experience"
    }]

    response = client.generate_response(messages, system_prompt="Analyze the resume")

    if response.get('success'):
        print("[OK] Resume analysis working")
        print(f"  Response length: {len(response['content'])} characters")
        print(f"  Input tokens: {response['usage']['input_tokens']}")
        print(f"  Output tokens: {response['usage']['output_tokens']}")
        print(f"  Response time: {response['response_time_ms']}ms")
        print(f"\n  Sample response:\n  {response['content'][:200]}...")
    else:
        print("[FAIL] Resume analysis failed")
        print(f"  Error: {response.get('error')}")
        return False

    # Test 2: Job Matching
    print("\n" + "=" * 60)
    print("Test 2: Job Matching")
    print("=" * 60)

    messages = [{
        "role": "user",
        "content": "Match this candidate with the job: Python developer position"
    }]

    response = client.generate_response(messages)

    if response.get('success'):
        print("[OK] Job matching working")
        print(f"  Response length: {len(response['content'])} characters")
        print(f"\n  Sample response:\n  {response['content'][:200]}...")
    else:
        print("[FAIL] Job matching failed")
        return False

    # Test 3: Skill Recommendations
    print("\n" + "=" * 60)
    print("Test 3: Skill Recommendations")
    print("=" * 60)

    messages = [{
        "role": "user",
        "content": "Recommend skills for a backend developer"
    }]

    response = client.generate_response(messages)

    if response.get('success'):
        print("[OK] Skill recommendations working")
        print(f"  Response length: {len(response['content'])} characters")
        print(f"\n  Sample response:\n  {response['content'][:200]}...")
    else:
        print("[FAIL] Skill recommendations failed")
        return False

    # All tests passed
    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe FREE mock AI is working perfectly!")
    print("You can now:")
    print("  1. Start the server: python manage.py runserver")
    print("  2. Test the API endpoints")
    print("  3. Build your frontend")
    print("  4. Deploy the application")
    print("\nNo API key required - everything works for FREE!")
    print("\nSee QUICKSTART_FREE.md for more details.")

    return True


if __name__ == '__main__':
    try:
        success = test_mock_ai()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        print("\nMake sure you've run:")
        print("  1. pip install -r requirements.txt")
        print("  2. python manage.py migrate")
        sys.exit(1)
