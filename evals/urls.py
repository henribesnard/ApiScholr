from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AssessmentViewSet, GradeViewSet, PerformanceViewSet, 
                    StudentAssessmentViewSet, ParentAssessmentViewSet, 
                    StudentGradeViewSet, ParentGradeViewSet,
                    StudentPerformanceViewSet, ParentPerformanceViewSet)

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'performances', PerformanceViewSet, basename='performance')
router.register(r'student/assessments', StudentAssessmentViewSet, basename='student-assessment')
router.register(r'student/grades', StudentGradeViewSet, basename='student-grade')
router.register(r'student/performances', StudentPerformanceViewSet, basename='student-performance')
router.register(r'parent/assessments', ParentAssessmentViewSet, basename='parent-assessment')
router.register(r'parent/grades', ParentGradeViewSet, basename='parent-grade')
router.register(r'parent/performances', ParentPerformanceViewSet, basename='parent-performance')

urlpatterns = [
    path('api/', include(router.urls)),
]
