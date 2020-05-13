# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile
from .docker_run_production import *

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}
