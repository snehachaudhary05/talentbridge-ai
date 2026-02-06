from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet, SavedJobViewSet, InterviewViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'saved-jobs', SavedJobViewSet, basename='saved-job')
router.register(r'interviews', InterviewViewSet, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
]
