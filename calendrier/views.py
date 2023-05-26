from rest_framework import viewsets
from .models import Room, Timeslot
from .serializers import RoomSerializer, TimeslotSerializer
from ApiScholr.permissions import IsHeadOrStaffUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsHeadOrStaffUser]

    def get_queryset(self):
        # Les utilisateurs ne peuvent voir que les Rooms dans leur établissement
        user = self.request.user
        return Room.objects.filter(establishment=user.establishment)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class TimeslotCreateView(CreateAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = [IsHeadOrStaffUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TimeslotUpdateView(UpdateAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = [IsHeadOrStaffUser]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class TimeslotDeleteView(DestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = [IsHeadOrStaffUser]

class TimeslotListView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeslotSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Timeslot.objects.none()

        # Staff and Heads can view all timeslots of their establishment
        if user.roles.filter(name__in=['HEAD', 'STAFF']).exists():
            queryset = Timeslot.objects.filter(schoolclass__establishment=user.establishment)

        # Teachers can view timeslots where they are teaching
        elif user.roles.filter(name='TEACHER').exists():
            queryset = Timeslot.objects.filter(course__teacher=user)

        # Students can view timeslots for their classes
        elif user.roles.filter(name='STUDENT').exists():
            queryset = Timeslot.objects.filter(schoolclass__students=user)

        # Parents can view timeslots of their children
        elif user.roles.filter(name='PARENT').exists():
            queryset = Timeslot.objects.filter(
                Q(schoolclass__students__in=user.children.all()) | 
                Q(course__students__in=user.children.all())
            )

        return queryset