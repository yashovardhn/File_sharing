from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import File, EmailVerificationToken

User = get_user_model()

# Check if the model is already registered
if not admin.site.is_registered(User):
    admin.site.register(User)

admin.site.register(File)
admin.site.register(EmailVerificationToken)
