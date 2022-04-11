# This file includes overrides to build the `development` environment for the LMS starting from the
# settings of the `production` environment

import json

from docker_run_production import *
from .utils import Configuration

# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

if "sentry" in LOGGING.get("handlers"):
    LOGGING["handlers"]["sentry"]["environment"] = "development"

DEBUG = True
REQUIRE_DEBUG = True

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

PIPELINE_ENABLED = False
STATICFILES_STORAGE = "openedx.core.storage.DevelopmentStorage"

ALLOWED_HOSTS = ["*"]

FEATURES["AUTOMATIC_AUTH_FOR_TESTING"] = True

# Simple JWT
SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "SIGNING_KEY": config("FONZIE_JWT_SIGNING_KEY", default="ThisIsAnExampleKeyForDevPurposeOnly"),
    "USER_ID_FIELD": "username",
    "USER_ID_CLAIM": "username",
}

# ORA2 fileupload
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = os.path.join(SHARED_ROOT, "openassessment_submissions")
ORA2_FILEUPLOAD_CACHE_ROOT = os.path.join(
    SHARED_ROOT, "openassessment_submissions_cache"
)

AUTHENTICATION_BACKENDS = config(
    "AUTHENTICATION_BACKENDS",
    default=["django.contrib.auth.backends.ModelBackend"],
    formatter=json.loads
)
