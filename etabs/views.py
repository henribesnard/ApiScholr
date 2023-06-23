from rest_framework import viewsets
from ApiScholr.permissions import IsAdminUser
from .models import Establishment, EstablishmentType
from .serializers import EstablishmentSerializer, EstablishmentTypeSerializer


class EstablishmentTypeViewSet(viewsets.ModelViewSet):
    queryset = EstablishmentType.objects.all()
    serializer_class = EstablishmentTypeSerializer
    permission_classes = [IsAdminUser]


class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = [IsAdminUser]
