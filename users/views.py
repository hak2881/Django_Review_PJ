from django.contrib.auth import login, get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, UserLoginSerializer, UserDetailSerializer


class UserCreatAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# class UserLoginAPIView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             login(request, serializer.validated_data.get('user'))
#             return Response({'message': 'login success'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 토큰기반 로그인
class UserTokenLoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]

class UserTokenLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try :
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist() # 로그아웃시 못쓰게하려고
            return Response({"message": "Logout Successfully"}, status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid Token"}, status= status.HTTP_400_BAD_REQUEST)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer

    # 로그인 처리
    def get_object(self):
        return get_object_or_404(get_user_model(), pk = self.request.user.pk)



