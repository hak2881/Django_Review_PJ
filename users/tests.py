from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = {
            'email' : 'test@test.com',
            'nickname' :'test',
            'password' : 'password1234'
        }
        self.super_user = {
            'email': 'admin@example.com',
            'nickname': 'admin_user',
            'password': 'password1234',
        }

    def test_user_manager_create_user(self):
        user = User.objects.create_user(**self.user)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, self.user['email'])
        self.assertFalse(user.is_staff, False)
        self.assertFalse(user.is_superuser, False)
        self.assertTrue(user.is_active, True)

    def test_user_manager_create_superuser(self):
        user = User.objects.create_superuser(**self.super_user)

        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_active, True)
        self.assertEqual(user.profile_image.url, '/media/users/blank_profile_image.png')
