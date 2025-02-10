from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from restaurants.models import Restaurant
from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewDetailSerializer


# Create your views here.


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Django ORM에서는 외래 키(ForeignKey)를 필터링할 때 _id를 사용해야 함 (restaurant_id)
        return self.queryset.filter(restaurant_id=self.kwargs.get('restaurant_pk'))

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_pk')
        restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
        serializer.save(user=self.request.user, restaurant=restaurant)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_pk'), user=self.request.user)  # ✅ 개별 객체 가져오기


