from django.contrib.auth.models import User
from .models import Post
from .models import Category
from .models import Location
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class PostListviewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='anna', password='12345')
        self.location = Location.objects.create(country="SE")
        self.category = Category.objects.create(name="Nature")
    
    def test_list_posts(self):
        anna = User.objects.get(username='anna')
        Post.objects.create(
            owner=anna,
            title='Title 1',
            location=self.location,
            locality="Stockholm",
            category=self.category)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_loggedin_user_can_create_post(self):
        # Login as the user
        self.client.login(username='anna', password='12345')
        
        # Create a post with all the necessary fields
        response = self.client.post('/posts/', {
            'title': 'Title 1',
            'location_id': self.location.id, 
            'locality': 'Stockholm',
            'category_id': self.category.id
        })
        
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_loggedin_user_cant_create_post(self):
        response = self.client.post('/posts/', {
        'title': 'Title 1',
        'location_id': self.location.id,
        'locality': 'Stockholm',
        'category_id': self.category.id
    })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        anna = User.objects.create_user(username='anna', password='12345')
        bill = User.objects.create_user(username='bill', password='12345')
        # Create location and category for posts
        self.location = Location.objects.create(country="SE")
        self.category = Category.objects.create(name="Nature")
        
        # Create posts for testing
        self.post1 = Post.objects.create(
            owner=anna,
            title='Title 1',
            content='Content 1',
            location=self.location,
            locality="Stockholm",
            category=self.category)
        self.post2 = Post.objects.create(
            owner=bill,
            title='Title 2',
            content='Content 2',
            location=self.location,
            locality="Stockholm",
            category=self.category)

    def test_retrieve_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'Title 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_loggedin_user_can_update_own_post(self):
        self.client.login(username='anna', password='12345')

        updated_data = {
            'title': 'Title 1 Updated',
            'content': 'Updated content',
            'location_id': self.location.id,
            'locality': 'Stockholm',
            'category_id': self.category.id
        }

        response = self.client.put(f'/posts/{self.post1.id}/', updated_data)
        
        post = Post.objects.get(pk=self.post1.id)
        
        # Check if the post is updated correctly
        self.assertEqual(post.title, 'Title 1 Updated')
        self.assertEqual(post.content, 'Updated content')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loggedin_user_cant_update_others_post(self):
        self.client.login(username='anna', password='12345')
        response = self.client.put('/posts/2/', {'title': 'Title 2 Updated'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        