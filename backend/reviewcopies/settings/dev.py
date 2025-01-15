from reviewcopies.settings.base import *  # noqa

AUTHENTICATION_BACKENDS = ["reviewcopies.backends.LDAPTestModelBackend"]

INSTALLED_APPS += ["django_extensions"]  # noqa
