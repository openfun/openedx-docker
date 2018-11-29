# This file includes overrides to build the `preprod` environment for the LMS starting from the
# settings of the `production` environment

from docker_run_production import *
from .utils import Configuration

# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

LOGGING["handlers"]["sentry"]["environment"] = "preprod"

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
