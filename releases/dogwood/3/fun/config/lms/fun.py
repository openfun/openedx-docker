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

SITE_VARIANT = "lms"

# Environment's name displayed in FUN's backoffice
ENVIRONMENT = config("ENVIRONMENT", default="no set")

BASE_ROOT = path("/edx/app/edxapp/")

# Fun-apps configuration
INSTALLED_APPS += (
    "backoffice",
    "bootstrapform",
    "ckeditor",
    "contact",
    "course_dashboard",
    "course_pages",
    "courses_api",
    "courses",
    "easy_thumbnails",
    "edx_gea",
    "forum_contributors",
    "fun_api",
    "fun_certificates",
    "fun_instructor",
    "fun",
    "funsite",
    "haystack",
    "newsfeed",
    "password_container",
    "payment_api",
    "payment",
    "pure_pagination",
    "raven.contrib.django.raven_compat",
    "rest_framework.authtoken",
    "selftest",
    "teachers",
    "universities",
    "videoproviders",
)

ROOT_URLCONF = "fun.lms.urls"

# Haystack configuration (default is minimal working configuration)
HAYSTACK_CONNECTIONS = config(
    "HAYSTACK_CONNECTIONS",
    default={
        "default": {"ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine"}
    },
    formatter=json.loads,
)

CKEDITOR_UPLOAD_PATH = "./"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            [
                "Undo",
                "Redo",
                "-",
                "Bold",
                "Italic",
                "Underline",
                "-",
                "Link",
                "Unlink",
                "Anchor",
                "-",
                "Format",
                "-",
                "SpellChecker",
                "Scayt",
                "-",
                "Maximize",
            ],
            [
                "HorizontalRule",
                "-",
                "Table",
                "-",
                "BulletedList",
                "NumberedList",
                "-",
                "Cut",
                "Copy",
                "Paste",
                "PasteText",
                "PasteFromWord",
                "-",
                "SpecialChar",
                "-",
                "Source",
            ],
        ],
        "toolbarCanCollapse": False,
        "entities": False,
        "width": 955,
        "uiColor": "#9AB8F3",
    },
    "news": {
        # Redefine path where the news images/files are uploaded. This would
        # better be done at runtime with the 'reverse' function, but
        # unfortunately there is no way around defining this in the settings
        # file.
        "filebrowserUploadUrl": "/news/ckeditor/upload/",
        "filebrowserBrowseUrl": "/news/ckeditor/browse/",
        "toolbar_Full": [
            [
                "Styles",
                "Format",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker",
                "Undo",
                "Redo",
            ],
            ["Image", "Flash", "Table", "HorizontalRule"],
            ["NumberedList", "BulletedList", "Blockquote", "TextColor", "BGColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
        ],
    },
}

# ### FUN-APPS SETTINGS ###

# This is dist-packages path where all fun-apps are
FUN_BASE_ROOT = path(os.path.dirname(pkgutil.get_loader("funsite").filename))
SHARED_ROOT = DATA_DIR / "shared"

# Add FUN applications templates directories to MAKO template finder before edX's ones
MAKO_TEMPLATES["main"] = [
    # overrides template in edx-platform/lms/templates
    FUN_BASE_ROOT / "funsite/templates/lms",
    FUN_BASE_ROOT / "funsite/templates",
    FUN_BASE_ROOT / "course_pages/templates",
    FUN_BASE_ROOT / "payment/templates",
    FUN_BASE_ROOT / "course_dashboard/templates",
    FUN_BASE_ROOT / "newsfeed/templates",
    FUN_BASE_ROOT / "fun_certificates/templates",
] + MAKO_TEMPLATES["main"]

# JS static override
DEFAULT_TEMPLATE_ENGINE["DIRS"].append(FUN_BASE_ROOT / "funsite/templates/lms")

