from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User


class AuthTest(APITestCase):
    def test_auth(self):
        # REGISTRATION TESTING
        # preparing register request
        register_url = reverse('Registration')
        data = {
            "email": "test@email.com",
            "username": "Test",
            "password": "testtest"
        }
        response = self.client.post(register_url, data, format='json')

        # checking response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)   # user is registred
        self.assertEqual(User.objects.count(), 1)  # user is saved into database
        self.assertIn('access', response.data['tokens'])  # access token is created
        self.assertIn('refresh', response.data['tokens'])  # refresh token is created
        self.assertNotEqual(User.objects.get(id=1).password, 'testtest')  # checking that password is hashed

        # checking same email and username registration
        response_duplicate = self.client.post(register_url, data, format='json')
        self.assertEqual(response_duplicate.status_code, status.HTTP_400_BAD_REQUEST)   # same email and username
        self.assertEqual(User.objects.count(), 1)   # still only one user registered
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)


        # LOGIN TESTING
        # preparing login request
        login_url = reverse('Login')
        data = {
            "email": "test@email.com",
            "password": "testtest"
        }
        response = self.client.post(login_url, data, format='json')

        # checking login response
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   # user logged in
        self.assertIn('access', response.data['tokens'])  # access token is created
        self.assertIn('refresh', response.data['tokens'])  # refresh token is created

        # preparing invalid request
        invalid_data = {
            "email": "invalid@email.com",
            "password": "invalid"
        }
        invalid_response = self.client.post(login_url, invalid_data, format='json')

        # checking invalid response
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)   # user did not log in
        self.assertIn('Invalid credentials', invalid_response.data['msg'])  # error msg is displayed
