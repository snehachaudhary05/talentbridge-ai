from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with role-based access"""

    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]

    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class CandidateProfile(models.Model):
    """Extended profile for candidates with resume storage"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_profile',
        limit_choices_to={'role': 'candidate'}
    )
    resume_file = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        help_text='Upload your resume (PDF, DOC, DOCX)'
    )
    resume_text = models.TextField(
        blank=True,
        help_text='Extracted or pasted resume text'
    )
    skills = models.TextField(
        blank=True,
        help_text='Comma-separated list of skills'
    )
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    education = models.TextField(blank=True)

    # Additional application fields
    college_name = models.CharField(max_length=200, blank=True)
    passout_year = models.IntegerField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    leetcode_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
