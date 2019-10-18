from ..common import *

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
    "selftest",
    "password_container",
    "raven.contrib.django.raven_compat",
    "edx_gea",
)

ROOT_URLCONF = "fun.cms.urls"

# This constant as nothing to do with github.
# Path is used to store tar.gz courses before import process
GITHUB_REPO_ROOT = DATA_DIR

# ### THIRD-PARTY SETTINGS ###
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine",
        "URL": "http://localhost:9200/",
        "INDEX_NAME": "haystack",
    }
}

CKEDITOR_UPLOAD_PATH = "./"

# ### FUN-APPS SETTINGS ###
# -- Base --
FUN_BASE_ROOT = path(os.path.dirname(imp.find_module("funsite")[1]))

# Add 'theme/cms/templates' directory to MAKO template finder to override some
# CMS templates
MAKO_TEMPLATES["main"] = [FUN_BASE_ROOT / "fun/templates/cms"] + MAKO_TEMPLATES["main"]

# JS static override
DEFAULT_TEMPLATE_ENGINE["DIRS"].append(FUN_BASE_ROOT / "funsite/templates/lms")

# Video front allowed languages
SUBTITLE_SUPPORTED_LANGUAGES = "fr"

# Generic LTI configuration
LTI_XBLOCK_CONFIGURATIONS = [{"display_name": "LTI consumer"}]
