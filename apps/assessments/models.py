# Path apps/assessments/models.py
from django.db import models
from apps.courses.models import Course, Lesson
from libs.models import TimeStampedModel


class Assessment(TimeStampedModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='assessments'
    )

    lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assessments',
        help_text="Optional: Link this assessment to a specific lesson."
    )

    passing_score = models.PositiveIntegerField(
        default=70, 
        help_text="Minimum score to pass the assessment."
    )

    total_score = models.PositiveIntegerField(
        default=100, 
        help_text="Total score for the assessment."
    )

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
        ordering = ['-created_at']
        unique_together = [('course', 'title')]

class Question(TimeStampedModel):
    assessment = models.ForeignKey(
        Assessment, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    text = models.TextField(verbose_name="Question statement")
    score = models.PositiveIntegerField(
        default=10,
        help_text="Score for this question"
    )

    def __str__(self):
        return f"Question: {self.text[:50]}..."