from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/admin/', AdminLogin.as_view(), name='admin-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]