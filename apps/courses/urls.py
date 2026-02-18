# Path: apps/courses/urls.py
from django.urls import path

from .views import (
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseListView,
    CourseUpdateView,
    LessonDetailView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("create/", CourseCreateView.as_view(), name="course_create"),
    path("<slug:course_slug>/", CourseDetailView.as_view(), name="course_detail"),
    path("<slug:course_slug>/edit/", CourseUpdateView.as_view(), name="course_update"),
    path("<slug:course_slug>/delete/", CourseDeleteView.as_view(), name="course_delete"),
    path(
        "<slug:course_slug>/lessons/<slug:lesson_slug>/",
        LessonDetailView.as_view(),
        name="lesson_detail",
    ),
]
