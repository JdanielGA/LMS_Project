from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ex. Master in Python Development'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }