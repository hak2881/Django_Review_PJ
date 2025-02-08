from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from restaurants.models import Restaurant


# Create your tests here.

class RestaurantTestCase(TestCase):
    def setUp(self):
        self.restaurant_info = {
            'name' : 'test',
            'address' :'주소',
            'contact' :'없음',
            'regular_holiday' :'MON'
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)

        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(restaurant.contact, '없음')
        self.assertEqual(restaurant.address, self.restaurant_info['address'])

class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.restaurant_info = {
            'name': 'test',
            'address': '주소',
            'contact': '없음',
            'regular_holiday': 'MON'
        }
    def test_restaurant_list_view(self):
        url = reverse('restaurant-list')
        restaurant = Restaurant.objects.create(**self.restaurant_info)

        # client.get -> 해당 엔드포인트로 GET요청을 보낸후 , JSON 형식으로 응답을 받는다.
        response = self.client.get(url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('name'), 'test')
        self.assertEqual(response.data[0]['regular_holiday'], self.restaurant_info['regular_holiday'])

    def test_restaurant_post_view(self):
        # restaurant-create 는 존재하지 않음
        url = reverse('restaurant-list')

        response = self.client.post(url, data=self.restaurant_info, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data['name'], 'test')

    def test_restaurant_detail_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk':restaurant.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data.get('name'), 'test')

    def test_restaurant_update_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurant-detail', kwargs={'pk':restaurant.pk})

        response = self.client.patch(url, {'name':'patch'}, format='json')

        self.assertEqual(response.data.get('name'),'patch')
    
    def test_restaurant_delete_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)

        url = reverse('restaurant-detail', kwargs={'pk':restaurant.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0)




