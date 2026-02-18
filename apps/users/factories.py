# apps/users/factories.py
import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "password123"
        self.set_password(password)

        if create:
            self.save()
