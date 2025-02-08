from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurant
from reviews.models import Review


# Create your tests here.

class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            nickname='test', email='test@example.com', password='password1234'
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='test',
            contact='없음'
        )
        self.data = {
            'user': self.user,
            'restaurant': self.restaurant,
            'title': 'test',
            'comment': 'test'
        }
    def test_create_review(self):
        review = Review.objects.create(**self.data)

        self.assertEqual(review.title, self.data['title'])
        self.assertEqual(review.comment, 'test')
        self.assertEqual(review.user, self.data['user'])
        self.assertEqual(review.restaurant, self.data['restaurant'])


class ReviewAPIViewTestCase(APITestCase):
    def setUp(self):
    # 테스트 코드를 작성하기 위해 필요한 것들을 미리 생성해두는 것
        self.user = get_user_model().objects.create_user(
            nickname='test', email='test@example.com', password='password1234'
        )
        self.client.login(email='test@example.com', password='password1234')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='test',
            contact='없음'
        )
        self.data = {
            'user': self.user,
            'restaurant': self.restaurant,
            'title': 'test',
            'comment': 'test'
        }

    def test_get_review_list(self):
    # 작성된 리뷰 리스트를 가져오기 위한 APIView 테스트를 위한 코드 작성
        review = Review.objects.create(**self.data)
        url = reverse('review-list-create', kwargs= {'restaurant_pk': review.restaurant.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)


    def test_post_review(self):
    # 리뷰를 작성하면 데이터베이스에 저장되는 APIView 테스트를 위한 코드 작성
        url = reverse('review-list-create', kwargs={'restaurant_pk': self.restaurant.pk})
        data ={
            'title':'test',
            'comment':'test'
        }
        response = self.client.post(url, data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_get_review_detail(self):
    # 리뷰 상세 정보를 가져오기 위한 APIView 테스트를 위한 코드 작성
        review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_pk': review.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'test')

    def test_update_review(self):
    # 리뷰 제목, 내용을 업데이트하기 위한 APIView 테스트를 위한 코드 작성
        review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_pk': review.pk})
        data = {
            'title' :'update'
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'update')

    def test_delete_review(self):
        # 리뷰를 삭제하는 APIView 테스트를 위한 코드 작성
        review = Review.objects.create(**self.data)
        url = reverse('review-detail', kwargs={'review_pk': review.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())