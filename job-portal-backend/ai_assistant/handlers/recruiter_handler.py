"""
AI Handler for Recruiter-specific features
"""
import json
from typing import Dict, List
from django.db.models import Q, Count

from jobs.models import Job, Application
from ..utils.ai_client import get_ai_client
from ..utils.prompt_templates import get_analysis_prompt, get_system_prompt


class RecruiterHandler:
    """Handles AI operations for recruiters"""

    def __init__(self, user):
        self.user = user
        self.ai_client = get_ai_client()

    def generate_job_description(self, job_data: Dict) -> str:
        """
        Generate an optimized job description

        Args:
            job_data: Dict containing position, company, requirements

        Returns:
            Generated job description
        """
        context = {
            'position': job_data.get('position', ''),
            'company': job_data.get('company', ''),
            'requirements': job_data.get('requirements', '')
        }

        system_prompt = get_analysis_prompt('job_description', context)

        prompt = f"""Generate a job description with these details:

Position: {context['position']}
Company: {context['company']}
Requirements: {context['requirements']}

Additional context: {job_data.get('additional_context', 'N/A')}
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # Check if AI response was successful
        if not response.get('success', False):
            error_msg = response.get('error', 'Unknown error occurred')
            raise Exception(f"AI job description generation failed: {error_msg}")

        if not response.get('content'):
            raise Exception("AI returned empty response")

        return response['content']

    def generate_interview_questions(self, role: str, skills: str, count: int = 10) -> Dict:
        """
        Generate interview questions based on role and skills

        Args:
            role: Job role/title
            skills: Required skills (comma-separated)
            count: Number of questions to generate

        Returns:
            Dict with interview questions
        """
        context = {
            'role': role,
            'skills': skills,
            'count': count
        }

        system_prompt = get_analysis_prompt('interview_questions', context)

        prompt = f"""Generate exactly {count} interview questions for this role:

Role: {role}
Key Skills: {skills}

Please generate a mix of:
- Technical questions to assess the required skills
- Behavioral questions to evaluate soft skills
- Scenario-based questions for problem-solving

Format the response as a numbered list."""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # Check if AI response was successful
        if not response.get('success', False):
            error_msg = response.get('error', 'Unknown error occurred')
            raise Exception(f"AI question generation failed: {error_msg}")

        if not response.get('content'):
            raise Exception("AI returned empty response")

        return {
            'role': role,
            'skills': skills,
            'count': count,
            'questions': response['content']
        }

    def screen_candidate(self, job_requirements: str, resume_text: str) -> Dict:
        """
        Screen a candidate against job requirements

        Args:
            job_requirements: Job requirements and skills needed
            resume_text: Candidate's resume text

        Returns:
            Dict with screening analysis
        """
        system_prompt = """You are an expert recruiter analyzing candidate resumes.
Evaluate the candidate's qualifications against the job requirements.
Provide a comprehensive, well-structured analysis."""

        prompt = f"""Analyze this candidate for the following position:

**JOB REQUIREMENTS:**
{job_requirements}

**CANDIDATE RESUME:**
{resume_text}

Provide a detailed screening analysis with these sections:

**Overall Match Assessment (Score: X/100)**
Brief overview of how well the candidate matches the requirements

**Key Strengths**
- Strength 1
- Strength 2
- Strength 3
(List 3-5 major strengths with specific examples)

**Relevant Experience & Achievements**
Detailed assessment of their experience level, key projects, and accomplishments

**Skills Analysis**

✅ Required Skills Met:
- Skill 1
- Skill 2
- Skill 3

⚠️ Skills Gaps:
- Missing skill 1
- Skill to develop 2

**Areas of Concern**
- Concern 1 (if any)
- Concern 2 (if any)

**Cultural Fit & Soft Skills**
Assessment of teamwork, leadership, communication abilities

**Recommendation:** [Strong Yes / Yes / Maybe / No]

**Next Steps:**
Clear recommendation on how to proceed with this candidate

