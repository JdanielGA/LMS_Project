# apps/assessments/tests/test_views.py
import pytest
from django.urls import reverse

from apps.courses.factories import CourseFactory
from apps.users.factories import UserFactory
from apps.users.models import TeacherProfile

pytestmark = pytest.mark.django_db


def test_create_assessment_with_questions_post(client):
    """
    Integration Test: Verifies that a teacher can create an exam
    with its questions in a single request.
    """
    # 1. Setup with Factories
    teacher = UserFactory()
    TeacherProfile.objects.create(user=teacher)
    course = CourseFactory(teacher=teacher)
    client.force_login(teacher)

    url = reverse("assessments:create", kwargs={"course_slug": course.slug})

    # 2. Form data (Exam + Management Form for the Formset)
    data = {
        "title": "Midterm Exam",
        "passing_score": 70,
        "total_score": 100,
        # Management form: essential for the formset
        "questions-TOTAL_FORMS": "2",
        "questions-INITIAL_FORMS": "0",
        "questions-MIN_NUM_FORMS": "0",
        "questions-MAX_NUM_FORMS": "1000",
        # Question 1 data
        "questions-0-text": "What is Django?",
        "questions-0-score": 50,
        # Question 2 data
        "questions-1-text": "How do you create a model?",
        "questions-1-score": 50,
    }

    response = client.post(url, data)

    # 3. Verifications
    assert response.status_code == 302  # Redirect on success
    assert course.assessments.count() == 1
    assessment = course.assessments.first()
    assert assessment.questions.count() == 2
