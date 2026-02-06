# Job Portal Backend - AI-Powered

A Django REST Framework-based job portal with integrated AI assistant capabilities for candidates, recruiters, and admins.

## Project Structure

```
job-portal-backend/
├── accounts/               # User authentication & management
│   ├── models.py          # Custom User model with role-based access
│   ├── views.py           # Registration endpoint
│   ├── serializers.py     # User serializers
│   ├── permissions.py     # Role-based permissions
│   └── urls.py            # Auth URLs
│
├── jobs/                  # Jobs & Applications management
│   ├── models.py          # Job and Application models
│   ├── views.py           # Job and application viewsets
│   ├── serializers.py     # API serializers
│   ├── admin.py           # Django admin configuration
│   └── urls.py            # Job-related URLs
│
├── ai_assistant/          # AI Assistant module
│   ├── models.py          # Conversation, Message, Analytics models
│   ├── views.py           # AI API endpoints
│   ├── serializers.py     # Request/response serializers
│   ├── config.py          # AI configuration
│   ├── admin.py           # Admin interface
│   ├── urls.py            # AI URLs
│   │
│   ├── handlers/          # Role-specific AI handlers
│   │   ├── candidate_handler.py    # Candidate AI features
│   │   ├── recruiter_handler.py    # Recruiter AI features
│   │   └── admin_handler.py        # Admin AI features
│   │
│   └── utils/             # Utility modules
│       ├── ai_client.py            # AI API client (Claude/GPT)
│       └── prompt_templates.py     # Prompt engineering
│
└── config/                # Django project configuration
    ├── settings.py        # Project settings
    ├── urls.py            # Main URL routing
    ├── wsgi.py            # WSGI configuration
    └── asgi.py            # ASGI configuration
```

## Features

### User Roles

1. **Candidates**
   - Apply to jobs
   - Resume analysis
   - Job recommendations
   - Skill gap analysis
   - ATS-optimized resume feedback

2. **Recruiters**
   - Post job listings
   - Manage applications
   - AI-generated job descriptions
   - Candidate ranking
   - Interview question suggestions
   - Resume summarization

3. **Admins**
   - Platform analytics
   - Spam detection
   - User moderation
   - Trend analysis
   - Security monitoring

## API Endpoints

### Authentication
```
POST   /api/token/                    # Login (get JWT tokens)
POST   /api/token/refresh/            # Refresh access token
POST   /api/accounts/register/        # User registration
```

### Jobs & Applications
```
GET    /api/jobs/jobs/                # List jobs
POST   /api/jobs/jobs/                # Create job (recruiter only)
GET    /api/jobs/jobs/{id}/           # Get job details
PUT    /api/jobs/jobs/{id}/           # Update job (recruiter only)
DELETE /api/jobs/jobs/{id}/           # Delete job (recruiter only)
POST   /api/jobs/jobs/{id}/increment_views/     # Track views
GET    /api/jobs/jobs/{id}/applications/        # Get job applications

GET    /api/jobs/applications/        # List applications
POST   /api/jobs/applications/        # Apply to job (candidate only)
GET    /api/jobs/applications/{id}/   # Get application details
PATCH  /api/jobs/applications/{id}/update_status/  # Update status (recruiter)
```

### AI Assistant - Candidate Features
```
POST   /api/ai/candidate/analyze_resume/        # Analyze resume
POST   /api/ai/candidate/suggest_jobs/          # Get job suggestions
POST   /api/ai/candidate/job_match/             # Match with specific job
POST   /api/ai/candidate/resume_feedback/       # Get resume feedback
POST   /api/ai/candidate/recommend_skills/      # Get skill recommendations
GET    /api/ai/candidate/application_status/    # Get application status info
```

### AI Assistant - Recruiter Features
```
POST   /api/ai/recruiter/generate_job_description/  # Generate job description
POST   /api/ai/recruiter/interview_questions/       # Generate interview questions
POST   /api/ai/recruiter/rank_candidates/           # Rank candidates for job
POST   /api/ai/recruiter/summarize_resume/          # Summarize candidate resume
GET    /api/ai/recruiter/hiring_insights/           # Get hiring insights
```

