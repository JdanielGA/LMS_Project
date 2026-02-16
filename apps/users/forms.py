# Path: apps/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, StudentProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
    
    # Clean and personalize the help text for the username and password fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = "Use at least 8 characters with mixed case."

    # Override the save method to create a StudentProfile when a new user is created
    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=commit)
            if commit:
                StudentProfile.objects.get_or_create(user=user)
            return user
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']