import os
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class ProfileTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='anna', password='12345')
        self.client = APIClient()
        self.client.login(username='anna', password='12345')

    def test_create_profile(self):
        """Test if a profile is created when a user is created."""

        self.user.refresh_from_db()
        response = self.client.get(f'/profiles/{self.user.profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['name'], '')

    def test_update_profile(self):
        """Test if a user can update their profile content (bio)."""
        response = self.client.put(
            f'/profiles/{self.user.profile.id}/',
            {'content': 'Test bio', 'name': 'Test User'},
            format='json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test bio')

    def test_profile_image(self):
        """Test if the profile image can be updated."""

        image_path = os.path.join(
          os.path.dirname(__file__), '..', 'images', 'testimage.webp')

        self.assertTrue(
          os.path.exists(image_path),
          "Image file not found at the specified path.")

        with open(image_path, 'rb') as image:
            response = self.client.put(
                f'/profiles/{self.user.profile.id}/',
                {
                    'image': image,
                    'name': 'Updated Test User'
                },
                format='multipart'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('image' in response.data)
