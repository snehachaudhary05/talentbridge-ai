from django.db import models
from django.conf import settings


class Job(models.Model):
    """Job or Internship posting model"""

    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]

    # Basic Info
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(help_text="Required skills and qualifications")
    responsibilities = models.TextField(help_text="Job responsibilities")

    # Job Details
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    is_remote = models.BooleanField(default=False)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Skills (comma-separated for simplicity, can be normalized later)
    required_skills = models.TextField(help_text="Comma-separated skills")
    required_experience = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required years of experience"
    )

    # Metadata
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs_posted',
        limit_choices_to={'role': 'recruiter'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['job_type']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company_name}"


class Application(models.Model):
    """Job Application model"""

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('oa_round', 'OA Round'),
        ('tech_round', 'Tech Round'),
        ('hr_round', 'HR Round'),
        ('offer_received', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    # Relations
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'candidate'}
    )

    # Application Data
    cover_letter = models.TextField(blank=True)
    resume_text = models.TextField(help_text="Extracted text from resume")
    resume_file_url = models.URLField(blank=True, help_text="URL to uploaded resume")

    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='applied')

    # AI-generated fields
    skill_match_score = models.FloatField(
        null=True,
        blank=True,
        help_text="AI-calculated skill match percentage"
    )
    ai_summary = models.TextField(
        blank=True,
        help_text="AI-generated summary of candidate profile"
    )

    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'candidate']  # One application per job per candidate
        indexes = [
            models.Index(fields=['status', '-applied_at']),
            models.Index(fields=['candidate', '-applied_at']),
        ]

    def __str__(self):
        return f"{self.candidate.email} -> {self.job.title}"


class SavedJob(models.Model):
    """Saved/Bookmarked jobs for candidates"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs',
        limit_choices_to={'role': 'candidate'}
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )
    notes = models.TextField(
        blank=True,
        help_text="Personal notes about this job"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'job']  # Can't save same job twice
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email} saved {self.job.title}"


class Interview(models.Model):
    """Interview scheduling for job applications"""

    INTERVIEW_TYPE_CHOICES = [
        ('phone', 'Phone Interview'),
        ('video', 'Video Interview'),
        ('in_person', 'In-Person Interview'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    scheduled_datetime = models.DateTimeField()
    duration_minutes = models.IntegerField(
        default=60,
        help_text="Interview duration in minutes"
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default='video'
    )
    location = models.CharField(
        max_length=500,
        blank=True,
        help_text="Physical location or meeting link (Zoom, Google Meet, etc.)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or instructions for the candidate"
    )
    reminder_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_datetime']
        indexes = [
            models.Index(fields=['scheduled_datetime', 'status']),
            models.Index(fields=['application', 'status']),
        ]

    def __str__(self):
        return f"Interview for {self.application.candidate.email} - {self.application.job.title} on {self.scheduled_datetime}"

    @property
    def recruiter(self):
        """Get the recruiter who posted the job"""
        return self.application.job.recruiter

    @property
    def candidate(self):
        """Get the candidate being interviewed"""
        return self.application.candidate
