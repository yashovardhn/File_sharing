from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import File, EmailVerificationToken
from .serializers import UserSerializer, FileSerializer
from .permissions import IsOpsUser, IsClientUser
import uuid

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = uuid.uuid4().hex
        EmailVerificationToken.objects.create(user=user, token=token)
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        verification_token.user.is_active = True
        verification_token.user.save()
        verification_token.delete()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    except EmailVerificationToken.DoesNotExist:
        return Response({'message': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.data['username'])
        if user.user_type == 'ops' and not user.is_active:
            return Response({'message': 'Account not verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsOpsUser])
def upload_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsClientUser])
def list_files(request):
    files = File.objects.filter(user=request.user)
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsClientUser])
def download_file(request, pk):
    try:
        file = File.objects.get(pk=pk, user=request.user)
        download_url = f"{settings.FRONTEND_URL}/download-file/{file.id}?token={uuid.uuid4().hex}"
        return Response({'download-link': download_url, 'message': 'success'}, status=status.HTTP_200_OK)
    except File.DoesNotExist:
        return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
