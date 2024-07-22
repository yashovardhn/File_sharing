from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUserAccount(AbstractUser):
    is_ops_user = models.BooleanField(default=False)

    # Set related_name to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

class File(models.Model):
    uploaded_by = models.ForeignKey(CustomUserAccount, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
