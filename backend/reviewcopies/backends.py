import re

from django.contrib.auth.backends import ModelBackend
from faker import Faker

from reviewcopies.models import User

DEFAULT_PASSWORD = "motdepasse"


class LDAPTestModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        res = super().authenticate(request, username, password, **kwargs)

        # User exists and authentication succeeded
        if res is not None:
            return res

        # User exists but authentication failed
        if User.objects.filter(username=username).exists():
            return None

        if re.match(r"^(h|e)[0-9]{6}[0-9]*$", username):
            fake = Faker("fr")
            User.objects.create_user(
                username,
                password=DEFAULT_PASSWORD,
                email=fake.email(),
                last_name=fake.last_name(),
                first_name=fake.first_name(),
            )

        return super().authenticate(request, username, password, **kwargs)
