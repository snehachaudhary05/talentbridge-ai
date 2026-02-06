from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.http import FileResponse

from .models import Job, Application, SavedJob, Interview
from .serializers import (
    JobSerializer,
    JobListSerializer,
    ApplicationSerializer,
    ApplicationCreateSerializer,
    SavedJobSerializer,
    InterviewSerializer
)
from accounts.permissions import IsRecruiter, IsCandidate
from accounts.models import CandidateProfile


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing jobs
    - Recruiters can create, update, delete their jobs
    - Candidates can view published jobs
    """
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Job.objects.all()

        if user.role == 'recruiter':
            # Recruiters see their own jobs (all statuses)
            queryset = queryset.filter(recruiter=user)
        elif user.role == 'candidate':
            # Candidates see only published jobs
            queryset = queryset.filter(status='published')

        # Apply filters from query parameters
        skills = self.request.query_params.get('skills', None)
        if skills:
            # Search for skills in required_skills field
            queryset = queryset.filter(required_skills__icontains=skills)

        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)

        company = self.request.query_params.get('company', None)
        if company:
            queryset = queryset.filter(company_name__icontains=company)

        job_type = self.request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        # Salary range filter (include jobs with NULL salary or within range)
        salary_min = self.request.query_params.get('salary_min', None)
        salary_max = self.request.query_params.get('salary_max', None)

        if salary_min:
            queryset = queryset.filter(
                Q(salary_max__isnull=True) |
                Q(salary_max__gte=int(salary_min))
            )

        if salary_max:
            queryset = queryset.filter(
                Q(salary_min__isnull=True) |
                Q(salary_min__lte=int(salary_max))
            )

        # Experience filter (include jobs with NULL experience or within range)
        experience_min = self.request.query_params.get('experience_min', None)
        experience_max = self.request.query_params.get('experience_max', None)

        if experience_min and experience_max:
            # Filter jobs where experience is either NULL or within the range
            queryset = queryset.filter(
                Q(required_experience__isnull=True) |
                Q(required_experience__range=(int(experience_min), int(experience_max)))
            )
        elif experience_min:
            queryset = queryset.filter(
                Q(required_experience__isnull=True) |
                Q(required_experience__gte=int(experience_min))
            )
        elif experience_max:
            queryset = queryset.filter(
                Q(required_experience__isnull=True) |
                Q(required_experience__lte=int(experience_max))
            )

        return queryset

    def perform_create(self, serializer):
        # Only recruiters can create jobs
        if self.request.user.role != 'recruiter':
            raise PermissionError("Only recruiters can create jobs")
        serializer.save(recruiter=self.request.user)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment view count when a job is viewed"""
        job = self.get_object()
        job.views_count += 1
        job.save()
        return Response({'views_count': job.views_count})

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Get available filter options from published jobs"""
        jobs = Job.objects.filter(status='published')

        # Get unique companies
        companies = jobs.values_list('company_name', flat=True).distinct()

        # Get unique locations
        locations = jobs.values_list('location', flat=True).distinct()

        # Get job types
        job_types = jobs.values_list('job_type', flat=True).distinct()

        # Get salary range
        salary_range = {
            'min': jobs.order_by('salary_min').values_list('salary_min', flat=True).first() or 0,
            'max': jobs.order_by('-salary_max').values_list('salary_max', flat=True).first() or 200000
        }

        # Get experience range (always start from 0)
        max_exp = jobs.order_by('-required_experience').values_list('required_experience', flat=True).first()
        experience_range = {
            'min': 0,  # Always start from 0
            'max': max_exp if max_exp else 20
        }

        return Response({
            'companies': list(companies),
            'locations': list(locations),
            'job_types': list(job_types),
            'salary_range': salary_range,
            'experience_range': experience_range
        })

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a job (recruiter only)"""
        job = self.get_object()
        if request.user.role != 'recruiter' or job.recruiter != request.user:
            return Response(
                {'error': 'You do not have permission to view these applications'},
                status=status.HTTP_403_FORBIDDEN
            )

        applications = job.applications.all()
        serializer = ApplicationSerializer(applications, many=True, context={'request': request})
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing applications
    - Candidates can create and view their applications
    - Recruiters can view and update applications for their jobs
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.all()

        if user.role == 'candidate':
            # Candidates see only their own applications
            return queryset.filter(candidate=user)
        elif user.role == 'recruiter':
            # Recruiters see applications for their jobs
            return queryset.filter(job__recruiter=user)
        else:
            # Admins see all applications
            return queryset

    def perform_create(self, serializer):
        # Only candidates can apply
        if self.request.user.role != 'candidate':
            raise PermissionError("Only candidates can apply to jobs")
        serializer.save(candidate=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status (recruiter only)"""
        application = self.get_object()

        # Only recruiter who posted the job can update status
        if (request.user.role != 'recruiter' or
                application.job.recruiter != request.user):
            return Response(
                {'error': 'You do not have permission to update this application'},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')
        if new_status not in dict(Application.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_resume(self, request, pk=None):
        """Download candidate resume (recruiter only)"""
        application = self.get_object()

        # Only recruiter who posted the job can download resume
        if (request.user.role != 'recruiter' or
                application.job.recruiter != request.user):
            return Response(
                {'error': 'You do not have permission to download this resume'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            profile = CandidateProfile.objects.get(user=application.candidate)
            if not profile.resume_file:
                return Response(
                    {'error': 'Candidate has not uploaded a resume'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response = FileResponse(
                profile.resume_file.open('rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{application.candidate.email}_resume.pdf"'
            return response
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Candidate profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class SavedJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing saved/bookmarked jobs
    - Candidates can save and view their saved jobs
    """
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        """Return saved jobs for current user only"""
        return SavedJob.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def save_job(self, request):
        """Save/bookmark a job"""
        job_id = request.data.get('job_id')

        if not job_id:
            return Response(
                {'error': 'job_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            job = Job.objects.get(id=job_id, status='published')
        except Job.DoesNotExist:
            return Response(
                {'error': 'Job not found or not published'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already saved
        saved_job, created = SavedJob.objects.get_or_create(
            user=request.user,
            job=job,
            defaults={'notes': request.data.get('notes', '')}
        )

        if not created:
            return Response(
                {'message': 'Job already saved', 'saved_job_id': saved_job.id},
                status=status.HTTP_200_OK
            )

        serializer = self.get_serializer(saved_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def unsave_job(self, request):
        """Remove a job from saved/bookmarked jobs"""
        job_id = request.data.get('job_id')

        if not job_id:
            return Response(
                {'error': 'job_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            saved_job = SavedJob.objects.get(user=request.user, job_id=job_id)
            saved_job.delete()
            return Response(
                {'message': 'Job removed from saved jobs'},
                status=status.HTTP_200_OK
            )
        except SavedJob.DoesNotExist:
            return Response(
                {'error': 'Job not found in saved jobs'},
                status=status.HTTP_404_NOT_FOUND
            )


class InterviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing interviews
    - Recruiters can schedule, update, and cancel interviews
    - Candidates can view their scheduled interviews
    """
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return interviews based on user role"""
        user = self.request.user
        queryset = Interview.objects.select_related(
            'application__candidate',
            'application__job',
            'application__job__recruiter'
        )

        if user.role == 'recruiter':
            # Recruiters see interviews for their jobs
            return queryset.filter(application__job__recruiter=user)
        elif user.role == 'candidate':
            # Candidates see their own interviews
            return queryset.filter(application__candidate=user)
        else:
            # Admins see all interviews
            return queryset

    def perform_create(self, serializer):
        """Only recruiters can create interviews"""
        if self.request.user.role != 'recruiter':
            raise PermissionError("Only recruiters can schedule interviews")

        # Verify the recruiter owns the job
        application = serializer.validated_data['application']
        if application.job.recruiter != self.request.user:
            raise PermissionError("You can only schedule interviews for your own job postings")

        serializer.save()

    def perform_update(self, serializer):
        """Only recruiters can update interviews"""
        if self.request.user.role != 'recruiter':
            raise PermissionError("Only recruiters can update interviews")

        # Verify the recruiter owns the job
        interview = self.get_object()
        if interview.application.job.recruiter != self.request.user:
            raise PermissionError("You can only update interviews for your own job postings")

        serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an interview"""
        interview = self.get_object()

        # Only recruiter can cancel
        if request.user.role != 'recruiter' or interview.application.job.recruiter != request.user:
            return Response(
                {'error': 'Only the recruiter can cancel interviews'},
                status=status.HTTP_403_FORBIDDEN
            )

        interview.status = 'cancelled'
        interview.save()

        serializer = self.get_serializer(interview)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming interviews for the user"""
        from django.utils import timezone

        queryset = self.get_queryset().filter(
            scheduled_datetime__gte=timezone.now(),
            status='scheduled'
        ).order_by('scheduled_datetime')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
