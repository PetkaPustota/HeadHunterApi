from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserCreateView, LogoutView

urlpatterns = [
    path('create/', UserCreateView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]