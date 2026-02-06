"""
Prompt templates for different AI assistant tasks
"""

# System prompts for different user roles
CANDIDATE_SYSTEM_PROMPT = """You are an AI career assistant helping job candidates. Your capabilities include:
- Analyzing resumes and extracting skills
- Suggesting relevant jobs based on candidate profile
- Recommending missing skills for target roles
- Providing ATS-optimized resume feedback
- Answering application status queries

Be professional, encouraging, and actionable. Focus on helping candidates improve their job search."""

RECRUITER_SYSTEM_PROMPT = """You are an AI hiring assistant helping recruiters. Your capabilities include:
- Generating optimized job descriptions
- Suggesting interview questions based on job requirements
- Ranking candidates based on skill match
- Summarizing candidate resumes
- Providing hiring best practices

Be professional, objective, and data-driven. Focus on helping recruiters make better hiring decisions."""

ADMIN_SYSTEM_PROMPT = """You are an AI admin assistant for a job portal platform. Your capabilities include:
- Summarizing platform analytics
- Detecting suspicious or spam activities
- Recommending actions for user/job moderation
- Identifying trends and patterns

Be analytical, security-conscious, and precise. Focus on platform health and safety."""


def get_system_prompt(user_role: str) -> str:
    """Get system prompt based on user role"""
    prompts = {
        'candidate': CANDIDATE_SYSTEM_PROMPT,
        'recruiter': RECRUITER_SYSTEM_PROMPT,
        'admin': ADMIN_SYSTEM_PROMPT
    }
    return prompts.get(user_role, CANDIDATE_SYSTEM_PROMPT)


def get_analysis_prompt(analysis_type: str, context: dict = None) -> str:
    """Get prompt for specific analysis tasks"""
    context = context or {}

    prompts = {
        'resume_analysis': """Analyze the provided resume and provide comprehensive feedback.

Extract and analyze:
1. Key skills (technical and soft skills)
2. Years of experience
3. Education background
4. Notable achievements
5. Career summary/objective quality

Provide detailed feedback on:
6. ATS compatibility score (0-100) with explanation
7. Formatting and structure issues
8. Missing keywords and sections
9. Weak action verbs to strengthen
10. Specific, actionable improvements for each section
11. Overall strengths and areas for improvement

Format your response as structured JSON with fields:
- key_skills: {technical_skills: [], soft_skills: []}
- years_of_experience: string
- education_background: array
- notable_achievements: array
- ats_score: number (0-100)
- formatting_feedback: array of specific issues
- content_feedback: array of specific improvements
- keyword_suggestions: array of missing keywords
- action_verb_improvements: array of weak verbs to replace
- overall_strengths: array
- areas_for_improvement: array with detailed explanations
- recommendation_summary: string (2-3 sentences)

Be specific and actionable with all feedback.""",

        'skill_extraction': """Extract all technical and professional skills from the resume.
Return a JSON array of skills with categories (e.g., programming, tools, soft skills).""",

        'job_match': f"""Compare this candidate's profile with the following job requirements:

Job Title: {context.get('job_title', 'N/A')}
Required Skills: {context.get('required_skills', 'N/A')}
Job Description: {context.get('job_description', 'N/A')}

Calculate a match score (0-100) and explain:
1. Matching skills
2. Missing skills
3. Recommendations for the candidate

Format as JSON with: match_score, matching_skills, missing_skills, recommendations.""",

        'resume_improvement': """Review this resume and provide ATS-optimization feedback:
1. Formatting issues
2. Missing keywords
3. Weak action verbs to strengthen
4. Sections to add or improve
5. Overall ATS compatibility score (0-100)

Be specific and actionable.""",

        'job_description': f"""Generate a compelling job description for:

Position: {context.get('position', 'N/A')}
Company: {context.get('company', 'N/A')}
Requirements: {context.get('requirements', 'N/A')}

Include:
1. Engaging overview
2. Key responsibilities
3. Required qualifications
4. Nice-to-have skills
5. Company culture highlights

Keep it concise and ATS-friendly.""",

        'interview_questions': f"""Generate 5-7 interview questions for:

Role: {context.get('role', 'N/A')}
Level: {context.get('level', 'Entry/Mid/Senior')}
Key Skills: {context.get('skills', 'N/A')}

Include:
1. Technical questions (if applicable)
2. Behavioral questions
3. Situational questions

Provide both questions and what to look for in answers.""",

        'candidate_summary': """Summarize this candidate's profile in 3-5 bullet points:
- Key strengths
- Relevant experience
- Notable achievements
- Fit for typical roles

Keep it concise and highlight standout qualities.""",

        'spam_detection': """Analyze this content for spam or suspicious activity:
1. Is it likely spam? (Yes/No)
2. Confidence level (0-100)
3. Red flags identified
4. Recommended action (approve/flag/block)

Format as JSON."""
    }

    return prompts.get(analysis_type, "Analyze the provided content and respond professionally.")


def format_conversation_history(messages: list, max_history: int = 10) -> list:
    """
    Format conversation history for AI context

    Args:
        messages: List of Message model instances
        max_history: Maximum number of messages to include

    Returns:
        List of formatted message dicts
    """
    recent_messages = messages[-max_history:] if len(messages) > max_history else messages

    formatted = []
    for msg in recent_messages:
        if msg.role in ['user', 'assistant']:
            formatted.append({
                'role': msg.role,
                'content': msg.content
            })

    return formatted
