from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, ProfileView, get_csrf_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]