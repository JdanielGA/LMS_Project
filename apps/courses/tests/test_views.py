# Path: apps/courses/tests/test_views.py
import pytest
from django.urls import reverse
from apps.courses.models import Course, Module, Lesson # Movido al top

pytestmark = pytest.mark.django_db

# --- FIXTURES PARA REUTILIZAR ---

@pytest.fixture
def teacher(db):
    from apps.users.models import User, TeacherProfile
    # Asignamos un email único a la fixture
    u = User.objects.create_user(
        username="teacher_user", 
        email="teacher@evolaris.uk", 
        password="p"
    )
    TeacherProfile.objects.create(user=u, specialty="Django")
    return u

@pytest.fixture
def course(teacher):
    return Course.objects.create(title="Pro Course", slug="pro", teacher=teacher)

@pytest.fixture
def lesson(course):
    module = Module.objects.create(course=course, title="M1", order=1)
    return Lesson.objects.create(module=module, title="L1", slug="l1", order=1)

# --- LOS TESTS ---

def test_course_list_view_accessible_by_anyone(client):
    url = reverse('courses:course_list')
    assert client.get(url).status_code == 200

def test_course_create_restricted_to_teachers(client):
    from apps.users.models import User
    student = User.objects.create_user(
        username="s", 
        email="s@test.com", # Añadir email
        password="p"
    )
    client.force_login(student)
    assert client.get(reverse('courses:course_create')).status_code == 403

def test_teacher_can_access_course_create(client, teacher):
    client.force_login(teacher)
    assert client.get(reverse('courses:course_create')).status_code == 200

def test_student_cannot_view_lesson_without_enrollment(client, lesson):
    from apps.users.models import User
    student = User.objects.create_user(username="stranger", password="p")
    client.force_login(student)
    
    url = reverse('courses:lesson_detail', kwargs={
        'course_slug': lesson.module.course.slug, 
        'lesson_slug': lesson.slug
    })
    response = client.get(url)
    
    # Verificamos la redirección de seguridad
    assert response.status_code == 302
    assert "courses/pro/" in response.url # Debe volver al detalle del curso