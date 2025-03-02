
# restaurants/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants import views

router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
]