FUN_SMALL_LOGO_RELATIVE_PATH = "funsite/images/logos/funmooc173.png"
FUN_BIG_LOGO_RELATIVE_PATH = "funsite/images/logos/funmoocfp.png"

# Locale paths
# Here we rewrite LOCAL_PATHS to give precedence to our applications above edx-platform's ones,
# then we add xblocks which provide translations as there is no native mechanism to handle this
# See Xblock i18n: http://www.libremente.eu/2017/12/06/edx-translation/
LOCALIZED_FUN_APPS = [
    "backoffice",
    "contact",
    "course_dashboard",
    "course_pages",
    "courses",
    "fun_api",
    "fun_certificates",
    "funsite",
    "newsfeed",
    "payment",
    "universities",
    "videoproviders",
]
LOCALE_PATHS = [FUN_BASE_ROOT / app / "locale" for app in LOCALIZED_FUN_APPS]
LOCALE_PATHS.append(REPO_ROOT / "conf/locale")  # edx-platform locales
LOCALE_PATHS.append(path(pkgutil.get_loader("proctor_exam").filename) / "locale")

# -- Certificates
CERTIFICATE_BASE_URL = "/attestations/"
CERTIFICATES_DIRECTORY = "/edx/var/edxapp/attestations/"
FUN_LOGO_PATH = FUN_BASE_ROOT / "funsite/static" / FUN_BIG_LOGO_RELATIVE_PATH
FUN_ATTESTATION_LOGO_PATH = (
    FUN_BASE_ROOT / "funsite/static" / "funsite/images/logos/funmoocattest.png"
)
STUDENT_NAME_FOR_TEST_CERTIFICATE = "Test User"

# Course image thumbnail sizes
FUN_THUMBNAIL_OPTIONS = {
    "small": {"size": (270, 152), "crop": "smart"},
    "big": {"size": (337, 191), "crop": "smart"},
    "about": {"size": (730, 412), "crop": "scale"},
    "facebook": {
        "size": (600, 315),
        "crop": "smart",
    },  # https://developers.facebook.com/docs/sharing/best-practices
}


# ora2 fileupload
ORA2_FILEUPLOAD_BACKEND = "swift"
ORA2_FILEUPLOAD_CACHE_NAME = "openassessment_submissions"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "uploads"

# Profile image upload
PROFILE_IMAGE_BACKEND = {
    "class": "storages.backends.overwrite.OverwriteStorage",
    "options": {
        "location": os.path.join(MEDIA_ROOT, "profile-images/"),
        "base_url": os.path.join(MEDIA_URL, "profile-images/"),
    },
}

ENABLE_ADWAYS_FOR_COURSES = config(
    "ENABLE_ADWAYS_FOR_COURSES", default=[], formatter=json.loads
)

# Add our v3 CSS and JS files to assets compilation pipeline to make them available in courseware.
# On FUN v3 frontend, which do not use edX's templates, those files are loaded
# by funsite/templates/funsite/parts/base.html and css/lms-main.css
PIPELINE_CSS["style-vendor"]["source_filenames"].append("fun/css/cookie-banner.css")
PIPELINE_CSS["style-vendor"]["source_filenames"].append("funsite/css/header.css")
PIPELINE_CSS["style-vendor"]["source_filenames"].append("funsite/css/footer.css")

#  can't find any common group
for group in ["base_vendor", "main_vendor"]:
    PIPELINE_JS[group]["source_filenames"].append("funsite/js/header.js")
    PIPELINE_JS[group]["source_filenames"].append("fun/js/cookie-banner.js")


LTI_XBLOCK_CONFIGURATIONS = config(
    "LTI_XBLOCK_CONFIGURATIONS", default=[], formatter=json.loads
)

DEFAULT_TEMPLATE_ENGINE["DIRS"].append(FUN_BASE_ROOT / "funsite/templates/lms")
DEFAULT_TEMPLATE_ENGINE["OPTIONS"]["context_processors"].append(
    "fun.context_processor.fun_settings"
)

