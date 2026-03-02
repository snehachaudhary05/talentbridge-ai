import logging
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from datetime import timedelta
from .models import User, CandidateProfile, OTPVerification, generate_otp
from .serializers import RegisterSerializer, CandidateProfileSerializer, CustomTokenObtainPairSerializer
from .permissions import IsCandidate
from notifications.utils.email_service import email_service

logger = logging.getLogger(__name__)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view that uses email instead of username"""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Mark as unverified and send OTP
        user.is_verified = False
        user.save()

        otp_code = generate_otp()
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            purpose='registration',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        logger.info(f"Sending registration OTP to {user.email}")
        sent = email_service.send_otp_email(user, otp_code, 'registration')
        if not sent:
            logger.error(f"Failed to send registration OTP to {user.email}")

        return Response(
            {'message': 'Registration successful. Please check your email for the OTP to verify your account.'},
            status=status.HTTP_201_CREATED
        )


class VerifyRegistrationOTPView(APIView):
    """Verify OTP sent during registration"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        otp_code = request.data.get('otp', '').strip()

        if not email or not otp_code:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({'message': 'Email already verified. Please login.'})

        otp = OTPVerification.objects.filter(
            user=user, otp_code=otp_code, purpose='registration', is_used=False
        ).last()

        if not otp or not otp.is_valid():
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()
        user.is_verified = True
        user.save()

        return Response({'message': 'Email verified successfully. You can now login.'})


class ResendOTPView(APIView):
    """Resend OTP for registration or login"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        purpose = request.data.get('purpose', 'registration')

        if purpose not in ('registration', 'login'):
            return Response({'error': 'Invalid purpose.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'No account found with this email.'}, status=status.HTTP_404_NOT_FOUND)

        otp_code = generate_otp()
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        logger.info(f"Resending {purpose} OTP to {user.email}")
        sent = email_service.send_otp_email(user, otp_code, purpose)
        if not sent:
            logger.error(f"Failed to resend {purpose} OTP to {user.email}")
            return Response(
                {'error': 'Failed to send OTP email. Please check email configuration.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'message': 'OTP resent to your email.'})


class RequestLoginOTPView(APIView):
    """Request OTP to login without password"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        logger.info(f"[OTP REQUEST] Received login OTP request for: {email}")

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            logger.info(f"[OTP REQUEST] User found: {email}, is_verified={user.is_verified}")
        except User.DoesNotExist:
            logger.warning(f"[OTP REQUEST] No user found with email: {email}")
            return Response({'error': 'No account found with this email.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_verified:
            logger.warning(f"[OTP REQUEST] User {email} is not verified")
            return Response(
                {'error': 'Email not verified. Please complete registration first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_code = generate_otp()
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            purpose='login',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        logger.info(f"[OTP REQUEST] Sending login OTP email to {user.email}, EMAIL_HOST_USER={bool(settings.EMAIL_HOST_USER)}")
        sent = email_service.send_otp_email(user, otp_code, 'login')
        if not sent:
            logger.error(f"[OTP REQUEST] Failed to send OTP email to {user.email}")
            return Response(
                {'error': 'Failed to send OTP email. Please check email configuration.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info(f"[OTP REQUEST] OTP sent successfully to {user.email}")
        return Response({'message': 'OTP sent to your email.'})


class VerifyLoginOTPView(APIView):
    """Verify login OTP and return JWT tokens"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        otp_code = request.data.get('otp', '').strip()

        if not email or not otp_code:
            return Response({'error': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = OTPVerification.objects.filter(
            user=user, otp_code=otp_code, purpose='login', is_used=False
        ).last()

        if not otp or not otp.is_valid():
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        })


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