### AI Assistant - Admin Features
```
GET    /api/ai/admin/platform_analytics/        # Platform statistics
POST   /api/ai/admin/detect_spam/               # Detect spam content
GET    /api/ai/admin/suspicious_activities/     # List suspicious activities
POST   /api/ai/admin/recommend_moderation/      # Get moderation recommendations
POST   /api/ai/admin/analyze_trends/            # Analyze platform trends
```

### Conversations (All roles)
```
GET    /api/ai/conversations/                   # List user's conversations
POST   /api/ai/conversations/                   # Create new conversation
GET    /api/ai/conversations/{id}/              # Get conversation details
POST   /api/ai/conversations/{id}/send_message/ # Send message in conversation
```

## Setup Instructions

### Quick Start - FREE Version (No API Key)

The system includes a **FREE mock AI** that works immediately without any API keys!

```bash
cd job-portal-backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

That's it! The system works with mock AI. See [QUICKSTART_FREE.md](QUICKSTART_FREE.md) for details.

### Full Setup with Real AI (Optional)

If you want to use real AI (Claude or OpenAI):

### 1. Install Dependencies

```bash
cd job-portal-backend
pip install -r requirements.txt

# Install AI provider (choose one)
pip install anthropic  # for Claude
# or
pip install openai     # for OpenAI
```

### 2. Configure AI API Keys

Create a `.env` file or set environment variables:

```bash
# For Claude (Anthropic)
export ANTHROPIC_API_KEY="your-api-key-here"
export AI_PROVIDER="claude"

# Or for OpenAI
export OPENAI_API_KEY="your-api-key-here"
export AI_PROVIDER="openai"
```

Alternatively, edit [ai_assistant/config.py](ai_assistant/config.py:4-5) directly (not recommended for production).

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## AI Configuration

### Supported Providers

The system supports multiple AI providers:

1. **Claude (Anthropic)** - Default
   - Models: claude-3-5-sonnet, claude-3-opus, claude-3-haiku
   - Requires: `pip install anthropic`

2. **OpenAI**
   - Models: gpt-4, gpt-4-turbo, gpt-3.5-turbo
   - Requires: `pip install openai`

### Configuration File

Edit [ai_assistant/config.py](ai_assistant/config.py) to customize:

- AI provider and models
- Token limits and temperature
- Rate limiting
- Feature flags
- Analysis thresholds

## Database Models

### User (accounts/models.py)
- Email-based authentication
- Role field: candidate, recruiter, or admin
- JWT token authentication

### Job (jobs/models.py)
- Title, company, description, requirements
- Job type: full_time, part_time, internship, contract
- Status: draft, published, closed
- Salary range, location, remote option
- Recruiter relationship

### Application (jobs/models.py)
- Job and candidate relationship (unique together)
- Resume text, cover letter
- Status tracking
- AI-generated match score and summary

### Conversation (ai_assistant/models.py)
- User's chat sessions with AI
- Title and timestamps

### Message (ai_assistant/models.py)
- Individual chat messages
- Role: user, assistant, system
- Metadata (tokens, model info)

### AIAnalytics (ai_assistant/models.py)
- Usage tracking
- Token consumption
- Response times
- Success/error tracking

## Example API Usage

### Register and Login

```bash
# Register
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepass123",
    "role": "candidate"
  }'

# Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepass123"
  }'
```

### Analyze Resume (Candidate)

```bash
curl -X POST http://localhost:8000/api/ai/candidate/analyze_resume/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 5 years of experience in Python, Django, React..."
  }'
```

### Generate Job Description (Recruiter)

```bash
curl -X POST http://localhost:8000/api/ai/recruiter/generate_job_description/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "position": "Senior Software Engineer",
    "company": "Tech Corp",
    "requirements": "Python, Django, REST APIs, 5+ years experience"
  }'
```

## Security Notes

1. **Never commit API keys** - Always use environment variables
2. **JWT tokens** - Stored in client, not in database
3. **Role-based permissions** - Enforced at view level
4. **Rate limiting** - Configure in ai_assistant/config.py
5. **Input validation** - Handled by DRF serializers

## Next Steps

1. Add API key to environment variables
2. Run migrations to create database tables
3. Create test users with different roles
4. Test AI features with the API
5. Configure CORS if building a frontend
6. Set up proper production deployment

## Dependencies

See [requirements.txt](requirements.txt) for full list.

Key dependencies:
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt
- anthropic (for Claude AI)
- openai (for OpenAI)

## License

MIT License

## Support

For issues or questions, please create an issue in the repository.
