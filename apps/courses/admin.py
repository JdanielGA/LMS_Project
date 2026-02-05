# Path: apps/courses/admin.py
from django.contrib import admin
from .models import Course, Module, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'teacher', 'status')

admin.site.register(Module)
admin.site.register(Lesson)
