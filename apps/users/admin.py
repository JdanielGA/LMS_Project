from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StudentProfile, User


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = "Student Profile"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (StudentProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("extra_field_if_any",)}),)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
