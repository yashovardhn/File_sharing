# api/permissions.py
from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'ops'

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'client'
