# Path: apps/courses/admin.py
from django.contrib import admin

from .models import Course, Enrollment, Lesson, Module, UserLessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "teacher", "status", "total_enrollments")
    list_filter = ("status", "teacher")
    search_fields = ("title", "description")
    list_editable = ("status",)
    ordering = ("-created_at",)

    def total_enrollments(self, obj):
        return obj.enrollments.count()

    total_enrollments.short_description = "Inscriptions"


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    ordering = ("course", "order")
    search_fields = ("title", "course__title")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "module", "order", "has_video")
    list_filter = ("module__course",)
    ordering = ("module", "order")
    search_fields = ("title", "content")

    def has_video(self, obj):
        return bool(obj.video_url)

    has_video.boolean = True  # Display as a boolean icon
    has_video.short_description = "Video"


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "status", "enrolled_at", "grade")
    list_filter = ("status", "course", "enrolled_at")
    search_fields = ("user__username", "user__email", "course__title")
    readonly_fields = ("enrolled_at", "created_at", "updated_at")
    date_hierarchy = "enrolled_at"
    list_editable = ("status",)


@admin.register(UserLessonProgress)
class UserLessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "is_completed", "completed_at")
    list_filter = ("is_completed", "lesson__module__course")
    search_fields = ("user__username", "lesson__title")
    readonly_fields = ("created_at", "updated_at", "completed_at")
    date_hierarchy = "completed_at"
