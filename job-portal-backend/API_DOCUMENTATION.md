# Job Portal API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints (except registration and login) require JWT authentication.

Include the access token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Response Format

All responses follow this structure:

**Success:**
```json
{
  "data": { ... },
  "status": "success"
}
```

**Error:**
```json
{
  "error": "Error message",
  "detail": "Detailed error description"
}
```

---

## 1. Authentication Endpoints

### Register User
```http
POST /api/accounts/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "candidate"  // Options: candidate, recruiter
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "candidate"
}
```

### Login
```http
POST /api/token/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```http
POST /api/token/refresh/
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 2. Jobs Endpoints

### List Jobs
```http
GET /api/jobs/jobs/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "company_name": "Tech Corp",
    "job_type": "full_time",
    "location": "San Francisco, CA",
    "is_remote": true,
    "salary_min": 120000,
    "salary_max": 180000,
    "status": "published",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Create Job (Recruiter only)
```http
POST /api/jobs/jobs/
```

**Request Body:**
```json
{
  "title": "Senior Python Developer",
  "company_name": "Tech Corp",
  "description": "We are looking for...",
  "requirements": "5+ years Python, Django, REST APIs",
  "responsibilities": "Design and implement features...",
  "job_type": "full_time",
  "location": "San Francisco, CA",
  "is_remote": true,
  "salary_min": 120000,
  "salary_max": 180000,
  "required_skills": "Python, Django, PostgreSQL, Docker",
  "status": "published",
  "deadline": "2024-12-31T23:59:59Z"
}
```

### Get Job Details
```http
GET /api/jobs/jobs/{id}/
```

### Update Job (Recruiter only)
```http
PUT /api/jobs/jobs/{id}/
```

### Delete Job (Recruiter only)
```http
DELETE /api/jobs/jobs/{id}/
```

### Get Job Applications (Recruiter only)
```http
GET /api/jobs/jobs/{id}/applications/
```

---

## 3. Application Endpoints

### List Applications
```http
GET /api/jobs/applications/
```
- Candidates see their own applications
- Recruiters see applications for their jobs

### Apply to Job (Candidate only)
```http
POST /api/jobs/applications/
```

**Request Body:**
```json
{
  "job": 1,
  "cover_letter": "I am excited to apply...",
  "resume_text": "Full resume text here...",
  "resume_file_url": "https://example.com/resume.pdf"
}
```

### Update Application Status (Recruiter only)
```http
PATCH /api/jobs/applications/{id}/update_status/
```

**Request Body:**
```json
{
  "status": "shortlisted"
}
```

Status options: `applied`, `under_review`, `shortlisted`, `interview_scheduled`, `rejected`, `accepted`

---

## 4. AI Assistant - Candidate Features

### Analyze Resume
```http
POST /api/ai/candidate/analyze_resume/
```

**Request Body:**
```json
{
  "resume_text": "Software Engineer with 5 years experience in Python, Django, React..."
}
```

**Response:**
```json
{
  "analysis": {
    "skills": ["Python", "Django", "React"],
    "experience_years": 5,
    "education": "Bachelor's in Computer Science",
    "strengths": ["Full-stack development", "Problem-solving"],
    "areas_for_improvement": ["Add quantifiable achievements"]
  },
  "usage": {
    "input_tokens": 250,
    "output_tokens": 150
  }
}
```

### Get Job Suggestions
```http
POST /api/ai/candidate/suggest_jobs/
```

**Request Body (Option 1 - with resume):**
```json
{
  "resume_text": "Your resume text...",
  "limit": 10
}
```

**Request Body (Option 2 - with skills):**
```json
{
  "skills": ["Python", "Django", "React"],
  "limit": 10
}
```

**Response:**
```json
{
  "skills_used": ["Python", "Django", "React"],
  "recommendations": [
    {
      "job_id": 1,
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "match_score": 85.5,
      "matching_skills": ["Python", "Django"],
      "missing_skills": ["Docker", "Kubernetes"]
    }
  ]
}
```

### Match with Specific Job
```http
POST /api/ai/candidate/job_match/
```

**Request Body:**
```json
{
  "resume_text": "Your resume...",
  "job_id": 1
}
```

**Response:**
```json
{
  "match_score": 85,
  "matching_skills": ["Python", "Django", "PostgreSQL"],
  "missing_skills": ["Docker", "Kubernetes"],
  "recommendations": "Consider learning Docker to strengthen your candidacy..."
}
```

### Get Resume Feedback
```http
POST /api/ai/candidate/resume_feedback/
```

**Request Body:**
```json
{
  "resume_text": "Your resume..."
}
```

**Response:**
```json
{
  "feedback": "Your resume can be improved by:\n1. Adding quantifiable achievements\n2. Using stronger action verbs...",
  "usage": {...}
}
```

### Get Skill Recommendations
```http
POST /api/ai/candidate/recommend_skills/
```

**Request Body:**
```json
{
  "current_skills": ["Python", "Django", "REST APIs"],
  "target_role": "Senior Backend Engineer"
}
```

**Response:**
```json
{
  "recommended_skills": [
    {
      "skill": "Docker",
      "priority": "High",
      "reason": "Essential for modern deployment",
      "timeline": "2-3 weeks"
    }
  ]
}
```

### Get Application Status Info
```http
GET /api/ai/candidate/application_status/?application_id=1
```

---

## 5. AI Assistant - Recruiter Features

### Generate Job Description
```http
POST /api/ai/recruiter/generate_job_description/
```

**Request Body:**
```json
{
  "position": "Senior Backend Engineer",
  "company": "Tech Startup Inc",
  "requirements": "5+ years Python, Django, microservices",
  "additional_context": "Fast-paced startup, equity offered"
}
```

**Response:**
```json
{
  "job_description": "We are seeking a talented Senior Backend Engineer..."
}
```

### Generate Interview Questions
```http
POST /api/ai/recruiter/interview_questions/
```

**Request Body:**
```json
{
  "job_id": 1
}
```

**Response:**
```json
{
  "questions": [
    {
      "category": "Technical",
      "question": "Explain how you would design a scalable REST API",
      "what_to_look_for": "Understanding of REST principles, scalability considerations"
    }
  ]
}
```

### Rank Candidates
```http
POST /api/ai/recruiter/rank_candidates/
```

**Request Body:**
```json
{
  "job_id": 1
}
```

**Response:**
```json
{
  "ranked_candidates": [
    {
      "application_id": 5,
      "candidate_email": "john@example.com",
      "candidate_name": "John Doe",
      "match_score": 92.5,
      "status": "applied",
      "applied_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Summarize Resume
```http
POST /api/ai/recruiter/summarize_resume/
```

**Request Body:**
```json
{
  "application_id": 5
}
```

**Response:**
```json
{
  "candidate_email": "john@example.com",
  "summary": "- 7 years of backend development\n- Strong Python and Django expertise\n- Led team of 5 developers",
  "application_id": 5,
  "job_title": "Senior Python Developer"
}
```

### Get Hiring Insights
```http
GET /api/ai/recruiter/hiring_insights/?job_id=1
```

**Response:**
```json
{
  "job_title": "Senior Python Developer",
  "total_applications": 45,
  "status_breakdown": [
    {"status": "applied", "count": 20},
    {"status": "under_review", "count": 15},
    {"status": "shortlisted", "count": 10}
  ],
  "average_match_score": 68.5
}
```

---

## 6. AI Assistant - Admin Features

### Get Platform Analytics
```http
GET /api/ai/admin/platform_analytics/?days=30
```

**Response:**
```json
{
  "period_days": 30,
  "users": {
    "total": 1250,
    "new": 85,
    "candidates": 950,
    "recruiters": 300
  },
  "jobs": {
    "total": 450,
    "published": 320,
    "new": 45
  },
  "applications": {
    "total": 3200,
    "recent": 280,
    "avg_per_job": 7.1
  }
}
```

### Detect Spam
```http
POST /api/ai/admin/detect_spam/
```

**Request Body:**
```json
{
  "content_type": "job",  // Options: job, application, user
  "content_id": 123
}
```

**Response:**
```json
{
  "is_spam": true,
  "confidence": 85,
  "red_flags": ["Suspicious keywords", "Unusual pattern"],
  "recommended_action": "block"
}
```

### Get Suspicious Activities
```http
GET /api/ai/admin/suspicious_activities/?threshold=10
```

**Response:**
```json
{
  "activities": [
    {
      "type": "excessive_applications",
      "user_id": 42,
      "user_email": "suspicious@example.com",
      "count": 25,
      "severity": "high"
    }
  ]
}
```

### Recommend Moderation Action
```http
POST /api/ai/admin/recommend_moderation/
```

**Request Body:**
```json
{
  "user_id": 42,
  "reason": "Multiple spam job postings reported"
}
```

**Response:**
```json
{
  "recommended_action": "temporary_suspension",
  "confidence": 85,
  "reasoning": "User has posted 15 jobs in 24 hours, all flagged as spam",
  "monitoring_suggestions": "Monitor for 7 days after suspension"
}
```

### Analyze Trends
```http
POST /api/ai/admin/analyze_trends/
```

**Request Body:**
```json
{
  "metric": "all",
  "days": 30
}
```

**Response:**
```json
{
  "analysis": "Platform growth trends:\n1. User signups increased 15% MoM\n2. Job postings concentrated in tech sector..."
}
```

---

## 7. Conversation Endpoints

### List Conversations
```http
GET /api/ai/conversations/
```

### Create Conversation
```http
POST /api/ai/conversations/
```

**Request Body:**
```json
{
  "title": "Resume help discussion"
}
```

### Get Conversation
```http
GET /api/ai/conversations/{id}/
```

### Send Message
```http
POST /api/ai/conversations/{id}/send_message/
```

**Request Body:**
```json
{
  "message": "How can I improve my resume?"
}
```

**Response:**
```json
{
  "message": "Here are some tips to improve your resume...",
  "conversation_id": 1,
  "usage": {
    "input_tokens": 50,
    "output_tokens": 200
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Default limits (configured in ai_assistant/config.py):
- 60 requests per minute
- 1000 requests per day

---

## Testing with cURL

Example: Analyze resume as a candidate
```bash
# 1. Register
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "pass123", "role": "candidate"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "pass123"}' \
  | jq -r '.access')

# 3. Use AI feature
curl -X POST http://localhost:8000/api/ai/candidate/analyze_resume/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Software Engineer with 5 years Python experience..."}'
```

---

## Need Help?

Contact support or check the README.md for more information.
