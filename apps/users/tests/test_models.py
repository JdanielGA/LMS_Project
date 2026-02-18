# Path: apps/users/tests/test_models.py
import pytest

from apps.users.models import TeacherProfile, User

# Mark database access
pytestmark = pytest.mark.django_db


def test_user_is_teacher_property_false_by_default():
    """
    Unit Test: A new user should not be a teacher by default.
    """
    user = User.objects.create_user(
        username="student_test", email="student@evolaris.uk", password="password123"
    )

    assert user.is_teacher is False
    # If you implemented Signals, this should pass:
    # assert StudentProfile.objects.filter(user=user).exists()


def test_user_is_teacher_property_true_with_profile():
    """
    Unit Test: The is_teacher property should be True if a TeacherProfile exists.
    """
    user = User.objects.create_user(
        username="teacher_test", email="teacher@evolaris.uk", password="password123"
    )

    # Create the teacher profile
    TeacherProfile.objects.create(user=user, bio="Expert in Python 3.14")

    # Important: Refresh the object from the DB to detect the new attribute
    user.refresh_from_db()
    assert user.is_teacher is True


def test_superuser_is_teacher_regardless_of_profile():
    """
    Unit Test: Administrators always have teacher status.
    """
    admin = User.objects.create_superuser(
        username="admin_test", email="admin@evolaris.uk", password="password123"
    )

    assert admin.is_teacher is True
    # Verify that a TeacherProfile is not required to return True
    assert not hasattr(admin, "teacher_profile")
