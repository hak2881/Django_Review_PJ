from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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

class UserAPIViewTestCase(APITestCase):
    def setUp(self):
        # 테스트 코드를 작성하기 위해 필요한 것들을 미리 생성해두는 것
        self.user = {
            'email': 'test@test.com',
            'nickname': 'test',
            'password': 'password1234'
        }

    def test_user_signup(self):
        # 회원가입 APIView 테스트를 위한 코드 작성
        url = reverse('user-signup')
        response = self.client.post(url, self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data.get('nickname'), 'test')

    def test_user_login(self):
        # 로그인 성공 시 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.user)
        url = reverse('user-login')
        data = {
            'email' : self.user.get('email'),
            'password': self.user.get('password'),
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'login success')

    def test_user_login_invalid_credentials(self):
        # 로그인 실패 시 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.user)
        data = {
            'email': 'test@test.com',
            'password': 'wrong'
        }
        response = self.client.post(reverse('user-login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_detail(self):
        # 유저 정보를 가져오는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.user)
        url = reverse('user-detail', kwargs={'pk': user.pk})
        # 로그인 시키는 위치 중요
        self.client.login(email=self.user['email'], password=self.user['password'])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'test@test.com')

    def test_update_user_details(self):
        # 유저 정보를 업데이트 하는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.user)
        url = reverse('user-detail', kwargs={'pk': user.pk})
        # 로그인 시키는 위치 중요
        self.client.login(email=self.user['email'], password=self.user['password'])

        data = {
            'nickname' : 'update_test'
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('nickname'), 'update_test')

    def test_delete_user(self):
        # 유저 회원 탈퇴(모델 삭제)를 진행하는 APIView 테스트를 위한 코드 작성
        user = User.objects.create_user(**self.user)
        url = reverse('user-detail', kwargs={'pk': user.pk})
        # 로그인 시키는 위치 중요
        self.client.login(email=self.user['email'], password=self.user['password'])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


