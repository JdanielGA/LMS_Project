# Path: apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Personalized User model for our project
class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, "url"):
            return self.avatar.url
        return (
            "/static/img/default-avatar.png"  # Path to a default avatar image in your static files
        )

    @property
    def is_teacher(self):
        return hasattr(self, "teacher_profile") or self.is_superuser

    def __str__(self):
        return self.username


# Student profile extending the User model
class StudentProfile(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="student_profile"
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"


# Teacher profile extending the User model
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="teacher_profile"
    )
    specialty = models.CharField(max_length=255)
    bio = models.TextField()
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"
