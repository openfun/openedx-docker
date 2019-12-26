import json

from lms.envs.fun.utils import Configuration, prefer_fun_video

from ..common import *


# Load custom configuration parameters from yaml files
config = Configuration(os.path.dirname(__file__))

# Fun-apps configuration
INSTALLED_APPS += (
    "fun",
    "videoproviders",
    "teachers",
    "courses",
    "haystack",
    "universities",
    "easy_thumbnails",
    "ckeditor",
    "raven.contrib.django.raven_compat",
)

ROOT_URLCONF = "fun.cms.urls"

# ### THIRD-PARTY SETTINGS ###

# Haystack configuration (default is minimal working configuration)
HAYSTACK_CONNECTIONS = config(
    "HAYSTACK_CONNECTIONS",
    default={
        "default": {"ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine"}
    },
    formatter=json.loads,
)

CKEDITOR_UPLOAD_PATH = "./"

# ### FUN-APPS SETTINGS ###
# -- Base --
FUN_BASE_ROOT = path(os.path.dirname(imp.find_module("funsite")[1]))

# Add 'theme/cms/templates' directory to MAKO template finder to override some
# CMS templates
MAKO_TEMPLATES["main"] = [FUN_BASE_ROOT / "fun/templates/cms"] + MAKO_TEMPLATES["main"]

# Generic LTI configuration
LTI_XBLOCK_CONFIGURATIONS = [{"display_name": "LTI consumer"}]

# Force Edx to use `libcast_xblock` as default video player
# in the studio (big green button) and if any xblock is called `video`
XBLOCK_SELECT_FUNCTION = prefer_fun_video