TEMPLATES = [DEFAULT_TEMPLATE_ENGINE]

# This force Edx Studio to use our own video provider Xblock on default button
FUN_DEFAULT_VIDEO_PLAYER = "libcast_xblock"


def prefer_fun_xmodules(identifier, entry_points):
    """
    Make sure that we use the correct FUN xmodule for video in the studio
    """
    from django.conf import settings
    from xmodule.modulestore import prefer_xmodules

    if identifier == "video" and settings.FUN_DEFAULT_VIDEO_PLAYER is not None:
        import pkg_resources
        from xblock.core import XBlock

        # These entry points are listed in the setup.py of the libcast module
        # Inspired by the XBlock.load_class method
        entry_points = list(
            pkg_resources.iter_entry_points(
                XBlock.entry_point, name=settings.FUN_DEFAULT_VIDEO_PLAYER
            )
        )
    return prefer_xmodules(identifier, entry_points)


XBLOCK_SELECT_FUNCTION = prefer_fun_xmodules


MIDDLEWARE_CLASSES += (
    "fun.middleware.LegalAcceptance",
    "backoffice.middleware.PathLimitedMasqueradeMiddleware",
)


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


ANONYMIZATION_KEY = config("ANONYMIZATION_KEY", default="")

RAVEN_CONFIG = config("RAVEN_CONFIG", default={"dsn": ""}, formatter=json.loads)

ELASTICSEARCH_INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "filter": {
                "elision": {
                    "type": "elision",
                    "articles": ["l", "m", "t", "qu", "n", "s", "j", "d"],
                }
            },
            "analyzer": {
                "custom_french_analyzer": {
                    "tokenizer": "letter",
                    "filter": [
                        "asciifolding",
                        "lowercase",
                        "french_stem",
                        "elision",
                        "stop",
                        "word_delimiter",
                    ],
                }
            },
        }
    }
}

# MKTG_URL_LINK_MAP links are named url reverses belonging to Django project
# (also see MKTG_URLS in cms.py)
MKTG_URL_LINK_MAP = config(
    "MKTG_URL_LINK_MAP", default=MKTG_URL_LINK_MAP, formatter=json.loads
)

FUN_MKTG_URLS = config("FUN_MKTG_URLS", default={}, formatter=json.loads)

# Registration form fields ('required', 'optional', 'hidden')
REGISTRATION_EXTRA_FIELDS = config(
    "REGISTRATION_EXTRA_FIELDS", default=REGISTRATION_EXTRA_FIELDS, formatter=json.loads
)

GRADES_DOWNLOAD = config(
    "GRADES_DOWNLOAD", default=GRADES_DOWNLOAD, formatter=json.loads
)
GRADES_DOWNLOAD_ROUTING_KEY = config(
    "GRADES_DOWNLOAD_ROUTING_KEY", default=GRADES_DOWNLOAD_ROUTING_KEY
)

# Default visibility of student's profile to other students
ACCOUNT_VISIBILITY_CONFIGURATION["default_visibility"] = "private"

PAID_COURSE_REGISTRATION_CURRENCY = ["EUR", u"\N{euro sign}"]

EDX_API_KEY = config("EDX_API_KEY", default="")

# A user is verified if he has an approved SoftwareSecurePhotoVerification entry
# this setting will create a dummy SoftwareSecurePhotoVerification for user in
# paybox success callback view. A this point, we think it's better to create a
# dummy one than to remove verifying process in edX
FUN_ECOMMERCE_DEBUG_NO_NOTIFICATION = config(
    "FUN_ECOMMERCE_DEBUG_NO_NOTIFICATION", default=False, formatter=bool
)

# when True this setting add a link in instructor dashbord to analytics insigt service
ANALYTICS_DASHBOARD_URL = config(
    "ANALYTICS_DASHBOARD_URL", default=False, formatter=bool
)
