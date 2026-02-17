# Path: apps/courses/managers.py
from django.db import models
from django.db.models import Count

class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')
    
    def with_student_count(self):
        return self.annotate(student_count=Count('enrollments'))
    
class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def popular(self):
        return self.get_queryset().published().with_student_count().order_by('-student_count')