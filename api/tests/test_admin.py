from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User
import environ
import os
from pathlib import Path


# environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ADMIN_EMAIL = env('ADMIN_EMAIL')
ADMIN_PASSWORD = env('ADMIN_PASSWORD')


class AdminTest(APITestCase):
    def setUp(self):
        # create superuser
        self.admin = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            is_superuser=True,
            is_staff=True
        )
        self.admin.save()

        # authorize as superuser
        login_url = reverse('Login')
        data = {
            'email': 'admin@example.com',
            'password': 'adminpass'
        }
        super_login = self.client.post(login_url, data, format='json')
        self.access_token = super_login.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


    def test_admin(self):
        # ADMIN TESTING
        # ensuring superuser exists
        self.assertEqual(User.objects.count(), 1)
        
        # registering new regular user
        register_url = reverse('Registration')
        data = {
            "email": "test@email.com",
            "username": "Test",
            "password": "testtest"
        }
        regular_user = self.client.post(register_url, data, format='json')
        regular_user_id = regular_user.data['id']

        # ensuring super and regular user exist
        self.assertEqual(User.objects.count(), 2)


        # checking that superuser cannot edit personal info of regular user
        patch_data = {
            'first_name': 'Unauthorized',
            'last_name': 'Unauthorized',
            'email': 'Unauthorized',
            'username': 'Unauthorized',
            'password': 'Unauthorized'
        }
        patch_request = self.client.patch(f'/admin/users/{regular_user_id}/', patch_data, format='json')

        self.assertEqual(patch_request.status_code, status.HTTP_400_BAD_REQUEST)


        # checking that superuser cannot delete himself
        self.client.delete(f'admin/users/1/')
        self.assertEqual(User.objects.count(), 2)

