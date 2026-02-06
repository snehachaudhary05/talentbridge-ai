from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConversationViewSet,
    CandidateAIViewSet,
    RecruiterAIViewSet,
    AdminAIViewSet
)

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'candidate', CandidateAIViewSet, basename='candidate-ai')
router.register(r'recruiter', RecruiterAIViewSet, basename='recruiter-ai')
router.register(r'admin', AdminAIViewSet, basename='admin-ai')

urlpatterns = [
    path('', include(router.urls)),
]
