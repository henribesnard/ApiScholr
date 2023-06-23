from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstablishmentTypeViewSet, EstablishmentViewSet

router = DefaultRouter()
router.register(r'api/establishment-types', EstablishmentTypeViewSet)
router.register(r'api/establishments', EstablishmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
