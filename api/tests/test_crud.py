from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User, Post


class CrudTest(APITestCase):
    def setUp(self):
            # registering new user
            register_url = reverse('Registration')
            data = {
                "email": "test@email.com",
                "username": "Test",
                "password": "testtest"
            }
            register = self.client.post(register_url, data, format='json')

            # getting access token
            self.access_token = register.data['tokens']['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


    def test_crud(self):
        # CRUD TESTING
        # READ EMPTY
        # preparing read request
        empty_read_request = self.client.get(reverse('Create new post or read all posts'))

        # checking read request
        self.assertEqual(empty_read_request.status_code, status.HTTP_200_OK)
        self.assertIn('Nothing to display', empty_read_request.data['msg'])


        # CREATE
        # preparing create request
        new_post = {
            "title": "First testing post",
            "content": "Content of first testing post.",
            "category": "Personal",
            "tags": ["First tag", "Second tag"]
        }
        create_request = self.client.post(reverse('Create new post or read all posts'), new_post, format='json')

        # checking create request
        self.assertEqual(create_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        # preparing invalid create request
        invalid_post = {
            "invalid": "invalid"
        }
        invalid_create_request = self.client.post(reverse('Create new post or read all posts'), invalid_post, format='json')

        # checking invalid create request
        self.assertEqual(invalid_create_request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 1)


        # READ
        # preparing read request
        read_request = self.client.get(reverse('Create new post or read all posts'))

        # checking read request
        self.assertEqual(read_request.status_code, status.HTTP_200_OK)
        for key in ('id', 'title', 'content', 'category', 'tags', 'author'):
            self.assertIn(key, read_request.data[0])


        # UPDATE
        # preparing update request
        updated_post = {
            'title': 'This is my updated post',
            'content': 'This is content of updated post'
        }
        update_request = self.client.put(reverse('Post by its pk (id)', kwargs={'pk': 1}), updated_post, format='json')

        # checking update request
        self.assertEqual(update_request.status_code, status.HTTP_200_OK)
        self.assertEqual('This is my updated post', update_request.data['title'])

        # preparing invalid update request
        invalid_updated_post = {
            'id': 10,
            'author': 12
        }
        invalid_update_request = self.client.put(reverse('Post by its pk (id)', kwargs={'pk': 1}), invalid_updated_post, format='json')

        # checking invalid update request
        self.assertEqual(invalid_update_request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid Input', invalid_update_request.data['msg'])


        # DELETE
        # preparing delete request
        delete_request = self.client.delete(reverse('Post by its pk (id)', kwargs={'pk': 1}))

        # checking delete request
        self.assertEqual(delete_request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

        # preparing invalid delete request
        invalid_delete_request = self.client.delete(reverse('Post by its pk (id)', kwargs={'pk': 1}))

        # checking invalid delete request
        self.assertEqual(invalid_delete_request.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Invalid ID', invalid_delete_request.data['msg'])

        