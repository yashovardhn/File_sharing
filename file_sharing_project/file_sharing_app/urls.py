from. import views
from django.urls import path
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('upload-file/', views.upload_file_view, name='upload_file'),
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('email-verify/<int:user_id>/', views.email_verify_view, name='email_verify'),
    path('download-file/<int:file_id>/', views.download_file_view, name='download_file'),
    path('list-files/', views.list_files_view, name='list_files'),
]