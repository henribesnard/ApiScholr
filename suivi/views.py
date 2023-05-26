from django.db.models import Q
from .models import CommunicationBook, Attendance
from .serializers import CommunicationBookSerializer, AttendanceSerializer, ParentCommunicationBookSerializer, StudentCommunicationBookSerializer
from ApiScholr.permissions import IsStaffOrTeacherCreating, IsParentUser, IsStudentUser
from rest_framework import viewsets

class CommunicationBookViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationBookSerializer
    permission_classes = [IsStaffOrTeacherCreating]

    def get_queryset(self):
        user = self.request.user
        return CommunicationBook.objects.filter(
            Q(schoolclass__establishment=user.establishment) | 
            Q(student__establishment=user.establishment) |
            Q(course__schoolclass__establishment=user.establishment)
        )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(author=user)



class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStaffOrTeacherCreating]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(establishment=user.establishment)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ParentCommunicationBookViewSet(viewsets.ModelViewSet):
    serializer_class = ParentCommunicationBookSerializer
    permission_classes = [IsParentUser]

    def get_queryset(self):
        user = self.request.user
        return CommunicationBook.objects.filter(Q(student__in=user.children.all()) | Q(schoolclass__students__in=user.children.all()) | Q(course__schoolclass__students__in=user.children.all()))

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ParentCommunicationBookSerializer
        return super().get_serializer_class()  # fallback to the original serializer if not updating

    def perform_update(self, serializer):
        serializer.save()

class StudentCommunicationBookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentCommunicationBookSerializer
    permission_classes = [IsStudentUser]

    def get_queryset(self):
        user = self.request.user
        return CommunicationBook.objects.filter(Q(student=user) | Q(schoolclass__students=user) | Q(course__schoolclass__students=user))
    
class StudentAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStudentUser]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(student=user)


class ParentAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsParentUser]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(student__in=user.children.all())