import pytest

from apps.users.forms import UserRegisterForm
from apps.users.models import StudentProfile, User

pytestmark = pytest.mark.django_db


def test_user_register_form_creates_profile():
    """Verify that the registration form creates a StudentProfile."""
    data = {
        "username": "new_student",
        "email": "new@test.com",
        "password1": "Pass12345",
        "password2": "Pass12345",
    }
    form = UserRegisterForm(data=data)
    assert form.is_valid()

    user = form.save()

    assert isinstance(user, User)
    assert StudentProfile.objects.filter(user=user).exists()
