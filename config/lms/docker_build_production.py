# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile for the production image of the edxapp LMS

from openedx.core.lib.derived import derive_settings
from path import Path as path

from ..common import *
from .utils import Configuration

# Load custom configuration parameters
config = Configuration()

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}

STATIC_ROOT = path("/edx/app/edxapp/staticfiles")

# Generate webpack stats file in the project's root and not in STATIC_ROOT or
# else, we'll be forced to copy it manually as it won't be collected.
WEBPACK_LOADER["DEFAULT"][
    "STATS_FILE"
] = "/edx/app/edxapp/edx-platform/webpack-stats-lms.json"

# Allow setting a custom theme
DEFAULT_SITE_THEME = config("DEFAULT_SITE_THEME", default=None)

########################## Derive Any Derived Settings  #######################

derive_settings(__name__)
