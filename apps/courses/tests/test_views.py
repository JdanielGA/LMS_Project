# Path: apps/courses/tests/test_views.py
import pytest
from django.urls import reverse

from apps.courses.factories import CourseFactory
from apps.courses.models import Course, Lesson, Module

pytestmark = pytest.mark.django_db

# --- REUSABLE FIXTURES ---


@pytest.fixture
def teacher(db):
    from apps.users.models import TeacherProfile, User

    # Assign a unique email to the fixture
    u = User.objects.create_user(username="teacher_user", email="teacher@evolaris.uk", password="p")
    TeacherProfile.objects.create(user=u, specialty="Django")
    return u


@pytest.fixture
def course(teacher):
    return Course.objects.create(title="Pro Course", slug="pro", teacher=teacher)


@pytest.fixture
def lesson(course):
    module = Module.objects.create(course=course, title="M1", order=1)
    return Lesson.objects.create(module=module, title="L1", slug="l1", order=1)


# --- TESTS ---


def test_course_list_view_accessible_by_anyone(client):
    url = reverse("courses:course_list")
    assert client.get(url).status_code == 200


def test_course_create_restricted_to_teachers(client):
    from django.urls import reverse

    from apps.users.models import User

    student = User.objects.create_user(
        username="s",
        email="s@test.com",  # Add email
        password="p",
    )

    client.force_login(student)

    url = reverse("courses:course_create")
    response = client.get(url)

    assert response.status_code == 302

    assert response.url == reverse("courses:course_list")


def test_teacher_can_access_course_create(client, teacher):
    client.force_login(teacher)
    assert client.get(reverse("courses:course_create")).status_code == 200


def test_student_cannot_view_lesson_without_enrollment(client, lesson):
    from apps.users.models import User

    student = User.objects.create_user(username="stranger", password="p")
    client.force_login(student)

    url = reverse(
        "courses:lesson_detail",
        kwargs={"course_slug": lesson.module.course.slug, "lesson_slug": lesson.slug},
    )
    response = client.get(url)

    # Verify the security redirection
    assert response.status_code == 302
    assert "courses/pro/" in response.url  # Should redirect back to course detail


def test_course_list_view_with_factory(client):
    CourseFactory.create_batch(5)

    url = reverse("courses:course_list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["courses"].count() == 5


def test_course_list_only_shows_published(client):
    CourseFactory(title="Visible", status="published")
    CourseFactory(title="Hidden", status="draft")

    url = reverse("courses:course_list")
    response = client.get(url)

    assert response.context["courses"].count() == 1
    assert response.context["courses"][0].title == "Visible"
