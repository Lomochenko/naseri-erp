from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserAPITest(APITestCase):
    """تست‌های API کاربران"""
    def setUp(self):
        self.admin = User.objects.create_superuser(
            phone_number="09120000000",
            password="adminpass123",
            first_name="ادمین",
            last_name="سیستم"
        )
        self.user = User.objects.create_user(
            phone_number="09123456789",
            password="password123",
            first_name="علی",
            last_name="محمدی"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        self.client.force_authenticate(user=self.admin)  # فقط ادمین مجاز است
        url = reverse('user-list')
        data = {
            "phone_number": "09121234567",
            "password": "testpass123",
            "first_name": "رضا",
            "last_name": "کاظمی"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone_number="09121234567").exists())

    def test_user_login(self):
        url = reverse('login')
        data = {"phone_number": "09123456789", "password": "password123"}
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_change_password(self):
        url = reverse('change-password')
        data = {"old_password": "password123", "new_password": "newpass456"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass456"))

    def test_profile_view_and_update(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], "09123456789")
        # ویرایش پروفایل
        data = {"first_name": "علی‌رضا", "last_name": "محمدی"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "علی‌رضا")
