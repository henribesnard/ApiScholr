# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Establishment, EstablishmentType
from django.contrib.auth import get_user_model

class EstablishmentCreationTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('besnard', 'besnard@example.com', 'Harena2032@')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.establishment_types = EstablishmentType.objects.all()
        self.valid_payload = {
            "name": "Test Establishment",
            "address": {
                "street_number": "123",
                "street_name": "Test street",
                "postal_code": "75000",
                "city": "Test city",
                "department": "Test department",
                "country": "Test country"
            },
            "types": [et.id for et in self.establishment_types],
            "category": "PRIVATE",
            "phone_number": "+33123456789",
            "head": None,
            "is_active": True
        }

    def test_create_establishment_all_types(self):
        url = reverse('establishment-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Establishment.objects.count(), 1)
        self.assertEqual(Establishment.objects.get().name, 'Test Establishment')
