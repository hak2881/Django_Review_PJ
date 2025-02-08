from django.contrib.auth import get_user_model
from django.test import TestCase

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