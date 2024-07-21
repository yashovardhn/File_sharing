# api/urls.py
from django.urls import path
from .views import SignUpView, VerifyEmailView, LoginView, FileUploadView, FileListView, FileDownloadView, DownloadFileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-file/', FileUploadView.as_view(), name='upload-file'),
    path('list-files/', FileListView.as_view(), name='list-files'),
    path('download-file/<int:pk>/', FileDownloadView.as_view(), name='download-file'),
    path('download-file/<int:file_id>/<str:token>/', DownloadFileView.as_view(), name='actual-download-file'),
]
