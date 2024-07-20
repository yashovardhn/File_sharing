from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.admin.sites import site, NotRegistered
from .models import File, EmailVerificationToken

User = get_user_model()

class CustomUserAdmin(DefaultUserAdmin):
    model = User
    list_display = ['username', 'email', 'user_type', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the custom UserAdmin only if not already registered
try:
    site.unregister(User)
except NotRegistered:
    pass

site.register(User, CustomUserAdmin)
site.register(File)
site.register(EmailVerificationToken)
