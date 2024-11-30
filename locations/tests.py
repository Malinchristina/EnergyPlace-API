from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location
from django.contrib.auth.models import User

# Create your tests here.


class LocationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='anna', password='12345')
        self.client.login(username='anna', password='12345')
        self.location = Location.objects.create(
            name='Location 1', country='SE'
        )
        self.location2 = Location.objects.create(
            name='Location 2', country='PS'
        )

    def test_list_locations(self):
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Location 1')
        self.assertEqual(response.data[1]['name'], 'Location 2')

    def test_list_locations_filter(self):
        response = self.client.get('/locations/?country=SE')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Location 1')

    def test_create_location(self):
        response = self.client.post('/locations/', {
            'name': 'New Location',
            'country': 'IE'
        },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 3)
        self.assertEqual(Location.objects.last().name, 'New Location')
        self.assertEqual(Location.objects.last().country, 'IE')
