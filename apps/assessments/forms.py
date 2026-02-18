# Path: apps/assessments/forms.py
from django import forms
from .models import Assessment, Question
from apps.courses.models import Lesson


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title', 'lesson', 'passing_score', 'total_score']
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError(
                "The title must be at least 5 characters long."
            )
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        passing_score = cleaned_data.get('passing_score')
        total_score = cleaned_data.get('total_score')

        if passing_score is not None and total_score is not None:
            if passing_score > total_score:
                raise forms.ValidationError(
                    "The passing score cannot be greater than the total score."
                )
            
        if title and self.course:
            exists = Assessment.objects.filter(
                course=self.course, 
                title__iexact=title
            ).exists()
            
            if exists:
                self.add_error('title', "An assessment with this title already exists for this course.")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': f'Enter {field.label.lower()}'})
        
        if self.course:
            from apps.courses.models import Lesson
            self.fields['lesson'].queryset = Lesson.objects.filter(module__course=self.course)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'score']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Enter the question statement...'
            }),
            'score': forms.NumberInput(attrs={
                'min': '0', 
                'max': '100'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
            if field_name == 'text':
                field.widget.attrs['class'] += ' form-control--textarea'

QuestionFormSet = forms.inlineformset_factory(
    Assessment, 
    Question, 
    form=QuestionForm, 
    extra=3,
    can_delete=True
)