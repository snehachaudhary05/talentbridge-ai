from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import FileResponse
from .models import User, CandidateProfile
from .serializers import RegisterSerializer, CandidateProfileSerializer, CustomTokenObtainPairSerializer
from .permissions import IsCandidate


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view that uses email instead of username"""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current user information"""
    return Response({
        'id': request.user.id,
        'email': request.user.email,
        'role': request.user.role
    })


class CandidateProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for candidate profile management"""
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = [IsAuthenticated, IsCandidate]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Candidates only see their own profile
        return CandidateProfile.objects.filter(user=self.request.user)

    def get_object(self):
        # Get or create profile for current user
        profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile, created = CandidateProfile.objects.get_or_create(
            user=request.user
        )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['post', 'put'])
    def upload_resume(self, request):
        """Upload resume file"""
        profile, created = CandidateProfile.objects.get_or_create(
            user=request.user
        )

        if 'resume_file' not in request.FILES:
            return Response(
                {'error': 'No resume file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.resume_file = request.FILES['resume_file']

        # Update other fields if provided
        if 'resume_text' in request.data:
            profile.resume_text = request.data['resume_text']
        if 'skills' in request.data:
            profile.skills = request.data['skills']
        if 'phone' in request.data:
            profile.phone = request.data['phone']
        if 'location' in request.data:
            profile.location = request.data['location']
        if 'experience_years' in request.data:
            profile.experience_years = request.data['experience_years']
        if 'education' in request.data:
            profile.education = request.data['education']

        profile.save()

        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def download_resume(self, request):
        """Download own resume"""
        try:
            profile = CandidateProfile.objects.get(user=request.user)
            if not profile.resume_file:
                return Response(
                    {'error': 'No resume uploaded'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response = FileResponse(
                profile.resume_file.open('rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{profile.resume_file.name}"'
            return response
        except CandidateProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
