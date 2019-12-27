from glob import glob
import json
import os.path
import pkgutil

from django.utils.translation import ugettext_lazy
from django.conf import global_settings

from lms.envs.fun.utils import Configuration, prefer_fun_video

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
FAVICON_PATH = "fun/images/favicon.ico"

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
THUMBNAIL_PRESERVE_EXTENSIONS = True
THUMBNAIL_EXTENSION = "png"

# ora2 fileupload
ORA2_FILEUPLOAD_BACKEND = "swift"
ORA2_FILEUPLOAD_CACHE_NAME = "openassessment_submissions"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "uploads"
ORA2_SWIFT_KEY = config("ORA2_SWIFT_KEY", default="")
ORA2_SWIFT_URL = config("ORA2_SWIFT_URL", default="")

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

DEFAULT_TEMPLATE_ENGINE["DIRS"].append(FUN_BASE_ROOT / "funsite/templates/lms")
DEFAULT_TEMPLATE_ENGINE["OPTIONS"]["context_processors"].append(
    "fun.context_processor.fun_settings"
)

TEMPLATES = [DEFAULT_TEMPLATE_ENGINE]

# This force Edx Studio to use our own video provider Xblock on default button
FUN_DEFAULT_VIDEO_PLAYER = "libcast_xblock"

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

FUN_MKTG_URLS = config("FUN_MKTG_URLS", default={}, formatter=json.loads)

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
ECOMMERCE_NOTIFICATION_URL = config("ECOMMERCE_NOTIFICATION_URL", default=None)
PAYMENT_ADMIN = "paybox@fun-mooc.fr"

# when True this setting add a link in instructor dashbord to analytics insigt service
ANALYTICS_DASHBOARD_URL = config(
    "ANALYTICS_DASHBOARD_URL", default=False, formatter=bool
)

# Force Edx to use `libcast_xblock` as default video player
# in the studio (big green button) and if any xblock is called `video`
XBLOCK_SELECT_FUNCTION = prefer_fun_video

