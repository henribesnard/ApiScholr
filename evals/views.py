from rest_framework import viewsets, permissions
from .models import Assessment, Grade, Performance
from .serializers import AssessmentSerializer, GradeSerializer, PerformanceSerializer
from ApiScholr.permissions import IsStaffOrTeacherCreating

class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsStaffOrTeacherCreating]

    def get_queryset(self):
        user = self.request.user
        return Assessment.objects.filter(course__created_by__current_establishment=user.current_establishment)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsStaffOrTeacherCreating]

    def get_queryset(self):
        user = self.request.user
        return Grade.objects.filter(student__current_establishment=user.current_establishment)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    permission_classes = [IsStaffOrTeacherCreating]

    def get_queryset(self):
        user = self.request.user
        return Performance.objects.filter(student__current_establishment=user.current_establishment)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class StudentAssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='STUDENT').exists():
            return Assessment.objects.filter(course__schoolclass__students=user)

class ParentAssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='PARENT').exists():
            return Assessment.objects.filter(course__schoolclass__students__in=user.children.all())

class StudentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='STUDENT').exists():
            return Grade.objects.filter(student=user)

class ParentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='PARENT').exists():
            return Grade.objects.filter(student__in=user.children.all())

class StudentPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='STUDENT').exists():
            return Performance.objects.filter(grade__student=user)

class ParentPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='PARENT').exists():
            return Performance.objects.filter(grade__student__in=user.children.all())
