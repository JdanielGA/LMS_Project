# Path: apps/courses/factories.py

import factory

from apps.courses.models import Course
from apps.users.factories import UserFactory


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"course de Python {n}")
    slug = factory.Sequence(lambda n: f"course-python-{n}")
    description = factory.Faker("paragraph")
    teacher = factory.SubFactory(UserFactory)
    status = "published"
