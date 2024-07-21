from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
