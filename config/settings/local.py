# Path: config/settings/local.py

import socket

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@evolaris.academy"

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]


hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
