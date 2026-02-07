"""
AI Handler for Candidate-specific features
"""
import json
from typing import Dict, List
from django.db.models import Q

from jobs.models import Job, Application
from ..utils.ai_client import get_ai_client
from ..utils.prompt_templates import get_analysis_prompt, get_system_prompt


class CandidateHandler:
    """Handles AI operations for job candidates"""

    def __init__(self, user):
        self.user = user
        self.ai_client = get_ai_client()

    def analyze_resume(self, resume_text: str) -> Dict:
        """
        Analyze resume and extract structured information

        Args:
            resume_text: The candidate's resume text

        Returns:
            Dict with extracted skills, experience, and recommendations
        """
        system_prompt = get_analysis_prompt('resume_analysis')

        messages = [
            {"role": "user", "content": resume_text}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # Check if response has content
        content = response.get('content', '').strip()
        if not content:
            # Return a helpful error message with more context
            print(f"[ERROR] AI returned empty response. Resume length: {len(resume_text)}, Response: {response}")
            return {
                'analysis': {
                    'error': 'AI returned empty response',
                    'message': 'The AI service did not return any analysis. This usually happens when the input is too large or complex.',
                    'resume_length': len(resume_text),
                    'suggestions': [
                        f'Your resume is {len(resume_text):,} characters. Try reducing it to under 10,000 characters.',
                        'Remove any formatting, tables, or special characters',
                        'Ensure your resume is plain text, not a scanned image',
                        'Try copy-pasting just the text content instead of uploading a file'
                    ],
                    'debug_info': {
                        'response_time_ms': response.get('response_time_ms', 0),
                        'ai_provider': 'openrouter/gemma-3-12b-it:free',
                        'note': 'Free AI models may struggle with large inputs. Consider using a smaller resume or upgrading to a paid AI service.'
                    }
                },
                'usage': response.get('usage', {}),
                'response_time_ms': response.get('response_time_ms', 0)
            }

        # Debug logging
        print(f"[DEBUG] AI Response Length: {len(content)}")
        print(f"[DEBUG] First 500 chars: {content[:500]}")

        # Clean up markdown code blocks if present
        import re
        # Remove ```json ... ``` or ``` ... ``` blocks
        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1).strip()
            print(f"[DEBUG] After markdown removal: {content[:200]}")

        try:
            # Try to parse as JSON
            analysis = json.loads(content)
            print(f"[DEBUG] Parsed JSON type: {type(analysis)}")

            # Handle double-encoded JSON (when AI returns JSON as a string)
            if isinstance(analysis, str):
                try:
                    analysis = json.loads(analysis)
                    print("[DEBUG] Successfully parsed double-encoded JSON")
                except json.JSONDecodeError:
                    # If second parse fails, treat as raw text
                    analysis = {
                        'raw_analysis': analysis,
                        'note': 'AI returned double-encoded text.'
                    }

            # Handle case where analysis is a dict but has raw_analysis as a JSON string
            elif isinstance(analysis, dict) and 'raw_analysis' in analysis:
                raw = analysis.get('raw_analysis', '')
                if isinstance(raw, str) and raw.strip().startswith('{'):
                    try:
                        parsed_raw = json.loads(raw)
                        print("[DEBUG] Found and parsed JSON in raw_analysis field")
                        analysis = parsed_raw
                    except json.JSONDecodeError:
                        print("[DEBUG] raw_analysis contains invalid JSON")
                        pass

        except json.JSONDecodeError:
            # Before giving up, check if content looks like JSON and try to parse it
            content_stripped = content.strip()
            if content_stripped.startswith('{'):
                try:
                    # Try to parse the content directly
                    analysis = json.loads(content_stripped)
                    print("[DEBUG] Successfully parsed JSON from text content in except block")
                except json.JSONDecodeError:
                    # If still fails, wrap as raw_analysis
                    analysis = {
                        'raw_analysis': content,
                        'note': 'AI returned text instead of structured JSON. This is normal for free models.'
                    }
            else:
                # Not JSON-like, wrap as raw_analysis
                analysis = {
                    'raw_analysis': content,
                    'note': 'AI returned text instead of structured JSON. This is normal for free models.'
                }

        # Final check: if we have a dict with raw_analysis containing JSON, extract it
        if isinstance(analysis, dict) and 'raw_analysis' in analysis:
            raw = analysis.get('raw_analysis', '')
            if isinstance(raw, str) and raw.strip().startswith('{'):
                try:
                    parsed_raw = json.loads(raw)
                    print("[DEBUG] Final extraction: Found and parsed JSON in raw_analysis field")
                    analysis = parsed_raw
                except json.JSONDecodeError:
                    print("[DEBUG] Final extraction: raw_analysis contains invalid JSON")
                    pass

        # Log the final structure being returned
        print(f"[DEBUG] Final analysis structure - has key_skills: {'key_skills' in analysis if isinstance(analysis, dict) else False}")
        print(f"[DEBUG] Final analysis structure - has ats_score: {'ats_score' in analysis if isinstance(analysis, dict) else False}")
        print(f"[DEBUG] Final analysis structure - has raw_analysis: {'raw_analysis' in analysis if isinstance(analysis, dict) else False}")

        return {
            'analysis': analysis,
            'usage': response.get('usage', {}),
            'response_time_ms': response.get('response_time_ms', 0)
        }

    def extract_skills(self, resume_text: str) -> List[str]:
        """
        Extract skills from resume text

        Args:
            resume_text: The candidate's resume text

        Returns:
            List of extracted skills
        """
        system_prompt = get_analysis_prompt('skill_extraction')

        messages = [
            {"role": "user", "content": resume_text}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        try:
            skills = json.loads(response['content'])
            if isinstance(skills, list):
                return skills
            elif isinstance(skills, dict) and 'skills' in skills:
                return skills['skills']
        except json.JSONDecodeError:
            pass

        # Fallback: extract from text
        return self._extract_skills_from_text(response['content'])

    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Fallback method to extract skills from text"""
        # Simple extraction - can be enhanced
        import re
        skills = re.findall(r'\b[A-Z][a-zA-Z+#\.]*\b', text)
        return list(set(skills))[:20]  # Return unique skills, max 20

    def suggest_jobs(self, candidate_skills: List[str], limit: int = 10) -> List[Dict]:
        """
        Suggest relevant jobs based on candidate skills

        Args:
            candidate_skills: List of candidate's skills
            limit: Maximum number of jobs to return

        Returns:
            List of job recommendations with match scores
        """
        # Get published jobs
        jobs = Job.objects.filter(status='published')

        recommendations = []

        for job in jobs[:50]:  # Analyze top 50 jobs
            job_skills = [s.strip() for s in job.required_skills.split(',')]

            # Convert to lowercase for case-insensitive matching
            candidate_skills_lower = [s.lower() for s in candidate_skills]
            job_skills_lower = [s.lower() for s in job_skills]

            # Calculate simple match score (case-insensitive)
            matching_skills_lower = set(candidate_skills_lower) & set(job_skills_lower)
            match_score = len(matching_skills_lower) / len(job_skills_lower) if job_skills_lower else 0

            if match_score > 0.3:  # At least 30% match
                # Get the original case for display
                matching_skills_display = [job_skills[job_skills_lower.index(s)] for s in matching_skills_lower]
                missing_skills_display = [job_skills[i] for i, s in enumerate(job_skills_lower) if s not in candidate_skills_lower]

                recommendations.append({
                    'job_id': job.id,
                    'title': job.title,
                    'company': job.company_name,
                    'location': job.location,
                    'match_score': round(match_score * 100, 2),
                    'matching_skills': matching_skills_display,
                    'missing_skills': missing_skills_display
                })

        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        return recommendations[:limit]

    def analyze_job_match(self, resume_text: str, job_id: int) -> Dict:
        """
        Analyze how well a candidate matches a specific job

        Args:
            resume_text: Candidate's resume
            job_id: Job ID to match against

        Returns:
            Dict with match analysis
        """
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return {'error': 'Job not found'}

        context = {
            'job_title': job.title,
            'required_skills': job.required_skills,
            'job_description': job.description,
            'requirements': job.requirements
        }

        system_prompt = get_analysis_prompt('job_match', context)

        messages = [
            {"role": "user", "content": f"Resume:\n{resume_text}"}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # Clean up markdown code blocks if present
        import re
        content = response.get('content', '').strip()
        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1).strip()

        try:
            match_data = json.loads(content)

            # Handle double-encoded JSON (when AI returns JSON as a string)
            if isinstance(match_data, str):
                try:
                    match_data = json.loads(match_data)
                except json.JSONDecodeError:
                    # If second parse fails, treat as raw text
                    match_data = {
                        'raw_response': match_data
                    }
        except json.JSONDecodeError:
            match_data = {
                'raw_response': content
            }

        return match_data

    def get_resume_feedback(self, resume_text: str) -> Dict:
        """
        Get ATS-focused resume improvement feedback

        Args:
            resume_text: Candidate's resume

        Returns:
            Dict with improvement suggestions
        """
        system_prompt = get_analysis_prompt('resume_improvement')

        messages = [
            {"role": "user", "content": resume_text}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        return {
            'feedback': response['content'],
            'usage': response.get('usage', {}),
            'response_time_ms': response.get('response_time_ms', 0)
        }

    def recommend_skills(self, current_skills: List[str], target_role: str) -> Dict:
        """
        Recommend skills to learn for a target role

        Args:
            current_skills: List of candidate's current skills
            target_role: The role they're targeting

        Returns:
            Dict with skill recommendations
        """
        prompt = f"""Given a candidate with these skills: {', '.join(current_skills)}

They want to pursue a role as: {target_role}

Recommend 5-7 skills they should learn. For each skill provide:
- skill: The skill name
- priority: High, Medium, or Low
- reason: Brief explanation of why this skill is important
- timeline: Estimated learning timeline

IMPORTANT: Return ONLY a JSON array. Example format:
[
  {{
    "skill": "Docker",
    "priority": "High",
    "reason": "Containerization is essential for modern deployments",
    "timeline": "2-4 weeks"
  }},
  {{
    "skill": "AWS",
    "priority": "Medium",
    "reason": "Cloud knowledge is valuable for scalability",
    "timeline": "6-8 weeks"
  }}
]

Return ONLY the JSON array, no other text."""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('candidate')
        )

        # Check for AI client errors
        if not response.get('success', True) or 'error' in response:
            error_msg = response.get('error', 'Unknown error')
            print(f"[ERROR] AI client error in skill recommendations: {error_msg}")
            return {
                'raw_response': '',
                'note': f'AI service error: {error_msg}. Please try again.'
            }

        # Clean up markdown code blocks if present
        import re
        content = response.get('content', '').strip()

        # Debug logging
        print(f"[DEBUG SKILLS] AI Response Length: {len(content)}")
        print(f"[DEBUG SKILLS] First 500 chars: {content[:500]}")

        # Check for empty response
        if not content:
            print("[ERROR] AI returned empty response for skill recommendations")
            return {
                'raw_response': '',
                'note': 'AI returned an empty response. Please try again with different skills or role.'
            }

        json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1).strip()
            print(f"[DEBUG SKILLS] After markdown removal: {content[:200]}")

        try:
            recommendations = json.loads(content)
            print(f"[DEBUG SKILLS] Parsed JSON type: {type(recommendations)}")

            # Handle double-encoded JSON (when AI returns JSON as a string)
            if isinstance(recommendations, str):
                try:
                    recommendations = json.loads(recommendations)
                except json.JSONDecodeError:
                    # If second parse fails, treat as raw text
                    recommendations = {
                        'raw_response': recommendations,
                        'note': 'AI returned double-encoded text.'
                    }
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing failed: {str(e)}")
            print(f"[ERROR] Content that failed to parse: {content[:200]}")
            recommendations = {
                'raw_response': content if content else '(empty)',
                'note': f'AI returned text format. Results may not be structured. Error: {str(e)}'
            }

        return recommendations

    def get_application_status_info(self, application_id: int) -> str:
        """
        Get information about application status

        Args:
            application_id: Application ID

        Returns:
            Explanation of current status
        """
        try:
            application = Application.objects.get(
                id=application_id,
                candidate=self.user
            )
        except Application.DoesNotExist:
            return "Application not found or you don't have access to it."

        status_explanations = {
            'applied': "Your application has been submitted and is waiting for review.",
            'under_review': "The recruiter is currently reviewing your application.",
            'shortlisted': "Great news! You've been shortlisted. The recruiter may contact you soon.",
            'interview_scheduled': "An interview has been scheduled. Check your email for details.",
            'rejected': "Unfortunately, your application wasn't selected for this position.",
            'accepted': "Congratulations! Your application has been accepted."
        }

        status_text = status_explanations.get(
            application.status,
            "Status information not available."
        )

        return f"""Application Status for: {application.job.title}
Company: {application.job.company_name}
Status: {application.get_status_display()}

{status_text}

Applied on: {application.applied_at.strftime('%B %d, %Y')}
"""
