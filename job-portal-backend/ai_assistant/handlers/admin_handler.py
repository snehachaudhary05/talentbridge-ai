"""
AI Handler for Admin-specific features
"""
import json
from typing import Dict, List
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from accounts.models import User
from jobs.models import Job, Application
from ..models import AIAnalytics
from ..utils.ai_client import get_ai_client
from ..utils.prompt_templates import get_analysis_prompt, get_system_prompt


class AdminHandler:
    """Handles AI operations for platform admins"""

    def __init__(self, user):
        self.user = user
        self.ai_client = get_ai_client()

    def get_platform_analytics(self, days: int = 30) -> Dict:
        """
        Get comprehensive platform analytics

        Args:
            days: Number of days to analyze

        Returns:
            Dict with platform statistics
        """
        cutoff_date = timezone.now() - timedelta(days=days)

        # User stats
        total_users = User.objects.count()
        new_users = User.objects.filter(date_joined__gte=cutoff_date).count()
        candidates = User.objects.filter(role='candidate').count()
        recruiters = User.objects.filter(role='recruiter').count()

        # Job stats
        total_jobs = Job.objects.count()
        published_jobs = Job.objects.filter(status='published').count()
        new_jobs = Job.objects.filter(created_at__gte=cutoff_date).count()

        # Application stats
        total_applications = Application.objects.count()
        recent_applications = Application.objects.filter(applied_at__gte=cutoff_date).count()

        # AI usage stats
        ai_requests = AIAnalytics.objects.filter(created_at__gte=cutoff_date).count()
        ai_success_rate = AIAnalytics.objects.filter(
            created_at__gte=cutoff_date
        ).aggregate(
            success_rate=Avg('success')
        )['success_rate']

        return {
            'period_days': days,
            'users': {
                'total': total_users,
                'new': new_users,
                'candidates': candidates,
                'recruiters': recruiters
            },
            'jobs': {
                'total': total_jobs,
                'published': published_jobs,
                'new': new_jobs
            },
            'applications': {
                'total': total_applications,
                'recent': recent_applications,
                'avg_per_job': round(total_applications / total_jobs, 2) if total_jobs > 0 else 0
            },
            'ai_usage': {
                'total_requests': ai_requests,
                'success_rate': round(ai_success_rate * 100, 2) if ai_success_rate else 0
            }
        }

    def detect_spam(self, content_type: str, content_id: int) -> Dict:
        """
        Detect spam or suspicious content

        Args:
            content_type: Type of content ('job', 'application', 'user')
            content_id: ID of the content

        Returns:
            Dict with spam detection results
        """
        content_text = self._get_content_for_spam_check(content_type, content_id)

        if not content_text:
            return {'error': 'Content not found'}

        system_prompt = get_analysis_prompt('spam_detection')

        messages = [
            {"role": "user", "content": content_text}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        try:
            spam_result = json.loads(response['content'])
        except json.JSONDecodeError:
            spam_result = {
                'raw_response': response['content']
            }

        return spam_result

    def _get_content_for_spam_check(self, content_type: str, content_id: int) -> str:
        """Get content text for spam checking"""
        try:
            if content_type == 'job':
                job = Job.objects.get(id=content_id)
                return f"""Job Title: {job.title}
Company: {job.company_name}
Description: {job.description}
Requirements: {job.requirements}
"""
            elif content_type == 'application':
                app = Application.objects.get(id=content_id)
                return f"""Cover Letter: {app.cover_letter}
Resume: {app.resume_text[:1000]}
"""
            elif content_type == 'user':
                user = User.objects.get(id=content_id)
                return f"""Email: {user.email}
Name: {user.first_name} {user.last_name}
Role: {user.role}
"""
        except Exception:
            return ""

    def get_suspicious_activities(self, threshold: int = 10) -> List[Dict]:
        """
        Identify suspicious user activities

        Args:
            threshold: Number of actions to consider suspicious

        Returns:
            List of suspicious activities
        """
        cutoff_date = timezone.now() - timedelta(hours=24)

        # Find users with too many applications in short time
        suspicious_candidates = Application.objects.filter(
            applied_at__gte=cutoff_date
        ).values('candidate').annotate(
            app_count=Count('id')
        ).filter(
            app_count__gte=threshold
        )

        # Find recruiters posting too many jobs
        suspicious_recruiters = Job.objects.filter(
            created_at__gte=cutoff_date
        ).values('recruiter').annotate(
            job_count=Count('id')
        ).filter(
            job_count__gte=threshold
        )

        suspicious_activities = []

        for item in suspicious_candidates:
            user = User.objects.get(id=item['candidate'])
            suspicious_activities.append({
                'type': 'excessive_applications',
                'user_id': user.id,
                'user_email': user.email,
                'count': item['app_count'],
                'severity': 'high' if item['app_count'] > threshold * 2 else 'medium'
            })

        for item in suspicious_recruiters:
            user = User.objects.get(id=item['recruiter'])
            suspicious_activities.append({
                'type': 'excessive_job_postings',
                'user_id': user.id,
                'user_email': user.email,
                'count': item['job_count'],
                'severity': 'high' if item['job_count'] > threshold * 2 else 'medium'
            })

        return suspicious_activities

    def recommend_moderation_action(self, user_id: int, reason: str) -> Dict:
        """
        Get AI recommendation for moderation action

        Args:
            user_id: User ID to analyze
            reason: Reason for investigation

        Returns:
            Dict with recommended action
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return {'error': 'User not found'}

        # Gather user activity data
        if user.role == 'candidate':
            applications = Application.objects.filter(candidate=user).count()
            recent_apps = Application.objects.filter(
                candidate=user,
                applied_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            activity_summary = f"Applications: {applications} total, {recent_apps} in last 7 days"

        elif user.role == 'recruiter':
            jobs = Job.objects.filter(recruiter=user).count()
            recent_jobs = Job.objects.filter(
                recruiter=user,
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            activity_summary = f"Jobs posted: {jobs} total, {recent_jobs} in last 7 days"

        else:
            activity_summary = "No specific activity data"

        prompt = f"""Analyze this user and recommend a moderation action:

User ID: {user_id}
Email: {user.email}
Role: {user.role}
Account Age: {(timezone.now() - user.date_joined).days} days

Activity: {activity_summary}

Reason for investigation: {reason}

Provide:
1. Recommended action (none/warning/temporary_suspension/permanent_ban)
2. Confidence level (0-100)
3. Reasoning
4. Additional monitoring suggestions

Format as JSON.
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('admin')
        )

        try:
            recommendation = json.loads(response['content'])
        except json.JSONDecodeError:
            recommendation = {
                'raw_response': response['content']
            }

        return recommendation

    def analyze_trends(self, metric: str = 'all', days: int = 30) -> str:
        """
        Analyze platform trends

        Args:
            metric: Specific metric to analyze or 'all'
            days: Number of days to analyze

        Returns:
            Trend analysis text
        """
        analytics = self.get_platform_analytics(days)

        prompt = f"""Analyze these platform metrics and identify trends:

{json.dumps(analytics, indent=2)}

Provide insights on:
1. Growth patterns
2. User engagement
3. Popular job categories (if data available)
4. Potential issues
5. Recommendations for improvement

Focus on actionable insights.
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('admin')
        )

        return response['content']

    def generate_report(self, report_type: str, parameters: Dict = None) -> str:
        """
        Generate various admin reports

        Args:
            report_type: Type of report to generate
            parameters: Additional parameters for the report

        Returns:
            Generated report text
        """
        parameters = parameters or {}

        if report_type == 'weekly_summary':
            analytics = self.get_platform_analytics(days=7)
            prompt = f"Generate a weekly summary report from this data:\n{json.dumps(analytics, indent=2)}"

        elif report_type == 'security':
            suspicious = self.get_suspicious_activities()
            prompt = f"Generate a security report from these activities:\n{json.dumps(suspicious, indent=2)}"

        elif report_type == 'performance':
            ai_analytics = AIAnalytics.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            )
            avg_response_time = ai_analytics.aggregate(
                avg_time=Avg('response_time_ms')
            )['avg_time']
            prompt = f"Generate a performance report. AI average response time: {avg_response_time}ms"

        else:
            prompt = f"Generate a {report_type} report for the platform"

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = self.ai_client.generate_response(
            messages=messages,
            system_prompt=get_system_prompt('admin')
        )

        return response['content']
