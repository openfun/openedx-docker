# This is a minimal settings file allowing us to run "update_assets"
# in the Dockerfile for the production image of the edxapp CMS

from openedx.core.lib.derived import derive_settings

from lms.envs.fun.utils import Configuration
from path import Path as path

from ..common import *

# Load custom configuration parameters
config = Configuration()

DATABASES = {"default": {}}

XQUEUE_INTERFACE = {"url": None, "django_auth": None}

# We need to override STATIC_ROOT because for CMS, edX appends the value of
# "EDX_PLATFORM_REVISION" to it by default and we don't want to use this.
# We should use Django's ManifestStaticFilesStorage for this purpose.
STATIC_URL = "/static/studio/"
STATIC_ROOT = path("/edx/app/edxapp/staticfiles/studio")

# Generate webpack stats file in the project's root and not in STATIC_ROOT or
# else, we'll be forced to copy it manually as it won't be collected.
WEBPACK_LOADER["DEFAULT"][
    "STATS_FILE"
] = "/edx/app/edxapp/edx-platform/webpack-stats-cms.json"

# Allow setting a custom theme
DEFAULT_SITE_THEME = config("DEFAULT_SITE_THEME", default=None)

########################## Derive Any Derived Settings  #######################

derive_settings(__name__)
