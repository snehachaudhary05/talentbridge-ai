# Quick Setup Guide

## Step 1: Install Dependencies

```bash
cd job-portal-backend
pip install -r requirements.txt
```

## Step 2: Get AI API Key

You need an API key from one of these providers:

### Option A: Anthropic Claude (Recommended)

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### Option B: OpenAI

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-...`)

## Step 3: Configure Environment Variables

### Windows (Command Prompt)
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
set AI_PROVIDER=claude
```

### Windows (PowerShell)
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
$env:AI_PROVIDER="claude"
```

### Mac/Linux
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
export AI_PROVIDER="claude"
```

### Using .env file (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your-actual-api-key-here
```

## Step 4: Setup Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

## Step 5: Run Server

```bash
python manage.py runserver
```

The API will be available at: http://localhost:8000/

## Step 6: Test the API

### Test Registration
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"testpass123\", \"role\": \"candidate\"}"
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"testpass123\"}"
```

You should receive access and refresh tokens.

### Test AI Feature (after getting token)
```bash
curl -X POST http://localhost:8000/api/ai/candidate/analyze_resume/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"resume_text\": \"Software Engineer with 5 years of Python experience...\"}"
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate virtual environment or install Django
```bash
pip install django djangorestframework
```

### "ANTHROPIC_API_KEY not found"
**Solution:** Set the environment variable (see Step 3)

### "ImportError: anthropic package not installed"
**Solution:** Install the AI provider package
```bash
pip install anthropic  # for Claude
# or
pip install openai     # for OpenAI
```

### "No migrations to apply"
**Solution:** Create migrations first
```bash
python manage.py makemigrations accounts jobs ai_assistant
python manage.py migrate
```

### Permission denied errors on Windows
**Solution:** Run Command Prompt or PowerShell as Administrator

## Next Steps

1. Read [README.md](README.md) for complete documentation
2. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for all endpoints
3. Explore the Django admin at http://localhost:8000/admin/
4. Test different AI features for each user role

## API Key Pricing (as of 2024)

### Anthropic Claude
- Claude 3.5 Sonnet: $3 per million input tokens, $15 per million output tokens
- Claude 3 Haiku (fast): $0.25 per million input tokens, $1.25 per million output tokens
- Free tier: Credits for testing

### OpenAI
- GPT-4: $30 per million input tokens, $60 per million output tokens
- GPT-3.5 Turbo: $0.50 per million input tokens, $1.50 per million output tokens
- Free tier: $5 credit for new accounts

## Security Best Practices

1. Never commit .env file to git
2. Add .env to .gitignore
3. Use different API keys for development and production
4. Rotate API keys regularly
5. Set spending limits in provider dashboard

## Common Use Cases

### For Candidates
- Analyze resume: `/api/ai/candidate/analyze_resume/`
- Get job matches: `/api/ai/candidate/suggest_jobs/`
- Improve resume: `/api/ai/candidate/resume_feedback/`

### For Recruiters
- Generate job descriptions: `/api/ai/recruiter/generate_job_description/`
- Rank candidates: `/api/ai/recruiter/rank_candidates/`
- Get interview questions: `/api/ai/recruiter/interview_questions/`

### For Admins
- Platform analytics: `/api/ai/admin/platform_analytics/`
- Detect spam: `/api/ai/admin/detect_spam/`
- Trend analysis: `/api/ai/admin/analyze_trends/`

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review error messages carefully
3. Ensure API keys are set correctly
4. Verify all dependencies are installed

Happy coding!
