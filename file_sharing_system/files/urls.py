# file_sharing_system/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify-email/', views.verify_email, name='verify-email'),
    path('login/', views.login, name='login'),
    path('upload-file/', views.upload_file, name='upload-file'),
    path('list-files/', views.list_files, name='list-files'),
    path('download-file/<int:pk>/', views.download_file, name='download-file'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


