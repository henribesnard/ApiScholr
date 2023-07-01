from rest_framework import generics, status
from .serializers import (SchoolclassSerializer, CourseSerializer, SchoolclassUpdateSerializer, CourseUpdateSerializer, SchoolclassSerializer, CourseSerializer)
from .models import Schoolclass, Course
from django.utils.translation import gettext_lazy as _
from ApiScholr.permissions import IsHeadOrStaffUser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from django.db.models import Q
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Handle PermissionDenied exceptions with your custom code
    if isinstance(exc, PermissionDenied):
        return Response(
            {"detail": _("Cannot create a school class. Please, make sure that you are authorized.")},
            status=status.HTTP_403_FORBIDDEN
        )

    # For all other exception types, use the default handler
    return exception_handler(exc, context)

class CreateSchoolclassView(generics.CreateAPIView):
    queryset = Schoolclass.objects.all()
    serializer_class = SchoolclassSerializer
    permission_classes = [IsHeadOrStaffUser]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": _("A class with this name already exists in this establishment.")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateCourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsHeadOrStaffUser]

    def get_exception_handler(self):
      return lambda exc, context: Response(
        {"detail": _("Cannot create a course. Please, make sure that you are authorized and the class belongs to your establishment.")},
        status=status.HTTP_403_FORBIDDEN
    ) if isinstance(exc, PermissionDenied) else super(CreateCourseView, self).get_exception_handler()(exc, context)



class SchoolclassUpdateView(generics.UpdateAPIView):
    queryset = Schoolclass.objects.all()
    serializer_class = SchoolclassUpdateSerializer
    permission_classes = [IsHeadOrStaffUser]

class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseUpdateSerializer
    permission_classes = [IsHeadOrStaffUser]


class SchoolclassListView(generics.ListAPIView):
    serializer_class = SchoolclassSerializer

    def get_queryset(self):
        user = self.request.user
        user_roles = [role for role in user.roles.values_list('name', flat=True)]
        if user.is_staff :
            return Schoolclass.objects.all()
        elif 'HEAD' in user_roles or 'STAFF' in user_roles:
            return Schoolclass.objects.filter(Q(establishment=user.current_establishment))
        else:
            return Schoolclass.objects.filter(Q(students=user) | Q(principal_teacher=user))

class SchoolclassDetailView(generics.RetrieveAPIView):
    serializer_class = SchoolclassSerializer

    def get_object(self):
        user = self.request.user
        user_roles = [role for role in user.roles.values_list('name', flat=True)]
        schoolclass = get_object_or_404(Schoolclass, pk=self.kwargs['pk'])

        if user.is_staff:
            return schoolclass
        elif 'HEAD' in user_roles or 'STAFF' in user_roles:
            if schoolclass.establishment == user.current_establishment:
                return schoolclass
            else:
                raise PermissionDenied(_("You can only view classes in your own establishment."))
        elif schoolclass.students.filter(id=user.id).exists() or schoolclass.principal_teacher == user:
            return schoolclass
        else:
            raise PermissionDenied


class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        user_roles = [role for role in user.roles.values_list('name', flat=True)]
        if user.is_staff:
            return Course.objects.all()
        elif 'HEAD' in user_roles or 'STAFF' in user_roles:
            return Course.objects.filter(Q(schoolclasses__establishment=user.current_establishment)).distinct()
        else:
            return Course.objects.filter(Q(schoolclasses__students=user) | Q(teachers=user)).distinct()


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer

    def get_object(self):
        user = self.request.user
        user_roles = [role for role in user.roles.values_list('name', flat=True)]
        course = get_object_or_404(Course, pk=self.kwargs['pk'])

        if user.is_staff:
            return course
        elif 'HEAD' in user_roles or 'STAFF' in user_roles:
            # Boucle à travers toutes les schoolclasses associées au course
            for schoolclass in course.schoolclasses.all():
                if schoolclass.establishment == user.current_establishment:
                    return course
            # Si aucune des schoolclasses n'est liée à l'établissement de l'utilisateur, déclenchez une erreur
            raise PermissionDenied(_("You can only view courses in your own establishment."))
        elif any(schoolclass.students.filter(id=user.id).exists() for schoolclass in course.schoolclasses.all()) or course.teachers.filter(id=user.id).exists():
            return course
        else:
            raise PermissionDenied

