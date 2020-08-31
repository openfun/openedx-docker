# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile
from .docker_run_development import *

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "default",
    },
    "general": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "general",
    },
    "celery": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "celery",
    },
    "mongo_metadata_inheritance": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "mongo_metadata_inheritance",
    },
    "openassessment_submissions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "openassessment_submissions",
    },
    "loc_cache": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "loc_cache",
    },
    # Cache backend used by Django 1.8 storage backend while processing static files
    "staticfiles": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "staticfiles",
    },
}
