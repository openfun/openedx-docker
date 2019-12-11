from glob import glob
import json
import os.path
import pkgutil

from django.utils.translation import ugettext_lazy
from django.conf import global_settings

from lms.envs.fun.utils import Configuration

from ..common import *


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

SITE_VARIANT = "cms"

# Fun-apps configuration
INSTALLED_APPS += (
    "ckeditor",
    "courses",
    "easy_thumbnails",
    "edx_gea",
    "fun",
    "haystack",
    "password_container",
    "raven.contrib.django.raven_compat",
    "selftest",
    "teachers",
    "universities",
    "videoproviders",
)

ROOT_URLCONF = "fun.cms.urls"


class LazyChoicesSorter(object):
    def __init__(self, choices):
        self.choices = choices

    def __iter__(self):
        for choice in sorted(self.choices, key=lambda peer: peer[1]):
            yield choice


# These are the allowed subtitle languages, we have the same list on Videofront server
# We remove 2 deprecated chinese language codes which do not exist on Django 1.10 VideoFront
SUBTITLE_SUPPORTED_LANGUAGES = LazyChoicesSorter(
    (code, ugettext_lazy(lang))
    for code, lang in global_settings.LANGUAGES
    if code not in ("zh-cn", "zh-tw")
)

# This constant as nothing to do with github.
# Path is used to store tar.gz courses before import process
GITHUB_REPO_ROOT = DATA_DIR

# Haystack configuration (default is minimal working configuration)
HAYSTACK_CONNECTIONS = config(
    "HAYSTACK_CONNECTIONS",
    default={
        "default": {"ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine"}
    },
    formatter=json.loads,
)

CKEDITOR_UPLOAD_PATH = "./"

# Glowbl
GLOWBL_LTI_ENDPOINT = config(
    "GLOWBL_LTI_ENDPOINT", default="http://ltiapps.net/test/tp.php"
)
GLOWBL_LTI_KEY = config("GLOWBL_LTI_KEY", default="jisc.ac.uk")
GLOWBL_LTI_SECRET = config("GLOWBL_LTI_SECRET", default="secret")
GLOWBL_LTI_ID = config("GLOWBL_LTI_ID", default="testtoolconsumer")
GLOWBL_LAUNCH_URL = config(
    "GLOWBL_LAUNCH_URL", default="http://ltiapps.net/test/tp.php"
)
GLOWBL_COLL_OPT = config("GLOWBL_COLL_OPT", default="FunMoocJdR")

# ### FUN-APPS SETTINGS ###

# This is dist-packages path where all fun-apps are
FUN_BASE_ROOT = path(os.path.dirname(pkgutil.get_loader("funsite").filename))

# Add 'theme/cms/templates' directory to MAKO template finder to override some
# CMS templates
MAKO_TEMPLATES["main"] = [FUN_BASE_ROOT / "fun/templates/cms"] + MAKO_TEMPLATES["main"]

# JS static override
DEFAULT_TEMPLATE_ENGINE["DIRS"].append(FUN_BASE_ROOT / "funsite/templates/lms")

# Generic LTI configuration
LTI_XBLOCK_CONFIGURATIONS = config(
    "LTI_XBLOCK_CONFIGURATIONS", default=[], formatter=json.loads
)

# Locale paths
# Here we rewrite LOCAL_PATHS to give precedence to our applications above edx-platform's ones,
# then we add xblocks which provide translations as there is no native mechanism to handle this
# See Xblock i18n: http://www.libremente.eu/2017/12/06/edx-translation/
LOCALIZED_FUN_APPS = ["courses", "universities", "videoproviders"]
LOCALE_PATHS = [FUN_BASE_ROOT / app / "locale" for app in LOCALIZED_FUN_APPS]
LOCALE_PATHS.append(REPO_ROOT / "conf/locale")  # edx-platform locales
LOCALE_PATHS.append(path(pkgutil.get_loader("proctor_exam").filename) / "locale")
