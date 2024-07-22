# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import File 
import uuid
# from .models import File  <-- remove this line
# from .forms import FileUploadForm  <-- remove this line

@login_required
def login_view(request):
    return JsonResponse({'message': 'Logged in successfully'})

@login_required
def upload_file_view(request):
    if request.user.role != 'ops':
        return JsonResponse({'error': 'Only ops users can upload files'}, status=403)
    from .forms import FileUploadForm  # import it here instead
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            return JsonResponse({'message': 'File uploaded successfully'})
        return JsonResponse({'error': 'Invalid file type'}, status=400)
    return render(request, 'upload_file.html', {'form': FileUploadForm()})

# rest of the code

def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username, password, role='client')
        return JsonResponse({'message': 'User created successfully', 'encrypted_url': f'https://example.com/verify-email/{user.id}'}), 201
    return render(request, 'sign_up.html')

@login_required
def email_verify_view(request, user_id):
    user = User.objects.get(id=user_id)
    if user:
        user.email_verified = True
        user.save()
        return JsonResponse({'message': 'Email verified successfully'})
    return JsonResponse({'error': 'Invalid user ID'}, status=404)

@login_required
def download_file_view(request, file_id):
    if request.user.role != 'client':
        return JsonResponse({'error': 'Only client users can download files'}, status=403)
    file = File.objects.get(id=file_id)
    if file:
        encrypted_url = f'https://example.com/download-file/{file_id}/{uuid.uuid4()}'
        return JsonResponse({'download-link': encrypted_url, 'message': 'success'})
    return JsonResponse({'error': 'File not found'}, status=404)

@login_required
def list_files_view(request):
    if request.user.role != 'client':
        return JsonResponse({'error': 'Only client users can list files'}, status=403)
    files = File.objects.all()
    return JsonResponse([{'id': file.id, 'filename': file.filename} for file in files], safe=False)