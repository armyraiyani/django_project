from django.urls import path
from .views import AdminLoginView, CreateUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
]