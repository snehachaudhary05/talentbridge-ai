from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, CandidateProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'candidate')
        )

        # Create candidate profile if role is candidate
        if user.role == 'candidate':
            CandidateProfile.objects.create(user=user)

        return user


class CandidateProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = CandidateProfile
        fields = [
            'id', 'user', 'user_email', 'first_name', 'last_name',
            'resume_file', 'resume_url', 'resume_text', 'skills', 'phone',
            'location', 'experience_years', 'education', 'college_name',
            'passout_year', 'linkedin_url', 'leetcode_url', 'github_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_resume_url(self, obj):
        if obj.resume_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume_file.url)
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that uses email instead of username"""
    username_field = 'email'
