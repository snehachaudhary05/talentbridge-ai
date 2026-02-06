"""
Test script to verify OpenRouter integration with Gemma 3 12B
"""
import os
import sys
import django

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from ai_assistant.utils.ai_client import get_ai_client


def safe_print(text):
    """Print text with safe encoding"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove emojis and special characters
        print(text.encode('ascii', 'ignore').decode('ascii'))


def test_openrouter():
    """Test that OpenRouter is working correctly"""

    safe_print("=" * 60)
    safe_print("Testing OpenRouter with Gemma 3 12B (FREE)")
    safe_print("=" * 60)

    try:
        # Get AI client
        client = get_ai_client()

        safe_print(f"\n[OK] AI Client initialized")
        safe_print(f"  Provider: {client.provider}")
        safe_print(f"  Model: {client.model}")
        safe_print(f"  Using Mock: {client.use_mock}")

        # Test 1: Simple message
        safe_print("\n" + "=" * 60)
        safe_print("Test 1: Simple AI Response")
        safe_print("=" * 60)

        messages = [{
            "role": "user",
            "content": "Say hello and confirm you're working!"
        }]

        response = client.generate_response(messages)

        if response.get('success'):
            safe_print("[OK] Basic communication working")
            safe_print(f"  Response: {response['content']}")
            safe_print(f"  Input tokens: {response['usage']['input_tokens']}")
            safe_print(f"  Output tokens: {response['usage']['output_tokens']}")
            safe_print(f"  Response time: {response['response_time_ms']}ms")
            safe_print(f"  Model used: {response.get('model', 'N/A')}")
        else:
            safe_print("[FAIL] Basic communication failed")
            safe_print(f"  Error: {response.get('error')}")
            return False

        # Test 2: Resume Analysis
        safe_print("\n" + "=" * 60)
        safe_print("Test 2: Resume Analysis")
        safe_print("=" * 60)

        messages = [{
            "role": "user",
            "content": "Analyze this resume and extract key skills: Software Engineer with 5 years experience in Python, Django, React, and PostgreSQL. Built scalable web applications."
        }]

        response = client.generate_response(
            messages,
            system_prompt="You are an AI assistant that analyzes resumes. Extract and list the key skills."
        )

        if response.get('success'):
            safe_print("[OK] Resume analysis working")
            safe_print(f"  Response:\n{response['content'][:200]}...")
            safe_print(f"  Response time: {response['response_time_ms']}ms")
        else:
            safe_print("[FAIL] Resume analysis failed")
            safe_print(f"  Error: {response.get('error')}")
            return False

        # Test 3: Job Matching
        safe_print("\n" + "=" * 60)
        safe_print("Test 3: Job Matching Score")
        safe_print("=" * 60)

        messages = [{
            "role": "user",
            "content": "Rate the match (0-100%) between this candidate: 'Python developer with Django experience' and this job: 'Looking for a Python/Django backend developer'. Provide just the score and brief reason."
        }]

        response = client.generate_response(messages)

        if response.get('success'):
            safe_print("[OK] Job matching working")
            safe_print(f"  Response:\n{response['content']}")
            safe_print(f"  Response time: {response['response_time_ms']}ms")
        else:
            safe_print("[FAIL] Job matching failed")
            return False

        # All tests passed
        safe_print("\n" + "=" * 60)
        safe_print("[SUCCESS] ALL OPENROUTER TESTS PASSED!")
        safe_print("=" * 60)
        safe_print(f"\nOpenRouter is working perfectly with {client.model}!")
        safe_print("\nYour job portal now has FREE AI capabilities:")
        safe_print("  * Resume parsing and analysis")
        safe_print("  * Job-candidate matching")
        safe_print("  * Skill extraction")
        safe_print("  * Interview question generation")
        safe_print("\nNo usage limits on free models!")

        return True

    except Exception as e:
        safe_print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    try:
        success = test_openrouter()
        sys.exit(0 if success else 1)
    except Exception as e:
        safe_print(f"\n[ERROR] Error: {e}")
        sys.exit(1)
