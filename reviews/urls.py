from django.urls import path
from reviews import views

urlpatterns = [
    path('restaurants/<int:restaurant_pk>/review/', views.ReviewListCreateView.as_view(),
         name='review-list-create'),
    path('review/<int:review_pk>/', views.ReviewDetailView.as_view(),
         name='review-detail'),
]