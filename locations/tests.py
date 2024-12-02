from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class LocationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='anna', password='12345')
        self.client.login(username='anna', password='12345')

        self.location1 = Location.objects.create(country='SE')
        self.location2 = Location.objects.create(country='PS')

    def test_list_locations(self):
        """Test that the locations are returned correctly."""
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(
            response.data[0]['country_name'], 'Sweden')
        self.assertEqual(
            response.data[1]['country_name'], 'Palestine, State of')

    def test_list_locations_filter(self):
        """Test filtering locations by country code."""
        response = self.client.get('/locations/?country=SE')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['country_name'], 'Sweden')

    def test_create_location(self):
        """Test that a new location can be created."""
        response = self.client.post('/locations/', {
            'country': 'IE'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 3)
        self.assertEqual(Location.objects.last().country.name, 'Ireland')
