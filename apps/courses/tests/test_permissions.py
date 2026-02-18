import pytest
from django.urls import reverse

from apps.courses.factories import CourseFactory
from apps.courses.models import Enrollment
from apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_enrollment_required_mixin_fails_for_non_enrolled(client):
    """Test that if a student is NOT enrolled, they cannot view the lesson."""
    student = UserFactory()
    course = CourseFactory(status="published")
    # Create a lesson for that course
    from apps.courses.models import Lesson, Module

    module = Module.objects.create(course=course, title="M1")
    lesson = Lesson.objects.create(module=module, title="L1", slug="l1")

    client.force_login(student)
    url = reverse(
        "courses:lesson_detail", kwargs={"course_slug": course.slug, "lesson_slug": lesson.slug}
    )

    response = client.get(url)
    assert response.status_code == 302  # Redirects to course detail
    assert reverse("courses:course_detail", kwargs={"course_slug": course.slug}) in response.url


def test_enrollment_required_mixin_success(client):
    """Test that if a student IS enrolled, they can view the lesson."""
    student = UserFactory()
    course = CourseFactory(status="published")
    # Enroll the student
    Enrollment.objects.create(user=student, course=course)

    from apps.courses.models import Lesson, Module

    module = Module.objects.create(course=course, title="M1")
    lesson = Lesson.objects.create(module=module, title="L1", slug="l1")

    client.force_login(student)
    url = reverse(
        "courses:lesson_detail", kwargs={"course_slug": course.slug, "lesson_slug": lesson.slug}
    )

    response = client.get(url)
    assert response.status_code == 200  # Access granted
