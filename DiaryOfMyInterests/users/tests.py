from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Users


class UserTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):

        response = self.client.post(
            '/users/register/',
            {
                'username': 'testuser2',
                'email': 'test2@test.com',
                'password': '12345678'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            Users.objects.filter(email='test@test.com').exists()
        )

class LoginTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = Users.objects.create_user(
            username='test',
            email='test@test.com',
            password='12345678'
        )

    def test_login(self):

        response = self.client.post(
            '/users/api/login/',
            {
                'email': 'test@test.com',
                'password': '12345678'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn('token', response.data)