from rest_framework import viewsets
from .models import Assessment, Grade
from .serializers import AssessmentSerializer, GradeSerializer
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

class UserAssessmentListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='STUDENT').exists():
            return Assessment.objects.filter(course__schoolclass__students=user)
        elif user.roles.filter(name='PARENT').exists():
            return Assessment.objects.filter(course__schoolclass__students__in=user.children.all())
        else:
            return Assessment.objects.none()

class UserGradeListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(name='STUDENT').exists():
            return Grade.objects.filter(student=user)
        elif user.roles.filter(name='PARENT').exists():
            return Grade.objects.filter(student__in=user.children.all())
        else:
            return Grade.objects.none()