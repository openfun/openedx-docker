import imp
import json
import os.path

from ..common import *
from .utils import Configuration


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

# Fun-apps configuration
INSTALLED_APPS += (
    "rest_framework.authtoken",
    "backoffice",
    "fun",
    "fun_api",
    "fun_instructor",
    "course_dashboard",
    "courses",
    "courses_api",
    "course_pages",
    "universities",
    "videoproviders",
    "bootstrapform",
    "raven.contrib.django.raven_compat",
    "pure_pagination",
    "selftest",
    "teachers",
    "edx_gea",
)

ROOT_URLCONF = "fun.lms.urls_wb"

# ### THIRD-PARTY SETTINGS ###

# Haystack configuration (default is minimal working configuration)
HAYSTACK_CONNECTIONS = config(
    "HAYSTACK_CONNECTIONS",
    default={
        "default": {"ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine"}
    },
    formatter=json.loads,
)

# ### FUN-APPS SETTINGS ###
# -- Base --
FUN_BASE_ROOT = path(os.path.dirname(imp.find_module("funsite")[1]))
SHARED_ROOT = DATA_DIR / "shared"

# Add FUN applications templates directories to MAKO template finder before edX's ones
MAKO_TEMPLATES["main"] = [
    # overrides template in edx-platform/lms/templates
    FUN_BASE_ROOT
    / "course_dashboard/templates"
] + MAKO_TEMPLATES["main"]

FUN_SMALL_LOGO_RELATIVE_PATH = "funsite/images/logos/fun61.png"
FUN_BIG_LOGO_RELATIVE_PATH = "funsite/images/logos/fun195.png"

# -- Certificates
CERTIFICATE_BASE_URL = "/attestations/"
CERTIFICATES_DIRECTORY = "/edx/var/edxapp/attestations/"
FUN_LOGO_PATH = FUN_BASE_ROOT / "funsite/static" / FUN_BIG_LOGO_RELATIVE_PATH
STUDENT_NAME_FOR_TEST_CERTIFICATE = "Test User"

# Used by pure-pagination app,
# https://github.com/jamespacileo/django-pure-pagination for information about
# the constants :
# https://camo.githubusercontent.com/51defa6771f5db2826a1869eca7bed82d9fb3120/687474703a2f2f692e696d6775722e636f6d2f4c437172742e676966
PAGINATION_SETTINGS = {
    # same formatting as in github issues, seems to be sane.
    "PAGE_RANGE_DISPLAYED": 4,
    "MARGIN_PAGES_DISPLAYED": 2,
}

NUMBER_DAYS_TOO_LATE = 31
