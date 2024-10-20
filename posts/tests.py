from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class PostListviewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username='anna', password='12345')
    
    def test_list_posts(self):
        anna = User.objects.get(username='anna')
        Post.objects.create(owner=anna, title='Title 1')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_loggedin_user_can_create_post(self):
        self.client.login(username='anna', password='12345')
        response = self.client.post('/posts/', {'title': 'Title 1'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_loggedin_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'Title 1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        anna = User.objects.create_user(username='anna', password='12345')
        bill = User.objects.create_user(username='bill', password='12345')
        Post.objects.create(owner=anna, title='Title 1', content='Content 1')
        Post.objects.create(owner=bill, title='Title 2', content='Content 2')

    def test_retrieve_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'Title 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_loggedin_user_can_update_own_post(self):
        self.client.login(username='anna', password='12345')
        response = self.client.put('/posts/1/', {'title': 'Title 1 Updated'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'Title 1 Updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loggedin_user_cant_update_others_post(self):
        self.client.login(username='anna', password='12345')
        response = self.client.put('/posts/2/', {'title': 'Title 2 Updated'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    