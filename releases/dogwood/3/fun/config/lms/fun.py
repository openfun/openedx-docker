import imp
import os.path

from ..common import *

# Fun-apps configuration
INSTALLED_APPS += (
    "rest_framework.authtoken",
    "backoffice",
    "fun",
    "funsite",
    "fun_api",
    "fun_certificates",
    "fun_instructor",
    "contact",
    "course_dashboard",
    "courses",
    "courses_api",
    "course_pages",
    "newsfeed",
    "universities",
    "videoproviders",
    "haystack",
    "easy_thumbnails",
    "bootstrapform",
    "ckeditor",
    "raven.contrib.django.raven_compat",
    "pure_pagination",
    "payment",
    "payment_api",
    "forum_contributors",
    "selftest",
    "password_container",
    "teachers",
    "edx_gea",
)

ROOT_URLCONF = "fun.lms.urls"

# ### THIRD-PARTY SETTINGS ###
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "courses.search_indexes.ConfigurableElasticSearchEngine",
        "URL": "http://localhost:9200/",
        "INDEX_NAME": "haystack",
    }
}

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
# -- Base --
FUN_BASE_ROOT = path(os.path.dirname(imp.find_module("funsite")[1]))
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

# -- Certificates
CERTIFICATE_BASE_URL = "/attestations/"
CERTIFICATES_DIRECTORY = "/edx/var/edxapp/attestations/"
FUN_LOGO_PATH = FUN_BASE_ROOT / "funsite/static" / FUN_BIG_LOGO_RELATIVE_PATH
FUN_ATTESTATION_LOGO_PATH = (
    FUN_BASE_ROOT / "funsite/static" / "funsite/images/logos/funmoocattest.png"
)
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
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = os.path.join(SHARED_ROOT, "openassessment_submissions")
ORA2_FILEUPLOAD_CACHE_ROOT = os.path.join(
    SHARED_ROOT, "openassessment_submissions_cache"
)
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


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


ensure_directory_exists(ORA2_FILEUPLOAD_ROOT)
ensure_directory_exists(ORA2_FILEUPLOAD_CACHE_ROOT)

ENABLE_ADWAYS_FOR_COURSES = (
    "course-v1:SciencesPo+05008+session01",
    "course-v1:SciencesPo+05008ENG+session01",
    "course-v1:Paris1+16007+session01",
    "course-v1:lorraine+30003+session03",
    "course-v1:CNAM+01035+session01",
    "course-v1:unicaen+48002+session01",
    "course-v1:umontpellier+08005+session03",
    "course-v1:lorraine+30003+SPOC_2018_session_1",
    "course-v1:AgroParisTech+32002+session04",
    "course-v1:FUN+1000+session1",
    "course-v1:lorraine+30003+SPOC_1819_session_2",
    "course-v1:lorraine+30003+SPOC_1920_session_1",
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

# Video front allowed languages
SUBTITLE_SUPPORTED_LANGUAGES = "fr"

# Generic LTI configuration
LTI_XBLOCK_CONFIGURATIONS = [{"display_name": "LTI consumer"}]
