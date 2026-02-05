# Path: apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Personalized User model for our project
class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
        )
    
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

# Student profile extending the User model
class StudentProfile(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Student: {self.user.username}"
    
# Teacher profile extending the User model
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    specialty = models.CharField(max_length=255)
    bio = models.TextField()
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Teacher: {self.user.username}"