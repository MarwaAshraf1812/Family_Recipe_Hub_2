from django.urls import path
from .views import UserRegistrationView, UserActivationView, Login

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<str:token>/', UserActivationView.as_view(), name='activate'),
    path('login/', Login.as_view(), name='login')
]
