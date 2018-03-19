from .common import *

# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}
