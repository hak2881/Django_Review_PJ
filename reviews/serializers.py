from rest_framework import serializers

from restaurants.serializers import RestaurantSerializer
from reviews.models import Review
from users.serializers import UserSerializer, UserDetailSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    # ✔ user 필드는 UserDetailSerializer를 사용하여 직렬화
    # ✔ 즉, Review 모델의 user 필드가 단순한 id가 아니라 사용자 정보 전체를 포함하도록 변환됨.
    # ✔ read_only=True → POST 요청 시 클라이언트가 값을 보내지 않아도 됨 (perform_create()에서 자동 설정됨).
    # 직렬화 시키지 않으면 Django REST Framework는 User와 Restaurant 객체를 자동으로 JSON으로 변환할 수 없음
    # 따라서, 단순히 변수 이름을 바꿔도 해결되지 않음

    class Meta:
        model = Review
        fields = ['pk','user','restaurant','title','comment']

        READ_ONLY_FIELDS = ['pk','restaurant']