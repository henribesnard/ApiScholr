from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunicationBookViewSet, AttendanceViewSet, ParentCommunicationBookViewSet, StudentAttendanceViewSet, ParentAttendanceViewSet

router = DefaultRouter()
router.register(r'communication-books', CommunicationBookViewSet, basename='communication-book')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'parent/communicationbooks', ParentCommunicationBookViewSet, basename='parent-communication-book')
router.register(r'student/attendances', StudentAttendanceViewSet, basename='student-attendance')
router.register(r'parent/attendances', ParentAttendanceViewSet, basename='parent-attendance')

urlpatterns = [
    path('api/', include(router.urls)),
]
