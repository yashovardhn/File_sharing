# api/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import FileExtensionValidator
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ops', 'Operation User'),
        ('client', 'Client User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='api_user_set',  # Changed related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='api_user_set',  # Changed related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='uploads/', 
        validators=[FileExtensionValidator(allowed_extensions=['pptx', 'docx', 'xlsx'])]
    )
    upload_date = models.DateTimeField(auto_now_add=True)

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
