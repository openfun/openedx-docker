# This file includes overrides to build the `CI` environment for the CMS, starting from
# the settings of the `production` environment

from docker_run_production import *


DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PIPELINE_ENABLED = False
STATICFILES_STORAGE = "openedx.core.storage.DevelopmentStorage"

ALLOWED_HOSTS = ["*"]
