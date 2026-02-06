from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CandidateProfileViewSet, get_current_user

router = DefaultRouter()
router.register(r'profile', CandidateProfileViewSet, basename='candidate-profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', get_current_user, name='current-user'),
    path('', include(router.urls)),
]
