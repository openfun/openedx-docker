# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile for the production image of the edxapp LMS

from openedx.core.lib.derived import derive_settings
from path import Path as path

from .docker_run_production import *
from .utils import Configuration

# Load custom configuration parameters
config = Configuration()

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}

STATIC_ROOT = path("/edx/app/edxapp/staticfiles")

# Allow setting a custom theme
DEFAULT_SITE_THEME = config("DEFAULT_SITE_THEME", default=None)

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


########################## Derive Any Derived Settings  #######################

derive_settings(__name__)
