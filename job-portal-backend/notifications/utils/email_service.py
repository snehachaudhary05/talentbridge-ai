import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service using Django's built-in Gmail SMTP backend.
    """

    def send_email(self, to_email, subject, html_content):
        from_email = settings.EMAIL_HOST_USER
        from_name = getattr(settings, 'EMAIL_FROM_NAME', 'TalentBridge AI')

        if not from_email:
            logger.warning("EMAIL_HOST_USER not configured. Email not sent.")
            return False

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=f"{from_name} <{from_email}>",
                to=[to_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_otp_email(self, user, otp_code, purpose):
        if purpose == 'registration':
            subject = "Verify Your Email - TalentBridge AI"
            action_text = "complete your registration"
        else:
            subject = "Your Login OTP - TalentBridge AI"
            action_text = "log in to your account"

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
                .otp-box {{ background: white; border: 2px dashed #667eea; padding: 20px;
                           text-align: center; margin: 20px 0; border-radius: 10px; }}
                .otp-code {{ font-size: 40px; font-weight: bold; color: #667eea; letter-spacing: 8px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h1>🔐 Your OTP Code</h1></div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>Use the OTP below to {action_text}:</p>
                    <div class="otp-box">
                        <div class="otp-code">{otp_code}</div>
                        <p style="color: #666; margin-top: 10px;">Valid for 10 minutes</p>
                    </div>
                    <p>If you did not request this, please ignore this email.</p>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body>
        </html>
        """
        return self.send_email(user.email, subject, html_content)

    def send_application_submitted_email(self, user, job_title, application_id):
        subject = f"Application Submitted - {job_title}"
        html_content = f"""
        <!DOCTYPE html><html><head><style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style></head><body>
            <div class="container">
                <div class="header"><h1>🎉 Application Submitted!</h1></div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>Your application for <strong>{job_title}</strong> has been submitted successfully!</p>
                    <p>The recruiter will review your application and get back to you soon.</p>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Application Status</a>
                    <p>Good luck! 🚀</p>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(user.email, subject, html_content)

    def send_application_status_changed_email(self, user, job_title, old_status, new_status, application_id):
        subject = f"Application Status Update - {job_title}"
        status_emoji = {
            'Under Review': '👀', 'Shortlisted': '⭐', 'OA Round': '📝',
            'Tech Round': '💻', 'HR Round': '🤝', 'Offer Received': '🎉',
            'Rejected': '😔', 'Accepted': '✅'
        }
        emoji = status_emoji.get(new_status, '📬')
        html_content = f"""
        <!DOCTYPE html><html><head><style>
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
        </style></head><body>
            <div class="container">
                <div class="header"><h1>{emoji} Application Status Updated</h1></div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>Your application for <strong>{job_title}</strong> has been updated.</p>
                    <div class="status-box"><p><strong>New Status:</strong> {new_status}</p></div>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Details</a>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(user.email, subject, html_content)

    def send_new_application_email(self, recruiter, candidate_name, job_title, application_id):
        subject = f"New Application Received - {job_title}"
        html_content = f"""
        <!DOCTYPE html><html><head><style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .candidate-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style></head><body>
            <div class="container">
                <div class="header"><h1>📬 New Application Received!</h1></div>
                <div class="content">
                    <p>Hi {recruiter.first_name or recruiter.email.split('@')[0]},</p>
                    <p>You have received a new application for <strong>{job_title}</strong>.</p>
                    <div class="candidate-box"><p><strong>Candidate:</strong> {candidate_name}</p></div>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">Review Application</a>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(recruiter.email, subject, html_content)

    def send_interview_scheduled_email(self, candidate, job_title, interview_datetime, interview_type, location, notes=""):
        type_emoji = {'phone': '📞', 'video': '🎥', 'in_person': '🏢'}.get(interview_type, '📅')
        type_display = interview_type.replace('_', ' ').title()
        formatted_date = interview_datetime.strftime("%A, %B %d, %Y")
        formatted_time = interview_datetime.strftime("%I:%M %p")
        subject = f"Interview Scheduled - {job_title}"
        html_content = f"""
        <!DOCTYPE html><html><head><style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .interview-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px;
                             border-left: 4px solid #10b981; }}
            .button {{ background: #10b981; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style></head><body>
            <div class="container">
                <div class="header"><h1>{type_emoji} Interview Scheduled!</h1></div>
                <div class="content">
                    <p>Hi {candidate.first_name or candidate.email.split('@')[0]},</p>
                    <p>Your interview for <strong>{job_title}</strong> has been scheduled.</p>
                    <div class="interview-box">
                        <p><strong>Date:</strong> {formatted_date}</p>
                        <p><strong>Time:</strong> {formatted_time}</p>
                        <p><strong>Type:</strong> {type_display}</p>
                        {f'<p><strong>Location/Link:</strong> {location}</p>' if location else ''}
                        {f'<p><strong>Notes:</strong> {notes}</p>' if notes else ''}
                    </div>
                    <a href="{settings.FRONTEND_URL}/dashboard" class="button">View Details</a>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(candidate.email, subject, html_content)

    def send_interview_cancelled_email(self, candidate, job_title, interview_datetime):
        formatted_date = interview_datetime.strftime("%A, %B %d, %Y at %I:%M %p")
        subject = f"Interview Cancelled - {job_title}"
        html_content = f"""
        <!DOCTYPE html><html><head><style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .info-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px;
                       border-left: 4px solid #ef4444; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style></head><body>
            <div class="container">
                <div class="header"><h1>❌ Interview Cancelled</h1></div>
                <div class="content">
                    <p>Hi {candidate.first_name or candidate.email.split('@')[0]},</p>
                    <p>Your interview for <strong>{job_title}</strong> has been cancelled.</p>
                    <div class="info-box">
                        <p><strong>Originally scheduled for:</strong> {formatted_date}</p>
                    </div>
                    <p>The recruiter will contact you if they wish to reschedule.</p>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(candidate.email, subject, html_content)

    def send_job_match_email(self, user, job_title, company, job_id):
        subject = f"New Job Match: {job_title}"
        html_content = f"""
        <!DOCTYPE html><html><head><style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .job-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none;
                      border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
        </style></head><body>
            <div class="container">
                <div class="header"><h1>🎯 Perfect Job Match Found!</h1></div>
                <div class="content">
                    <p>Hi {user.first_name or user.email.split('@')[0]},</p>
                    <p>We found a job that matches your profile!</p>
                    <div class="job-box">
                        <h3>{job_title}</h3>
                        <p><strong>Company:</strong> {company}</p>
                    </div>
                    <a href="{settings.FRONTEND_URL}/jobs/{job_id}" class="button">View Job</a>
                </div>
                <div class="footer"><p>© 2024 {self.from_name}. All rights reserved.</p></div>
            </div>
        </body></html>
        """
        return self.send_email(user.email, subject, html_content)


# Global instance
email_service = EmailService()
