from django.urls import path
from users import views

urlpatterns =[
    path('signup/', views.UserCreatAPIView.as_view(), name='user-signup'),
    path('login/', views.UserTokenLoginAPIView.as_view(), name='user-login'),
    path('logout/', views.UserTokenLogoutAPIView.as_view(), name='user-logout'),
    path('detail/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
]