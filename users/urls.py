from django.urls import path
from users import views

urlpatterns =[
    path('signup/', views.UserCreatAPIView.as_view(), name='user-signup'),
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('detail/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),

]