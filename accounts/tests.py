from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient



class AccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

    def test_user_registration(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "password_confirm": "newpass123",
            "full_name": "New User",
        }
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_user_login(self):
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
