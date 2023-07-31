from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentViewSet, GradeViewSet,
    UserAssessmentListView, UserGradeListView,
)

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'user/assessments', UserAssessmentListView, basename='user-assessment')
router.register(r'user/grades', UserGradeListView, basename='user-grade')

urlpatterns = [
    path('api/', include(router.urls)),
]