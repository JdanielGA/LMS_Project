# Path: apps/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    # Override the save method to create a StudentProfile when a new user is created
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            StudentProfile.objects.create(user=user)
        return user