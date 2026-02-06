import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ResendEmailService:
    """
    Email service using Resend API
    Handles all email sending for notifications
    """

    def __init__(self):
        self.api_key = settings.RESEND_API_KEY
        self.from_email = settings.EMAIL_FROM
        self.from_name = settings.EMAIL_FROM_NAME
        self.api_url = "https://api.resend.com/emails"
        # Force all test emails to Resend account owner email
        self.test_email_override = "chaudharysneha693@gmail.com"

    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send email using Resend API

        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML email content
            text_content (str): Plain text fallback (optional)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.api_key:
            logger.warning("Resend API key not configured. Email not sent.")
            return False

        # Override recipient for Resend testing (free tier limitation)
        # All emails will go to Resend account owner
        actual_recipient = self.test_email_override
        logger.info(f"Email intended for: {to_email}, sending to: {actual_recipient}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [actual_recipient],
            "subject": f"[For: {to_email}] {subject}",  # Include intended recipient in subject
            "html": html_content,
        }

        if text_content:
            payload["text"] = text_content

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(
                    f"Failed to send email to {to_email}. "
                    f"Status: {response.status_code}, "
                    f"Response: {response.text}"
                )
                return False

        except requests.RequestException as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

    def send_application_submitted_email(self, user, job_title, application_id):
        """Send email when candidate submits an application"""
        subject = f"Application Submitted - {job_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                          border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Application Submitted Successfully!</h1>
                </div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>Your application for <strong>{job_title}</strong> has been submitted successfully!</p>
                    <p>The recruiter will review your application and get back to you soon.</p>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Application Status</a>
                    <p>Good luck! 🚀</p>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(user.email, subject, html_content)

    def send_application_status_changed_email(self, user, job_title, old_status, new_status, application_id):
        """Send email when application status changes"""
        subject = f"Application Status Update - {job_title}"

        # Status emojis
        status_emoji = {
            'Under Review': '👀',
            'Shortlisted': '⭐',
            'OA Round': '📝',
            'Tech Round': '💻',
            'HR Round': '🤝',
            'Offer Received': '🎉',
            'Rejected': '😔',
            'Accepted': '✅'
        }

        emoji = status_emoji.get(new_status, '📬')

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .status-box {{ background: white; padding: 20px; border-left: 4px solid #667eea;
                              margin: 20px 0; border-radius: 5px; }}
                .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                          border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{emoji} Application Status Updated</h1>
                </div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>Your application for <strong>{job_title}</strong> has been updated.</p>
                    <div class="status-box">
                        <p><strong>New Status:</strong> {new_status}</p>
                    </div>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Details</a>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(user.email, subject, html_content)

    def send_new_application_email(self, recruiter, candidate_name, job_title, application_id):
        """Send email to recruiter when they receive a new application"""
        subject = f"New Application Received - {job_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .candidate-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                          border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📬 New Application Received!</h1>
                </div>
                <div class="content">
                    <p>Hi {recruiter.first_name or recruiter.email.split('@')[0]},</p>
                    <p>You have received a new application for <strong>{job_title}</strong>.</p>
                    <div class="candidate-box">
                        <p><strong>Candidate:</strong> {candidate_name}</p>
                    </div>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">Review Application</a>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(recruiter.email, subject, html_content)

    def send_job_match_email(self, user, job_title, company, job_id):
        """Send email when a new job matches candidate's profile"""
        subject = f"New Job Match: {job_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .job-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                          border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Perfect Job Match Found!</h1>
                </div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>We found a job that matches your profile!</p>
                    <div class="job-box">
                        <h3>{job_title}</h3>
                        <p><strong>Company:</strong> {company}</p>
                    </div>
                    <a href="{settings.FRONTEND_URL}/jobs/{job_id}" class="button">View Job</a>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(user.email, subject, html_content)

    def send_interview_scheduled_email(self, candidate, job_title, interview_datetime, interview_type, location, notes=""):
        """Send email to candidate when interview is scheduled"""
        from datetime import datetime

        # Format datetime
        dt = interview_datetime
        formatted_date = dt.strftime("%A, %B %d, %Y")
        formatted_time = dt.strftime("%I:%M %p")

        # Interview type display
        type_emoji = {
            'phone': '📞',
            'video': '🎥',
            'in_person': '🏢'
        }.get(interview_type, '📅')

        type_display = interview_type.replace('_', ' ').title()

        subject = f"Interview Scheduled - {job_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .interview-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px;
                                 border-left: 4px solid #10b981; }}
                .detail-row {{ display: flex; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
                .detail-label {{ font-weight: bold; width: 150px; }}
                .button {{ background: #10b981; color: white; padding: 12px 30px; text-decoration: none;
                          border-radius: 5px; display: inline-block; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{type_emoji} Interview Scheduled!</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate.first_name or candidate.email.split('@')[0]},</p>
                    <p>Great news! Your interview for <strong>{job_title}</strong> has been scheduled.</p>

                    <div class="interview-box">
                        <h3>Interview Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Date:</span>
                            <span>{formatted_date}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Time:</span>
                            <span>{formatted_time}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Type:</span>
                            <span>{type_display}</span>
                        </div>
                        {"<div class='detail-row'><span class='detail-label'>Location/Link:</span><span>" + location + "</span></div>" if location else ""}
                    </div>

                    {f"<p><strong>Additional Notes:</strong><br>{notes}</p>" if notes else ""}

                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Interview Details</a>

                    <p style="margin-top: 20px; color: #666;">
                        <strong>Tip:</strong> Make sure to arrive 5-10 minutes early and prepare your questions!
                    </p>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(candidate.email, subject, html_content)

    def send_interview_cancelled_email(self, candidate, job_title, interview_datetime):
        """Send email to candidate when interview is cancelled"""
        formatted_date = interview_datetime.strftime("%A, %B %d, %Y at %I:%M %p")

        subject = f"Interview Cancelled - {job_title}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px;
                           border-left: 4px solid #ef4444; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Interview Cancelled</h1>
                </div>
                <div class="content">
                    <p>Hi {candidate.first_name or candidate.email.split('@')[0]},</p>
                    <p>We regret to inform you that your interview for <strong>{job_title}</strong> has been cancelled.</p>

                    <div class="info-box">
                        <p><strong>Originally scheduled for:</strong> {formatted_date}</p>
                    </div>

                    <p>The recruiter will contact you if they wish to reschedule.</p>
                </div>
                <div class="footer">
                    <p>© 2024 {self.from_name}. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(candidate.email, subject, html_content)


# Global instance
email_service = ResendEmailService()
