# Quick Start - FREE Version (No API Key Required!)

Your job portal now includes a **100% FREE mock AI** that works immediately without any API keys!

## Start in 3 Steps

### Step 1: Install Dependencies
```bash
cd job-portal-backend
pip install -r requirements.txt
```

Note: The AI packages (anthropic, openai) are commented out - you don't need them!

### Step 2: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Run Server
```bash
python manage.py runserver
```

That's it! The API is running at `http://localhost:8000/`

## No Configuration Needed

The system automatically uses the FREE mock AI when no API keys are configured. You'll see this message when starting:
```
ℹ️  Using FREE Mock AI (no API key required)
```

## Test the Free AI Features

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"test123\", \"role\": \"candidate\"}"
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"test123\"}"
```

Copy the "access" token from the response.

### 3. Test AI Resume Analysis
```bash
curl -X POST http://localhost:8000/api/ai/candidate/analyze_resume/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"resume_text\": \"Software Engineer with 5 years of experience in Python, Django, React, PostgreSQL\"}"
```

You'll get a realistic mock response!

## What Works with Mock AI (Everything!)

### Candidate Features
- Resume analysis ✓
- Job suggestions ✓
- Job matching ✓
- Resume feedback ✓
- Skill recommendations ✓
- Application status info ✓

### Recruiter Features
- Job description generation ✓
- Interview questions ✓
- Candidate ranking ✓
- Resume summarization ✓
- Hiring insights ✓

### Admin Features
- Platform analytics ✓
- Spam detection ✓
- Suspicious activity monitoring ✓
- Moderation recommendations ✓
- Trend analysis ✓

## Mock AI Features

The mock AI provides:
- Realistic, contextual responses
- No cost, no limits
- No API key required
- Perfect for development and testing
- Instant responses
- Realistic token usage simulation

## Example Responses

### Resume Analysis
```json
{
  "skills": ["Python", "Django", "React", "PostgreSQL"],
  "experience_years": 5,
  "strengths": [
    "Strong full-stack development experience",
    "Proven track record of delivering scalable applications"
  ],
  "areas_for_improvement": [
    "Add more quantifiable metrics to achievements"
  ],
  "ats_score": 85
}
```

### Job Match
```json
{
  "match_score": 87,
  "matching_skills": ["Python", "Django", "PostgreSQL"],
  "missing_skills": ["Kubernetes", "Redis"],
  "recommendations": [
    "Strong match! Your Python experience aligns perfectly.",
    "Consider learning Kubernetes to strengthen your DevOps skills."
  ]
}
```

## Switching to Real AI Later

When you're ready to use real AI (Claude or OpenAI):

### Option 1: Environment Variable
```bash
# For Claude
export ANTHROPIC_API_KEY="your-api-key"
export AI_PROVIDER="claude"

# For OpenAI
export OPENAI_API_KEY="your-api-key"
export AI_PROVIDER="openai"
```

### Option 2: Edit Config File
Edit `ai_assistant/config.py`:
```python
AI_PROVIDER = 'claude'  # Change from 'mock' to 'claude' or 'openai'
ANTHROPIC_API_KEY = 'your-api-key-here'
```

### Option 3: .env File
```bash
AI_PROVIDER=claude
ANTHROPIC_API_KEY=your-api-key-here
```

Then install the required package:
```bash
pip install anthropic  # for Claude
# or
pip install openai     # for OpenAI
```

Restart the server and it will automatically use real AI!

## Benefits of Mock AI

### For Development
- Test all features without costs
- No rate limits
- Instant responses
- Deterministic testing

### For Demos
- Show functionality without API keys
- No unexpected costs
- Works offline
- Consistent demo results

### For Learning
- Understand the system architecture
- Test different scenarios
- Build frontend without backend costs
- Practice API integration

## Next Steps

1. **Test all endpoints** - See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. **Create test data** - Add jobs and applications
3. **Build a frontend** - Connect to the API
4. **Deploy** - Works on any hosting platform
5. **Upgrade to real AI** - When you're ready and have budget

## Common Questions

### Q: Is the mock AI good enough for production?
A: No, it's for development and testing. Use real AI for production.

### Q: How do I know if I'm using mock AI?
A: You'll see "Using FREE Mock AI" in the console when the server starts.

### Q: Can I mix mock and real AI?
A: The system uses one or the other. Set `AI_PROVIDER` to switch.

### Q: Are the responses realistic?
A: Yes! The mock provides contextual, realistic responses for testing.

### Q: Can I customize mock responses?
A: Yes! Edit `ai_assistant/utils/mock_ai_client.py`

## Support

Everything works out of the box! No setup, no API keys, no cost.

Start building your job portal now - for FREE!
