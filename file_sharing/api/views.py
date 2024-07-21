# api/views.py
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, File, EmailVerificationToken
from .serializers import UserSerializer, FileSerializer
from .permissions import IsOpsUser, IsClientUser
import hashlib
import hmac
import time

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = EmailVerificationToken.objects.create(user=user, token=hashlib.sha256(f'{user.username}{time.time()}'.encode()).hexdigest())
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: http://localhost:8000/api/verify-email/{token.token}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

class VerifyEmailView(APIView):
    def get(self, request, token):
        token_obj = get_object_or_404(EmailVerificationToken, token=token)
        if token_obj.is_used:
            return Response({'message': 'Token already used'}, status=status.HTTP_400_BAD_REQUEST)
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.is_used = True
        token_obj.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsOpsUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_queryset(self):
        return File.objects.all()

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, pk):
        file = get_object_or_404(File, pk=pk)
        url = f'http://localhost:8000/api/download-file/{file.id}/{hashlib.sha256(f"{file.id}{request.user.id}".encode()).hexdigest()}'
        return Response({'download-link': url, 'message': 'success'}, status=status.HTTP_200_OK)

class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, file_id, token):
        file = get_object_or_404(File, pk=file_id)
        expected_token = hashlib.sha256(f'{file.id}{request.user.id}'.encode()).hexdigest()
        if hmac.compare_digest(expected_token, token):
            response = HttpResponse(file.file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={file.file.name}'
            return response
        return Response({'error': 'Access Denied'}, status=status.HTTP_403_FORBIDDEN)
