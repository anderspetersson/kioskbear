import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kioskbear",
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_SERVICE_HOST"),
        "PORT": os.environ.get("POSTGRES_SERVICE_PORT"),
        "CONN_MAX_AGE": 600,
    }
}

sentry_sdk.init(
    dsn="https://3e761fef8fb3324856226151e917f7b7@o420303.ingest.sentry.io/4505696508575744",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production,
    profiles_sample_rate=0.1,
)

# Email
DEFAULT_FROM_EMAIL = "Kioskbear <info+noreply@mg.kioskbear.com>"
SERVER_EMAIL = "Kioskbear <info+noreply@mg.kioskbear.com>"
EMAIL_BACKEND: str = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
