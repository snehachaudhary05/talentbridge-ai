from rest_framework import serializers
from .models import Job, Application, SavedJob, Interview
from accounts.models import CandidateProfile


class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model"""
    recruiter_email = serializers.EmailField(source='recruiter.email', read_only=True)
    applications_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'description', 'requirements',
            'responsibilities', 'job_type', 'location', 'is_remote',
            'salary_min', 'salary_max', 'required_skills', 'status',
            'views_count', 'deadline', 'created_at', 'updated_at',
            'recruiter', 'recruiter_email', 'applications_count', 'is_saved'
        ]
        read_only_fields = ['id', 'recruiter', 'views_count', 'created_at', 'updated_at']

    def get_applications_count(self, obj):
        return obj.applications.count()

    def get_is_saved(self, obj):
        """Check if current user has saved this job"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False


class JobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job listings"""
    recruiter_email = serializers.EmailField(source='recruiter.email', read_only=True)
    applications_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'job_type', 'location',
            'is_remote', 'salary_min', 'salary_max', 'status',
            'created_at', 'recruiter_email', 'applications_count', 'is_saved'
        ]

    def get_applications_count(self, obj):
        return obj.applications.count()

    def get_is_saved(self, obj):
        """Check if current user has saved this job"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False


class ApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Application model"""
    candidate_email = serializers.EmailField(source='candidate.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company_name', read_only=True)
    candidate_profile = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'company_name', 'candidate',
            'candidate_email', 'candidate_profile', 'cover_letter', 'resume_text',
            'resume_file_url', 'status', 'skill_match_score',
            'ai_summary', 'applied_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'candidate', 'skill_match_score', 'ai_summary',
            'applied_at', 'updated_at'
        ]

    def get_candidate_profile(self, obj):
        """Include candidate profile data for recruiters"""
        request = self.context.get('request')

        # Only show profile to recruiters who own the job
        if request and request.user.role == 'recruiter' and obj.job.recruiter == request.user:
            try:
                profile = CandidateProfile.objects.get(user=obj.candidate)
                return {
                    'id': profile.id,
                    'first_name': obj.candidate.first_name,
                    'last_name': obj.candidate.last_name,
                    'email': obj.candidate.email,
                    'skills': profile.skills,
                    'phone': profile.phone,
                    'location': profile.location,
                    'experience_years': profile.experience_years,
                    'education': profile.education,
                    'college_name': profile.college_name,
                    'passout_year': profile.passout_year,
                    'linkedin_url': profile.linkedin_url,
                    'leetcode_url': profile.leetcode_url,
                    'github_url': profile.github_url,
                    'resume_url': request.build_absolute_uri(profile.resume_file.url) if profile.resume_file else None,
                    'has_resume': bool(profile.resume_file)
                }
            except CandidateProfile.DoesNotExist:
                return None

        # Candidates and other users don't see this data
        return None


class ApplicationCreateSerializer(serializers.Serializer):
    """Serializer for creating applications with profile updates"""

    # Application fields
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    cover_letter = serializers.CharField(required=False, allow_blank=True)

    # Profile fields
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    college_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    passout_year = serializers.IntegerField(required=False, allow_null=True)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    leetcode_url = serializers.URLField(required=False, allow_blank=True)
    github_url = serializers.URLField(required=False, allow_blank=True)
    resume = serializers.FileField(required=False, allow_null=True)

    def validate(self, data):
        """Check if candidate has already applied to this job"""
        user = self.context['request'].user
        job = data.get('job')

        # Check if application already exists
        if Application.objects.filter(job=job, candidate=user).exists():
            raise serializers.ValidationError(
                "You have already applied to this job. You can only apply once per job."
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        job = validated_data['job']

        # Update user's first and last name
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.save()

        # Get or create candidate profile
        profile, created = CandidateProfile.objects.get_or_create(user=user)

        # Update profile fields
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        if 'college_name' in validated_data:
            profile.college_name = validated_data['college_name']
        if 'passout_year' in validated_data:
            profile.passout_year = validated_data['passout_year']
        if 'linkedin_url' in validated_data:
            profile.linkedin_url = validated_data['linkedin_url']
        if 'leetcode_url' in validated_data:
            profile.leetcode_url = validated_data['leetcode_url']
        if 'github_url' in validated_data:
            profile.github_url = validated_data['github_url']
        if 'resume' in validated_data and validated_data['resume']:
            profile.resume_file = validated_data['resume']

        profile.save()

        # Create application
        application = Application.objects.create(
            job=job,
            candidate=user,
            cover_letter=validated_data.get('cover_letter', ''),
            status='applied'
        )

        return application

    def to_representation(self, instance):
        """Use ApplicationSerializer for the response"""
        serializer = ApplicationSerializer(instance, context=self.context)
        return serializer.data


class SavedJobSerializer(serializers.ModelSerializer):
    """Serializer for SavedJob model"""
    job_details = JobListSerializer(source='job', read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'job', 'job_details', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class InterviewSerializer(serializers.ModelSerializer):
    """Serializer for Interview model"""
    candidate_email = serializers.EmailField(source='application.candidate.email', read_only=True)
    candidate_name = serializers.SerializerMethodField()
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    company_name = serializers.CharField(source='application.job.company_name', read_only=True)
    recruiter_email = serializers.EmailField(source='application.job.recruiter.email', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'application', 'scheduled_datetime', 'duration_minutes',
            'interview_type', 'location', 'status', 'notes', 'reminder_sent',
            'candidate_email', 'candidate_name', 'job_title', 'company_name',
            'recruiter_email', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reminder_sent', 'created_at', 'updated_at']

    def get_candidate_name(self, obj):
        """Get candidate's full name"""
        candidate = obj.application.candidate
        if candidate.first_name or candidate.last_name:
            return f"{candidate.first_name} {candidate.last_name}".strip()
        return candidate.email
