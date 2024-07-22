from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileListCreateAPIView, FileRetrieveUpdateDestroyAPIView

router = DefaultRouter()
router.register(r'files', FileListCreateAPIView, basename='file-create')
router.register(r'files/(?P<pk>\d+)', FileRetrieveUpdateDestroyAPIView, basename='file-detail')

urlpatterns = [
    path('', include(router.urls)),
]
