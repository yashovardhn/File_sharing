from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.decorators import user_passes_test

from .models import File
from .serializers import FileSerializer
from .utils import generate_download_url

class FileListCreateAPIView(ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def test_func(self):
        file = self.get_object()
        return self.request.user == file.uploaded_by

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists.'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists.'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            # Generate and send verification email
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            link = 'http://localhost:8000/accounts/api/users/verify/' + urlsafe_base64_encode(smart_bytes(user.pk)) + '/' + token

            email_subject = 'Verify your account'
            email_body = f'Hello {user.username},\n\nPlease click the link below to verify your account:\n\n{link}\n\nIf you did not request this email, please ignore it.\n\nRegards,\nThe Team'

            email = EmailMessage(email_subject, email_body, to=[email])
            email.send()

            return Response({'message': 'Account created. Please verify your email.'}, status=201)
        else:
            return Response({'error': 'Passwords do not match.'}, status=400)
    else:
        return render(request, 'signup.html')

def verify_email(request, uidb64, token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid token.'}, status=400)

        user.is_active = True
        user.save()

        return Response({'message': 'Email verified. You can now log in.'}, status=200)
    except Exception as e:
        return Response({'error': 'An error occurred while verifying your email.'}, status=500)

def download_file(request, file_id):
    file = File.objects.get(pk=file_id)

    if file.uploaded_by == request.user:
        download_url = generate_download_url(file)
        return Response({'download-link': download_url, 'message': 'success'})
    else:
        return Response({'error': 'Unauthorized access.'}, status=401)

@user_passes_test(lambda user: user.is_ops_user)
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')

        if file and file_type in ['pptx', 'docx', 'xlsx']:
            file_serializer = FileSerializer(data=request.POST, files=request.FILES)

            if file_serializer.is_valid():
                file_serializer.save(uploaded_by=request.user)
                return JsonResponse({'message': 'File uploaded successfully.'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid file or file type.'}, status=400)
        else:
            return JsonResponse({'error': 'No file selected or invalid file type.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
