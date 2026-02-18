# Path apps/users/tests/conftest.py
import pytest

from apps.users.models import User


@pytest.fixture
def base_user(db):
    """Fixture that provides a regular user."""
    return User.objects.create_user(
        username="base_user", email="user@test.com", password="password123"
    )


@pytest.fixture
def teacher_user(db):
    """Fixture that provides a user with a teacher profile."""
    from apps.users.models import TeacherProfile

    user = User.objects.create_user(username="teacher", email="t@test.com", password="p")
    TeacherProfile.objects.create(user=user, bio="Senior Tutor")
    return user
