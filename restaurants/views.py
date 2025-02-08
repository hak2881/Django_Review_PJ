from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