Use clear headers, bullet points, and emojis for visual appeal. Be thorough and specific."""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # Check if AI response was successful
        if not response.get('success', False):
            error_msg = response.get('error', 'Unknown error occurred')
            raise Exception(f"AI analysis failed: {error_msg}")

        if not response.get('content'):
            raise Exception("AI returned empty response")

        return {
            'job_requirements': job_requirements,
            'analysis': response['content']
        }

    def rank_candidates(self, job_id: int) -> List[Dict]:
        """
        Rank candidates for a job based on skill match

        Args:
            job_id: Job ID

        Returns:
            List of ranked candidates with scores
        """
        try:
            job = Job.objects.get(id=job_id, recruiter=self.user)
        except Job.DoesNotExist:
            return []

        applications = Application.objects.filter(job=job).select_related('candidate')

        job_skills = set([s.strip().lower() for s in job.required_skills.split(',')])

        ranked_candidates = []

        for application in applications:
            # Extract skills from resume (simplified)
            resume_words = set(application.resume_text.lower().split())

            # Calculate match
            matching_skills = job_skills & resume_words
            match_score = (len(matching_skills) / len(job_skills) * 100) if job_skills else 0

            # Update application with match score if not already set
            if application.skill_match_score is None:
                application.skill_match_score = match_score
                application.save(update_fields=['skill_match_score'])

            ranked_candidates.append({
                'application_id': application.id,
                'candidate_email': application.candidate.email,
                'candidate_name': f"{application.candidate.first_name} {application.candidate.last_name}",
                'match_score': round(match_score, 2),
                'status': application.status,
                'applied_at': application.applied_at.isoformat()
            })

        # Sort by match score
        ranked_candidates.sort(key=lambda x: x['match_score'], reverse=True)

        return ranked_candidates

    def summarize_resume(self, application_id: int) -> Dict:
        """
        Generate a concise summary of a candidate's resume

        Args:
            application_id: Application ID

        Returns:
            Dict with resume summary
        """
        try:
            application = Application.objects.get(
                id=application_id,
                job__recruiter=self.user
            )
        except Application.DoesNotExist:
            return {'error': 'Application not found or you do not have access'}

        system_prompt = get_analysis_prompt('candidate_summary')

        messages = [
            {"role": "user", "content": application.resume_text}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        summary = response['content']

        # Save summary to application if not already present
        if not application.ai_summary:
            application.ai_summary = summary
            application.save(update_fields=['ai_summary'])

        return {
            'candidate_email': application.candidate.email,
            'summary': summary,
            'application_id': application.id,
            'job_title': application.job.title
        }

    def get_hiring_insights(self, job_id: int = None) -> Dict:
        """
        Get hiring insights and statistics

        Args:
            job_id: Optional specific job ID, or all jobs if None

        Returns:
            Dict with insights
        """
        jobs_query = Job.objects.filter(recruiter=self.user)

        if job_id:
            jobs_query = jobs_query.filter(id=job_id)

        total_jobs = jobs_query.count()
        total_applications = Application.objects.filter(job__recruiter=self.user).count()

        if job_id:
            job = jobs_query.first()
            if not job:
                return {'error': 'Job not found'}

            applications = Application.objects.filter(job=job)

            status_breakdown = applications.values('status').annotate(count=Count('status'))

            return {
                'job_title': job.title,
                'total_applications': applications.count(),
                'status_breakdown': list(status_breakdown),
                'average_match_score': applications.filter(
                    skill_match_score__isnull=False
                ).aggregate(
                    avg_score=models.Avg('skill_match_score')
                )['avg_score']
            }

        # Overall insights
        return {
            'total_jobs_posted': total_jobs,
            'total_applications_received': total_applications,
            'average_applications_per_job': round(total_applications / total_jobs, 2) if total_jobs > 0 else 0,
            'active_jobs': jobs_query.filter(status='published').count(),
            'closed_jobs': jobs_query.filter(status='closed').count()
        }

    def suggest_improvements(self, job_id: int) -> str:
        """
        Suggest improvements for a job posting

        Args:
            job_id: Job ID

        Returns:
            Improvement suggestions
        """
        try:
            job = Job.objects.get(id=job_id, recruiter=self.user)
        except Job.DoesNotExist:
            return "Job not found or you do not have access"

        applications_count = job.applications.count()
        views_count = job.views_count

        prompt = f"""Analyze this job posting and suggest improvements:

Title: {job.title}
Description: {job.description}
Requirements: {job.requirements}
Required Skills: {job.required_skills}

Statistics:
- Views: {views_count}
- Applications: {applications_count}
- Application Rate: {(applications_count/views_count*100) if views_count > 0 else 0:.2f}%

Provide specific suggestions to:
1. Improve visibility
2. Attract more qualified candidates
3. Clarify requirements
4. Optimize for ATS
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('recruiter')
        )

        return response['content']

    def compare_candidates(self, application_ids: List[int]) -> str:
        """
        Compare multiple candidates side by side

        Args:
            application_ids: List of application IDs to compare

        Returns:
            Comparison analysis
        """
        applications = Application.objects.filter(
            id__in=application_ids,
            job__recruiter=self.user
        ).select_related('candidate', 'job')

        if applications.count() < 2:
            return "Need at least 2 applications to compare"

        candidates_data = []
        for app in applications:
            candidates_data.append(f"""
Candidate {app.id}:
Email: {app.candidate.email}
Match Score: {app.skill_match_score or 'Not calculated'}
Resume: {app.resume_text[:500]}...
""")

        prompt = f"""Compare these candidates and provide:
1. Key strengths of each
2. Best fit for the role: {applications.first().job.title}
3. Recommended ranking
4. What to focus on in interviews

{chr(10).join(candidates_data)}
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('recruiter')
        )

        return response['content']
