# Path: apps/courses/urls.py
from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailView

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug:course_slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/lessons/<slug:lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
]