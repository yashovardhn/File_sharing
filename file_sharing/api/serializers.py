# api/serializers.py
from rest_framework import serializers
from .models import User, File

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'upload_date')
