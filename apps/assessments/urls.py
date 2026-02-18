# Path: apps/assessments/urls.py
from django.urls import path
from .views import AssessmentCreateView

app_name = 'assessments'

urlpatterns = [
    path('<slug:course_slug>/create/', AssessmentCreateView.as_view(), name='create'),
]