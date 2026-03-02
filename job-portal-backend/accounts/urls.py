from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, CandidateProfileViewSet, get_current_user,
    VerifyRegistrationOTPView, ResendOTPView,
    RequestLoginOTPView, VerifyLoginOTPView,
)

router = DefaultRouter()
router.register(r'profile', CandidateProfileViewSet, basename='candidate-profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyRegistrationOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('request-login-otp/', RequestLoginOTPView.as_view(), name='request-login-otp'),
    path('verify-login-otp/', VerifyLoginOTPView.as_view(), name='verify-login-otp'),
    path('me/', get_current_user, name='current-user'),
    path('', include(router.urls)),
]
